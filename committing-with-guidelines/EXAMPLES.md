# Commit examples

Use these examples when a change is hard to split, a message needs more context, or unpublished history needs cleanup. The workflow and rules live in [SKILL.md](SKILL.md).

## Product outcome versus implementation inventory

### Product-focused

```text
Add team filtering to the progress dashboard

- Supports combinations of teams, goals, and date ranges
- Persists filter state in the URL so a view can be shared
```

The message records capabilities and a user-facing decision.

### Implementation-focused

```text
Add team filtering

- Add TeamFilterForm
- Update the controller
- Add form specs
- Update the dashboard partial
```

This body repeats the diff and hides the reason for the change.

## Self-explanatory change

```text
Update password reset email copy
```

A body would add no useful context.

## Architectural decision

```text
Add an event bus for cross-domain notifications

- Separates notification delivery from domain actions
- Allows audit logging to subscribe without changing business logic
```

The body explains why the abstraction exists and what boundary it creates.

## Trade-off

```text
Add indexes for team goal dashboard queries

- Reduces the measured dashboard query from 2.5 seconds to 300 milliseconds
- Accepts slower writes because this table serves a read-heavy workflow
```

Use measurements and name the accepted cost.

## Breaking change

```text
Remove deprecated v1 API endpoints

- All known clients now use v2
- Removes an authentication path the team would otherwise need to patch
```

The body records why removal is safe and why it matters.

## Splitting a mixed worktree

Suppose one worktree contains a schema change, domain behavior, controller integration, UI, and their tests.

### 1. Assign hunks to outcomes

A reviewable sequence could be:

1. `Add schema for team goal filtering`
2. `Add filtering behavior to team goals`
3. `Add team filtering to the progress dashboard`

The model test belongs with filtering behavior. The request test and view belong with the dashboard outcome. A migration belongs with the first commit only when later commits can safely build on it.

### 2. Stage and verify each unit

```bash
git add db/migrate/20260712000000_add_filters_to_team_goals.rb
git diff --cached
git commit -m "Add schema for team goal filtering"

git add app/models/team_goal.rb spec/models/team_goal_spec.rb
git diff --cached
git commit -m "Add filtering behavior to team goals"

git add app/controllers/team_goals_controller.rb \
  app/views/team_goals/_filters.html.haml \
  spec/requests/team_goals_spec.rb
git diff --cached
git commit -m "Add team filtering to the progress dashboard"
```

Use `git add -p` when one file contains hunks for different outcomes. Re-check `git diff --cached` after every staging command.

## Separating unrelated changes

If a feature and an unrelated bug fix share the worktree:

```bash
git add -p
git diff --cached
git commit -m "Add saved filters to the progress dashboard"

git add path/to/unrelated_fix.rb path/to/unrelated_fix_spec.rb
git diff --cached
git commit -m "Update invoice rounding for partial refunds"
```

The second subject describes the corrected behavior rather than saying only “Fix bug.”

## Cleaning unpublished history

History editing is appropriate only when the commits have not become shared history or the user has approved rewriting them.

Inspect the range first:

```bash
git log --oneline -n 6
git rebase -i HEAD~6
```

Useful rebase actions:

- `reword`: improve a message without changing its tree;
- `edit`: amend the commit's content;
- `fixup`: fold a follow-up into the previous commit and discard its message;
- `squash`: combine commits while editing their messages;
- `drop`: remove a commit.

Arrange foundational changes before the behavior that depends on them. Fold typo-only or correction commits into their logical parent. After the rebase, run the relevant checks and inspect the rewritten log.

If the branch was already pushed and rewriting is approved:

```bash
git push --force-with-lease
```

Create a backup branch before a complex rewrite:

```bash
git branch backup-before-rebase
```
