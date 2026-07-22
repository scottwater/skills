# Issue tracker: GitHub

Issues and specs (PRDs) for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either — resolve with `gh issue view 42` and fall back to `gh pr view 42`.

## When a skill says "publish to the issue tracker"

Create a GitHub issue. Tickets published by `/to-tickets` get the `ready-for-agent` label — they are fully specified and agent-grabbable by construction.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.

## Blocking edges (used by /to-tickets)

Express each ticket's blockers as GitHub's **native issue dependencies** — the canonical, UI-visible representation:

- **Add an edge**: `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, where `<blocker-db-id>` is the blocker's numeric **database id** (`gh api repos/<owner>/<repo>/issues/<n> --jq .id` — *not* the `#number` or `node_id`).
- **Check blockers**: GitHub reports `issue_dependencies_summary.blocked_by` (open blockers only — the live gate).
- **Fallback** where dependencies aren't available: a `Blocked by: #<n>, #<n>` line at the top of the ticket body. A ticket is unblocked when every blocker is closed.

**Frontier query** — the next tickets `/implement` can grab: list open `ready-for-agent` issues, drop any with an open blocker (`issue_dependencies_summary.blocked_by > 0`, or an open issue in the `Blocked by` line) or an assignee.

**Parent linkage**: where sub-issues are enabled, attach tickets to their parent spec issue as sub-issues; otherwise put `Part of #<parent>` at the top of each ticket body. Never close or modify the parent when publishing.
