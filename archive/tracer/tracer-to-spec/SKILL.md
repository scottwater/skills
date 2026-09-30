---
name: tracer-to-spec
description: "Turn settled decisions into a concise spec with observable acceptance and material safety limits."
disable-model-invocation: true
---

This skill produces a spec (you may know this document as a PRD) from one of two settled inputs:

- the current conversation after `/interview-me`, normally in the same context window; or
- a cleared `/tracer-wayfinder` map passed as a URL, issue number, or local path.

Do NOT restart the interview. The decisions have already been made; synthesize them without silently adding new ones.

**Where it publishes:** if `docs/agents/issue-tracker.md` configures a tracker (set up via `/tracer-setup`), publish there without `ready-for-agent`; that label is reserved for executable tickets from `/tracer-to-tickets`. Otherwise write the spec to `.tracer/<feature-slug>/spec.md`.

## Process

### 1. Gather the settled input

For a normal interview, work from the current conversation.

For a Wayfinder map, hydrate its distributed detail before writing:

1. Read the map's Destination, Notes, Decisions so far, Not yet specified, and Out of scope.
2. Use the configured tracker's Wayfinding operations to query all children. Stop and return to `/tracer-wayfinder` if any child is open, claimed, or in flight, if Not yet specified is not empty, or if any resolved child is absent from both Decisions so far and Out of scope.
3. Fetch the full body and resolution comment or Answer section for every resolved ticket indexed under Decisions so far. Follow linked research notes, prototype verdicts, ADRs, and other decision assets as needed. The map's one-line gists are an index, not the source of truth.
4. Preserve the map's explicit scope boundary. Read a linked out-of-scope ticket when its one-line explanation is not enough to state the exclusion accurately.

### 2. Explore and choose test seams

Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

Prefer existing high-level test seams and focused checks for observable acceptance and material failure paths. Reuse prior exploration. A test seam is not a requirement to build a new fixture framework, enumerate every configuration, or run every platform and full suite.

State the proposed verification briefly. Ask for confirmation only when it introduces a new seam with substantial machinery, expensive/external verification, or an unsettled acceptance decision. Separate required evidence from optional broader checks. Return new product or safety decisions to the user or originating Wayfinder map rather than inventing them here.

### 3. Write and publish

Write the shortest spec that preserves the settled behavior and material limits using the template below, then publish it (see above). Omit empty optional sections and combine overlapping criteria. When the input was a Wayfinder map, include its linked decisions without copying tracker-only bookkeeping into the prose.

Afterwards, the flow continues with `/tracer-to-tickets` (multi-session builds) or straight to `/tracer-implement` (single-session work).

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Acceptance Criteria

A concise numbered list of observable outcomes, including material failure behavior and data/security invariants. Each criterion must follow from a settled user requirement, not a hypothetical consumer or planner preference. Group related variants; more criteria are not inherently a better spec.

Use a user story only when the actor's motivation clarifies a distinct requirement. Ordinary implementation steps do not need separate stories.

## Implementation Decisions

Only implementation decisions explicitly settled with the user or already required by the repository. Distinguish those constraints from optional suggestions, which the implementer may simplify. Do not turn safe reruns into concurrency/crash-recovery guarantees or a clear permission error into a custom authorization evaluator without an explicit decision. This optional section can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Keep durable decisions at the behavior/interface level. Exact affected paths and verification commands belong in `/tracer-implement`'s short ephemeral plan; implementation code belongs in the implementation.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo.

## Testing Decisions

Name existing seams and focused evidence for the acceptance criteria. Cover material failures without requiring every speculative variant. Record required real-environment checks only when agreed or mandated by repository policy; label broader platform runs and full-suite checks as optional unless impact justifies them.

Reference useful prior tests rather than prescribing a new harness or duplicating test code.

## Out of Scope

State the exclusions and limits that keep this small, including supported environments and any relevant concurrency or recovery boundaries. Preserve required safeguards; clarify a genuine safety trade-off rather than silently omitting it.

## Further Notes

Any further notes about the feature.

</spec-template>
