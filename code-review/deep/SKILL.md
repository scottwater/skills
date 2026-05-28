---
name: deep
description: Coordinate a deep multi-lens code review including standard review, comments and documentation analysis, and type-design analysis.
---

# Code Review: Deep

Coordinate a deeper code review for a requested scope such as a pull request, branch comparison, complex feature, public API change, type-heavy change, or documentation-sensitive change.

Use this when the user asks for a deeper review than `code-review/standard`, or when the changes touch comments, documentation, public APIs, types, domain models, or complex behavior.

## Lenses

Run or simulate everything in `code-review/standard`:

- `code-review/skeptic`
- `code-review/general`
- `code-review/tests`
- `code-review/failures`

Also run:

- `code-review/comments`: comment, docstring, README, API documentation, and inline documentation accuracy.
- `code-review/types`: invariant expression, illegal states, encapsulation, naming, and type-design clarity.

Finish with:

- `code-review/synthesize`: final deduplication and prioritization.

## Scope Resolution

Resolve the review scope once before running lenses.

If the user provides an explicit scope, use it directly. If no scope is provided:

1. Review staged and unstaged changes against `HEAD` when the working tree has changes.
2. Otherwise compare the current branch against `main` using `main...HEAD`.
3. If `main` is unavailable, try `origin/main...HEAD`.
4. If no useful diff is available, review the current checkout at a high level and clearly state that no diff scope was available.

Useful read-only commands:

```sh
git status --short
git diff --name-status HEAD
git diff --stat HEAD
git diff --cached --name-status
git diff --cached --stat
git diff --name-status main...HEAD
git diff --stat main...HEAD
git log --oneline main..HEAD
```

## Shared Context Packet

Pass this packet to each lens when delegating, or keep it in front of you when simulating lenses in one session:

```md
Resolved deep code review context:

Scope: `<range, files, working tree, or repository>`
Scope source: `<user request or default>`
Review mode: review-only.

Changed files:
<git diff --name-status output or file list>

Diff stat:
<git diff --stat output when available>

Commit summary:
<git log --oneline output when applicable>

Your focus:
<skeptic | general | tests | failures | comments | types>

Report only high-confidence, actionable findings. Preserve file paths, line references when available, concrete reasoning, and suggested fixes. Do not modify files.
```

## Coordinator Workflow

1. Resolve the scope and state it briefly.
2. Inspect changed files, diff stat, and commit summary when available.
3. Run the six specialist lenses in parallel when the harness supports subagents or separate skill runs.
4. If separate agents are unavailable, run each lens sequentially using the specialist checklists.
5. Synthesize with `code-review/synthesize` logic.
6. Deduplicate overlap, remove speculative findings, and preserve the highest severity.
7. Separate must-fix issues from medium or low priority improvements.
8. Return one concise report.

## Output Format

```md
# Deep Code Review

Scope: `<resolved scope>`
Date: `<date>`

## Summary
- Overall assessment.
- Highest-risk areas.

## Findings

### Critical: <title>
- Source lenses:
- Files/areas:
- Problem:
- Why it matters:
- Suggested fix:

### High: <title>
- Source lenses:
- Files/areas:
- Problem:
- Why it matters:
- Suggested fix:

### Medium: <title>
- Source lenses:
- Files/areas:
- Problem:
- Why it matters:
- Suggested fix:

## Test and Validation Gaps
- <only meaningful gaps from the tests lens>

## Comment and Documentation Notes
- <only high-value notes from the comments lens>

## Type Design Notes
- <only high-value notes from the types lens>

## Open Questions
- <questions blocking confidence, if any>

## Recommendation
- <merge/block/fix-first recommendation>
```

## Rules

- Do not edit files.
- Do not list every changed file.
- Do not report low-confidence nits.
- Do not broaden scope beyond the user's request.
- Mark incomplete child output as an incomplete-review note instead of inventing findings.
