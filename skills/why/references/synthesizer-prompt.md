# Synthesizer prompt

Use this template after every planned evidence category has returned a result or a gap.

---

Answer a historical “why” question from the evidence gathered by independent source investigations. Preserve uncertainty and make every material claim verifiable.

## Question

> {QUESTION}

## Code anchor

{CODE_ANCHOR}

## Source findings

{INVESTIGATOR_FINDINGS}

## Unsearched sources

{SKIPPED_SOURCES_WITH_REASONS}

## Method

1. Read the confidence framework in `references/epistemics.md`.
2. Merge duplicate references without losing distinct context.
3. Spot-check quotations and citations that carry a major conclusion.
4. Classify each claim as Direct, Supported, Inferred, Speculative, or Unknown.
5. Keep contradictions visible and explain whether sources may describe different stages or scopes.
6. Treat any hypothesis in the question as a candidate rather than a premise.
7. Preserve documented null results and access gaps.

Do not cite current code as evidence for its own intent. Use code only to anchor what behavior or decision the history concerns.

## Output

### Question

Restate the precise rationale being investigated.

### Code anchor

Give the relevant paths, lines, symbols, and historical window.

### Direct and supported findings

For each claim, label the tier and cite the evidence adjacent to it. Quote the decisive wording when useful.

### Reasonable inferences

Show the observations and inference step for every Inferred claim. Use calibrated language.

### Competing hypotheses

For each viable explanation, state evidence for it, evidence against it, and evidence still needed. Omit this section only when the record supports one explanation without a material alternative.

### Unknowns and gaps

Name unanswered questions, bounded searches with no result, inaccessible sources, and likely follow-up sources or people.

### Sources consulted

For each evidence category, state the source, queries or items reviewed, time window, and outcome. Include null results and skip reasons.

### Confidence summary

Summarize which parts are documented, supported, inferred, speculative, or unknown and how coverage limits that judgment.

### Change constraints

When the user plans to modify the target, add Preserve, Change, Avoid, and Risk bullets derived from the lineage. Omit otherwise.

## Final check

- Every Direct or Supported claim has a citation.
- Every Inferred or Speculative claim uses tier-appropriate language.
- Contradictions and source gaps remain visible.
- The source coverage account matches what investigators actually searched.
- No wording implies more confidence than the evidence supplies.

**Complete when:** a reader can verify the decisive claims, challenge the inference chain, and see exactly where the historical record ends.
