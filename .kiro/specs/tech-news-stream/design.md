# Design Document: Tech News Stream

## Overview

Tech News Stream demo 展示了 OpenAgents 框架中两种不同代理模式的协作：
- **WorkerAgent (Python)**: 程序化代理，用于后台任务和外部 API 集成
- **CollaboratorAgent (YAML)**: LLM 代理，用于自然语言理解和响应

该设计遵循 OpenAgents 的标准架构模式，参考已有的 startup_pitch_room demo 结构。

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  TechNewsStream Network                      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   news-feed 频道                        │ │
│  │                                                         │ │
│  │   ┌──────────────┐         ┌──────────────┐           │ │
│  │   │ news-hunter  │  post   │ commentator  │           │ │
│  │   │   (Python)   │ ──────► │    (YAML)    │           │ │
│  │   │              │         │              │           │ │
│  │   │ WorkerAgent  │         │Collaborator  │           │ │
│  │   │ + 定时任务    │         │Agent+Trigger │           │ │
│  │   └──────────────┘         └──────────────┘           │ │
│  │         │                         │                    │ │
│  │         │    Hacker News API      │                    │ │
│  │         ▼                         ▼                    │ │
│  │   ┌──────────────┐         ┌──────────────┐           │ │
│  │   │news_fetcher  │         │   LLM API    │           │ │
│  │   │   tools      │         │  (分析评论)   │           │ │
│  │   └──────────────┘         └──────────────┘           │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  传输层: HTTP:8050 (Studio) | gRPC:8060                     │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Network Configuration (network.yaml)

网络配置定义了代理通信的基础设施：

```yaml
network:
  name: "TechNewsStream"
  mode: "centralized"
  node_id: "tech-news-stream-1"

  transports:
    - type: "http"
      config:
        port: 8050
        serve_studio: true
    - type: "grpc"
      config:
        port: 8060

  manifest_transport: "http"
  recommended_transport: "grpc"

  mods:
    - name: "openagents.mods.workspace.messaging"
      enabled: true
      config:
        default_channels:
          - name: "news-feed"
            description: "Tech news and commentary"
```

### 2. News Hunter Agent (Python WorkerAgent)

News Hunter 是一个程序化代理，继承自 `WorkerAgent`：

```python
class NewsHunterAgent(WorkerAgent):
    """
    职责：
    - 定期从 Hacker News API 获取新闻
    - 去重并发布新闻到 news-feed 频道
    - 管理后台任务生命周期
    """
    
    # 接口
    async def on_startup(self) -> None
    async def on_shutdown(self) -> None
    async def _hunt_news_loop(self) -> None
    async def _fetch_and_post_news(self) -> None
    async def _post_story(self, story: dict) -> None
```

### 3. News Fetcher Tools (tools/news_fetcher.py)

独立的工具模块，提供新闻获取功能：

```python
def fetch_hackernews_top(count: int = 5) -> str:
    """
    获取 Hacker News 热门新闻
    
    Args:
        count: 获取的新闻数量
    
    Returns:
        格式化的新闻字符串，包含标题、URL、分数
    """
```

### 4. Commentator Agent (YAML CollaboratorAgent)

Commentator 使用 YAML 配置，通过触发器响应新闻：

```yaml
type: "openagents.agents.collaborator_agent.CollaboratorAgent"
agent_id: "commentator"

config:
  model_name: "glm-4.7"
  instruction: "..."
  react_to_all_messages: false
  triggers:
    - event: "thread.channel_message.notification"
      instruction: "..."
```

## Data Models

### Story Data Structure

```python
@dataclass
class Story:
    title: str      # 新闻标题
    url: str        # 新闻链接
    score: int      # Hacker News 分数
    id: int         # Hacker News story ID
```

### Message Format

News Hunter 发布的消息格式：
```
**{title}**

{url}
{score} points
```

### Hacker News API Response

Top Stories API: `https://hacker-news.firebaseio.com/v0/topstories.json`
- 返回: `[story_id_1, story_id_2, ...]`

Story Detail API: `https://hacker-news.firebaseio.com/v0/item/{id}.json`
- 返回: `{"id": int, "title": str, "url": str, "score": int, ...}`



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: URL Deduplication

*For any* sequence of news fetches, if a story URL has been posted in a previous cycle, that URL SHALL NOT be posted again in subsequent cycles.

**Validates: Requirements 2.4**

### Property 2: Max Posts Per Cycle

*For any* fetch cycle that returns N new (unposted) stories where N > 0, the number of stories actually posted SHALL be min(N, 2).

**Validates: Requirements 2.5**

### Property 3: Story Format Completeness

*For any* story with title T, URL U, and score S, the formatted message SHALL contain all three values: T, U, and S.

**Validates: Requirements 2.6**

### Property 4: Fetch Function Correctness

*For any* valid Hacker News API response with K stories, the fetch_hackernews_top(count=N) function SHALL return exactly min(N, K) stories, each containing title, URL, and score.

**Validates: Requirements 3.1, 3.2**

## Error Handling

### Network Errors

- **Hacker News API 不可用**: fetch_hackernews_top 应捕获 requests 异常并返回错误消息
- **网络连接失败**: 代理应记录错误并在下一个周期重试
- **超时**: 设置合理的请求超时（如 10 秒）

### Agent Lifecycle Errors

- **启动失败**: 记录错误并退出
- **后台任务异常**: 捕获异常，记录日志，继续运行
- **关闭时任务取消**: 优雅地取消 asyncio 任务

### Data Validation

- **无效的 API 响应**: 跳过格式不正确的故事
- **缺失字段**: 使用默认值或跳过该故事

## Testing Strategy

### Unit Tests

单元测试用于验证具体示例和边界情况：

1. **news_fetcher.py 测试**
   - 测试 fetch_hackernews_top 返回正确数量的故事
   - 测试 API 错误处理
   - 测试空响应处理

2. **news_hunter.py 测试**
   - 测试故事格式化
   - 测试 URL 去重逻辑
   - 测试命令行参数解析

### Property-Based Tests

使用 `hypothesis` 库进行属性测试，每个属性测试运行至少 100 次迭代：

1. **Property 1 测试**: 生成随机 URL 序列，验证去重行为
2. **Property 2 测试**: 生成随机数量的新故事，验证最大发布数限制
3. **Property 3 测试**: 生成随机故事数据，验证格式完整性
4. **Property 4 测试**: 模拟 API 响应，验证获取函数正确性

### Integration Tests

集成测试验证代理间协作：

1. 启动网络和代理
2. 验证 News Hunter 能够发布消息
3. 验证 Commentator 能够响应消息

### Test Configuration

```python
# pytest.ini 或 conftest.py
from hypothesis import settings

settings.register_profile("ci", max_examples=100)
settings.load_profile("ci")
```

测试标注格式：
```python
# Feature: tech-news-stream, Property 1: URL Deduplication
@given(urls=st.lists(st.text(min_size=1)))
def test_url_deduplication(urls):
    ...
```
