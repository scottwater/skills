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

### ASD

`asd`: Explain a topic in [ASD-STE100](https://www.asd-ste100.org/) Simplified Technical English, the controlled language written for aerospace maintenance manuals. Ask for `soft` to go about 80% of the way, or ask for a diagram, an interactive HTML page, or a 3Blue1Brown-style narrated video. Each format keeps its text in STE.

### Simplify

`simplify`: Explicitly invoke a behavior-preserving refinement pass over an implementation to simplify, deduplicate, reorganize, remove low-value tests, and eliminate unnecessary churn.

### Session Review

`session-review`: Report what recent project work took from the invoking agent's session logs: token usage and estimated cost, subagents and models, skills/plugins/extensions used, and repeated attempts around tooling or workflow problems. Supply a timeframe and focus; when no timeframe is given, reviews the current project's preceding seven days. Reports inline unless a file is requested, such as `/session-review look at the last 3 days and generate a 3-day-report.md`.

### Agent Speak

`agent-speak`: Write and refine skills, `AGENTS.md`, `CLAUDE.md`, and other documents agents consume, with explicit context pointers, progressive disclosure, completion criteria, leading words, and pruning.

### Slop Monkey

[`slop-monkey`](skills/slop-monkey/README.md): Rewrite prose to sound direct, readable, and distinctly human. A modified adaptation of Hardik Pandya's [Stop Slop](https://github.com/hardikpandya/stop-slop), renamed to distinguish it from the original skill.

### Rigor

`rigor`: Fix a bug, build a feature, refactor, or improve performance with one focused, evidence-driven playbook. Rigor stops where you ask it to (diagnosis or fix), scales its ceremony to the risk, and hands off with a recommendation to run `/convince-me` for the full proof.

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

### T3 Review

`t3-review`: Review code inside a [T3 Code](https://github.com/pingdotgg/t3code) thread with a reviewer from another model family. Any coding model that is not from OpenAI hands the review to `sol-loop`, so Sol reviews it. OpenAI models get Opus 5.5 at `xhigh` reasoning effort through T3's `delegate_task`. The reviewer only reports. The calling agent checks every Critical, High, and Medium finding against the code, fixes the confirmed ones, and lists the rejected ones with a reason for each. It triggers automatically on requests like `review this code` when T3's MCP tools are available.

### T3 Review Quorum

`t3-review-quorum`: Run an explicitly invoked `code-quorum` review inside a T3 Code thread. Each selected reviewer rubric runs as a T3 delegated task on both Sol 6.1 and Opus 5.5, each at `xhigh` reasoning effort, unless you name other models. It keeps Code Quorum's read-only boundary and report format.

### Orchestrate

`orchestrate`: Turn the current T3 Code session into an orchestrator that writes no code. Pass a prompt or one or more ToVo issues. Each one gets its own T3 worker thread (Opus 5.5 by default) on the current branch. Sol 6.1 reviews each unit, and a run with more than one unit also gets a `t3-review-quorum` review of the combined changes. The orchestrator checks every Medium or higher finding against the code and sends the confirmed ones back to the worker to fix. When the work is done, it marks the ToVo issues completed.

### Herdr Quorum

`herdr-quorum` is an explicitly invoked quorum that runs fresh CLI agents in visible Herdr panes, then synthesizes their reports. It requires a Herdr-managed session and the configured worker CLIs. Each Markdown profile lists `cli|model|reasoning` workers and supplies the worker and synthesis instructions.

Use `/herdr-quorum review Review the current diff` or name another profile. The bundled `review` profile is advisory and issues no merge verdict. Add profiles under [skills/herdr-quorum/profiles](skills/herdr-quorum/profiles/); worker panes stay open for inspection and follow-up.

The Python 3 launcher uses the documented CLI mappings without discovery, starts workers concurrently, and dispatches each as soon as it is ready. Failures are recorded without retries or substitutions. Reviewers work directly rather than spawning another review tier; the lead collects and checks reports as they arrive. Compatibility diagnosis is a separate, explicitly requested task.

### Full Send

`full-send`: Take a change all the way to a merged PR while you are not watching. It finishes the smallest change that works, proves it with evidence it observed itself, reviews it with `sol-loop`, files it with `file-pr`, babysits it with `babysit-pr`, and merges once the merge gate passes. It asks you only when it cannot prove the change, cannot pass the gate, or needs permission it was not given.

### Full Stop

`full-stop`: Do the same work as `full-send`, but stop with the PR open and ready for you to merge. It never merges, and it turns off auto-merge or merge queues on the PR.

### Modernize

`modernize`: Bring an aging PR up to date, and decide honestly whether it should still exist. It checks what changed on the base branch since the PR diverged, then reports `MODERNIZE`, `REWORK`, or `CLOSE`. Only `MODERNIZE` rebases and pushes, with `--force-with-lease`. It never merges or closes the PR.

### Sol Loop

`sol-loop`: Review a change with GPT Sol in a loop until both agents agree. It runs up to three rounds by default (five for security, data-loss, or concurrency risk), keeps a ledger of findings, and pushes back on scope creep. It runs Sol through T3's `delegate_task` or a native subagent, and stops with the blocker rather than substituting another model. `full-send` uses it for review.

### Council

`council`: Review work with three models from three providers: Claude Opus 5.5, GPT Sol 6.1, and Muse Wonder Full, each at high reasoning effort unless you ask for another. It runs them only through T3 Code's `delegate_task` and never substitutes a missing member. Each round, the members score the work out of 10; the calling agent checks their findings, fixes the ones it confirms, and runs another round until all three are satisfied. The scores for each round go into the PR description.

### File PR

`file-pr`: File a PR that opens with a three-to-four-sentence overview of the problem and fix, then folds the rest of the detail into a collapsed `<details>` block labeled with the model and harness that made it, following [Simon Willison's details-summary pattern](https://simonwillison.net/2026/Nov/9/details-summary/). `full-send` uses it, and it triggers on requests to file or open a PR.

### Babysit PR

`babysit-pr`: Watch a PR through CI and human review, and fix the real findings. It waits with `watch_pull_request` in T3 Code and with the bundled `pr-wait` script elsewhere. `pr-wait` needs `python3` and an authenticated `gh`.

### Leaving PR Comments

`leaving-pr-comments`: Format comments that an agent posts on GitHub for you, with a note naming the model and the user it speaks for. The PR skills use it for every comment and reply.

## Archive

Retired skills live in [archive](archive/): `gpt-image-prompts`, `rails-security`, `solo`, and the [Tracer](archive/tracer/README.md) skill set. They are no longer maintained.

## Credits

`slop-monkey` is a modified adaptation of [Stop Slop](https://github.com/hardikpandya/stop-slop) by [Hardik Pandya](https://hvpandya.com), not the upstream skill. This version adds a voice-contract workflow, explicit completion checks, and on-demand diagnostic references. See its [README](skills/slop-monkey/README.md) for details.

`rigor`, `blast-radius`, `bro`, `how`, and `why`, along with the human-voice direction in `slop-monkey`, were influenced by, borrowed from, and shamelessly stolen from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [Lauren “poteto” Tan](https://x.com/poteto). They have been adapted here to remove Cursor- and model-specific assumptions and to follow this repository's skill-writing conventions.

`full-send`, `full-stop`, `modernize`, `sol-loop`, `council`, `file-pr`, `babysit-pr`, and `leaving-pr-comments` are adapted from [tstack](https://github.com/t3dotgg/tstack) by [Theo Browne](https://x.com/theo). These versions do not wait for AI review bots, and `council` seats a fixed T3 council instead of picking each provider's latest flagship.

`agent-speak` is adapted from Matt Pocock's original [`writing-for-agents`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) skill.

## License

[MIT](LICENSE)
