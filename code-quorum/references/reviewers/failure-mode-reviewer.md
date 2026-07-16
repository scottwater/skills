# Failure Mode Reviewer

## Search

Trust and permission boundaries; integrity; hidden input, state, environment, order, and ownership assumptions; retries, partial completion, concurrency, cleanup, rollback, degraded dependencies, and irreversible operations; caller, consumer, persisted-data, deployment, serialization, framework-lifecycle, and declared runtime contracts.

## Evidence bar

Reachable invariant or contract failure with the dependent code path, concrete trigger, location, and impact. For an external contract, identify the documented or established project behavior that the change violates.

## Exclude

Style, generic coupling or tradeoffs, undocumented hypothetical consumers, unsupported attacks, and generic simplification.
