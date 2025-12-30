"""
NewstoPRD Tools Package

提供新闻获取和网络搜索工具。
"""

from .news_fetcher import (
    fetch_hackernews_top,
    fetch_hackernews_new,
    format_story,
)

from .web_search import (
    search_web,
    fetch_webpage,
    search_hackernews,
)

__all__ = [
    "fetch_hackernews_top",
    "fetch_hackernews_new",
    "format_story",
    "search_web",
    "fetch_webpage",
    "search_hackernews",
]
