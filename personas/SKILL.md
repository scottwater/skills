---
name: personas
description: Apply one or more expert lenses to feedback, critique, or guidance.
disable-model-invocation: true
---

# Persona lenses

Use the requested persona as a critical lens. Ground the response in the persona file rather than inventing opinions or performing a caricature.

## Workflow

### 1. Resolve the requested lens

Match the user's name or archetype to a file under `personas/`, relative to this skill directory:

| File | Lens |
| --- | --- |
| `bits.md` | Dan Cederholm / SimpleBits |
| `conversion-copywriter.md` | Joanna Wiebe / conversion copywriting |
| `fireball.md` | John Gruber / Daring Fireball |
| `focused-product-manager.md` | Focused product manager |
| `fried.md` | Jason Fried / 37signals |
| `humor-copywriter.md` | Lianna Patch / humor copywriting |
| `skeptical-engineer.md` | Skeptical engineer |
| `user-advocate.md` | User advocate |

If the request does not identify a persona, show this list and ask the user to choose. Do not select one for them.

**Complete when:** every requested lens maps to one persona file.

### 2. Load the persona

Read each matched file in full. Extract its priorities, recurring questions, positions, and delivery style. Treat named-person files as a bounded synthesis of public ideas, not authority to invent new quotations or claim endorsement.

**Complete when:** the relevant criteria from every loaded file are represented in working notes.

### 3. Apply the lens

Evaluate the user's material against those criteria. Tie each material observation to a priority, question, or position from the persona file. Separate evidence in the user's material from extrapolation through the lens.

Use the lens to sharpen judgment, not to replace analysis. Preserve factual accuracy and flag missing context that would change the recommendation.

**Complete when:** every major recommendation has evidence from the material and a clear connection to the requested lens.

### 4. Deliver the response

For one persona, use:

```markdown
## <Persona> lens

<Assessment and recommendations>
```

For multiple personas, give each lens its own section. Add `## Common ground` or `## Tensions` only when the comparison yields useful guidance.

Use first person only when the user explicitly requests role-play. Otherwise, describe what the lens emphasizes. Attribute direct quotations only when the source is known; paraphrase the persona file without quotation marks.

**Complete when:** the response keeps the lenses distinct, identifies agreements or conflicts, and makes no unsupported claims about a real person.
