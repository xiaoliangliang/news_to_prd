#!/usr/bin/env python3
"""
News Hunter Agent - 新闻猎手代理

一个基于 WorkerAgent 的程序化代理，定期从 Hacker News 获取新闻并发布到频道。
"""

import asyncio
import argparse
import sys
import os

# 添加 tools 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openagents.agents.worker_agent import WorkerAgent
from tools.news_fetcher import fetch_hackernews_top, format_story


class NewsHunterAgent(WorkerAgent):
    """
    新闻猎手代理 - 定期从 Hacker News 获取新闻并发布到频道。
    
    特性：
    - 定期从 Hacker News API 获取热门新闻
    - 去重机制避免重复发布
    - 每个周期最多发布 2 条新闻
    - 支持命令行参数配置
    """
    
    default_agent_id = "news-hunter"
    
    def __init__(self, fetch_interval: int = 300):
        """
        初始化 News Hunter 代理。
        
        Args:
            fetch_interval: 获取新闻的间隔时间（秒），默认 300 秒
        """
        super().__init__()
        self.fetch_interval = fetch_interval
        self.posted_urls = set()  # 已发布的 URL 集合，用于去重
        self._hunting_task = None
    
    async def on_startup(self):
        """代理启动时调用，开始后台新闻获取任务。"""
        print(f"[news-hunter] News Hunter connected! Starting hunt loop...")
        print(f"[news-hunter] Fetch interval: {self.fetch_interval} seconds")
        self._hunting_task = asyncio.create_task(self._hunt_news_loop())
    
    async def on_shutdown(self):
        """代理关闭时调用，取消后台任务。"""
        print("[news-hunter] Shutting down News Hunter...")
        if self._hunting_task:
            self._hunting_task.cancel()
            try:
                await self._hunting_task
            except asyncio.CancelledError:
                pass
        print("[news-hunter] News Hunter stopped.")
    
    async def _hunt_news_loop(self):
        """后台循环，定期获取并发布新闻。"""
        # 等待初始化完成
        await asyncio.sleep(5)
        
        while True:
            try:
                await self._fetch_and_post_news()
            except Exception as e:
                print(f"[news-hunter] Error in hunt loop: {e}")
            
            await asyncio.sleep(self.fetch_interval)
    
    async def _fetch_and_post_news(self):
        """获取新闻并发布新故事。"""
        print("[news-hunter] Fetching news from Hacker News...")
        
        # 获取热门新闻
        stories = fetch_hackernews_top(count=5)
        
        if not stories:
            print("[news-hunter] No stories fetched.")
            return
        
        # 过滤已发布的故事
        new_stories = [
            s for s in stories 
            if s.get("url") and s["url"] not in self.posted_urls
        ]
        
        if not new_stories:
            print("[news-hunter] No new stories to post.")
            return
        
        print(f"[news-hunter] Found {len(new_stories)} new stories.")
        
        # 每个周期最多发布 1 条新闻（默认 5 分钟一条）
        stories_to_post = new_stories[:1]
        
        for story in stories_to_post:
            await self._post_story(story)
            self.posted_urls.add(story["url"])
    
    async def _post_story(self, story: dict):
        """
        发布单条新闻到 news-feed 频道。
        
        Args:
            story: 包含 title, url, score 的新闻字典
        """
        message = format_story(story)
        
        print(f"[news-hunter] Posting: {story.get('title', 'Untitled')[:50]}...")
        
        try:
            # 使用 workspace API 发布消息
            ws = self.workspace()
            await ws.channel("news-feed").post(message)
            print(f"[news-hunter] Posted successfully!")
        except Exception as e:
            print(f"[news-hunter] Error posting story: {e}")


def parse_args():
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="News Hunter Agent - Fetches and posts tech news from Hacker News"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Fetch interval in seconds (default: 300)"
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
        default=8050,
        help="Network port (default: 8050)"
    )
    return parser.parse_args()


def main():
    """主函数，启动 News Hunter 代理。"""
    args = parse_args()
    
    print("=" * 50)
    print("News Hunter Agent")
    print("=" * 50)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Fetch Interval: {args.interval} seconds")
    print("=" * 50)
    
    # 创建代理
    agent = NewsHunterAgent(fetch_interval=args.interval)
    
    # 启动代理并连接到网络
    agent.start(network_host=args.host, network_port=args.port)
    
    # 等待代理停止
    agent.wait_for_stop()


if __name__ == "__main__":
    main()
