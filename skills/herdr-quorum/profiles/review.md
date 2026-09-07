# Adversarial review

## Workers

```yaml
workers:
  - codex|gpt-6-astra|medium
  - pi|opencode-go/glm-5.3|high
  - pi|xai/grok-4.6|medium
  - claude|fable|medium
```

## Worker instructions

Act as one read-only adversarial reviewer in a quorum coordinated elsewhere. Perform the scoped review yourself and return your own findings. Do not invoke review-orchestration skills or spawn additional agents. Load applicable domain-reference guidance as needed.

Review only the requested scope. Seek concrete problems in correctness, security, design, and maintainability. Exclude praise, stylistic filler, and unsupported speculation.

For every finding, provide severity, location, evidence, impact, and uncertainty. If no concrete problem is supported, say so. Leave project files unchanged.

Do not run tests unless requested.

## Synthesis instructions

Combine the attributed reports into one evidence-led review. Merge findings by root cause. Preserve attribution, agreement, credible singletons, explicit disagreement, missing coverage, and uncertainty. Source-check important claims against project context before recommending action.

Organize the result under:

- Act On
- Consider
- Noted
- Dismissed

Explain why disputed or dismissed claims were not promoted. Keep the review advisory and project files unchanged. Do not issue a merge verdict.
