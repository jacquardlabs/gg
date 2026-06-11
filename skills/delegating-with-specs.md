---
name: delegating-with-specs
description: "Use before spawning any subagent. Every delegation gets a mini-spec (goal, verification, non-goals, guidelines, reserved decisions). Subagent output is verified at the boundary — never trusted on the agent's say-so. Reserved decisions propagate and cannot be absorbed by a subagent. Enforced by a PreToolUse hook."
---

# Delegating with Specs

A delegation without a spec is a wish with a subagent attached. The same problems that make informal specs between humans fail — ambiguous scope, untested output, unspoken constraints — apply to agent-to-agent handoffs, at higher speed.

<HARD-GATE>
Do NOT spawn a subagent without writing a mini-spec first. The PreToolUse hook on the Agent tool enforces this: a delegation prompt missing Goal, Verification, or Non-goals labels is rejected.
</HARD-GATE>

## TRIGGER

Invoke this skill when:

- you are about to spawn a subagent (Agent tool, dispatching-parallel-agents, etc.)
- a plan item says "delegate X to a subagent"
- the work you are about to hand off has a distinct goal that can be verified

Do NOT trigger for calls to single-purpose tools (bash commands, file reads, API calls). Delegation is specifically the act of spawning an agent with a goal.

---

## Writing the mini-spec

File: `specs/<NN>-<slug>/delegations/<NNN>-<slug>.md` (sequential NNN; slug from the goal).

Also paste the mini-spec directly into the delegation prompt — the file is the record; the prompt is the enforcement.

Follow `templates/mini-spec.md`. Required fields:

**Goal:** One sentence. A measurable output, not an activity. "Implement X so that Y" is a goal; "work on X" is not. If you cannot state the goal as a measurable output, the delegation is not ready.

**Verification:** How the output will be checked. At least one concrete, mechanical check: a test to run, a behavior to observe, a file to inspect, an assertion to make. This is what you will run when the subagent returns — it is not a subjective judgment. "Looks good" is not verification.

**Non-goals:** What the subagent must not do. At least one. Non-goals prevent a well-intentioned subagent from expanding scope in a direction that seems logical from inside the task. If you can't name a non-goal, you haven't bounded the task.

**Guidelines:** Rules inherited from CLAUDE.md apply by default. List any overrides or additional constraints specific to this delegation. If there are none, write "Standard CLAUDE.md guidelines apply."

**Reserved decisions:** Decisions propagated from the parent spec that the subagent cannot make. If reached: the subagent escalates, it does not absorb. If the parent spec has none, write "None; escalate any decision that affects the parent spec's interfaces."

---

## Verification at the boundary

When the subagent returns, run the Verification check in the mini-spec before accepting the output. Do not trust the subagent's claim of completion.

If the verification passes: accept the output and continue.

If the verification fails:
- Do not re-delegate the same task without a revised mini-spec
- If the failure reveals a problem with the mini-spec (underspecified goal, wrong verification), revise the mini-spec first, then re-delegate
- If the failure is a bug in the subagent's output, report it as a plan-item failure (same as a first-party failure) and route accordingly

A subagent that returns claiming "done" without meeting the Verification criteria is exactly the same situation as the agent claiming "done" before running gates. The response is the same: run the check, trust the check.

---

## Reserved decisions

Reserved decisions from the parent spec propagate into every delegation. The subagent inherits the constraint: it does not make reserved decisions, it escalates them.

If a subagent returns having absorbed a reserved decision (implemented something the spec reserved for the human), that is a gate failure — the output must be revised or reverted until the human makes the decision.

Never narrow or drop a reserved decision in a delegation. If the parent spec says "storage backend is reserved for human," the mini-spec cannot say "use Postgres" without explicit human authorization.

---

## The hook

The PreToolUse hook checks every Agent tool invocation for the presence of `Goal:`, `Verification:`, and `Non-goals:` labels in the prompt. A delegation missing any of these is rejected with a message explaining what is missing.

The hook is enforcement, not guidance. If it fires:
1. Write the mini-spec file
2. Paste the mini-spec into the delegation prompt
3. Re-attempt the delegation

Do not work around the hook by adding dummy labels. The hook tests for the labels; you are testing for the content.

---

## Output artifacts

| Artifact | Path | Notes |
|---|---|---|
| Mini-spec | `specs/<NN>-<slug>/delegations/<NNN>-<slug>.md` | Permanent record; also pasted into the prompt |

---

## Rules

- No delegation without a mini-spec. The hook enforces this.
- Goal is a measurable output, not an activity.
- Verification is mechanical, not subjective.
- Non-goals: at least one. If you can't name one, the task is unbounded.
- Reserved decisions propagate. They are never narrowed or absorbed.
- Verify at the boundary. A subagent's "done" is not a completion signal.
- Verification failure → fix the mini-spec or the output; never accept on the claim.
