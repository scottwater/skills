# Epistemics for historical rationale

Historical evidence is incomplete and may contradict itself. Classify every claim before writing it so confidence comes from the record rather than the smoothness of the narrative.

## Confidence tiers

### Direct

A source explicitly states the motivation, constraint, alternative, or decision. Examples include a review description naming the bug, a ticket recording a customer requirement, a decision record comparing options, or a comment explaining a threshold.

Use confident causal language with an adjacent citation.

### Supported

Several indirect sources converge, though none states the rationale alone. Name each source and the role it plays in the conclusion.

Use language such as “the evidence points to” and show the chain.

### Inferred

The context supports a reasonable interpretation without explicit confirmation. State the observations, the inference step, and alternative readings.

Use “appears to,” “likely,” “suggests,” or “is consistent with.”

### Speculative

A hypothesis is plausible but evidence is thin or several explanations fit. Present it as one possibility and name the missing evidence that would distinguish it.

### Unknown

The investigation did not recover an answer. Report the sources, queries, time ranges, and access gaps so the reader knows what “unknown” covers.

## Evidence rules

- A claim about intent needs a historical citation. Current code establishes behavior, not why someone chose it.
- Exact wording matters for direct evidence. Quote the relevant passage and identify author, date, and location when available.
- Absence of evidence becomes informative only after a bounded search. A missing result is not proof that no rationale existed.
- Correlation in time supports an inference; it does not establish causation.
- Source authority depends on the question. A ticket may capture the business trigger while a review records the implementation trade-off.
- Later documentation may rationalize or replace the original reason. Compare dates and preserve both when they answer different historical moments.

## Contradictions

Show conflicting sources side by side. State whether they may describe different scopes or stages of the decision. Leave the conflict unresolved when the record cannot choose between them.

## Embedded hypotheses

Treat a reason suggested by the user as one candidate. Search for evidence that would support it and evidence expected under alternatives. Report the result even when it contradicts the prompt's framing.

## Missing evidence

For each material gap, record:

- the unanswered question;
- sources and queries searched;
- inaccessible or expired sources;
- the person or artifact most likely to resolve it, when known.

An explicit unknown is a successful outcome when the record is silent.

## Calibration check

Before finalizing every claim, verify:

1. The confidence tier matches the evidence.
2. Direct and supported claims carry adjacent citations.
3. Inferences expose their reasoning and alternatives.
4. Current code is not cited as proof of its own motivation.
5. Contradictions and gaps remain visible.
6. The confidence summary reflects source coverage and access limits.

**Complete when:** moving any claim to a stronger tier would require new evidence, not stronger wording.
