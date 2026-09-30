# Consolidated repair prompt

Use at most once after accepted review findings, preferably in the existing implementation context. Fill every `[BRACKET]`.

```text
Correct accepted findings in [DIRECTORY] from [FIX_BASE].
Original requirements and safety limits: [SOURCE_AND_LIMITS].
Findings and controller dispositions: [FINDINGS_FILE].
Implementation evidence: [REPORT_FILES].
Agreed focused checks: [CHECKS].
Save results to [FIX_REPORT_FILE].

Address the accepted list together. Deferred/contested findings are context,
not work orders. For each accepted finding, establish the broken behavior with
a regression test where practical, make the smallest correction, and verify
corrected and preserved behavior. Inspect affected consumers when changing a
shared contract; keep unrelated cleanup outside this pass.

Preserve explicit decisions and accepted invariants. If a fix conflicts with
one or requires additional custom infrastructure or a stronger safety guarantee,
report the conflict to the controller with its practical impact, recommended
next action and trade-off, and exact decision or input needed to unblock it.
Complete only repairs that can safely coexist within the agreed scope.

Run the agreed focused checks and commit coherent corrections using repository
conventions. Report every accepted finding ID: resolved change and before/after
evidence with commit, or unresolved reason. Include affected behavior checked,
commands/results, final HEAD, and possible regressions.

Stop after the report. No nested agents, extra review, or additional repair pass.
```

Use `.tracer/implement/repair-report.md` for the report. Findings may live in the initial review or a separate findings file if needed; pass the actual path rather than creating duplicate bookkeeping. A correction-only review follows changed code, not a fresh full-scope audit.
