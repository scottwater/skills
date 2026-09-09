---
name: herdr-quorum
description: Run a saved model quorum in visible Herdr panes and synthesize its reports.
disable-model-invocation: true
---

# Herdr Quorum

## Resolve the run

Use the requested profile from `profiles/`; default to [review](profiles/review.md). Load only that profile. Resolve the user's request to an exact scope; ask when ambiguous rather than infer a whole-repository task. For a commit range, resolve and freeze the endpoint hashes and check working-tree status in one call. Leave diff inventories and source investigation to the workers.

Require `HERDR_ENV=1`. Read the Herdr skill for terminal mechanics and safety; if unavailable in the skill catalog, load it with `herdr --skill`. Stop if Herdr or its instructions are unavailable. For quorum's documented operations, use the bundled contract directly; general Herdr discovery instructions do not add a preflight here.

Complete when the profile, scope, and Herdr execution context are known.

## Prepare the brief

Prepare one common brief containing the profile's worker instructions, resolved scope, user constraints, and applicable project rules already in context. Keep the synthesis instructions with the lead. Workers load further project guidance as needed during their task; discovering optional rule directories is not a launch prerequisite. An absent optional directory ends that lookup.

Use the profile's `cli|model|reasoning` tuples as data. The [launcher](scripts/launch.py) validates their structure, rejects duplicates and unmapped CLIs, and translates the bundled [CLI mappings](references/cli-arguments.md). Trust those mappings and requested identifiers. Execution is the compatibility check: no help calls, model listings, configuration searches, or documentation probes before launch. Keep compatibility diagnosis separate from a quorum run.

Complete when the exact scope and one common brief are ready. Proceed directly to launch; do not perform the workers' investigation first.

## Launch once

Invoke the launcher with `python3`, its absolute skill-relative path, and one `--worker` per selected tuple. Send the common brief once on stdin using a quoted heredoc. For example, replacing the example tuple and brief with the selected profile and resolved task:

```sh
python3 /absolute/skill/path/scripts/launch.py \
  --worker 'pi|provider/exact-model|high' <<'QUORUM_BRIEF'
<common brief>
QUORUM_BRIEF
```

Run from the project directory. Choose a heredoc delimiter absent from the brief and shell-quote each tuple as one argument. Pass `--direction right` or `--direction down` only when the user requested that first split direction. Allow 120 seconds for the launcher command; worker execution continues independently afterward.

The launcher creates sibling panes without moving focus, partitions only its own worker area, starts fresh interactive agents concurrently, and prompts each immediately when ready. It preserves native configuration and permissions. Each worker receives the common brief plus ten-minute pacing instructions: reserve the final minute for reporting and disclose unfinished scope. Workers remain blind to each other's conclusions and the lead's proposed answer.

Its JSON output prints a private temporary `run_dir` containing `brief.txt`, `run.json`, and `monitor.log`. A detached monitor owns concurrent `agent prompt --wait` calls, durable collection events, and each worker's deadline from submission. It inspects and interrupts only this run's working agents at their deadlines, recording uncertain or still-active outcomes. It continues while the lead reviews reports or a collection command is interrupted.

The launcher returns when every worker has reached a wait attempt or a recorded failure; `waiting` is not proof of prompt delivery or completion. Exit 0 means no failure was recorded at return, not that workers succeeded; exit 1 means recorded failures or a launch/monitor problem; exit 2 means invalid input or context. Inspect the manifest after any interruption, including a tool timeout. Never rerun the launcher automatically or regenerate its mechanics in shell.

Startup or dispatch failures are missing coverage: continue with survivors without retries, substitutions, or repairs. A layout failure stops launch with partial pane IDs preserved. Leave approval decisions to the user.

Complete when the launcher returns or its interrupted outcome has been inspected in the recorded run directory.

## Collect progressively

Use the [collector](scripts/collect.py) rather than agent-state polling:

```sh
python3 /absolute/skill/path/scripts/collect.py --run-dir '<run_dir>' --after 0
```

Allow 390 seconds for each collector command. It blocks until new events, monitor completion, or a five-minute checkpoint; already-recorded events return immediately. Read reports for newly settled workers promptly and source-check them while others continue. Keep those findings with the lead so remaining workers stay blind. Pass the returned `cursor` as `--after` on the next call, after processing the batch. An interrupted call can safely reuse its previous cursor; collection never consumes events.

A `checkpoint` permits one health inspection of this run's unresolved workers, then another blocking collection. A settled state, including `blocked`, is only a cue to inspect—not a usable report. Inspect failed, blocked, unknown, deadline, and interruption events through Herdr. `complete: true` means monitoring ended, not that every worker succeeded. Reconcile every worker in the returned snapshot, including any still active, before synthesis. If the monitor is unavailable, inspect `run.json`, `monitor.log`, and the recorded panes; handle survivors within their remaining budgets without relaunching.

To cancel the run, use the same collector with `--cancel` and allow 720 seconds. It inspects and interrupts this run's working agents without answering approval dialogs or closing panes. Cancellation overlapping a slow submission waits for activity within the worker's original budget. Review the recorded outcomes and report any agents still active; if monitoring has already finished, the collector sends no new input and directs cleanup back to Herdr. A collector/tool timeout alone leaves the monitor and workers running; reconnect with the same cursor. If the monitor is unavailable during cancellation, inspect and interrupt only this run's working agents directly through Herdr.

Read reports using Herdr's recent-unwrapped output. Follow its larger-read and temporary-Markdown fallback when a complete response cannot be recovered. Preserve usable reports even when accompanied by a lifecycle anomaly, and disclose that anomaly. Treat an observed failure to honor an explicit model or reasoning setting as a worker failure. Missing output is missing coverage, not agreement or a no-findings result.

Complete when every worker has a usable report or a failure reason.

## Synthesize

Apply the profile's synthesis instructions to the attributed reports. Label one usable report a single-worker result; if none are usable, return the failure summary without synthesis.

Append coverage for every worker: name, requested CLI/model/reasoning, pane ID when created, and result or failure reason. Distinguish requested settings from any observed mismatch. Leave worker panes open for inspection and follow-up.

Complete when the synthesis and coverage account for every selected worker.

## Maintain profiles and mappings

Add `profiles/<name>.md` with a `Workers` YAML block and `Worker instructions` and `Synthesis instructions` sections. Keep task policy in the profile and execution mechanics in the launcher. Profiles are reference documents, not separately invokable skills.

Only when asked to diagnose compatibility or add a CLI, consult installed help or authoritative documentation and update the [CLI contract](references/cli-arguments.md), launcher, and tests together. Run `python3 -m unittest discover -s /absolute/skill/path/tests -v`; the tests use a fake Herdr and never start real agents.
