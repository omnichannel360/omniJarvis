# Jarvis Project - Claude Code Instructions

Phase 0 complete. Ready for Phase 1.

## Branches

- main: stable
- dev: active development
- phase/0-foundations: Phase 0 (current)
- phase/1-hands-gate: Phase 1 (next)

## Commits

Format: type(area): description
Types: feat, fix, refactor, docs, test, chore, ci

## Pre-commit

```bash
ruff check --fix .
mypy --strict brain/ hands/ policy/
pytest tests/ -v --cov=policy --cov-fail-under=80
```

## Next: Phase 1

- File index (FTS5 + embeddings)
- Connectors (email, calendar, GitHub, Drive)
- Full tier table + promotions
- Comprehensive gate tests
