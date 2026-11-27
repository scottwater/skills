---
name: ship-pr
description: Take a change unattended through proof, review, PR filing, and babysitting until merge-ready. Pass merge to merge once the gate passes. Use when the user says ship-pr or wants work finished into a PR without supervision.
---

# Ship PR

The user invoked this because they are not watching this thread and want the
work taken end-to-end into a merge-ready pull request. Your updates and final
message go unread until long after you stop.

## Mode and permissions

- **Default (open and ready):** stop with the PR open, merge-ready, and
  unmerged. Never merge, enable auto-merge, enter a merge queue, push to the
  default branch, bypass branch protection, or delegate those actions. Disable
  any existing auto-merge and remove the PR from any merge queue before work
  begins and again before each push; report those changes. If you cannot prevent
  automatic merging, report the blocker before proceeding.
- **With `merge`:** when the user passes `merge` (or explicitly asks to merge),
  you are authorized to merge the PR once the merge gate passes.

Invoking this skill grants permission to:

- Force-push the PR's own branch with `--force-with-lease` after a rebase.
- Use the test methods Proof needs without asking first.
- Merge the PR only when `merge` was requested.

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

1. **Finish the change.** Complete the goal from the user's request with the
   smallest change that works. Fix the case that happened, not every case that
   could. If you are on the default branch, create a branch first.
2. **Try it and prove it.** Exercise what you built on the real path and capture
   observed proof for every change you made. See "Proof".
3. **Get feedback.** If the user named `review-loop` or `council`, use that
   skill. Otherwise, choose based on scope and risk:
   - Use `council` for new features, public API, schema, or contract changes,
     multi-subsystem edits, or anything touching security, auth, permissions,
     data integrity, or concurrency.
   - Use `review-loop` for smaller, self-contained changes (localized bug fixes,
     UI, copy, or config tweaks, minor refactors, tests). Escalate to `council`
     if the diff grows wider or riskier than expected.
   Pass your observed proof into the review, and re-prove any behavior a fix
   touches.
4. **File the PR** with the `file-pr` skill. Rebase onto the latest default
   branch first. Add one short line to the description saying how you proved the
   change, and the council's score table when `council` reviewed it.
5. **Babysit the PR** with the `babysit-pr` skill. Fix CI failures and real
   human review findings. Prove each fix before pushing it.
6. **Finish at the merge gate.**
   - **Default (no `merge`):** use the merge gate as the readiness check. Fetch
     the target branch and check the live PR's head, base, checks, reviews, and
     mergeability. Confirm it is open, not a draft, and not set to auto-merge
     (if someone else merged it, report that). Call `unwatch_pull_request` in
     T3 Code before handing off with a verdict: **Ready to merge**, **Waiting
     for required approval**, or **Blocked**.
   - **With `merge`:** merge when the merge gate passes, using the repo's
     allowed merge method and branch protection (never `--admin`). If the repo
     uses a merge queue or auto-merge, stay active until GitHub reports the PR
     as merged.
7. **Report** in your final message: the PR link, final head or merge commit,
   verdict (open and unmerged, or merged), your proof, reviewer outcome,
   decisions you made, and remaining risks.

Stay active from step 1 to step 7. If you end your turn while checks are
pending, the work stops because nobody will prompt you again. Wait with the
watcher from `babysit-pr` (`watch_pull_request` in T3 Code). Always call
`unwatch_pull_request` before stopping unmerged or asking a question.

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
  Attach screenshots to the PR when helpful and uploadable.

When you cannot find a way to prove a change, you do not have full confidence.
Ask the user.

## Merge gate

Full confidence means all of these are true on the latest commit:

- Observed proof and review cover the final diff (re-check behavior changes and
  meaningful conflict fixes).
- Required checks are green.
- Every review comment is fixed or answered with a written reason, and no
  review thread is unresolved.
- No human review still requests changes.
- The branch is up to date with the default branch, and GitHub reports it as
  mergeable.

## Asking the user

A question in a normal message goes unseen and makes the thread look done. Use
the harness's question tool (`AskUserQuestion`, `request_user_input`, or
equivalent) with full context: PR link, blocker, and options with your
recommendation first.

Ask only when you cannot continue alone:

- You cannot prove the change.
- Review cannot finish: the council cannot be seated or circles, or
  `review-loop` ends stuck.
- The merge gate cannot pass and you cannot fix it yourself.
- The next step is outside the grant above: deleting data, touching production,
  changing things outside the repo, closing a PR, or force-pushing another
  branch.
- The goal is ambiguous in a way that changes the result.
- Another PR makes this one obsolete.

Decide everything else with sensible defaults and list those decisions in the
report. If no question tool is available or returns no answer, leave the PR
open and unmerged and start your final message with the question.
