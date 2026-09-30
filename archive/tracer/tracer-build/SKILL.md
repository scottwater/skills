---
name: tracer-build
description: Implement a concrete request with a quick plan, minimal delegation, and Convince Me evidence; finish with a review recommendation.
disable-model-invocation: true
---

# Build

Quick plan → implement here → prove the stated goals.

## 1. Quick plan

Inspect the request, relevant code, branch, and working tree. Assume the current workspace is suitable; preserve unrelated changes. On `main` or `master`, call out the branch and continue. Branch or worktree changes need a separate request.

State the goal, intended changes, and checks in a few chat bullets, then proceed. Ask only about ambiguity that materially changes the goal or scope. Keep the plan in the conversation; workflow files and plan approval are unnecessary.

## 2. Implement

Make the smallest change that meets the stated goals, using existing repository patterns. Work in the current agent context. Use a subagent only when necessary to unblock the task or meet an explicit requirement; state why and give it one bounded task. File count or potential speedup alone is insufficient.

Use focused checks while developing and add regression coverage where it fits. Broaden verification when required by repository policy or the change's impact.

## 3. Convince me

Read and execute Convince Me's [completion evidence protocol](../../../skills/convince-me/SKILL.md) in the current context against the original request and final changes. Every stated goal needs fresh evidence and a verdict: proven, disproven, or unverified.

If proof exposes an in-scope defect, return to implementation, fix it, then rerun affected proof. If progress needs unavailable access, an environment, or a scope decision, report the blocker and affected goals. Never label disproven or unverified goals complete.

## Close-out

Report what changed, the goal/evidence/verdict results, and any remaining limits. Leave changes in the current workspace; commits and delivery actions follow separate user instructions.

End with **Review warranted: yes/no — reason.** Base this on concrete risk in the final diff: security or data handling, cross-cutting behavior, difficult logic, or evidence gaps. For yes, name the review focus. Recommend the review without launching it.
