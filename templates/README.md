# gg artifact templates

Six boundary artifacts. Blank templates here; worked examples (one consistent
work item) in `../examples/specs/06-orchestrator/`.

## Conventions

- **Location:** each work item gets a directory: `specs/<NN>-<slug>/` containing
  `triage.md`, `spec.md` (human-owned), `plan.md` (agent-owned), `questions.md`,
  `escalations/<NNN>-<slug>.md`, `delegations/<NNN>-<slug>.md`,
  `drift/<YYYY-MM-DD>-<slug>.md`, `gates/<YYYY-MM-DD>.md`.
- **Frontmatter is for machines, body is for people.** The YAML keys are the
  trend dataset (steward greps them); the body must be legible to someone who
  has never heard of gg.
- **Brevity is a floor, not a ceiling.** A five-line escalation note is a good
  escalation note.
- **Every field must have a reader.** A field nobody reads gets deleted at
  harvest.

| Artifact | Written when | Primary reader |
|---|---|---|
| `triage.md` | a ticket or idea arrives; before any spec work | the sender (PM, lead) |
| `steward-read.md` | weekly light / monthly deep; after change burst; "I've lost the thread" | yourself (the perception-gap record); eventually steward the tool |
| `questions.md` | before any code, after receiving a spec | the spec author |
| `escalation.md` | a stopping condition fires mid-build | the lead / future you |
| `delegations/<NNN>-<slug>.md` | before spawning a subagent | the subagent; verified on return |
| `gate-report.md` | work is claimed done, before any PR | the PR reviewer, then steward |
| `drift-note.md` | milestone, interface touch, refactor, ADR conflict | steward, in aggregate |
