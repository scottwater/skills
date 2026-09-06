# Consolidated repair prompt

Dispatch at most once, between the two delivery-wide review rounds. Fill every `[BRACKET]`.

```text
Subagent (general-purpose; fixer):
  description: "Correct accepted delivery findings"
  prompt: |
    Work in [DIRECTORY] from [FIX_BASE].
    Original scope and limits: [SCOPE_AND_PLAN].
    Accepted findings and controller decisions: [FINDINGS_FILE].
    Implementer reports: [REPORT_FILES].
    Write your repair report to [FIX_REPORT_FILE].

    This is the delivery's single repair pass. Address the complete accepted
    material list together; contested and deferred findings are not work
    orders. Do not start another reviewer, fixer, or approval workflow.

    For each accepted finding:
    1. Establish the violated behavior with a failing regression test where
       practical, or concrete code-path evidence when execution is not
       feasible. Record the invariant the fix must preserve.
    2. Make the smallest correction within the agreed requirements.
    3. When changing a shared result, error, or state contract, identify all
       affected consumers and propagation paths, including analogous code
       that relies on the same contract. Verify each relevant boundary;
       avoid unrelated architectural cleanup.
    4. Run focused checks for the corrected and preserved behavior. Retain
       regression evidence so a later remedy cannot silently undo this one.

    If a remedy conflicts with another accepted invariant or requires a new
    safety guarantee, record the finding as unresolved and name the decision
    needed. Preserve every accepted invariant while completing the repairs
    you can safely make within this pass.

    Commit coherent corrections using repository conventions. Account for
    every accepted finding ID in the report below. Reserve the full suite
    for closing verification.

    Report:
    - Finding → invariant → before/after evidence → commit or unresolved reason.
    - Affected consumers checked and any remaining uncertainty.
    - Focused commands/results and final HEAD.
    - Possible correction-induced regressions or conflicting requirements.

    Stop after the report, including when findings remain unresolved.
```
