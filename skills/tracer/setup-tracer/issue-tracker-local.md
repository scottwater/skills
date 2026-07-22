# Issue tracker: Local Markdown

Issues and specs (PRDs) for this repo live as markdown files in `.tracer/` (git-ignored).

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

## Blocking edges (used by /to-tickets)

A `Blocked by: <NN>, <NN>` line near the top of each ticket file (or `None — can start immediately`). A ticket is unblocked when every ticket it lists has `Status: done`.

**Frontier query** — the next tickets `/implement` can grab: scan `.tracer/<feature-slug>/issues/` for files with `Status: ready-for-agent` whose blockers are all `done`; lowest number first. Unblocked tickets with no edges between them can run in parallel (one `/implement` session each, in separate worktrees — set `Status: in-progress` when a session claims one).
