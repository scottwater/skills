# Tracer

A **tracer bullet** is thin, complete, and visibly lands or visibly misses. That's the unit this whole flow produces, at every scale: tickets are tracer-bullet vertical slices, tests are tracer bullets through pre-agreed seams, and every task ends in a commit that either proves itself or gets sent back.

I been using SuperPowers for a while, but started to find them a big overbearing. I also felt like brainstorming was not fully capturing my intent. I started to use Matt Pocock's sills and found they did a better job of staying out of the way until I needed. However, I also found they did not follow through start to finish quite a well as SuperPowers. So what we have here is a fork of the two. The unubtrusiveness of Matt's skills with his excellent grill-me approach and once we are locked in and doing work, the SuperPowers push to the finish. This is still an experiment, so who knows for sure!

> [!IMPORTANT]
> I cannot state this enough. These skills are 99% based on the back of the hard work by Matt and the SuperPowers team. At this point, I would highly recommend you start there and circle back only if you want to experiment with a more customized workflow.

A lean, user-invoked skill set for spec-driven development. Forked from two parents:

- **[Matt Pocock's skills](https://github.com/mattpocock/skills)**  — the shape and philosophy: lightweight, user-invoked only (nothing auto-triggers), seams-first testing, durable prose specs/tickets, the two-axis review.
- **[superpowers](https://github.com/obra/superpowers)** — the execution machinery: precise task plans, fresh sub-agent per task, a review gate after every task with a fix → re-review loop, a commit per task, worktree isolation, and evidence-before-claims verification.

Nothing here auto-invokes. Three invocation tiers, declared twice per skill — `disable-model-invocation` in `SKILL.md` frontmatter (Claude Code) and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex):

- **User-only** (10 skills) — every entry-point workflow: only you can start it.
- **Internally driven** ([`tdd`](tdd/SKILL.md), [`code-review`](code-review/SKILL.md)) — model-invocable because `/implement` drives them as part of its gates; they never fire outside a flow you started.
- **Vocabulary** ([`domain-modeling`](domain-modeling/SKILL.md), [`codebase-design`](codebase-design/SKILL.md)) — model-invoked references that define language and never run a process.

Not sure which skill fits? **[`/wat`](wat/SKILL.md)** is the router.

## The main flow: idea → ship

```
/interview-me → /to-spec → /to-tickets → /implement (per ticket) → merge/PR
```

1. **[`/interview-me`](interview-me/SKILL.md)** — the entry point. A relentless interview worked as a design tree: each round asks the entire frontier of answerable questions at once, with recommended answers. Facts get looked up by sub-agents; decisions go to you. Docs-aware in a codebase (existing `CONTEXT.md`/ADRs prune the tree; settled terms and decisions get written back), stateless without one. Done when the frontier is empty and nothing is silently assumed.
2. **[`/to-spec`](to-spec/SKILL.md)** — synthesize the settled thread into a spec (problem, user stories, implementation and testing decisions, pre-agreed test seams). No interview — the grilling already happened. Durable prose: no file paths or code.
3. **[`/to-tickets`](to-tickets/SKILL.md)** — split the spec into tracer-bullet vertical slices, each declaring its blocking edges. Skip for single-session work and go straight to `/implement`.
4. **[`/implement`](implement/SKILL.md)** — the centerpiece. Per ticket: write an **ephemeral task plan** (exact paths, real code, interfaces, global constraints — precision that can't go stale because it dies with the branch), then execute it with a fresh implementer sub-agent per task, a **review gate after every task** (spec compliance + code quality, fix → re-review until approved), and a **commit per task**. Closes with a full-suite run, a whole-branch `/code-review`, and `/finish-branch`.

Keep steps 1–3 in one unbroken context window; each `/implement` starts fresh from its ticket.

**Parallel tickets:** frontier tickets with no edges between them each get their own `/implement` session in their own [`/worktrees`](worktrees/SKILL.md) checkout. Because every task commits, parallel sessions never collide on a dirty tree, and [`/finish-branch`](finish-branch/SKILL.md) merges or PRs each one when it's done.

## Skills

| Skill | Role |
|---|---|
| [`wat`](wat/SKILL.md) | The router — which skill or flow fits your situation |
| [`interview-me`](interview-me/SKILL.md) | Frontier-driven interview until shared understanding — docs-aware in a repo, stateless without |
| [`to-spec`](to-spec/SKILL.md) | Conversation → durable spec with pre-agreed test seams |
| [`to-tickets`](to-tickets/SKILL.md) | Spec → tracer-bullet tickets with blocking edges |
| [`implement`](implement/SKILL.md) | Ticket → plan → per-task implement/commit/review loop → reviewed branch |
| [`code-review`](code-review/SKILL.md) | Two-axis review (Standards + Spec), severity-graded, with a consuming fix → re-review loop |
| [`tdd`](tdd/SKILL.md) | The red → green reference: good tests, seams, anti-patterns |
| [`worktrees`](worktrees/SKILL.md) | Isolated checkout per parallel ticket |
| [`setup-tracer`](setup-tracer/SKILL.md) | Once per repo: configure the issue tracker and domain-doc layout |
| [`finish-branch`](finish-branch/SKILL.md) | Verify → merge/PR/keep/discard → safe cleanup |
| [`prototype`](prototype/SKILL.md) | Throwaway code that answers one design question |
| [`handoff`](handoff/SKILL.md) | Compact the conversation into a doc a fresh session picks up |
| [`domain-modeling`](domain-modeling/SKILL.md) | Vocabulary reference (model-invoked): glossary discipline, CONTEXT.md and ADR formats |
| [`codebase-design`](codebase-design/SKILL.md) | Vocabulary reference (model-invoked): deep modules, seams, interfaces |

## Conventions

- **`.tracer/`** (git-ignored) holds everything ephemeral: local specs and tickets (`.tracer/<feature>/`), and `/implement`'s workspace (`.tracer/implement/` — task plan, briefs, reports, review packages, progress ledger).
- **Durable vs. ephemeral:** specs and tickets are durable prose and never contain file paths or code; the task plan is ephemeral and contains exactly that. Precision lives where it can't go stale.
- **Evidence before claims:** no "done", "passing", or "fixed" without having run the proving command in the current session and read its output.
- If `docs/agents/issue-tracker.md` exists, `to-spec`/`to-tickets` publish to that tracker; otherwise everything works locally under `.tracer/`. Run [`/setup-tracer`](setup-tracer/SKILL.md) once per repo to configure a real tracker (it also seeds the exact commands for blocking edges and frontier queries).

## Install

Symlink each skill into your harness's skill directory, e.g.:

```bash
for s in */; do
  ln -sfn "$(pwd)/$s" ~/.claude/skills/"$(basename "$s")"
done
```

Or install via the skills CLI from the repo root:

```bash
npx skills add scottwater/skills
```
