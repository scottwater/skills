# Issue tracker: GitLab

Issues and specs (PRDs) for this repo live as GitLab issues. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`. Use a heredoc for multi-line descriptions.
- **Read an issue**: `glab issue view <number> --comments`. Use `-F json` for machine-readable output.
- **List issues**: `glab issue list -F json` with appropriate `--label` filters.
- **Comment on an issue**: `glab issue note <number> --message "..."`. GitLab calls comments "notes".
- **Apply / remove labels**: `glab issue update <number> --label "..."` / `--unlabel "..."`. Comma-separate or repeat the flag for multiple labels.
- **Close**: `glab issue close <number>` — it does not accept a closing comment, so post the explanation first with `glab issue note`, then close.
- **Merge requests**: GitLab calls PRs "merge requests" — `glab mr create`, `glab mr view`, `glab mr note`, the same shape as `gh pr ...` with `mr` for `pr` and `note`/`--message` for `comment`/`--body`. (`/tracer-finish-branch`'s "create a PR" means `glab mr create` here.)

Infer the repo from `git remote -v` — `glab` does this automatically when run inside a clone.

GitLab numbers issues and MRs separately, so `#42` is unambiguous once you know which surface is meant.

## When a skill says "publish to the issue tracker"

Create a GitLab issue. Tickets published by `/tracer-to-tickets` get the `ready-for-agent` label — they are fully specified and agent-grabbable by construction.

## When a skill says "fetch the relevant ticket"

Run `glab issue view <number> --comments`.

## Blocking edges (used by /tracer-to-tickets)

Express each ticket's blockers as GitLab's **native blocking link** — the canonical, UI-visible representation:

- **Add an edge**: post the `/blocked_by #<blocker>` quick action as a note: `glab issue note <child> --message "/blocked_by #<blocker>"`.
- **Availability**: native blocking links are a Premium/Ultimate feature. On the free tier (or where unavailable), fall back to a `Blocked by: #<n>, #<n>` line at the top of the description. A ticket is unblocked when every blocker is closed.
- **Check blockers**: `glab api projects/:id/issues/:iid/links` (native), or the `Blocked by` line.

**Frontier query** — the next tickets `/tracer-implement` can grab: `glab issue list -F json` scoped to open `ready-for-agent` issues, drop any with an open blocker or an assignee.

**Parent linkage**: put `Part of #<parent>` at the top of each ticket description (or use epics where available). Never close or modify the parent when publishing.
