# Log sources

Use the invoking harness's branch below. Paths are discovery hints, not a fixed schema: check environment/configuration overrides, installed documentation, and actual records. Read metadata first; inspect message bodies only for the selected project and linked children. Avoid credential stores. A conversation-history index alone is not a usage ledger.

## Friction evidence across formats

Retain friction events even without usage counters:

- **Compaction:** preserve trigger/reason metadata and explicit user compact actions tied to the event. Verify trigger semantics against the running harness's format; marker names and generated summaries alone may not identify the trigger.
- **Skill execution:** preserve invocation and child-dispatch links to reconstruct call chains.
- **Execution failures:** preserve operation, exit status, exception/message, and subsequent workaround to compare causes and remedies across sessions.

## Pi

Start with `~/.pi/agent/sessions/`, overridden by `PI_CODING_AGENT_DIR`, `PI_CODING_AGENT_SESSION_DIR`, or an explicit session directory. Locate the current session through harness metadata such as `PI_SESSION_FILE` when available. Check installed Pi session-format documentation for the running version.

JSONL headers commonly identify `cwd`, session ID, and `parentSession`; entries form a tree. Assistant messages carry model/provider and per-response `usage`. Compaction and branch-summary entries may carry additional usage. Tool results can contain nested model usage; reconcile it with child logs before including it. Extension records and Agent result banners may repeat child work or omit cache/compaction counters.

Pi commonly separates `input`, `cacheRead`, `cacheWrite`, and `output`; `reasoning`, when present, can already be inside output. Test the identities in this corpus. Model-change entries record selection, not necessarily execution. Assistant and enclosing-entry timestamps may provide a response-span estimate, not exact API timing.

## Codex

Start with `$CODEX_HOME` or `~/.codex`, including `sessions/` and `archived_sessions/` when present. Rollout JSONL commonly includes `session_meta`, `turn_context`, `response_item`, and `event_msg` records. Use metadata such as cwd, session/thread ID, parent/fork IDs, and agent source to identify the project and descendants. Preserve model/provider context by segment when individual events omit it.

`event_msg` token-count records can contain both `info.total_token_usage` and `info.last_token_usage`. **Never sum cumulative snapshots.** Repeated telemetry may describe the same completion; pair last-usage records with unique completions or derive validated cumulative deltas. Forks, inherited histories, resets, and window boundaries require a known baseline; if attribution remains ambiguous, report the supported session/segment total rather than fabricated turn totals.

Cached input is commonly a subset of input tokens, and reasoning output a subset of output tokens. Validate before normalization. Pricing, per-call timestamps, compaction cost, and child usage can be unavailable even when aggregate token counters exist.

## Claude Code

Start with `~/.claude/projects/`, respecting any configured Claude data directory. Project transcripts and nested subagent files may be separate. Use cwd, session/agent IDs, message/request IDs, parent links, and sidechain markers where present.

Assistant records commonly include model and usage with input/output plus cache-creation/cache-read fields. Validate whether cache fields are additive. Streaming fragments or repeated records can share a message ID and usage; count the logical response once. Confirm how the installed version records compaction, tool use, hooks, and subagents. Installed plugin lists and startup tool catalogs show availability, not execution.

## Other harnesses or changed formats

Use that harness's local documentation/configuration to locate transcripts, usage exports, and child traces. Document its event identity, cumulative/per-call semantics, cache/reasoning relationships, and timing limits before aggregation. An SQLite/index source may aid discovery but does not automatically contain full execution evidence. Use read-only access; separate provider billing records from session-derived estimates.
