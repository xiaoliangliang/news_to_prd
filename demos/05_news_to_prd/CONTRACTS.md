# NewstoPRD 关键决策与契约

> 本文档定义了 NewstoPRD 流水线的核心契约，所有实现必须遵循这些约定。

## 1. 项目隔离策略

**决策**: 每条新闻创建 1 个独立的 project（不复用同一个长项目）

**理由**:
- 上下文隔离：不同新闻之间不会串线
- 可追踪性：每个 project 对应一条新闻的完整生命周期
- 便于调试：可以独立查看每条新闻的处理过程

## 2. 并发策略

**决策**: drop-on-overload（超过上限直接丢弃，不排队等待）

**行为**:
- 当 `active_projects >= max_concurrent_projects` 时：
  - 跳过该新闻的 project 创建
  - 记录日志（包含被丢弃的新闻标题和原因）
  - 向 `prd-pipeline` 频道发送用户可见提示

**配置**:
```yaml
max_concurrent_projects: 3  # MVP 建议值，便于观察 drop 行为
```

## 3. 最小 Payload Schema

### 3.1 NewsPayload（新闻触发 payload）

```python
@dataclass
class NewsPayload:
    """新闻触发流水线的最小 payload"""
    run_id: str           # 本次流水线唯一标识（UUID）
    news_id: str          # 新闻唯一标识（来自 HackerNews）
    title: str            # 新闻标题（必填）
    url: str              # 新闻链接（必填）
    summary: str          # 新闻摘要（MVP 允许为空字符串）
    source: str           # 来源（默认 "hackernews"）
    published_at: str     # 发布时间（ISO 8601 格式）
```

### 3.2 JSON 格式示例

```json
{
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "news_id": "12345678",
  "title": "OpenAI Releases GPT-5",
  "url": "https://example.com/news/gpt5",
  "summary": "",
  "source": "hackernews",
  "published_at": "2024-01-15T10:30:00Z"
}
```

## 4. Summary 字段处理

### MVP 阶段
- `summary` 允许为空字符串 `""`
- 后续由 analyst / prd-expert 在内容里补充

### 增强阶段（后置）
- 抓取网页正文后生成 1-3 句摘要
- 使用 LLM 或规则提取

## 5. 入口事件

**决策**: 使用 `project.notification.started` 作为流水线入口事件

**流程**:
1. News Hunter 调用 `workspace.start_project()` 创建项目
2. Project mod 自动触发 `project.notification.started` 事件
3. Router 监听该事件，解析 project goal 获取新闻信息
4. Router 开始编排后续流水线

**Project Goal 格式**:
```
NEWS_JSON={"run_id":"...","news_id":"...","title":"...","url":"...","summary":"...","source":"...","published_at":"..."}
```

## 6. 事件流定义

| 事件名称 | 触发者 | 接收者 | Payload 要求 |
|---------|--------|--------|-------------|
| `project.notification.started` | project mod | router | project goal 包含 NEWS_JSON |
| `task.delegate` | router | web-searcher/analyst | 包含 `run_id`, `task_id`, `query` |
| `task.complete` | web-searcher/analyst | router | 包含 `run_id`, `task_id`, `results` |
| `research.complete` | router | product-insight | 包含 `run_id`, 完整调研报告 |
| `insight.complete` | product-insight | prd-expert | 包含 `run_id`, 爆款选题三要素 |
| `prd.complete` | prd-expert | router | 包含 `run_id`, 完整 PRD |

## 7. 输出统一由 Router 负责

**决策**: MVP 期间，所有对用户可见的输出由 Router 统一调用 `send_project_message`

**理由**:
- 减少多 Agent 直接发消息导致的重复/错格式/漏字段问题
- 便于控制输出顺序和格式一致性

**输出时机**:
1. 调研报告完成后 → Router 输出
2. 爆款选题完成后 → Router 输出
3. MVP PRD 完成后 → Router 输出

## 8. 端口配置

| 服务 | 端口 |
|-----|------|
| HTTP (Studio) | 8800 |
| gRPC | 8900 |

## 9. 必需的 Mods

```yaml
mods:
  - name: "openagents.mods.workspace.project"
    enabled: true
    config:
      max_concurrent_projects: 3
      
  - name: "openagents.mods.workspace.default"
    enabled: true
    config:
      custom_events_enabled: true
      
  - name: "openagents.mods.workspace.messaging"
    enabled: true
```

## 10. Project Template

```yaml
project_templates:
  news_to_prd:
    name: "News to PRD Pipeline"
    description: "从科技新闻自动生成 MVP PRD"
    agent_groups: ["coordinators", "researchers", "experts"]
    context: |
      NewstoPRD 流水线
      
      阶段：
      1. 调研阶段：web-searcher 搜索 → analyst 分析
      2. 洞察阶段：product-insight 挖掘爆款选题
      3. PRD 阶段：prd-expert 生成 MVP PRD
      
      输出格式：
      - 调研报告：市场趋势/竞品分析/用户讨论/关键洞察
      - 爆款选题：目标用户/用户痛点/Web解决方案
      - MVP PRD：产品名称/需求文档/SEO关键词/域名推荐
```

---

**契约版本**: 1.0.0  
**最后更新**: 2024-01-15  
**状态**: ✅ 已对齐
