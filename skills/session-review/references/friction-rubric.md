# Friction rubric

## Recurrence

Link episodes by operation, cause, and remedy—not matching error text alone. Normalize error signatures by removing volatile IDs, ports, and paths while retaining the meaningful exception and implicated prerequisite. Count attempts separately from distinct sessions; exclude inherited history and duplicated parent/child reports.

Call a pattern **cross-session recurring** only with cited occurrences in at least two sessions in scope. With one visible session, report local repetition and the comparison gap. Include out-of-window examples only when broader history was requested, separately from window totals. Merge overlapping patterns into one finding per episode.

## Compaction

Classify events by evidenced trigger:

- **Automatic:** flag as an avoidable context-management concern. Record count, affected sessions, and observed rediscovery or rework. Automatic compaction establishes risk; claims of lost information, waste, or ignored warnings require separate evidence.
- **Manual/user-requested:** acceptable intentional context management, excluded from automatic-compaction findings. Assess any later failure on its own evidence.
- **Unknown:** a coverage gap, kept separate from automatic and manual counts.

**Remedies:** checkpoint decisions, changed files, validation status, and next steps at phase boundaries; manually compact before context pressure becomes disruptive, or start a fresh session with a focused handoff. For unattended children, propose bounded work units and durable checkpoints. Attribute responsibility only where an opportunity to intervene is evidenced.

**Success check:** fewer unmanaged automatic events and less post-compaction rediscovery.

## Skill recursion and convergence

Trace executed invocation chains, including child dispatches: direct recursion (`A → A`), indirect recursion (`A → B → A`), and repeated review/fix or research/planning cycles. Repeated skill reads alone do not establish recursive execution.

Flag cycles that repeat an objective without new evidence, a changed artifact, or a narrower problem; record the chain, iterations, exit condition, and outcome. Distinguish productive iteration and user-requested reruns from self-triggered loops.

**Remedies:** give the outer workflow ownership of iteration; have inner skills return findings to their caller. Define completion criteria and retry budgets; escalate when a cycle adds no information.

**Success check:** each iteration makes identifiable progress or stops at its stated limit.

## Execution blockers

Inspect failed app starts, scripts, service launches, and feature runs for missing dependencies, runtime mismatches, wrong commands/directories, absent environment variables, and unavailable services. Include failures eventually worked around.

Classify by failure, not command name: a test/spec runner that cannot boot is an **execution blocker**; a failing assertion, defect reproduction, or intentional TDD red phase can be **useful validation**.

For each occurrence, record attempts, resolution, and whether a previously discovered remedy was available but missed. Repeatedly rediscovering a workaround is a finding even when every session succeeds. Treat first-time setup discovery separately from recurrence and retries that ignore an established cause.

**Remedies:** repair the bootstrap path, add a preflight check, align dependency/runtime declarations, or place the proven command and non-obvious prerequisite where the agent reaches them before execution. Capture durable guidance rather than leaving the fix buried in a transcript.

**Success check:** a fresh session reaches the intended operation without repeating the known blocker.

## Other teachable patterns

| Pattern | Evidence | Remedy → success check |
| --- | --- | --- |
| Blind retries | Same failing action with unchanged inputs, environment, and diagnostic hypothesis | Require a changed hypothesis or prerequisite → retries gather new information. |
| Rediscovery / fragile handoffs | Decisions or constraints repeatedly reconstructed across sessions or children | Keep a concise decision/handoff note at the point of use → later work reuses it. |
| Late validation | An available cheap check would have exposed a blocker before substantial implementation | Run a boot/smoke check or smallest relevant test early → prerequisites are established before expanding the work. |
| Scope drift | Work expands beyond the request or reopens without new evidence | Define deliverable, acceptance checks, and exclusions → delivery stops at those criteria. |
| Duplicated delegation | Overlapping work without an intentional independent-verification purpose | Assign disjoint ownership and a merge point → remaining duplication has an explicit verification benefit. |
