# Architecture critique rubric

Apply only the lenses relevant to the subsystem. Demand evidence from the code for every judgment.

## Abstraction fit

- Does each abstraction represent a real concept or remove repeated complexity?
- Do boundaries separate concerns that change independently?
- Does indirection reduce reader load, or merely move it?
- Is domain behavior isolated from framework and transport wiring where that separation pays off?

A flat design is appropriate for a simple domain. More layers are not an improvement by themselves.

## Data and state

- Do representations match runtime data and access patterns?
- Does code repeatedly reshape data because a boundary owns the wrong form?
- Do types express real invariants or claim certainty the runtime lacks?
- Is state ownership clear, with explicit transitions and lifecycle?

## Boundary discipline

- Are validation and normalization concentrated at entry points?
- Do errors cross boundaries in deliberate, usable forms?
- Are contracts explicit enough to test a component without starting the whole system?
- Do process, persistence, network, and trust boundaries receive the handling they require?

## Evolution

- Which likely next change would touch many unrelated components, and why?
- Which assumptions are embedded in several places?
- Does compatibility code still protect a known consumer?
- Is the subsystem aligned with the repository's current direction?

Judge likely evolution from repository evidence rather than hypothetical scale or features.

## Complexity for value

- Is complexity concentrated around genuine domain constraints?
- Which component, layer, or configuration no longer earns its cost?
- Could one clearer ownership boundary remove repeated coordination?
- Does the design make routine debugging and testing harder than the problem requires?

## Consistency

- Does the subsystem follow established repository patterns for similar problems?
- When it differs, does the domain or runtime explain the difference?
- Would a contributor predict where behavior belongs and how data moves?

Unexplained inconsistency is evidence of maintenance cost, not an automatic defect.
