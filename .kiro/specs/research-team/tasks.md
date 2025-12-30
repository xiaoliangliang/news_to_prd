# Implementation Plan: Research Team Demo

## Overview

基于 OpenAgents 框架实现 Research Team Demo，包括网络配置、三个代理（Router、Web Searcher、Analyst）和 Web 搜索工具。实现采用增量方式，先创建基础结构，再逐步完善各组件。

## Tasks

- [x] 1. 创建项目目录结构
  - 创建 demos/03_research_team/ 目录
  - 创建 agents/、tools/、config/agent_env/、logs/agents/、logs/llm/ 子目录
  - 创建必要的 .gitkeep 文件
  - _Requirements: 6.1, 6.3, 6.4, 6.5, 6.6_

- [x] 2. 实现网络配置
  - [x] 2.1 创建 network.yaml
    - 配置 ResearchTeam 网络名称和 centralized 模式
    - 配置 HTTP (8700) 和 gRPC (8600) 传输
    - 定义 coordinators 和 researchers 代理组
    - 启用 default mod 和 project mod
    - 配置 research_task 项目模板
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

- [x] 3. 实现 Web 搜索工具
  - [x] 3.1 创建 tools/web_search.py
    - 实现 search_web 函数（支持 Brave API 和 DuckDuckGo 回退）
    - 实现 fetch_webpage 函数
    - 实现 search_hackernews 函数
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ]* 3.2 编写 web_search.py 的属性测试
    - **Property 7: Webpage content truncation**
    - **Validates: Requirements 5.2**

- [x] 4. 实现 Router 代理
  - [x] 4.1 创建 agents/router.yaml
    - 配置 CollaboratorAgent 类型和 agent_id
    - 配置 coordinators 代理组
    - 设置 max_iterations: 3
    - 编写 instruction 和 triggers
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [x] 5. 实现 Web Searcher 代理
  - [x] 5.1 创建 agents/web_searcher.yaml
    - 配置 CollaboratorAgent 类型和 agent_id
    - 配置 researchers 代理组
    - 配置 tools 引用
    - 编写 instruction 和 triggers
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 6. 实现 Analyst 代理
  - [x] 6.1 创建 agents/analyst.yaml
    - 配置 CollaboratorAgent 类型和 agent_id
    - 配置 researchers 代理组
    - 编写 instruction 和 triggers
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 7. Checkpoint - 验证配置文件
  - 确保所有 YAML 文件语法正确
  - 确保目录结构完整
  - 如有问题请询问用户

- [x] 8. 创建 README 文档
  - [x] 8.1 创建 README.md
    - 编写项目介绍和架构说明
    - 编写前置条件和环境变量配置
    - 编写快速开始指南
    - 编写排障指南
    - _Requirements: 6.7_

- [x] 9. 创建 tools/__init__.py
  - 创建空的 __init__.py 文件使 tools 成为 Python 包
  - _Requirements: 6.4_

- [x] 10. Final Checkpoint - 完整性验证
  - 确保所有文件已创建
  - 确保配置正确
  - 如有问题请询问用户

## Notes

- 任务标记 `*` 的为可选任务，可跳过以加快 MVP 开发
- 每个任务都引用了具体的需求以便追溯
- Checkpoint 任务用于增量验证
- 属性测试验证通用正确性属性
