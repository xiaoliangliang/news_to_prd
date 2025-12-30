# Requirements Document

## Introduction

实现 OpenAgents Grammar Check Forum Demo - 一个基于论坛模块的语法检查系统。该系统使用 forum mod 提供话题讨论功能，通过 Grammar Checker 代理自动监控论坛帖子并回复语法纠正建议。

## Glossary

- **Network**: OpenAgents 网络节点，负责管理代理连接和消息传递
- **Grammar_Checker**: 语法检查代理，负责监控论坛帖子并提供语法纠正
- **Forum_Mod**: 论坛模块，提供话题创建、评论、投票和搜索功能
- **Topic**: 论坛话题，包含标题和内容
- **Comment**: 话题下的评论/回复
- **Event**: 事件消息，用于触发代理响应（如 forum.topic.created）

## Requirements

### Requirement 1: 网络配置

**User Story:** 作为开发者，我想要配置一个支持论坛功能的 OpenAgents 网络，以便代理可以监控和回复论坛帖子。

#### Acceptance Criteria

1. THE Network SHALL be named "GrammarCheckForum" and use centralized mode
2. THE Network SHALL configure HTTP transport on port 8700 with Studio enabled
3. THE Network SHALL configure gRPC transport on port 8600
4. THE Network SHALL enable the "openagents.mods.workspace.forum" mod with appropriate configuration
5. WHEN the forum mod is configured, THE Network SHALL set max_topics_per_agent to 100
6. WHEN the forum mod is configured, THE Network SHALL set max_comments_per_topic to 50
7. WHEN the forum mod is configured, THE Network SHALL enable voting and search features

### Requirement 2: Grammar Checker 代理

**User Story:** 作为论坛用户，我想要一个自动语法检查代理来审查我的帖子并提供纠正建议。

#### Acceptance Criteria

1. THE Grammar_Checker SHALL use CollaboratorAgent type with agent_id "grammar-checker"
2. THE Grammar_Checker SHALL enable the forum mod
3. THE Grammar_Checker SHALL set react_to_all_messages to false and only respond via explicit event triggers
4. WHEN a forum.topic.created event is received, THE Grammar_Checker SHALL analyze the topic title/content for grammar issues
5. WHEN a forum.comment.posted or forum.comment.replied event is received, THE Grammar_Checker SHALL analyze the comment content for grammar issues
6. WHEN grammar issues are found, THE Grammar_Checker SHALL reply with corrections in a structured format
7. WHEN no grammar issues are found, THE Grammar_Checker SHALL provide positive feedback

### Requirement 3: 语法检查功能

**User Story:** 作为用户，我想要获得全面的语法检查，包括各种类型的错误和改进建议。

#### Acceptance Criteria

1. THE Grammar_Checker SHALL check for grammar errors including subject-verb agreement, tense, and articles
2. THE Grammar_Checker SHALL check for spelling mistakes including typos and commonly confused words
3. THE Grammar_Checker SHALL check for punctuation errors including commas, periods, and apostrophes
4. THE Grammar_Checker SHALL check for sentence structure issues including run-ons and fragments
5. THE Grammar_Checker SHALL suggest better word choices for clarity improvements
6. THE Grammar_Checker SHALL provide style suggestions including conciseness and active voice

### Requirement 4: 响应格式

**User Story:** 作为用户，我想要收到清晰、结构化的语法检查结果，以便我能轻松理解和应用纠正。

#### Acceptance Criteria

1. WHEN responding to grammar issues, THE Grammar_Checker SHALL use a structured format with emoji markers
2. THE response SHALL include a "Grammar Check Results" header
3. THE response SHALL list each issue with original text, corrected text, and explanation
4. THE response SHALL provide a complete corrected version of the text
5. THE response SHALL include relevant writing tips
6. THE Grammar_Checker SHALL maintain a helpful and encouraging tone

### Requirement 5: 项目目录结构

**User Story:** 作为开发者，我想要一个标准的项目目录结构，以便于管理和运行 demo。

#### Acceptance Criteria

1. THE project SHALL be located at demos/04_grammar_check_forum/
2. THE project SHALL include network.yaml in the root directory
3. THE project SHALL include agents/ directory with grammar_checker.yaml
4. THE project SHALL include config/agent_env/ directory for environment configuration
5. THE project SHALL include logs/agents/ and logs/llm/ directories for logging
6. THE project SHALL include a README.md with setup and usage instructions
