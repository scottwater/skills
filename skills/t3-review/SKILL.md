---
name: t3-review
description: Review code inside a T3 Code thread by delegating to a cross-family reviewer, then verifying and fixing its findings. Use when asked to review code, a diff, branch, commit, or PR and the t3-code MCP tools are available.
---

# T3 Review

A **cross-family** review: the reviewer comes from a different model family than you, so it brings different blind spots. The reviewer is report-only. It returns findings, and you verify each one and make every edit.

When the user asks for a Quorum review, read and follow `~/.agents/skills/code-quorum/SKILL.md` instead.

## Resolve scope

Use the scope the user named. Otherwise take the first that exists: pending changes against `HEAD` (staged, unstaged, and relevant untracked files), the current branch from its merge-base with the default branch, the linked pull request, or the latest commit. Record any requirements source: the issue, PR description, spec, or the task from this conversation.

Classify the change as **simple** or **complex**. Simple means a small, local change with one obvious intent. Complex means multiple subsystems, concurrency, security, data migrations, public interfaces, or a diff large enough that you would want a second pass on it yourself. When unsure, choose complex.

Done when you can state the exact diff, range, or files; the requirements source or that there is none; and simple or complex.

## Pick the reviewer

Pick by your own model family:

| You are | Reviewer |
| --- | --- |
| Claude (Fable, Opus, Sonnet, Haiku) | Sol 6.1 if simple, Astra 6 if complex |
| OpenAI (Astra 6, Sol 6.1) | Opus 5.5; Fable 5.1 only when the user asks for it |
| Any other model | Sol 6.1 |

Call `orchestrator_capabilities` and resolve the reviewer's label to an exact `providerInstanceId` and model `id` from the live catalog. Prefer the provider's native driver (`codex` for OpenAI models, `claudeAgent` for Claude models) over a proxy such as Pi, and pick only an instance with `canRunChildTask: true`. If the reviewer is unavailable, tell the user which model is missing and ask them how to proceed. Never fall back to a same-family reviewer.

## Launch the review

Call `delegate_task` with:

- `target`: the resolved `providerInstanceId` and `model`
- `role`: `"review"`
- `runtimeMode`: `"inherit"` and `interactionMode`: `"inherit"`, so the reviewer runs with exactly your permissions and sandbox. Never request a broader mode.
- `mode`: `"async"`
- `title`: `Review: <short scope>`
- `clientRequestId`: unique to this round and reused on retries of it
- `task`: the review brief below

The child starts with no conversation history, so the brief carries everything:

```text
You are a report-only code reviewer. Do not edit files, apply patches, commit, or run mutating commands. Use read-only inspection and non-mutating commands only.

Repository: <absolute path>
Scope: <exact diff command, range, PR, or file list>
Intent: <what the change is supposed to do, in one or two sentences>
Requirements: <source and key acceptance criteria, or "none recorded">

Review for correctness bugs, regressions, missed edge cases, error handling, security, and requirement gaps. Read surrounding code to confirm each claim before reporting it.

Return findings ranked most severe first. For each finding give:
- Severity: Critical, High, Medium, or Low
- Location: path:line
- Problem: one sentence
- Failure scenario: concrete input or state, and the wrong result
- Fix: one sentence

Finish with anything you could not verify. If you find nothing, say so.
```

Retain the returned `taskId`, then end your turn. The child's completion wakes this thread; read the result with `task_status` only if it is needed mid-turn.

## Verify and fix

For every Critical, High, or Medium finding, read the code yourself and decide whether it is real. Confirm it from the source, a test, or a non-mutating reproduction, not from the reviewer's wording.

Implement each verified finding unless the user said otherwise. Low findings are optional: fix them when the fix is cheap and clearly right, and list the rest.

When the fixes are large or you dispute a finding and want a second opinion, run another round: call `delegate_task` again with a new `clientRequestId`, and include the original brief, the prior findings, what you changed, and the unresolved objections. Never continue a review with `t3_thread_send` on the child's `childThreadId`.

Done when every Critical, High, and Medium finding is fixed or rejected with a reason.

## Report

Tell the user:

- The reviewer model and the scope reviewed
- The findings you fixed, each with its `path:line`
- The findings you rejected, each with the reason
- Low findings left unfixed
- Any checks you ran after fixing, with their results
