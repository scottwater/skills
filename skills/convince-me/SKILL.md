---
name: convince-me
description: Build the strongest honest, end-to-end case that completed work satisfies its original goal.
disable-model-invocation: true
---

# Convince Me

Prove that completed work satisfies its original goal. Produce fresh, observable evidence — not confidence, code inspection alone, or results remembered from earlier in the session. This skill proves; it does not repair. Report failures instead of fixing them.

## 1. Establish the case

Read the original request, available spec or ticket, acceptance criteria, relevant changes, and existing tests. Translate every expectation into an observable claim. Keep the agreed environment and safety limits attached to those claims; stronger guarantees are scope proposals, not silently added acceptance criteria.

Inspect the available context before asking questions. Ask all questions whose answers would materially change the proof together, in one message.

**Complete when:** every expectation has an observable claim with agreed limits, and material ambiguities are resolved.

## 2. Design the proof

For each claim, choose the strongest practical verification boundary. Prefer the real user path and production-like integration over isolated implementation details.

Cover the successful path and any material failure, boundary, or regression paths. Existing tests count as evidence only when run now. Supplement them with a focused test, script, fixture, manual interaction, screenshot, or disposable harness when they do not prove the claim. One executed check may support several claims.

One-off verification may be rough, but it must be safe and scoped. Get approval before destructive actions, external side effects, production access, or spending money. When approval or the required environment is unavailable, mark the affected claim unverified.

**Complete when:** each claim has a verification method covering its material paths, or a named reason verification is unavailable.

## 3. Execute

Run every proving command or interaction now and inspect its result. Record enough detail to connect each result to the claim it proves, including the checked revision and relevant environment.

Record failures as disproven and inconclusive results as unverified. Do not weaken the proof or substitute explanation for execution.

Use disposable fixtures or ignored files for verification. When an artifact would have durable regression value, add it to the repo only with the user's approval; otherwise report it as a follow-up. Remove temporary files and restore modified state without disturbing user work.

**Complete when:** every planned check has an observed result or a recorded blocker, and temporary state is restored.

## 4. Report

Present:

- each expectation;
- the evidence gathered for it;
- whether it was proven, disproven, or remains unverified;
- any limits or environmental differences that weaken the case.

Use the smallest presentation that makes the proof traceable. Default to a claim/evidence/verdict table. Add one focused call tree, state flow, component or file tree, diff, screenshot, or diagram only when it clarifies sequence, ownership, change, or observed behavior. Place it beside the claim it supports and omit unrelated detail.

Explanatory visuals organize evidence; they are not evidence themselves. Only artifacts captured from an executed verification — such as a screenshot of the tested user path — can support a verdict.

**Complete when:** every expectation has fresh evidence and a verdict, or is explicitly unverified. If a blocker stopped execution, name all unchecked claims. Never claim more than the evidence establishes: disproven and unverified requirements remain blockers.
