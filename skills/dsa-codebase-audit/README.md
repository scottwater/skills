# DSA Codebase Audit

A user-invoked, read-only skill that inventories an entire codebase, assigns non-overlapping subsystem reviews to bounded agent lanes, verifies each finding, and returns a dependency-aware list of material simplifications in data structures, state representation, control flow, algorithms, and ownership.

The skill does not edit code or begin remediation. Every subsystem must end with a verified recommendation or an explicit skip, and the final report includes an auditable coverage ledger.

## Invocation

Invoke the skill explicitly:

```text
/dsa-codebase-audit
```

Fresh subagents are used when the runtime supports them. Without subagents, the coordinator reviews subsystems sequentially and discloses the coverage limitation.

## Credit

Adapted from the **DSA Codebase Audit** prompt shared by [Aaron Francis](https://x.com/aarondfrancis/status/2088285625946370352?s=20).
