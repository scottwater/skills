---
name: why
description: Investigate why code or a design decision exists. Use for rationale, rejected alternatives, regressions, postmortems, historical constraints, and evidence-backed thresholds; use how for runtime behavior.
---

# Why

Recover the forces that shaped code from historical evidence. Separate documented intent from supported inference, plausible hypotheses, and unknowns.

Code is evidence of mechanics, not motivation. Motivation may live in source history, reviews, tickets, documents, team discussions, incidents, telemetry, or product data.

## Investigation workflow

### 1. Frame the question

Identify:

- the target code, pattern, feature, or decision;
- the specific rationale the user wants;
- any hypothesis embedded in the question.

Use open files, recent edits, and conversation context to interpret a vague referent. State the interpretation so the user can redirect it. Ask only when different interpretations would require materially different investigations.

Treat the user's suggested explanation as a hypothesis to test.

**Complete when:** the target and question are precise enough to define relevant evidence.

### 2. Build the code anchor

Record the relevant paths and lines, key symbols, last-touch commits, earlier history through renames, and linked reviews or tickets. Useful starting commands include:

```bash
git blame -L <start>,<end> <file>
git log --follow -p -- <file>
git log --oneline -20 -- <file>
git log -1 --format=%B <commit>
```

Use an available forge client or API to read review descriptions and discussion. Do not assume a particular forge or tool is installed.

Capture paths, symbols, commits, review IDs, ticket IDs, dates, authors, and search terms for reuse across sources.

**Complete when:** an investigator can search another system without rediscovering what code and time window the question concerns.

### 3. Build the coverage map

Discover the repository and external read-only connectors available in the current runtime. Create one ledger entry per connector, then map each entry to an evidence category:

1. source control and code review;
2. issue or ticket tracking;
3. long-form documents;
4. real-time team discussion;
5. infrastructure observability and incidents;
6. error or exception tracking;
7. product analytics or warehouse data.

Read [references/source-playbook.md](references/source-playbook.md), then load only the playbook for each available category. Tool names and schemas come from the runtime, not this skill.

Search every available connector by default, including multiple connectors in one category when they hold distinct records. Mark each ledger entry `searched`, `unavailable`, `inaccessible`, or `inapplicable`, with a reason and scope. A category may be inapplicable only when the target cannot enter it by construction.

**Complete when:** every discovered connector has a search plan or a specific status reason, and all seven categories appear in the ledger even when no connector is available.

### 4. Investigate each source

Search connectors concurrently when independent read-only agents are available; otherwise search them sequentially. Use one bounded lane per connector, combining connectors only when they expose the same records and query vocabulary. The method must not depend on a particular agent provider, model, or runner configuration.

Use [references/investigator-prompt.md](references/investigator-prompt.md) as the lane contract. Pass the question, code anchor, category playbook, and any cross-cutting incident angle. Investigators gather evidence rather than answer the question.

For each source:

- search broadly, then narrow;
- read complete relevant items and their discussion;
- capture exact quotations with stable citations when wording matters;
- record queries, time ranges, null results, contradictions, and access limits;
- pass cross-source leads to the matching category rather than silently changing scope.

A null result becomes useful evidence only when the search that produced it is documented.

**Complete when:** every planned category returns cited evidence, a documented null result, or a named access gap.

### 5. Synthesize with calibrated confidence

Read [references/epistemics.md](references/epistemics.md) and [references/synthesizer-prompt.md](references/synthesizer-prompt.md). Synthesize directly or delegate to one read-only synthesizer with access to all findings and the code anchor.

Classify each claim:

- **Direct:** a source explicitly states the rationale.
- **Supported:** multiple indirect sources converge.
- **Inferred:** a reasonable interpretation with a visible inference chain.
- **Speculative:** a plausible hypothesis with thin or competing evidence.
- **Unknown:** the search did not answer the question.

Spot-check citations before presenting them. Surface contradictions instead of resolving them for narrative neatness. Preserve confidence language during any final edit.

**Complete when:** every rationale claim has a confidence tier, tier-appropriate phrasing, and adjacent evidence or an explicit gap.

### 6. Present the lineage

Use this structure, omitting only sections that truly have no content:

1. **Question**
2. **Code anchor**
3. **Direct and supported findings**
4. **Reasonable inferences**
5. **Competing hypotheses**
6. **Unknowns and gaps**
7. **Sources consulted**
8. **Confidence summary**

For each source, state what was searched and what was found, including null results and skip reasons. A reader should be able to verify a cited claim quickly and judge the investigation's coverage.

When the investigation precedes a code change, add a concise constraint set:

- **Preserve:** behavior or rationale still supported by evidence.
- **Change:** assumptions the evidence shows are obsolete.
- **Avoid:** rejected paths whose failure still applies.
- **Risk:** gaps or uncertainty the plan must protect against.

**Complete when:** the answer distinguishes knowledge from inference, exposes the search boundary, and leaves the user with verifiable evidence rather than a plausible story.
