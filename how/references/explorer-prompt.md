# Explorer prompt

Use this template for each independent exploration angle. Fill every placeholder.

---

You are tracing one slice of a codebase to answer a broader architecture question. Gather source-backed facts for a later explainer. Stay within the assigned angle.

## Question

> {QUESTION}

## Exploration angle

{EXPLORATION_ANGLE}

## Method

1. Find the concrete entry point and cite it.
2. Follow calls, data, and state from the entry point to an observable effect.
3. Read the definitions of central types, interfaces, services, and configuration.
4. Identify inputs, outputs, persistence, process boundaries, and external dependencies.
5. Record behavior that is surprising or easy to misread.
6. Stop only when the assigned path is continuous or the missing edge is named.

Use the runtime's available file-search and read tools. Read implementations rather than inferring behavior from names. Do not broaden into another explorer's angle unless a shared boundary is necessary to complete your own trace.

## Output

### Components

For each central component: name, path, relevant lines, and one-sentence responsibility.

### Flow

Trace the path step by step. Cite the function or method, file, data entering and leaving, decisions made, and next call.

### Boundaries

List interfaces to other modules, processes, stores, services, or users. State the shape crossing each boundary.

### Files read

List every file used as evidence.

### Non-obvious behavior

Record lifecycle, ordering, defaults, error paths, historical artifacts, or misleading names.

### Open questions

Name each edge you could not trace and what evidence would resolve it.

**Complete when:** the assigned path can be reconstructed from the citations without guessing across an omitted step.
