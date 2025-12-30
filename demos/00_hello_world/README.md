# Demo: Hello World

最简单的 OpenAgents 演示 - 一个在聊天频道中回复任何消息的单一代理。这是验证安装是否正常工作的完美起点。

## 架构

```
┌─────────────────────────────────────────────────┐
│              general 频道                        │
│                                                  │
│    用户: "Hello!"                               │
│         │                                        │
│         ▼                                        │
│    ┌─────────┐                                  │
│    │ charlie │  "Hello! Welcome to OpenAgents!" │
│    └─────────┘                                  │
│                                                  │
│         messaging mod                            │
└─────────────────────────────────────────────────┘
```

## 前置条件

- Python >= 3.10
- OpenAgents >= 0.7.0 (`pip install openagents`)
- 智谱 AI API Key（或其他 OpenAI 兼容的 API）

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

### 终端 1: 启动网络

```bash
openagents network start demos/00_hello_world/
```

你应该看到输出表明网络正在端口 8700 (HTTP) 和 8600 (gRPC) 上运行。

### 终端 2: 启动代理

```bash
openagents agent start demos/00_hello_world/agents/charlie.yaml
```

### 终端 3: 连接 Studio

```bash
openagents studio -s
```

打开浏览器访问 `http://localhost:8050`，连接到 `localhost:8700`。

### 与 Charlie 聊天

在 `general` 频道中，尝试打招呼或向 Charlie 提问！你应该看到 Charlie 回复你的消息。

## 排障

### 代理无响应

1. 检查网络是否运行: `curl http://localhost:8700/health`
2. 验证 API Key: `echo %OPENAI_API_KEY%` (Windows) 或 `echo $OPENAI_API_KEY` (Linux/macOS)
3. 检查代理终端中的错误日志

### 连接问题

```bash
# 查找占用端口的进程
# Windows:
netstat -ano | findstr :8700

# Linux/macOS:
lsof -i :8700

# 如需终止进程
# Windows: taskkill /PID <PID> /F
# Linux/macOS: kill -9 <PID>
```

## 文件结构

```
demos/00_hello_world/
├── network.yaml          # 网络配置
├── agents/
│   └── charlie.yaml      # Charlie 代理配置
└── README.md             # 本文档
```

## 下一步

现在你已经验证了基础功能，可以尝试更有趣的演示：

- **Startup Pitch Room** - 多个代理扮演创业团队成员
- **Tech News Stream** - 代理获取和讨论真实新闻
