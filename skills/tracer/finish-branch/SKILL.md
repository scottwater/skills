---
name: finish-branch
description: Finish a development branch — verify tests with fresh evidence, then present merge / PR / keep / discard options and execute the choice, cleaning up worktrees safely.
disable-model-invocation: true
---

# Finish Branch

Complete development work: verify tests → detect environment → present options → execute choice → clean up.

## 1. Verify tests — fresh evidence

Run the project's full test suite **now**, and read the output. A green run from earlier in the session is not evidence; "should pass" is not a status.

If tests fail: show the failures and stop. No merge, no PR, until green.

## 2. Detect environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
```

- `GIT_DIR == GIT_COMMON` → normal checkout; no worktree cleanup later.
- `GIT_DIR != GIT_COMMON`, named branch → linked worktree; provenance-based cleanup (step 5).
- `GIT_DIR != GIT_COMMON`, detached HEAD → externally managed workspace; no merge option, no cleanup.

Determine the base branch: `git merge-base HEAD main` (or `master`), or ask.

## 3. Present options

Exactly these, concisely, no added explanation:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
```

(Detached HEAD: drop option 1; option 2 becomes "Push as new branch and create a PR".)

## 4. Execute the choice

**1 — Merge locally:**

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch> && git pull && git merge <feature-branch>
<test command>   # verify tests on the merged result
```

Only after the merge succeeds and tests pass: clean up the worktree (step 5), then `git branch -d <feature-branch>` — in that order; branch deletion fails while a worktree still references it.

**2 — Push and create PR:** `git push -u origin <feature-branch>`, then create the PR (`gh pr create`). Do **not** remove the worktree — it's needed to iterate on PR feedback.

**3 — Keep as-is:** report "Keeping branch <name>. Worktree preserved at <path>." Touch nothing.

**4 — Discard:** confirm first —

```
This will permanently delete:
- Branch <name>
- All commits: <list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for the exact word. Then `cd` to the main root, clean up the worktree (step 5), and `git branch -D <feature-branch>`.

## 5. Worktree cleanup (options 1 and 4 only)

Only remove worktrees this workflow created — paths under `.worktrees/` or `worktrees/`. Harness-created workspaces belong to the harness: if a workspace-exit tool exists, use it; otherwise leave the workspace in place.

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"    # never run remove from inside the worktree being removed
git worktree remove "$WORKTREE_PATH"
git worktree prune
```

## Never

- Proceed with failing tests, or merge without re-verifying tests on the merged result
- Delete work without the typed confirmation
- Force-push without an explicit request
- Remove a worktree before the merge is confirmed, remove one you didn't create, or run `git worktree remove` from inside it
