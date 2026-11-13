---
name: quick-send
description: Take a change straight to the default branch unattended, proving and reviewing it, then pushing without a PR. Use when the user says quick send or wants work pushed directly to main.
---

# Quick Send

Do the same unattended work as `full-send`, but push the change straight to
origin's default branch instead of filing a PR. The user is not watching this
thread, so your updates and final message go unread until long after you stop.

Read [full-send](../full-send/SKILL.md) and follow its Testing permission,
Proof, and Asking the user sections. Its PR steps (file, babysit, merge gate,
merge) do not apply. The rules below take precedence.

The user grants you permission to:

- Push this task's commits to origin's default branch as a fast-forward.
- Use the test methods that Proof needs, without asking first.

## Steps

1. **Find the default branch.** Fetch origin and read its default branch
   (`git symbolic-ref refs/remotes/origin/HEAD`, or
   `gh repo view --json defaultBranchRef`). It may be `main`, `master`, or
   something else.
2. **Finish the change.** Complete the goal from the user's request with the
   smallest change that works. Work on the local default branch, or on a branch
   when the checkout holds unrelated work, you are in a worktree, or a branch
   keeps things cleaner.
3. **Prove it.** Get proof for every change you made.
4. **Get feedback.** Use the `sol-loop` skill to verify changes. Re-prove any
   behavior a fix touches.
5. **Commit** with the `committing-with-guidelines` skill. Commit only this
   task's changes; leave unrelated uncommitted work where you found it.
6. **Rebase** onto the latest `origin/<default>`. If upstream moved, re-run the
   repo's CI checks on the rebased commit, and re-prove behavior a conflict fix
   touched.
7. **Push** when the push gate passes: `git push origin HEAD:<default>`. If the
   push is rejected as non-fast-forward, return to step 6 and push again.
8. **Check CI.** If the repo runs CI on pushes to the default branch, wait for
   the run on your commit (`gh run watch <id> --exit-status`). When your change
   breaks it, fix forward with a new commit through steps 3 to 7.
9. **Report** in your final message: the default branch, each pushed commit
   SHA, your proof, the CI result, and each decision you made for the user.

Stay active from step 1 to step 9. Ending your turn while CI is pending stops
the work, because nobody will prompt you again.

## Push gate

Push only when all of these are true on the rebased commit:

- Your proof covers every change in `git diff origin/<default>..HEAD`.
- `sol-loop` ended in agreement.
- The repo's CI checks pass locally.
- The commits hold only this task's changes.
- The push is a fast-forward of `origin/<default>`.

Pushed history is shared: fix it forward with new commits. Never force-push the
default branch, rewrite commits already on origin, or bypass branch protection.
If origin rejects direct pushes (protected branch, required PR), ask the user,
and offer `full-send` as the recommended option.

## Asking the user

Follow full-send's rules with these swaps: give the default branch and your
local commits in place of a PR link, treat "the push gate cannot pass" as the
merge gate case, and when no answer comes, leave the commits unpushed and start
your final message with the question.
