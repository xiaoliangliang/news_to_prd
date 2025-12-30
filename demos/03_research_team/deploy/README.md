# Research Team 云端部署指南

## 一键部署到 Sealos

### 步骤 1：构建镜像

在 `demos/03_research_team` 目录下执行：

```bash
docker build -f deploy/Dockerfile -t research-team:latest .
```

### 步骤 2：推送到镜像仓库

```bash
# 推送到 Docker Hub
docker tag research-team:latest your-dockerhub-username/research-team:latest
docker push your-dockerhub-username/research-team:latest

# 或推送到阿里云镜像仓库
docker tag research-team:latest registry.cn-hangzhou.aliyuncs.com/your-namespace/research-team:latest
docker push registry.cn-hangzhou.aliyuncs.com/your-namespace/research-team:latest
```

### 步骤 3：在 Sealos 部署

1. 打开 Sealos 应用管理
2. 点击「新建应用」
3. 填写配置：
   - 镜像地址：`your-registry/research-team:latest`
   - CPU：0.5 Core
   - 内存：512 Mi
   - 端口：8700 (HTTP), 8600 (gRPC)
   - 开启公网访问

4. 添加环境变量：
   - `GLM_API_KEY`: 你的智谱 API Key（必填）
   - `BRAVE_API_KEY`: Brave Search API Key（可选，用于网页搜索）

5. 点击部署

### 步骤 4：访问

部署成功后，通过公网地址访问 Studio：
```
https://your-app.sealoshzh.site/studio
```

## 环境变量说明

| 变量名 | 必填 | 说明 |
|--------|------|------|
| GLM_API_KEY | 是 | 智谱 GLM-4 API Key |
| BRAVE_API_KEY | 否 | Brave Search API Key |
| OPENAI_API_KEY | 否 | OpenAI API Key（如果用 OpenAI 模型）|

## 功能说明

部署后包含以下组件：

- **Network**: OpenAgents 网络协调器
- **Router Agent**: 接收研究请求，协调任务分配
- **Web-Searcher Agent**: 搜索网络信息
- **Analyst Agent**: 分析和综合研究结果

## 使用方法

1. 访问 Studio UI
2. 创建一个 Research Task 项目
3. 输入研究主题，如 "Rust vs Go 性能对比"
4. 等待 agents 协作完成研究报告
