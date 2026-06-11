---
type: steward-read
date: <YYYY-MM-DD>
depth: <light | deep>        # light = parts 1–2 (~20 min); deep = all three (~60–90 min)
system: <what system / codebase this covers>
gap-score: <N/M>             # misses / total items surfaced — filled in after part 2
intent-refresh-needed: <yes | no | maybe>   # deep only; omit for light
---

<!--
SEQUENCE IS LOAD-BEARING.
Complete Part 1 entirely before opening any gg artifacts, git logs, or dashboards.
The value of this practice is the gap between your unaided read and what actually
happened — that gap is only measurable if Part 1 was written blind.
-->

# Part 1 — Own read
*Write this before looking at any data.*

**Trigger:** <why now — weekly, monthly, change burst, "I've lost the thread">

**What I think the current state is:**
<Your unaided model of the system: architecture, recent changes, where things
stand. Two to six sentences. Not a summary of docs — what you actually believe
is true right now.>

**What I think changed since last read (<date> or "first read"):**
<Changes you're aware of. Work items shipped, refactors, PRs merged. Write
what you remember, not what you'd look up.>

**Where I'd worry:**
<Hot spots: areas of complexity, recent churn, deferred decisions, or things
you're less certain about. At least one.>

**What I'm uncertain about:**
<Open questions you have about the system right now. These are the candidates
to check in Part 2.>

---

<!--
STOP HERE. Open gg artifacts now: drift notes, gate reports, guideline
changelog (specs/<NN>-<slug>/drift/, gates/, ../CLAUDE.md history).
For a deep read: also compute the trend metrics below.
-->

# Part 2 — Compare
*Fill in after reading gg artifacts.*

**Artifacts read:**
- [ ] Drift notes since last read: `specs/*/drift/`
- [ ] Gate reports since last read: `specs/*/gates/`
- [ ] Guideline changelog: `git log -- CLAUDE.md`
- [ ] Open escalations: `specs/*/escalations/`

**Confirmed:** <What your own read got right — matches between Part 1 and artifacts.>

**Missed:** <What artifacts surfaced that wasn't in your Part 1. These are the
perception-gap data points. Be specific: what exactly did you not know?>

**False positives:** <Things you believed in Part 1 that artifacts contradict or
qualify. What did you think was true that isn't?>

**Perception-gap summary:**
<One to three sentences: the most significant gap between what you thought and
what the artifacts show. This is the sentence steward will eventually read.>

---

# Part 3 — Drift & trends
*Deep read only. Skip for light.*

**Trend metrics** *(compute from git history — see docs/steward-metrics.md):*

| Metric | This period | Last period | Direction |
|---|---|---|---|
| Duplication delta | | | ↑ / ↓ / — |
| 30-day revert rate | | | ↑ / ↓ / — |
| Refactor ratio | | | ↑ / ↓ / — |
| Diff-size / fix-size | | | ↑ / ↓ / — |

**Claimed-vs-verified gap trend:**
<From gate reports: is the gap between agent completion claims and verified
results growing, shrinking, or stable? Name the direction, not just a number.>

**Repeat harvests:**
<Any lesson that keeps re-appearing in the guideline changelog — something
that was "fixed" but keeps recurring. This is the signal for a structural
problem, not a missing rule.>

**Intent refresh needed?**
<Does any trend suggest the ADRs or system charter are no longer accurate?
If yes: name the specific decision that needs revisiting. This feeds step 10.>

<!--
File at: steward/reads/YYYY-MM-DD-<light|deep>.md
Cadence: weekly light, monthly deep, and on any of these triggers:
  - after a change burst (3+ PRs merged in a week)
  - "I've lost the thread"
  - before a major architectural decision
  - when the claimed-vs-verified gap in gate reports widens

The gap-score frontmatter key (misses/total) is the machine-readable
perception-gap datum steward will eventually trend. Fill it in after
completing Part 2: count how many distinct items the artifacts surfaced
(total), and how many of those you hadn't mentioned in Part 1 (misses).
Example: you write 4 items in "Missed" out of 10 items total in the
artifacts → gap-score: 4/10.
-->
