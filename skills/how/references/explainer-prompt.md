# Explainer prompt

Use this template to synthesize one or more code traces. Fill every placeholder.

---

Write an architectural explanation for a senior engineer unfamiliar with this area.

## Question

> {QUESTION}

## Prior findings

{PRIOR_FINDINGS_OR_EMPTY}

## Instructions

Use prior findings when supplied. Trace missing evidence directly when they are empty or incomplete. Reconcile overlap and contradictions, and check the code before choosing between conflicting accounts. Preserve open questions when the evidence does not resolve them.

Build a working model rather than an inventory. Name concrete components and calls, explain why each step exists in the flow, and cite the files and symbols a reader should inspect. Use a diagram only when it clarifies interaction or transformation better than prose.

## Output

### Overview

Explain the subsystem's purpose and boundary in one or two paragraphs.

### Key concepts

Define only the types, services, state, or conventions needed to follow the flow.

### How it works

Walk from trigger to observable effect. Include data movement, transformations, decisions, errors, and asynchronous or lifecycle behavior. Cite specific files and symbols.

### Where things live

Map the small set of files a contributor should open first and what each owns.

### Gotchas

Include surprising behavior, sharp edges, and unresolved gaps. Omit the section when none are material.

**Complete when:** the reader can locate the entry point, narrate the main path, identify system boundaries, and distinguish verified behavior from open questions.
