# Jarvis Production Runbook

## Daily Operations Checklist

### Morning (06:00)
- [ ] Check server health (Hetzner CPU, memory, disk)
- [ ] Verify Tailscale connection (both sides)
- [ ] Check audit log for overnight activity

### 07:00 Manila
- [ ] Morning brief saved to C:\Jarvis\logs\brief.txt
- [ ] Verify email, calendar, project status in log

### Throughout Day
- [ ] Monitor API quota (daily limit: $50)
- [ ] Check for Tier 2 approvals pending >10min
- [ ] Verify no unexpected Tier 3 attempts in audit log

### Evening (18:00)
- [ ] Review red team suite results (if weekly run)
- [ ] Check cost tracking (daily total)
- [ ] Verify scheduled jobs completed

### Night (23:00)
- [ ] Nightly consolidation should run
- [ ] Pending facts reviewed and promoted
- [ ] Database integrity check

---

## Monitoring & Alerts

### WebSocket UI Alerts
- CPU >80%: alert in browser UI
- Memory >85%: alert in browser UI
- Daily cost >$50: log entry (check C:\Jarvis\logs\cost.log)
- Tier 2 approval pending >10min: UI panel reminder

### Log Monitoring
- File: `C:\Jarvis\logs\audit.jsonl`
- Check: every tool call, tier assigned, approved/refused
- Alert: Tier 3 attempt = investigate immediately

### Performance Targets
- Wake-to-response: <2.5s
- STT latency: <1s
- TTS latency: <500ms
- File search: <100ms

---

## Troubleshooting

### Brain Not Responding
```bash
# SSH to Hetzner
ssh root@<ip>

# Check logs
docker-compose logs brain

# Restart
docker-compose restart brain

# Verify
curl http://localhost:8000/health
```

### Hands Service Down
```powershell
# Windows
net stop JarvisHands
net start JarvisHands

# Or via Services:
services.msc -> JarvisHands -> Restart
```

### No Morning Brief
- Verify morning_brief.md job scheduled
- Check brain logs for job execution errors
- Verify output file: C:\Jarvis\logs\brief.txt
- Run: `python brain/jarvis_brain/app ask "test brief"`

### Tier 2 Approval Not Working
- Verify WebSocket UI accessible at http://localhost:8788
- Check browser console for errors
- Verify hands/server.py running (Windows Service)
- Check C:\Jarvis\logs\approvals.jsonl for approval events

### File Index Slow
- Rebuild index: `python hands/index/builder.py rebuild <workspace>`
- Check Ollama running: `curl http://localhost:11434/api/tags`
- Verify nomic-embed-text model: `ollama pull nomic-embed-text`

---

## Rollback Procedures

### Code Rollback
```bash
git revert <commit>
git push
# Brain auto-redeploys via CD pipeline
```

### Database Rollback
```bash
# Backup current DB
cp C:\Jarvis\memory\jarvis.db C:\Jarvis\memory\jarvis.db.backup

# Restore from backup
cp C:\Jarvis\memory\jarvis.db.20261001 C:\Jarvis\memory\jarvis.db

# Restart brain
docker-compose restart brain
```

### Kill Switch
```bash
# Immediate stop (all branches)
touch C:\Jarvis\.JARVIS_STOP

# Gate will refuse all tool calls
# Remove to resume:
rm C:\Jarvis\.JARVIS_STOP
```

---

## Security Audits

### Weekly (Every Monday)
- Run red team injection suite: `python brain/redteam/run_suite.py`
- Review audit log for anomalies
- Check Tier 2 promotion pipeline (14-day cycles)
- Rotate device token: `python hands/scripts/setup_device_token.py`

### Monthly
- Full security review (threat model vs reality)
- API key rotation
- Audit log export + archive (30-day rolling retention)

### Quarterly
- Penetration test against gate
- Performance audit (latencies, costs)
- Dependency security scan

---

## Cost Tracking

### Daily
- Monitor `C:\Jarvis\logs\cost.jsonl`
- Expected: $0.50-2.00/day (depends on job frequency)
- Alert: >$50/day triggers halt

### Monthly Breakdown
- API calls: ~1000-2000
- Tokens: ~100K-500K
- Cost: $15-40/month (typical)

### Optimization
- Haiku for light tasks (<100 tokens)
- Sonnet for medium (100-500 tokens)
- Opus only for reasoning (complex decisions)

---

## Escalation Path

### Critical (System Down)
1. Activate kill switch
2. Alert James (Telegram + email)
3. Check logs (brain + hands)
4. Restart affected service
5. Verify recovery
6. Root cause analysis

### High (Tier 3 Attempt)
1. Log incident (audit trail)
2. Alert James immediately
3. Review perpetrator (was it intentional? compromised?)
4. Add rule to gate if new vector
5. Report to team

### Medium (Tier 2 Stall)
1. Check Telegram connection
2. Manually approve or deny
3. Monitor for pattern
4. Adjust timeout if needed

### Low (Performance Degradation)
1. Profile (CPU, memory, queries)
2. Optimize hotspot
3. Monitor for improvement
4. Document in runbook

---

## Useful Commands

```bash
# Brain
docker-compose logs -f brain                    # Live logs
docker-compose restart brain                    # Restart service
curl http://localhost:8000/health               # Health check

# PC
net start JarvisHands                          # Start service
net stop JarvisHands                           # Stop service
curl http://127.0.0.1:8787/health             # Health check
http://127.0.0.1:8787/ui                      # UI (browser)

# Database
sqlite3 C:\Jarvis\memory\jarvis.db             # SQLite shell
SELECT * FROM decisions ORDER BY created_at DESC LIMIT 5;  # Recent decisions

# Audit
type C:\Jarvis\logs\audit.jsonl | findstr "Tier"           # Filter by tier
type C:\Jarvis\logs\audit.jsonl | findstr "false"          # Denied actions

# Git
git log --oneline | head -10                  # Recent commits
git diff main..HEAD                            # Pending changes
git push                                       # Deploy changes
```

---

## Contact & Escalation

**Owner:** James Duran (itsupport@omnichannelsol.com)  
**On-Call:** [TBD - escalation contact]  
**Slack:** [TBD - team channel]  
**Runbook Maintainer:** [TBD]

Last Updated: October 12, 2026  
Next Review: November 12, 2026
