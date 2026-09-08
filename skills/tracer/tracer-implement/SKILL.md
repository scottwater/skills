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

## Review budget

The entire agreed scope has two review passes and at most one consolidated repair pass, including delegated and inline work. Helpers return results to the controller; they cannot launch nested reviewers or fixers. Review findings stay in the repair pass rather than becoming new implementation tasks.

After pass 2, report unresolved work and stop. A new explicit user authorization may extend the budget; a resume, compaction, renamed task, or generic “continue” does not reset it.

## Phase 0 — Workspace

1. Choose the workspace from the current branch: run `CURRENT_BRANCH=$(git symbolic-ref --quiet --short HEAD || true)`.
   - A named branch other than `main` or `master` is already the feature workspace. Work where you are.
   - On `main` or `master`, run `/tracer-worktrees` before implementing.
   - A detached HEAD or failed branch lookup is ambiguous. Ask where the work should live.
2. Inspect `.tracer/implement/progress.md` before starting work. Ensure `.tracer/` is git-ignored (`git check-ignore -q .tracer`; if not, add it to `.gitignore` and commit before recording a fresh base).
3. On a fresh run, run the test suite once to establish a clean baseline. Stop and report a red baseline. Record `BASE=$(git rev-parse HEAD)` once and create the ledger below. Every task and both reviews use this fixed point.
4. On resume, verify the workflow, scope, base, task commits, reviewed HEADs, and saved reports against Git. Resume the unfinished phase with its existing budget. A missing or invalid base, legacy ledger without review accounting, different workflow, or unexplained HEAD change requires clarification; never silently start over.

Keep these fields in `.tracer/implement/progress.md`:

```text
Workflow: implement-bounded-v1
Scope: <ticket/spec references and agreed boundaries>
Base: <immutable commit SHA>
Plan: pending | approved; path=<path>
Tasks: <implemented commits, focused checks, concerns>
Pass 1: not-started | running | complete; head=<sha>; report=<path>; agent=<id>
Repair: not-started | running | complete | skipped; base=<sha>; head=<sha>; report=<path>; agent=<id>
Pass 2: not-started | running | complete; head=<sha>; report=<path>; agent=<id>
Final evidence: not-started | running | complete; head=<sha>; report=<path>
Outcome: pending | Implemented | Implemented with concerns | Needs attention
```

Mark a phase running **before** dispatch or inline execution; save worker IDs and results as they become available. If interrupted, recover the existing worker/report before continuing that phase. Give a failed worker's replacement the saved findings, decisions, evidence, and unfinished work within the same phase. If recovery is unsafe, stop with Needs attention and ask for clarification.

Keep review reports and findings in the ignored workspace through final reporting and any resume. A completed pass 2 is not rerun: finish only outstanding final evidence/reporting against the same unchanged HEAD and tracked tree, or report the saved outcome. Preserve the approved plan on resume rather than restarting the checkpoint.

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
- that there will be exactly two review passes and at most one targeted fix pass between them;
- that this skill stops before whole-branch review and branch finishing.

Wait for approval or corrections. Batch any contradictions found in the source into this checkpoint. Record approval in the ledger before dispatching tasks.

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

1. Pin `REVIEW_HEAD=$(git rev-parse HEAD)`, record pass 1 running, and run `scripts/review-package "$BASE" "$REVIEW_HEAD"` to capture the cumulative ticket diff.
2. Dispatch one fresh ticket-wide reviewer using [ticket-reviewer-prompt.md](ticket-reviewer-prompt.md). Pass the ticket/spec, plan, all task reports, review package, fixed SHAs, and Global Constraints. Save the full result to `.tracer/implement/review-1.md` with the checked HEAD and mark pass 1 complete.
3. Verify each finding against the code and apply the Attention budget. In `.tracer/implement/findings.md`, retain stable IDs and record: violated requirement, trigger/consequence, evidence, disposition (**accepted / contested / deferred**), invariant to preserve, and correction commit or unresolved reason. Combine overlapping findings while retaining their IDs as aliases; preserve deferred and blocked findings as well as accepted ones. Ask the user about contested requirements that materially affect acceptance rather than silently choosing a new contract.
4. If actionable findings are accepted, record repair running with `FIX_BASE=$REVIEW_HEAD`. Dispatch one fixer using [fixer-prompt.md](fixer-prompt.md) with the findings file, original scope/plan, Global Constraints, task reports, and `.tracer/implement/repair-report.md`. Only accepted findings are work orders. Record correction commits, focused evidence, and unresolved findings; mark repair complete even when some repairs remain blocked.
5. If nothing is accepted, mark repair skipped. Preserve contested and deferred findings for pass 2 and final reporting.

There is one targeted repair pass. The next review verifies the cumulative result; it does not restart an open-ended fix loop.

**Complete when:** pass 1 is recorded and every selected finding is either mapped to a correction commit or explicitly reported as blocked.

## Phase 4 — Review pass 2

Pin `FINAL_HEAD=$(git rev-parse HEAD)`, record pass 2 running, and rebuild the review package from the original `$BASE` through `$FINAL_HEAD`. Dispatch one fresh reviewer with [ticket-reviewer-prompt.md](ticket-reviewer-prompt.md), current task reports, `.tracer/implement/review-1.md`, `.tracer/implement/findings.md`, and the repair report or skipped status.

Pass 2 reconciles every earlier finding, verifies corrections and affected behavior, and checks the original ticket requirements. The cumulative package supplies context; this is not a fresh search for unrelated improvements. Require evidence for any proposed reversal of an earlier decision, including the earlier finding ID and conflicting requirement. Earlier reviews are claims to evaluate, not authority to obey blindly.

This is the final review pass:

- Verify its findings against the code and apply the Attention budget.
- Do not dispatch another fixer from this skill.
- Any remaining P0/Critical or High finding makes the result **Needs attention**.
- Any selected P1/Medium finding makes the result **Needs attention**.
- Deferred P1/Medium and Low/Minor findings become reported concerns.
- Record newly demonstrated defects, including correction-induced regressions; identify uncertain provenance rather than guessing.
- An unresolved material requirement conflict or required behavior that cannot be verified makes the result **Needs attention**.

Save the full result to `.tracer/implement/review-2.md` with the checked HEAD. Update findings with resolved / unresolved / unverified status, evidence, and any explicit supersession; preserve the original decisions and reasons. Mark pass 2 complete even when the verdict is Needs attention.

**Complete when:** every prior finding has a disposition, and the second verdict and unresolved concern list are saved. There is no third review.

## Phase 5 — Final evidence and report

Record final evidence running. Run the complete test suite and typecheck once against final `HEAD` and read the output. Save commands, results, checked HEAD, and tracked-tree state to `.tracer/implement/final-evidence.md`; mark evidence complete. On resume, reuse this phase's completed evidence only for the same unchanged HEAD and tracked tree. Failed checks are reported, not another repair pass.

Report:

- task commits and implementation status;
- both review verdicts;
- fixes made after pass 1, mapped to finding IDs;
- accepted/contested/deferred findings, their final status, and any explicit reversals;
- unresolved actionable findings and unverified requirements;
- deferred concerns, including implementer concerns;
- exact full-suite and typecheck commands with results;
- the current branch and that it was left in place.

Use one outcome:

- **Implemented** — final checks pass, required behavior is verified, and pass 2 has no actionable findings, material requirement conflicts, or reported concerns.
- **Implemented with concerns** — final checks pass, required behavior is verified, and only deferred concerns remain.
- **Needs attention** — tests are red, an actionable finding remains, a task is blocked, or a material requirement conflict or unverified required behavior remains.

Save `.tracer/implement/final-report.md` and record the outcome in the ledger. End after the report. Do not invoke another review or branch workflow.

## Red flags — never

- Implement on `main` or `master` without explicit consent
- Begin either review before all subtasks are implemented
- Run more than two ticket-wide review passes
- Spend the repair pass on Low/Minor polish or speculative hardening
- Hide deferred findings to claim a clean result
- Run `/tracer-code-review` or `/tracer-finish-branch` from this skill
- Claim completion without fresh full-suite evidence
