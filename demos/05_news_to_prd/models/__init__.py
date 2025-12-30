"""
NewstoPRD Data Models

定义流水线中使用的核心数据结构和 payload schema。
"""

from .payloads import (
    NewsPayload,
    TaskDelegatePayload,
    TaskCompletePayload,
    ResearchCompletePayload,
    InsightCompletePayload,
    PRDCompletePayload,
)

__all__ = [
    "NewsPayload",
    "TaskDelegatePayload",
    "TaskCompletePayload",
    "ResearchCompletePayload",
    "InsightCompletePayload",
    "PRDCompletePayload",
]
