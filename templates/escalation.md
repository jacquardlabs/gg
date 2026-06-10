---
type: escalation
spec: <NN>-<slug>
id: <NNN>                     # sequential within this work item
date: <YYYY-MM-DD>
status: open                  # open | resolved
blocks: [<plan-item>, ...]    # plan items that cannot proceed
scope: [<path>, ...]          # files this thread owns; edits here while open get flagged
---
# <One-line description of what stopped this thread>

**Situation.** <What happened. If this is a repeated-failure escalation: what
attempt 1 and attempt 2 were, and the current hypothesis. Two to four
sentences.>

**Options.**
1. <Option> — <tradeoff>
2. <Option> — <tradeoff>

**Recommendation.** <Option N>, because <one clause>.

**Continuing meanwhile.** <Plan items unaffected by this thread, or "nothing —
session ends if no unblocked work remains".>

**Resolution.** _(filled by the human; flips status to resolved)_

<!--
- `scope` powers enforcement: edits to those paths while status is open get
  flagged, and gates refuse to pass work overlapping an open escalation.
- `blocks` powers the session-end rule: when every remaining plan item appears
  in some open escalation's blocks, end the session gracefully.
- Five lines total is fine. Do not pad.
-->
