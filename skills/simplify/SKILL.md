---
name: simplify
description: Refine an implementation by simplifying, deduplicating, reorganizing, and removing low-value tests or unnecessary churn while preserving behavior.
disable-model-invocation: true
---

# Simplify

Refine the requested implementation without changing its observable behavior.

## 1. Establish the boundary

Read the repository guidance and inspect the implementation, its callers, its tests, and the current diff. Use the scope the user supplied. If none was supplied, scope the pass to pending changes in the current worktree; do not turn it into a repository-wide cleanup.

Identify the behavior and public contracts the implementation must preserve. Separate changes that belong to this implementation from unrelated user work. If the intended behavior or ownership boundary is materially ambiguous, ask before editing.

## 2. Find material simplifications

Look for:

- duplicated logic, data, helpers, or tests;
- control flow or state that can be expressed directly;
- unnecessary indirection, wrappers, abstractions, or configuration;
- fragmented code whose ownership becomes clearer when reorganized;
- compatibility paths or defensive branches the scoped implementation does not need;
- comments, formatting changes, renames, and other churn unrelated to the behavior;
- tests that repeat coverage, assert implementation details, or provide no meaningful regression signal.

Prefer deletion and straightforward local code over a new abstraction. Keep an abstraction when it owns a real invariant, reduces repetition across genuine callers, or protects a stable boundary. Do not trade visible complexity for hidden coupling.

Keep tests that prove important behavior, boundaries, failure modes, or regressions. Remove a test only when its signal is already provided elsewhere or the behavior it covered was removed; the remaining suite must still make the preserved contract observable.

## 3. Refine the implementation

Make the smallest coherent edits that materially reduce complexity or churn. Preserve external behavior, public interfaces, data formats, errors, side effects, and supported edge cases unless the user explicitly authorizes a change.

Stay inside the established boundary. Do not rewrite surrounding code merely for consistency, and do not overwrite unrelated work in a dirty worktree.

## 4. Verify preservation

Review the resulting diff for accidental behavior changes and unnecessary edits. Run the narrowest relevant tests, then any broader test, typecheck, lint, or format commands required by the repository. When tests were removed, confirm the retained tests still exercise the behavior that matters.

If verification fails, fix the simplification or revert the unsafe part. Never weaken assertions or delete a failing test merely to make verification pass.

## 5. Report

Summarize:

- what was simplified or removed;
- why behavior is preserved;
- verification run and its result;
- any part left unchanged because simplifying it would increase risk or alter behavior.

The pass is complete when the scoped implementation is materially simpler, the final diff contains no unrelated churn introduced by the pass, and preserved behavior has fresh verification evidence.
