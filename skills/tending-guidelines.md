---
name: tending-guidelines
description: "Use when a pattern of failure recurs, something keeps going wrong, a gate fails in a way that should have been caught earlier, or during a weekly retro. Routes each lesson to the right layer (spec vs. guideline vs. skill), writes guidelines that are short and testable, tunes hooks when false positives or false negatives accumulate. The output is a dated guideline diff in git."
---

# Tending Guidelines

A repeating failure means a missing guideline, not a bad agent. When the same mistake appears twice, the correct response is not stronger resolve — it is a new rule that makes the mistake structurally harder. This skill is the mechanism.

## TRIGGER

Invoke this skill when:

- the same problem has appeared more than once ("why does this keep happening?")
- a gate fails in a way the agent should have caught before running gates
- something surprised you mid-build that the spec or plan should have anticipated
- a hook fired a false positive (blocked work that was legitimate)
- a hook missed something it should have caught (false negative)
- weekly retro, end-of-project review, "let's clean up CLAUDE.md"
- a pain point was awkward enough to note but didn't rise to an escalation

Do NOT trigger for a first-time failure — one occurrence is data; two is a pattern.

---

## Routing: spec, guideline, or skill?

Before writing anything, route the lesson to the right layer. Misfiled knowledge is the most common failure mode in this skill.

| Layer | What belongs here | Test |
|---|---|---|
| **Spec** | Per-project constraints; what's in and out of scope for a specific work item; reserved decisions; non-goals | Would this rule apply to every project, or only to this one? If project-specific, it's spec material. |
| **Guideline (CLAUDE.md)** | Durable behavioral rules that apply in any session in this project; things the agent should always or never do; Iron Laws | Is this a persistent pattern that will recur without a rule? Can it be stated as one short, testable sentence? |
| **Skill (gg plugin)** | Portable boundary behaviors that govern handoff protocols; behaviors that apply across projects, not just this one | Does it govern the protocol at a handoff (what/when/boundaries), or how the domain work is done? Boundary protocols are skills; how-knowledge is a guideline or trusted to the agent. |
| **Trust it to the agent** | Domain-specific implementation judgment, aesthetic choices, anything that changes by context | Would writing this rule constrain good judgment more than it prevents bad judgment? If so, don't write it. |

**The routing question:** state the lesson. Then ask: is this a rule I would want active in a project I don't control? If yes: skill or global guideline. Is it specific to this project's conventions? If yes: project-level CLAUDE.md entry. Does it depend on the specific work item? If yes: spec material (add it to the open spec if the work is ongoing, or note it for the next triage).

State the routing explicitly before writing anything. "This routes to CLAUDE.md because..." — the reason is part of the record.

---

## Writing a guideline

A good guideline is:

- **Short.** One sentence. Two at most. If it takes a paragraph to state, it's a principle, not a rule — write it in the project docs, not CLAUDE.md.
- **Testable.** You can look at a session and say "this rule was followed" or "this rule was violated." Vague rules ("be careful with X") are unenforceable and create false confidence.
- **Behavioral.** It describes an action or prohibition, not a property or goal. "Never run a destructive command without showing the command first" is behavioral. "Be cautious with destructive operations" is not.
- **Owned by a layer.** Every guideline states explicitly what happens when it fails: is it a habit the agent should correct? Does it need a hook? Does violation mean escalation?

**Structure for CLAUDE.md entries:**

```
## <Category>

- <Rule>. <One-clause consequence or rationale if non-obvious.>
```

Keep categories stable — adding a new category is a structural change that should be deliberate.

**Guideline quality checks before committing:**

1. Can this rule be violated without detecting it? If so, add a hook or gate reference.
2. Does this rule conflict with an existing one? Read the surrounding section before adding.
3. Is there an existing rule this makes redundant? Prune rather than duplicate.
4. Would this rule have caught the failure it was written in response to? If not, rewrite it until it would.

---

## Pruning stale rules

During a harvest session, read each existing guideline and ask: has this rule been exercised in the last N sessions (use cctx data if available; estimate otherwise)? A rule that never fires may mean:

- The agent already internalized it (good — the rule did its job; consider removing it as clutter)
- It's covering an edge case that hasn't come up (retain if the edge case is high-consequence)
- It's testing the wrong thing and never actually applies (remove — dead rules erode trust in active ones)

Delete a rule when its absence would not change behavior and its presence adds noise. State why in the commit message.

---

## Hook and tripwire tuning

gg's hooks enforce some rules mechanically. `tending-guidelines` owns the tuning of those mechanisms:

**False positives** (hook blocked work that was legitimate):

1. Record the false positive: what was the legitimate action, which hook fired, what was the rule?
2. Decide: is the rule wrong, or is the threshold wrong?
   - Wrong rule → update the rule in CLAUDE.md and the hook's matching logic together
   - Wrong threshold → change the threshold (e.g. failure counter THRESHOLD) and record the new value and why
3. A false positive is harvest input — it tells you the rule was over-specified

**False negatives** (hook should have fired, didn't):

1. Record the miss: what happened, which hook should have caught it?
2. Decide: is the observable proxy too narrow, or is the threshold too loose?
   - Narrow proxy → add a new observable or widen the matcher
   - Loose threshold → tighten it
3. A false negative is harvest input too — it tells you where the coverage gap is

In both cases: update the hook and the corresponding rule together. A hook that enforces a rule no longer in CLAUDE.md is orphaned enforcement. A CLAUDE.md rule with no hook is an honor system. Keep them paired.

Tripwire threshold changes go in git with a reason. "Changed failure_counter THRESHOLD from 2 to 3 — threshold of 2 was triggering on one flaky test + one retry (legitimate behavior in CI)" is a good commit message. "Tweaked threshold" is not.

---

## The harvest session

A harvest session is a short, structured review. Run it after pain, surprise, a gate failure that should have been caught earlier, or on a weekly cadence.

**Step 1: Collect candidates.** List the things that hurt this week or this project: failures that recurred, surprises that weren't in the spec, gate failures, false positives, false negatives. A candidate is anything you wouldn't want to face again without a rule change.

**Step 2: Route each candidate.** For each: spec, guideline, skill, hook change, or "trust the agent." State the routing.

**Step 3: Draft the changes.** Write new guidelines. Prune obsolete ones. Adjust hook thresholds.

**Step 4: Quality-check.** Apply the guideline quality checks above to every new rule.

**Step 5: Commit.** One commit per logical change. Commit messages state what changed and why.

**Step 6: Note what you're not doing.** Sometimes the right answer is "nothing — this was a one-off and a rule would over-fit." Record that decision. A future harvest will know not to re-examine this.

---

## Output

The artifact is a git commit (or PR if guidelines are shared) with:

- CLAUDE.md changes (additions, edits, deletions)
- Hook changes if any (with corresponding CLAUDE.md updates)
- A commit message that reads like a record, not a label

The diff is dated implicitly by git. There is no separate harvest artifact file — the commit history is the changelog.

---

## Rules

- Route before writing. Misfiled knowledge is the primary failure mode.
- One sentence per guideline. Testable or don't write it.
- False positives and false negatives are both harvest input — neither is more important.
- Hooks and their CLAUDE.md rules are maintained together. No orphaned enforcement; no honor-system rules.
- Prune rules that have done their job and now add noise.
- Commit messages are records, not labels.
- "Don't write a rule" is a valid harvest outcome. Note it.
