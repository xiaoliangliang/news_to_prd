#!/bin/bash
set -e

echo "=========================================="
echo "  Research Team - All-in-One Deployment"
echo "=========================================="

# Start the network in background
echo "[1/4] Starting OpenAgents Network..."
openagents network start /app/network.yaml &
NETWORK_PID=$!

# Wait for network to be ready
echo "[2/4] Waiting for network to be ready..."
sleep 10

# Check if network is running
for i in {1..30}; do
    if curl -s http://localhost:8700/api/health > /dev/null 2>&1; then
        echo "Network is ready!"
        break
    fi
    echo "Waiting for network... ($i/30)"
    sleep 2
done

# Start agents
echo "[3/4] Starting agents..."

echo "  - Starting router agent..."
openagents agent start /app/agents/router.yaml &
sleep 3

echo "  - Starting web-searcher agent..."
openagents agent start /app/agents/web_searcher.yaml &
sleep 3

echo "  - Starting analyst agent..."
openagents agent start /app/agents/analyst.yaml &
sleep 3

echo "[4/4] All components started!"
echo ""
echo "=========================================="
echo "  Research Team is now running!"
echo "=========================================="
echo ""
echo "  Studio UI: http://localhost:8700/studio"
echo "  API Health: http://localhost:8700/api/health"
echo ""
echo "  Agents:"
echo "    - router (coordinator)"
echo "    - web-searcher (information gatherer)"
echo "    - analyst (research synthesizer)"
echo ""
echo "=========================================="

# Keep container running and forward signals
wait $NETWORK_PID
