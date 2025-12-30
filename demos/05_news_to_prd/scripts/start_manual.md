# 手动启动指南

如果 PowerShell 脚本有问题，可以手动在多个终端窗口中启动各组件。

## 步骤

### 终端 1: 启动 Network
```powershell
cd demos/05_news_to_prd
openagents network start --config network.yaml
```

### 终端 2: 启动 Router
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/router.yaml
```

### 终端 3: 启动 Web Searcher
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/web_searcher.yaml
```

### 终端 4: 启动 Analyst
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/analyst.yaml
```

### 终端 5: 启动 Product Insight
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/product_insight.yaml
```

### 终端 6: 启动 PRD Expert
```powershell
cd demos/05_news_to_prd
openagents agent start --config agents/prd_expert.yaml
```

### 终端 7: 启动 News Hunter
```powershell
cd demos/05_news_to_prd

# 单次运行（立即触发）
python agents/news_hunter.py --host localhost --port 8800 --run-once

# 或持续运行（每5分钟抓取一次）
python agents/news_hunter.py --host localhost --port 8800 --interval 300
```

## 访问 Studio

启动后访问 http://localhost:8800
