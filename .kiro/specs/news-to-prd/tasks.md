# Implementation Plan: NewstoPRD

## Overview

基于 demo02（新闻获取）和 demo03（调研团队）的现有代码，构建一个“每条新闻 → 自动生成 MVP PRD”的流水线 demo。优先跑通端到端闭环（MVP），再补测试与鲁棒性。

本计划采用 **项目模式（project mod）**：每条新闻自动创建一个 project，确保上下文隔离、可追踪；并发满时采用 **drop-on-overload（直接丢弃并提示）**，先保证跑通和行为可控。

## Tasks

- [x] 0. 对齐关键决策与契约（开工前必须统一）
  - 明确：每条新闻创建 1 个 project（不复用同一个长项目）
  - 明确：并发策略 = drop-on-overload（不排队等待）
  - 定义最小 payload schema（建议）：
    - `run_id`（本次流水线唯一标识）
    - `news_id/title/url/summary/source/published_at`
  - 明确 `summary` 的来源与兜底：
    - MVP：允许为空字符串（后续由 analyst / prd-expert 在内容里补充）
    - 增强：抓取网页正文后生成 1-3 句摘要（可后置）
  - 统一入口事件：project 模式下入口用 `project.notification.started`（复用 demo03 的 project 生命周期）
  - _Requirements: 1.2, 5.1, 5.2, 5.3, 5.6_

- [x] 1. 创建项目结构和网络配置（NewstoPRD 独立 demo）
  - 创建 `demos/05_news_to_prd/` 目录结构
  - 复制并修改 demo03 的 `network.yaml` 作为基础
  - 配置端口：HTTP:8800, gRPC:8900
  - 启用 mods：
    - `openagents.mods.workspace.project`
    - `openagents.mods.workspace.default`（custom events enabled）
    - `openagents.mods.workspace.messaging`（用于 drop 通知 / 运行态提示）
  - 设置 `max_concurrent_projects`（MVP 建议 2~3，便于观察 drop 行为）
  - 配置默认频道（建议至少 1 个）：
    - `prd-pipeline`：运行态提示（drop / 关键阶段里程碑）
  - 新增 project template：`news_to_prd`
    - `agent_groups` 需包含流水线所有参与 agent（router/web-searcher/analyst/product-insight/prd-expert）
    - `context` 写清楚流水线阶段与输出格式（避免 LLM 自行发挥）
  - _Requirements: 5.1, 5.2, 5.3, 5.6_

- [x] 1.1 一键启动与冒烟（强烈建议，提升跑通效率）
  - 新增 `demos/05_news_to_prd/scripts/run_all.ps1`
    - 启动 network（8800/8900）
    - 启动 agents：router/web-searcher/analyst/product-insight/prd-expert
    - 启动 news-hunter（带 `--run-once` 便于立即触发）
  - 新增 `demos/05_news_to_prd/scripts/smoke.ps1`
    - 启动后等待固定时间（例如 60~120s）
    - 验证 Studio/日志里出现：project 创建成功 + 至少 1 条“调研报告”输出
  - README 中提供“只跑一次”的最短命令（避免 5 分钟等待）

- [-] 2. 复用和扩展 News Hunter（确定性组件：抓取 + 创建项目）
  - [x] 2.1 复制 demo02 的代码到新项目
    - 复制 `tools/news_fetcher.py`
    - 复制 `agents/news_hunter.py`
    - _Requirements: 1.1_

  - [x] 2.2 调整抓取节奏（默认 5 分钟 1 条）
    - `poll_interval_seconds` 默认 300
    - `max_news_per_poll` 默认 1
    - 增加“手动触发一次”的开发入口（例如 `--once` / `--run-once`），避免每次调试都要等 5 分钟
    - _Requirements: 1.5_

  - [ ] 2.3 实现“每条新闻创建一个 project”
    - 对每条被选中的新闻：
      - 生成 `run_id`
      - 组装 project goal（强烈建议用可解析的 JSON 块，避免 router 解析歧义）
        - 示例：goal 里包含 `NEWS_JSON={...}`（title/url/news_id/summary/run_id）
      - 调用 project mod 创建：`workspace.start_project(Project(template_id="news_to_prd", goal=..., name=...))`
    - 创建成功后：
      - 在 project 内发送第一条消息（写入新闻 title/url/summary，作为可见起点）
    - 并发满（或创建失败）时：
      - 直接 drop（不排队）
      - 记录日志 + 给用户可见提示（例如：系统繁忙/并发已满，已跳过本条新闻）
    - _Requirements: 1.2, 5.6_

  - [ ]* 2.4 News Hunter 单元测试（可选，MVP 可跳过）
    - 去重逻辑
    - project 创建失败时 drop 行为

- [x] 3. 复用调研团队（web-searcher + analyst）
  - [x] 3.1 复制 demo03 的 web 搜索工具
    - 复制 `tools/web_search.py`
    - 复制 `tools/__init__.py`
    - _Requirements: 2.3_

  - [x] 3.2 复制并修改 Web Searcher Agent
    - 复制 `agents/web_searcher.yaml`，修改连接端口为 8800
    - 约束输出：返回可引用的证据（链接 + 摘要），不要输出大段无结构文本
    - _Requirements: 2.2, 2.3_

  - [x] 3.3 复制并修改 Analyst Agent（结构化产出）
    - 复制 `agents/analyst.yaml`，修改连接端口为 8800
    - Analyst 产出必须结构化：市场趋势 / 竞品分析 / 用户讨论 / 关键洞察
    - 建议：Analyst 只 `send_event(task.complete)` 把结构化结果发回 router，由 router 统一对用户输出（降低多 Agent 输出错乱风险）
    - _Requirements: 2.4_

- [x] 4. Router（项目内总控：事件编排 + 统一对用户输出）
  - [x] 4.1 基于 demo03 扩展 Router 配置
    - 入口事件：`project.notification.started`
    - 流程事件：`task.delegate` / `task.complete` / `research.complete` / `insight.complete` / `prd.complete`
    - 修正 router 的提示词约束与 `max_iterations`，确保与“实际需要的 tool call 次数”一致（避免重复/漏发）
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 4.2 实现编排逻辑（推荐由 router 统一 send_project_message）
    - `project.notification.started` → 解析 project goal 获取新闻 → 委派 `task.delegate` 给 web-searcher
    - `task.complete` (from web-searcher) → 委派 `task.delegate` 给 analyst
    - `task.complete` (from analyst) → `send_project_message` 输出调研报告 → 发送 `research.complete`
    - `insight.complete` → `send_project_message` 输出爆款选题 → 委派给 prd-expert
    - `prd.complete` → `send_project_message` 输出 MVP PRD → `complete_project`
    - 所有事件 payload 建议携带 `run_id`（避免并发时串线）
    - _Requirements: 5.2, 5.3, 5.5_

- [ ] 5. Checkpoint 1：先跑通“新闻 → 调研报告”
  - 启动网络与 agents（news-hunter, router, web-searcher, analyst）
  - 观察：创建 project → router 开始调研 → 输出调研报告
  - 验证 drop-on-overload：将 `max_concurrent_projects` 临时调小触发丢弃提示
  - Definition of Done（必须满足）：
    - 看到新建的 project（名称建议以 `NewstoPRD:` 开头），且 project goal 可解析出 `NEWS_JSON`（含 `run_id/title/url/news_id`）
    - project 内第一条消息包含新闻 `title` + `url`（`summary` 允许为空）
    - project 内出现 **“调研报告”** 输出，且包含 4 个小节：市场趋势 / 竞品分析 / 用户讨论 / 关键洞察（每节至少 1 条要点）
    - 将 `max_concurrent_projects` 设为 1 后继续触发：后续新闻不会创建 project，且在 `prd-pipeline` 频道看到 drop 提示

- [x] 6. Product Insight Expert（产出爆款选题）
  - [x] 6.1 创建 `agents/product_insight.yaml`
    - 触发器：`research.complete`
    - 输出必须包含三要素：目标用户 / 用户痛点 / Web 解决方案
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [x] 6.2 产出与事件
    - 发送 `insight.complete`（结构化对象发给 router / prd-expert）
    - _Requirements: 3.5_

  - [ ]* 6.3 属性测试（可选）：Hit Product Topic 完整性

- [x] 7. PRD Expert（产出 MVP PRD）
  - [x] 7.1 创建 `agents/prd_expert.yaml`
    - 触发器：`insight.complete`
    - PRD 必含：产品名称 / 详细需求 / SEO 关键词（5-10）/ 域名推荐（3-5）
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 7.2 产出与事件
    - 发送 `prd.complete`（结构化 PRD 发给 router）
    - _Requirements: 4.4, 4.5, 4.7, 6.1, 6.2_

  - [ ]* 7.3~7.5 属性测试（可选）：PRD 结构、SEO 数量、域名数量

- [x] 8. Checkpoint 2：跑通完整流水线
  - 启动所有 agents
  - 验证端到端：新闻 → 调研 → 洞察 → PRD
  - 验证三阶段输出都可见（建议由 router 统一输出）
  - Definition of Done（必须满足）：
    - 依次出现 3 个阶段输出：调研报告 → 爆款产品选题 → MVP PRD
    - 爆款产品选题必须包含三要素：目标用户 / 用户痛点 / Web 解决方案
    - MVP PRD 必含：产品名称 + 需求文档（含 MVP Must-have/Nice-to-have）+ SEO 关键词 5-10 个 + 域名推荐 3-5 个
    - router 成功 `complete_project`，并在 project summary 中包含产品名与一句价值主张
  - ✅ 已验证通过（2025-12-30）：完整Pipeline执行成功，项目bc491675-b4d1-439c-ae05-d9049ba85e47已完成

- [x] 9. 错误处理与可观测性（MVP 可后置）
  - Router：阶段失败提示、失败原因透传
  - News Hunter：drop 的日志与提示格式统一
  - _Requirements: 5.4, 5.6_

- [x] 10. README（可运行说明）
  - 创建 `demos/05_news_to_prd/README.md`
  - 包含：架构、启动顺序、如何验证两次 checkpoint、常见问题

## Notes

- 标记 `*` 的测试项为可选，MVP 先跑通闭环再补。
- MVP 期间建议“router 统一对用户输出”，减少多 Agent 直接发 `send_project_message` 导致的重复/错格式/漏字段问题。
