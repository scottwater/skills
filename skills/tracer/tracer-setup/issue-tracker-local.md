# Issue tracker: Local Markdown

Issues and specs (PRDs) for this repo live as markdown files in `.tracer/`.

Before first use, run `git check-ignore -q .tracer`. If it is not ignored, add `/.tracer/` to the repository root's `.gitignore` before creating tracker state.

## Conventions

- One feature per directory: `.tracer/<feature-slug>/`
- The spec is `.tracer/<feature-slug>/spec.md`
- Implementation tickets are one file per ticket at `.tracer/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order — never a single combined tickets file
- Ticket state is a `Status:` line near the top of each file: `ready-for-agent` (fully specified, grabbable), `in-progress`, or `done`
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.tracer/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path directly.

## Blocking edges (used by /tracer-to-tickets)

A `Blocked by: <NN>, <NN>` line near the top of each ticket file (or `None — can start immediately`). A ticket is unblocked when every ticket it lists has `Status: done`.

**Frontier query** — the next tickets `/tracer-implement` can grab: scan `.tracer/<feature-slug>/issues/` for files with `Status: ready-for-agent` whose blockers are all `done`; lowest number first. Unblocked tickets with no edges between them can run in parallel (one `/tracer-implement` session each, in separate worktrees — set `Status: in-progress` when a session claims one).

## Wayfinding operations

Used by `/tracer-wayfinder`. Decision maps use the same feature directory but a separate `decisions/` collection so planning questions cannot be mistaken for executable implementation tickets.

- **Map**: `.tracer/<effort-slug>/map.md`. Its body holds Destination, Notes, Decisions so far, Not yet specified, and Out of scope.
- **Child decision ticket**: `.tracer/<effort-slug>/decisions/<NN>-<slug>.md`, numbered from `01` in map order. Record `Type: research|prototype|interview|task`, `Status: open|claimed|resolved|out-of-scope`, and `Blocked by: <NN>, <NN>|None` near the top, followed by `## Question`.
- **Blocking**: a decision is unblocked when every file named by `Blocked by` has `Status: resolved`. Create all new decision files before adding their blocker numbers.
- **Frontier query**: scan this map's `decisions/` directory in numeric order for `Status: open` files whose blockers are all resolved. `claimed` is in-flight and excluded.
- **Claim**: the single map coordinator changes `Status: open` to `Status: claimed` before dispatch or discussion. Parallel workers receive distinct pre-claimed question files; they do not claim for themselves. Reset an abandoned claim only after confirming its worker stopped.
- **Resolve child**: a worker returns an answer and map delta to the coordinator. The coordinator appends `## Answer` and `## Map delta` to the decision file and sets `Status: resolved`. Isolated worktrees must not edit `.tracer/` because this git-ignored state exists only in the coordinating checkout.
- **Update map**: the single coordinator applies completed deltas one at a time and appends each relative linked gist to Decisions so far. Do not run multiple coordinator sessions for one local map.
- **Out of scope**: the coordinator sets `Status: out-of-scope`, omits the ticket from Decisions so far, and appends one linked explanation under Out of scope.

Local `.tracer/` state is git-ignored and coordinates sessions on one checkout; use a configured shared tracker when collaborators on different machines need the same map.
