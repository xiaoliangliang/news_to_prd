# Research Team - All-in-One Deployment
# Network + Router + Web-Searcher + Analyst

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install openagents
RUN pip install --no-cache-dir openagents

# Copy all files
COPY network.yaml /app/network.yaml
COPY agents/ /app/agents/
COPY tools/ /app/tools/
COPY deploy/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Expose ports
EXPOSE 8700 8600

# Environment variables
ENV OPENAI_API_KEY=""
ENV GLM_API_KEY=""
ENV BRAVE_API_KEY=""

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8700/api/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
