# Skills

A collection of agent skills for use with coding agents.

## Install

```bash
npx skills add scottwater/skills
```

See the [skills CLI](https://github.com/vercel-labs/skills) for more options and supported agents.

## Available Skills

### ELI5

`eli5`: Explain a topic with a simple HTML artifact that uses big pictures and few words.

### Simplify

`simplify`: Explicitly invoke a behavior-preserving refinement pass over an implementation to simplify, deduplicate, reorganize, remove low-value tests, and eliminate unnecessary churn.

### Rigor

`rigor`: Apply one focused, evidence-driven engineering workflow to a concrete investigation, bug, feature, refactor, performance problem, prototype, or review. Rigor chooses the matching playbook, scales its gates to the risk, and verifies the requested outcome without starting Tracer's interview, spec, or ticket flow.

Use Rigor when the task is already concrete, such as `/rigor figure out why notifications duplicate after a retry`. Use `/tracer-interview-me` instead when the product idea itself still needs to be discovered.

### Tracer

A lean, user-invoked skill set for spec-driven development: normally `/tracer-interview-me` → `/tracer-to-spec` → `/tracer-to-tickets` → `/tracer-implement`, with `/tracer-wayfinder` as the on-ramp for huge, foggy efforts that must be mapped across sessions. Supporting skills cover research, prototypes, reviews, worktrees, and handoffs. See the [Tracer README](skills/tracer/README.md) for the full flow and skill list.

### DSA Codebase Audit

`dsa-codebase-audit`: Run an explicitly invoked, application-wide, read-only audit for material simplifications in data structures, state representation, control flow, algorithms, and ownership. It inventories every subsystem, reviews non-overlapping boundaries through bounded agent lanes, verifies each finding, and returns a dependency-aware implementation order without changing the repository.

Adapted from the **DSA Codebase Audit** prompt shared by [Aaron Francis](https://x.com/aarondfrancis/status/2088285625946370352?s=20).

### GPT Image Prompts

`gpt-image-prompts`: Turn a visual idea into a production-ready prompt and API settings for OpenAI GPT Image models (`gpt-image-2`), with capability-specific patterns for photorealism, infographics, ads, logos, UI mockups, edits, and compositing.

### GitHub Social Preview

`github-social`: Generate a 1280x640 GitHub repository social preview (Open Graph) image and link it at the top of the README.

### Rails Security

`rails-security` is a multi-agent security review of Rails application code, built on the same quorum pattern as `code-quorum`: independent blind lens agents review the resolved scope, and their findings are merged, verified against source, and returned as one prioritized report. It reviews only what can be inspected and run in development. Server, cloud, container, and CI configuration are out of scope.

| Mode | Lenses |
| --- | --- |
| `quick` | Access control and injection |
| `default` | Access control, injection, and dependencies |
| `full` | Default lenses plus AI/prompt injection |

The AI lens joins any mode automatically when the scope contains LLM or agent code. Request a mode or specific lenses, such as `Run a quick rails-security review of this branch` or `Audit the app with the access-control and ai lenses`.

### Code Quorum

`code-quorum` is an explicitly invoked, read-only review that runs independent reviewer agents, verifies material findings, and returns one prioritized report. It reports medium-and-higher issues by default; explicitly ask for all recommendations to include low-severity items. It runs reviewers on the runtime's native subagent mechanism, reviews pending changes by default, and accepts a PR, branch, revision range, commit, file set, diff, or supplied artifact.

| Mode | Reviewers |
| --- | --- |
| `quick` | Correctness reviewer and silent-failure hunter |
| `default` | Quick reviewers plus failure-mode and test-behavior reviewers |
| `full` | Default reviewers plus simplification reviewer |

A requirements reviewer joins any mode when the review has testable requirements. Request a mode or named combination, such as `Run a quick code quorum` or `Use the failure-mode reviewer and silent-failure hunter from code-quorum`.

## Credits

`rigor`, `blast-radius`, `bro`, `how`, and `why`, along with the human-voice direction in `stop-slop`, were influenced by, borrowed from, and shamelessly stolen from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [Lauren “poteto” Tan](https://x.com/poteto). They have been adapted here to remove Cursor- and model-specific assumptions and to follow this repository's skill-writing conventions.

## License

[MIT](LICENSE)
