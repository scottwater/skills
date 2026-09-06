---
name: tracer-autopilot
description: "Deliver a ticket or spec through bounded review, fresh proof, and a branch-finishing choice."
disable-model-invocation: true
---

# Autopilot

Deliver the user's agreed scope: **plan → implement and test every task → broad review → one repair pass → focused review with completion evidence → report and finish**. Continue between tasks without approval checkpoints; stop for a material ambiguity, a blocker, or the final branch decision.

Use `/tracer-implement` when the user wants to approve the task order and stop with the implementation report rather than proceed to branch finishing.

## Delivery budget

A **delivery** is the entire scope accepted for this invocation, including every ticket and task it contains. It has **two review rounds and at most one consolidated repair pass**, not that allowance per task, reviewer, or axis.

- Round 1 discovers material defects against the agreed requirements.
- Round 2 verifies corrections, affected behavior, and the original goal with fresh evidence.
- Tasks use TDD and implementer self-checks; they have no independent review gates.
- All delegated and inline reviews count toward the same budget. Helpers return evidence to the controller; they cannot launch nested reviews, fixers, or approval gates.
- After round 2, report unresolved work. No third review, second repair pass, or extra whole-branch audit. A new user authorization may extend the budget; a resume, compaction, renamed task, or generic “continue” does not reset it.

**Material findings** identify a reachable trigger, a violated requirement or invariant, and a current consequence: incorrect user-visible behavior, data loss, security exposure, silent failure, or tests that cannot detect broken required behavior. A severity label alone does not qualify. Record polish, speculative hardening, hypothetical consumers, and structural preferences as follow-ups. Treat stronger safety guarantees as scope proposals.

## Phase 0 — Workspace and resume

1. Run `CURRENT_BRANCH=$(git symbolic-ref --quiet --short HEAD || true)`.
   - A named branch other than `main` or `master` identifies the feature workspace; stay there.
   - On `main` or `master`, follow the `/tracer-worktrees` workspace instructions before implementation unless the user explicitly chose this checkout.
   - For detached HEAD or a failed lookup, ask where the work should live.
2. Ensure `.tracer/` is git-ignored; commit a needed ignore rule before recording the delivery base. Inspect `.tracer/implement/progress.md` before starting work.
   - **Fresh delivery:** establish a clean baseline with the project's tests, record `BASE=$(git rev-parse HEAD)`, and create the ledger below. A failing baseline is Blocked, not permission to fix unrelated defects. If no suite exists yet, record that limitation rather than inventing a green baseline.
   - **Resume:** verify the scope, base, task commits, reviewed HEADs, and saved reports against Git. Resume the unfinished phase with its existing budget. A missing base, legacy ledger without review accounting, or unexplained HEAD change requires clarification; never silently start over.
3. Keep these fields in the ledger:

```text
Workflow: autopilot-bounded-v1
Scope: <ticket/spec references and agreed boundaries>
Base: <immutable commit SHA>
Tasks: <implemented commits, focused checks, concerns>
Round 1: not-started | running | complete; head=<sha>; report=<path>; agent=<id>
Repair: not-started | running | complete | skipped; base=<sha>; head=<sha>; report=<path>
Round 2: not-started | running | complete; head=<sha>; report=<path>; agent=<id>
Outcome: pending | Complete | Complete with follow-ups | Blocked
```

Mark a phase running **before** dispatch; save its ID and result as they become available. If interrupted, recover the existing worker/report before continuing the same phase. Give a failed worker's replacement the saved findings, evidence, scope, and unfinished work within the same phase. If that cannot be recovered safely, report Blocked. When round 2 is already complete, report its saved outcome rather than rerunning verification; only an outstanding branch decision may continue within this budget.

**Complete when:** the workspace, baseline state, fixed delivery base, and remaining budget are known.

## Phase 1 — Task plan

Write `.tracer/implement/plan.md`. This ephemeral plan supplies the paths and test precision omitted from durable specs.

```markdown
# <Feature> — Task Plan

**Goal:** one sentence.
**Ticket/Spec:** references or paths covering the entire delivery.
**Architecture:** 2–3 sentences.
**Seams under test:** the pre-agreed test seams.
**Acceptance claims:** observable required behavior, including material failure paths.
**Limits:** agreed environment, concurrency, durability, and recovery guarantees;
identify unresolved assumptions instead of silently strengthening the contract.

## Global Constraints

Project-wide requirements copied verbatim from the spec/ticket.

### Task N: <name>

**Files:** exact create/modify/test paths.
**Interfaces:** exact names/signatures consumed from and produced for other tasks.

Steps: write the failing test with actual code, run the exact command and
confirm the expected failure, implement the minimal change, run focused
checks, self-check against the brief, and commit with the intended message.
```

Group tasks by coherent behavior and commits. Check requirement coverage, executable test steps, and cross-task interfaces; replace every placeholder with the code, command, or decision needed to execute it.

Show a short task-order summary and the delivery budget, then proceed. Batch material contradictions into one question; routine task boundaries need no user approval.

**Complete when:** every acceptance claim maps to a task and verification step, cross-task interfaces agree, and material scope decisions are settled.

## Phase 2 — Implement every task

For each incomplete task, in order:

1. Record the task's starting SHA. Run this skill's `scripts/task-brief .tracer/implement/plan.md N` to write its brief.
2. Dispatch a fresh implementer using [implementer-prompt.md](implementer-prompt.md): brief path, concise scene-setting, earlier-task interfaces, Global Constraints, checkout, and `.tracer/implement/task-N-report.md`. Await its result. Choose an available model suited to the task.
3. Verify its commits and focused-check evidence. Record DONE_WITH_CONCERNS observations for round 1. Supply missing context for NEEDS_CONTEXT; if a task cannot safely support its dependents, resolve the implementation context or report Blocked rather than continue on a broken prerequisite.
4. Append `Task N: implemented (commits <base>..<head>, focused checks <result>)` and continue. Implemented does not mean independently reviewed.

Implementers run focused TDD checks and one self-check, not full-suite runs or review subagents per task. Keep tasks sequential within a checkout. Review findings belong to the delivery's repair pass, not newly invented implementation tasks.

**Complete when:** every task has verified commits and a report with focused-check results; unresolved concerns are recorded for round 1.

## Phase 3 — Round 1: discover and repair

1. Pin `REVIEW_HEAD=$(git rev-parse HEAD)`, record round 1 running, and run `scripts/review-package "$BASE" "$REVIEW_HEAD"` once for the cumulative delivery diff.
2. Dispatch one fresh reviewer using [delivery-reviewer-prompt.md](delivery-reviewer-prompt.md). Pass the original scope, plan, task reports, package, and fixed SHAs. Save its result to `.tracer/implement/review-1.md` and mark round 1 complete.
3. Adjudicate the findings yourself against their cited evidence. In `.tracer/implement/findings.md`, give each a stable ID and record: violated claim, trigger/consequence, evidence, disposition (**accepted / contested / deferred**), and any correction commit. Combine overlapping findings. Distinguish existing defects from correction-induced ones where evidence allows; mark uncertain provenance rather than guessing.
4. If material findings are accepted, record `FIX_BASE=$REVIEW_HEAD` and dispatch **one** fixer using [fixer-prompt.md](fixer-prompt.md) with the complete accepted list. Record its correction commits, check results, and unresolved findings in the ledger. If nothing is accepted, mark repair skipped and set `FIX_BASE=$REVIEW_HEAD`.

Ask the user to resolve contested requirements that materially change acceptance. Keep repairs within the agreed scope and invariants. After the repair pass, proceed to closing verification with any unresolved findings.

**Complete when:** round 1 and the repair disposition are recorded, with each accepted finding linked to evidence and a correction or an explicit unresolved reason.

## Phase 4 — Round 2: focused review and completion evidence

Pin `FINAL_HEAD=$(git rev-parse HEAD)` and record round 2 running. Generate the correction package with `scripts/review-package "$FIX_BASE" "$FINAL_HEAD"`. An empty correction diff is valid when repair was skipped.

Dispatch one fresh closing verifier using [closing-verifier-prompt.md](closing-verifier-prompt.md). Give it the original acceptance claims and limits, round-1 findings/dispositions, repair report (or skipped status), correction package, and the prior delivery package for reference. Pass the shared [proof protocol](../tracer-convince-me/proof-protocol.md) for fresh claim-by-claim evidence within this round.

The verifier checks corrections and affected callers, proves the original acceptance claims, and runs the full suite and typecheck once where available. Inspect its commands and results; save `.tracer/implement/review-2.md` with claim/evidence/verdict rows and the checked HEAD.

Newly demonstrated defects remain visible, including regressions caused by the repair. Record them and their consequences; **no implementation repair follows round 2**. Mark failed proof as disproven and inconclusive proof as unverified. An unresolved serious finding may justify stopping proof work early; list the remaining claims as unverified.

**Complete when:** every acceptance claim and accepted finding is proven, disproven, or explicitly unverified; the final report names all remaining concerns. Record round 2 complete even when the outcome is Blocked.

## Phase 5 — Outcome and branch decision

Record and report one outcome:

- **Complete:** required acceptance claims have fresh evidence, applicable checks pass, and no material blockers or follow-ups remain.
- **Complete with follow-ups:** required behavior is proven and checks pass; only non-blocking concerns or limitations within the agreed scope remain. For each follow-up, state the affected area, evidence or uncertainty, consequence, and suggested next action. Do not automatically schedule or implement it.
- **Blocked:** a task is incomplete, a material defect or required claim remains disproven/unverified, an applicable check fails, or a scope decision prevents acceptance. Preserve the branch and reports; explain the smallest decision or repair needed. Stop without merge, push, PR, discard, or cleanup.

Include the goal, task/fix commits, each round's status (including not run if blocked earlier), accepted/contested/deferred findings, exact verification commands/results and limits, and the branch/HEAD. A clean reviewer verdict alone is not completion evidence.

For either Complete outcome, follow the shared [branch-finishing procedure](../tracer-finish-branch/branch-finishing.md). Carry the outcome and follow-ups into the merge / PR / keep / discard choice; wait for the user's explicit choice. Use that procedure's evidence-reuse and merged-result checks. A finishing failure stops the attempt for the user's decision.

**Complete when:** the outcome is reported and either the blocked workspace is preserved or the authorized branch decision is executed.

## Inline mode

When subagents are unavailable or the delivery is one small task, perform the same phases inline. Use the same ledger, two-round budget, one repair pass, evidence protocol, and outcomes. The absence of delegation changes execution, not the stopping rule.
