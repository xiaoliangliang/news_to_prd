# 需求文档

## 简介

本项目实现 OpenAgents 的 Hello World Demo，这是一个最简单的 OpenAgents 演示项目。该 demo 包含一个单一的 AI Agent（Charlie），它能够在聊天频道中回复任何消息。这是验证 OpenAgents 安装是否正常工作的完美起点。

## 术语表

- **Network（网络）**: OpenAgents 网络，是 Agent 之间通信的基础设施
- **Agent（代理）**: AI 代理，能够接收消息并生成响应的智能实体
- **CollaboratorAgent（协作代理）**: 基于 LLM 的协作代理类型，能够接收消息和事件并使用 LLM 生成响应
- **Messaging_Mod（消息模块）**: 提供基于频道的通信功能的模块
- **Channel（频道）**: 聊天频道，Agent 和用户可以在其中发送和接收消息
- **Studio（工作室）**: OpenAgents Studio，用于与 Agent 交互的 Web 界面，运行在端口 8050
- **YAML_Config（YAML配置）**: YAML 配置文件，用于定义 Network 和 Agent 的配置

## 需求

### 需求 1: 项目结构设置

**用户故事:** 作为开发者，我希望有一个合理的项目结构，以便我可以组织网络和代理的配置文件。

#### 验收标准

1. 项目结构 SHALL 在 `demos/00_hello_world/` 目录下包含一个 `network.yaml` 文件用于网络配置
2. 项目结构 SHALL 在 `demos/00_hello_world/agents/` 目录下存放代理配置文件
3. 项目结构 SHALL 包含 `demos/00_hello_world/agents/charlie.yaml` 文件用于 Charlie 代理的配置

### 需求 2: 网络配置

**用户故事:** 作为开发者，我希望配置 OpenAgents 网络，以便代理可以通过它连接和通信。

#### 验收标准

1. 网络配置 SHALL 定义网络名称为 "HelloWorld"
2. 网络配置 SHALL 设置网络模式为 "centralized"（集中式）
3. 网络配置 SHALL 配置 HTTP 传输在端口 8700（用于 Studio 连接和网络发现）
4. 网络配置 SHALL 配置 gRPC 传输在端口 8600（用于 Agent 连接）
5. 网络配置 SHALL 启用消息模块 (`openagents.mods.workspace.messaging`)
6. 网络配置 SHALL 定义一个名为 "general" 的默认频道，描述为 "通用聊天频道"

### 需求 3: Charlie 代理配置

**用户故事:** 作为开发者，我希望配置 Charlie 代理，以便它能够以友好的方式回复消息。

#### 验收标准

1. 代理配置 SHALL 指定代理类型为 `openagents.agents.collaborator_agent.CollaboratorAgent`
2. 代理配置 SHALL 设置 agent_id 为 "charlie"
3. 代理配置 SHALL 配置 model_name 为 "gpt-4o-mini" 或其他兼容的 OpenAI 模型
4. 代理配置 SHALL 包含定义 Charlie 友好个性和行为的指令（instruction）
5. 代理配置 SHALL 设置 `react_to_all_messages` 为 true，使 Charlie 响应每条消息
6. 代理配置 SHALL 为代理启用消息模块
7. 代理配置 SHALL 配置连接到 localhost:8700，使用 gRPC 传输（按官方 demo 配置）

### 需求 4: 代理行为规范

**用户故事:** 作为用户，我希望 Charlie 以友好和有帮助的方式回复，以便我有愉快的交互体验。

#### 验收标准（人工验收 + 提示词约束）

1. Charlie 代理的 instruction SHALL 包含角色定义：友好的 OpenAgents demo 代理
2. Charlie 代理的 instruction SHALL 包含行为规则：回复保持简洁（1-3句话）
3. Charlie 代理的 instruction SHALL 包含问候规则：收到问候时热情回应
4. Charlie 代理的 instruction SHALL 包含问答规则：收到问题时尝试提供帮助
5. 验收方式：人工在 Studio 中测试交互，确认 Charlie 按预期行为响应

### 需求 5: 运行环境要求

**用户故事:** 作为开发者，我希望有清晰的环境要求，以便我可以正确设置和运行演示。

#### 验收标准

1. 环境 SHALL 要求 Python 版本 >= 3.10
2. 环境 SHALL 要求 OpenAgents 版本 >= 0.7.0，通过 `pip install openagents` 安装
3. 环境 SHALL 要求设置 OpenAI API 密钥：
   - Linux/macOS: `export OPENAI_API_KEY="your-key-here"`
   - Windows CMD: `set OPENAI_API_KEY=your-key-here`
   - Windows PowerShell: `$env:OPENAI_API_KEY="your-key-here"`
4. WHERE 需要自定义 OpenAI 基础 URL 时，环境 SHALL 支持 `OPENAI_BASE_URL` 环境变量

### 需求 6: 运行与排障

**用户故事:** 作为开发者，我希望有清晰的运行步骤和排障指南，以便我可以顺利启动和调试演示。

#### 验收标准

1. 运行前 SHALL 确保没有其他 OpenAgents 网络正在运行（先停止已有网络）
2. 网络健康检查 SHALL 可通过 `curl http://localhost:8700/health` 验证
3. Studio SHALL 运行在 `http://localhost:8050`，连接到 `localhost:8700`
4. IF Agent 无响应，THEN 用户 SHALL 检查 API Key 配置和 Agent 终端日志
