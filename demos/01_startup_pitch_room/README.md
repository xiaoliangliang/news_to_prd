# Demo: Startup Pitch Room

多代理创业路演室 - 三个 AI 代理扮演创业团队成员（创始人、工程师、投资人），从不同角度讨论和评估创业想法。

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    StartupPitchRoom Network                  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   pitch-room 频道                       │ │
│  │                                                         │ │
│  │   用户: "I have a startup idea about AI for restaurants"│ │
│  │         │                                               │ │
│  │         ▼                                               │ │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │   │ founder  │  │ engineer │  │ investor │            │ │
│  │   │(热情远见) │  │(技术可行) │  │(投资回报) │            │ │
│  │   └──────────┘  └──────────┘  └──────────┘            │ │
│  │        │              │              │                 │ │
│  │        └──────────────┼──────────────┘                 │ │
│  │                       ▼                                │ │
│  │              messaging mod (频道消息)                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    ideas 频道                           │ │
│  │         (备用频道，用于分享新创业想法)                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  传输层: HTTP:8700 (Studio) | gRPC:8600                     │
└─────────────────────────────────────────────────────────────┘
```

## 代理角色

| 代理 | 角色 | 个性 | 关注点 |
|------|------|------|--------|
| founder | 创始人 | 热情、乐观、有创造力 | 愿景、机会、影响力 |
| engineer | 工程师 | 分析性、注重细节 | 技术可行性、实现挑战 |
| investor | 投资人 | 分析性、关注回报 | 市场契合度、ROI、竞争格局 |

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

需要打开 **4 个终端窗口**：

### 终端 1: 启动网络

```bash
openagents network start demos/01_startup_pitch_room/
```

你应该看到输出表明网络正在端口 8700 (HTTP) 和 8600 (gRPC) 上运行。

### 终端 2: 启动创始人代理

```bash
openagents agent start demos/01_startup_pitch_room/agents/founder.yaml
```

### 终端 3: 启动工程师代理

```bash
openagents agent start demos/01_startup_pitch_room/agents/engineer.yaml
```

### 终端 4: 启动投资人代理

```bash
openagents agent start demos/01_startup_pitch_room/agents/investor.yaml
```

### 访问 Studio

打开浏览器访问 `http://localhost:8700`，你将看到 OpenAgents Studio 界面。

### 开始路演

1. 在左侧选择 `pitch-room` 频道
2. 输入你的创业想法，例如：
   - "I want to build an AI-powered restaurant recommendation app"
   - "What about a platform for remote team collaboration?"
   - "Let's discuss a blockchain-based supply chain solution"
3. 观察三个代理从不同角度给出反馈！

## 排障

### 代理无响应

1. 检查网络是否运行: `curl http://localhost:8700/api/health`
2. 验证 API Key 是否设置正确
3. 检查代理终端中的错误日志
4. 确保所有三个代理都已启动

### 代理相互响应（无限循环）

如果代理开始相互响应，检查 instruction 中的过滤规则是否正确配置。代理应该只响应人类消息。

### 连接问题

```bash
# 查找占用端口的进程
# Windows:
netstat -ano | findstr :8700
netstat -ano | findstr :8600

# Linux/macOS:
lsof -i :8700
lsof -i :8600

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
demos/01_startup_pitch_room/
├── network.yaml              # 网络配置
├── agents/
│   ├── founder.yaml          # 创始人代理配置
│   ├── engineer.yaml         # 工程师代理配置
│   └── investor.yaml         # 投资人代理配置
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

### 修改代理个性

编辑 `agents/*.yaml` 文件中的 `instruction` 字段来调整代理的个性和响应风格。

### 添加新频道

编辑 `network.yaml` 中的 `default_channels` 配置来添加新的讨论频道。

### 更换 LLM 模型

修改各代理配置文件中的 `model_name` 字段，支持任何 OpenAI 兼容的模型。

## 下一步

- 尝试在 `ideas` 频道分享更多创业想法
- 修改代理个性，创建不同风格的讨论
- 添加更多代理角色（如市场专家、产品经理等）
