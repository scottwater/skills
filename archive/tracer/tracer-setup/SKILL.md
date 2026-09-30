---
name: tracer-setup
description: Configure a repo for the tracer skills — set up its issue tracker and domain doc layout. Run once before first use; everything falls back to local files if you skip it.
disable-model-invocation: true
---

# Setup Tracer

Scaffold the per-repo configuration the tracer skills read:

- **Issue tracker** — where `/tracer-wayfinder` charts decision maps, `/tracer-to-spec` and `/tracer-to-tickets` publish, and `/tracer-code-review` fetches specs from (GitHub, GitLab, local markdown, or a workflow you describe)
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

Skipping setup is fine: every skill falls back to local markdown under `.tracer/`. Run this when you want a real tracker, or to make the conventions explicit for other agents working in the repo.

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Read whatever exists; don't assume:

- `git remote -v` — GitHub? GitLab? No remote?
- `CLAUDE.md` / `AGENTS.md` at the repo root — does either exist? Already an `## Agent skills` section?
- `docs/agents/` — does this skill's prior output already exist?
- `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/` — existing domain docs
- `.tracer/` — sign the local-markdown convention is already in use
- Monorepo signals — `pnpm-workspace.yaml`, a `workspaces` field, a populated `packages/*` with its own `src/`. Absence means single-context, which is almost every repo.

### 2. Present findings and ask

Lead each section with the recommended answer so the user can accept it in a word.

**Section A — Issue tracker.** If the remote points at GitHub, propose GitHub; GitLab host, propose GitLab; otherwise propose local markdown. The options:

- **GitHub** — issues in GitHub Issues (`gh` CLI) → seed from [issue-tracker-github.md](./issue-tracker-github.md)
- **GitLab** — issues in GitLab Issues (`glab` CLI) → seed from [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)
- **Local markdown** — files under `.tracer/` (projects with no remote) → seed from [issue-tracker-local.md](./issue-tracker-local.md)
- **Other** (Jira, Linear, …) — ask the user to describe the workflow in one paragraph; write `docs/agents/issue-tracker.md` from scratch around it. It must answer how to create and fetch an implementation ticket, express a blocking edge, and mark a ticket agent-ready. It must also include **Wayfinding operations**: create/update a map, create and parent a decision ticket, query the map-scoped frontier, let one coordinator claim tickets before parallel dispatch, let workers resolve only their child ticket, and let the coordinator apply map-index updates serially.

**Section B — Domain docs.** Default to **single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root; write it without asking. Offer **multi-context** (a root `CONTEXT-MAP.md` pointing at per-context `CONTEXT.md` files) only when exploration found monorepo signals. Seed from [domain.md](./domain.md).

### 3. Confirm and write

Show the user drafts of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and the `## Agent skills` block below; let them edit before writing. When updating an existing tracker doc, preserve user customizations and add or refresh its **Wayfinding operations** rather than replacing the whole file. If the user chose local markdown, verify `.tracer/` is ignored and add `/.tracer/` to the root `.gitignore` when needed.

**Pick the file for the block:** edit `CLAUDE.md` if it exists, else `AGENTS.md`; if neither exists, ask which to create. Never create one when the other already exists. If an `## Agent skills` block already exists, update it in place.

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Domain docs

[one-line summary — "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

### 4. Done

Tell the user which skills now read these files (`/tracer-wayfinder`, `/tracer-to-spec`, `/tracer-to-tickets`, `/tracer-code-review`, `/tracer-implement`; all skills for domain docs) and that editing `docs/agents/*.md` directly is the normal way to adjust later. Re-run this skill when switching trackers or when an older tracker doc needs the Wayfinding operations added.
