# Implementation Plan: Tech News Stream

## Overview

基于 OpenAgents 框架实现 Tech News Stream demo，包含一个 Python 程序化代理（News Hunter）和一个 YAML 配置的 LLM 代理（Commentator）。实现将参考已有的 startup_pitch_room demo 结构。

## Tasks

- [x] 1. 创建项目目录结构
  - 创建 `demos/02_tech_news_stream/` 目录
  - 创建 `agents/`、`tools/`、`config/agent_env/`、`logs/agents/`、`logs/llm/`、`mods/openagents.mods.workspace.messaging/files/` 子目录
  - 创建必要的 `.gitkeep` 文件
  - _Requirements: 5.1, 5.3, 5.4, 5.5, 5.6, 5.7_

- [x] 2. 实现网络配置
  - [x] 2.1 创建 network.yaml 配置文件
    - 配置网络名称为 "TechNewsStream"，模式为 "centralized"
    - 配置 HTTP 传输端口 8050，启用 Studio
    - 配置 gRPC 传输端口 8060
    - 配置 messaging mod 和 "news-feed" 频道
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 5.2_

- [x] 3. 实现 News Fetcher 工具
  - [x] 3.1 创建 tools/news_fetcher.py
    - 实现 fetch_hackernews_top 函数
    - 从 Hacker News API 获取热门新闻
    - 返回格式化的新闻字符串（标题、URL、分数）
    - 实现错误处理
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ]* 3.2 编写 news_fetcher 属性测试
    - **Property 4: Fetch Function Correctness**
    - **Validates: Requirements 3.1, 3.2**

- [x] 4. 实现 News Hunter 代理
  - [x] 4.1 创建 agents/news_hunter.py
    - 继承 WorkerAgent 类
    - 实现 on_startup 启动后台任务
    - 实现 on_shutdown 取消后台任务
    - 实现 _hunt_news_loop 定时获取新闻
    - 实现 _fetch_and_post_news 获取并发布新闻
    - 实现 _post_story 发布单条新闻
    - 实现 URL 去重逻辑
    - 实现命令行参数解析（interval、host、port）
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8_

  - [ ]* 4.2 编写 URL 去重属性测试
    - **Property 1: URL Deduplication**
    - **Validates: Requirements 2.4**

  - [ ]* 4.3 编写最大发布数属性测试
    - **Property 2: Max Posts Per Cycle**
    - **Validates: Requirements 2.5**

  - [ ]* 4.4 编写故事格式属性测试
    - **Property 3: Story Format Completeness**
    - **Validates: Requirements 2.6**

- [x] 5. Checkpoint - 验证 News Hunter 功能
  - 确保所有测试通过，如有问题请询问用户

- [x] 6. 实现 Commentator 代理
  - [x] 6.1 创建 agents/commentator.yaml
    - 配置为 CollaboratorAgent 类型
    - 设置 agent_id 为 "commentator"
    - 配置 LLM 模型和 instruction
    - 设置 react_to_all_messages 为 false
    - 配置 triggers 响应 news-feed 频道消息
    - 配置 messaging mod
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 7. 创建 README 文档
  - [x] 7.1 创建 README.md
    - 编写中文使用说明
    - 包含架构图、代理角色说明
    - 包含环境变量配置说明
    - 包含快速开始步骤
    - 包含排障指南
    - _Requirements: 5.8, 6.1, 6.2, 6.3_

- [x] 8. Final Checkpoint - 完整功能验证
  - 确保所有文件创建完成
  - 确保目录结构正确
  - 如有问题请询问用户

## Notes

- 任务标记 `*` 的为可选测试任务，可跳过以加快 MVP 开发
- 每个任务都引用了具体的需求以便追溯
- Checkpoint 任务用于增量验证
- 属性测试验证通用正确性属性
- 单元测试验证具体示例和边界情况
