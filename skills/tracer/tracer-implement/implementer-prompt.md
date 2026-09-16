# Implementation prompt

Use inline by default. For justified delegation, give one implementer the cohesive change and reuse its context for related work. Fill every `[BRACKET]`.

```text
Implement [BEHAVIOR] in [DIRECTORY].
Original requirements and explicit decisions: [SOURCE_AND_LIMITS].
Short plan or task brief: [BRIEF_FILE].
Relevant existing facilities/interfaces: [CONTEXT].
Verification scope: [CHECKS].

Deliver the required behavior with the smallest repository-specific change.
Acceptance and explicit user decisions are binding. The plan's mechanisms,
code sketches, and class boundaries are proposals, not transcription orders.
Simplify them when existing commands or libraries suffice; record the change.
Ask if acceptance, an explicit decision, or a material safety limit must change.

Before introducing custom parsing, a generic runner, permission evaluation,
concurrency guarantees, or persisted recovery machinery not explicitly chosen
by the user, report the need and simpler alternative to the controller. If
implementation is growing substantially beyond the approved approach, pause
before building the extra machinery rather than finishing it with concerns.

Use focused red/green tests for new or corrected behavior. Test observable
requirements and material failures, not every speculative variant. Use relevant
validation for documentation-only changes. Honor the supplied verification
scope; identify a concrete reason before proposing broader checks.

Self-check changed behavior, meaningful assertions, and scope once. Correct
material defects; report optional polish/hardening without implementing it.
Commit coherent changes using repository conventions. Do not spawn agents or
start a review workflow. Escalate a blocker with what you tried and the smallest
missing decision instead of repeatedly searching or retrying.

Write [REPORT_FILE]: behavior and files changed, any approach simplification,
checks and observed results (including red/green evidence where applicable),
commits, and remaining concerns. Reply briefly with:
- DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
- Commits and focused-check results
- Concern or precise decision needed, and report path

Stop after reporting. Further related work can resume this same context.
```

For a delegated task, `scripts/task-brief` can produce `.tracer/implement/task-N-brief.md`; use `.tracer/implement/task-N-report.md` for its report. Pass original requirements and safety limits separately because the extracted task may not contain them. Inline work can record results directly in the progress ledger.
