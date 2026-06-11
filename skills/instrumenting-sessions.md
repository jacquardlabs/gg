---
name: instrumenting-sessions
description: "Hybrid skill: session-start is a deterministic hook (cctx watch, purpose capture, MCP manifest verification); session-end self-autopsy is a skill (what shipped, cost, deviations, harvest candidates, open threads). The session-start hook runs automatically. Invoke this skill explicitly at session end or when asked to wrap up."
---

# Instrumenting Sessions

Sessions are the unit of work. The session-start hook arms the instrumentation; the session-end skill reads what it collected and turns it into a record the human and steward can use. Together they close the loop between what was intended and what actually happened.

## How the two halves work

**Session-start (hook — automatic).** The `session_start.py` hook runs at SessionStart. It:
1. Starts a `cctx watch` subprocess against the current transcript (degrades gracefully if cctx is absent)
2. Captures the session purpose from `GG_PURPOSE` env var, or prompts interactively if stdin is a tty
3. Writes `.gg/state/session.json` with session_id, transcript_path, and purpose
4. Verifies the MCP/skills manifest against the lockfile (see MCP verification section)

Nothing in session-start requires this skill to be invoked — it runs automatically.

**Session-end (skill — this document).** Invoke when the session is finishing or when the user says "wrap up," "what did we do," "end the session," or "let's close out."

---

## TRIGGER (session-end)

Invoke this skill when:

- the user says "wrap up", "close out", "what did we do", "end the session"
- a plan is complete and gates have run (the session is naturally ending)
- all threads are blocked (escalations ended the session — generate the record before closing)
- you are about to lose context and want to leave a clean handoff

Do NOT trigger at session-start — that's the hook's job. This skill is the session-end half only.

---

## Session-end self-autopsy

The self-autopsy is a judgment artifact, not a mechanical report. It answers the questions cctx cannot: what was the intent, what changed from the plan, what deserves a follow-up.

The autopsy is not required to go anywhere specific — it is a self-record. If the session produced work that will be reviewed (a PR, a gate report), attach or reference the relevant parts. The full autopsy is for the human and for steward.

**What to cover:**

**What shipped.** List what was actually completed: plan items marked done, artifacts created, tests passing. Be specific about what exists now that didn't before. Avoid vague summaries ("made progress on X").

**Cost and consumption.** If cctx watch was running: note what it reported (retry loops, scope creep signals, cost estimate). If cctx was absent, estimate: how many turns, any patterns of repeated attempts?

**Deviations from the plan.** What changed between the initial plan and what was built? Plan revisions are logged in `plan.md` — read them. Note any deviations that were not logged (a sign something should have been logged but wasn't).

**Open threads.** What is unfinished? List open escalations by id and title. List plan items not yet started or in progress. Any non-escalation blockers that came up.

**Harvest candidates.** What surprised you? What would you do differently? What pattern appeared more than once? Each item is a candidate for `tending-guidelines`. State them now while the session is fresh — the harvest session can route them later.

---

## MCP manifest verification (session-start hook)

The session-start hook verifies MCP server tool descriptions and installed skills against a lockfile (`.gg/state/mcp-lockfile.json`). This is a security check, not a configuration audit.

**Why this matters.** MCP tool descriptions are attacker-controlled text that lands in the model's context. A server can push a poisoned update between sessions — the client reloads descriptions without re-prompting, and the change is invisible (rug-pull attack; CVE-2025-54136 class). The lockfile captures what was approved; the hook detects what changed.

**On session-start:**
- If no lockfile exists: the hook writes one from the current state and continues. No blocking.
- If a lockfile exists and current state matches: session proceeds normally.
- If a lockfile exists and current state differs: **the hook reports the drift and blocks.** This is a blocking signal — not a warning.

The blocking message names which servers or descriptions changed. The human decides whether to approve the change (run `gg mcp-approve` to update the lockfile) or investigate before continuing.

**Manifest drift is a blocking signal, not a config curiosity.** A poisoned or unexpectedly updated tool description is an attack surface. The correct response to unexpected drift is to investigate, not to dismiss and continue.

---

## Session-start graceful degradation

The session-start hook degrades gracefully when:
- **cctx is absent**: `cctx watch` is skipped; `.gg/state/session.json` is still written; a one-line note is logged to stderr. Session proceeds.
- **No tty for purpose prompt**: purpose is recorded as null; session proceeds. Set `GG_PURPOSE` in your shell profile to avoid the gap.
- **No lockfile yet**: written fresh from current state on first run; session proceeds.

Graceful degradation means gg's hooks never block a session from starting due to an absent dependency. cctx enriches; it is never load-bearing.

---

## Output

The self-autopsy is conversational — spoken or written in the session, not filed as a separate artifact. If the human wants it persisted, write it as a brief session note in `steward/reads/` or hand it off for the next `steward-read.md`.

What does get filed, automatically, by the hook: `.gg/state/session.json` (machine-readable session record for cctx and steward). Don't edit this file manually.

---

## Rules

- Session-start is automatic. Do not invoke this skill at session-start.
- Session-end autopsy is a judgment artifact, not a checklist. Cover what was real, skip what was routine.
- MCP manifest drift is a blocking signal. Investigate; do not dismiss.
- cctx absence degrades gracefully — gg never blocks on cctx presence.
- Harvest candidates are named at session-end while the session is fresh. Routing happens later in `tending-guidelines`.
- The full session-end record is for the human and steward. Relevant parts attach to PRs or gate reports; the rest is internal.
