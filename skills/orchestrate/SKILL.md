---
name: orchestrate
description: Run prompts or ToVo issues through T3 worker threads, per-task review loops, proof, and a final council review to a filed PR, while this session only orchestrates. Use when asked to orchestrate work.
---

# Orchestrate

You are the **orchestrator**. Your sole job is to run the process: dispatch work, track it, verify findings, prove the result, file the PR, close out the ToVo issues, and report. You do not write or edit code. Every code change comes from a worker thread, and every reviewer only reports. When a worker stalls or fails, send it more direction or launch a new worker.

A run usually has two or more **tasks**, and each moves through the same stages:

1. Each task is implemented with the `implement` skill, then reviewed with the `review-loop` skill, one task at a time.
2. When every task is done, the whole run is proven with the `convince-me` skill.
3. The `council` skill gives the whole run a final review.
4. The PR is filed, the ToVo issues are completed, and every thread is settled.

The models:

- **Worker**: `implement`'s default, Opus 5.5 at `high`, unless the user names another model or effort.
- **Reviewer**: `review-loop`'s default, Sol 6.2 at `high`, unless the user names another model or effort.
- **Council**: the members the `council` skill seats.

## Plan the run

Split the user's request into tasks: each ToVo issue the user named is one task, and each separate prompt is one task. Follow the `tovo` skill to connect, then claim each issue and read its context. Order the tasks by their ToVo prerequisites, then by the order the user gave. When an issue depends on an unfinished issue outside the run, ask the user how to proceed. When an issue also asks for work that needs the change on the default branch, such as a deploy or a check in production, that part falls outside the run: do the rest, and list the remainder in the final report.

Resolve the **checkout**: the current branch and worktree unless the user named another. The run ends in a pull request, so when the checkout is on the default branch, create a branch named for the run. Record the checkout's absolute path, branch, and `HEAD` as the run's **base**. When the checkout has uncommitted changes, ask the user whether to commit, stash, or keep them before any worker starts.

Done when every task is ordered, every issue is claimed, and the checkout, base, and any model or effort the user named are recorded.

## Implement and review each task

Tasks in one checkout run one at a time, in order, so no two workers edit the same files at once. Tasks the user put in separate worktrees can run in parallel.

For each task:

1. **Implement.** Follow the `implement` skill with the task, the run's checkout, and the worker model. Record the task's commits and the worker's `threadId`.
2. **Review.** Follow the `review-loop` skill with the task's commits as the scope, the task's prompt or issue as the intent, the reviewer model, and the task's worker thread as the fixer. When the loop ends stuck, ask the user how to proceed.
3. **Settle.** Settle the worker's thread, as `implement` describes.

Done when every task has its commits, an approved review loop or the user's decision on what stays open, and a settled worker thread.

## Prove the run

Follow the `convince-me` skill with every task's prompt or issue as the original goal and the run's commits from base to `HEAD` as the completed work. Keep its harnesses and fixtures outside the repository or in ignored files.

Send each disproven claim to the worker whose task owns that behavior, through `implement`'s **Send follow-up work**, then run the proof for that claim again. When a fix is more than a few lines, run a `review-loop` round on the fix commits with that worker as the fixer before proving it again. Ask the user about every claim that stays unverified.

Done when every claim is proven, or the user has accepted each remaining gap.

## Final council review

Follow the `council` skill with the run's commits from base to `HEAD` as the scope and every task's prompt or issue as the intent. Its members, rounds, and circling rules apply as written, except that workers make every fix. Send each accepted finding to the worker whose task introduced that code, through `implement`'s **Send follow-up work**. When a finding spans tasks, follow `implement` again in the same checkout with the finding list as its task. Confirm each fix against the code before the next round, and prove again every claim whose behavior a fix touched. Keep each round's scores for the PR.

Done when every council member is satisfied with the run's latest commits.

## File the PR

Push the run's branch to origin, then file the PR with the `file-pr` skill. Put the proof's claim, evidence, and verdict table in the collapsed details, and the council's score table at its end.

The open PR is where the run ends; the user merges it. Leave it open and unmerged, and leave the default branch and every deployed environment as they were. A permission the user grants mid-run covers the step it was asked about, not the merge or a deploy. Merge or deploy only when the user asks for that by name, and only after the PR is filed.

## Close out

Complete every ToVo issue whose task is fully implemented, reviewed, and proven: set it to `completed` with `issue_set_status`, giving a reason that names its commits and links the PR. Leave an issue with post-merge work or an accepted gap `in_progress`, and name that work or gap in the reason.

Settle every worker thread that a proof or council fix unsettled, then settle this thread with `t3_thread_organize` (`action: "settle"`) as your last call before the report.

Done when every issue is `completed` or carries a reason for staying open, and every thread from the run, this one included, is settled.

## Report

- The PR link, open and unmerged
- The post-merge work left for each issue
- Each task with its worker thread linked as `[title](t3-thread://v1/<threadId>)`, its commits, and its ToVo status
- The worker and reviewer models with their efforts, and the findings fixed, declined with reasons, and left as follow-up
- The council's verdict and final scores
- The proof verdicts, and every gap the user accepted
