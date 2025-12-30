# News to PRD - 新闻转产品需求文档自动生成系统

基于 OpenAgents 框架的多智能体流水线系统，自动从科技新闻生成 MVP 产品需求文档（PRD）。

## 项目简介

本项目实现了一个完整的 AI 智能体协作流水线：

```
新闻获取 → 网络调研 → 分析总结 → 产品洞察 → PRD生成
```

### 核心智能体

| 智能体 | 职责 |
|--------|------|
| **News Hunter** | 从 Hacker News 获取科技新闻 |
| **Router** | 流水线协调器，调度各阶段任务 |
| **Web Searcher** | 网络搜索专家，收集相关信息 |
| **Analyst** | 调研分析师，生成调研报告 |
| **Product Insight** | 产品洞察师，挖掘产品选题 |
| **PRD Expert** | PRD专家，生成MVP需求文档 |

## 快速开始

### 环境要求

- Python 3.9+
- OpenAgents SDK

```bash
pip install openagents
```

### 可选配置

设置 Brave Search API Key 以获得更好的搜索效果：

```bash
# Windows PowerShell
$env:BRAVE_API_KEY="your-api-key"

# Linux/Mac
export BRAVE_API_KEY="your-api-key"
```

## 启动流程

### 方式一：一键启动（推荐）

```powershell
cd demos/05_news_to_prd

# 持续运行模式（每5分钟抓取一条新闻）
.\scripts\run_all.ps1

# 单次运行模式（立即触发，适合调试）
.\scripts\run_all.ps1 -RunOnce
```

### 方式二：手动启动

需要打开 **7 个终端窗口**，按顺序执行：

**终端 1 - 启动 Network：**
```powershell
cd demos/05_news_to_prd
openagents network start --config network.yaml
```

**终端 2 - 启动 Router：**
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/router.yaml
```

**终端 3 - 启动 Web Searcher：**
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/web_searcher.yaml
```

**终端 4 - 启动 Analyst：**
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/analyst.yaml
```

**终端 5 - 启动 Product Insight：**
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/product_insight.yaml
```

**终端 6 - 启动 PRD Expert：**
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/prd_expert.yaml
```

**终端 7 - 启动 News Hunter：**
```powershell
cd demos/05_news_to_prd

# 单次运行
python agents/news_hunter.py --host localhost --port 8800 --run-once

# 或持续运行
python agents/news_hunter.py --host localhost --port 8800 --interval 300
```

### 访问 Studio 界面

启动完成后，访问 http://localhost:8800 查看流水线运行状态。

## 流水线输出

完整流水线会依次生成：

1. **📊 调研报告** - 市场趋势、竞品分析、用户讨论、关键洞察
2. **💡 爆款产品选题** - 目标用户、用户痛点、Web解决方案
3. **📝 MVP PRD** - 产品名称、需求文档、SEO关键词、域名推荐

## 项目结构

```
demos/05_news_to_prd/
├── agents/                 # 智能体配置
│   ├── news_hunter.py      # 新闻猎手
│   ├── router.yaml         # 流水线协调器
│   ├── web_searcher.yaml   # 网络搜索专家
│   ├── analyst.yaml        # 调研分析师
│   ├── product_insight.yaml # 产品洞察师
│   └── prd_expert.yaml     # PRD专家
├── tools/                  # 工具模块
│   ├── news_fetcher.py     # 新闻获取工具
│   └── web_search.py       # 网络搜索工具
├── scripts/                # 启动脚本
│   ├── run_all.ps1         # 一键启动
│   └── smoke.ps1           # 冒烟测试
├── network.yaml            # 网络配置
└── README.md               # 详细文档
```

## 常见问题

**Q: 流水线没有启动？**
A: 确保按顺序启动：先 Network，再各 Agent，最后 News Hunter。

**Q: 搜索结果不理想？**
A: 设置 `BRAVE_API_KEY` 环境变量使用 Brave Search，效果更好。

**Q: 如何查看详细日志？**
A: 查看 `demos/05_news_to_prd/logs/` 目录下的日志文件。

## 相关文档

- [详细说明](demos/05_news_to_prd/README.md)
- [契约文档](demos/05_news_to_prd/CONTRACTS.md)
