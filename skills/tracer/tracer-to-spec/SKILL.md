---
name: tracer-to-spec
description: Turn a settled interview or cleared Wayfinder map into a spec and publish it — no new interview, just synthesis of decisions already made.
disable-model-invocation: true
---

This skill produces a spec (you may know this document as a PRD) from one of two settled inputs:

- the current conversation after `/tracer-interview-me`, normally in the same context window; or
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

Sketch the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better — the ideal number is one.

Present the inferred seams for confirmation without reopening settled product decisions. If the confirmation exposes a new decision, return it to the originating interview or Wayfinder map instead of inventing an answer inside the spec.

### 3. Write and publish

Write the spec using the template below, then publish it (see above). When the input was a Wayfinder map, include its linked decisions without copying tracker-only bookkeeping into the prose.

Afterwards, the flow continues with `/tracer-to-tickets` (multi-session builds) or straight to `/tracer-implement` (single-session work).

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly. (The precise, path-and-code level lives in `/tracer-implement`'s ephemeral task plan, which dies with the branch.)

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
