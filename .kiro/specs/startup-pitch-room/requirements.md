# Requirements Document

## Introduction

实现 OpenAgents 的 Startup Pitch Room demo，这是一个多代理聊天室，AI 代理扮演创业团队成员（创始人、工程师、投资人）讨论和辩论创业想法。该 demo 展示了多个代理如何在共享频道中协作，每个代理都有独特的个性和视角。

## Glossary

- **Network**: OpenAgents 网络节点，负责管理代理之间的通信和消息路由
- **Agent**: AI 代理，具有特定角色和个性的自主实体
- **Channel**: 消息频道，代理和用户可以在其中发送和接收消息
- **Founder_Agent**: 创始人代理，扮演有远见的创业者角色
- **Engineer_Agent**: 工程师代理，扮演技术联合创始人角色
- **Investor_Agent**: 投资人代理，扮演风险投资人角色
- **Messaging_Mod**: 消息模块，提供频道消息功能
- **Studio**: OpenAgents 的 Web UI 界面，用于与代理交互

## Requirements

### Requirement 1: 网络配置

**User Story:** As a developer, I want to configure a network for the Startup Pitch Room demo, so that multiple agents can communicate in shared channels.

#### Acceptance Criteria

1. THE Network SHALL be named "StartupPitchRoom"
2. THE Network SHALL use centralized mode
3. THE Network SHALL expose HTTP transport on port 8700 with Studio serving enabled
4. THE Network SHALL expose gRPC transport on port 8600
5. THE Network SHALL set manifest_transport to "http"
6. THE Network SHALL set recommended_transport to "grpc"
7. THE Network SHALL enable the messaging mod with default channels
8. THE Messaging_Mod default_channels SHALL include a "pitch-room" channel for startup pitch discussions
9. THE Messaging_Mod default_channels SHALL include an "ideas" channel for sharing new startup ideas

### Requirement 2: 创始人代理配置

**User Story:** As a user, I want a Founder agent that acts as a passionate visionary entrepreneur, so that I can get enthusiastic and creative responses to startup ideas.

#### Acceptance Criteria

1. THE Founder_Agent SHALL use the CollaboratorAgent type
2. THE Founder_Agent SHALL have agent_id "founder"
3. THE Founder_Agent SHALL use the configured LLM model (glm-4.7)
4. THE Founder_Agent SHALL have a personality that is enthusiastic, optimistic, and creative
5. WHEN a human sends a message, THE Founder_Agent SHALL respond with passion about solving big problems
6. WHEN another agent sends a message, THE Founder_Agent SHALL NOT respond to prevent infinite loops
7. THE Founder_Agent SHALL keep responses under 50 words
8. THE Founder_Agent SHALL connect to the network at localhost:8700 (HTTP discovery) and use the network's recommended gRPC transport (localhost:8600)

### Requirement 3: 工程师代理配置

**User Story:** As a user, I want an Engineer agent that evaluates technical feasibility, so that I can understand implementation challenges of startup ideas.

#### Acceptance Criteria

1. THE Engineer_Agent SHALL use the CollaboratorAgent type
2. THE Engineer_Agent SHALL have agent_id "engineer"
3. THE Engineer_Agent SHALL use the configured LLM model (glm-4.7)
4. THE Engineer_Agent SHALL have a personality that is analytical and detail-oriented
5. WHEN a human sends a message, THE Engineer_Agent SHALL evaluate technical feasibility and ask about implementation details
6. WHEN another agent sends a message, THE Engineer_Agent SHALL NOT respond to prevent infinite loops
7. THE Engineer_Agent SHALL keep responses under 50 words
8. THE Engineer_Agent SHALL connect to the network at localhost:8700 (HTTP discovery) and use the network's recommended gRPC transport (localhost:8600)

### Requirement 4: 投资人代理配置

**User Story:** As a user, I want an Investor agent that questions market fit and ROI, so that I can understand the business viability of startup ideas.

#### Acceptance Criteria

1. THE Investor_Agent SHALL use the CollaboratorAgent type
2. THE Investor_Agent SHALL have agent_id "investor"
3. THE Investor_Agent SHALL use the configured LLM model (glm-4.7)
4. THE Investor_Agent SHALL have a personality that is analytical and focused on returns
5. WHEN a human sends a message, THE Investor_Agent SHALL question market fit, ROI, and competitive landscape
6. WHEN another agent sends a message, THE Investor_Agent SHALL NOT respond to prevent infinite loops
7. THE Investor_Agent SHALL keep responses under 50 words
8. THE Investor_Agent SHALL connect to the network at localhost:8700 (HTTP discovery) and use the network's recommended gRPC transport (localhost:8600)

### Requirement 5: 代理响应行为

**User Story:** As a user, I want agents to respond naturally with random delays, so that the conversation feels more realistic.

#### Acceptance Criteria

1. WHEN a human message is received, THE Founder_Agent SHALL respond with a random delay between 0-3 seconds
2. WHEN a human message is received, THE Engineer_Agent SHALL respond with a random delay between 0-3 seconds
3. WHEN a human message is received, THE Investor_Agent SHALL respond with a random delay between 0-3 seconds
4. THE Agents SHALL use send_channel_message (NOT reply_channel_message) for responses

### Requirement 6: 项目文档

**User Story:** As a developer, I want clear documentation for the demo, so that I can understand how to run and use it.

#### Acceptance Criteria

1. THE Demo SHALL include a README.md file with architecture diagram
2. THE README.md SHALL include prerequisites section
3. THE README.md SHALL include environment variable configuration instructions
4. THE README.md SHALL include quick start guide with terminal commands
5. THE README.md SHALL include troubleshooting section
6. THE README.md SHALL include file structure documentation
