---
name: oracle
description: Perform a high-context consistency review of the current plan, conversation, or code-review direction for decision drift, contradictions, hidden assumptions, risks, and the best next move.
---

# Code Review: Oracle

Use this skill for high-context decision consistency review. It is self-contained and does not depend on an external `oracle` agent.

Use it when the user wants a second opinion on a plan, a review strategy, a conversation thread, or a proposed next move.

## Review Focus

Check for:

1. Decision drift: the current direction no longer matches the user's approved goal.
2. Contradictions: requirements, plans, or recommendations conflict with each other.
3. Hidden assumptions: the plan relies on facts not established in the conversation or repository.
4. Risk concentration: one decision creates outsized implementation, maintenance, security, or review risk.
5. Missing sequencing: work is ordered in a way that increases rework or blocks validation.
6. Best next move: the immediate next action that preserves momentum and reduces risk.

## Inputs To Inspect

Use the available conversation context first. If reviewing repository work, inspect only the files needed to answer the consistency question.

Useful read-only commands when repository context matters:

```sh
git status --short
git log --oneline -5
git diff --stat HEAD
git diff --name-status HEAD
```

## Output Format

```md
# Oracle Review

## Current Direction
- <one or two sentences describing the apparent plan or decision path>

## Decision Drift
- <drift found, or `No material drift found`>

## Contradictions
- <contradictions found, or `No material contradictions found`>

## Hidden Assumptions
- <assumptions that need validation>

## Key Risks
- <highest leverage risks>

## Best Next Move
- <specific next action>

## Confidence
- <High | Medium | Low> — <why>
```

## Rules

- Do not edit files.
- Do not invent missing context.
- Prefer one actionable recommendation over a broad menu.
- If the best next move is to ask the user a question, ask one question.
