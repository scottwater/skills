---
name: wat
description: Ask which skill or flow fits your situation. A router over the tracer skills.
disable-model-invocation: true
---

# Wat

You don't remember every skill, so ask.

Most work travels one **main flow**; a few skills run underneath it or stand alone. Everything here is user-invoked — nothing triggers itself.

## The main flow: idea → ship

1. **`/interview-me`** — start here. A relentless interview worked as a design tree: each round asks the **entire frontier** of currently answerable questions at once, numbered, each with a recommended answer. Facts get looked up by sub-agents; decisions are yours. In a codebase it's docs-aware — existing `CONTEXT.md`/ADRs prune the tree before round 1, and settled terms/decisions get written back; with no codebase it runs stateless. If a frontier question needs a *runnable* answer (does this state model feel right, what should this UI look like), detour through **`/prototype`** — throwaway code that answers the question; keep the answer, delete the code. Done when the frontier is empty and nothing is silently assumed — then it hands off to `/to-spec`.

2. **`/to-spec`** — synthesize the settled thread into a spec: problem, user stories, implementation and testing decisions, and the **pre-agreed test seams**. No interview — the grilling already happened. Durable prose: no file paths, no code.

3. **Branch — is this a multi-session build?**
   - **Yes** → **`/to-tickets`**: split the spec into tracer-bullet vertical slices, each declaring its **blocking edges**. Then kick off **`/implement`** per ticket, clearing context between each one.
   - **No** → **`/implement`** right here.

4. **`/implement`** — the workhorse. Per ticket it:
   - writes an **ephemeral task plan** (`.tracer/implement/plan.md`) — exact file paths, real code, interfaces, global constraints copied verbatim; the precision the durable spec/tickets deliberately omit, safe here because the plan dies with the branch;
   - executes one task at a time with a **fresh implementer sub-agent**, driving `/tdd` at the pre-agreed seams, **committing every task**;
   - gates every task with a **reviewer sub-agent** (spec compliance + code quality), looping fix → re-review until approved;
   - closes with a fresh full-suite run, a whole-branch **`/code-review`**, and **`/finish-branch`**.

Keep steps 1–3 in **one unbroken context window** — don't compact or clear until the tickets are published, so the grilling, spec, and tickets build on the same thinking. Each `/implement` then starts fresh from its ticket.

## Running tickets in parallel

Frontier tickets (all blockers done) with no edges between them can run **simultaneously** — one `/implement` session each:

- **`/worktrees`** first in each session — its own checkout, branch, and `.tracer/implement/` workspace. Because every task commits, parallel sessions never collide on a dirty tree.
- **`/finish-branch`** when each session's work is done — verify tests with fresh evidence, then merge / PR / keep / discard, with safe worktree cleanup.

## Standalone

- **`/code-review`** — two-axis review (Standards + Spec) of any diff against a fixed point, severity-graded with a verdict per axis. `/implement` calls it at close-out; reach for it directly to review a branch or PR. If you produced the diff, its findings loop back: Critical/Important means not done.
- **`/tdd`** — the red → green reference: what a good test is, seams, anti-patterns, rules of the loop. `/implement` drives it internally; use it alone to build one behaviour test-first without a full spec.
- **`/worktrees`** / **`/finish-branch`** — bookends for any isolated branch work, even outside the main flow.
- **`/prototype`** — a small, throwaway program that answers one design question. The detour in step 1, but reach for it any time a design question is hard to settle on paper.

## Vocabulary underneath

Two model-invoked references that run *beneath* the other skills — each the single source of truth for its vocabulary. They define language, never run a process; reach for them directly when the **words** are the problem, or let the skills above pull them in.

- **`/domain-modeling`** — the *domain* language: challenge a fuzzy term, resolve an overloaded word, record a hard-to-reverse decision as an ADR. Owns the `CONTEXT.md` and ADR formats that `/interview-me`'s docs-aware mode writes with.
- **`/codebase-design`** — the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*. `/to-spec`'s seam step, `/tdd`, and `/implement`'s Interfaces blocks all speak it.

## Crossing sessions

- **`/handoff`** — compacts the current conversation into a document a fresh session picks up. Use it when a thread fills up before `/to-tickets`, or to branch into a `/prototype` session and carry the answer back.
- **`/compact`** (built-in) — stay in the same conversation, letting earlier turns be summarized. Use at intentional breaks between phases; don't compact mid-phase. `/handoff` forks; `/compact` continues.

## Precondition (optional)

**`/setup-tracer`** — run once per repo to configure the issue tracker (`docs/agents/issue-tracker.md`: GitHub, GitLab, local, or your own) and domain-doc layout that `/to-spec`, `/to-tickets`, and `/code-review` read. Skippable: everything falls back to local markdown under `.tracer/`.

## What's deliberately not here

No auto-triggering workflows, no brainstorming skill (that's `/interview-me`'s job), no triage/wayfinder on-ramps — this set covers idea → ship, self-contained. Heavyweight multi-reviewer packs (e.g. `/code-quorum`) compose at milestone boundaries, not per task.
