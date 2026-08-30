---
name: blast-radius
description: Analyze and prove the external breakage risks of a proposed change.
disable-model-invocation: true
---

# Blast radius

Find the breakage a diff can cause beyond the files it touches. The result is useful only when its key safety claims are supported by code, an executable check, or a clearly named evidence gap.

Use `how` to trace runtime behavior and `why` to recover historical constraints when those branches matter.

## Proof ladder

Take each safety-critical claim as far down this ladder as the repository and available tools allow:

1. **Assertion.** A plausible statement with no evidence.
2. **Source.** A concrete `file:line`, pinned dependency source, schema, or protocol definition.
3. **Trace.** A step-by-step path showing whether the failure can reach an affected boundary.
4. **Executable check.** A script or test that calls the production path and fails when the claim is false.
5. **Runtime reproduction.** The behavior reproduced in the running system.

Treat levels 1 and 2 as leads. Mark a safety-critical claim unproven when it cannot reach level 4, and explain what prevented stronger proof.

## Workflow

### 1. Define the change boundary

Read the diff and identify every added, changed, and deleted symbol or behavior. Include implicit changes such as timing, ordering, defaults, serialization, and error handling. Recover related commits or rationale when the diff lacks the decision context.

**Complete when:** every changed behavior has an explicit before-and-after statement.

### 2. Find the load-bearing safety facts

Identify the one or two facts that make the change safe. Examples include an idempotency guarantee, a caller invariant, a compatibility promise, or a lifecycle ordering constraint. Phrase each fact so an executable check could prove it false.

**Complete when:** disproving any listed fact would reveal a concrete failure path.

### 3. Trace beyond symbol search

Follow direct callers and the boundaries a symbol search misses:

- pinned dependency behavior and local patches;
- task queues, callbacks, teardown, and lifecycle ordering;
- APIs, schemas, databases, files, and wire formats;
- other languages or services consuming the same data;
- flags, configuration, caches, and downstream jobs.

Search for both current and previous names, values, and formats. Record searches that return no matches when the absence is relevant evidence.

**Complete when:** each changed behavior has been traced to its external consumers or to a verified boundary that contains it.

### 4. Evaluate risks

For each candidate risk, state:

- the failure mechanism;
- the affected caller or boundary with a citation;
- likelihood and impact, with evidence;
- the cheapest check that would confirm or clear it.

Separate confirmed risks from cleared candidates. Omit speculative risks that have no reachable failure path.

**Complete when:** every retained risk has a cited path from the change to an observable failure.

### 5. Prove the load-bearing facts

Prefer a focused script or test that imports and runs the same code the product uses. Run it and capture the command, result, and relevant output. Use a runtime reproduction when it is cheap and materially stronger.

For a wide change, divide the review by independent dependency area and reconcile the results. Use parallel reviewers only when the runtime supports them; the method must not depend on a particular agent or model.

**Complete when:** every load-bearing fact has a proof-ladder level and the strongest practical evidence available.

## Output

### What changed

Describe the behavioral difference, including non-obvious timing, format, or lifecycle effects.

### Load-bearing safety facts

For each fact, give its proof-ladder level, evidence, and status: `proven` or `unproven`.

### Confirmed risks

List only reachable failures. Include location, likelihood, impact, and the check or mitigation.

### Cleared candidates

Name plausible risks that the investigation ruled out and cite the evidence that cleared them.

### Before merge

Give the smallest test or reproduction that protects the real boundary. Include any script created during the investigation.

**Complete when:** a reviewer can reproduce the proof, distinguish confirmed risk from uncertainty, and see every remaining gap.
