---
name: tracer-implement
description: "Implement a ticket or spec with a visible task plan, sequential task commits, two bounded ticket-wide review passes, and a final test run."
disable-model-invocation: true
---

# Implement

Implement a ticket, spec, or user description and stop with reviewed code on the current feature branch. The flow is: **plan checkpoint → implement every task → review → targeted fix → verification review → test → report**.

This skill does not run `/tracer-code-review`, `/tracer-finish-branch`, merge, open a PR, or clean up the workspace. Use `/tracer-autopilot` when the user asks for that end-to-end flow.

## Attention budget

Spend review and repair effort on defects that matter now:

- **Always address:** P0/Critical and High findings.
- **Address selectively:** P1/Medium findings only when evidence shows a current spec violation, incorrect user-visible behavior, security or data-integrity risk, silent failure, or a test that cannot detect broken behavior.
- **Report without fixing:** Low/Minor findings, polish, speculative hardening, hypothetical future consumers, and stylistic preferences not required by the repository.

Severity labels are not sufficient by themselves. Require a concrete trigger and consequence before selecting a finding for repair. Preserve deferred findings in the final report as concerns; do not silently discard them.

## Phase 0 — Workspace

1. Choose the workspace from the current branch: run `CURRENT_BRANCH=$(git symbolic-ref --quiet --short HEAD || true)`.
   - A named branch other than `main` or `master` is already the feature workspace. Work where you are.
   - On `main` or `master`, run `/tracer-worktrees` before implementing.
   - A detached HEAD or failed branch lookup is ambiguous. Ask where the work should live.
2. If `.tracer/implement/progress.md` exists, read its `Base: <sha>` entry, verify completed tasks against `git log`, and resume at the first incomplete task with that recorded base.
3. Ensure `.tracer/` is git-ignored (`git check-ignore -q .tracer`; if not, add it to `.gitignore` and commit).
4. Run the test suite once to establish a clean baseline. Stop and report a red baseline.
5. On a fresh run, record `BASE=$(git rev-parse HEAD)` once and create `.tracer/implement/progress.md` with `Base: $BASE`. Every task and both reviews use this fixed point. If a resumed ledger has no base or the base no longer resolves, stop and ask rather than reviewing a partial range.

**Complete when:** the feature workspace, green baseline, resume point, and fixed review base are known.

## Phase 1 — Task plan and checkpoint

Write `.tracer/implement/plan.md`. Tickets and specs deliberately omit paths and code that go stale; this ephemeral plan supplies exact paths, interfaces, commands, and test code.

Use this header:

```markdown
# <Feature> — Task Plan

**Goal:** one sentence.
**Ticket/Spec:** reference or path.
**Architecture:** 2–3 sentences.
**Seams under test:** the pre-agreed seams from the spec.

## Global Constraints

Project-wide requirements copied verbatim from the spec or ticket.
```

Write each task as the smallest sequential implementation unit worth its own commit:

````markdown
### Task N: <name>

**Files:**
- Create: `exact/path`
- Modify: `exact/path`
- Test: `exact/path`

**Interfaces:**
- Consumes: exact names and signatures from earlier tasks
- Produces: exact names and signatures later tasks need

Steps: write the failing test with actual code, run it with the exact command
and expected failure, write the minimal implementation with actual code, run
the focused test, and commit with the exact message.
````

Reject placeholders such as “TBD,” “handle edge cases,” “write tests,” or “similar to Task N.” Self-review the plan for requirement coverage, placeholders, and interface consistency.

Before dispatching work, show the user:

- the task count and ordered task names;
- the purpose of each task in one line;
- that all tasks run before either ticket-wide review;
- that there will be exactly two review passes and one targeted fix pass between them;
- that this skill stops before whole-branch review and branch finishing.

Wait for approval or corrections. Batch any contradictions found in the source into this checkpoint.

**Complete when:** the user has seen and approved the execution shape.

## Phase 2 — Implement every task

For each incomplete task, in order:

1. Run `scripts/task-brief .tracer/implement/plan.md N`; it writes `.tracer/implement/task-N-brief.md`.
2. Dispatch a fresh implementer using [implementer-prompt.md](implementer-prompt.md). Pass the brief path, one or two lines of feature context, earlier-task interfaces the brief cannot know, the Global Constraints verbatim, and `.tracer/implement/task-N-report.md`.
3. Handle its status:
   - **DONE** — verify the named commit exists, then continue.
   - **DONE_WITH_CONCERNS** — record the concerns and continue unless they question correctness or scope.
   - **NEEDS_CONTEXT** — supply the missing context and re-dispatch.
   - **BLOCKED** — change the context, model, or task shape before retrying; ask the user when the plan is wrong.
4. Append `Task N: implemented (commit <sha>, focused tests green)` to `.tracer/implement/progress.md`.
5. Report one progress line to the user and continue without a review gate.

Implementers run focused tests and commit their task. They do not run the full suite; the controller runs it once after both ticket-wide reviews.

**Complete when:** every planned task is committed and every report exists. Do not begin review while a task remains incomplete.

## Phase 3 — Review pass 1 and targeted repair

1. Run `scripts/review-package $BASE HEAD` to capture the cumulative ticket diff.
2. Dispatch one fresh ticket-wide reviewer using [ticket-reviewer-prompt.md](ticket-reviewer-prompt.md). Pass the ticket/spec, plan, all task reports, review package, BASE/HEAD, and Global Constraints.
3. Verify each finding against the code. Classify it using the Attention budget as **actionable now** or **reported concern**.
4. If there are actionable findings, dispatch one fixer with the complete actionable list and the review-fix instructions from [implementer-prompt.md](implementer-prompt.md). The fixer runs focused tests, commits coherent corrections, and maps every finding ID to a commit in its report.
5. Do not send reported concerns to the fixer.

There is one targeted repair pass. The next review verifies the cumulative result; it does not restart an open-ended fix loop.

**Complete when:** pass 1 is recorded and every selected finding is either mapped to a correction commit or explicitly reported as blocked.

## Phase 4 — Review pass 2

Rebuild the review package from the original `$BASE` through current `HEAD`. Dispatch one fresh reviewer with the same ticket-wide prompt and current reports.

This is the final review pass:

- Verify its findings against the code and apply the Attention budget.
- Do not dispatch another fixer from this skill.
- Any remaining P0/Critical or High finding makes the result **Needs attention**.
- Any selected P1/Medium finding makes the result **Needs attention**.
- Deferred P1/Medium and Low/Minor findings become reported concerns.

**Complete when:** the second verdict and unresolved concern list are captured. There is no third review.

## Phase 5 — Final evidence and report

Run the complete test suite and typecheck once against final `HEAD` and read the output.

Report:

- task commits and implementation status;
- both review verdicts;
- fixes made after pass 1, mapped to finding IDs;
- unresolved actionable findings;
- deferred concerns, including implementer concerns;
- exact full-suite and typecheck commands with results;
- the current branch and that it was left in place.

Use one outcome:

- **Implemented** — tests are green and pass 2 has no actionable findings or reported concerns.
- **Implemented with concerns** — tests are green and only deferred concerns remain.
- **Needs attention** — tests are red, an actionable finding remains, or a task is blocked.

End after the report. Do not invoke another review or branch workflow.

## Red flags — never

- Implement on `main` or `master` without explicit consent
- Begin either review before all subtasks are implemented
- Run more than two ticket-wide review passes
- Spend the repair pass on Low/Minor polish or speculative hardening
- Hide deferred findings to claim a clean result
- Run `/tracer-code-review` or `/tracer-finish-branch` from this skill
- Claim completion without fresh full-suite evidence
