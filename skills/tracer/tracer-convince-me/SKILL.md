---
name: tracer-convince-me
description: Build the strongest honest, end-to-end case that completed work satisfies its original goal.
disable-model-invocation: true
---

# Convince Me

Prove that the completed work satisfies its original goal. Produce fresh, observable evidence—not confidence, code inspection alone, or results remembered from earlier in the session.

## 1. Establish the case

Read the original request, available spec or ticket, acceptance criteria, relevant changes, and existing tests. Translate every expectation into an observable claim.

Inspect the available context before asking questions. If an unresolved ambiguity would materially change what must be proven, ask all clarification questions together.

## 2. Design the proof

For each claim, choose the strongest practical verification boundary. Prefer the real user path and production-like integration over isolated implementation details.

Cover the successful path and any material failure, boundary, or regression paths. Existing tests count as evidence only when run now. Supplement them with a focused test, script, fixture, manual interaction, screenshot, or disposable harness when they do not prove the claim.

One-off verification may be rough, but it must be safe and scoped. Get approval before destructive actions, external side effects, production access, or spending money.

## 3. Execute

Run every proving command or interaction now and inspect its result. Record enough detail to connect each result to the claim it proves.

A failure or inconclusive result is evidence that the work is not yet proven. Do not weaken the proof or substitute explanation for execution.

Keep a verification artifact when it provides durable regression value. Otherwise remove temporary files and restore modified state.

## 4. Report

Present:

- each expectation;
- the evidence gathered for it;
- whether it was proven, disproven, or remains unverified;
- any limits or environmental differences that weaken the case.

The verification is complete only when every expectation is backed by fresh evidence or explicitly named as unverified. Never claim more than the evidence establishes.
