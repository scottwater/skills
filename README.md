# Skills

A collection of agent skills for use with coding agents.

## Install

```bash
npx skills add scottwater/skills
```

See the [skills CLI](https://github.com/vercel-labs/skills) for more options and supported agents.

## Available Skills

### Tracer

A lean, user-invoked skill set for spec-driven development: `/tracer-interview-me` → `/tracer-to-spec` → `/tracer-to-tickets` → `/tracer-implement`, plus supporting skills for reviews, worktrees, and handoffs. See the [Tracer README](skills/tracer/README.md) for the full flow and skill list.

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

`code-quorum` is an explicitly invoked, read-only review that runs independent reviewer agents, verifies material findings, and returns one prioritized report. It runs reviewers on the runtime's native subagent mechanism (ask for Solo explicitly to dispatch through the `solo` skill instead), reviews pending changes by default, and accepts a PR, branch, revision range, commit, file set, diff, or supplied artifact.

| Mode | Reviewers |
| --- | --- |
| `quick` | Correctness reviewer and silent-failure hunter |
| `default` | Quick reviewers plus failure-mode and test-behavior reviewers |
| `full` | Default reviewers plus simplification reviewer |

A requirements reviewer joins any mode when the review has testable requirements. Request a mode or named combination, such as `Run a quick code quorum` or `Use the failure-mode reviewer and silent-failure hunter from code-quorum`.

## License

[MIT](LICENSE)
