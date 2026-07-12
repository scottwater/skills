---
name: code-quorum
description: Review code changes through independent reviewer lenses, verify material claims, and return one prioritized read-only report. Use when the user asks for a code quorum; requests a quick, default, full, or custom multi-perspective review; names a quorum reviewer; or asks to review pending changes, a branch, commit, pull request, diff, or file set.
---

# Code Quorum

## Resolve scope

Resolve explicit scope first. Otherwise resolve, in order, pending changes against `HEAD` including staged changes, unstaged tracked changes, and relevant untracked files; a branch from its merge-base; an associated pull request; a recent commit; or named task artifacts. Never infer a whole-repository review. Flag unusually large inferred ranges.

Complete this step when the exact diff, range, or files can be stated.

## Select reviewers

Honor explicit reviewer names before named sets before the default set. Apply the user's focus, additions, and exclusions. Accept `simple` and `lightweight` as aliases for `quick`.

```yaml
quick:
  - general-reviewer
  - silent-failure-hunter
default:
  - adversarial-reviewer
  - general-reviewer
  - silent-failure-hunter
  - skeptical-engineer
full:
  - adversarial-reviewer
  - general-reviewer
  - simplification-reviewer
  - silent-failure-hunter
  - skeptical-engineer
```

Load only the selected files from `references/reviewers/`. Complete this step when the selection has one interpretation.

## Construct task packets

Give every reviewer the same scope, source, changed files, focus, exclusions, project rules, read-only flag, and finding contract. Add one distinct reviewer rubric. Include no prior conclusions.

Complete this step when every packet is bounded and equivalent except for its rubric.

## Run the quorum

Prefer isolated concurrent workers, then sequential delegated workers, then separated in-context passes. Record weak isolation. Continue after one reviewer fails and disclose the missing coverage.

Record each reviewer result separately before synthesis. `source_reviewers` may include only reviewers that independently returned a materially equivalent claim. Reviewer selection alone is not agreement or attribution evidence.

Complete this step when each reviewer returns findings, `no_findings`, or a recorded failure.

## Normalize candidates

Normalize every candidate to `finding-v1`:

```yaml
title: Concrete failure or concern
location: { file: path/to/file, lines: 10-18 }
category: correctness
severity: critical | high | medium | low
confidence: 0.0-1.0
claim: What is wrong
trigger: Conditions that expose it
impact: Resulting behavior or risk
evidence: [Relevant code-path evidence]
recommendation: Direction for addressing it
source_reviewers: [reviewer-name]
```

Require every field. Complete this step when every candidate conforms or has a rejection reason.

## Synthesize

Merge candidates by root cause. Remove style-only, speculative, pre-existing, and out-of-scope claims. Resolve disagreement from source evidence.

Complete this step when each candidate is merged, retained, rejected, or unresolved.

## Verify

Trace every potential blocker through source, safeguards, and tests. Reproduce when proportionate. Assign `verified`, `partially-verified`, `unverified`, or `rejected` and record the method and evidence.

Complete this step when each potential blocker has a status, method, and evidence.

## Prioritize and report

Assign severity, verification, confidence, and a disposition: `block`, `address`, `investigate`, or `consider`. Permit `block` only for verified material findings. Use P0-P3 aliases only when requested.

State scope, reviewer coverage and isolation, prioritized findings, open investigations, and a terse recommendation. Separate verified defects, unresolved risks, and optional improvements.

Complete this step when every reported item has severity, verification, confidence, and disposition, and the report contains all required sections.
