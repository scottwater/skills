# Investigator prompt

Use one copy of this template per evidence category. Fill every placeholder and append the matching category playbook.

---

Gather historical evidence about why a piece of code or a design decision exists. A later synthesizer will form conclusions. Stay within the assigned source category.

## Question

> {QUESTION}

## Code anchor

- **Paths and lines:** {FILES_WITH_LINE_RANGES}
- **Symbols:** {SYMBOLS}
- **Relevant commits or reviews:** {CHANGE_IDS}
- **Linked tickets or documents:** {LINKED_IDS}
- **Time window:** {TIME_WINDOW}

## Assigned source

{SOURCE_NAME}

{SOURCE_PLAYBOOK}

## Method

1. Start with the linked identifiers, symbols, user-facing terms, authors, and time window.
2. Search broader synonyms and neighboring dates before narrowing.
3. Read each relevant item and its discussion in full.
4. Follow links within this source category. Record cross-category links as leads for another lane.
5. Quote exact wording when it bears directly on intent or trade-offs.
6. Record every consequential query, time range, null result, contradiction, retention limit, and access failure.
7. Separate direct statements from circumstantial evidence.

Use only read operations. Discover the available source's tool schema at runtime; do not assume vendor-specific command names.

## Output

### Source and scope

Name the source, account or project scope, and time window.

### Searches performed

List queries, filters, items opened, and links followed with enough detail to reproduce the search.

### Direct evidence

For each item:

- exact quote or faithful excerpt;
- stable citation or identifier;
- author and date when available;
- the part of the question it answers.

### Circumstantial evidence

For each item:

- observation and citation;
- inference it could support;
- plausible alternative readings.

### Contradictions

Place conflicting items together with both citations.

### Null results and gaps

Record searches with no relevant result, inaccessible material, retention limits, and unresolved questions.

### Cross-source leads

List references another category should follow.

**Complete when:** another investigator can reproduce the search, distinguish evidence from interpretation, and see every material gap without asking what was omitted.
