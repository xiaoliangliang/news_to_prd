# Requirements Document

## Introduction

NewstoPRD 是一个自动化的新闻到产品需求文档（PRD）生成系统。该系统整合了新闻获取（demo02）和调研团队（demo03）的能力，当获取到一条科技新闻时，自动触发调研流程，挖掘爆款产品选题，并最终输出一份MVP版本的PRD文档。

## Glossary

- **News_Hunter**: 新闻猎手代理，负责从Hacker News获取科技新闻
- **Research_Team**: 调研团队，包含Router、Web_Searcher和Analyst，负责对新闻进行深度调研
- **Product_Insight_Expert**: 产品Idea洞察师，负责从新闻中挖掘爆款产品选题
- **PRD_Expert**: 网站产品PRD专家，负责将产品选题转化为MVP版本的PRD
- **Hit_Product_Topic**: 爆款产品选题，包含目标用户群体、用户痛点和解决方案三要素
- **MVP_PRD**: 最小可行产品需求文档，包含产品名称、详细需求、SEO关键词和域名推荐

## Requirements

### Requirement 1: 新闻获取与触发

**User Story:** As a user, I want the system to automatically fetch tech news and trigger the PRD generation pipeline, so that I can discover product opportunities from trending news.

#### Acceptance Criteria

1. WHEN the News_Hunter fetches a new tech news article, THE System SHALL publish the news to the designated channel
2. WHEN a news article is published, THE System SHALL automatically trigger the research pipeline
3. THE News_Hunter SHALL include the news title, URL, and summary in the published message
4. WHEN the news article lacks sufficient content, THE System SHALL skip the PRD generation and log the reason
5. THE System SHALL be configurable to fetch at most 1 news item per 5 minutes by default (poll interval = 300 seconds)

### Requirement 2: 新闻调研

**User Story:** As a user, I want the system to conduct comprehensive research on the news topic, so that I have sufficient context for product ideation.

#### Acceptance Criteria

1. WHEN a news article triggers the pipeline, THE Research_Team SHALL receive the news content for investigation
2. WHEN the Router receives the news, THE Router SHALL delegate search tasks to the Web_Searcher
3. WHEN the Web_Searcher completes searches, THE Web_Searcher SHALL return findings including market trends, competitor analysis, and user discussions
4. WHEN search results are available, THE Analyst SHALL synthesize the findings into a structured research report
5. THE Research_Team SHALL complete the research within a reasonable timeframe and return results to the pipeline

### Requirement 3: 产品Idea洞察

**User Story:** As a user, I want the system to identify hit product opportunities from the news, so that I can understand what products could be built.

#### Acceptance Criteria

1. WHEN the research report is ready, THE Product_Insight_Expert SHALL analyze the news and research findings
2. THE Product_Insight_Expert SHALL identify the target user group for the potential product
3. THE Product_Insight_Expert SHALL identify the pain points that the target users currently experience
4. THE Product_Insight_Expert SHALL propose a web-based solution that addresses the identified pain points
5. WHEN the analysis is complete, THE Product_Insight_Expert SHALL output the Hit_Product_Topic containing all three elements (user group, pain points, solution)
6. IF multiple product opportunities exist, THE Product_Insight_Expert SHALL select the most promising one based on market potential

### Requirement 4: MVP PRD生成

**User Story:** As a user, I want the system to generate a complete MVP PRD document, so that I can start building the product immediately.

#### Acceptance Criteria

1. WHEN the Hit_Product_Topic is ready, THE PRD_Expert SHALL generate a complete MVP PRD document
2. THE PRD_Expert SHALL include a creative and memorable product name in the PRD
3. THE PRD_Expert SHALL include detailed functional requirements in the PRD
4. THE PRD_Expert SHALL include 5-10 SEO keywords relevant to the product
5. THE PRD_Expert SHALL recommend 3-5 domain name options for the product
6. THE PRD_Expert SHALL structure the PRD in a clear, actionable format
7. WHEN the PRD is complete, THE System SHALL publish the PRD to the designated output channel

### Requirement 5: 流水线协调

**User Story:** As a system operator, I want the pipeline to be well-coordinated, so that each stage flows smoothly to the next.

#### Acceptance Criteria

1. THE System SHALL use event-driven communication between pipeline stages
2. WHEN a stage completes, THE System SHALL automatically trigger the next stage with the appropriate payload
3. THE System SHALL maintain context throughout the pipeline (news content, research findings, product insights)
4. IF any stage fails, THE System SHALL log the error and notify the user
5. WHEN the entire pipeline completes, THE System SHALL send a summary notification to the user
6. IF the System reaches the maximum concurrent projects limit, THE System SHALL drop the incoming news-triggered pipeline run, log the reason, and notify the user (drop-on-overload strategy)

### Requirement 6: 输出格式

**User Story:** As a user, I want the PRD output to be well-formatted and comprehensive, so that I can use it directly for product development.

#### Acceptance Criteria

1. THE MVP_PRD SHALL include the following sections: Product Overview, Target Users, User Pain Points, Core Features, User Stories, SEO Strategy, and Domain Recommendations
2. THE MVP_PRD SHALL be formatted in Markdown for easy reading and sharing
3. THE MVP_PRD SHALL include a clear value proposition statement
4. THE MVP_PRD SHALL prioritize features for MVP scope (must-have vs nice-to-have)
5. WHEN generating domain recommendations, THE PRD_Expert SHALL consider availability patterns and brand memorability
