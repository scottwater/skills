# Feature

1. **Pin the behavior.** Translate the request into observable success and material failure conditions. Look up technical facts; ask only unresolved product choices that would change the behavior.
   **Complete when:** implementation can be judged without inventing intent.
2. **Ground the system.** Trace the existing path, ownership, contracts, analogous behavior, and tests. Identify compatibility and lifecycle constraints.
   **Complete when:** the integration point and affected boundaries are supported by repository evidence.
3. **Shape.** Apply the loaded Shape rules only to state, interfaces, and boundaries changed by the behavior. Keep local stateless behavior local.
   **Complete when:** every changed shape satisfies the Shape reference and unchanged shapes remain outside the design.
4. **Plan verifiable units.** Put blocking foundations first and order dependencies. Apply the loaded Safety ownership rules when work can proceed in parallel.
   **Complete when:** every unit ends in an observable check, dependencies are ordered, and every shared mutable target has either an isolated owner or an explicit serialization boundary.
5. **Implement narrowly.** Build the smallest complete path through the requested behavior. Keep unrelated cleanup out; subtract obsolete paths that the new behavior directly replaces.
   **Complete when:** the implementation covers the promised path without unrelated changes or speculative extension points.
6. **Prove the feature.** Exercise the actual user or integration path, then run focused and repository-required checks. Review the diff against the requested behavior, failure conditions, and existing contracts.
   **Complete when:** every promised behavior has fresh evidence and every unverified edge is disclosed.

**Done when:** the requested behavior works at the strongest practical boundary and maintainers inherit a coherent data and ownership model.
