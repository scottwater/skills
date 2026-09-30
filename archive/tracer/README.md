# Tracer

A **tracer bullet** is thin and complete, and it visibly lands or visibly misses. That's the unit this whole flow produces, at every scale: tickets are tracer-bullet vertical slices, tests are tracer bullets through pre-agreed seams, and every task ends in a commit that either proves itself or gets sent back.

I've been using SuperPowers for a while, but I started to find them a bit overbearing. I also felt that brainstorming did not fully capture my intent. I started using Matt Pocock's skills and found that they did a better job of staying out of the way until I needed them. However, they did not follow through from start to finish quite as well as SuperPowers. What we have here is a blend of the two: the unobtrusiveness of Matt's skills and his excellent grill-me approach, combined with SuperPowers' push to the finish once we are locked in and doing work. This is still an experiment, so who knows for sure!

> [!IMPORTANT] I cannot state this enough. These skills are 99% built on the hard work of Matt and the SuperPowers team. At this point, I would highly recommend you start there and circle back only if you want to experiment with a more customized workflow.

A lean skill set for spec-driven development. Forked from two parents:

- **[Matt Pocock's skills](https://github.com/mattpocock/skills)** — the shape and philosophy: lightweight, user-invoked only (nothing auto-triggers), seams-first testing, durable prose specs/tickets, the two-axis review.
- **[superpowers](https://github.com/obra/superpowers)**: the original execution machinery. Tracer retains coherent commits, worktree isolation, and evidence before claims, but now defaults to short plans, one implementation context, focused checks, and one review.

Entry-point workflows require explicit invocation. Supporting and vocabulary skills may load inside a flow you started. Invocation policy is declared in `SKILL.md` frontmatter (Claude Code) and `agents/openai.yaml` (Codex):

- **User-only** (12 skills) — every entry-point workflow, including [`tracer-build`](tracer-build/SKILL.md) and [`tracer-wayfinder`](tracer-wayfinder/SKILL.md): only you can start them.
- **Supporting** ([`tracer-tdd`](tracer-tdd/SKILL.md), [`tracer-code-review`](tracer-code-review/SKILL.md), [`tracer-research`](tracer-research/SKILL.md)) — model-invocable references and delegated workflows used beneath a flow you started.
- **Vocabulary** ([`tracer-domain-modeling`](tracer-domain-modeling/SKILL.md), [`tracer-codebase-design`](tracer-codebase-design/SKILL.md)) — model-invoked references that define language and never run a process.

Not sure which skill fits? **[`/tracer-wat`](tracer-wat/SKILL.md)** is the router.

## The main flow: idea → ship

Start at the lightest useful step. A concrete request can go directly to [`/tracer-build`](tracer-build/SKILL.md): quick plan, implement here with minimal delegation, then Convince Me evidence and a review recommendation. It calls out `main`/`master` and continues in place. Use `/tracer-implement` when you want plan approval and a review cycle; interview, spec, and ticketing are optional structure.

```
ordinary idea      → /interview-me ─┐
huge, foggy effort → /tracer-wayfinder ────┴→ /tracer-to-spec → /tracer-to-tickets → /tracer-implement (per ticket)
                                                                                              └→ optional review → /tracer-finish-branch

End-to-end alternative: replace `/tracer-implement` plus the explicit review/finish steps with `/tracer-autopilot`.
```

0. **[`/tracer-wayfinder`](tracer-wayfinder/SKILL.md)** — the situational on-ramp for an effort too large _and too foggy_ for one session. It charts a shared issue-tracker map of decision tickets, resolves one per session, and hands the cleared map to `/tracer-to-spec`. Skip it when the decision tree fits in one interview.
1. **[`/interview-me`](../../skills/interview-me/SKILL.md)** — the normal entry point. A relentless interview structured as a design tree: each round asks the entire frontier of answerable questions at once, with recommended answers. Facts get looked up by sub-agents; decisions go to you. It reads and writes no docs. Done when the frontier is empty and nothing is silently assumed.
2. **[`/tracer-to-spec`](tracer-to-spec/SKILL.md)**: write concise acceptance criteria, explicit decisions, safety limits, and focused verification from the settled thread or cleared map. No exhaustive story list or new architecture disguised as requirements.
3. **[`/tracer-to-tickets`](tracer-to-tickets/SKILL.md)** — split the spec into tracer-bullet vertical slices, each declaring its blocking edges. Skip for single-session work and go straight to `/tracer-implement`.
4. **[`/tracer-implement`](tracer-implement/SKILL.md)**: approve a short approach and verification plan, then implement the cohesive change in one context. Reuse existing facilities; new custom infrastructure needs an explicit decision. Review once, repair accepted defects in one pass, and recheck corrections only if code changed. Report focused evidence and concerns, leaving the branch in place. Full-suite runs need policy, a user request, or an impact-based reason.
5. Choose close-out deliberately with [`/tracer-finish-branch`](tracer-finish-branch/SKILL.md), adding a separate review only when warranted. For delivery without routine checkpoints, use [`/tracer-autopilot`](tracer-autopilot/SKILL.md). It uses the same proportionate implementation and review, then asks for your branch-finishing choice. Review/repair limits cover the whole delivery and survive resumes. **Complete** and **Complete with follow-ups** lead to that choice; **Blocked** preserves the workspace.

For the ordinary path, keep steps 1–3 in one unbroken context window. Wayfinder deliberately spans sessions and persists its state in the map; `/tracer-to-spec` reloads every linked resolution. Each implementation or autopilot run starts fresh from its ticket.

**Parallel tickets:** frontier tickets with no edges between them each get their own implementation session in their own [`/tracer-worktrees`](tracer-worktrees/SKILL.md) checkout. Because every task commits, parallel sessions never collide on a dirty tree. Finish each branch explicitly, or choose `/tracer-autopilot` when that decision should remain inside the automated flow.

## Skills

| Skill | Role |
| --- | --- |
| [`tracer-wat`](tracer-wat/SKILL.md) | The router — which skill or flow fits your situation |
| [`tracer-wayfinder`](tracer-wayfinder/SKILL.md) | Huge, foggy effort → shared map of decision tickets → cleared route to a spec |
| [`interview-me`](../../skills/interview-me/SKILL.md) | Frontier-driven interview until shared understanding (standalone skill, shared with Tracer) |
| [`tracer-to-spec`](tracer-to-spec/SKILL.md) | Conversation → durable spec with pre-agreed test seams |
| [`tracer-to-tickets`](tracer-to-tickets/SKILL.md) | Spec → tracer-bullet tickets with blocking edges |
| [`tracer-build`](tracer-build/SKILL.md) | Request → quick plan → implement here → Convince Me → review recommendation |
| [`tracer-implement`](tracer-implement/SKILL.md) | Request → short approved plan → implement → one review → repair/recheck if needed → report |
| [`tracer-autopilot`](tracer-autopilot/SKILL.md) | Proportionate delivery without routine checkpoints → explicit branch decision |
| [`tracer-code-review`](tracer-code-review/SKILL.md) | Two-axis review (Standards + Spec), severity-graded, with a fix → re-review loop |
| [`convince-me`](../../skills/convince-me/SKILL.md) | Completed work → observable claims → fresh end-to-end evidence → honest verdict (standalone skill, shared with Tracer) |
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

- **Delegation:** Tracer owns workflow stages and review budgets. A delegated pass satisfies one named Tracer step; the runtime supplies execution and isolation rather than additional stages. Helpers return findings to the controller within that budget.
- **Shared procedures:** Implement and Autopilot share worker/reviewer prompts. Autopilot uses Finish Branch's [finishing procedure](tracer-finish-branch/branch-finishing.md), carrying forward the agreed evidence scope. Build always runs Convince Me's [proof protocol](../../skills/convince-me/SKILL.md); other workflows use it only when explicitly requested.
- **`.tracer/`** (git-ignored) holds everything ephemeral: local specs and tickets (`.tracer/<feature>/`), and `/tracer-implement`'s workspace (`.tracer/implement/` — task plan, briefs, reports, review packages, progress ledger).
- **Durable vs. ephemeral:** specs and tickets preserve acceptance and explicit decisions. Short ephemeral plans name affected paths and checks; code is written during implementation rather than duplicated in the plan.
- **Evidence before claims:** report only observed results. Reuse recorded evidence on resume only after verifying the same unchanged HEAD and tracked tree; rerun affected checks after changes.
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
