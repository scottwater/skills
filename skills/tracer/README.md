# Tracer

A **tracer bullet** is thin and complete, and it visibly lands or visibly misses. That's the unit this whole flow produces, at every scale: tickets are tracer-bullet vertical slices, tests are tracer bullets through pre-agreed seams, and every task ends in a commit that either proves itself or gets sent back.

I've been using SuperPowers for a while, but I started to find them a bit overbearing. I also felt that brainstorming did not fully capture my intent. I started using Matt Pocock's skills and found that they did a better job of staying out of the way until I needed them. However, they did not follow through from start to finish quite as well as SuperPowers. What we have here is a blend of the two: the unobtrusiveness of Matt's skills and his excellent grill-me approach, combined with SuperPowers' push to the finish once we are locked in and doing work. This is still an experiment, so who knows for sure!

> [!IMPORTANT] I cannot state this enough. These skills are 99% built on the hard work of Matt and the SuperPowers team. At this point, I would highly recommend you start there and circle back only if you want to experiment with a more customized workflow.

A lean, user-invoked skill set for spec-driven development. Forked from two parents:

- **[Matt Pocock's skills](https://github.com/mattpocock/skills)** — the shape and philosophy: lightweight, user-invoked only (nothing auto-triggers), seams-first testing, durable prose specs/tickets, the two-axis review.
- **[superpowers](https://github.com/obra/superpowers)** — the execution machinery: precise task plans, fresh sub-agent per task, a review gate after every task with a fix → re-review loop, a commit per task, worktree isolation, and evidence-before-claims verification.

Entry-point workflows never auto-invoke. Supporting and vocabulary skills may load inside a flow you started. Invocation policy is declared in `SKILL.md` frontmatter (Claude Code) and `agents/openai.yaml` (Codex):

- **User-only** (13 skills) — every entry-point workflow, including [`tracer-wayfinder`](tracer-wayfinder/SKILL.md): only you can start it.
- **Supporting** ([`tracer-tdd`](tracer-tdd/SKILL.md), [`tracer-code-review`](tracer-code-review/SKILL.md), [`tracer-research`](tracer-research/SKILL.md)) — model-invocable references and delegated workflows used beneath a flow you started.
- **Vocabulary** ([`tracer-domain-modeling`](tracer-domain-modeling/SKILL.md), [`tracer-codebase-design`](tracer-codebase-design/SKILL.md)) — model-invoked references that define language and never run a process.

Not sure which skill fits? **[`/tracer-wat`](tracer-wat/SKILL.md)** is the router.

## The main flow: idea → ship

```
ordinary idea      → /tracer-interview-me ─┐
huge, foggy effort → /tracer-wayfinder ────┴→ /tracer-to-spec → /tracer-to-tickets → /tracer-implement (per ticket)
                                                                                              └→ optional review → /tracer-finish-branch

End-to-end alternative: replace `/tracer-implement` plus the explicit review/finish steps with `/tracer-autopilot`.
```

0. **[`/tracer-wayfinder`](tracer-wayfinder/SKILL.md)** — the situational on-ramp for an effort too large _and too foggy_ for one session. It charts a shared issue-tracker map of decision tickets, resolves one per session, and hands the cleared map to `/tracer-to-spec`. Skip it when the decision tree fits in one interview.
1. **[`/tracer-interview-me`](tracer-interview-me/SKILL.md)** — the normal entry point. A relentless interview structured as a design tree: each round asks the entire frontier of answerable questions at once, with recommended answers. Facts get looked up by sub-agents; decisions go to you. Docs-aware in a codebase (existing `CONTEXT.md`/ADRs prune the tree; settled terms and decisions get written back), stateless without one. Done when the frontier is empty and nothing is silently assumed.
2. **[`/tracer-to-spec`](tracer-to-spec/SKILL.md)** — synthesize the settled thread or cleared map into a spec (problem, user stories, implementation and testing decisions, pre-agreed test seams). No new interview — the decisions are already settled. Durable prose: no file paths or code.
3. **[`/tracer-to-tickets`](tracer-to-tickets/SKILL.md)** — split the spec into tracer-bullet vertical slices, each declaring its blocking edges. Skip for single-session work and go straight to `/tracer-implement`.
4. **[`/tracer-implement`](tracer-implement/SKILL.md)** — the visible, bounded workhorse. Per ticket: write an **ephemeral task plan** (exact paths, real code, interfaces, global constraints), show the execution shape for approval, implement and commit every task sequentially, then run two ticket-wide review passes with one targeted repair pass between them. It runs the full suite once, reports actionable and deferred concerns, and stops. It does not run a whole-branch audit or finish the branch.
5. Choose the close-out deliberately: run your own review pack or [`/tracer-code-review`](tracer-code-review/SKILL.md) when warranted, then invoke [`/tracer-finish-branch`](tracer-finish-branch/SKILL.md). For unattended end-to-end delivery, use [`/tracer-autopilot`](tracer-autopilot/SKILL.md), which preserves the former per-task review loops, whole-branch review, and branch-finishing flow.

For the ordinary path, keep steps 1–3 in one unbroken context window. Wayfinder deliberately spans sessions and persists its state in the map; `/tracer-to-spec` reloads every linked resolution. Each implementation or autopilot run starts fresh from its ticket.

**Parallel tickets:** frontier tickets with no edges between them each get their own implementation session in their own [`/tracer-worktrees`](tracer-worktrees/SKILL.md) checkout. Because every task commits, parallel sessions never collide on a dirty tree. Finish each branch explicitly, or choose `/tracer-autopilot` when that decision should remain inside the automated flow.

## Skills

| Skill | Role |
| --- | --- |
| [`tracer-wat`](tracer-wat/SKILL.md) | The router — which skill or flow fits your situation |
| [`tracer-wayfinder`](tracer-wayfinder/SKILL.md) | Huge, foggy effort → shared map of decision tickets → cleared route to a spec |
| [`tracer-interview-me`](tracer-interview-me/SKILL.md) | Frontier-driven interview until shared understanding — docs-aware in a repo, stateless without |
| [`tracer-to-spec`](tracer-to-spec/SKILL.md) | Conversation → durable spec with pre-agreed test seams |
| [`tracer-to-tickets`](tracer-to-tickets/SKILL.md) | Spec → tracer-bullet tickets with blocking edges |
| [`tracer-implement`](tracer-implement/SKILL.md) | Ticket → approved plan → sequential task commits → two bounded reviews → report and stop |
| [`tracer-autopilot`](tracer-autopilot/SKILL.md) | Ticket → per-task review loops → whole-branch review → branch finishing |
| [`tracer-code-review`](tracer-code-review/SKILL.md) | Two-axis review (Standards + Spec), severity-graded, with a fix → re-review loop |
| [`tracer-convince-me`](tracer-convince-me/SKILL.md) | Completed work → observable claims → fresh end-to-end evidence → honest verdict |
| [`tracer-tdd`](tracer-tdd/SKILL.md) | The red → green reference: good tests, seams, anti-patterns |
| [`tracer-worktrees`](tracer-worktrees/SKILL.md) | Isolated checkout per parallel ticket |
| [`tracer-setup`](tracer-setup/SKILL.md) | Once per repo: configure the issue tracker and domain-doc layout |
| [`tracer-finish-branch`](tracer-finish-branch/SKILL.md) | Verify → merge/PR/keep/discard → safe cleanup |
| [`tracer-prototype`](tracer-prototype/SKILL.md) | Throwaway code that answers one design question |
| [`tracer-research`](tracer-research/SKILL.md) | Focused primary-source research → one cited Markdown note |
| [`tracer-handoff`](tracer-handoff/SKILL.md) | Compact the conversation into a doc a fresh session picks up |
| [`tracer-domain-modeling`](tracer-domain-modeling/SKILL.md) | Vocabulary reference (model-invoked): glossary discipline, CONTEXT.md and ADR formats |
| [`tracer-codebase-design`](tracer-codebase-design/SKILL.md) | Vocabulary reference (model-invoked): deep modules, seams, interfaces |

## Conventions

- **Delegation:** Tracer owns workflow stages and review gates. A delegated pass satisfies one named Tracer step; the runtime supplies execution and isolation rather than additional stages.
- **`.tracer/`** (git-ignored) holds everything ephemeral: local specs and tickets (`.tracer/<feature>/`), and `/tracer-implement`'s workspace (`.tracer/implement/` — task plan, briefs, reports, review packages, progress ledger).
- **Durable vs. ephemeral:** specs and tickets are durable prose and never contain file paths or code; the task plan is ephemeral and contains exactly that. Precision lives where it can't go stale.
- **Evidence before claims:** no "done", "passing", or "fixed" without having run the proving command in the current session and read its output.
- If `docs/agents/issue-tracker.md` exists, `tracer-wayfinder` charts there and `tracer-to-spec`/`tracer-to-tickets` publish there; otherwise everything works locally under `.tracer/`. Run [`/tracer-setup`](tracer-setup/SKILL.md) once per repo to configure a real tracker (it seeds exact Wayfinding, blocking-edge, and frontier operations).

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
