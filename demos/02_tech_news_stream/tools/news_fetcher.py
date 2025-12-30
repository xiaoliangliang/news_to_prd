"""
News Fetcher Tools - 新闻获取工具模块

提供从 Hacker News API 获取新闻的功能。
"""

import requests
from typing import List, Dict, Any, Optional


# Hacker News API endpoints
HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_NEW_STORIES_URL = "https://hacker-news.firebaseio.com/v0/newstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Request timeout in seconds
REQUEST_TIMEOUT = 10


def fetch_hackernews_top(count: int = 5) -> List[Dict[str, Any]]:
    """
    获取 Hacker News 热门新闻。
    
    Args:
        count: 获取的新闻数量，默认为 5
    
    Returns:
        新闻列表，每条新闻包含 id, title, url, score 字段
        如果获取失败，返回空列表
    """
    try:
        # 获取热门故事 ID 列表
        response = requests.get(HN_TOP_STORIES_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        story_ids = response.json()[:count]
        
        # 获取每个故事的详细信息
        stories = []
        for story_id in story_ids:
            story = _fetch_story_detail(story_id)
            if story:
                stories.append(story)
        
        return stories
    
    except requests.RequestException as e:
        print(f"[news_fetcher] Error fetching top stories: {e}")
        return []
    except Exception as e:
        print(f"[news_fetcher] Unexpected error: {e}")
        return []


def fetch_hackernews_new(count: int = 5) -> List[Dict[str, Any]]:
    """
    获取 Hacker News 最新新闻。
    
    Args:
        count: 获取的新闻数量，默认为 5
    
    Returns:
        新闻列表，每条新闻包含 id, title, url, score 字段
        如果获取失败，返回空列表
    """
    try:
        response = requests.get(HN_NEW_STORIES_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        story_ids = response.json()[:count]
        
        stories = []
        for story_id in story_ids:
            story = _fetch_story_detail(story_id)
            if story:
                stories.append(story)
        
        return stories
    
    except requests.RequestException as e:
        print(f"[news_fetcher] Error fetching new stories: {e}")
        return []
    except Exception as e:
        print(f"[news_fetcher] Unexpected error: {e}")
        return []


def _fetch_story_detail(story_id: int) -> Optional[Dict[str, Any]]:
    """
    获取单个故事的详细信息。
    
    Args:
        story_id: Hacker News 故事 ID
    
    Returns:
        包含 id, title, url, score 的字典，如果获取失败返回 None
    """
    try:
        url = HN_ITEM_URL.format(story_id)
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return None
        
        # 提取需要的字段，处理可能缺失的字段
        return {
            "id": data.get("id", story_id),
            "title": data.get("title", "Untitled"),
            "url": data.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
            "score": data.get("score", 0)
        }
    
    except requests.RequestException as e:
        print(f"[news_fetcher] Error fetching story {story_id}: {e}")
        return None
    except Exception as e:
        print(f"[news_fetcher] Unexpected error for story {story_id}: {e}")
        return None


def format_story(story: Dict[str, Any]) -> str:
    """
    格式化单条新闻为消息字符串。
    
    Args:
        story: 包含 title, url, score 的新闻字典
    
    Returns:
        格式化的消息字符串
    """
    title = story.get("title", "Untitled")
    url = story.get("url", "")
    score = story.get("score", 0)
    
    return f"**{title}**\n\n{url}\n{score} points"


if __name__ == "__main__":
    # 测试代码
    print("Fetching top 3 stories from Hacker News...")
    stories = fetch_hackernews_top(count=3)
    
    for i, story in enumerate(stories, 1):
        print(f"\n--- Story {i} ---")
        print(format_story(story))
