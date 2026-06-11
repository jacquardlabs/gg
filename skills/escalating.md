---
name: escalating
description: "Use when a stopping condition fires during a build: repeated failure, reserved decision reached, contract change required, structural drift detected. Writes an escalation note with situation/options/recommendation, continues unblocked work, ends the session gracefully when all threads are blocked."
---

# Escalating

Escalation is not failure. It is the mechanism by which a blocked thread stays honest and unblocked threads keep moving. The stopping conditions below are the moments when grinding forward causes more damage than pausing.

<HARD-GATE>
When a stopping condition fires, do NOT attempt another workaround on the blocked thread. Write the escalation note, then continue with unblocked work or end the session. Continuing to grind is the only wrong move.
</HARD-GATE>

## TRIGGER

Invoke this skill when any of the following fires during a build:

**Automated signals:**
- `failure_counter` warns that the same command has failed consecutively (≥ threshold) — you have been attempting the same fix and it is not working
- A plan revision would change a requirement, drop a gate, or modify a spec-named interface — this is a contract change, not replanning

**Agent-recognized signals:**
- You have reached a decision listed in the spec's "Reserved for human" section
- You cannot proceed on a plan item without absorbing a decision the spec forbids you to make
- A dependency you assumed would exist does not exist and creating it changes the contract
- Implementing a requirement would violate a non-goal
- A requirement contradicts another requirement and the questions round-trip did not resolve it

**Structural signals:**
- An edit would touch a spec-named interface in a way not described in the spec
- The implementation path requires a new external dependency the spec doesn't reserve for the human (if the spec reserves it, escalate; if the spec is silent and it's clearly a reserved-class decision, escalate anyway)

**When NOT to escalate:**
- You can solve the problem by choosing a different technical approach within the spec's constraints
- A test is failing because of a bug you wrote — fix the bug
- An ambiguity the questions round-trip already resolved — apply the recorded answer
- Something is harder than expected — difficulty alone is not a stopping condition

---

## What escalation means

**Stop means stop on this thread.** Not globally. The blocked thread pauses; every other plan item that doesn't depend on this thread continues. Only when ALL remaining plan items are blocked — each appears in some open escalation's `blocks` list — does the session end.

This distinction is load-bearing. A single blocked thread that halts the whole session is an alibi, not a stopping condition. The escalation note says explicitly what continues meanwhile.

---

## Writing the escalation note

File: `specs/<NN>-<slug>/escalations/<NNN>-<slug>.md` (create the `escalations/` directory if it doesn't exist; assign the next sequential NNN).

Follow `templates/escalation.md` exactly:

**Frontmatter:**
- `status: open` — do not flip this yourself; the human resolves it
- `blocks: [P3, P5]` — plan items that cannot proceed until this resolves
- `scope: [path/to/file.py]` — files this thread owns; edits to these paths while the escalation is open get flagged by the hook

**Body:**

**Situation.** What stopped this thread. For a repeated-failure escalation: what attempt 1 and attempt 2 were and the hypothesis for why both failed. For a reserved-decision escalation: the decision, which spec item triggered it, and what the options are. Two to four sentences is the right length.

**Options.** Two to four options with their tradeoffs. Be concrete — each option names what changes, what risk it carries, and what it unblocks. Do not list options that are obviously worse; list the genuine alternatives.

**Recommendation.** Pick one. State it and give one reason. An escalation note without a recommendation transfers more work to the human than necessary.

**Continuing meanwhile.** List the plan items that continue while this escalation is open. If nothing continues, say so — "nothing unblocked; session ends after this note."

---

## After writing the note

1. **Continue unblocked work.** Check the plan: which items do not depend on `blocks`? Proceed with those.

2. **If all threads are blocked:** End the session gracefully. The closing message is:

   > Blocked on N escalation(s): [list titles]. No unblocked plan items remain. Session ends here. Open notes: [filenames].

   Do not idle, rationalize a workaround, or attempt the blocked work again. The escalation is the output of this session.

3. **Do not edit files in `scope` while the escalation is open.** The hook will flag these edits; avoid triggering false alarms on work the human hasn't reviewed yet.

---

## Resolution protocol

When the human resolves an escalation:
- They fill in the `**Resolution.**` line in the note
- They flip `status: resolved`
- You read the resolution, update the plan if the resolution changes the approach (re-check verification mapping), and unblock the affected plan items

If the resolution changes the contract (drops a requirement, modifies an interface), the human updates the spec first. Then you continue.

---

## Escalation vs. plan revision

These look similar but are distinct:

| Situation | Correct action |
|---|---|
| Need to add a file to the manifest to serve an existing requirement | Plan revision (free, logged) |
| Need to change the approach to meet a requirement | Plan revision (free, logged) |
| Need to drop a requirement or change an interface | Escalation — contract change |
| Hit a reserved decision from the spec | Escalation — reserved decision |
| Same command failed twice and you're out of hypotheses | Escalation — consecutive failure |
| A new external dependency is required | Escalation if reserved-class; plan revision note if clearly within-scope |

When in doubt, escalate. A false alarm costs a two-minute conversation. Absorbing a decision that should have been escalated costs a refactor.

---

## Output artifact

| Artifact | Path | Status lifecycle |
|---|---|---|
| Escalation note | `specs/<NN>-<slug>/escalations/<NNN>-<slug>.md` | `open` → `resolved` (human fills) |

Gates refuse to pass work overlapping an open escalation (the `running-gates` skill checks for unresolved escalations in the work item's `escalations/` directory before attesting completion).

---

## Rules

- Stopping conditions stop the thread, not the session. Unblocked threads continue.
- Write the note before doing anything else on the blocked thread.
- `blocks` and `scope` frontmatter keys are not optional — the hooks use them.
- Every note has a recommendation. Transferring the decision is not the same as transferring the work.
- When all threads are blocked: end the session with the closing message. Do not idle.
- Gates refuse work overlapping open escalations. Resolve before claiming done.
