---
type: questions
spec: <NN>-<slug>
date: <YYYY-MM-DD>
status: awaiting-answers      # awaiting-answers | answered
---
# Questions before work starts

Reply inline at each "answer:". Each question states what happens if I guess.

<!--
Rules:
- Numbered throughout, so answers can be given by number.
- Reserved decisions come FIRST — only the human can unblock those.
- Every question in "Open questions" carries a default-if-unanswered, so
  silence becomes a logged decision instead of a blocker.
- No code is written until status flips to "answered".
-->

## Needs your decision (reserved for you)

1. **<The decision, as a question.>** <Why the spec reserves it; one-line
   tradeoff per option.>
   Recommendation: <option, one clause of why>. → answer:

## Open questions

2. **<The ambiguity, as a question.>** <Where it appears in the spec; what
   depends on it.> If unanswered I will <default>, and that becomes the gate.
   → answer:

## Contradictions

3. **<Requirement A> conflicts with <requirement B / non-goal>:** <one
   sentence on how>. Which wins? → answer:
