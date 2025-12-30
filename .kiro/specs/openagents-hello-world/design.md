# 设计文档

## 概述

本设计文档描述 OpenAgents Hello World Demo 的技术实现方案。该 demo 是一个最简单的 OpenAgents 演示，包含一个网络配置和一个 Charlie 代理，用于验证 OpenAgents 安装是否正常工作。

### 架构图

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

┌──────────────────────────────────────────────────────────────┐
│                    OpenAgents Network                         │
│                                                               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
│  │   HTTP      │     │   gRPC      │     │  Messaging  │    │
│  │  Transport  │     │  Transport  │     │    Mod      │    │
│  │  (8700)     │     │  (8600)     │     │             │    │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘    │
│         │                   │                   │            │
│         └───────────────────┴───────────────────┘            │
│                             │                                │
│                    ┌────────┴────────┐                       │
│                    │  general 频道   │                       │
│                    └─────────────────┘                       │
└──────────────────────────────────────────────────────────────┘
         ▲                                    ▲
         │ HTTP (8700)                        │ gRPC (8700)
         │                                    │
┌────────┴────────┐                  ┌────────┴────────┐
│  OpenAgents     │                  │  Charlie Agent  │
│    Studio       │                  │  (CollaboratorAgent)
│  (localhost:8050)                  │                 │
└─────────────────┘                  └─────────────────┘
```

## 组件和接口

### 1. 项目目录结构

```
demos/
└── 00_hello_world/
    ├── network.yaml          # 网络配置文件
    └── agents/
        └── charlie.yaml      # Charlie 代理配置文件
```

### 2. Network 配置 (network.yaml)

网络配置定义了 OpenAgents 网络的基本设置，包括传输协议和启用的模块。

```yaml
network:
  name: "HelloWorld"
  mode: "centralized"
  node_id: "hello-world-1"

  transports:
    - type: "http"
      config:
        port: 8700
    - type: "grpc"
      config:
        port: 8600

  mods:
    - name: "openagents.mods.workspace.messaging"
      enabled: true
      config:
        default_channels:
          - name: "general"
            description: "通用聊天频道"
```

#### 配置说明

| 字段 | 值 | 说明 |
|------|-----|------|
| name | "HelloWorld" | 网络名称 |
| mode | "centralized" | 集中式网络模式 |
| node_id | "hello-world-1" | 节点唯一标识 |
| HTTP port | 8700 | Studio 连接和网络发现 |
| gRPC port | 8600 | Agent 连接（备用） |
| messaging mod | enabled | 启用频道消息功能 |

### 3. Charlie Agent 配置 (charlie.yaml)

Charlie 是一个基于 LLM 的协作代理，配置为响应所有消息。

```yaml
type: "openagents.agents.collaborator_agent.CollaboratorAgent"
agent_id: "charlie"

config:
  model_name: "gpt-4o-mini"

  instruction: |
    你是 Charlie，一个友好的 OpenAgents demo 代理。

    你的角色：
    回复你收到的任何消息，保持友好和有帮助的态度。

    行为规则：
    - 保持温暖和欢迎的态度
    - 回复保持简洁（1-3句话）
    - 如果有人打招呼，热情地回应
    - 如果有人提问，尝试提供帮助

  react_to_all_messages: true

mods:
  - name: "openagents.mods.workspace.messaging"
    enabled: true

connection:
  host: "localhost"
  port: 8700
  transport: "grpc"
```

#### 配置说明

| 字段 | 值 | 说明 |
|------|-----|------|
| type | CollaboratorAgent | LLM 驱动的协作代理 |
| agent_id | "charlie" | 代理唯一标识 |
| model_name | "gpt-4o-mini" | 使用的 LLM 模型 |
| react_to_all_messages | true | 响应所有消息 |
| connection.host | "localhost" | 连接到本地网络 |
| connection.port | 8700 | 连接端口 |
| connection.transport | "grpc" | 使用 gRPC 协议 |

## 数据模型

### 消息流

1. 用户通过 Studio 在 `general` 频道发送消息
2. 消息通过 HTTP transport 到达 Network
3. Messaging Mod 将消息广播到频道
4. Charlie Agent 通过 gRPC 接收消息事件
5. Charlie 使用 LLM 生成响应
6. 响应通过 `send_channel_message` 工具发送回频道
7. Studio 显示 Charlie 的回复

### 事件类型

| 事件 | 说明 |
|------|------|
| channel_message | 频道消息事件，包含发送者、内容、时间戳 |

## 正确性属性

*正确性属性是指在系统所有有效执行中都应该保持为真的特征或行为。属性作为人类可读规范和机器可验证正确性保证之间的桥梁。*

由于本项目主要是配置文件的创建，大部分验收标准是关于文件结构和内容的静态验证，以及 LLM 行为的人工验收，因此可自动化测试的属性有限。

### Property 1: 配置文件结构完整性

*对于任意* 有效的项目部署，`demos/00_hello_world/network.yaml` 和 `demos/00_hello_world/agents/charlie.yaml` 文件都应该存在且可被 YAML 解析器正确解析。

**验证: 需求 1.1, 1.2, 1.3**

### Property 2: 网络配置完整性

*对于任意* 有效的 network.yaml 配置，解析后应包含：
- network.name 等于 "HelloWorld"
- network.mode 等于 "centralized"
- 至少一个 HTTP transport 配置在端口 8700
- 至少一个 gRPC transport 配置在端口 8600
- messaging mod 已启用
- 存在名为 "general" 的默认频道

**验证: 需求 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**

### Property 3: Agent 配置完整性

*对于任意* 有效的 charlie.yaml 配置，解析后应包含：
- type 等于 "openagents.agents.collaborator_agent.CollaboratorAgent"
- agent_id 等于 "charlie"
- config.model_name 存在且非空
- config.instruction 存在且非空
- config.react_to_all_messages 等于 true
- mods 中包含已启用的 messaging mod
- connection 配置指向 localhost:8700

**验证: 需求 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7**

## 错误处理

### 常见错误场景

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Agent 无响应 | API Key 未设置 | 检查 OPENAI_API_KEY 环境变量 |
| 连接失败 | 网络未启动 | 先启动网络再启动 Agent |
| 端口占用 | 其他进程占用端口 | 使用 `lsof -i :8700` 查找并终止进程 |
| 网络健康检查失败 | 网络未正常运行 | 检查网络启动日志 |

### 排障步骤

1. 检查网络健康: `curl http://localhost:8700/health`
2. 检查 API Key: `echo $OPENAI_API_KEY` (Linux/macOS) 或 `echo %OPENAI_API_KEY%` (Windows CMD)
3. 检查 Agent 终端日志中的错误信息
4. 确保没有其他 OpenAgents 网络正在运行

## 测试策略

### 单元测试

由于本项目主要是配置文件，单元测试将验证：
- YAML 文件语法正确性
- 配置字段完整性
- 配置值符合预期

### 集成测试（人工验收）

1. 启动网络: `openagents network start demos/00_hello_world/`
2. 启动 Agent: `openagents agent start demos/00_hello_world/agents/charlie.yaml`
3. 启动 Studio: `openagents studio -s`
4. 在 `general` 频道发送消息，验证 Charlie 响应

### 测试用例

| 测试 | 输入 | 预期输出 |
|------|------|----------|
| 问候测试 | "Hello!" | Charlie 友好回应问候 |
| 问题测试 | "What can you help me with?" | Charlie 尝试提供帮助 |
| 分享测试 | "I just learned about OpenAgents!" | Charlie 友好回应 |

## 运行指南

### 前置条件

```bash
# 1. 确保 Python >= 3.10
python --version

# 2. 安装 OpenAgents >= 0.7.0
pip install openagents

# 3. 设置 API Key
# Linux/macOS:
export OPENAI_API_KEY="your-key-here"
# Windows CMD:
set OPENAI_API_KEY=your-key-here
# Windows PowerShell:
$env:OPENAI_API_KEY="your-key-here"

# 可选: 设置自定义 OpenAI Base URL
export OPENAI_BASE_URL="your-base-url-here"
```

### 启动步骤

```bash
# 终端 1: 启动网络
openagents network start demos/00_hello_world/

# 终端 2: 启动 Agent
openagents agent start demos/00_hello_world/agents/charlie.yaml

# 终端 3: 启动 Studio
openagents studio -s
```

### 访问 Studio

打开浏览器访问 `http://localhost:8050`，连接到 `localhost:8700`，在 `general` 频道与 Charlie 交互。
