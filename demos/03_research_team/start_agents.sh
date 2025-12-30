#!/bin/bash
# Start all research team agents

echo "Starting Research Team Agents..."
echo "Connecting to network at ${NETWORK_HOST}:${NETWORK_PORT}"

# Wait for network to be ready
sleep 5

# Start agents in background
echo "Starting router agent..."
openagents agent start /app/agents/router.yaml \
  --network-host ${NETWORK_HOST} \
  --network-port ${NETWORK_PORT} &

sleep 2

echo "Starting web-searcher agent..."
openagents agent start /app/agents/web_searcher.yaml \
  --network-host ${NETWORK_HOST} \
  --network-port ${NETWORK_PORT} &

sleep 2

echo "Starting analyst agent..."
openagents agent start /app/agents/analyst.yaml \
  --network-host ${NETWORK_HOST} \
  --network-port ${NETWORK_PORT} &

echo "All agents started. Waiting..."

# Keep container running
wait
