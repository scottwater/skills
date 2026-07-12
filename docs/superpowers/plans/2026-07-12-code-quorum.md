# Code Quorum Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `code-review/` with one portable, read-only `code-quorum` skill that selects independent lenses, verifies material claims, and returns a prioritized report.

**Architecture:** Keep the shared process in `code-quorum/SKILL.md`. Put conditional review rubrics in `code-quorum/references/reviewers/`. Define portable task packets and execution fallbacks without naming an agent API.

**Tech Stack:** Markdown skills, YAML frontmatter, POSIX shell checks, skill-creator validators

## Global Constraints

- Review only; remediation requires separate authorization.
- Default to pending staged, unstaged, and relevant untracked changes.
- Support `quick`, `default`, `full`, and explicit reviewer selections.
- Verify every potential blocker.
- Use severity words canonically and P0-P3 only as requested aliases.
- Keep each behavioral rule in one authoritative file.
- Keep platform mechanics outside the canonical workflow.
- Remove `code-review/` without compatibility wrappers.

---

## File Map

- Create `code-quorum/SKILL.md`: shared process and contracts.
- Create `code-quorum/references/reviewers/adversarial-reviewer.md`: ship-readiness attacks.
- Create `code-quorum/references/reviewers/general-reviewer.md`: correctness and regressions.
- Create `code-quorum/references/reviewers/simplification-reviewer.md`: needless complexity.
- Create `code-quorum/references/reviewers/silent-failure-hunter.md`: hidden failures.
- Create `code-quorum/references/reviewers/skeptical-engineer.md`: assumptions and design risks.
- Modify `README.md`: replace the legacy catalog.
- Delete the 11 tracked `code-review/*/SKILL.md` files with `trash`.

### Task 1: Build the canonical skill

**Files:**
- Create: `code-quorum/SKILL.md`
- Create: `code-quorum/references/reviewers/*.md` (five named files from the file map)

**Interfaces:**
- Consumes: a review request plus repository or artifact context.
- Produces: normalized `finding-v1` candidates and one prioritized report.

- [ ] **Step 1: Confirm the structural test starts red**

Run: `test -f code-quorum/SKILL.md`

Expected: exit 1 because the skill does not exist.

- [ ] **Step 2: Initialize with skill-creator**

Run:

```bash
/Users/scott/.codex/skills/.system/skill-creator/scripts/init_skill.py code-quorum --path /Users/scott/projects/skills --resources references --interface display_name="Code Quorum" --interface short_description="Run independent code-review lenses and synthesize verified findings" --interface default_prompt="Run the default code quorum on pending changes and return a verified prioritized review."
trash code-quorum/agents
mkdir -p code-quorum/references/reviewers
```

Expected: `SKILL.md` and `references/` exist. Generated Codex-only UI metadata has moved to Trash so the canonical package stays portable.

- [ ] **Step 3: Write the shared skill**

Use only this frontmatter:

```yaml
---
name: code-quorum
description: Review code changes through independent reviewer lenses, verify material claims, and return one prioritized read-only report. Use when the user asks for a code quorum; requests a quick, default, full, or custom multi-perspective review; names a quorum reviewer; or asks to review pending changes, a branch, commit, pull request, diff, or file set.
---
```

Write these ordered sections and completion criteria:

1. `Resolve scope`: explicit scope; pending changes against `HEAD`; branch merge-base; associated PR; recent commit; task artifacts. Never infer a whole-repository review; flag unusually large inferred ranges. Complete when the exact diff, range, or files can be stated.
2. `Select reviewers`: explicit names before named sets before default. Apply focus, additions, and exclusions. Complete when selection has one interpretation.
3. `Construct task packets`: same scope, source, changed files, focus, exclusions, project rules, read-only flag, and contract; one distinct rubric; no prior conclusions. Complete when every packet is bounded and equivalent except for rubric.
4. `Run the quorum`: isolated concurrent workers, sequential delegated workers, then separated in-context passes. Record weak isolation. Continue after one reviewer fails and disclose the missing coverage. Complete when each reviewer returns findings, `no_findings`, or a recorded failure.
5. `Normalize candidates`: require title, file and lines, category, proposed severity, confidence, claim, trigger, impact, evidence, recommendation, and source reviewer. Complete when every candidate conforms or has a rejection reason.
6. `Synthesize`: merge by root cause; remove style-only, speculative, pre-existing, and out-of-scope claims; resolve disagreement from source evidence. Complete when each candidate is merged, retained, rejected, or unresolved.
7. `Verify`: trace every potential blocker through source, safeguards, and tests; reproduce when proportionate; assign `verified`, `partially-verified`, `unverified`, or `rejected`. Complete when each potential blocker has status, method, and evidence.
8. `Prioritize and report`: assign severity, verification, confidence, and disposition. Complete when the report separates verified defects, unresolved risks, and optional improvements.

Define sets exactly:

```yaml
quick:
  - general-reviewer
  - silent-failure-hunter
default:
  - adversarial-reviewer
  - general-reviewer
  - silent-failure-hunter
  - skeptical-engineer
full:
  - adversarial-reviewer
  - general-reviewer
  - simplification-reviewer
  - silent-failure-hunter
  - skeptical-engineer
```

Accept `simple` and `lightweight` as `quick` aliases. Load only selected reviewer files.

Define `finding-v1`:

```yaml
title: Concrete failure or concern
location: { file: path/to/file, lines: 10-18 }
category: correctness
severity: critical | high | medium | low
confidence: 0.0-1.0
claim: What is wrong
trigger: Conditions that expose it
impact: Resulting behavior or risk
evidence: [Relevant code-path evidence]
recommendation: Direction for addressing it
source_reviewers: [reviewer-name]
```

Permit `block` only for verified material findings. Use dispositions `block`, `address`, `investigate`, and `consider`. Use P0-P3 aliases only when requested. Final output states scope, reviewer coverage and isolation, prioritized findings, open investigations, and a terse recommendation.

- [ ] **Step 4: Write the reviewer rubrics**

Give each file `# Name`, `## Search`, `## Evidence bar`, and `## Exclude` headings. Use this exact behavioral content:

| Reviewer | Search | Evidence bar | Exclude |
| --- | --- | --- | --- |
| Adversarial | Trust boundaries, permissions, integrity, retries, partial completion, concurrency, rollback, compatibility, degraded dependencies, irreversible operations | Reachable failure, violated invariant, location, impact | Style, intent, unsupported attacks |
| General | Project rules, correctness, changed behavior, regressions, boundaries, security, performance, meaningful missing tests | Behavioral failure or explicit rule violation with location, trigger, impact | Preferences, low-confidence nits, unchanged problems not made reachable |
| Simplification | Over-engineering, needless abstraction, redundant configuration, nesting, duplication, confusing flow, clever compression, oversized changes | Complexity cost, behavior to preserve, simpler direction | Edits, patches, cosmetics, weakened used extensibility |
| Silent failure | Swallowed errors, broad catches, misleading success, defaults, exhausted retries, lost context, broken propagation, skipped cleanup | Hidden failure, suppression path, impact, visibility or propagation direction | Logging or feedback demands when handling preserves an intentional observable outcome |
| Skeptical | Hidden input/state/environment/order/ownership assumptions, inconsistent patterns, collateral changes, coupling, tradeoffs, operational fragility, regressions | Assumption or risk connected to a plausible consequence | Generic simplification unless complexity creates a design risk |

- [ ] **Step 5: Run structural validation**

```bash
/Users/scott/.codex/skills/.system/skill-creator/scripts/quick_validate.py code-quorum
test ! -e code-quorum/agents
test "$(find code-quorum/references/reviewers -type f -name '*.md' | wc -l | tr -d ' ')" = 5
rg -n 'quick|default|full|finding-v1|verified|partially-verified|unverified|rejected|block|address|investigate|consider' code-quorum/SKILL.md
git diff --check
```

Expected: validation succeeds, reviewer count is five, contract terms are present, and whitespace passes.

- [ ] **Step 6: Commit**

```bash
git add code-quorum
git commit -m "feat: add portable code quorum"
```

### Task 2: Replace the legacy suite

**Files:**
- Modify: `README.md`
- Delete: all 11 tracked `code-review/*/SKILL.md` files

**Interfaces:**
- Consumes: Task 1 names and modes.
- Produces: one repository catalog entry with no legacy triggers.

- [ ] **Step 1: Confirm the legacy inventory**

```bash
test "$(find code-review -type f -name 'SKILL.md' | wc -l | tr -d ' ')" = 11
rg -n 'code-review/' README.md
```

Expected: 11 files and existing README references.

- [ ] **Step 2: Replace the README section**

Replace `### Code Review` through the line before `### Inertia Docs` with:

```markdown
### Code Quorum

`code-quorum` runs a read-only review through independent lenses, verifies material findings, and returns one prioritized report. It reviews pending changes by default and accepts a PR, branch, revision range, commit, file set, diff, or supplied artifact.

| Mode | Reviewers |
| --- | --- |
| `quick` | General reviewer and silent-failure hunter |
| `default` | Adversarial reviewer, general reviewer, silent-failure hunter, and skeptical engineer |
| `full` | Default reviewers plus simplification reviewer |

Request a mode or named combination, such as `Run a quick code quorum` or `Use the skeptical engineer and silent-failure hunter from code-quorum`.
```

- [ ] **Step 3: Remove the old suite safely**

Run: `trash code-review`

Expected: the directory is absent and Git records 11 deletions.

- [ ] **Step 4: Verify the replacement**

```bash
test ! -e code-review
test -f code-quorum/SKILL.md
! rg -n 'code-review/' README.md
rg -n 'code-quorum|quick|default|full|skeptical engineer|silent-failure hunter|simplification reviewer' README.md
git diff --check
```

Expected: no legacy path or index entry; all new modes and named reviewers are indexed.

- [ ] **Step 5: Commit**

```bash
git add README.md code-review
git commit -m "refactor: replace code review skills with code quorum"
```

### Task 3: Forward-test behavior

**Files:**
- Modify on a failed gate only: `code-quorum/SKILL.md` or one reviewer rubric

**Interfaces:**
- Consumes: fresh workers and a disposable Git fixture.
- Produces: evidence for selection, scope fallback, read-only behavior, and verification gating.

- [ ] **Step 1: Create a disposable pending-change fixture**

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

- [ ] **Step 2: Test quick selection and pending scope in a fresh worker**

Pass this prompt with the shell's `$fixture` value interpolated: `Use code-quorum to run a quick review in $fixture. Do not change files.`

Require pending `service.py` against `HEAD`; only general and silent-failure reviewers; separate severity, verification, confidence, and disposition; unchanged fixture status.

- [ ] **Step 3: Test explicit selection in another fresh worker**

Pass this prompt with the shell's `$fixture` value interpolated: `Use the skeptical engineer and simplification reviewer from code-quorum on pending changes in $fixture. Do not change files.`

Require only those reviewers. Skeptical output addresses assumptions or design consequences. Simplification output addresses avoidable complexity without edits.

- [ ] **Step 4: Test clean-tree inference and verification gating**

Commit the fixture change. Pass this prompt with the shell's `$fixture` value interpolated: `Run the default code quorum in $fixture. No scope is specified. Do not change files.`

Require a branch-diff or recent-commit scope instead of the whole repository. Require `verified` plus source evidence for every `block` disposition.

- [ ] **Step 5: Apply the gate**

```bash
/Users/scott/.codex/skills/.system/skill-creator/scripts/quick_validate.py code-quorum
git diff --check
git status --short
```

Expected: validation and whitespace pass. If a forward test misses a required observation, stop and report that observation before changing the approved design.

- [ ] **Step 6: Commit evidence-driven corrections when present**

```bash
git add code-quorum README.md
git commit -m "fix: tighten code quorum execution rules"
```

Skip this commit when no correction was needed.

### Task 4: Final verification

**Files:**
- Verify: `code-quorum/SKILL.md`
- Verify: `code-quorum/references/reviewers/*.md`
- Verify: `README.md`

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: final proof of a valid, portable, read-only replacement.

- [ ] **Step 1: Run all static gates**

```bash
/Users/scott/.codex/skills/.system/skill-creator/scripts/quick_validate.py code-quorum
test "$(find code-quorum/references/reviewers -type f -name '*.md' | wc -l | tr -d ' ')" = 5
test ! -e code-review
test ! -e code-quorum/agents
! rg -n 'code-review/' README.md
! rg -n 'model:|tools:|subagent_type:|Task tool|Claude' code-quorum
git diff --check
```

Expected: all commands exit 0; five rubrics; no legacy suite, platform metadata, legacy index names, or platform declarations.

- [ ] **Step 2: Check completion criteria and rubric shape**

```bash
test "$(rg -c 'Complete this step' code-quorum/SKILL.md)" = 8
rg -n 'read-only' code-quorum/SKILL.md
for file in code-quorum/references/reviewers/*.md; do test "$(rg -c '^## (Search|Evidence bar|Exclude)$' "$file")" = 3 || exit 1; done
```

Expected: eight completion criteria, a read-only contract, and three required headings in every rubric.

- [ ] **Step 3: Inspect repository state**

```bash
git status --short
git log --oneline -5
```

Expected: no uncommitted implementation changes. Report pre-existing unrelated untracked files separately.
