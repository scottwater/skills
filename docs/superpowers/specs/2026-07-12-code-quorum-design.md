# Code Quorum Design

## Purpose

`code-quorum` performs a read-only review of code changes through multiple independent review lenses. It collects candidate findings, verifies material claims, removes duplicates and weak speculation, then returns a prioritized advisory report.

The skill must work in Codex, Claude, Pi, and runtimes without delegated workers. Platform-specific adapters may translate the execution protocol, but the canonical skill owns all review behavior.

## Invocation

Make `code-quorum` model-invoked so natural requests can reach it. Support these branches:

- `code-quorum`: use the default reviewer set.
- `quick code-quorum`: use the lightweight set. Accept "simple" and "lightweight" as natural-language aliases.
- `full code-quorum`: use every applicable reviewer.
- Named reviewers: use only the requested reviewers.
- Set plus overrides: apply requested additions, exclusions, focus areas, and confidence thresholds to the selected set.

Selection precedence:

1. Explicit reviewers
2. Named set
3. Default set

User focus and exclusions modify the resulting selection.

## Read-only boundary

Reviewers inspect and report. The delegator, reviewers, verifier, and synthesizer do not edit files, generate patches, commit changes, or begin remediation. Recommendations describe a direction for a later, separately authorized workflow.

## Information hierarchy

Use this canonical package:

```text
code-quorum/
├── SKILL.md
└── references/
    └── reviewers/
        ├── adversarial-reviewer.md
        ├── general-reviewer.md
        ├── simplification-reviewer.md
        ├── silent-failure-hunter.md
        └── skeptical-engineer.md
```

Keep the ordered process and material required by every branch in `SKILL.md`:

- Scope resolution
- Reviewer-set membership and selection
- Task packet contract
- Execution fallbacks
- Finding contract
- Verification rules
- Severity and disposition rules
- Synthesis and final response contract

Disclose only reviewer rubrics. Load a reviewer file when selection includes that reviewer. Each rule has one authoritative location: reviewer behavior in its file; shared process and contracts in `SKILL.md`.

Keep platform adapters outside the canonical package or generate them from it. Adapters contain invocation mechanics only and do not copy review rules.

## Reviewer sets

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

Keep simplification outside the default set because it usually produces advisory feedback rather than defects.

## Reviewer responsibilities

### Adversarial reviewer

Search for expensive failure modes: trust-boundary violations, data integrity failures, concurrency faults, unsafe rollback, retries, partial completion, and compatibility hazards. Try to disprove that the change is safe to ship. Ground every claim in a reachable scenario.

### General reviewer

Search for concrete correctness bugs, regressions, violated repository rules, and missing tests for changed behavior. This reviewer owns broad integration coverage rather than the specialized concerns below.

### Simplification reviewer

Identify unnecessary complexity, accidental abstractions, confusing control flow, and maintainability hazards in the selected changes. Preserve behavior in every recommendation. Return advice only.

### Silent-failure hunter

Trace swallowed errors, misleading success, unjustified fallbacks, lost diagnostic context, and broken error propagation. Judge handling against the project's intended failure semantics. Do not assume that every handled error requires logging or user feedback.

### Skeptical engineer

Challenge hidden assumptions, coupling, design risks, operational fragility, and likely future regressions. Report high-confidence concerns with concrete consequences.

## Scope resolution

Resolve scope before selecting reviewers. Use this precedence:

1. User-specified PR, branch or revision range, commit, file set, directory, diff, or artifact.
2. Pending changes against `HEAD`: staged changes, unstaged tracked changes, and relevant untracked files.
3. Current branch changes against the merge base with its default or upstream branch.
4. The current branch's associated PR when the runtime can discover it and it does not conflict with a stronger explicit scope.
5. The most recent commit.
6. Files or artifacts named in the surrounding task context.

Outside a Git repository, use artifacts named by the user. If none exist, report that no defensible scope was found.

State the resolved scope in the final response. Exclude recognizable generated, vendored, and irrelevant untracked files. Inspect surrounding code when needed for understanding, but keep findings attributable to the selected changes unless surrounding code causes a direct regression.

Do not infer an entire-repository review. Flag unusually large or ambiguous inferred ranges.

Scope resolution completes when the skill can state the exact diff, revision range, or files under review.

## Task packet

Give every reviewer the same bounded packet without other reviewers' conclusions:

```yaml
objective: Review the selected changes
scope:
  kind: pending | pull-request | revision-range | commit | files | artifact
  value: runtime-specific scope description
focus: []
exclusions: []
project_instructions: []
reviewer: reviewer-name
read_only: true
output_contract: finding-v1
```

Task construction completes when each selected reviewer has the same scope, focus, exclusions, project instructions, and finding contract plus its own rubric.

## Execution

Use the strongest isolation the runtime supplies:

1. Run isolated reviewers independently and concurrently when available.
2. Run delegated reviewers sequentially when concurrency is unavailable.
3. Run separated passes in the current context when delegation is unavailable. Do not expose earlier conclusions to later passes when the runtime permits that separation.

Disclose when reviewers did not receive isolated contexts. The delegator resolves scope, selects reviewers, constructs task packets, collects results, and starts synthesis. It contains no reviewer-specific expertise.

The quorum completes when every selected reviewer has returned findings, returned an explicit no-findings result, or has a recorded failure.

## Finding contract

Each candidate finding contains:

```yaml
title: Concrete failure or concern
location:
  file: path/to/file
  lines: 10-18
category: correctness
severity: critical | high | medium | low
confidence: 0.0-1.0
claim: What is wrong
trigger: Conditions that expose it
impact: Resulting behavior or risk
evidence:
  - Relevant code-path evidence
recommendation: Direction for addressing it
source_reviewers:
  - reviewer-name
```

A reviewer may return `no_findings` instead. Normalize unambiguous format differences. Reject candidates that lack a concrete claim, affected location, plausible trigger, impact, or supporting evidence.

Normalization completes when every candidate satisfies the contract or has a recorded rejection reason.

## Synthesis

Merge candidates that share one root cause. Preserve distinct consequences when they change severity or remediation. Remove style-only, speculative, pre-existing, and out-of-scope claims. Treat reviewer agreement as corroboration rather than proof.

Inspect source when reviewers disagree. Record unresolved disagreement when available evidence cannot decide it.

Synthesis completes when every candidate has been merged, retained, rejected, or marked as unresolved.

## Verification

Independently verify every candidate that may receive a blocking disposition. Trace the claimed execution path, inspect existing safeguards and tests, and reproduce behavior when proportionate and possible.

Assign one verification status:

- `verified`: available evidence establishes the claim.
- `partially-verified`: evidence supports part of the claim or impact.
- `unverified`: verification needs unavailable runtime or contextual evidence.
- `rejected`: evidence disproves or fails to support the claim.

Only a verified material finding may receive `block`. Keep important unverified claims under `investigate` and state the missing evidence. Omit rejected findings unless the user requests audit provenance.

Verification completes when every potential blocker has a status, method, and supporting or contradictory evidence.

## Prioritization

Keep severity, verification, confidence, and disposition separate:

```yaml
severity: critical | high | medium | low
verification: verified | partially-verified | unverified | rejected
confidence: 0.0-1.0
disposition: block | address | investigate | consider
```

Use these severity meanings:

- `critical`: catastrophic, actively dangerous, or irreversible impact.
- `high`: material defect that should block shipping.
- `medium`: important defect that does not normally block shipping.
- `low`: minor risk or worthwhile improvement.

Support `P0` through `P3` as presentation aliases when requested:

- P0 = critical
- P1 = high
- P2 = medium
- P3 = low

Prioritization completes when every surviving finding has all four fields.

## Final response

Return:

1. Resolved scope
2. Reviewers run and any coverage failures
3. Prioritized findings ordered by severity, verification, impact, and confidence
4. Open investigations
5. Terse recommendation

For each finding, include its location, trigger, impact, evidence, verification status, source reviewers, and remediation direction. Return a concise no-findings result when the quorum finds no defensible issues.

The report completes when readers can distinguish verified defects, unresolved risks, and optional improvements without consulting raw reviewer output.

## Failure handling

- Continue after one reviewer fails and disclose the missing coverage.
- Normalize malformed reviewer output only when the intended fields are unambiguous.
- Downgrade findings when verification cannot reach the required evidence.
- Merge excessive duplicates by root cause.
- Use the next execution level when the runtime lacks a preferred delegation feature.
- Report no findings without inventing suggestions.

## Validation

Validate the implementation with these cases:

- Natural-language invocation for quick, default, full, and explicit selections
- Staged, unstaged, untracked, clean-branch, PR, recent-commit, and non-Git scopes
- Malformed, duplicate, speculative, conflicting, and no-findings responses
- Verified, partially verified, unverified, and rejected claims
- Isolated-worker and no-delegation execution
- A read-only check that detects workspace mutations
- Forward tests using raw code changes without leaked expected findings

The skill passes when each run follows the same scope, selection, contract, verification, and prioritization process even when reviewers reach different conclusions.
