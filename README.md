# Jarvis — Voice Desktop AI Assistant for James

Jarvis is a security-gated voice-driven desktop AI. Brain runs on Hetzner VPS, hands run on PC, joined by Tailscale. All tool calls pass through a permission gate (Tier 0-3) before execution.

## Phases

- **Phase 0** (week 1): Foundations - OpenJarvis fork, policy gate, MCP hello-world
- **Phase 1** (weeks 2-3): Hands & gate - file index, connectors, tier table
- **Phase 2** (weeks 4-5): Voice & gateway - wake word, STT, TTS, Telegram
- **Phase 3** (weeks 6-7): Memory & heartbeat - scheduled jobs, recall, consolidation
- **Phase 4** (weeks 8-10): Autonomy & hardening - QuickDesk, redteam, local Ollama tier

## Architecture

Brain (Hetzner) <-> Hands (PC) over Tailscale. All tools pass through gate.

## Setup

```bash
python scripts/setup_keys.py        # Store API keys
python -m brain.jarvis_brain.app ask "hello"  # Test brain
python hands/server.py              # Start hands server
pytest tests/ -v                    # Run tests
```

## Tiers

- Tier 0: Read (auto)
- Tier 1: Reversible (auto)
- Tier 2: External (ask, 10m)
- Tier 3: Forbidden (never)

See SECURITY.md for full table.

## Kill File

Path: C:\Jarvis\.JARVIS_STOP
Effect: Halts execution before next tool call.

## Development

```bash
ruff check --fix .
mypy --strict brain/ hands/ policy/
pytest tests/ -v --cov=policy --cov-fail-under=80
```
