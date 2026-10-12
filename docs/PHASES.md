# Jarvis Implementation Phases

## Phase 0: Foundations (COMPLETE)
- Policy gate (Tier 0-3, hard Tier 3 refusal)
- Brain boot (OpenJarvis + Claude)
- Hands server (device-token auth)
- UI (canvas visualization)
- Tests & CI/CD

## Phase 1: Hands & Gate (Weeks 2-3)
- File index (FTS5 + embeddings)
- Connectors (email, calendar, GitHub, Drive - Tier 0 read)
- Full tier table (50+ tools)
- Tier promotion (14-day tracker)
- 100+ integration tests

## Phase 2: Voice & Gateway (Weeks 4-5)
- Wake word (openWakeWord)
- STT (Whisper large-v3-turbo)
- TTS (kokoro local)
- Telegram gateway (approve/deny Tier 2)
- UI WebSocket (state, captions, audio)

## Phase 3: Memory & Heartbeat (Weeks 6-7)
- Memory DB (SQLite + embeddings)
- 5 scheduled jobs (morning brief, triage, health checks)
- Nightly consolidation
- Recall accuracy tests

## Phase 4: Autonomy & Hardening (Weeks 8-10)
- QuickDesk remote desktop
- Local Ollama tier (offline mode)
- Red team injection suite
- Monitoring & alerts
- Cost tracking

Total: 8-10 weeks
