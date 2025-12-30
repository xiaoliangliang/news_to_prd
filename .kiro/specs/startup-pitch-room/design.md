# Design Document

## Overview

Startup Pitch Room demo 是一个多代理协作演示，展示了 OpenAgents 框架中多个 AI 代理如何在共享频道中进行角色扮演对话。该 demo 包含三个代理（创始人、工程师、投资人），它们各自具有独特的个性和视角，能够对用户提出的创业想法进行多角度讨论。

### 核心设计原则

1. **角色分离** - 每个代理有明确的角色定位和响应风格
2. **防止无限循环** - 代理只响应人类消息，不响应其他代理
3. **自然对话** - 使用随机延迟使对话更自然
4. **简洁响应** - 限制响应长度，保持对话流畅

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    StartupPitchRoom Network                  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   pitch-room channel                    │ │
│  │                                                         │ │
│  │   User: "I have a startup idea about AI for restaurants"│ │
│  │         │                                               │ │
│  │         ▼                                               │ │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │   │ founder  │  │ engineer │  │ investor │            │ │
│  │   │(visionary│  │(technical│  │  (VC     │            │ │
│  │   │  ideas)  │  │feasibility│ │perspective│           │ │
│  │   └──────────┘  └──────────┘  └──────────┘            │ │
│  │        │              │              │                 │ │
│  │        └──────────────┼──────────────┘                 │ │
│  │                       ▼                                │ │
│  │              messaging mod (channels)                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    ideas channel                        │ │
│  │         (备用频道，用于分享新创业想法)                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Transports: HTTP:8700 (Studio) | gRPC:8600                 │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Network Component

网络组件负责管理代理之间的通信。

```yaml
# network.yaml 结构
network:
  name: "StartupPitchRoom"
  mode: "centralized"
  node_id: "startup-pitch-room-1"
  
  transports:
    - type: "http"      # HTTP 传输，支持 Studio
      config:
        port: 8700
        serve_studio: true
    - type: "grpc"      # gRPC 传输，代理连接
      config:
        port: 8600

  # 代理连接时会通过 /api/health 探测网络配置，然后按 recommended_transport 选择传输层
  manifest_transport: "http"
  recommended_transport: "grpc"
  
  mods:
    - name: "openagents.mods.workspace.messaging"  # 消息模块
      enabled: true
      config:
        default_channels:
          - name: "pitch-room"
            description: "Startup pitch discussions"
          - name: "ideas"
            description: "Share new startup ideas"
```

### 2. Agent Components

每个代理使用 CollaboratorAgent 类型，具有以下通用结构：

```yaml
# 代理配置结构
type: "openagents.agents.collaborator_agent.CollaboratorAgent"
agent_id: "<unique_id>"

config:
  model_name: "glm-4.7"
  instruction: "<role_specific_instructions>"
  react_to_all_messages: true
  reaction_delay: "random(0, 3)"

mods:
  - name: "openagents.mods.workspace.messaging"

connection:
  host: "localhost"
  port: 8700  # HTTP 端口（用于 /api/health 探测与自动选择 recommended_transport）
  transport: "grpc"  # 提示性字段：实际使用的传输由 network.recommended_transport 决定
```

### 3. Agent Role Definitions

| Agent | Role | Personality | Response Focus |
|-------|------|-------------|----------------|
| founder | Visionary Entrepreneur | 热情、乐观、有创造力 | 解决大问题、发现机会 |
| engineer | Technical Co-founder | 分析性、注重细节 | 技术可行性、实现细节 |
| investor | VC Perspective | 分析性、关注回报 | 市场契合度、ROI、竞争格局 |

## Data Models

### Message Flow Model

```
Human Message → Network → All Agents (parallel)
                           │
                           ├─ founder: check sender → respond if human
                           ├─ engineer: check sender → respond if human
                           └─ investor: check sender → respond if human
```

### Agent Response Rules

```
IF sender IN ["founder", "engineer", "investor"]:
    call finish() immediately  # 不响应其他代理
ELSE:
    process message and respond with delay
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Agent Identity Uniqueness
*For any* set of agents in the network, each agent SHALL have a unique agent_id that distinguishes it from all other agents.
**Validates: Requirements 2.2, 3.2, 4.2**

### Property 2: No Agent-to-Agent Response Loop
*For any* message sent by an agent (founder, engineer, or investor), no other agent SHALL generate a response to that message.
**Validates: Requirements 2.6, 3.6, 4.6**

### Property 3: Human Message Response Guarantee
*For any* message sent by a human user, all three agents (founder, engineer, investor) SHOULD attempt to generate a response (subject to LLM/provider availability).
**Validates: Requirements 2.5, 3.5, 4.5**

### Property 4: Response Length Constraint
*For any* agent response, the response content SHALL be under 50 words.
**Validates: Requirements 2.7, 3.7, 4.7**

### Property 5: Network Channel Availability
*For any* successfully started network, the "pitch-room" and "ideas" channels SHALL be available for messaging.
**Validates: Requirements 1.6, 1.7**

## Error Handling

### Network Startup Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| Port already in use | 端口 8700/8600 被占用 | 终止占用进程或更改端口 |
| Mod not found | 消息模块未安装 | 确保 OpenAgents >= 0.7.0 |

### Agent Connection Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| Connection refused | 网络未启动 | 先启动网络 |
| Authentication failed | API Key 无效 | 检查环境变量配置 |
| Model not found | 模型名称错误 | 检查 model_name 配置 |

### Agent Response Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| Infinite loop | 代理响应其他代理 | 检查 instruction 中的过滤规则 |
| No response | 代理未连接或崩溃 | 检查代理终端日志 |

## Testing Strategy

### Manual Testing

1. **网络启动测试**
   - 启动网络，验证端口监听
   - 使用 `curl http://localhost:8700/api/health` 检查健康状态

2. **代理连接测试**
   - 逐个启动代理，验证连接日志
   - 在 Studio 中确认代理在线状态

3. **消息响应测试**
   - 在 pitch-room 频道发送创业想法
   - 验证三个代理都有响应
   - 验证代理不会相互响应

4. **角色一致性测试**
   - 验证 founder 响应体现热情和远见
   - 验证 engineer 响应关注技术可行性
   - 验证 investor 响应关注市场和回报

### Integration Testing

1. **端到端流程测试**
   - 完整启动网络和所有代理
   - 发送多条消息验证稳定性
   - 验证消息延迟在预期范围内

2. **错误恢复测试**
   - 模拟代理断开重连
   - 验证网络在代理离线时的行为
