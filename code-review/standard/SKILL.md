---
name: standard
description: Coordinate a routine multi-lens code review across skeptical design review, general correctness review, test coverage, and silent-failure auditing.
---

# Code Review: Standard

Coordinate a routine code review for a requested scope such as the current diff, a pull request, a branch comparison, a file list, or the last N commits.

Use this when the user asks for a normal code review and does not need the deeper comments or type-design lenses.

## Lenses

Run or simulate these specialist skills:

- `code-review/skeptic`: hidden assumptions, design risks, over-engineering, maintainability, and regressions.
- `code-review/general`: guideline compliance, correctness, functional bugs, security concerns, and high-confidence implementation issues.
- `code-review/tests`: meaningful missing tests, weak assertions, brittle tests, and untested failure modes.
- `code-review/failures`: swallowed errors, weak fallbacks, silent failures, observability gaps, and poor error reporting.
- `code-review/synthesize`: final deduplication and prioritization.

## Scope Resolution

Resolve the review scope once before running lenses.

If the user provides an explicit scope, use it directly. Examples: a file path, PR range, branch comparison, commit range, staged changes, pending changes, or last N commits.

If no scope is provided:

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
Resolved code review context:

Scope: `<range, files, working tree, or repository>`
Scope source: `<user request or default>`
Review mode: review-only unless explicitly running `code-review/simplify` separately.

Changed files:
<git diff --name-status output or file list>

Diff stat:
<git diff --stat output when available>

Commit summary:
<git log --oneline output when applicable>

Your focus:
<skeptic | general | tests | failures>

Report only high-confidence, actionable findings. Preserve file paths, line references when available, concrete reasoning, and suggested fixes. Do not modify files.
```

## Coordinator Workflow

1. Resolve the scope and state it briefly.
2. Inspect changed files, diff stat, and commit summary when available.
3. Run the four specialist lenses in parallel when the harness supports subagents or separate skill runs.
4. If separate agents are unavailable, run each lens sequentially using the specialist checklists.
5. Synthesize with `code-review/synthesize` logic.
6. Deduplicate overlap, remove speculative findings, and preserve the highest severity.
7. Return one concise report.

## Output Format

```md
# Standard Code Review

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

## Test and Validation Gaps
- <only meaningful gaps from the tests lens>

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
