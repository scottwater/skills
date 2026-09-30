---
name: tracer-worktrees
description: Set up an isolated workspace when feature work starts on main/master — reuse any existing feature branch or isolation, prefer the harness's native worktree tool, and fall back to git worktree.
disable-model-invocation: true
---

# Worktrees

Choose the feature workspace without disrupting one the user already chose. A named non-default branch stays in its current checkout; work that starts on `main` or `master` gets a feature branch and, when accepted, an isolated checkout. Separate checkouts make parallel `/tracer-implement` runs safe.

**Order of preference: keep a named feature branch → reuse existing isolation → native harness tool → git worktree fallback. Never fight the harness.**

## 0. Gate on the current branch

```bash
CURRENT_BRANCH=$(git symbolic-ref --quiet --short HEAD || true)
```

- If `CURRENT_BRANCH` is named and is neither `main` nor `master`, the repository already has a clear feature workspace. **Stop this skill and work in the current checkout.** A linked worktree is not required; the branch is the signal that the workspace has already been chosen.
- If `CURRENT_BRANCH` is empty, HEAD is detached or branch detection failed. Report the state and ask whether to keep working there or create a branch; do not create a worktree by assumption.
- Only when `CURRENT_BRANCH` is exactly `main` or `master` should this skill consider creating a worktree. Continue below.

## 1. Detect existing isolation

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
git rev-parse --show-superproject-working-tree   # non-empty ⇒ submodule, not a worktree
```

If `GIT_DIR != GIT_COMMON` and you're not in a submodule, you are **already** in a linked worktree. Run `git switch -c "$BRANCH_NAME"` to create the feature branch in this checkout, then skip to setup (step 3); do not nest another worktree.

Otherwise, if the user hasn't already declared a worktree preference, ask once: "Set up an isolated worktree? It protects your current branch." If declined, run `git switch -c "$BRANCH_NAME"` and work in the current checkout.

## 2. Create the workspace

**2a. Native tool first.** If the harness provides one — `EnterWorktree`, a `/worktree` command, a `--worktree` flag — use it and skip to step 3. Using `git worktree add` when a native tool exists creates phantom state the harness can't manage; this is the #1 mistake.

**2b. Git fallback** (only when no native tool exists):

- Directory priority: explicit user preference → existing `.worktrees/` → existing `worktrees/` → default `.worktrees/` at the project root.
- **Verify it's ignored** before creating anything: `git check-ignore -q .worktrees` — if not, add to `.gitignore` and commit. Otherwise worktree contents end up tracked.
- Create: `git worktree add "$LOCATION/$BRANCH_NAME" -b "$BRANCH_NAME" && cd "$LOCATION/$BRANCH_NAME"`
- If creation fails on a sandbox/permission error, say so, run `git switch -c "$BRANCH_NAME"`, and work in the current checkout instead.

## 3. Project setup

Install dependencies per project type (`npm install`, `cargo build`, `pip install -r requirements.txt` / `poetry install`, `go mod download` — whatever the repo uses).

## 4. Verify a clean baseline

Run the test suite. If it fails, report the failures and ask before proceeding — otherwise you can't tell new bugs from pre-existing ones. If it passes, report:

```
Workspace ready at <path> (<branch>)
Tests passing (<N> tests, 0 failures)
Ready to implement <feature>
```

When the work is done, `/tracer-finish-branch` handles merge/PR and worktree cleanup — don't remove worktrees ad hoc.
