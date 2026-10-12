# Jarvis Setup Guide

## Phase 0: Foundation (Completed)

Repo is scaffolded. To verify Phase 0 is ready:

```bash
cd C:\Users\Administrator\omniJarvis
git log --oneline | head -1
# Should show: feat(phase-0): Jarvis foundations...
```

## Phase 0 Verification

### 1. Install Python dependencies

```bash
# Install uv (package manager)
pip install uv

# Sync dependencies
uv sync

# Verify
python -c "import anthropic; print('OK')"
```

### 2. Store API keys

```bash
python scripts/setup_keys.py
# Prompts for: ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_OWNER_ID
# Stores in Windows Credential Manager
```

### 3. Test brain boot

```bash
# Brain needs ANTHROPIC_API_KEY set
set ANTHROPIC_API_KEY=your-key-here
python -m brain.jarvis_brain.app ask "What is 2+2?"
# Should return: Four. or similar
```

### 4. Test hands server

```bash
# Terminal 1: Start hands server
python hands/server.py
# Output: INFO:     Uvicorn running on http://127.0.0.1:8787

# Terminal 2: Test health endpoint
curl http://127.0.0.1:8787/health
# Response: {"status":"ok","service":"hands"}

# Test UI
# Navigate to: http://127.0.0.1:8787/ui
# Should see canvas with breathing core, idle state
```

### 5. Run tests

```bash
# All tests
pytest tests/ -v --cov=policy,brain,hands --cov-fail-under=80

# Output should show:
# test_tier_0_is_read_only PASSED
# test_tier_3_is_forbidden PASSED
# test_gate_check_refuses_tier_3 PASSED
# ... (80%+ coverage required)
```

### 6. Verify gate audit log

```bash
# After running tests, check audit log
type logs\audit.jsonl

# Should see JSONL entries like:
# {"timestamp": "...", "tool": "file.read", "tier": "Read", "allowed": true, ...}
```

## Next: Phase 1 (File Index & Connectors)

When ready to start Phase 1:

```bash
git checkout -b phase/1-hands-gate

# Follow docs/PHASES.md Phase 1 objectives
```

## GitHub Setup

To push to GitHub:

```bash
# Create repo on GitHub (https://github.com/jamesduran/jarvis)

# Add remote
git remote add origin https://github.com/jamesduran/jarvis.git
git branch -M main
git push -u origin main

# Create dev branch
git checkout -b dev
git push -u origin dev
```

## Hetzner Deployment (Phase 1+)

Brain deployment ready via docker-compose:

```bash
# On Hetzner VPS:
git clone https://github.com/jamesduran/jarvis.git
cd jarvis

# Setup env
export ANTHROPIC_API_KEY=...
export TELEGRAM_BOT_TOKEN=...
export POSTGRES_PASSWORD=...

# Deploy
docker-compose up -d

# Logs
docker-compose logs -f brain
```

## PC Service Installation (Phase 2+)

Hands service installation:

```bash
# On Windows PC:
python hands/scripts/install_service.py
# Creates Windows Service + Chrome app-mode shortcut

# Start service
net start JarvisHands

# Verify
curl http://127.0.0.1:8787/health
```

## Troubleshooting

### API key not found
```bash
python scripts/setup_keys.py
```

### Port already in use (8787)
```bash
netstat -ano | findstr :8787
taskkill /PID <PID> /F
```

### Tests fail
```bash
# Clear cache
rmdir /s /q __pycache__ .mypy_cache .pytest_cache

# Re-run
pytest tests/ -v
```

### Git line ending warnings
```bash
git config core.autocrlf true
```

## Architecture Checklist

- [ ] Phase 0 repo cloned/setup
- [ ] Dependencies installed (uv sync)
- [ ] API keys stored (scripts/setup_keys.py)
- [ ] Brain boots (app.py ask test)
- [ ] Hands server runs (health endpoint)
- [ ] UI loads (http://127.0.0.1:8787/ui)
- [ ] Tests pass (pytest 80%+ coverage)
- [ ] Git workflows configured (.github/workflows/)
- [ ] GitHub remote added (git remote add origin...)
- [ ] Ready for Phase 1
