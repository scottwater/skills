---
name: how
description: Explain how a subsystem works or where code should live. Use for runtime walkthroughs, architectural ownership, layering questions, and architecture critique; use why for historical motivation.
---

# How

Build a senior-engineer working model of a subsystem from the code that runs it. Explain the architecture and runtime flow without turning the answer into annotated source.

## Choose a mode

- **Explain** is the default for “how does this work?” questions.
- **Place** answers ownership and layering questions such as “where should this live?” Trace the relevant architecture before recommending a boundary.
- **Critique** applies when the user also asks what is architecturally wrong or worth improving. Complete the explanation before judging the design.

## Explain workflow

### 1. Frame the question

Identify the target, desired depth, and likely entry point. For an ambiguous target, state the best interpretation from the conversation and repository context; ask only when different interpretations would require different investigations.

Classify the scope:

- **Narrow:** one module, utility, function, or contained call path.
- **Broad:** a subsystem spanning boundaries, services, persistence, or several independent flows.

Start narrow when uncertain and widen only when an unexplained boundary requires it.

**Complete when:** the target, entry point, and investigation boundary are explicit.

### 2. Trace the code

For a narrow question, trace the implementation directly. For a broad question, divide the subsystem into two to four independent angles, such as state, request flow, persistence, or external boundaries. Explore those angles in parallel when the runtime supports independent read-only agents; otherwise inspect them sequentially.

Use [references/explorer-prompt.md](references/explorer-prompt.md) for delegated exploration. Each angle must follow actual symbols and calls from entry to effect, record files read, and name gaps rather than infer across them.

**Complete when:** every material step from trigger to observable effect has a code citation, and every untraced edge is listed as an open question.

### 3. Synthesize the working model

Reconcile overlap and contradictions across the traces. Re-read code where findings disagree. Use [references/explainer-prompt.md](references/explainer-prompt.md) as the synthesis contract whether the lead writes the answer or delegates it.

The explanation should cover only the sections the question needs:

- **Overview:** purpose and boundary.
- **Key concepts:** the few types or services needed to follow the flow.
- **How it works:** trigger, steps, data transformations, decisions, and effects.
- **Where things live:** the files a new contributor should open first.
- **Gotchas:** surprising behavior, gaps, or sharp edges.

Include a diagram only when component interaction or data transformation is clearer visually than in prose.

**Complete when:** a senior engineer unfamiliar with the area could identify the entry point, trace the main path, and name the subsystem's boundaries without reopening every file.

## Placement workflow

First trace the behavior and boundaries that the proposed code will affect. Then compare candidate owners against:

- domain responsibility and state ownership;
- dependency direction and lifecycle;
- repository patterns for similar behavior;
- the boundary where validation, errors, and side effects belong;
- testability and the likely next change supported by repository evidence.

Recommend one location, explain why it owns the behavior, and state what it should import, expose, and leave elsewhere. Name credible alternatives and why they fit less well. Avoid creating a new layer unless it removes demonstrated coupling or repeated complexity.

**Complete when:** the recommendation cites current boundaries and analogous code, assigns one clear owner, and describes the smallest integration path.

## Critique workflow

### 1. Establish the explanation

Complete the explain workflow first. Critique the architecture that exists, not an assumed design.

### 2. Gather independent judgments

Use [references/critic-prompt.md](references/critic-prompt.md) with the explanation, relevant files, and [references/critique-rubric.md](references/critique-rubric.md). When the runtime supports parallel reviewers, use two or more independent critics to reduce framing bias; otherwise apply the rubric directly.

The method must not depend on a particular agent provider, model, or runner configuration.

**Complete when:** every proposed issue cites the code and states a practical cost rather than a style preference.

### 3. Make the lead judgment

Classify each finding:

- **Act on:** a demonstrated architectural problem worth fixing now.
- **Consider:** a real concern whose cost or remedy remains uncertain.
- **Noted:** a low-priority trade-off or debt marker.
- **Dismissed:** incorrect, unsupported, or merely preferential.

Present the explanation first, followed by the critique. Keep an empty critique when the architecture is sound.

**Complete when:** overlapping findings are merged, disagreements are resolved or exposed, and every retained recommendation has evidence, impact, and an appropriate priority.
