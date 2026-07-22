---
name: worktrees
description: Set up an isolated workspace for feature work — detect existing isolation, prefer the harness's native worktree tool, fall back to git worktree. Use before running /implement on tickets in parallel.
disable-model-invocation: true
---

# Worktrees

Ensure work happens in an isolated workspace. This is what makes parallel `/implement` runs safe: each ticket gets its own checkout, branch, and `.tracer/implement/` workspace, and every task commits, so nothing rides on a shared dirty tree.

**Order of preference: detect existing isolation → native harness tool → git worktree fallback. Never fight the harness.**

## 0. Detect existing isolation

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
git rev-parse --show-superproject-working-tree   # non-empty ⇒ submodule, not a worktree
```

If `GIT_DIR != GIT_COMMON` and you're not in a submodule, you are **already** in a linked worktree — do not create another; skip to setup (step 2).

Otherwise, if the user hasn't already declared a worktree preference, ask once: "Set up an isolated worktree? It protects your current branch." If declined, work in place.

## 1. Create the workspace

**1a. Native tool first.** If the harness provides one — `EnterWorktree`, a `/worktree` command, a `--worktree` flag — use it and skip to step 2. Using `git worktree add` when a native tool exists creates phantom state the harness can't manage; this is the #1 mistake.

**1b. Git fallback** (only when no native tool exists):

- Directory priority: explicit user preference → existing `.worktrees/` → existing `worktrees/` → default `.worktrees/` at the project root.
- **Verify it's ignored** before creating anything: `git check-ignore -q .worktrees` — if not, add to `.gitignore` and commit. Otherwise worktree contents end up tracked.
- Create: `git worktree add "$LOCATION/$BRANCH_NAME" -b "$BRANCH_NAME" && cd "$LOCATION/$BRANCH_NAME"`
- If creation fails on a sandbox/permission error, say so and work in place instead.

## 2. Project setup

Install dependencies per project type (`npm install`, `cargo build`, `pip install -r requirements.txt` / `poetry install`, `go mod download` — whatever the repo uses).

## 3. Verify a clean baseline

Run the test suite. If it fails, report the failures and ask before proceeding — otherwise you can't tell new bugs from pre-existing ones. If it passes, report:

```
Worktree ready at <path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature>
```

When the work is done, `/finish-branch` handles merge/PR and worktree cleanup — don't remove worktrees ad hoc.
