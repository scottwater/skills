# Issue tracker: GitLab

Issues and specs (PRDs) for this repo live as GitLab issues. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`. Use a heredoc for multi-line descriptions.
- **Read an issue**: `glab issue view <number> --comments`. Use `--output json` for machine-readable output.
- **List issues**: `glab issue list --output json` with appropriate `--label` filters. Add `--all` when every page and state is required.
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

**Frontier query** — the next tickets `/tracer-implement` can grab: `glab issue list --output json` scoped to open `ready-for-agent` issues, drop any with an open blocker or an assignee.

**Parent linkage**: put `Part of #<parent>` at the top of each ticket description (or use epics where available). Never close or modify the parent when publishing.

## Wayfinding operations

Used by `/tracer-wayfinder`. A Wayfinder **map** is one issue whose children are decision tickets; these planning tickets are distinct from the `ready-for-agent` implementation tickets above.

- **Labels**: ensure `wayfinder:map` and the type labels `wayfinder:research`, `wayfinder:prototype`, `wayfinder:interview`, and `wayfinder:task` exist before first use.
- **Map**: `glab issue create --title "<title>" --description "$(cat <body-file>)" --label wayfinder:map`. Its description holds Destination, Notes, Decisions so far, Not yet specified, and Out of scope.
- **Child decision ticket**: create an issue with `Part of #<map>` as the first description line and one `wayfinder:<type>` label. The marker is the parent relationship on every GitLab tier.
- **Blocking**: use the native blocking-link operation from the section above, with the same description-line fallback. Add edges only after every new ticket has an identity.
- **Enumerate children**: `glab issue list --all --output json | jq --arg parent "Part of #<map>" '[.[] | select(.description | startswith($parent))] | sort_by(.iid)'` returns every child across pages and states in deterministic IID order. Use this complete set for reconciliation and `/tracer-to-spec` hydration.
- **Frontier query**: filter the complete child set to open issues with no assignee, then drop any with an open blocker from `glab api projects/:id/issues/:iid/links` (or the fallback description check).
- **Claim**: the single map coordinator runs `glab issue update <n> --assignee @me` before dispatch or discussion. Parallel workers receive distinct pre-claimed ticket numbers; they never race this operation. Clear an abandoned claim only after confirming its worker stopped.
- **Resolve child**: the ticket worker posts one note containing `## Answer` and `## Map delta`, then closes the child. It never edits the map description.
- **Update map**: the single coordinator fetches the current description, applies completed deltas one at a time, and writes it with `glab issue update <map> --description "$(cat <body-file>)"`. Do not run multiple coordinator sessions for one map.
- **Out of scope**: the worker closes the child with an out-of-scope delta; the coordinator omits it from Decisions so far and appends one linked explanation under Out of scope.
