---
description: "Orientation and next-action routing for gg. Use when you don't know what stage you're at, want to know what to do next, or need a handoff to the right skill."
---

You've been asked to orient using gg. Read the current work item state and tell the user exactly what stage this session is at and what to do next.

## Step 1: Find the active work item

Look in `specs/` for work item directories. If the user mentioned a specific ticket or feature, find the matching directory (by slug or number). If nothing is active or you can't tell, scan all directories and report their stages.

## Step 2: Read the work item state

For each active work item, check what exists:

| File/dir | What it tells you |
|---|---|
| `triage.md` | Verdict exists? If `DEFER` or `DONT-BUILD`, this item is closed. |
| `spec.md` | Has a spec been authored and confirmed? |
| `questions.md` | `status: awaiting-answers` → waiting on human. `status: answered` → proceed. |
| `plan.md` | Does a plan with a manifest block exist? |
| `escalations/*.md` | Any `status: open`? → blocked threads. |
| `gates/*.md` | Any gate reports? What was the last verdict? |

## Step 3: Route to the right stage

| State | What to do |
|---|---|
| No `specs/` directory or no active work item | `writing-specs` — nothing to build yet; start with triage |
| Triage verdict is DEFER or DONT-BUILD | This work item is closed; pick a different one or start fresh |
| No triage verdict | `writing-specs` Phase 1 — triage this idea first |
| Triage done (BUILD-ish), no `spec.md` | `writing-specs` Phase 2 — author the spec |
| `spec.md` exists, no `questions.md` | `decomposing-specs` Phase 1 — write the questions report |
| `questions.md` with `status: awaiting-answers` | Waiting on human answers; nothing to do until they reply |
| `questions.md` answered, no `plan.md` | `decomposing-specs` Phase 2 — write the plan |
| `plan.md` exists, open escalations | Resume unblocked plan items; surface open escalation titles |
| `plan.md` exists, no open escalations, plan not complete | Continue the next incomplete plan item |
| All plan items complete, no gate report | `running-gates` — verify before claiming done |
| Gate report exists with `verdict: fail` | Fix the failures; reopen the failed plan items |
| Gate report exists with `verdict: pass` | Ready for PR; use `finishing-a-development-branch` |

## Step 4: Report

Tell the user in two to four sentences:
1. What work item this is (name and directory)
2. What stage it's at and why (cite the file that tells you)
3. The next concrete action
4. If multiple work items exist: list all of them with their stages

If there are open escalations: list each one by title and id. The user may not remember what they were.

If the state is ambiguous (e.g., a plan exists but some items lack clear done/not-done status): say so and ask what's been completed so you can proceed accurately.
