---
type: questions
spec: 01-hooks
date: 2026-06-10
status: answered
---
# Questions before work starts

Reply inline at each "answer:". Each question states what happens if I guess.

## Needs your decision (reserved for you)

1. **What is the plan manifest format in plan.md?** The manifest check hook
   needs to parse the file list from plan.md. Two options:
   - (a) A fenced code block tagged `manifest` containing one path per line
   - (b) A `## Files` section with a bulleted list of paths
   Option (a) is easier to parse deterministically; option (b) reads more
   naturally. If unanswered I will use option (a).
   → answer: a — fenced ```manifest block

2. **Failure counter threshold: how many consecutive failures before warning?**
   2 is aggressive (catches retry loops fast but may false-positive on
   flaky tests); 3 gives more breathing room. If unanswered I will use 2.
   → answer: 2 (default)

3. **Session start — missing GG_PURPOSE: prompt or skip?**
   If `GG_PURPOSE` is not set, should the hook (a) prompt the user for a
   one-line purpose and record it, or (b) skip purpose tagging silently
   and log "no purpose set"? Option (a) enforces the habit; option (b)
   avoids blocking non-interactive sessions (CI, subagents). If unanswered
   I will use (b) — degrade gracefully, log the miss.
   → answer: a — prompt
