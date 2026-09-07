# Architecture critic prompt

Use this template for an independent architectural judgment. Fill every placeholder.

---

Review the architecture of a subsystem after orienting yourself with the explanation. Read the cited code and form your judgment from the implementation.

## Explanation

{EXPLANATION}

## Relevant files

{FILE_PATHS}

## Rubric

{CRITIQUE_RUBRIC}

## Instructions

Find architectural problems rather than line-level bugs or style preferences. A finding must demonstrate a problematic boundary, representation, dependency, or complexity and state what it costs in practice. Intentional trade-offs with a clear benefit can remain as observations or disappear.

For each finding, provide:

- **Severity:** `structural`, `concern`, or `observation`.
- **Finding:** the precise architectural issue and components involved.
- **Evidence:** concrete paths, symbols, and dependency or data-flow chain.
- **Impact:** the change, test, operation, performance, or ownership cost.
- **Direction:** the smallest plausible design move, when evidence supports one.

A `structural` finding blocks likely evolution or rests on a broken boundary or representation. A `concern` creates a demonstrated maintenance or reasoning cost. An `observation` records a lower-priority trade-off. Return no findings when the design is sound.

**Complete when:** every finding survives direct comparison with the code and could be evaluated independently by another engineer.
