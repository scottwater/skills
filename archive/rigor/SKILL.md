---
name: rigor
description: Fix a bug, build a feature, refactor, or improve performance with a focused, evidence-driven workflow.
disable-model-invocation: true
---

# Rigor

Take one concrete code change from request to evidence.

**Boundary.** Rigor changes code, or diagnoses a defect or slowdown on the way to changing it. Open product questions belong to `/interview-me`; recommend it and stop when the decisions that define the task are still unknown.

## 1. Frame and route

Resolve from the request and repository:

- **Finish line:** the observable condition that ends the task. "Figure out what is wrong" stops at diagnosis; "fix it" continues through implementation and proof. The same split applies to performance diagnosis versus optimization.
- **Scope:** the affected system and the smallest plausible problem boundary.
- **Risk:** security, permissions, money, data loss, migrations, concurrency, external compatibility, production access, or a one-way architectural choice.

Then load exactly one playbook:

| Request shape | Playbook |
| --- | --- |
| Diagnose or fix incorrect behavior, a failing test, crash, or regression | [Bug fix](playbooks/bug-fix.md) |
| Add or change product or system behavior | [Feature](playbooks/feature.md) |
| Change structure while preserving behavior | [Refactoring](playbooks/refactoring.md) |
| Diagnose or improve measured speed, memory, throughput, or resource use | [Performance](playbooks/performance.md) |

**Complete when:** the finish line is stated and one playbook matches both the work type and the authorized stopping point. When none fits, name the gap and stop.

## 2. Execute

Follow the playbook's steps under the principles below. Scale ceremony to risk: local, reversible work goes straight to the focused proof; every added plan, delegate, or check answers a named uncertainty.

**Complete when:** the playbook's Done criterion is met and the worktree holds only intended changes.

## 3. Hand off

Report the outcome, the evidence gathered now, and every gap or unverified claim. Then recommend `/convince-me` to build the full end-to-end case, and `/code-quorum` for an independent review when the task touched a named risk.

## Principles

### Evidence

- Keep observations, hypotheses, and unknowns distinct.
- Fix root causes. Establish the symptom, form competing hypotheses, instrument uncertain state, and change the mechanism that produces the failure. A defensive guard is not a root-cause explanation.
- Prove the real outcome at the strongest practical boundary. Compilation, summaries, and self-report are supporting evidence; inspect delegated artifacts directly.
- Work in units small enough that a failed check identifies the responsible change.
- Build a script, codemod, or reproducible command when scale or repetition justifies it; otherwise change directly.

### Shape

For Feature and Refactoring work that changes state, interfaces, or boundaries:

- Name the data shape and its invariants before writing branching logic. Reach for a state machine, discriminated model, table, or registry when it removes scattered rules or invalid states; keep local code local.
- Convert external input into trusted values where it enters.
- Make illegal states hard to represent, exhaust known variants, and narrow or validate instead of casting.
- When a requirement invalidates an existing assumption, design as though it had existed from the start. When an established extension point fits, use it.
- For a consequential open design choice, compare two or three materially different designs against the same criteria.

### Burden

- Subtract first: within the problem boundary, remove dead paths, obsolete adapters, and redundant validation the change replaces.
- Change only what the mechanism and finish line require. Leave adjacent cleanup outside the task.
- A wrapper or abstraction earns its place by owning a real invariant, hiding meaningful complexity, or serving genuine callers.

### Safety

- Give state-mutating operations an explicit retry and partial-run contract.
- Give parallel writers separate files, branches, or worktrees; serialize only around a real shared invariant.
- For internal API changes, migrate every caller and remove the old path in the same effort unless a real external contract requires staging.
- When a failure recurs, prefer a test, type, or lint that makes the fix structural.

### Authority

- Facts are your work: search, run safe commands, or build a cheap probe before asking. Test a technical fork instead of asking which behavior occurs.
- Decisions on product direction, acceptable risk, spend, sensitive data, or external communication belong to the user. Batch them with a recommendation.
- Inspect repository guidance and current work before mutating; preserve unrelated work.
- Pause before deployments, releases, unauthorized merges, destructive data operations, force-pushes to shared history, production mutations, or messages to other people.
- Delegate only when isolation, independence, or bulk reduction materially improves the result. Give each delegate its outcome, scope, write authority, verification criteria, expected report, and stop condition. You own scope, decisions, synthesis, and final claims.
