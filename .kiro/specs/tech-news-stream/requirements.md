# Requirements Document

## Introduction

Tech News Stream 是一个多代理协作 demo，展示两种不同的代理模式协同工作：一个基于 Python 的程序化代理（WorkerAgent）负责从 Hacker News 获取科技新闻，另一个基于 YAML 配置的 LLM 代理（CollaboratorAgent）负责对新闻进行分析和评论。该 demo 演示了外部 API 集成、后台任务调度、事件驱动触发器等高级功能。

## Glossary

- **Network**: OpenAgents 网络节点，负责协调代理间通信
- **News_Hunter**: Python 程序化代理，负责定期从 Hacker News API 获取新闻并发布到频道
- **Commentator**: YAML 配置的 LLM 代理，负责对新闻进行分析评论
- **WorkerAgent**: OpenAgents 提供的程序化代理基类，支持后台任务和自定义生命周期
- **CollaboratorAgent**: OpenAgents 提供的 LLM 代理类型，通过 YAML 配置
- **Trigger**: 事件触发器，用于选择性响应特定类型的消息
- **Messaging_Mod**: OpenAgents 消息模块，提供频道消息功能
- **Hacker_News_API**: Hacker News 提供的免费公开 API

## Requirements

### Requirement 1: 网络配置

**User Story:** As a developer, I want to configure the OpenAgents network, so that agents can communicate through channels.

#### Acceptance Criteria

1. THE Network SHALL be configured with name "TechNewsStream" and centralized mode
2. THE Network SHALL expose HTTP transport on port 8050 with Studio enabled
3. THE Network SHALL expose gRPC transport on port 8060
4. THE Network SHALL configure Messaging_Mod with a "news-feed" channel for news posting and discussion

### Requirement 2: News Hunter 代理实现

**User Story:** As a user, I want a news hunter agent that automatically fetches tech news, so that I can stay updated with the latest tech stories.

#### Acceptance Criteria

1. THE News_Hunter SHALL extend WorkerAgent class and use agent_id "news-hunter"
2. WHEN News_Hunter starts, THE News_Hunter SHALL begin a background task to periodically fetch news
3. THE News_Hunter SHALL fetch top stories from Hacker_News_API every 60 seconds by default
4. WHEN News_Hunter fetches news, THE News_Hunter SHALL track posted URLs to avoid duplicate posts
5. WHEN News_Hunter has new stories, THE News_Hunter SHALL post maximum 2 stories per fetch cycle to the "news-feed" channel
6. WHEN News_Hunter posts a story, THE News_Hunter SHALL format it with title, URL, and score
7. THE News_Hunter SHALL support command-line arguments for interval, host, and port configuration
8. WHEN News_Hunter shuts down, THE News_Hunter SHALL cancel the background hunting task

### Requirement 3: News Fetcher 工具实现

**User Story:** As a developer, I want reusable news fetching tools, so that agents can access external news APIs.

#### Acceptance Criteria

1. THE fetch_hackernews_top function SHALL fetch top N stories from Hacker News API
2. THE fetch_hackernews_top function SHALL return formatted string with story title, URL, and score
3. IF Hacker_News_API request fails, THEN THE fetch_hackernews_top function SHALL handle the error gracefully and return an error message

### Requirement 4: Commentator 代理配置

**User Story:** As a user, I want a commentator agent that provides insightful analysis on tech news, so that I can understand the implications of news stories.

#### Acceptance Criteria

1. THE Commentator SHALL be configured as CollaboratorAgent with agent_id "commentator"
2. THE Commentator SHALL use triggers instead of react_to_all_messages for selective responses
3. WHEN a message is posted to "news-feed" channel, THE Commentator SHALL respond with analysis and commentary
4. THE Commentator SHALL provide different commentary styles based on news category (AI/ML, Startup, Big Tech, Security)
5. THE Commentator SHALL use emojis to indicate hot takes, analysis, predictions, and concerns
6. THE Commentator SHALL keep responses concise and insightful

### Requirement 5: 项目结构

**User Story:** As a developer, I want a well-organized project structure, so that the demo is easy to understand and maintain.

#### Acceptance Criteria

1. THE demo SHALL be located in "demos/02_tech_news_stream/" directory
2. THE demo SHALL include network.yaml for network configuration
3. THE demo SHALL include agents/ directory with news_hunter.py and commentator.yaml
4. THE demo SHALL include tools/ directory with news_fetcher.py
5. THE demo SHALL include config/agent_env/ directory for agent environment configuration
6. THE demo SHALL include logs/ directory with agents/ and llm/ subdirectories
7. THE demo SHALL include mods/ directory for messaging module files
8. THE demo SHALL include README.md with usage instructions in Chinese

### Requirement 6: 用户交互

**User Story:** As a user, I want to interact with the news stream through Studio, so that I can view news and commentary in real-time.

#### Acceptance Criteria

1. WHEN user opens Studio at http://localhost:8050, THE Network SHALL display the news-feed channel
2. WHEN user sends a message mentioning "@news-hunter", THE News_Hunter SHALL respond appropriately
3. WHEN News_Hunter posts news, THE Commentator SHALL automatically provide commentary
