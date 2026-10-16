---
name: t3-review-quorum
description: Run a Code Quorum review inside a T3 Code thread, with reviewers delegated to Astra and Fable.
disable-model-invocation: true
---

# T3 Review Quorum

A Code Quorum review whose reviewers run as T3 delegated tasks on two model families. Read and follow `~/.agents/skills/code-quorum/SKILL.md` for the whole workflow: its read-only boundary, scope, reviewer selection, finding contract, verification, and report template all apply unchanged. This skill replaces only the worker mechanism and the reviewer models.

## Confirm agents

This step replaces Code Quorum's **Confirm agents** step.

The worker mechanism is T3's `delegate_task`. Each delegated task is a blind agent: it starts with no conversation history and sees only its task packet.

The reviewer models are **Astra 6** and **Fable 5.1**. When the user names other models, use those instead. Call `orchestrator_capabilities` and resolve each model to an exact `providerInstanceId` and model `id` from the live catalog. Prefer the provider's native driver (`codex` for OpenAI models, `claudeAgent` for Claude models) over a proxy such as Pi, and pick only an instance with `canRunChildTask: true`. When a model is unavailable, tell the user which one is missing and ask how to proceed.

Complete this step when every reviewer model resolves to a `providerInstanceId` and model `id` that can run a child task.

## Run the quorum

This step replaces how Code Quorum's **Run the quorum** step creates agents; its task packet, waiting rules, and failure rules still apply.

Run every selected rubric once on each reviewer model, so each rubric gets a reviewer from both families. For each pair, call `delegate_task` with:

- `target`: the resolved `providerInstanceId` and `model`
- `role`: `"review"`
- `runtimeMode`: `"inherit"` and `interactionMode`: `"inherit"`
- `mode`: `"async"`
- `title`: `Quorum: <rubric> (<model>)`
- `clientRequestId`: unique to this rubric and model, reused on retries of it
- `task`: the Code Quorum task packet with the rubric's full text, and the report-only rule stated first

Retain every returned `taskId` with its rubric and model, then end your turn. Each child's completion wakes this thread; use `task_status` to read a result or to check a task that has not reported. A task whose status is `failed`, `cancelled`, or `interrupted`, or whose summary holds no report, is a missing reviewer.

Record each reviewer as `<rubric> (<model>)` in `source_reviewers`. Two models reporting the same claim under one rubric count as corroboration only under Code Quorum's independent-evidence rule. In the report's Scope line, give the mechanism as `T3 delegate_task, <model> + <model>`.

Complete this step when every rubric-and-model pair has a usable report or a recorded failure reason, and at least one usable report exists.
