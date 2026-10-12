# Jarvis Production Launch Checklist

## Pre-Launch (Day -3)

### Code & Deployment
- [x] All 4 phases complete (Phase 0-4 merged to master)
- [x] Tests pass (80%+ coverage)
- [x] CI/CD workflows configured (GitHub Actions)
- [x] docker-compose.yml ready (Hetzner brain)
- [x] Windows Service scripts ready (PC hands)
- [ ] GitHub repo created (jamesduran/jarvis)
- [ ] Hetzner VPS provisioned (Ubuntu 24.04, CX42)
- [ ] Tailscale configured on all devices

### Credentials & Security
- [ ] ANTHROPIC_API_KEY stored in keyring (not in code)
- [ ] TELEGRAM_BOT_TOKEN stored in keyring
- [ ] Device token generated for PC
- [ ] Hetzner SSH key configured
- [ ] GitHub SSH key or PAT configured
- [ ] Rotation schedule documented

### Monitoring Setup
- [ ] Telegram owner ID verified
- [ ] Alert thresholds set (CPU 80%, memory 85%, cost $50)
- [ ] Log rotation configured (365-day retention)
- [ ] Backup strategy defined (daily snapshots)

---

## Launch Day (Day 0)

### 08:00 — Pre-Flight Checks
- [ ] Brain code pushed to GitHub
- [ ] PC service scripts tested locally
- [ ] Hetzner SSH access verified
- [ ] Tailscale connectivity confirmed (both sides)

### 09:00 — Brain Deployment (Hetzner)
```bash
ssh root@<HETZNER_IP>
cd /opt && git clone https://github.com/jamesduran/jarvis.git
cd jarvis
export ANTHROPIC_API_KEY=<key>
export TELEGRAM_BOT_TOKEN=<token>
export POSTGRES_PASSWORD=<password>
docker-compose up -d
```
- [ ] docker-compose up -d completes
- [ ] Postgres starts
- [ ] Brain service starts
- [ ] curl http://localhost:8000/health returns 200

### 09:30 — PC Deployment (Windows)
```powershell
cd C:\Users\Administrator\omniJarvis
uv sync
python scripts/setup_keys.py
python hands/scripts/install_service.py
net start JarvisHands
```
- [ ] Dependencies installed
- [ ] API keys stored in keyring
- [ ] Windows Service registered
- [ ] Service starts automatically
- [ ] curl http://127.0.0.1:8787/health returns 200

### 10:00 — Smoke Tests
```bash
# Brain
python -m brain.jarvis_brain.app ask "What is 2+2?"

# Hands
curl http://127.0.0.1:8787/ui
# UI should load, click enable mic

# Gateway
# Send test message to Telegram bot: /status
# Should respond with system status
```
- [ ] Brain responds to queries
- [ ] Hands server healthy
- [ ] UI loads correctly
- [ ] Telegram bot responds

### 11:00 — Verification Suite
```bash
pytest tests/ -v --cov=policy,brain,hands --cov-fail-under=80
```
- [ ] All tests pass
- [ ] Coverage >= 80%
- [ ] No Tier 3 executions

### 12:00 — Audit Trail Verification
```bash
# Verify audit logging
tail -20 C:\Jarvis\logs\audit.jsonl

# All tool calls should be logged with tier assignments
```
- [ ] Audit log contains entries
- [ ] Tier assignments correct
- [ ] No unexpected failures

### 13:00 — Go/No-Go Decision
- [ ] All checks pass: **GO** → proceed to operations
- [ ] Any check fails: **NO-GO** → rollback, investigate, retry

---

## Post-Launch (Day 1-7)

### Day 1: 24h Stability Watch
- [ ] Monitor logs hourly
- [ ] Verify no errors in audit.jsonl
- [ ] Check CPU/memory usage trending
- [ ] Confirm no unexpected alerts

### Day 2-3: Feature Activation
- [ ] Voice pipeline tested (wake word + STT + TTS)
- [ ] Telegram approval flow tested (manual Tier 2 task)
- [ ] File index rebuilt (workspace scan)

### Day 4: Scheduled Jobs
- [ ] Morning brief arrives 07:00 Manila time ✓
- [ ] Inbox triage runs 09:00 ✓
- [ ] Repo health check runs 14:00 ✓
- [ ] Server health check runs 15:00 ✓
- [ ] School reminders run 16:00 ✓

### Day 5: Red Team Suite
```bash
python brain/redteam/run_suite.py
```
- [ ] Injection suite passes
- [ ] SQL injection blocked
- [ ] XSS injection blocked
- [ ] Path traversal blocked

### Day 6: Monitoring & Alerts
- [ ] Cost tracking working ($0.50-2.00/day expected)
- [ ] CPU/memory alerts configured
- [ ] Telegram alerts flowing
- [ ] Log retention policy enforced

### Day 7: Production Handoff
- [ ] Runbook reviewed with team
- [ ] Escalation procedures clear
- [ ] On-call rotation established
- [ ] Weekly audit schedule set

---

## Rollback Triggers

**Immediate Rollback If:**
- Brain or PC service crashes and won't restart
- Audit log stops recording (security breach risk)
- Tier 3 tool executes (gate failure)
- API quota exhausted in <4h (cost runaway)
- Tailscale connectivity lost >30min

**Procedure:**
```bash
# Kill switch (halts all tool calls)
touch C:\Jarvis\.JARVIS_STOP

# Investigate
docker-compose logs brain | tail -50
type C:\Jarvis\logs\audit.jsonl | tail -20

# Rollback code
git revert <commit>
git push
docker-compose restart brain

# Resume
rm C:\Jarvis\.JARVIS_STOP
```

---

## Success Criteria (Go-Live Ready)

- [x] Phase 0-4 complete and merged
- [x] All tests pass (80%+ coverage)
- [x] Deployment scripts created
- [x] Runbook documented
- [x] Security model validated
- [ ] GitHub repo created
- [ ] Hetzner VPS running
- [ ] PC service installed
- [ ] Smoke tests passing
- [ ] Red team suite passing
- [ ] 24h stability verified
- [ ] Scheduled jobs running
- [ ] Cost tracking healthy

---

## Sign-Off

**Jarvis Project Manager:** _________________  
**Date:** October 12, 2026  
**Go-Live Target:** November 12, 2026 (4 weeks)

**Owner Approval:** James Duran  
**Signature:** _________________ **Date:** _______

---

**Once both signed, proceed with production deployment.**
