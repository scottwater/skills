# Implementer prompt

Dispatch one fresh implementer per task. Fill every `[BRACKET]`.

```text
Subagent (general-purpose; fresh implementer):
  description: "Implement Task N: [TASK_NAME]"
  prompt: |
    Implement Task N in [DIRECTORY].

    Read [BRIEF_FILE] for the exact task requirements, values, interfaces,
    test code, and commands. Context: [SCENE_AND_EARLIER_INTERFACES].
    Global Constraints: [GLOBAL_CONSTRAINTS].

    Implement only this task using TDD at its named seams: demonstrate the
    expected failure, make the minimal correction, and run focused checks.
    Preserve the original acceptance claims and agreed safety limits.
    If the brief conflicts with actual code or requirements, identify the
    conflict and ask for the decision needed to proceed.

    Self-check once against the brief: required behavior, affected callers,
    meaningful assertions, and scope. Correct defects in your task before
    committing. Record optional polish and hardening as concerns.
    Run focused checks, not the full suite; the controller owns final
    delivery-wide verification. Do not dispatch reviewers or other agents.

    Commit coherent task changes using the brief's intended messages and
    the repository's commit conventions. If blocked, preserve the work and
    identify what prevents safe continuation. Use DONE only when required
    behavior is implemented and focused checks pass; use DONE_WITH_CONCERNS
    when only non-blocking concerns remain.

    Write [REPORT_FILE] with:
    - Implemented behavior and files changed.
    - RED/GREEN commands, observed results, and why the failure demonstrated
      the intended requirement (or why TDD was not applicable).
    - Commits, self-check findings, and unresolved concerns.

    Reply in under 15 lines:
    - Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
    - Commits and focused-check results
    - Unresolved concerns or the precise missing context/decision
    - Report path
```

Use `.tracer/implement/task-N-brief.md` and `task-N-report.md`. Copy Global Constraints verbatim from the plan; pass earlier interfaces rather than pasting prior-task history. Await the result before continuing to a dependent task.

Implementation self-checks belong to this task. After delivery review, dispatch corrections through [fixer-prompt.md](fixer-prompt.md) within the single repair pass.
