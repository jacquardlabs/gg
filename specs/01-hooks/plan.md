---
type: plan
spec: 01-hooks
date: 2026-06-10
status: in-progress
---
# Plan

## Verification mapping

| Plan item | Requirement | Verification |
|---|---|---|
| P1: common.py | R5 | — (utility; tested transitively) |
| P2: manifest_check.py | R1, R2 | V1, V2 |
| P3: manifest_updater.py | R2, R5 | V2 |
| P4: failure_counter.py | R3, R5 | V3 |
| P5: session_start.py | R4, R5 | V4, V5 |
| P6: tests | V1–V5 | — |
| P7: pyproject.toml | R6 | — |
| P8: docs/install.md | R6 | V6 |
| P9: templates/plan.md | — | — |

## Steps

1. (P1) `hooks/common.py` — git root detection, state dir helpers
2. (P2) `hooks/manifest_check.py` — PreToolUse: block edit outside manifest
3. (P3) `hooks/manifest_updater.py` — PostToolUse/Write: re-parse manifest from plan.md
4. (P4) `hooks/failure_counter.py` — PostToolUse/Bash: count consecutive failures
5. (P5) `hooks/session_start.py` — SessionStart: cctx watch + purpose tag
6. (P6) `tests/` — pytest suite for P2–P5
7. (P7) `pyproject.toml` — project metadata + test deps
8. (P8) `docs/install.md` — settings.json block + one-step install
9. (P9) `templates/plan.md` — plan template including manifest block

```manifest
hooks/common.py
hooks/manifest_check.py
hooks/manifest_updater.py
hooks/failure_counter.py
hooks/session_start.py
tests/test_manifest_check.py
tests/test_manifest_updater.py
tests/test_failure_counter.py
tests/test_session_start.py
pyproject.toml
docs/install.md
templates/plan.md
.gitignore
```
