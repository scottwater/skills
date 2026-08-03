---
name: tracer-research
description: Investigate a focused question against high-trust primary sources and capture cited findings as one Markdown note. Use for documentation, API, specification, or local knowledge-base research, including AFK Wayfinder research tickets.
---

# Research

The caller gives one focused question to one background worker so the parent session can continue. If you are that worker, perform the research directly; do not delegate again.

The worker must:

1. Start with **primary sources** — official documentation, specifications, source code, first-party APIs, or the local resource that owns the fact. Do not cite a secondary summary when its underlying source is available.
2. Write the findings to one Markdown note. Match the repo's existing research-note convention; if none exists, use `docs/research/<question-slug>.md`.
3. Cite the source for every material claim and distinguish sourced facts from inference. Include confidence, unresolved gaps, and the implications for the decision waiting on the research.
4. Return the note's path plus a concise answer. Do not modify product code.

For a `/tracer-wayfinder` research ticket, follow the map's capture protocol: work in an isolated checkout, commit the note to the assigned unique `research/<map-slug>/<ticket-slug>` branch, and return the answer plus a branch or commit pointer. Also return a `## Map delta` that states the one-line decision gist, fog entries this answer makes precise or obsolete, proposed new decision tickets and blockers, and any scope change. Do not edit the map or local `.tracer/` ticket state; the Wayfinder coordinator records the resolution and applies the delta.
