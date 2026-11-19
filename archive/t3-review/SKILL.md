---
name: t3-review
description: Review code inside a T3 Code thread by delegating to a cross-family reviewer, then verifying and fixing its findings. Use when asked to review code, a diff, branch, commit, or PR and the t3-code MCP tools are available.
---

# T3 Review

A **cross-family** review: the reviewer comes from a different model family than you, so it brings different blind spots. The reviewer is report-only. It returns findings, and you verify each one and make every edit.

## Pick the reviewer

Pick by your own model family:

| You are | Reviewer |
| --- | --- |
| An OpenAI model | Opus 5.5 at `xhigh` reasoning effort, through the rest of this skill |
| Any other model, Claude included | Sol, through the `sol-loop` skill |

When you are not an OpenAI model, invoke `sol-loop` with the scope the user named and follow it in place of the remaining steps here. Sol is the reviewer; `sol-loop` owns the rounds, verification, and fixes. Finish with this skill's **Report**.

When you are an OpenAI model, call `orchestrator_capabilities` and resolve Opus 5.5 to an exact `providerInstanceId` and model `id` from the live catalog. Prefer the native `claudeAgent` driver over a proxy such as Pi, and pick only an instance with `canRunChildTask: true`. Set the effort to `xhigh` with the reasoning-effort option id and value the catalog lists for that model. If Opus 5.5 or `xhigh` is unavailable, tell the user what is missing and ask them how to proceed. Opus 5.5 is the only reviewer model for this path.

## Resolve scope

Use the scope the user named. Otherwise take the first that contains reviewable changes: pending changes against `HEAD` (staged, unstaged, and relevant untracked files), the current branch from its merge-base with the default branch, the linked pull request, or the latest commit. Record any requirements source: the issue, PR description, spec, or the task from this conversation.

Done when you can state the exact diff, range, or files, and the requirements source or that there is none.

## Launch the review

Call `delegate_task` with:

- `target`: the resolved `providerInstanceId`, `model`, and `xhigh` effort option
- `role`: `"review"`
- `runtimeMode`: `"inherit"` and `interactionMode`: `"inherit"`, so the reviewer gets your T3 runtime mode. T3 rejects any broader mode, and each provider enforces the mode with its own sandbox, so the boundary matches in intent rather than mechanism.
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

Start only from a usable report. When the task status is `failed`, `cancelled`, or `interrupted`, or the summary holds no review, tell the user the review did not complete and offer to retry under a new `clientRequestId`. Never treat a missing report as a clean review.

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
