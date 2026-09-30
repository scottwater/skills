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

Create a GitHub issue. Tickets published by `/tracer-to-tickets` get the `ready-for-agent` label — they are fully specified and agent-grabbable by construction.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.

## Blocking edges (used by /tracer-to-tickets)

Express each ticket's blockers as GitHub's **native issue dependencies** — the canonical, UI-visible representation:

- **Add an edge**: `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, where `<blocker-db-id>` is the blocker's numeric **database id** (`gh api repos/<owner>/<repo>/issues/<n> --jq .id` — *not* the `#number` or `node_id`).
- **Check blockers**: GitHub reports `issue_dependencies_summary.blocked_by` (open blockers only — the live gate).
- **Fallback** where dependencies aren't available: a `Blocked by: #<n>, #<n>` line at the top of the ticket body. A ticket is unblocked when every blocker is closed.

**Frontier query** — the next tickets `/tracer-implement` can grab: list open `ready-for-agent` issues, drop any with an open blocker (`issue_dependencies_summary.blocked_by > 0`, or an open issue in the `Blocked by` line) or an assignee.

**Parent linkage**: where sub-issues are enabled, attach tickets to their parent spec issue as sub-issues; otherwise put `Part of #<parent>` at the top of each ticket body. Never close or modify the parent when publishing.

## Wayfinding operations

Used by `/tracer-wayfinder`. A Wayfinder **map** is one issue whose children are decision tickets; these planning tickets are distinct from the `ready-for-agent` implementation tickets above.

- **Labels**: ensure `wayfinder:map` and the type labels `wayfinder:research`, `wayfinder:prototype`, `wayfinder:interview`, and `wayfinder:task` exist before first use (`gh label create "<label>" --force`).
- **Map**: `gh issue create --title "<title>" --body-file <body-file> --label wayfinder:map`. Its body holds Destination, Notes, Decisions so far, Not yet specified, and Out of scope.
- **Child decision ticket**: create an issue with one `wayfinder:<type>` label. Resolve its database id with `gh api repos/<owner>/<repo>/issues/<child> --jq .id`, then attach it with `gh api --method POST repos/<owner>/<repo>/issues/<map>/sub_issues -F sub_issue_id=<child-db-id>`. Where sub-issues are unavailable, put `Part of #<map>` at the top of the child and maintain a task-list link in the map.
- **Blocking**: use the native dependency operation from the section above, with the same body-line fallback. Add edges only after every new ticket has an identity.
- **Enumerate children**: with sub-issues, `gh api --paginate repos/<owner>/<repo>/issues/<map>/sub_issues` returns every child in configured order. With the fallback, run `gh issue list --state all --limit 1000 --json number,title,body,state,assignees,labels | jq --arg parent "Part of #<map>" '[.[] | select(.body | startswith($parent))] | sort_by(.number)'`; cross-check the map task list if it exists. Use the complete open-and-closed set for reconciliation and `/tracer-to-spec` hydration.
- **Frontier query**: filter the complete child set to open issues with no assignee, then fetch each candidate's blocker state through the dependency endpoint or fallback body line. Do not query every Wayfinder ticket in the repo as one frontier.
- **Claim**: the single map coordinator runs `gh issue edit <n> --add-assignee @me` before dispatch or discussion. Parallel workers receive distinct pre-claimed ticket numbers; they never race this operation. Clear an abandoned claim only after confirming its worker stopped.
- **Resolve child**: the ticket worker posts one comment containing `## Answer` and `## Map delta`, then closes the child. It never edits the map body.
- **Update map**: the single coordinator fetches the current body, applies completed deltas one at a time, and writes it with `gh issue edit <map> --body-file <file>`. Do not run multiple coordinator sessions for one map.
- **Out of scope**: the worker closes the child with an out-of-scope delta; the coordinator omits it from Decisions so far and appends one linked explanation under Out of scope.
