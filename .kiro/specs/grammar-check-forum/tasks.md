# Implementation Plan: Grammar Check Forum Demo

## Overview

基于 OpenAgents 框架实现 Grammar Check Forum Demo，包括网络配置和 Grammar Checker 代理。实现采用增量方式，先创建基础结构，再配置网络和代理。

## Tasks

- [x] 1. 创建项目目录结构
  - 创建 demos/04_grammar_check_forum/ 目录
  - 创建 agents/、config/agent_env/、logs/agents/、logs/llm/ 子目录
  - 创建必要的 .gitkeep 文件
  - _Requirements: 5.1, 5.3, 5.4, 5.5_

- [x] 2. 实现网络配置
  - [x] 2.1 创建 network.yaml
    - 配置 GrammarCheckForum 网络名称和 centralized 模式
    - 配置 HTTP (8700) 和 gRPC (8600) 传输
    - 启用 forum mod 并配置参数
    - 设置 max_topics_per_agent: 100, max_comments_per_topic: 50
    - 启用 voting 和 search 功能
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

- [x] 3. 实现 Grammar Checker 代理
  - [x] 3.1 创建 agents/grammar_checker.yaml
    - 配置 CollaboratorAgent 类型和 agent_id "grammar-checker"
    - 启用 forum mod
    - 设置 react_to_all_messages: true
    - 编写 instruction（语法检查规则和响应格式）
    - 配置 forum.topic.created 和 forum.comment.created 触发器
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 4. Checkpoint - 验证配置文件
  - 确保所有 YAML 文件语法正确
  - 确保目录结构完整
  - 如有问题请询问用户

- [x] 5. 创建 README 文档
  - [x] 5.1 创建 README.md
    - 编写项目介绍和架构说明
    - 编写前置条件和环境变量配置
    - 编写快速开始指南（启动网络、启动代理、连接 Studio）
    - 编写使用示例（创建话题、查看语法检查结果）
    - 编写排障指南
    - _Requirements: 5.2, 5.6_

- [x] 6. 创建 mods 目录结构
  - 创建 mods/openagents.mods.workspace.forum/files/ 目录
  - 创建 grammar-checker 子目录
  - _Requirements: 5.1_

- [x] 7. Final Checkpoint - 完整性验证
  - 确保所有文件已创建
  - 确保配置正确
  - 如有问题请询问用户

## Notes

- 该 demo 不需要自定义工具，Grammar Checker 使用 LLM 内置能力进行语法检查
- 所有配置都是 YAML 文件，无需编写 Python 代码
- 测试需要手动通过 Studio UI 创建话题验证
