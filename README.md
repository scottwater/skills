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

### Session Review

`session-review`: Report what recent project work took from the invoking agent's session logs: token usage and estimated cost, subagents and models, skills/plugins/extensions used, and repeated attempts around tooling or workflow problems. Supply a timeframe and focus; when no timeframe is given, reviews the current project's preceding seven days. Reports inline unless a file is requested, such as `/session-review look at the last 3 days and generate a 3-day-report.md`.

### Agent Speak

`agent-speak`: Write and refine skills, `AGENTS.md`, `CLAUDE.md`, and other documents agents consume, with explicit context pointers, progressive disclosure, completion criteria, leading words, and pruning.

### Slop Monkey

[`slop-monkey`](skills/slop-monkey/README.md): Rewrite prose to sound direct, readable, and distinctly human. A modified adaptation of Hardik Pandya's [Stop Slop](https://github.com/hardikpandya/stop-slop), renamed to distinguish it from the original skill.

### Rigor

`rigor`: Apply one focused, evidence-driven engineering workflow to a concrete investigation, bug, feature, refactor, performance problem, prototype, or review. Rigor chooses the matching playbook, scales its gates to the risk, and verifies the requested outcome without starting a discovery interview.

Use Rigor when the task is already concrete, such as `/rigor figure out why notifications duplicate after a retry`. Use `/interview-me` instead when the product idea itself still needs to be discovered.

### Interview Me

`interview-me`: Interview relentlessly, round by round, until you and the agent share an understanding. Each round asks every question that can be answered now, each with a recommended answer; the agent looks up facts itself and leaves decisions to you. It writes nothing.

### Convince Me

`convince-me`: Build the strongest honest, end-to-end case that completed work meets its original goal. Each claim is reported as proven, disproven, or unverified, and failures are returned without repairs.

### DSA Codebase Audit

`dsa-codebase-audit`: Run an explicitly invoked, application-wide, read-only audit for material simplifications in data structures, state representation, control flow, algorithms, and ownership. It inventories every subsystem, reviews non-overlapping boundaries through bounded agent lanes, verifies each finding, and returns a dependency-aware implementation order without changing the repository.

Adapted from the **DSA Codebase Audit** prompt shared by [Aaron Francis](https://x.com/aarondfrancis/status/2088285625946370352?s=20).

### GitHub Social Preview

`github-social`: Generate a 1280x640 GitHub repository social preview (Open Graph) image and link it at the top of the README.

### Code Quorum

`code-quorum` is an explicitly invoked, read-only review that runs independent reviewer agents, verifies material findings, and returns one prioritized report. It reports medium-and-higher issues by default; explicitly ask for all recommendations to include low-severity items. It runs reviewers on the runtime's native subagent mechanism, reviews pending changes by default, and accepts a PR, branch, revision range, commit, file set, diff, or supplied artifact.

| Mode | Reviewers |
| --- | --- |
| `quick` | Correctness reviewer and silent-failure hunter |
| `default` | Quick reviewers plus failure-mode and test-behavior reviewers |
| `full` | Default reviewers plus simplification reviewer |

A requirements reviewer joins any mode when the review has testable requirements. Request a mode or named combination, such as `Run a quick code quorum` or `Use the failure-mode reviewer and silent-failure hunter from code-quorum`.

### Herdr Quorum

`herdr-quorum` is an explicitly invoked quorum that runs fresh CLI agents in visible Herdr panes, then synthesizes their reports. It requires a Herdr-managed session and the configured worker CLIs. Each Markdown profile lists `cli|model|reasoning` workers and supplies the worker and synthesis instructions.

Use `/herdr-quorum review Review the current diff` or name another profile. The bundled `review` profile is advisory and issues no merge verdict. Add profiles under [skills/herdr-quorum/profiles](skills/herdr-quorum/profiles/); worker panes stay open for inspection and follow-up.

The Python 3 launcher uses the documented CLI mappings without discovery, starts workers concurrently, and dispatches each as soon as it is ready. Failures are recorded without retries or substitutions. Reviewers work directly rather than spawning another review tier; the lead collects and checks reports as they arrive. Compatibility diagnosis is a separate, explicitly requested task.

## Archive

Retired skills live in [archive](archive/): `gpt-image-prompts`, `rails-security`, `solo`, and the [Tracer](archive/tracer/README.md) skill set. They are no longer maintained.

## Credits

`slop-monkey` is a modified adaptation of [Stop Slop](https://github.com/hardikpandya/stop-slop) by [Hardik Pandya](https://hvpandya.com), not the upstream skill. This version adds a voice-contract workflow, explicit completion checks, and on-demand diagnostic references. See its [README](skills/slop-monkey/README.md) for details.

`rigor`, `blast-radius`, `bro`, `how`, and `why`, along with the human-voice direction in `slop-monkey`, were influenced by, borrowed from, and shamelessly stolen from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [Lauren “poteto” Tan](https://x.com/poteto). They have been adapted here to remove Cursor- and model-specific assumptions and to follow this repository's skill-writing conventions.

`agent-speak` is adapted from Matt Pocock's original [`writing-for-agents`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) skill.

## License

[MIT](LICENSE)
