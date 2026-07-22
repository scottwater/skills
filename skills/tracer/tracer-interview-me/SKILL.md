---
name: tracer-interview-me
description: A relentless interview that asks every frontier question at once, round by round. The entry point of the main flow — interview until shared understanding, then hand off to /tracer-to-spec. Docs-aware in a codebase (reads/writes CONTEXT.md and ADRs), stateless without one.
disable-model-invocation: true
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask *now* without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

Finding *facts* is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it — don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the rest of the frontier now. The *decisions* are the user's — put each to them and wait.

## With a codebase (stateful)

When run inside a repo, the interview is document-aware in both directions:

- **Read before round 1:** `CONTEXT.md` (or `CONTEXT-MAP.md` and the relevant per-context files) and any `docs/adr/` entries touching the area. Existing glossary terms and ADRs are *settled decisions* — they prune the design tree before the first question is asked, and the frontier is computed against them. If the docs don't exist, proceed silently; don't suggest creating them upfront.
- **Write when settled:** when a round resolves a fuzzy or overloaded term, record it in `CONTEXT.md`'s glossary; when it settles a hard-to-reverse decision, record it as an ADR under `docs/adr/`. Follow `/tracer-domain-modeling`'s discipline and formats (its `CONTEXT-FORMAT.md` and `ADR-FORMAT.md`): the glossary stays a glossary — no implementation details — and an ADR is offered only when the decision is hard to reverse, surprising without context, *and* the result of a real trade-off. Write at the moment of settlement, not as a batch at the end — the paper trail is how the next session starts with a smaller tree. If the interview contradicts an existing ADR, that's a frontier question in its own right: surface it ("contradicts ADR-NNNN — reopen it?") and let the user decide.

## Without a codebase (stateless)

No repo, or a plan/idea that doesn't live in one: run the same interview with nothing read and nothing written. The design tree lives entirely in the conversation; the output is the shared understanding itself, carried forward by staying in the same context window.

## Done

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

**Then hand off:** once the user confirms, offer `/tracer-to-spec` — the settled tree is exactly what it synthesizes from. Keep the whole grill and the spec in one unbroken context window.
