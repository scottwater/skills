---
name: code-quorum
description: Run independent code-review agents and synthesize verified findings.
disable-model-invocation: true
---

# Code Quorum

## Read-only boundary

The entire workflow is inspection and reporting only. The delegator, every reviewer, the synthesizer, and the verifier must not edit reviewed files, generate or apply patches, commit changes, or begin remediation. Recommendations describe directions for a later, separately authorized workflow. Reproduce claims only with non-mutating commands or in disposable isolation that cannot alter the reviewed workspace.

## Confirm agents

Confirm an independent-worker mechanism before inspecting the review scope.

Probe Solo identity first when the runtime exposes a Solo identity or status tool. In Pi, use `solo_status`; with direct Solo MCP access, use `whoami`. A response that identifies the current process as Solo-managed and reports agent spawning available selects Solo for the quorum. Use the runtime's native subagent abstraction only when the Solo probe is unavailable, cannot identify the current process, reports MCP or spawning unavailable, or fails. Tool visibility alone is not proof that the current process is Solo-managed.

When Solo is selected, create every reviewer as a Solo-managed agent. Otherwise create every reviewer through the native subagent abstraction. Do not mix mechanisms within one quorum merely to increase concurrency.

Require a fresh isolated context for every reviewer. Concurrency is optional; independence is required. Do not continue to scope resolution when neither Solo nor another subagent abstraction can create fresh workers. Return an execution-unavailable response that names the missing capability.

Complete this step when one available mechanism can create a fresh agent for each selected reviewer.

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

Create one fresh agent for each selected reviewer through the mechanism confirmed above. Run agents concurrently when capacity allows. Schedule them sequentially when capacity is constrained, while preserving a fresh isolated context for each reviewer. Give each agent only the shared task packet and its selected rubric. Do not run reviewer passes in the delegator context.

When the native subagent runtime supports acceptance gates, disable them for each reviewer task (for example, `acceptance: "none"`). Never request `reviewed` acceptance for a quorum reviewer: these workers already are the independent reviewers, and requiring another automatic reviewer can falsely mark valid reviewer output as failed.

Report reviewer completion as results arrive when the runtime supports progress updates. Wait until every selected reviewer has returned, failed, timed out, or could not start before synthesis.

Record each returned result separately. Judge usability from the returned report, not only the wrapper's lifecycle label. If a worker exits successfully and returns a complete report but the wrapper reports only an unavailable optional acceptance reviewer, retain the report and disclose the wrapper anomaly under coverage limitations. `source_reviewers` may include only reviewers that independently returned a materially equivalent claim. Selection alone is not agreement or attribution evidence.

Synthesize every usable returned result. List each missing reviewer and its failure reason under coverage limitations. Treat no missing reviewer as agreement, disagreement, or `no_findings`. Return an execution failure instead of a review when no reviewer returns a usable result.

Complete this step when every selected reviewer has a usable result or a recorded failure reason, and at least one usable result exists.

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

Assign severity using these canonical meanings:

- `critical`: catastrophic, actively dangerous, or irreversible impact.
- `high`: material, ship-blocking defect.
- `medium`: important defect that is normally nonblocking.
- `low`: minor risk or worthwhile improvement.

Keep severity, verification, confidence, and disposition separate. Dispositions mean:

- `block`: only a verified material finding.
- `address`: a verified or partially verified actionable nonblocker.
- `investigate`: an important unverified claim; state the missing evidence.
- `consider`: low-risk simplification or maintainability advice.

Omit rejected findings unless the user requests provenance. Use P0-P3 aliases only when requested.

State scope, reviewer coverage and isolation, prioritized findings, open investigations, and a terse recommendation. Separate verified defects, unresolved risks, and optional improvements.

Complete this step when every reported item has severity, verification, confidence, and disposition, and the report contains all required sections.
