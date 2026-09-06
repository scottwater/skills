# Round 1 — Delivery reviewer prompt

Dispatch once after all tasks are implemented. One reviewer covers requirements and material code quality across the accepted delivery. Fill every `[BRACKET]`.

```text
Subagent (general-purpose; fresh reviewer):
  description: "Review delivery against agreed requirements"
  prompt: |
    Review [BASE_SHA]..[REVIEW_HEAD] in [DIRECTORY].
    Original request/spec/tickets: [SCOPE_SOURCES].
    Plan and agreed limits: [PLAN_FILE].
    Task reports: [REPORT_FILES].
    Read the cumulative diff package once: [DIFF_FILE].

    This is round 1 of a delivery-wide two-round budget. Return findings
    to the controller. Do not fix code, delegate, or invoke another review.
    Keep the working tree, index, and HEAD unchanged.

    Reports and comments are claims, not proof. Check the implementation
    against the original requirements, observable behavior, and repository
    standards. Inspect callers or unchanged code when a concrete risk
    requires it; state what risk justified that inspection.

    Look for missing or misunderstood requirements, incorrect behavior,
    silent failures, data/security risks, and tests that cannot detect
    broken required behavior. For every material finding provide:
    - Stable ID: C1, C2... for severe current impact; I1, I2... for other
      material defects. Use M1, M2... for separate non-blocking follow-ups.
    - File:line and the violated requirement or invariant.
    - A reachable trigger and current consequence.
    - A reproduction or concrete code-path evidence; identify uncertainty.
    - The behavior a correction must preserve, not just a preferred patch.

    Code smells, duplication, warnings, and unusual fault combinations do
    not establish materiality by themselves. Tie them to a current defect
    or record a follow-up. A stronger concurrency, durability, platform, or
    threat-model guarantee outside the agreed limits is a scope proposal.
    Surface contradictory requirements instead of silently changing them.

    Run focused checks to resolve concrete doubts. Reserve the full suite
    and end-to-end proof for the closing phase.

    Return:
    - Requirements assessment: met / material gaps / unverified claims.
    - Material findings, with the evidence fields above; combine overlap.
    - Non-blocking follow-ups and scope questions, kept separate.
    - Checks performed and limits of the review.

    Zero findings is a valid result. Stop after this report; the controller
    adjudicates it and owns the one repair pass.
```
