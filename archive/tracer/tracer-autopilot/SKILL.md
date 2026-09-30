---
name: tracer-autopilot
description: "Deliver a request with a short plan, focused checks, one review, and an explicit branch-finishing choice."
disable-model-invocation: true
---

# Autopilot

Deliver the agreed scope: **short plan → implement → review → repair if needed → verify → branch decision**. Continue through routine steps without approval checkpoints. Stop for a material scope/architecture decision, a blocker, or the final branch choice. Use `/tracer-implement` when the user wants plan approval and an implementation report without finishing.

## Scope and execution

Acceptance requirements and explicit user decisions are binding; planner-generated mechanisms are proposals. Prefer existing commands and libraries and simplify the approach without changing required behavior. Before adding custom parsing, a generic process runner, a permission evaluator, concurrency guarantees, or persisted recovery machinery not explicitly chosen by the user, explain the need and simpler alternative, then ask. Safe reruns alone do not imply concurrent execution or automatic crash recovery. Preserve agreed data/security safeguards.

Default to one implementation context for cohesive work, normally the controller. A new task, file, or commit is not a reason to spawn a fresh agent. Delegate only a named investigation or separable unit with a clear benefit, reuse its context for follow-ups, and keep dependent changes sequential. Helpers return evidence without spawning agents or extending the workflow.

## 1. Workspace and short plan

1. Inspect branch and working tree. Stay on an existing feature branch; follow `/tracer-worktrees` on `main` or `master`. Ask about detached HEAD or ambiguous ownership. Preserve unrelated work.
2. Ensure `.tracer/` is ignored; commit a needed ignore rule before recording the base. Read `.tracer/implement/progress.md` before starting. For a fresh delivery, record scope and the immutable starting SHA. On resume, verify scope, base, commits, running workers, and reports against Git and recover the unfinished step. Ask about invalid or unexplained state rather than resetting the workflow.
3. Select focused checks for required behavior and material failure paths. Run relevant existing baseline tests when available; a new feature needs a failing acceptance test, not a full-repository baseline. Report unrelated failures without repairing them. Clarify failures that prevent assessing the change.
4. Write `.tracer/implement/plan.md`: goal, source, acceptance and safety limits, existing facilities to reuse, affected paths, and verification commands. Add `### Task N: <behavior>` headings only to organize coherent implementation units. One task is valid. A few bullets per task suffice; code belongs in implementation, not the plan.
5. Show the approach, task order, delegation if any, and checks, then proceed. Explicitly surface new infrastructure or stronger safety guarantees for approval; an innocuous task name is not disclosure of a complex architecture.

Use focused testing by default. Full-suite runs and broad typechecks require repository policy, a user request, or a stated impact-based reason. Otherwise leave broad validation to CI or the user and report that limit.

Keep a short ledger with scope, base, plan, implementation context/commits, review/repair status, checked HEAD/tree, evidence, concerns, and outcome. Mark work running before dispatch and save worker IDs. Resume existing work and budgets; generic “continue” does not authorize more reviews or repairs.

**Complete when:** workspace, scope, minimal approach, verification, and any material decisions are settled.

## 2. Implement in one context

Implement the coherent change using focused red/green tests for new or corrected behavior. Documentation-only changes need relevant validation, not invented runtime tests. Cover observable acceptance and meaningful failures rather than every conceivable configuration.

Simplify planner-generated mechanisms when existing facilities suffice. If substantially more machinery is emerging than disclosed, stop and propose the smaller alternative before building it. Self-check once for correctness, scope, and meaningful tests; record optional hardening as concerns. Commit coherent changes and record evidence.

For justified delegation, use `scripts/task-brief` and [implementer-prompt.md](implementer-prompt.md), passing original requirements and limits. Verify the actual diff, commits, and focused results. Reuse the implementation context for subsequent related work.

**Complete when:** required behavior is implemented and focused checks pass, or a blocker is reported.

## 3. One review and optional repair

Pin `REVIEW_HEAD` and run `scripts/review-package BASE REVIEW_HEAD` for the entire agreed scope. Use [delivery-reviewer-prompt.md](delivery-reviewer-prompt.md) for one review, preferably by one independent read-only reviewer; review inline when delegation is unavailable or disproportionate. Save `.tracer/implement/review-1.md`.

Adjudicate findings against their evidence. Accepted repairs require a reachable trigger, violated requirement, and current consequence: incorrect behavior, security/data loss, silent failure, or a test unable to detect broken required behavior. Retain stable finding IDs and record accepted, contested, and deferred dispositions. Ask about material requirement conflicts; speculative hardening and polish are follow-ups.

- **No accepted repairs:** proceed to final evidence. Skip the closing verifier entirely.
- **Accepted repairs:** use [fixer-prompt.md](fixer-prompt.md) in the existing implementation context where possible. Correct the accepted list in one consolidated pass and save `.tracer/implement/repair-report.md`. If code changed, use [closing-verifier-prompt.md](closing-verifier-prompt.md) to recheck corrections and affected behavior only, saving `.tracer/implement/review-2.md`. If all repairs are blocked and nothing changed, report Blocked without a ceremonial recheck.

The whole delivery has one initial review, at most one repair pass, and one correction-only recheck if repairs were made. This includes inline and delegated work and survives resumes. No nested reviews, new tasks made from findings, second repair pass, or additional audit. After the recheck, report unresolved work; only explicit new user authorization extends the budget.

**Complete when:** findings have dispositions and changes from the repair pass have been rechecked, or blockers are recorded.

## 4. Evidence and outcome

The controller verifies the agreed acceptance and checks against final HEAD and tracked-tree state. Reuse completed evidence for the same unchanged state; rerun affected checks after changes. Record actual commands/results and limits in the ledger. No separate proof agent or mandatory Convince Me protocol is needed. Missing required evidence is unverified, not successful; optional broader checks remain explicit limitations.

Report goal, commits, review and repair/recheck status (including skipped steps), findings and follow-ups, exact checks, branch, and HEAD. Record one outcome:

- **Complete:** required behavior is verified and no actionable findings or concerns remain.
- **Complete with follow-ups:** required behavior is verified; only non-blocking concerns remain.
- **Blocked:** a task, required check, material defect, or scope decision remains unresolved or unverified. Preserve the workspace and stop without push, PR, merge, or cleanup.

For either Complete outcome, follow the shared [branch-finishing procedure](../tracer-finish-branch/branch-finishing.md). Pass the agreed verification scope, evidence, and follow-ups, then wait for the user's explicit merge / PR / keep / discard choice. Finishing adds neither another review nor an automatic expansion of test scope.

**Complete when:** the blocked workspace is preserved or the authorized branch decision is executed and reported.
