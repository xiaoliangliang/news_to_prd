# Demo: Tech News Stream

科技新闻流 - 展示两种不同代理模式协作的 demo：一个 Python 程序化代理（WorkerAgent）从 Hacker News 获取新闻，另一个 YAML 配置的 LLM 代理（CollaboratorAgent）提供新闻评论和分析。

## 架构

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

## 代理角色

| 代理 | 类型 | 角色 | 能力 |
|------|------|------|------|
| news-hunter | Python (WorkerAgent) | 新闻猎手 | 定期从 Hacker News 获取热门新闻 |
| commentator | YAML (CollaboratorAgent) | 评论员 | 对新闻提供分析和评论 |

## 学习要点

- 创建基于 Python 的程序化代理（WorkerAgent）
- 使用自定义工具访问外部 API
- 结合程序化代理和 LLM 代理
- 使用事件驱动触发器进行选择性响应

## 前置条件

- Python >= 3.10
- OpenAgents >= 0.7.0 (`pip install openagents`)
- 智谱 AI API Key（或其他 OpenAI 兼容的 API）

**注意：** news-hunter 使用免费的 Hacker News API，无需额外的 API Key！

## 环境变量配置

### Windows CMD
```cmd
set OPENAI_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
set OPENAI_API_KEY=your-api-key-here
```

### Windows PowerShell
```powershell
$env:OPENAI_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4"
$env:OPENAI_API_KEY="your-api-key-here"
```

### Linux/macOS
```bash
export OPENAI_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4"
export OPENAI_API_KEY="your-api-key-here"
```

## 快速开始

需要打开 **3 个终端窗口**：

### 终端 1: 启动网络

```bash
openagents network start demos/02_tech_news_stream/
```

你应该看到输出表明网络正在端口 8050 (HTTP) 和 8060 (gRPC) 上运行。

### 终端 2: 启动 News Hunter (Python 代理)

```bash
python demos/02_tech_news_stream/agents/news_hunter.py
```

或使用自定义设置：

```bash
python demos/02_tech_news_stream/agents/news_hunter.py --interval 120 --host localhost --port 8050
```

### 终端 3: 启动 Commentator

```bash
openagents agent start demos/02_tech_news_stream/agents/commentator.yaml
```

### 访问 Studio

打开浏览器访问 `http://localhost:8050`，你将看到 OpenAgents Studio 界面。

## 使用方法

news-hunter 默认每 300 秒轮询一次，并且每次最多发布 1 条新闻（即 5 分钟 1 条）。你也可以手动交互：

在 `news-feed` 频道发送消息：

> "@news-hunter 最新的 AI 新闻是什么？"

commentator 会对新闻帖子进行分析，例如：

> "🔥 Hot Take: 这在基准测试上看起来很impressive，但真正的考验是开发者是否真的会切换。AI 的护城河不仅仅是能力——还有生态系统和可靠性。"

## Python 代理深入解析

### WorkerAgent 模式

与 YAML 配置的代理不同，news-hunter 是一个**程序化 Python 代理**，继承自 `WorkerAgent`：

```python
from openagents.agents.worker_agent import WorkerAgent

class NewsHunterAgent(WorkerAgent):
    """持续获取并发布科技新闻的新闻猎手。"""

    default_agent_id = "news-hunter"

    def __init__(self, fetch_interval: int = 300, **kwargs):
        super().__init__(**kwargs)
        self.fetch_interval = fetch_interval
        self.posted_urls = set()  # 跟踪已发布的 URL 避免重复
        self._hunting_task = None

    async def on_startup(self):
        """代理连接到网络时调用。"""
        self._hunting_task = asyncio.create_task(self._hunt_news_loop())

    async def on_shutdown(self):
        """代理关闭时调用。"""
        if self._hunting_task:
            self._hunting_task.cancel()
```

### 何时使用 Python 代理

使用基于 Python 的 `WorkerAgent` 当你需要：

- **后台任务**: 定期轮询、计划任务
- **自定义生命周期**: 启动/关闭钩子
- **外部集成**: API 客户端、数据库连接
- **状态管理**: 跟踪历史、管理队列
- **非 LLM 逻辑**: 无需 AI 的确定性行为

使用基于 YAML 的 `CollaboratorAgent` 当你需要：

- **LLM 驱动的响应**: 自然语言理解
- **快速迭代**: 通过编辑提示词改变行为
- **简单事件处理**: 用 AI 响应消息

## 触发器 vs react_to_all_messages

| 方式 | 使用场景 |
|------|----------|
| `react_to_all_messages: true` | 简单机器人、问候代理 |
| `triggers` 配合事件过滤 | 选择性响应、复杂逻辑 |

## 排障

### News Hunter 不发布新闻

1. 检查 Python 代理是否运行：查找 "News Hunter connected!" 消息
2. 验证网络连接：`curl http://localhost:8050/api/health`
3. 检查 Python 终端中的错误日志

### Commentator 不响应

1. 验证它已连接到网络
2. 检查消息是否在 `news-feed` 频道（不是 `general`）
3. 确保触发器事件与消息类型匹配

### 连接问题

```bash
# 查找占用端口的进程
# Windows:
netstat -ano | findstr :8050
netstat -ano | findstr :8060

# Linux/macOS:
lsof -i :8050
lsof -i :8060

# 如需终止进程
# Windows: taskkill /PID <PID> /F
# Linux/macOS: kill -9 <PID>
```

### 模型调用失败

1. 确认 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY` 环境变量已设置
2. 检查 API Key 是否有效
3. 确认模型名称 `glm-4.7` 是否正确（或根据你的 API 提供商调整）

## 文件结构

```
demos/02_tech_news_stream/
├── network.yaml              # 网络配置
├── agents/
│   ├── news_hunter.py        # Python 新闻猎手代理
│   └── commentator.yaml      # YAML 评论员代理配置
├── tools/
│   ├── __init__.py           # 工具包初始化
│   └── news_fetcher.py       # 新闻获取工具
├── config/
│   └── agent_env/            # 代理环境配置
├── logs/
│   ├── agents/               # 代理日志
│   └── llm/                  # LLM 调用日志
├── mods/
│   └── openagents.mods.workspace.messaging/
│       └── files/            # 消息模块文件
└── README.md                 # 本文档
```

## 自定义

### 修改获取间隔

```bash
python demos/02_tech_news_stream/agents/news_hunter.py --interval 120
```

### 添加更多新闻源

扩展 `tools/news_fetcher.py`：

```python
def fetch_reddit_tech(subreddit: str = "technology", count: int = 5) -> str:
    """从 Reddit 技术子版块获取新闻。"""
    # 实现代码
```

### 修改评论风格

编辑 `agents/commentator.yaml` 中的 `instruction` 字段来调整评论员的个性和响应风格。

## 下一步

- 尝试添加更多新闻源（Reddit、TechCrunch 等）
- 创建一个总结代理，每小时总结当天的新闻
- 添加情感分析功能
