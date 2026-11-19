---
name: implement
description: Hand a task to a T3 worker thread that implements and commits it, Opus 5.5 on high by default. Use when asked to implement work in a worker thread, or when another skill asks for an implement thread.
---

# Implement

Hand one task to a **worker**: a top-level T3 thread that implements it, runs the project's checks, and commits. You brief the worker, wait, answer its questions, and report. The worker writes every line of code.

## Pick the model

The worker runs Opus 5.5 at `high` reasoning effort. Use the model and effort the user or calling skill names instead.

Call `orchestrator_capabilities` and resolve the worker to an exact `providerInstanceId`, model `id`, and the reasoning-effort option the catalog lists for it. Prefer the provider's native driver (`claudeAgent` for Claude models, `codex` for OpenAI models). When the model or effort is unavailable, tell the user what is missing and ask how to proceed. Never substitute a model.

## Resolve the checkout

Use the checkout the calling skill names. Otherwise use the current branch and worktree, and when that is the default branch, create a branch named for the task first. When the checkout has uncommitted changes, ask the user whether to commit, stash, or keep them before the worker starts.

Done when you have the checkout's absolute path and branch, and the worker's resolved model and effort.

## Launch the worker

Call `t3_thread_launch` with the resolved model and effort, a title naming the task, and a `workspaceStrategy` that points at the checkout: `existing_worktree` with its path and branch for a worktree, or `root` for the project's main checkout. When the user asked for a separate worktree, use `worktree` with the branch as `baseRef`. The `message` carries the whole brief, since the thread starts with no history:

```text
You are the worker for one task.

Repository: <absolute path>
Branch: <branch>
Task: <the prompt, or "ToVo issue <ID>: read its context with the tovo skill">

Implement the task and run the project's checks. Commit your work on this branch with atomic, descriptive commits. Do not push or open a pull request. For a ToVo issue, comment on friction as you go and leave the issue's status to whoever launched you; they also run the code review.

When done, reply with a summary of the change, the commit SHAs, and the checks you ran with their results.
```

Retain the `threadId` and wait with `t3_thread_wait`, reading each reply with `t3_thread_read`. When the worker asks a question, answer it from the request and the task's context, or ask the user when only they can decide.

Done when the worker has replied with its commits and its checks pass, or the user has decided how to handle a failure.

## Send follow-up work

Review findings, disproven proof claims, and other fixes go back to the same worker. When its thread is settled, unsettle it first with `t3_thread_organize` (`action: "unsettle"`). Send the items with `t3_thread_send`, each with its location, failure scenario, and suggested fix, and ask the worker to fix and commit them. Wait for its reply as above, then confirm each fix against the code.

## Settle and report

Settle the worker's thread with `t3_thread_organize` (`action: "settle"`) when no more work will go to it: right after your report when you run this skill on its own, or when the calling skill says so.

Report the worker's thread linked as `[title](t3-thread://v1/<threadId>)`, its model and effort, its commits, and its checks with their results.
