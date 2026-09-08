# Consolidated repair prompt

Dispatch at most once between the two ticket-wide review passes. Fill every `[BRACKET]`.

```text
Subagent (general-purpose; fixer):
  description: "Correct accepted ticket findings"
  prompt: |
    Work in [DIRECTORY] from [FIX_BASE].
    Original ticket/spec and approved plan: [SCOPE_AND_PLAN].
    Global Constraints: [GLOBAL_CONSTRAINTS].
    Saved findings and controller decisions: [FINDINGS_FILE].
    Task reports: [REPORT_FILES].
    Write the repair report to [FIX_REPORT_FILE].

    This is the single consolidated repair pass. Address the complete
    accepted list together; contested and deferred findings are context,
    not work orders. Do not launch reviewers, fixers, or approval workflows.

    For each accepted finding:
    1. Record the violated requirement and invariant the correction must
       preserve. Establish the defect with a failing regression test where
       practical, or concrete code-path evidence when execution is infeasible.
    2. Make the smallest correction within the original scope and constraints.
    3. For shared result, error, or state contracts, identify all affected
       consumers and propagation paths. Check the relevant boundaries.
    4. Run focused checks for both corrected and preserved behavior. Retain
       regression evidence so a later remedy cannot silently undo this one.

    Preserve every accepted invariant. If a remedy conflicts with an earlier
    decision or another accepted invariant, or needs a stronger safety
    guarantee, leave that finding unresolved and identify the conflicting
    finding IDs, evidence, and decision needed. Earlier findings may be
    mistaken; explain the contradiction rather than silently reversing them.
    Complete only repairs that can safely coexist within the agreed scope.

    Commit coherent corrections using repository conventions:
    - Group related findings; separate corrections to unrelated behavior.
    - Name the corrected behavior in each action-oriented commit subject.
    - In commit bodies, use one bullet per corrected finding ID describing
      the original defect and corrected behavior, including its trigger or
      consequence. Map each corrected ID to its correction commit.

    Reserve the full suite and typecheck for the controller's final evidence
    phase. Report every accepted ID, including findings left unresolved:
    - Finding → invariant → before/after evidence → commit or unresolved reason.
    - Affected consumers checked and remaining uncertainty.
    - Focused commands/results and final HEAD.
    - Possible correction-induced regressions and conflicting requirements.

    Stop after saving the report, even when findings remain unresolved.
```

Use `.tracer/implement/findings.md` for `[FINDINGS_FILE]` and `.tracer/implement/repair-report.md` for `[FIX_REPORT_FILE]`. Resolve scope, constraints, reports, and fixed SHAs from the approved plan and ledger.
