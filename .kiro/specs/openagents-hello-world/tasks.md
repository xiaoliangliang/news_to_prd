# 实现计划: OpenAgents Hello World Demo

## 概述

本实现计划将 OpenAgents Hello World Demo 的设计转化为具体的编码任务。任务按顺序执行，每个任务都建立在前一个任务的基础上。

## 任务列表

- [x] 1. 创建项目目录结构
  - 创建 `demos/00_hello_world/` 目录
  - 创建 `demos/00_hello_world/agents/` 子目录
  - _需求: 1.1, 1.2_

- [x] 2. 创建网络配置文件
  - [x] 2.1 创建 `demos/00_hello_world/network.yaml`
    - 配置网络名称为 "HelloWorld"
    - 配置网络模式为 "centralized"
    - 配置 node_id 为 "hello-world-1"
    - 配置 HTTP transport 在端口 8700
    - 配置 gRPC transport 在端口 8600
    - 启用 messaging mod
    - 配置 "general" 默认频道
    - _需求: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 3. 创建 Charlie Agent 配置文件
  - [x] 3.1 创建 `demos/00_hello_world/agents/charlie.yaml`
    - 配置代理类型为 CollaboratorAgent
    - 配置 agent_id 为 "charlie"
    - 配置 model_name 为 "gpt-4o-mini"
    - 编写友好的 instruction 提示词
    - 设置 react_to_all_messages 为 true
    - 启用 messaging mod
    - 配置连接到 localhost:8700 使用 gRPC
    - _需求: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [x] 4. 检查点 - 验证配置文件
  - 确保所有配置文件语法正确
  - 验证 YAML 格式无误
  - 如有问题请向用户确认

- [x] 5. 创建 README 文档
  - [x] 5.1 创建 `demos/00_hello_world/README.md`
    - 编写项目简介
    - 编写前置条件说明
    - 编写运行步骤
    - 编写排障指南
    - _需求: 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4_

- [x] 6. 最终检查点
  - 确保所有文件已创建
  - 验证目录结构符合设计
  - 如有问题请向用户确认

## 备注

- 本项目主要是配置文件的创建，不涉及复杂的代码编写
- 配置文件使用 YAML 格式，需确保语法正确
- 运行 demo 需要用户手动设置环境变量
- 测试需要用户手动在 Studio 中进行人工验收

## 环境变量配置（智谱 AI）

运行前需要设置以下环境变量：

**Windows CMD:**
```cmd
set OPENAI_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
set OPENAI_API_KEY=your-api-key-here
```

**Windows PowerShell:**
```powershell
$env:OPENAI_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4"
$env:OPENAI_API_KEY="your-api-key-here"
```

**Linux/macOS:**
```bash
export OPENAI_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4"
export OPENAI_API_KEY="your-api-key-here"
```

**注意:** 智谱 AI 兼容 OpenAI API 格式，model_name 可使用 "glm-4-flash" 或其他支持的模型。
