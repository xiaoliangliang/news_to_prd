# Requirements Document

## Introduction

实现 OpenAgents Research Team Demo - 一个基于路由器协调的多代理研究团队系统。该系统使用 project mod 进行任务管理，通过 Router 代理协调 Web Searcher 和 Analyst 代理完成研究任务。

## Glossary

- **Network**: OpenAgents 网络节点，负责管理代理连接和消息传递
- **Router**: 协调器代理，负责接收研究请求、分配任务、汇总结果
- **Web_Searcher**: 信息收集代理，负责执行网络搜索和获取信息
- **Analyst**: 分析师代理，负责分析和综合研究结果
- **Project_Mod**: 项目管理模块，提供任务管理和项目模板功能
- **Agent_Group**: 代理分组，用于权限管理和任务分配
- **Event**: 事件消息，用于代理间的任务委派和完成通知

## Requirements

### Requirement 1: 网络配置

**User Story:** 作为开发者，我想要配置一个支持项目管理的 OpenAgents 网络，以便代理可以协作完成研究任务。

#### Acceptance Criteria

1. THE Network SHALL be named "ResearchTeam" and use centralized mode
2. THE Network SHALL configure HTTP transport on port 8700 with Studio enabled
3. THE Network SHALL configure gRPC transport on port 8600
4. THE Network SHALL define two agent groups: "coordinators" and "researchers"
5. THE Network SHALL enable the "openagents.mods.workspace.default" mod with custom events
6. THE Network SHALL enable the "openagents.mods.workspace.project" mod with research task template
7. WHEN the project template is configured, THE Network SHALL include workflow context describing the research process

### Requirement 2: Router 代理

**User Story:** 作为系统协调者，我想要一个 Router 代理来接收研究请求并协调其他代理完成任务。

#### Acceptance Criteria

1. THE Router SHALL use CollaboratorAgent type with agent_id "router"
2. THE Router SHALL join the "coordinators" agent group
3. THE Router SHALL have max_iterations set to 3 to prevent duplicate actions
4. WHEN a project.notification.started event is received, THE Router SHALL delegate a search task to web-searcher using send_event
5. WHEN a task.complete event is received from web-searcher, THE Router SHALL delegate analysis to analyst
6. WHEN a task.complete event is received from analyst, THE Router SHALL compile results and complete the project
7. THE Router SHALL call finish() after each action to prevent duplicate sends

### Requirement 3: Web Searcher 代理

**User Story:** 作为信息收集者，我想要一个 Web Searcher 代理来执行网络搜索并返回相关信息。

#### Acceptance Criteria

1. THE Web_Searcher SHALL use CollaboratorAgent type with agent_id "web-searcher"
2. THE Web_Searcher SHALL join the "researchers" agent group
3. WHEN a task.delegate event is received, THE Web_Searcher SHALL execute web search based on the query
4. WHEN search is complete, THE Web_Searcher SHALL send task.complete event back to router with results
5. THE Web_Searcher SHALL have access to web search tools (search_web, fetch_webpage, search_hackernews)

### Requirement 4: Analyst 代理

**User Story:** 作为分析师，我想要一个 Analyst 代理来分析搜索结果并提供综合结论。

#### Acceptance Criteria

1. THE Analyst SHALL use CollaboratorAgent type with agent_id "analyst"
2. THE Analyst SHALL join the "researchers" agent group
3. WHEN a task.delegate event is received, THE Analyst SHALL analyze the provided information
4. WHEN analysis is complete, THE Analyst SHALL send task.complete event back to router with conclusions
5. THE Analyst SHALL provide structured analysis with key findings and recommendations

### Requirement 5: Web 搜索工具

**User Story:** 作为开发者，我想要提供网络搜索工具，以便 Web Searcher 代理可以获取互联网信息。

#### Acceptance Criteria

1. THE search_web function SHALL search using Brave API if BRAVE_API_KEY is set, otherwise fall back to DuckDuckGo
2. THE fetch_webpage function SHALL fetch and extract text content from a URL with configurable max length
3. THE search_hackernews function SHALL search Hacker News using Algolia API
4. WHEN search results are returned, THE tools SHALL format them in a readable structure

### Requirement 6: 项目目录结构

**User Story:** 作为开发者，我想要一个标准的项目目录结构，以便于管理和运行 demo。

#### Acceptance Criteria

1. THE project SHALL be located at demos/03_research_team/
2. THE project SHALL include network.yaml in the root directory
3. THE project SHALL include agents/ directory with router.yaml, web_searcher.yaml, and analyst.yaml
4. THE project SHALL include tools/ directory with web_search.py
5. THE project SHALL include config/agent_env/ directory for environment configuration
6. THE project SHALL include logs/agents/ and logs/llm/ directories for logging
7. THE project SHALL include a README.md with setup and usage instructions
