# Branch-finishing procedure

Finish a verified branch: check evidence → detect checkout → present options → execute the user's choice → clean up. Return failures to the user; this procedure does not authorize review or repair.

## 1. Verify entry evidence

Run the project's full test suite now and read the output. Reuse a caller's suite output only after verifying that it comes from this same close-out for the **same unchanged HEAD and tracked tree**, with no intervening implementation changes. Otherwise, run the suite.

If tests fail or required acceptance remains blocked/unverified: show the failures or gaps, preserve the branch, and stop. No merge or PR. An absent test suite is not a green result: report the limitation and ask the user for an explicit finishing decision rather than silently passing this gate.

Carry forward the caller's outcome and non-blocking follow-ups, including the qualification in Complete with follow-ups.

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

Report any follow-ups before these options. Use the caller's outcome as the heading, or “Implementation complete” when no qualified outcome was supplied:

```text
<Complete | Complete with follow-ups | Implementation complete>. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
```

Wait for the user's explicit choice. Detached HEAD: drop option 1; option 2 becomes “Push as new branch and create a PR.”

## 4. Execute the choice

**1 — Merge locally:**

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch> && git pull && git merge <feature-branch>
<test command>   # verify tests on the merged result
```

Only after the merge succeeds and tests pass: clean up the worktree (step 5), then `git branch -d <feature-branch>` — in that order; branch deletion fails while a worktree still references it. A failed merge or check stops here for the user's decision; preserve the workspace and report its actual state rather than beginning another repair loop.

**2 — Push and create PR:** `git push -u origin <feature-branch>`, then create the PR (`gh pr create`). Include non-blocking follow-ups and verification limits. Preserve the worktree for PR feedback. Force-push only on explicit request.

**3 — Keep as-is:** report “Keeping branch <name>. Worktree preserved at <path>.” Touch nothing.

**4 — Discard:** confirm first —

```text
This will permanently delete:
- Branch <name>
- All commits: <list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for the exact word. Then `cd` to the main root, clean up the worktree (step 5), and `git branch -D <feature-branch>`.

## 5. Worktree cleanup (options 1 and 4 only)

Only remove worktrees this workflow created. Confirm ownership from the workflow record; a path under `.worktrees/` or `worktrees/` alone is not proof. For harness-created workspaces, use the harness's workspace-exit tool if available; otherwise leave them in place.

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"    # never run remove from inside the worktree being removed
git worktree remove "$WORKTREE_PATH"
git worktree prune
```
