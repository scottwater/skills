---
name: quick-stop
description: Do quick-send's unattended work, but stop with commits ready to push to the default branch. Use when the user says quick stop or wants work committed locally without pushing.
---

# Quick Stop

Do the same work as `quick-send`, but stop with the commits ready for the user
to push to origin's default branch. Never push them.

Read [quick-send](../quick-send/SKILL.md) and follow its workflow, proof rules,
review, and push gate. Invoking this skill authorizes that work, and
full-send's testing permission with it. Its push permission does not apply.
The overrides below take precedence.

## No pushing

You may commit, rebase, and fix conflicts locally. Never push to the default
branch or any other branch, open a PR, or delegate those actions.

## Stop at the gate

Run quick-send through step 6, then use its push gate as the readiness check.
Replace its push, CI, and report steps with a handoff. Fetch origin right
before the handoff and rebase again if the default branch moved, so the push is
a fast-forward.

Leave the commits on the branch you worked on. Name the exact command that
pushes them: `git push origin HEAD:<default>` from that branch.

- **Ready to push:** the push gate passes.
- **Blocked:** explain what prevents readiness, what you tried, and what is
  needed. Follow quick-send's rules for asking the user.

Report the default branch, the branch holding the commits, each commit SHA, the
push command, your proof, the reviewer outcome, and remaining risks. State that
nothing was pushed.
