# Design Document: NewstoPRD

## Overview

NewstoPRD 是一个基于 OpenAgents 框架的自动化新闻到PRD生成系统。该系统整合了新闻获取能力（来自demo02）和调研团队能力（来自demo03），通过事件驱动的流水线架构，将科技新闻自动转化为可执行的MVP产品需求文档。

默认节奏（可配置）：
- **抓取频率**：每 5 分钟轮询一次（poll interval = 300s）
- **入流水线速率**：每次轮询最多进入流水线 1 条新闻（5 分钟 1 条）
- **并发策略**：当项目并发达到上限时，直接丢弃该条新闻触发（drop），记录日志并对用户可见提示（先跑通优先）

### 设计原则

1. **代码复用优先** - 最大程度复用 demo02（news_hunter.py, news_fetcher.py）和 demo03（router.yaml, web_searcher.yaml, analyst.yaml, web_search.py）的现有代码
2. **阶段可见性** - 每个关键阶段的结果都要发送到对话框供用户查看
3. **渐进式输出** - 用户可以实时看到：调研结论 → 爆款选题 → 最终PRD

### Agent角色

系统采用多Agent协作模式，包含6个核心角色：
1. **News Hunter** - 新闻猎手（Python WorkerAgent）- 复用自demo02
2. **Router** - 流水线协调器（YAML CollaboratorAgent）- 扩展自demo03
3. **Web Searcher** - 网络搜索专家（YAML CollaboratorAgent）- 复用自demo03
4. **Analyst** - 调研分析师（YAML CollaboratorAgent）- 扩展自demo03，增加对话框输出
5. **Product Insight Expert** - 产品洞察师（YAML CollaboratorAgent）- 新增，输出到对话框
6. **PRD Expert** - PRD专家（YAML CollaboratorAgent）- 新增，输出到对话框

### 用户可见输出

在流水线执行过程中，用户将在对话框中看到三个关键输出：

| 阶段 | 输出Agent | 输出内容 |
|------|----------|---------|
| 调研完成 | Analyst | 📊 **调研报告**：市场趋势、竞品分析、用户讨论、关键洞察 |
| 产品洞察 | Product Insight Expert | 💡 **爆款选题**：目标用户、用户痛点、解决方案 |
| PRD生成 | PRD Expert | 📝 **MVP PRD**：产品名称、需求文档、SEO关键词、域名推荐 |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NewstoPRD Network                                     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         prd-pipeline 频道                               │ │
│  │                                                                         │ │
│  │   ┌──────────────┐                                                     │ │
│  │   │ news-hunter  │  project.notification.started (after start_project) │ │
│  │   │   (Python)   │ ─────────────────┐                                  │ │
│  │   │ WorkerAgent  │                  │                                  │ │
│  │   └──────────────┘                  ▼                                  │ │
│  │                            ┌──────────────┐                            │ │
│  │                            │    router    │                            │ │
│  │                            │ (coordinator)│                            │ │
│  │                            └──────┬───────┘                            │ │
│  │                                   │                                    │ │
│  │              ┌────────────────────┼────────────────────┐               │ │
│  │              │ task.delegate      │ task.delegate      │               │ │
│  │              ▼                    │                    ▼               │ │
│  │   ┌──────────────┐               │         ┌──────────────┐           │ │
│  │   │ web-searcher │               │         │   analyst    │           │ │
│  │   │ (search web) │               │         │ (synthesize) │           │ │
│  │   └──────┬───────┘               │         └──────┬───────┘           │ │
│  │          │ task.complete         │                │ task.complete     │ │
│  │          └───────────────────────┼────────────────┘                   │ │
│  │                                  │                                    │ │
│  │                                  │ research.complete                  │ │
│  │                                  ▼                                    │ │
│  │                       ┌──────────────────┐                            │ │
│  │                       │ product-insight  │                            │ │
│  │                       │    (ideation)    │                            │ │
│  │                       └────────┬─────────┘                            │ │
│  │                                │ insight.complete                     │ │
│  │                                ▼                                      │ │
│  │                       ┌──────────────────┐                            │ │
│  │                       │   prd-expert     │                            │ │
│  │                       │ (generate PRD)   │                            │ │
│  │                       └────────┬─────────┘                            │ │
│  │                                │ prd.complete                         │ │
│  │                                ▼                                      │ │
│  │                       ┌──────────────────┐                            │ │
│  │                       │   Final Output   │                            │ │
│  │                       │   (MVP PRD)      │                            │ │
│  │                       └──────────────────┘                            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  传输层: HTTP:8800 (Studio) | gRPC:8900                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. News Hunter Agent (Python WorkerAgent)

继承自 demo02 的 news_hunter.py，扩展以支持流水线触发。

关键运行参数（默认，可配置）：
- `poll_interval_seconds = 300`
- `max_news_per_poll = 1`

```python
class NewsHunterAgent(WorkerAgent):
    """新闻猎手 - 获取新闻并触发PRD流水线"""
    
    default_agent_id = "news-hunter"
    
    async def _post_story(self, story: dict):
        """发布新闻并触发流水线"""
        # 发布到频道
        ws = self.workspace()
        await ws.channel("prd-pipeline").post(format_story(story))
        
        # 创建一个新项目（每条新闻一个项目），由 project mod 触发 router 的 project.notification.started
        # 并发满时：start_project 失败即 drop-on-overload（记录日志并提示用户）
        from openagents.workspace import Project

        project_goal = format_story(story)  # 建议包含 title/url/summary/news_id
        project = Project(
            goal=project_goal,
            template_id="news_to_prd",
            initiator_agent_id=self.agent_id,
            name=f"NewstoPRD: {story.get('title', '')[:40]}",
        )

        result = await ws.start_project(project)
        if not result.get("success"):
            # drop-on-overload
            return
```

## Throughput & Backpressure

### 并发上限与丢弃策略（方案一：每条新闻一个项目）

NewstoPRD 采用“每条新闻 → 自动新建一个项目（project）”的隔离策略，以保证不同新闻之间上下文不串线、产出可追踪。

为保证稳定性，**项目创建由确定性代码组件负责**（建议放在 Python WorkerAgent / 外部脚本中），并在达到 `max_concurrent_projects` 时采用“超过上限直接丢弃”的策略（先保证 demo 跑通、行为可控）：

1. News Hunter 获取到候选新闻后，先做去重（按 `news_id` 或 `url`）。
2. 当 `active_projects < max_concurrent_projects`：
   - 立即为该新闻创建一个项目，并把新闻（title/url/summary/news_id）写入项目上下文/goal。
3. 当 `active_projects >= max_concurrent_projects`：
   - 直接跳过该新闻的项目创建与后续流水线，记录日志，并向用户输出一条简短提示（例如：系统繁忙/并发已满，已跳过本条新闻）。

建议配置项：
- `max_concurrent_projects`：项目并发上限（由 project mod 控制）
- `drop_on_overload`：是否在并发满时直接丢弃（默认 true）

### 2. Router Agent (YAML CollaboratorAgent)

流水线协调器，负责协调整个PRD生成流程。

```yaml
agent_id: "router"
triggers:
  - event: "project.notification.started"
    # 项目启动，触发调研流程
  - event: "task.complete"
    # 处理调研结果，触发下一阶段
  - event: "research.complete"
    # 触发产品洞察
  - event: "insight.complete"
    # 触发PRD生成
  - event: "prd.complete"
    # 完成流水线，输出结果
```

### 3. Web Searcher Agent (YAML CollaboratorAgent)

继承自 demo03，负责网络搜索。

```yaml
agent_id: "web-searcher"
tools:
  - search_web
  - fetch_webpage
  - search_hackernews
triggers:
  - event: "task.delegate"
    # 执行搜索任务
```

### 4. Analyst Agent (YAML CollaboratorAgent)

扩展自 demo03，负责分析和综合调研结果，**并将调研报告发送到对话框**。

```yaml
agent_id: "analyst"
triggers:
  - event: "task.delegate"
    instruction: |
      分析搜索结果，生成调研报告。
      
      完成后：
      1. 使用 send_project_message 将调研报告发送到对话框
         格式：📊 **调研报告**
         - 市场趋势：...
         - 竞品分析：...
         - 用户讨论：...
         - 关键洞察：...
      2. 发送 task.complete 事件给 router
```

### 5. Product Insight Expert Agent (YAML CollaboratorAgent)

新增角色，负责挖掘爆款产品选题，**并将选题结果发送到对话框**。

```yaml
agent_id: "product-insight"
instruction: |
  你是产品Idea洞察师，专注于从新闻中挖掘爆款产品选题。
  
  你需要输出爆款选题三要素：
  1. 目标用户群体 - 这个产品面向谁？
  2. 用户痛点 - 这些用户目前有什么问题？
  3. 解决方案 - 通过什么样的Web产品来解决？

triggers:
  - event: "research.complete"
    instruction: |
      分析新闻和调研结果，输出产品选题。
      
      完成后：
      1. 使用 send_project_message 将爆款选题发送到对话框
         格式：💡 **爆款产品选题**
         
         🎯 **目标用户群体**
         [详细描述目标用户]
         
         😣 **用户痛点**
         - 痛点1
         - 痛点2
         - ...
         
         💡 **解决方案**
         [Web产品解决方案描述]
         
      2. 发送 insight.complete 事件给 prd-expert
```

### 6. PRD Expert Agent (YAML CollaboratorAgent)

新增角色，负责生成MVP PRD文档，**并将完整PRD发送到对话框**。

```yaml
agent_id: "prd-expert"
instruction: |
  你是网站产品PRD专家，负责将产品选题转化为MVP版本的PRD。
  
  PRD必须包含：
  - 产品名称（创意、易记）
  - 详细需求文档
  - SEO关键词（5-10个）
  - 域名推荐（3-5个）

triggers:
  - event: "insight.complete"
    instruction: |
      根据产品选题生成MVP PRD文档。
      
      完成后：
      1. 使用 send_project_message 将完整PRD发送到对话框
         格式：📝 **MVP产品需求文档**
         
         ## 产品名称
         [创意产品名称]
         
         ## 产品概述
         [价值主张和产品定位]
         
         ## 目标用户
         [用户画像]
         
         ## 用户痛点
         - 痛点1
         - 痛点2
         
         ## 核心功能
         ### Must-Have (MVP必备)
         - 功能1
         - 功能2
         
         ### Nice-to-Have (后续迭代)
         - 功能3
         - 功能4
         
         ## 用户故事
         - As a [用户], I want [功能], so that [价值]
         
         ## SEO策略
         **关键词**: keyword1, keyword2, ...
         
         ## 域名推荐
         1. domain1.com
         2. domain2.com
         3. domain3.com
         
      2. 发送 prd.complete 事件给 router
```

## Data Models

### NewsArticle

```python
@dataclass
class NewsArticle:
    """新闻文章数据模型"""
    news_id: str
    title: str
    url: str
    summary: str
    source: str = "hackernews"
    published_at: datetime = field(default_factory=datetime.now)
```

### ResearchReport

```python
@dataclass
class ResearchReport:
    """调研报告数据模型"""
    news_id: str
    market_trends: List[str]
    competitor_analysis: List[str]
    user_discussions: List[str]
    key_insights: List[str]
    created_at: datetime = field(default_factory=datetime.now)
```

### HitProductTopic

```python
@dataclass
class HitProductTopic:
    """爆款产品选题数据模型"""
    news_id: str
    target_users: str           # 目标用户群体
    user_pain_points: List[str] # 用户痛点列表
    solution: str               # 解决方案描述
    market_potential: str       # 市场潜力评估
    created_at: datetime = field(default_factory=datetime.now)
```

### MVPPRD

```python
@dataclass
class MVPPRD:
    """MVP PRD数据模型"""
    news_id: str
    product_name: str
    value_proposition: str
    target_users: str
    pain_points: List[str]
    core_features: List[Feature]
    user_stories: List[UserStory]
    seo_keywords: List[str]
    domain_recommendations: List[str]
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Feature:
    """功能特性"""
    name: str
    description: str
    priority: str  # "must-have" | "nice-to-have"

@dataclass
class UserStory:
    """用户故事"""
    as_a: str
    i_want: str
    so_that: str
```

### PipelineEvent

```python
@dataclass
class PipelineEvent:
    """流水线事件数据模型"""
    event_name: str
    source_id: str
    destination_id: str
    payload: dict
    timestamp: datetime = field(default_factory=datetime.now)
```

## Event Flow

### 事件类型定义

| 事件名称 | 触发者 | 接收者 | 描述 |
|---------|--------|--------|------|
| `project.notification.started` | project mod | router | 项目启动，触发流水线 |
| `task.delegate` | router | web-searcher/analyst | 委派调研任务 |
| `task.complete` | web-searcher/analyst | router | 调研任务完成 |
| `research.complete` | router | product-insight | 调研完成，触发产品洞察 |
| `insight.complete` | product-insight | prd-expert | 产品洞察完成，触发PRD生成 |
| `prd.complete` | prd-expert | router | PRD生成完成 |

### 流水线状态机

```
[IDLE] --project.notification.started--> [RESEARCHING]
[RESEARCHING] --research.complete--> [IDEATING]
[IDEATING] --insight.complete--> [GENERATING_PRD]
[GENERATING_PRD] --prd.complete--> [COMPLETED]
[COMPLETED] --> [IDLE]
```



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Project Start Triggers Pipeline

*For any* news article selected by News_Hunter for processing, when it creates a project successfully, the router SHALL receive a `project.notification.started` event for that project.

**Validates: Requirements 1.1, 1.2**

### Property 2: News Message Completeness

*For any* news article published by News_Hunter, the message SHALL contain non-empty values for title, URL, and summary fields.

**Validates: Requirements 1.3**

### Property 3: Research Delegation Flow

*For any* `project.notification.started` event received by the router, a `task.delegate` event SHALL be sent to web-searcher with the news content in the payload.

**Validates: Requirements 2.2**

### Property 4: Search Results Completeness

*For any* search task completed by web-searcher, the results payload SHALL contain market_trends, competitor_analysis, and user_discussions fields.

**Validates: Requirements 2.3**

### Property 5: Research Report Structure

*For any* search results processed by the analyst, the output research report SHALL contain key_insights as a non-empty list.

**Validates: Requirements 2.4**

### Property 6: Hit Product Topic Completeness

*For any* completed product insight analysis, the Hit_Product_Topic output SHALL contain all three elements: target_users (non-empty string), user_pain_points (non-empty list), and solution (non-empty string).

**Validates: Requirements 3.2, 3.3, 3.4, 3.5**

### Property 7: PRD Structure Completeness

*For any* generated MVP PRD, the document SHALL contain all required sections: Product Overview, Target Users, User Pain Points, Core Features, User Stories, SEO Strategy, and Domain Recommendations.

**Validates: Requirements 4.2, 4.3, 6.1**

### Property 8: SEO Keywords Count

*For any* generated MVP PRD, the seo_keywords list SHALL contain between 5 and 10 items (inclusive).

**Validates: Requirements 4.4**

### Property 9: Domain Recommendations Count

*For any* generated MVP PRD, the domain_recommendations list SHALL contain between 3 and 5 items (inclusive).

**Validates: Requirements 4.5**

### Property 10: PRD Output Delivery

*For any* completed PRD generation, the PRD content SHALL be published to the designated output channel.

**Validates: Requirements 4.7**

### Property 11: Pipeline Stage Flow

*For any* pipeline stage that completes successfully, the next stage SHALL be triggered with a payload containing the previous stage's output.

**Validates: Requirements 5.2**

### Property 12: Context Preservation

*For any* completed pipeline run, the final PRD output SHALL contain a reference to the original news_id that triggered the pipeline.

**Validates: Requirements 5.3**

### Property 13: Completion Notification

*For any* pipeline that completes all stages, a summary notification SHALL be sent to the user containing the PRD and pipeline status.

**Validates: Requirements 5.5**

### Property 14: Markdown Format Validity

*For any* generated MVP PRD, the content SHALL be valid Markdown that can be parsed without errors.

**Validates: Requirements 6.2, 6.3**

### Property 15: Feature Prioritization

*For any* MVP PRD with core_features, each feature SHALL have a priority field with value either "must-have" or "nice-to-have".

**Validates: Requirements 6.4**

### Property 16: Drop-on-Overload Behavior

*For any* news article that triggers the pipeline when `active_projects >= max_concurrent_projects`, the system SHALL skip project creation, log the reason, and notify the user.

**Validates: Requirements 5.6**

## Error Handling

### 错误类型与处理策略

| 错误类型 | 触发条件 | 处理策略 |
|---------|---------|---------|
| `NewsContentError` | 新闻内容为空或不完整 | 跳过PRD生成，记录日志 |
| `SearchTimeoutError` | 网络搜索超时 | 重试3次，失败后使用缓存结果 |
| `AnalysisError` | 分析过程失败 | 记录错误，通知用户 |
| `InsightGenerationError` | 产品洞察生成失败 | 使用默认模板，标记为需人工审核 |
| `PRDGenerationError` | PRD生成失败 | 记录错误，输出部分结果 |
| `EventDeliveryError` | 事件传递失败 | 重试机制，最终失败通知用户 |

### 错误恢复流程

```python
async def handle_stage_error(stage: str, error: Exception, context: dict):
    """处理流水线阶段错误"""
    # 1. 记录错误
    logger.error(f"Stage {stage} failed: {error}", extra=context)
    
    # 2. 尝试恢复
    if stage in RECOVERABLE_STAGES:
        retry_count = context.get("retry_count", 0)
        if retry_count < MAX_RETRIES:
            await retry_stage(stage, context, retry_count + 1)
            return
    
    # 3. 通知用户
    await notify_user_error(
        news_id=context.get("news_id"),
        stage=stage,
        error_message=str(error)
    )
    
    # 4. 标记流水线状态
    await mark_pipeline_failed(context.get("pipeline_id"), stage)
```

## Testing Strategy

### 测试框架选择

- **单元测试**: pytest
- **属性测试**: hypothesis (Python PBT库)
- **集成测试**: pytest-asyncio

### 单元测试覆盖

1. **数据模型测试**
   - NewsArticle 序列化/反序列化
   - HitProductTopic 字段验证
   - MVPPRD 结构完整性

2. **Agent 逻辑测试**
   - News Hunter 新闻获取逻辑
   - Router 事件路由逻辑
   - Product Insight Expert 选题生成逻辑
   - PRD Expert 文档生成逻辑

3. **事件处理测试**
   - 事件序列化/反序列化
   - 事件路由正确性
   - 事件负载完整性

### 属性测试配置

```python
from hypothesis import given, strategies as st, settings

# 配置：每个属性测试运行100次迭代
@settings(max_examples=100)
@given(news=st.builds(NewsArticle, ...))
def test_property_news_completeness(news):
    """
    Feature: news-to-prd, Property 2: News Message Completeness
    Validates: Requirements 1.3
    """
    message = format_news_message(news)
    assert news.title in message
    assert news.url in message
    assert news.summary in message
```

### 集成测试场景

1. **端到端流水线测试**
   - 从新闻发布到PRD输出的完整流程
   - 验证所有阶段正确触发

2. **错误恢复测试**
   - 模拟各阶段失败
   - 验证错误处理和通知

3. **并发测试**
   - 多条新闻同时触发流水线
   - 验证资源隔离和状态管理
