---
name: tracer-implement
description: "Implement a ticket or request with a short approved plan, focused tests, and one review; recheck corrections only when needed."
disable-model-invocation: true
---

# Implement

Deliver the agreed behavior with the smallest repository-specific change: **short plan and approval → implement → review → repair if needed → verify and report**. Stop on the feature branch without merging, opening a PR, or invoking another review workflow. Use `/tracer-autopilot` for delivery through a branch-finishing choice.

## Scope and simplicity

Acceptance requirements and explicit user decisions are binding. Planner-generated code, class boundaries, and mechanisms are proposals: simplify them when existing commands or libraries satisfy the same requirements. Record the changed approach; ask only when it changes acceptance, an explicit decision, or a material safety limit.

Before introducing custom parsing, a generic process runner, a permission evaluator, concurrency guarantees, or persisted recovery machinery that the user has not explicitly chosen, explain the concrete need and the simpler alternative, then ask. Safe reruns do not by themselves imply concurrent execution or automatic crash recovery. Preserve required data/security safeguards; expose a trade-off rather than quietly weakening them.

Default to one implementation context for a cohesive change, normally the controller itself. Multiple files or commits do not require multiple agents. Delegate only a named investigation or separable implementation unit whose benefit exceeds the handoff cost. Reuse its context for follow-up work. Helpers return results without spawning more agents.

## Decision questions

Whenever this workflow needs a user decision, make the choice answerable from the message itself:

1. **Issue and impact:** explain what happened, which required behavior is affected, and what remains blocked or unverified. Use plain language; distinguish observed evidence from uncertainty. Include only the technical detail needed to judge the choice.
2. **Recommendation:** say “I recommend [specific next action] because [reason].” State its scope and material trade-off, including any change to acceptance, safety limits, or the review/repair budget. Recommend investigating a named unknown when evidence is insufficient to choose a fix.
3. **Question:** end with one direct question naming the proposed action: “Should I [specific action]?” For a real trade-off, offer concise, mutually exclusive choices with the recommendation first and each choice's consequence. Ask for the smallest decision that unblocks work; avoid “How should I proceed?” or an unexplained list of options.

Explain why input is needed: a missing requirement, a conflict with an explicit decision, or the specific authorization boundary. Honor existing answers and authorization; resolve ordinary reversible implementation details yourself. Complete useful independent work while waiting, and resume dependent work only after the answer. A question left unanswered is still pending.

Example at the repair limit: “The repair is complete, but the duplicate-submit check still fails: a retry can create two orders. I recommend one additional repair pass limited to preventing duplicate orders, followed by the focused retry check. This exceeds the agreed one-pass repair budget. Should I make that additional repair and run the retry check?”

Non-blocking concerns need a clear impact and disposition; ask only if a user choice is actually needed. A successful completion with no pending decision needs no follow-up question.

## 1. Workspace and evidence plan

1. Inspect the branch and working tree. Stay on an existing feature branch. On `main` or `master`, follow `/tracer-worktrees`; ask about detached HEAD or ambiguous ownership. Preserve unrelated changes.
2. Ensure `.tracer/` is ignored before writing workflow artifacts; commit a needed ignore rule before recording the base.
3. On a fresh run, record the starting SHA in `.tracer/implement/progress.md`. On resume, read that ledger and verify its scope, base, commits, running workers, and saved reports against Git before continuing the unfinished step. Recover existing work rather than restarting it. Ask about an invalid base or unexplained changes.
4. Select the smallest checks that establish the changed behavior and material failure paths. Run relevant existing tests as a baseline when available. An unrelated failing suite is not a work order; report it. A baseline failure that prevents assessing this change needs clarification.

Use focused tests by default. Run the full suite or broad typecheck only when repository policy requires it, the user requests it, or the impact justifies it; explain that choice. Otherwise report that broad validation is left to CI or the user. A new feature with no existing tests needs a failing acceptance test, not a whole-repository baseline.

Keep the ledger brief: scope, immutable base, approved plan, implementation commits/context, review and repair status, checked HEAD/tree, evidence, concerns, and outcome. Mark work running before delegation and save worker IDs. Completed review/repair budgets survive resumes and generic “continue” messages.

**Complete when:** workspace, resume point, base, and proportionate verification are known.

## 2. Short plan and approval

Write `.tracer/implement/plan.md`, normally a few bullets per coherent behavior:

```markdown
# <Feature> Task Plan

**Goal:** observable outcome.
**Source:** request, ticket, or spec.
**Acceptance and limits:** required behavior and material safety boundaries.
**Approach:** existing commands/modules to reuse; proposed new mechanisms.
**Verification:** focused commands and the behavior they establish.

### Task 1: <coherent behavior>
- Files: exact affected paths.
- Change: smallest approach; only interfaces needed to coordinate work.
- Check: observable success and material failure behavior.
```

One task is valid. Group tasks by coherent behavior, not framework layers. Write code during implementation rather than prewriting tests and implementation in the plan. Resolve acceptance-changing ambiguities; ordinary reversible details remain implementation choices.

Show the goal, approach, task order, delegation if any, and checks. Call out custom infrastructure and safety/recovery guarantees explicitly: task names alone are not architectural approval. Explain that there is one review, at most one consolidated repair, and a correction-only recheck if repairs occur. Use the Decision questions format to recommend the approach and explicitly ask to implement it with the stated checks. Wait for approval and record it.

**Complete when:** the user has approved the actual approach and verification scope, not merely a task count.

## 3. Implement

Work through the plan in the same context. Use focused red/green tests for new or corrected behavior and existing checks where appropriate; documentation-only changes need relevant validation, not invented runtime tests. Test observable requirements and material failure paths, not every speculative variant. Add parameterized cases when they cheaply cover genuinely distinct behavior.

Prefer existing facilities over new abstractions. If the approach starts requiring substantially more machinery than approved, stop and propose the smaller alternative before building it. Do not finish an oversized design merely to report concerns afterward.

Commit coherent changes using repository conventions. Self-check changed behavior and scope once; fix material defects and record optional hardening as concerns. Save commits and focused results in the ledger.

If delegation is justified, extract the relevant task with `scripts/task-brief` and use [implementer-prompt.md](implementer-prompt.md). Pass the original acceptance requirements and limits alongside the brief. Verify the returned diff, commits, and evidence; a report alone is not proof. A task boundary is not a fresh-agent requirement.

**Complete when:** agreed behavior is implemented, focused checks pass, and implementation evidence is recorded.

## 4. Review and optional repair

Pin the current HEAD and run `scripts/review-package BASE HEAD` once for the complete agreed scope. Use [ticket-reviewer-prompt.md](ticket-reviewer-prompt.md) for one review, preferably by one independent read-only reviewer; review inline if delegation is unavailable or disproportionate.

Accept findings only with a reachable trigger, violated requirement, and current consequence: incorrect behavior, security/data loss, silent failure, or tests unable to detect broken required behavior. Record polish and speculative hardening as concerns, not work orders. Ask about material conflicts with the agreed requirements. Save the review and dispositions in `.tracer/implement/review-1.md`.

- **No accepted repairs:** finish verification and report. No second review or closing-verifier agent is needed.
- **Accepted repairs:** correct the complete accepted list in one repair pass, preferably in the existing implementation context, using [fixer-prompt.md](fixer-prompt.md). Save finding IDs, changes, and focused results to `.tracer/implement/repair-report.md`. If code changed, recheck corrections and affected behavior only, preferably in the original reviewer context, and save `.tracer/implement/review-2.md`. If all repairs are blocked and nothing changed, report Needs attention without a ceremonial recheck.

The budget covers the whole agreed scope, including delegated and inline work: one initial review, at most one repair pass, and one correction-only recheck if repairs were made. Helpers cannot launch reviews or fixers. After the recheck, report unresolved work and stop; only explicit new user authorization extends the budget. A concern does not become a new implementation task.

**Complete when:** review findings have dispositions and any repairs have a correction-only recheck, or unresolved work is recorded.

## 5. Final evidence and report

Verify the agreed checks against final HEAD and tracked-tree state. Reuse already completed evidence for that same unchanged state; rerun affected checks after changes. Record commands, actual results, and unavailable checks. Focused passing tests are not a claim that the full suite ran.

Report goal, commits, review result (and recheck or skipped status), corrections, deferred concerns, verification limits, and the preserved branch. Use:

- **Implemented:** required behavior is verified and no actionable findings or concerns remain.
- **Implemented with concerns:** required behavior is verified; only non-blocking concerns remain.
- **Needs attention:** a task, required check, actionable finding, or material scope decision remains blocked or unverified.

For **Needs attention**, lead with the unresolved issue and its practical impact, distinguish completed work from missing evidence, and close with the recommendation and explicit question from Decision questions. Summarize the decision in the reply itself; a status label or report path is insufficient. If work depends on user-provided access or information, request the exact missing input and explain what it enables. Reaching the review/repair limit is a reason to ask for a bounded next step, not permission to start it.

Save the outcome and any pending decision in the ledger and end. No additional audit, proof workflow, or branch finishing is implied.
