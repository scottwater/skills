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

### Interview Me

`interview-me`: Interview relentlessly, round by round, until you and the agent share an understanding. Each round asks every question that can be answered now, each with a recommended answer; the agent looks up facts itself and leaves decisions to you. It writes nothing.

### Convince Me

`convince-me`: Build the strongest honest, end-to-end case that completed work meets its original goal. Each claim is reported as proven, disproven, or unverified, and failures are returned without repairs.

### DSA Codebase Audit

`dsa-codebase-audit`: Run an explicitly invoked, application-wide, read-only audit for material simplifications in data structures, state representation, control flow, algorithms, and ownership. It inventories every subsystem, reviews non-overlapping boundaries through bounded agent lanes, verifies each finding, and returns a dependency-aware implementation order without changing the repository.

Adapted from the **DSA Codebase Audit** prompt shared by [Aaron Francis](https://x.com/aarondfrancis/status/2088285625946370352?s=20).

### GitHub Social Preview

`github-social`: Generate a 1280x640 GitHub repository social preview (Open Graph) image and link it at the top of the README.

### Orchestrate

`orchestrate`: Turn the current T3 Code session into an orchestrator that writes no code. Pass two or more prompts or ToVo issues (one works too). Each task is built in its own T3 worker thread with `implement`, then reviewed with `review-loop`; the orchestrator checks every finding against the code and sends the confirmed ones back to that worker to fix. Once every task is done, it proves the whole run with `convince-me`, gives it a final `council` review, files a PR with `file-pr`, marks the finished ToVo issues `completed`, and settles every thread it used, its own included.

### Herdr Quorum

`herdr-quorum` is an explicitly invoked quorum that runs fresh CLI agents in visible Herdr panes, then synthesizes their reports. It requires a Herdr-managed session and the configured worker CLIs. Each Markdown profile lists `cli|model|reasoning` workers and supplies the worker and synthesis instructions.

Use `/herdr-quorum review Review the current diff` or name another profile. The bundled `review` profile is advisory and issues no merge verdict. Add profiles under [skills/herdr-quorum/profiles](skills/herdr-quorum/profiles/); worker panes stay open for inspection and follow-up.

The Python 3 launcher uses the documented CLI mappings without discovery, starts workers concurrently, and dispatches each as soon as it is ready. Failures are recorded without retries or substitutions. Reviewers work directly rather than spawning another review tier; the lead collects and checks reports as they arrive. Compatibility diagnosis is a separate, explicitly requested task.

### Full Send

`full-send`: Take a change all the way to a merged PR while you are not watching. It finishes the smallest change that works, proves it with evidence it observed itself, reviews it with `council` (or `review-loop` for a trivial change), files it with `file-pr`, babysits it with `babysit-pr`, and merges once the merge gate passes. It asks you only when it cannot prove the change, cannot pass the gate, or needs permission it was not given.

### Full Stop

`full-stop`: Do the same work as `full-send`, but stop with the PR open and ready for you to merge. It never merges, and it turns off auto-merge or merge queues on the PR.

### Direct Send

`direct-send`: Do the same unattended work as `full-send`, but push straight to origin's default branch (`main`, `master`, or whatever origin names) instead of filing a PR. It proves the change, reviews it with `review-loop`, commits, rebases, pushes as a fast-forward, and watches CI on the pushed commit, fixing forward if it breaks. It never force-pushes, and it asks you when branch protection rejects direct pushes.

### Direct Stop

`direct-stop`: Do the same work as `direct-send`, but stop with the commits rebased and ready to push. It never pushes, and it hands back the exact push command.

### Modernize

`modernize`: Bring an aging PR up to date, and decide honestly whether it should still exist. It checks what changed on the base branch since the PR diverged, then reports `MODERNIZE`, `REWORK`, or `CLOSE`. Only `MODERNIZE` rebases and pushes, with `--force-with-lease`. It never merges or closes the PR.

### Implement

`implement`: Hand a task to a T3 worker thread that implements it, runs the project's checks, and commits, without pushing. The worker runs Opus 5.5 at `high` reasoning effort unless you or the calling skill name another model or effort. The calling agent answers the worker's questions, sends it follow-up fixes, and settles its thread when the work is done. `orchestrate` uses it for every task.

### Review Loop

`review-loop`: Review a change in a loop until the reviewer and the calling agent agree. The reviewer is GPT Sol 6.2 at `high` reasoning effort unless you or the calling skill name another model or effort. It runs up to three rounds by default (five for security, data-loss, or concurrency risk), keeps a ledger of findings, and pushes back on scope creep. It runs the reviewer through T3's `delegate_task` or a native subagent, and stops with the blocker rather than substituting another model. The calling agent fixes verified findings itself, or sends them to an `implement` thread when one owns the code. `direct-send` and `orchestrate` use it for review, and `full-send` uses it for trivial changes.

### Council

`council`: Review work with four models from four providers: Claude Opus 5.5, GPT Sol 6.2, Muse Wonder Full, and Gemini 4 Neon, each at high reasoning effort unless you ask for another. It runs them only through T3 Code's `delegate_task` and never substitutes a missing member. It carries on when at least three members are available, and stops for you below that unless you override the quorum. Each round, the members score the work out of 10; the calling agent checks their findings, fixes the ones it confirms, and runs another round until every present member is satisfied. The scores for each round go into the PR description. `full-send` and `orchestrate` use it for non-trivial review.

### File PR

`file-pr`: File a PR that opens with a three-to-four-sentence overview of the problem and fix, then folds the rest of the detail into a collapsed `<details>` block labeled with the model and harness that made it, following [Simon Willison's details-summary pattern](https://simonwillison.net/2026/Nov/9/details-summary/). `full-send` uses it, and it triggers on requests to file or open a PR.

### Babysit PR

`babysit-pr`: Watch a PR through CI and human review, and fix the real findings. It waits with `watch_pull_request` in T3 Code and with the bundled `pr-wait` script elsewhere. `pr-wait` needs `python3` and an authenticated `gh`.

### Leaving PR Comments

`leaving-pr-comments`: Format comments that an agent posts on GitHub for you, with a note naming the model and the user it speaks for. The PR skills use it for every comment and reply.

## Archive

Retired skills live in [archive](archive/): `code-quorum`, `gpt-image-prompts`, `rails-security`, `rigor`, `solo`, `t3-review`, `t3-review-quorum`, and the [Tracer](archive/tracer/README.md) skill set. They are no longer maintained.

## Credits

`slop-monkey` is a modified adaptation of [Stop Slop](https://github.com/hardikpandya/stop-slop) by [Hardik Pandya](https://hvpandya.com), not the upstream skill. This version adds a voice-contract workflow, explicit completion checks, and on-demand diagnostic references. See its [README](skills/slop-monkey/README.md) for details.

`rigor`, `blast-radius`, `bro`, `how`, and `why`, along with the human-voice direction in `slop-monkey`, were influenced by, borrowed from, and shamelessly stolen from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [Lauren “poteto” Tan](https://x.com/poteto). They have been adapted here to remove Cursor- and model-specific assumptions and to follow this repository's skill-writing conventions.

`full-send`, `full-stop`, `modernize`, `review-loop`, `council`, `file-pr`, `babysit-pr`, and `leaving-pr-comments` are adapted from [tstack](https://github.com/t3dotgg/tstack) by [Theo Browne](https://x.com/theo). These versions do not wait for AI review bots, and `council` seats a fixed T3 council instead of picking each provider's latest flagship.

`agent-speak` is adapted from Matt Pocock's original [`writing-for-agents`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) skill.

## License

[MIT](LICENSE)
