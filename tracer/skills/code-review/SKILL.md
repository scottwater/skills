---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents, reports them side by side with severity-graded findings and a verdict per axis. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings. Each axis returns severity-graded findings and an explicit verdict — a review that only narrates is a review nobody can act on.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it (when called from `/implement`, it's the branch's merge-base).

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here — not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. A path or issue reference the caller passed as an argument.
2. Issue references in the commit messages (`#123`, `Closes #45`, etc.) — fetch via the tracker workflow in `docs/agents/issue-tracker.md` if it exists.
3. A PRD/spec file under `docs/`, `specs/`, or `.tracer/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below — a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and, like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` tool calls. Use the `general-purpose` subagent for both. Both prompts carry this preamble:

> Verify, don't trust. Commit messages, code comments, and any implementer report are unverified claims — judge only the diff. Read-only review: never mutate the working tree, index, or HEAD.
>
> Grade every finding: **Critical** (bugs, data loss, security, broken functionality), **Important** (can't be trusted until fixed — incorrect or fragile behavior, a missed requirement, swallowed errors, tests that assert nothing), or **Minor** (polish, style, "coverage could be broader"). Not everything is Critical. Every finding cites file:line and says why it matters. End with a verdict: **Approved** or **Needs fixes** (any Critical/Important finding means Needs fixes).

**Standards sub-agent prompt** — additionally include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full — the sub-agent has no other access to it.
- The brief: "Report — per file/hunk where relevant — (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Documented-standard breaches take the severity their impact earns; baseline smells are judgement calls and default to Minor unless the damage is concrete (e.g. verbatim duplication of a logic block is Important). A documented repo standard overrides the baseline. Skip anything tooling enforces."

**Spec sub-agent prompt** — additionally include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) **Missing** — requirements the spec asked for that are absent or partial; (b) **Extra** — behaviour in the diff that wasn't asked for (scope creep); (c) **Misunderstood** — requirements that look implemented but wrongly. Quote the spec line for each finding. A missing or misunderstood requirement is at least Important."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, each ending with its verdict. Do **not** merge or rerank findings — the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: verdict and finding counts per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes — that's the reranking the separation exists to prevent.

### 6. Consuming the review

A review with open Critical/Important findings means **the work is not done** — reporting is not resolving. If you produced the diff under review (e.g. called from `/implement`):

1. **Verify before implementing.** Each finding is a claim — check it against the codebase. If a finding is wrong for this codebase (breaks existing behavior, misses context, violates YAGNI — grep for actual usage before "implementing properly"), push back with technical reasoning or put it to the user; don't blindly apply it. No performative agreement either way — evaluate, then fix or contest.
2. **Fix in one pass.** Dispatch one fix sub-agent (or fix inline) with the complete list of confirmed Critical/Important findings — never one fixer per finding. The fixer re-runs the covering tests and reports the output.
3. **Re-review the failed axis** on the updated diff. Loop until both axes are Approved.
4. Minor findings: fix cheaply now or record where the user will see them — never silently discard.

If the user asked for the review of someone else's changes, stop after step 5 — the report is the deliverable.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
