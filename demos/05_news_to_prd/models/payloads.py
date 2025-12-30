"""
NewstoPRD Payload Schemas

定义流水线各阶段事件的 payload 结构。
遵循 CONTRACTS.md 中定义的最小 payload schema。
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional
import json
import uuid


@dataclass
class NewsPayload:
    """
    新闻触发流水线的最小 payload。
    
    Attributes:
        run_id: 本次流水线唯一标识（UUID）
        news_id: 新闻唯一标识（来自 HackerNews）
        title: 新闻标题（必填）
        url: 新闻链接（必填）
        summary: 新闻摘要（MVP 允许为空字符串）
        source: 来源（默认 "hackernews"）
        published_at: 发布时间（ISO 8601 格式）
    """
    news_id: str
    title: str
    url: str
    summary: str = ""
    source: str = "hackernews"
    published_at: str = field(default_factory=lambda: datetime.now().isoformat())
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def to_dict(self) -> dict:
        """转换为字典。"""
        return asdict(self)
    
    def to_json(self) -> str:
        """转换为 JSON 字符串。"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def to_goal(self) -> str:
        """
        转换为 project goal 格式。
        格式: NEWS_JSON={...}
        """
        return f"NEWS_JSON={self.to_json()}"
    
    @classmethod
    def from_dict(cls, data: dict) -> "NewsPayload":
        """从字典创建实例。"""
        return cls(
            run_id=data.get("run_id", str(uuid.uuid4())),
            news_id=data.get("news_id", ""),
            title=data.get("title", ""),
            url=data.get("url", ""),
            summary=data.get("summary", ""),
            source=data.get("source", "hackernews"),
            published_at=data.get("published_at", datetime.now().isoformat()),
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> "NewsPayload":
        """从 JSON 字符串创建实例。"""
        return cls.from_dict(json.loads(json_str))
    
    @classmethod
    def from_goal(cls, goal: str) -> "NewsPayload":
        """
        从 project goal 解析。
        格式: NEWS_JSON={...}
        """
        prefix = "NEWS_JSON="
        if goal.startswith(prefix):
            json_str = goal[len(prefix):]
            return cls.from_json(json_str)
        raise ValueError(f"Invalid goal format, expected 'NEWS_JSON=...', got: {goal[:50]}...")
    
    @classmethod
    def from_story(cls, story: dict) -> "NewsPayload":
        """
        从 HackerNews story 字典创建实例。
        
        Args:
            story: 包含 id, title, url, score 等字段的字典
        """
        return cls(
            news_id=str(story.get("id", "")),
            title=story.get("title", ""),
            url=story.get("url", ""),
            summary="",  # MVP: 允许为空
            source="hackernews",
            published_at=datetime.now().isoformat(),
        )


@dataclass
class TaskDelegatePayload:
    """
    task.delegate 事件的 payload。
    
    Attributes:
        run_id: 流水线唯一标识
        task_id: 任务唯一标识
        query: 任务查询/指令
        context: 附加上下文（可选）
    """
    run_id: str
    task_id: str
    query: str
    context: Optional[dict] = None
    
    def to_dict(self) -> dict:
        """转换为字典。"""
        return asdict(self)


@dataclass
class TaskCompletePayload:
    """
    task.complete 事件的 payload。
    
    Attributes:
        run_id: 流水线唯一标识
        task_id: 任务唯一标识
        results: 任务结果
    """
    run_id: str
    task_id: str
    results: dict
    
    def to_dict(self) -> dict:
        """转换为字典。"""
        return asdict(self)


@dataclass
class ResearchReport:
    """调研报告结构。"""
    market_trends: List[str] = field(default_factory=list)
    competitor_analysis: List[str] = field(default_factory=list)
    user_discussions: List[str] = field(default_factory=list)
    key_insights: List[str] = field(default_factory=list)


@dataclass
class ResearchCompletePayload:
    """
    research.complete 事件的 payload。
    
    Attributes:
        run_id: 流水线唯一标识
        news: 原始新闻信息
        report: 调研报告
    """
    run_id: str
    news: dict
    report: ResearchReport
    
    def to_dict(self) -> dict:
        """转换为字典。"""
        return {
            "run_id": self.run_id,
            "news": self.news,
            "report": asdict(self.report),
        }


@dataclass
class HitProductTopic:
    """爆款产品选题结构。"""
    target_users: str = ""
    user_pain_points: List[str] = field(default_factory=list)
    solution: str = ""


@dataclass
class InsightCompletePayload:
    """
    insight.complete 事件的 payload。
    
    Attributes:
        run_id: 流水线唯一标识
        news: 原始新闻信息
        topic: 爆款产品选题
    """
    run_id: str
    news: dict
    topic: HitProductTopic
    
    def to_dict(self) -> dict:
        """转换为字典。"""
        return {
            "run_id": self.run_id,
            "news": self.news,
            "topic": asdict(self.topic),
        }


@dataclass
class Feature:
    """功能特性。"""
    name: str
    description: str
    priority: str  # "must-have" | "nice-to-have"


@dataclass
class UserStory:
    """用户故事。"""
    as_a: str
    i_want: str
    so_that: str


@dataclass
class MVPPRD:
    """MVP PRD 结构。"""
    product_name: str = ""
    value_proposition: str = ""
    target_users: str = ""
    pain_points: List[str] = field(default_factory=list)
    core_features: List[Feature] = field(default_factory=list)
    user_stories: List[UserStory] = field(default_factory=list)
    seo_keywords: List[str] = field(default_factory=list)
    domain_recommendations: List[str] = field(default_factory=list)


@dataclass
class PRDCompletePayload:
    """
    prd.complete 事件的 payload。
    
    Attributes:
        run_id: 流水线唯一标识
        news: 原始新闻信息
        prd: MVP PRD 文档
    """
    run_id: str
    news: dict
    prd: MVPPRD
    
    def to_dict(self) -> dict:
        """转换为字典。"""
        return {
            "run_id": self.run_id,
            "news": self.news,
            "prd": {
                "product_name": self.prd.product_name,
                "value_proposition": self.prd.value_proposition,
                "target_users": self.prd.target_users,
                "pain_points": self.prd.pain_points,
                "core_features": [asdict(f) for f in self.prd.core_features],
                "user_stories": [asdict(s) for s in self.prd.user_stories],
                "seo_keywords": self.prd.seo_keywords,
                "domain_recommendations": self.prd.domain_recommendations,
            },
        }
