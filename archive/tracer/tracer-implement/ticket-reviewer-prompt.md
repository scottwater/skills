# Reviewer prompt

Use once for the complete agreed change. Use correction mode only after repairs actually change code; preferably resume the same reviewer. Fill every `[BRACKET]`.

```text
Review [BASE_SHA]..[HEAD_SHA] in [DIRECTORY].
Mode: [INITIAL_OR_CORRECTION].
Original requirements and safety limits: [SOURCE_AND_LIMITS].
Short plan: [PLAN_FILE].
Implementation evidence: [REPORT_FILES].
Diff package: [DIFF_FILE].
Prior findings/dispositions and repair report: [PRIOR_REPORTS_OR_NONE].
Save the review with checked HEAD to [REVIEW_REPORT_FILE].

Initial mode: check agreed behavior across the change. Planner-generated
mechanisms are not requirements unless explicitly chosen by the user. A simpler
implementation satisfying acceptance is valid. Examine unchanged code only to
resolve a concrete risk at a named caller or contract.

Correction mode: reconcile prior findings and verify the repairs, preserved
invariants, and affected behavior. Use the original diff only as context for a
specific doubt. Do not restart a full-scope audit. Report newly demonstrated
regressions, retaining prior finding IDs and explaining any proposed reversal.

Reports are claims to check against code and evidence. Material findings need
a reachable trigger, violated requirement, and current consequence: incorrect
behavior, security/data loss, silent failure, or tests unable to detect broken
required behavior. Give each a stable ID, file:line, severity, evidence, and
invariant a correction must preserve. Combine overlapping findings.

Record optional polish, speculative variants, and stronger guarantees outside
the agreed limits separately. Do not require a generic framework or extra tests
merely because the plan mentioned them. Zero findings is a valid result.

Run focused checks only to resolve a specific doubt not answered by available
evidence. Preserve tracked files, index, and HEAD; write only the ignored review
report and safe disposable evidence. Return findings without repairs, nested
agents, or another workflow.

Report:
- Approved | Concerns | Needs attention
- Actionable findings with evidence, or None
- Non-blocking concerns and material scope questions
- Correction mode: prior IDs resolved / unresolved / unverified, with evidence
- Checks run and required behavior that could not be verified

Approved: required behavior verified and no findings or concerns remain.
Concerns: required behavior verified; only non-blocking concerns remain.
Needs attention: an actionable finding, material conflict, or required evidence
remains unresolved. Stop after the report; this is not authority for more work.
```

For initial mode, use `scripts/review-package` from the immutable base to current HEAD and save `.tracer/implement/review-1.md`. For correction mode, package only the repair's starting and ending SHAs, supply the initial package for reference, and save `.tracer/implement/review-2.md`. No repairs means no correction review.
