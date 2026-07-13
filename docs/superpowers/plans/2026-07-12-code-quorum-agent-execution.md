# Code Quorum Agent Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Code Quorum user-invoked and require one fresh Solo-managed or runtime subagent for every selected reviewer.

**Architecture:** Add an agent-capability gate before scope resolution. Prefer Solo only when the current workflow uses Solo and Solo MCP is available; otherwise use the host's subagent abstraction. Remove in-context review simulation, retain valid partial results, and stop when no independent worker mechanism or usable reviewer result exists.

**Tech Stack:** Markdown skills, YAML frontmatter, Solo MCP contract, runtime subagent abstractions, skill-creator validation

## Global Constraints

- Set `disable-model-invocation: true`; run only after explicit user invocation.
- Keep `description` short and human-facing.
- Create one fresh isolated agent per selected reviewer.
- Prefer Solo-managed agents when already using Solo and Solo MCP is available.
- Use another runtime subagent abstraction when Solo is not the active mechanism.
- Permit sequential scheduling only when each reviewer still gets a fresh context.
- Stop before scope inspection when no independent-agent mechanism exists.
- Synthesize all usable returned findings and disclose missing reviewer coverage.
- Return an execution failure when no reviewer returns a usable result.
- Preserve the existing read-only, provenance, verification, severity, and disposition contracts.

---

### Task 1: Require independent reviewer agents

**Files:**
- Modify: `code-quorum/SKILL.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: explicit Code Quorum invocation and the selected reviewer set.
- Produces: one isolated worker result per successful reviewer, coverage limitations for missing results, or an execution-unavailable response.

- [ ] **Step 1: Run contract checks to establish RED**

```bash
test "$(rg -c '^disable-model-invocation: true$' code-quorum/SKILL.md)" = 1
test "$(rg -c '^## Confirm agents$' code-quorum/SKILL.md)" = 1
rg -q 'Do not continue to scope resolution' code-quorum/SKILL.md
rg -q 'Solo-managed agent' code-quorum/SKILL.md
rg -q 'Do not run reviewer passes in the delegator context' code-quorum/SKILL.md
```

Expected: the combined check fails because the current skill is model-invoked and permits separated in-context passes.

- [ ] **Step 2: Make invocation user-only**

Replace frontmatter with:

```yaml
---
name: code-quorum
description: Run independent code-review agents and synthesize verified findings.
disable-model-invocation: true
---
```

- [ ] **Step 3: Add the agent preflight before scope resolution**

Insert this section after `Read-only boundary`:

```markdown
## Confirm agents

Confirm an independent-worker mechanism before inspecting the review scope.

When the current workflow uses Solo, check whether Solo MCP is available. If available, use it to create one Solo-managed agent for each selected reviewer. Otherwise use the runtime's subagent abstraction. Do not switch into Solo merely because its tools exist when the current workflow is not using Solo.

Require a fresh isolated context for every reviewer. Concurrency is optional; independence is required. Do not continue to scope resolution when neither Solo nor another subagent abstraction can create fresh workers. Return an execution-unavailable response that names the missing capability.

Complete this step when one available mechanism can create a fresh agent for each selected reviewer.
```

- [ ] **Step 4: Replace the quorum execution fallback**

Replace the existing `Run the quorum` body with:

```markdown
## Run the quorum

Create one fresh agent for each selected reviewer through the mechanism confirmed above. Run agents concurrently when capacity allows. Schedule them sequentially when capacity is constrained, while preserving a fresh isolated context for each reviewer. Give each agent only the shared task packet and its selected rubric. Do not run reviewer passes in the delegator context.

Report reviewer completion as results arrive when the runtime supports progress updates. Wait until every selected reviewer has returned, failed, timed out, or could not start before synthesis.

Record each returned result separately. `source_reviewers` may include only reviewers that independently returned a materially equivalent claim. Selection alone is not agreement or attribution evidence.

Synthesize every usable returned result. List each missing reviewer and its failure reason under coverage limitations. Treat no missing reviewer as agreement, disagreement, or `no_findings`. Return an execution failure instead of a review when no reviewer returns a usable result.

Complete this step when every selected reviewer has a usable result or a recorded failure reason, and at least one usable result exists.
```

- [ ] **Step 5: Update repository documentation**

Replace the first Code Quorum paragraph in `README.md` with:

```markdown
`code-quorum` is an explicitly invoked, read-only review that runs independent reviewer agents, verifies material findings, and returns one prioritized report. It requires Solo MCP or another subagent mechanism, reviews pending changes by default, and accepts a PR, branch, revision range, commit, file set, diff, or supplied artifact.
```

- [ ] **Step 6: Run GREEN static validation**

```bash
uv run --with pyyaml python /Users/scott/.codex/skills/.system/skill-creator/scripts/quick_validate.py code-quorum
test "$(rg -c '^disable-model-invocation: true$' code-quorum/SKILL.md)" = 1
test "$(rg -c '^## Confirm agents$' code-quorum/SKILL.md)" = 1
test "$(rg -c 'Complete this step' code-quorum/SKILL.md)" = 9
rg -q 'Do not continue to scope resolution' code-quorum/SKILL.md
rg -q 'Solo-managed agent' code-quorum/SKILL.md
rg -q "runtime's subagent abstraction" code-quorum/SKILL.md
rg -q 'Do not run reviewer passes in the delegator context' code-quorum/SKILL.md
rg -q 'Synthesize every usable returned result' code-quorum/SKILL.md
rg -q 'no reviewer returns a usable result' code-quorum/SKILL.md
! rg -n 'separated in-context|separated current-context|simulate reviewer' code-quorum/SKILL.md
rg -q 'explicitly invoked.*independent reviewer agents.*requires Solo MCP or another subagent mechanism' README.md
git diff --check
```

Expected: validator reports `Skill is valid!`; nine completion criteria; mandatory agent, partial-result, and stop contracts present; old in-context fallback absent; README and whitespace checks pass.

- [ ] **Step 7: Commit**

```bash
git add code-quorum/SKILL.md README.md
git commit -m "feat: require agents for code quorum"
```

### Task 2: Forward-test execution routing and failure behavior

**Files:**
- Modify on failed behavior only: `code-quorum/SKILL.md`

**Interfaces:**
- Consumes: the Task 1 skill and disposable review fixtures.
- Produces: evidence for non-Solo routing, unavailable-agent stop, isolated reviewer contexts, and partial-result synthesis.

- [ ] **Step 1: Create a disposable review fixture**

```bash
fixture="$(mktemp -d)"
git -C "$fixture" init -q
git -C "$fixture" config user.email test@example.com
git -C "$fixture" config user.name "Code Quorum Test"
printf 'def fetch(cache):\n    return cache.read()\n' > "$fixture/service.py"
git -C "$fixture" add service.py
git -C "$fixture" commit -qm baseline
printf 'def fetch(cache):\n    try:\n        return cache.read()\n    except Exception:\n        return []\n' > "$fixture/service.py"
git -C "$fixture" status --short
```

Expected: ` M service.py`.

- [ ] **Step 2: Test non-Solo subagent routing**

Start a fresh controller that is not using Solo with this prompt:

```text
Use code-quorum at /Users/scott/projects/skills/code-quorum/SKILL.md to run a quick review in the repository identified by the shell's $fixture value. This workflow is not using Solo. Use your available subagent mechanism. Do not edit files.
```

Require two fresh reviewer agents, one for `general-reviewer` and one for `silent-failure-hunter`. Require the final report to state reviewer coverage without in-context simulation. Confirm `git -C "$fixture" status --short` remains ` M service.py`.

- [ ] **Step 3: Test Solo routing with a capability fixture**

Start a fresh evaluator with this capability fixture:

```yaml
workflow: solo
solo_mcp: available
selected_reviewers: [general-reviewer, silent-failure-hunter]
```

Require a routing plan that creates one Solo-managed agent for each reviewer. Reject a plan that uses generic subagents, puts both rubrics in one agent, or runs either pass in the delegator context.

- [ ] **Step 4: Test unavailable-agent behavior**

Start a fresh evaluator with the skill and this capability fixture:

```text
The user explicitly invoked code-quorum. This runtime has no Solo MCP and no subagent abstraction. Show the response required before any scope inspection. Do not inspect repository state.
```

Require an execution-unavailable response naming the missing independent-worker capability. Reject output that resolves scope or performs any reviewer pass.

- [ ] **Step 5: Test partial results**

Start a fresh evaluator with pre-recorded worker outcomes:

```yaml
selected_reviewers: [general-reviewer, silent-failure-hunter]
general-reviewer:
  status: returned
  result: no_findings
silent-failure-hunter:
  status: timed_out
```

Require synthesis of the usable general result, a coverage limitation naming the timed-out reviewer, and no claim that the missing reviewer agreed or returned `no_findings`.

- [ ] **Step 6: Test zero usable results**

Use this outcome fixture:

```yaml
selected_reviewers: [general-reviewer, silent-failure-hunter]
general-reviewer: { status: failed }
silent-failure-hunter: { status: timed_out }
```

Require an execution failure rather than a review or no-findings conclusion.

- [ ] **Step 7: Validate and commit evidence-driven corrections**

```bash
uv run --with pyyaml python /Users/scott/.codex/skills/.system/skill-creator/scripts/quick_validate.py code-quorum
test "$(rg -c 'Complete this step' code-quorum/SKILL.md)" = 9
git diff --check
```

Expected: all commands pass. If a behavioral test misses a requirement, make the smallest correction in the authoritative execution section, rerun the failed case, then commit:

```bash
git add code-quorum/SKILL.md
git commit -m "fix: tighten code quorum agent routing"
```

Skip the correction commit when all forward tests pass.

### Task 3: Final verification

**Files:**
- Verify: `code-quorum/SKILL.md`
- Verify: `README.md`

**Interfaces:**
- Consumes: Tasks 1-2.
- Produces: final proof that Code Quorum is user-invoked and cannot review without independent agents.

- [ ] **Step 1: Run the complete gate set**

```bash
uv run --with pyyaml python /Users/scott/.codex/skills/.system/skill-creator/scripts/quick_validate.py code-quorum
test "$(find code-quorum/references/reviewers -type f -name '*.md' | wc -l | tr -d ' ')" = 5
test "$(rg -c '^disable-model-invocation: true$' code-quorum/SKILL.md)" = 1
test "$(rg -c 'Complete this step' code-quorum/SKILL.md)" = 9
test ! -e code-review
test ! -e code-quorum/agents
! rg -n 'code-review/' README.md
! rg -n 'model:|tools:|subagent_type:|Task tool|Claude' code-quorum
! rg -n 'separated in-context|separated current-context|simulate reviewer' code-quorum/SKILL.md
for file in code-quorum/references/reviewers/*.md; do test "$(rg -c '^## (Search|Evidence bar|Exclude)$' "$file")" = 3 || exit 1; done
git diff --check
git diff --cached --check
```

Expected: every command exits 0.

- [ ] **Step 2: Inspect repository state**

```bash
git status --short
git log --oneline -6
```

Expected: no tracked changes. Report unrelated pre-existing untracked files separately.
