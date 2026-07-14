---
name: code-quorum
description: Run independent code-review agents and synthesize verified findings.
disable-model-invocation: true
---

## Read-only boundary

The whole workflow inspects and reports. No agent in it edits reviewed files, generates or applies patches, commits, or begins remediation; recommendations point at a later, separately authorized workflow. Reproduce claims only with non-mutating commands or in disposable isolation that cannot alter the reviewed workspace.

## Confirm agents

Confirm the worker mechanism before touching the review scope.

Probe Solo first when a Solo identity tool is visible: `whoami` (direct MCP) or `solo_status` (Pi). Select Solo only when the probe confirms this process is Solo-managed with agent spawning available — tool visibility alone is not proof. In every other case (no probe, probe fails, spawning unavailable), use the runtime's native subagent abstraction. One mechanism runs the whole quorum.

When Solo is selected, resolve the current process's configured agent tool before dispatch. Under Pi, use the process id from `solo_status` with `solo_process status`; match its process name and launch command to an enabled agent tool reported by `solo_status`, preferring an exact tool-name match. Pass that tool explicitly as `agentTool` on every `solo_task`; never rely on `solo_task`'s generic default, because it does not inherit the current process's model or arguments. Do not pass separate `model` or `thinking` overrides when the selected agent tool already defines them. With direct MCP, use the equivalent agent-tool identity returned by `whoami`. If the current process cannot be mapped unambiguously to an enabled tool, stop before reviewing scope and ask the user which enabled agent tool to use.

Every reviewer is a blind agent: fresh context, no prior conclusions, no reviewer passes in the delegator context. Concurrency is optional; blindness is required. When no mechanism can create blind agents, stop and return an execution-unavailable response naming the missing capability.

Complete this step when one mechanism can create a blind agent per reviewer and, for Solo, the exact agent tool is resolved.

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

## Run the quorum

Give every reviewer an identical task packet — scope, source, changed files, focus, exclusions, project rules, read-only flag, finding contract — plus its one distinct rubric. Create one blind agent per reviewer through the confirmed mechanism, concurrently when capacity allows, sequentially otherwise. For Solo, pass the resolved `agentTool` explicitly on every dispatch so all reviewers use the parent process's configured agent tool.

Where the runtime offers acceptance gates, disable them (`acceptance: "none"`): the reviewers are the acceptance layer, and a gate can falsely fail valid reviewer output.

Wait for every reviewer to return, fail, or time out. Judge each result by its returned report, not the wrapper's lifecycle label — retain a complete report even when the wrapper flags an anomaly, and disclose the anomaly under coverage limitations. A missing reviewer contributes only a coverage limitation — never agreement or `no_findings`. Return an execution failure when no reviewer returns a usable result.

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

Require every field. List in `source_reviewers` only reviewers whose own report contains a materially equivalent claim — selection alone is not attribution evidence. Complete this step when every candidate conforms or has a rejection reason.

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

Render the report exactly in this template — each section once, in this order, omitting Consider and Open questions when empty:

```markdown
## Verdict

<One sentence: **Merge**, **Merge after fixes**, or **Do not merge** — with the deciding reason.>

Scope: <range/PR · files · +/− lines> · Reviewers: <usable/selected> (<mechanism>)

## Do next

- [ ] `path/to/file:lines` — <imperative action> (finding 1)

## Findings

### 1. <Concrete failure in plain words> — <severity> · <disposition>

- **Where:** `path/to/file:lines` — <function or block name>
- **What:** <claim and trigger, at most two sentences>
- **Impact:** <resulting behavior or risk, one sentence>
- **Fix:** <one imperative sentence>
- **Verification:** <status> · confidence <n> · <source reviewers>

## Consider

- `path/to/file:lines` — <one-line suggestion> (<source reviewers>)

## Open questions

- <Unverified claim> — <the evidence that would settle it>

## Coverage

<Isolation, reviewer failures, and limitations in two or three lines.>
```

Every Do next item and every finding carries an exact `file:lines` location — when a reviewer supplied only a file or block name, resolve the line numbers from source before reporting. Do next lists every `block` and `address` item ordered by severity, one imperative line each; `consider` items live only in Consider. Findings are numbered in Do next order so the checklist and the detail cross-reference by number.

Complete this step when the report matches the template: every reported item has severity, verification, confidence, and disposition; every finding and Do next item has a `file:lines` location and a one-sentence fix; and each Do next entry names its finding.
