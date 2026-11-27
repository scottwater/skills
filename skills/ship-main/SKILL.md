---
name: ship-main
description: Take a change unattended straight to the default branch, proving, reviewing, committing, pushing fast-forward, and watching CI. Pass hold to stop locally before pushing. Use when the user says ship-main or wants work pushed directly to main.
---

# Ship Main

The user invoked this because they are not watching this thread and want the
work shipped directly to origin's default branch without a PR. Your updates and
final message go unread until long after you stop.

## Mode and permissions

- **Default (push and watch CI):** push this task's commits to
  `origin/<default>` as a fast-forward and watch CI on the pushed commit.
- **With `hold` (or `local`):** stop after step 6 with commits rebased and
  ready locally. Never push to the default branch or any other branch, open a
  PR, or delegate those actions. Hand back the exact push command.

Invoking this skill grants permission to:

- Use the test methods Proof needs without asking first.
- Push this task's commits to `origin/<default>` as a fast-forward (unless
  `hold` was requested).

## Testing permission

Invoking this skill is the permission. If a project file or other instruction
says to ask before a test method, or to leave testing to the user, this request
replaces that rule for this task.

That includes ask-first rules for computer use, browser automation, simulators
and devices, running the app or a dev server, screenshots, and visual checks.
Use the method that gives direct proof and list it in the report.

Rules about how to test still apply: follow the repo's commands, fixtures, and
checks. This removes only the ask-first step. It does not cover actions under
"Asking the user" (such as production changes or data deletion), nor does it
bypass a harness or system approval prompt.

## Steps

1. **Find the default branch.** Fetch origin and read its default branch
   (`git symbolic-ref refs/remotes/origin/HEAD`, or
   `gh repo view --json defaultBranchRef`). It may be `main`, `master`, or
   something else.
2. **Finish the change.** Complete the goal from the user's request with the
   smallest change that works. Work on the local default branch, or on a branch
   when the checkout holds unrelated work, you are in a worktree, or a branch
   keeps things cleaner.
3. **Try it and prove it.** Exercise what you built on the real path and capture
   observed proof for every change you made. See "Proof".
4. **Get feedback.** Review the change with `review-loop` (or `council` if the
   user explicitly names it), passing your observed proof. Re-prove any behavior
   a fix touches.
5. **Commit** with the `committing-with-guidelines` skill. Commit only this
   task's changes; leave unrelated uncommitted work where you found it.
6. **Rebase** onto the latest `origin/<default>`. If upstream moved, re-run the
   repo's CI checks on the rebased commit, and re-prove any behavior a conflict
   fix touched.
7. **Push or hold.**
   - **With `hold`:** fetch origin once more and rebase if `origin/<default>`
     moved, confirm the push gate passes, leave commits on the local branch,
     and skip step 8.
   - **Default:** push when the push gate passes with
     `git push origin HEAD:<default>`. If rejected as non-fast-forward, return
     to step 6 and push again.
8. **Check CI.** If the repo runs CI on pushes to the default branch, wait for
   the run on your commit (`gh run watch <id> --exit-status`). When your change
   breaks it, fix forward with a new commit through steps 3 to 7.
9. **Report** in your final message: the default branch, each commit SHA,
   whether commits were pushed or held (with `git push origin HEAD:<default>`
   and the holding branch when held), your proof, reviewer outcome, CI result,
   decisions you made, and remaining risks.

Stay active until the final report. Ending your turn while CI is pending stops
the work because nobody will prompt you again.

## Proof

Proof is evidence you observed yourself in this session: running what you built,
command output, a reproduction, a screenshot. Use the most direct proof the
change allows:

- Reproduce the original failure, apply the fix, then watch the same
  reproduction pass.
- Run the checks that the repo's CI runs (typecheck, lint, tests).
- Add one focused test that fails without the fix when the behavior has none
  and the repo has a test setup.
- For UI, CLI, API, and runtime behavior, run the real code path and inspect
  the result. Green mocked tests alone do not prove the user experience works.

When you cannot find a way to prove a change, you do not have full confidence.
Ask the user.

## Push gate

Ready to push only when all of these are true on the rebased commit:

- Observed proof covers every change in `git diff origin/<default>..HEAD`.
- Review (`review-loop`, or `council` if requested) ended in agreement.
- The repo's CI checks pass locally.
- The commits hold only this task's changes.
- The push is a fast-forward of `origin/<default>`.

Pushed history is shared: fix it forward with new commits. Never force-push the
default branch, rewrite commits already on origin, or bypass branch protection.
If origin rejects direct pushes (protected branch, required PR), ask the user
and offer `ship-pr` as the recommended option.

## Asking the user

A question in a normal message goes unseen and makes the thread look done. Use
the harness's question tool (`AskUserQuestion`, `request_user_input`, or
equivalent) with full context: the default branch, your local commits, the
blocker, and options with your recommendation first.

Ask only when you cannot continue alone:

- You cannot prove the change.
- Review cannot finish (`review-loop` ends stuck, or `council` cannot be seated
  or circles).
- The push gate cannot pass and you cannot fix it yourself.
- Branch protection rejects direct pushes.
- The next step is outside the grant above: deleting data, touching production,
  changing things outside the repo, or force-pushing.
- The goal is ambiguous in a way that changes the result.

Decide everything else with sensible defaults and list those decisions in the
report. If no question tool is available or returns no answer, leave commits
unpushed and start your final message with the question.
