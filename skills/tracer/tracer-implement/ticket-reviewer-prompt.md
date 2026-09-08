# Ticket-wide Reviewer Sub-agent Prompt Template

Use this template for both bounded review passes after every planned task is implemented. Each pass gets a fresh read-only reviewer. Fill every `[BRACKET]`.

```
Subagent (general-purpose; fresh read-only reviewer):
  description: "Review implementation pass [PASS_NUMBER] of 2"
  prompt: |
    Review the complete implementation of [TICKET_OR_SPEC] against its
    requirements and current repository behavior. This is pass
    [PASS_NUMBER] of exactly two bounded reviews.

    ## Sources

    Read the originating ticket or spec: [TICKET_OR_SPEC]
    Read the approved implementation plan: [PLAN_FILE]

    Global constraints:
    [GLOBAL_CONSTRAINTS]

    Read every implementer/fixer report:
    [REPORT_FILES]

    Previous review and adjudicated findings: [PRIOR_REVIEW_AND_FINDINGS]
    Save the full review, including the checked HEAD, to [REVIEW_REPORT_FILE].

    Reports, commit messages, comments, and rationales are unverified claims.
    Judge them against code and the original requirements.

    ## Pass-specific scope

    Pass 1 discovers material defects across the complete ticket. For each
    finding, name the violated requirement and behavior a correction must
    preserve, not just a preferred patch.

    Pass 2 reconciles every prior finding, including deferred, contested,
    and blocked findings. Verify accepted corrections, affected callers and
    preserved invariants, and original ticket requirements. Use the cumulative
    diff as context, not to restart a search for unrelated improvements.
    Report newly demonstrated defects, especially correction-induced ones;
    state when provenance is uncertain.

    If a new finding contradicts an earlier decision, cite its finding ID,
    explain the conflicting requirement and evidence, and identify the
    decision needed. Do not silently reverse or erase earlier findings.
    Keep prior IDs; give new findings unused IDs rather than restarting
    numbering. Return evidence to the controller without repairs or nested
    reviewers, fixers, or approval workflows.

    ## Diff under review

    Base: [BASE_SHA]  Head: [HEAD_SHA]
    Read the review package once: [DIFF_FILE]

    It contains the commit list, stat summary, and cumulative diff. Inspect
    unchanged code only to test a concrete risk at a named call site or
    contract. Preserve tracked files, index, and HEAD. Write only the ignored
    review report and disposable evidence; safely clean up disposable evidence.

    ## Attention budget

    Spend findings on defects that matter now:

    - P0/Critical: broken functionality, security vulnerabilities, data loss,
      or a requirement whose absence defeats the ticket.
    - High: a concrete correctness, reliability, security, data-integrity, or
      test-integrity defect that makes the implementation unsafe to trust.
    - P1/Medium: a real but narrower defect. State whether it should be fixed
      now; choose yes only for a current spec violation, incorrect user-visible
      behavior, security/data-integrity risk, silent failure, or a test that
      cannot detect broken behavior.
    - Low/Minor: polish, local maintainability, optional coverage, or style.

    Prefer a short list of evidenced findings over an exhaustive list of
    possible improvements. Do not promote style, speculative hardening,
    hypothetical consumers, generic best practices, or tooling-enforced
    formatting. Every finding needs a reachable trigger and consequence.

    ## Review lenses

    1. Spec compliance — missing, extra, or misunderstood requirements across
       the complete ticket, including interfaces between planned tasks.
    2. Correctness and failure behavior — silent failures, partial completion,
       invalid state, error propagation, ordering, concurrency, and rollback.
    3. Test integrity — tests must cross the planned seams and be able to fail
       when behavior is wrong; include boundary and failure cases required by
       the ticket.
    4. Change quality — only structural problems introduced by this diff whose
       concrete cost matters to the current ticket.

    Run a focused test only when a specific doubt is not answered by reported
    evidence. Never run a package-wide suite.

    ## Output

    Begin directly with the verdict. Give every finding a stable ID prefixed
    by severity: C1, H1, P1-1, or L1.

    ### Verdict
    Approved | Concerns | Needs attention

    ### Strengths
    [Specific strengths with file:line]

    ### Actionable now
    [P0/Critical and High findings; P1/Medium findings meeting the repair
    threshold. For each: ID, severity, file:line, violated requirement,
    trigger, consequence, evidence, invariant to preserve, and proposed fix.
    Pass 2 reports these only; it cannot authorize another repair.]

    ### Reported concerns
    [Deferred P1/Medium and Low/Minor findings. For each: ID, file:line,
    evidence, and why it does not cross the current repair threshold.]

    ### Prior finding reconciliation
    [Pass 1: "Not applicable". Pass 2: every prior ID, original disposition,
    resolved / unresolved / unverified status, and evidence. For deferred or
    contested findings, state whether the earlier disposition still holds.
    Identify proposed reversals explicitly, with conflicting IDs and reasons.]

    ### Cannot verify
    [Requirement and what the controller must check, or "None"]

    ### Checks run
    [Focused command and result, or "None"]

    `Approved` means required behavior is verified and no actionable findings,
    material requirement conflicts, or reported concerns remain.
    `Concerns` means required behavior is verified and only reported concerns
    remain. `Needs attention` means
    an actionable finding, unresolved material requirement conflict, or
    unverified required behavior remains.
```

**Placeholders:**

- `[PASS_NUMBER]` — `1` or `2`
- `[TICKET_OR_SPEC]` — path, URL, or fetched issue contents
- `[PLAN_FILE]` — `.tracer/implement/plan.md`
- `[GLOBAL_CONSTRAINTS]` — verbatim from the plan
- `[REPORT_FILES]` — every `.tracer/implement/task-*-report.md` plus `.tracer/implement/repair-report.md` when present; otherwise state repair skipped for pass 2
- `[PRIOR_REVIEW_AND_FINDINGS]` — pass 1: `None`; pass 2: `.tracer/implement/review-1.md` and `.tracer/implement/findings.md`
- `[REVIEW_REPORT_FILE]` — `.tracer/implement/review-1.md` or `.tracer/implement/review-2.md`, matching the pass
- `[BASE_SHA]` / `[HEAD_SHA]` — the fixed base recorded before task execution and current HEAD
- `[DIFF_FILE]` — from `scripts/review-package BASE HEAD`

Pass 1 may feed one targeted fixer. Pass 2 is final and reports anything that remains; this workflow never dispatches a third review.
