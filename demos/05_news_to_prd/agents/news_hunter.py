#!/usr/bin/env python3
"""
News Hunter Agent - NewstoPRD Version

A WorkerAgent-based programmatic agent that periodically fetches news from Hacker News
and creates an independent project for each news item to trigger the PRD generation pipeline.

Extended from demo02, with additions:
- Each news item creates an independent project (context isolation)
- drop-on-overload concurrency strategy
- --run-once development mode
"""

import asyncio
import argparse
import sys
import os
import uuid
from datetime import datetime

# Add tools and models directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openagents.agents.worker_agent import WorkerAgent
from tools.news_fetcher import fetch_hackernews_top, format_story


class NewsHunterAgent(WorkerAgent):
    """
    News Hunter Agent - Fetches news and creates projects to trigger PRD pipeline.
    
    Features:
    - Periodically fetches top news from Hacker News API
    - Deduplication mechanism to avoid reprocessing
    - Each news item creates an independent project (context isolation)
    - drop-on-overload: directly drops when at capacity
    - Supports --run-once development mode
    """
    
    default_agent_id = "news-hunter"
    
    def __init__(
        self,
        poll_interval_seconds: int = 300,
        max_news_per_poll: int = 1,
        run_once: bool = False,
    ):
        """
        Initialize News Hunter agent.
        
        Args:
            poll_interval_seconds: Interval for fetching news (seconds), default 300 (5 minutes)
            max_news_per_poll: Max news items to process per poll, default 1
            run_once: Whether to run only once (development mode)
        """
        super().__init__()
        self.poll_interval_seconds = poll_interval_seconds
        self.max_news_per_poll = max_news_per_poll
        self.run_once = run_once
        self.posted_urls = set()  # Set of processed URLs for deduplication
        self._hunting_task = None
    
    async def on_startup(self):
        """Called when agent starts, begins background news fetching task."""
        print(f"[news-hunter] News Hunter connected! Starting hunt loop...")
        print(f"[news-hunter] Poll interval: {self.poll_interval_seconds} seconds")
        print(f"[news-hunter] Max news per poll: {self.max_news_per_poll}")
        print(f"[news-hunter] Run once mode: {self.run_once}")
        self._hunting_task = asyncio.create_task(self._hunt_news_loop())
    
    async def on_shutdown(self):
        """Called when agent shuts down, cancels background task."""
        print("[news-hunter] Shutting down News Hunter...")
        if self._hunting_task:
            self._hunting_task.cancel()
            try:
                await self._hunting_task
            except asyncio.CancelledError:
                pass
        print("[news-hunter] News Hunter stopped.")
    
    async def _hunt_news_loop(self):
        """Background loop that periodically fetches and processes news."""
        # Wait for initialization to complete
        await asyncio.sleep(5)
        
        while True:
            try:
                await self._fetch_and_process_news()
            except Exception as e:
                print(f"[news-hunter] Error in hunt loop: {e}")
            
            # If run_once mode, exit after first poll
            if self.run_once:
                print("[news-hunter] Run-once mode: exiting after first poll")
                break
            
            await asyncio.sleep(self.poll_interval_seconds)
    
    async def _fetch_and_process_news(self):
        """Fetch news and create a project for each news item."""
        print("[news-hunter] Fetching news from Hacker News...")
        
        # Fetch top news
        stories = fetch_hackernews_top(count=5)
        
        if not stories:
            print("[news-hunter] No stories fetched.")
            return
        
        # Filter already processed stories
        new_stories = [
            s for s in stories 
            if s.get("url") and s["url"] not in self.posted_urls
        ]
        
        if not new_stories:
            print("[news-hunter] No new stories to process.")
            return
        
        print(f"[news-hunter] Found {len(new_stories)} new stories.")
        
        # Process at most max_news_per_poll items per cycle
        stories_to_process = new_stories[:self.max_news_per_poll]
        
        for story in stories_to_process:
            success = await self._create_project_for_story(story)
            if success:
                self.posted_urls.add(story["url"])
    
    async def _create_project_for_story(self, story: dict) -> bool:
        """
        Create a project for a news story to trigger the PRD pipeline.
        
        Args:
            story: Dict containing id, title, url, score
            
        Returns:
            Whether project was created successfully
        """
        import json
        import aiohttp
        
        # Generate run_id
        run_id = str(uuid.uuid4())
        
        # Build NewsPayload
        news_payload = {
            "run_id": run_id,
            "news_id": str(story.get("id", "")),
            "title": story.get("title", ""),
            "url": story.get("url", ""),
            "summary": "",  # MVP: allow empty
            "source": "hackernews",
            "published_at": datetime.now().isoformat(),
        }
        
        # Build project goal (use NEWS_JSON= prefix for router to parse)
        project_goal = f"NEWS_JSON={json.dumps(news_payload, ensure_ascii=False)}"
        
        # Build project name
        title_short = story.get("title", "Untitled")[:40]
        project_name = f"NewstoPRD: {title_short}"
        
        print(f"[news-hunter] Creating project for: {title_short}...")
        print(f"[news-hunter] run_id: {run_id}")
        
        try:
            # Use MCP protocol to call start_project tool
            async with aiohttp.ClientSession() as session:
                url = "http://localhost:8800/mcp"
                mcp_request = {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "id": 1,
                    "params": {
                        "name": "start_project",
                        "arguments": {
                            "template_id": "news_to_prd",
                            "goal": project_goal,
                            "name": project_name,
                        }
                    }
                }
                
                async with session.post(url, json=mcp_request) as resp:
                    result = await resp.json()
                    print(f"[news-hunter] MCP result: {result}")
                    
                    if resp.status == 200 and "result" in result:
                        content = result.get("result", {}).get("content", [])
                        if content and len(content) > 0:
                            text = content[0].get("text", "")
                            # Parse the response text to get project_id
                            if "success': True" in text or "'success': True" in text:
                                print(f"[news-hunter] Project created successfully!")
                                return True
                        
                    error_msg = str(result)
                    print(f"[news-hunter] Project creation failed: {error_msg}")
                    await self._notify_drop(story, error_msg)
                    return False
                
        except Exception as e:
            print(f"Error starting project: {e}")
            import traceback
            traceback.print_exc()
            print(f"[news-hunter] Error creating project: {e}")
            await self._notify_drop(story, str(e))
            return False
    
    async def _notify_drop(self, story: dict, reason: str):
        """
        Send drop notification to prd-pipeline channel.
        
        Args:
            story: The dropped news story
            reason: Reason for dropping
        """
        try:
            title = story.get("title", "Untitled")[:50]
            
            drop_message = f"[SKIPPED] {title}... - Reason: {reason}"
            
            # Use workspace API to post to channel
            ws = self.workspace()
            await ws.channel("prd-pipeline").post(drop_message)
            print(f"[news-hunter] Drop notification sent to prd-pipeline channel")
        except Exception as e:
            print(f"[news-hunter] Failed to send drop notification: {e}")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="News Hunter Agent - Fetches news and triggers PRD pipeline"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Poll interval in seconds (default: 300, i.e., 5 minutes)"
    )
    parser.add_argument(
        "--max-news",
        type=int,
        default=1,
        help="Max news per poll (default: 1)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Network host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8800,
        help="Network port (default: 8800)"
    )
    parser.add_argument(
        "--run-once",
        action="store_true",
        help="Run once and exit (development mode)"
    )
    return parser.parse_args()


def main():
    """Main function, starts News Hunter agent."""
    args = parse_args()
    
    print("=" * 50)
    print("News Hunter Agent (NewstoPRD)")
    print("=" * 50)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Poll Interval: {args.interval} seconds")
    print(f"Max News Per Poll: {args.max_news}")
    print(f"Run Once: {args.run_once}")
    print("=" * 50)
    
    # Create agent
    agent = NewsHunterAgent(
        poll_interval_seconds=args.interval,
        max_news_per_poll=args.max_news,
        run_once=args.run_once,
    )
    
    # Start agent and connect to network
    agent.start(network_host=args.host, network_port=args.port)
    
    # Wait for agent to stop
    agent.wait_for_stop()


if __name__ == "__main__":
    main()
