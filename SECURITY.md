# Security Model

## Permission Tiers

| Tier | Level | Approval | Example |
|------|-------|----------|---------|
| 0 | Read-only | Auto | file.read, screenshot |
| 1 | Reversible | Auto | workspace.write, git.commit, app.open |
| 2 | External/costly | Ask (10m) | mail.send, github.create_pr |
| 3 | Forbidden | NEVER | payment.process, account.delete |

**Tier 3 is hard-refused in code. No config can override it.**

## Audit Trail

Path: C:\Jarvis\logs\audit.jsonl

JSONL entries: timestamp, tool, tier, allowed, reason

Retention: 365 days

## Kill File

Path: C:\Jarvis\.JARVIS_STOP

Checked before every tool call. Halts execution immediately.

## Secrets

- Stored in OS keystore (Credential Manager, Keychain)
- Never in files, logs, or .env
- Fail loudly if missing

## Tier Promotion (Phase 1+)

Tier 2 -> Tier 1 after:
- 14 days without rollback
- 10+ successful executions
- Manual approval in promotions.yaml

Tracked in C:\Jarvis\logs\approvals.jsonl
