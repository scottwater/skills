---
name: tracer-implement
description: "Implement a ticket or spec with a task plan, fresh sub-agent per task, a review gate after every task, and a commit per task."
disable-model-invocation: true
---

# Implement

Implement the work described in a ticket (from `/tracer-to-tickets`), a spec, or the user's description. The flow is: **plan → per-task loop (implement, commit, review, fix) → final review → finish the branch**. Precision comes from the plan; quality comes from the review gates; parallel-safety comes from committing every task on an isolated branch.

## Phase 0 — Workspace

1. **Never implement on `main`/`master`.** If you're on it, create a feature branch. If this ticket will run alongside other work, use `/tracer-worktrees` for an isolated checkout instead.
2. **Check for a ledger.** If `.tracer/implement/progress.md` exists, a previous session was mid-flight: tasks it marks complete are DONE — verify against `git log`, then resume at the first incomplete task. Trust the ledger and git over your own recollection.
3. Ensure `.tracer/` is git-ignored (`git check-ignore -q .tracer` — if not, add it to `.gitignore` and commit).
4. Run the test suite once to confirm a clean baseline. If it's already red, stop and report — don't build on a broken base.

## Phase 1 — Task plan

Tickets and specs deliberately avoid file paths and code because they'd go stale. The plan is where that precision gets manufactured — it's **ephemeral** (lives in `.tracer/implement/plan.md`, dies with the branch), so exact paths and real code belong here.

Write the plan as if the implementer has zero context for this codebase and questionable taste — because each task's implementer is a fresh sub-agent that sees only its own task.

**Header:**

```markdown
# <Feature> — Task Plan

**Goal:** one sentence.
**Ticket/Spec:** reference or path.
**Architecture:** 2–3 sentences.
**Seams under test:** the pre-agreed seams from the spec (see /tracer-tdd) — every test in this plan lives at one of these.

## Global Constraints

Project-wide requirements copied VERBATIM from the spec/ticket — exact
values, version floors, naming rules, copy strings. Every task implicitly
includes this section.
```

**Each task:**

````markdown
### Task N: <name>

**Files:**
- Create: `exact/path/to/file.ts`
- Modify: `exact/path/to/existing.ts`
- Test: `exact/path/to/file.test.ts`

**Interfaces:**
- Consumes: what this task uses from earlier tasks — exact signatures
- Produces: what later tasks rely on — exact names, parameter and return
  types. (A task's implementer sees only its own task; this block is how
  it learns what its neighbours expect.)

Steps, each one small action: write the failing test (show the actual test
code), run it and confirm it fails (exact command + expected failure),
write the minimal implementation (show the code), run and confirm green,
**commit** (exact `git commit` message).
````

**Right-sizing:** a task is the smallest unit that carries its own test cycle and is worth a fresh reviewer's gate. Fold setup/scaffolding into the task whose deliverable needs it; split only where a reviewer could reject one task while approving its neighbour.

**No placeholders — these are plan failures, never write them:**
- "TBD", "add appropriate error handling", "handle edge cases"
- "Write tests for the above" without the actual test code
- "Similar to Task N" (repeat the code — tasks are read in isolation)
- References to types or functions no task defines

**Self-review the plan** before executing (a checklist you run yourself, not a dispatch):
1. **Spec coverage** — walk the ticket/spec requirement by requirement; point each at a task. Gaps become tasks.
2. **Placeholder scan** — search the plan for the patterns above; fix inline.
3. **Interface consistency** — do names/signatures used in later tasks match what earlier tasks define?

If the plan surfaced a contradiction in the ticket/spec itself, put it to the user as one batched question before executing — not one interrupt per discovery mid-run.

## Phase 2 — Per-task loop

For each task, in order:

1. **Record BASE:** `BASE=$(git rev-parse HEAD)` — before dispatching. Re-reviews and multi-commit tasks depend on this; never substitute `HEAD~1` later.
2. **Extract the brief:** run this skill's `scripts/task-brief plan.md N` — it writes `.tracer/implement/task-N-brief.md` and prints the path. The brief, not pasted text, is the implementer's source of requirements.
3. **Dispatch a fresh implementer sub-agent** using [implementer-prompt.md](implementer-prompt.md). The dispatch contains: one line of scene-setting (where this task fits), the brief path, interfaces/decisions from earlier tasks the brief can't know, your resolution of any ambiguity you noticed, and the report-file path (`.tracer/implement/task-N-report.md`). Exact values live only in the brief — don't paste the plan or prior-task history into the prompt.
4. **Handle the status it returns:**
   - **DONE** → proceed to review.
   - **DONE_WITH_CONCERNS** → read the concerns. Correctness or scope doubts: address before review. Observations: note them, proceed.
   - **NEEDS_CONTEXT** → provide the missing context, re-dispatch.
   - **BLOCKED** → change something before retrying: more context, a more capable model, a smaller task split, or escalate to the user if the plan itself is wrong. Never re-run the same dispatch unchanged.
5. **Review the task** (Phase 3). Only a clean review marks the task complete.
6. **Update the ledger:** append to `.tracer/implement/progress.md`:
   `Task N: complete (commits <base7>..<head7>, review clean)`.

Do not pause between tasks to check in — the user asked for the ticket implemented. Stop only for BLOCKED you can't resolve, genuine ambiguity, or completion.

## Phase 3 — Task review gate

Every task gets reviewed by a fresh sub-agent before the next task starts — issues caught here are cheap; the same issue three tasks later has cascaded.

1. **Build the review package:** run `scripts/review-package $BASE HEAD` — it writes the commit list, stat summary, and full diff to one file and prints the path. The diff never enters your context.
2. **Dispatch the task reviewer** using [task-reviewer-prompt.md](task-reviewer-prompt.md), passing three paths — brief, report, review package — plus the plan's Global Constraints copied verbatim. Never tell a reviewer what *not* to flag or pre-rate a finding's severity; if you think a finding will be a false positive, let it be raised and adjudicate then.

   **High-risk tasks** — concurrency, auth/permissions, data migration, irreversible operations, money: dispatch two or three reviewers in parallel instead of one, each restricted to a single lens from the template (silent failures / hidden assumptions & failure modes / test integrity), and merge their findings yourself. A small quorum for the tasks that earn it; the single generalist reviewer stays the default.
3. **Act on the verdicts.** The reviewer returns a spec-compliance verdict and a quality verdict:
   - Both clean → task complete.
   - **Critical or Important findings** → dispatch one fix sub-agent with the complete findings list (fixes spec gaps and quality issues together). The fixer re-runs the covering tests and appends results to the report file. Then re-run `review-package $BASE HEAD` and **re-review**. Loop until approved — never proceed with open Critical/Important findings.
   - **Minor findings** → record in the ledger; the final review triages them.
   - **⚠️ cannot-verify items** (requirements living in unchanged code or spanning tasks) → resolve them yourself; you hold the cross-task context. A confirmed gap is a failed spec review — back to the fixer.

## Phase 4 — Close out

1. **Full suite, fresh evidence.** Run the complete test suite and typecheck now (focused tests were fine during the loop). No completion claim without having run the proving command *in this session* and read its output — "should pass" is not a status.
2. **Whole-branch review:** run `/tracer-code-review` against the branch point (`git merge-base main HEAD`), pointing it at the originating ticket/spec and the ledger's list of accumulated Minor findings. Treat its Critical/Important findings as un-done work: dispatch **one** fix sub-agent with the complete list (never one fixer per finding), then re-run the failed axis until it approves. (A heavyweight multi-reviewer pack — e.g. `/code-quorum` — belongs at milestone boundaries or before merging a large feature, not per task; the task gates exist so it finds little.)
3. **Finish the branch:** use `/tracer-finish-branch` — verify tests, then present the merge / PR / keep / discard options. Everything is committed by construction; nothing rides on a dirty working tree.

## Inline mode

If sub-agents are unavailable, or the ticket is genuinely one task big, run the same shape yourself: plan (even a three-line plan states files, interface, and test), TDD at the pre-agreed seams, **commit per task**, self-review against the brief with the reviewer prompt's checklist, full suite + `/tracer-code-review` + `/tracer-finish-branch` at the end. The gates don't disappear when the sub-agents do.

## Red flags — never

- Implement on `main`/`master` without explicit user consent
- Leave work uncommitted at the end of a task, or batch several tasks into one commit
- Skip the task review, accept a review missing either verdict, or move on with open Critical/Important findings
- Skip the fix → re-review loop ("the fix is obviously right" is not a re-review)
- Dispatch parallel implementers inside one ticket (they conflict; parallelism belongs at the ticket/worktree level)
- Paste the whole plan or session history into a dispatch — brief file + interfaces + constraints, nothing else
- Trust an implementer's or fixer's report without the reviewer verifying it against the diff
- Re-dispatch a task the ledger already marks complete
- Claim done without fresh full-suite evidence from this session
