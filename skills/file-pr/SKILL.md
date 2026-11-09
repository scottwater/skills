---
name: file-pr
description: File a concise pull request that leads with the problem. Use when filing, opening, or creating a PR.
---

# File PR

Before filing, check whether a PR for this branch already exists. Review the
diff locally against the base branch (usually `origin/main`) to make sure its
contents match the goal.

PR titles usually become commit messages, so follow the repository's title
conventions. Look at recently merged PRs and Git history for examples. Prefer a
concise, human-readable title that explains why the change matters:

BAD

> ❌ perf(server): negotiate permessage-deflate on the websocket

GOOD

> ✅ perf(server): cut websocket frame size by 70%+ with gzipping

Open the description with a brief overview of three or four sentences at most:
the shortest text that gets a reviewer up to speed. Explain the problem simply,
based on the user's original prompt, then give the solution in a sentence. Do
not lead with an implementation inventory:

BAD

> ❌ Removed implicit workspace carry-over from every "new thread" entry point (cmd+n / cmd+shift+o, sidebar v1/v2 buttons, command palette). New threads inherit only the project from context; branch, worktree, and env mode always come from the configured defaults. Deleted buildContextualThreadOptions, startNewThreadInProjectFromContext, and the v1 sidebar's seed-context machinery.

GOOD

> ✅ My "new worktree" default was ignored when starting new threads on existing worktrees. Super unintuitive. Now your preferences always apply.

If the change is visible, add a screenshot after the overview.

Fold everything else into a collapsed `<details>` block below the overview:
implementation notes, file-by-file changes, testing, and trade-offs. GitHub
shows only the `<summary>` line until a reviewer expands it. The summary names
the public model, effort level, and harness that made the changes, so the
reviewer knows what is folded away. Include subagent models that wrote part of
the change. Use the model name the harness reports. If model identity is
unavailable, name the harness without guessing a model. Leave a blank line
after `</summary>` and before `</details>` so GitHub renders the Markdown
inside:

```markdown
<details>
<summary>Claude Opus 5.5 (xhigh) in Claude Code</summary>

## Implementation

...

</details>
```

When the overview already says everything, skip the block and end the
description with `Created with <model> in <harness>.` instead.

Before submission, check the title, description, quotes, and attachments for
secrets and private details.

Open a ready-for-review PR, not a draft, unless the user asks for a draft. If `gh pr create` fails
because the GraphQL rate limit is used up, open it through REST with
`gh api repos/<owner>/<repo>/pulls -f title=... -f head=... -f base=... -F body=@<file>`. If the user also asked
to babysit it, continue with the `babysit-pr` skill.

Do not post a follow-up PR comment unless it serves the user's request. When a
comment is needed, use the `leaving-pr-comments` skill.
