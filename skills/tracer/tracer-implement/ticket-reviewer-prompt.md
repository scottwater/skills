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

    Reports, commit messages, comments, and rationales are unverified claims.
    Judge the cumulative diff.

    ## Diff under review

    Base: [BASE_SHA]  Head: [HEAD_SHA]
    Read the review package once: [DIFF_FILE]

    It contains the commit list, stat summary, and cumulative diff. Inspect
    unchanged code only to test a concrete risk at a named call site or
    contract. Read-only: never mutate the worktree, index, or HEAD.

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
    [P0/Critical and High findings; P1/Medium findings selected for current
    repair. For each: ID, severity, file:line, trigger, consequence, and fix.]

    ### Reported concerns
    [Deferred P1/Medium and Low/Minor findings. For each: ID, file:line,
    evidence, and why it does not cross the current repair threshold.]

    ### Cannot verify
    [Requirement and what the controller must check, or "None"]

    ### Checks run
    [Focused command and result, or "None"]

    `Approved` means no actionable findings and no reported concerns.
    `Concerns` means only reported concerns remain. `Needs attention` means at
    least one actionable finding exists.
```

**Placeholders:**

- `[PASS_NUMBER]` — `1` or `2`
- `[TICKET_OR_SPEC]` — path, URL, or fetched issue contents
- `[PLAN_FILE]` — `.tracer/implement/plan.md`
- `[GLOBAL_CONSTRAINTS]` — verbatim from the plan
- `[REPORT_FILES]` — every `.tracer/implement/task-*-report.md` plus the fixer report when present
- `[BASE_SHA]` / `[HEAD_SHA]` — the fixed base recorded before task execution and current HEAD
- `[DIFF_FILE]` — from `scripts/review-package BASE HEAD`

Pass 1 may feed one targeted fixer. Pass 2 is final and reports anything that remains; this workflow never dispatches a third review.
