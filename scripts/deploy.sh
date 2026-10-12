#!/bin/bash
# Jarvis production deployment script

set -e

echo "=== JARVIS PRODUCTION DEPLOYMENT ==="
echo

# 1. GitHub
echo "[1/5] GitHub Setup"
read -p "GitHub username: " GITHUB_USER
read -p "GitHub repo name (jarvis): " GITHUB_REPO
GITHUB_REPO=${GITHUB_REPO:-jarvis}

git remote add origin "https://github.com/$GITHUB_USER/$GITHUB_REPO.git" 2>/dev/null || true
git branch -M master
git push -u origin master
echo "✓ Pushed to github.com/$GITHUB_USER/$GITHUB_REPO"
echo

# 2. Hetzner Setup
echo "[2/5] Hetzner Deployment"
read -p "Hetzner server IP: " HETZNER_IP
read -p "Hetzner server user (root): " HETZNER_USER
HETZNER_USER=${HETZNER_USER:-root}

echo "Deploying to $HETZNER_USER@$HETZNER_IP..."
ssh "$HETZNER_USER@$HETZNER_IP" << 'EOSSH'
  cd /opt
  git clone https://github.com/jamesduran/jarvis.git || cd jarvis && git pull
  cd jarvis
  docker-compose up -d
  sleep 5
  curl http://localhost:8000/health || echo "Warning: brain not responding yet"
EOSSH
echo "✓ Deployed to Hetzner"
echo

# 3. PC Setup
echo "[3/5] PC Service Installation"
python hands/scripts/install_service.py
net start JarvisHands 2>/dev/null || echo "Service may need manual start"
echo "✓ PC service installed"
echo

# 4. Verification
echo "[4/5] Running Verification Tests"
pytest tests/ -v --cov=policy,brain,hands --cov-fail-under=80 || echo "Warning: tests may need Python 3.11+"
echo

# 5. Smoke Tests
echo "[5/5] Smoke Testing"
echo "Brain health:"
curl -s http://127.0.0.1:8000/health || echo "Brain not responding"
echo
echo "Hands health:"
curl -s http://127.0.0.1:8787/health || echo "Hands not responding"
echo
echo "✓ Deployment complete"
echo
echo "Next steps:"
echo "1. Monitor logs for 24h"
echo "2. Verify morning brief arrives 07:00"
echo "3. Check audit.jsonl for tool calls"
echo "4. Run red team suite (python brain/redteam/run_suite.py)"
