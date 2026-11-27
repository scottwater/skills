---
name: review-loop
description: Review a change in a loop with a report-only reviewer from a model family that did not write it, Neon first, until both agents agree. Use when asked to review code, a diff, branch, or PR, or when another skill asks for a review loop.
---

# review-loop

This is a workflow for making code changes more correct before (or sometimes
after) filing a pull request: a second model reviews the change in a loop until
you both agree.

Make the most minimal possible changes to appease the reviewer. Be careful of
scope creep and don't be scared to push back.

## Roles

- **Reviewer**: the first model family in step 2's order that did not write
  the change, at `high` reasoning effort. The reviewer only reports.
- **Fixer**: you, by default. When the calling skill names an `implement`
  thread as the fixer, you still verify every finding, but the thread makes
  each fix: send it your verified findings as the `implement` skill's
  **Send follow-up work** section describes, and wait for its commits.

## Budget

- Default: 3 rounds total. Round 1 is full. Later rounds check only
  changed code and open findings.
- Extend to 5 only for security, permissions, auth, data loss, or
  state/concurrency, while a blocker or should stays open with evidence. Or when
  the user asks.
- Stop early if a round returns only nits. Declined nits and comment,
  doc, or format-only fixes need no new round.
- One reviewer only. The reviewer must not start subagents or reviewers.
- Keep a ledger: id, severity, outcome, usage if returned. Never guess it.

## 1. Scope

Use the scope the calling skill names, such as a commit range. Otherwise run
`git status --short`. Do not stash, discard, or include unrelated
changes. Limit review to the change paths if they separate cleanly.
Otherwise stop and ask.

Find the base after `git fetch origin`:

- PR: `gh pr view <n> --json baseRefName,headRefOid`. Check out the branch
  only if clean. Confirm `HEAD` is the PR head, or ahead only by this
  change. Base: `git merge-base HEAD origin/<baseRefName>`.
- Local: `git merge-base HEAD origin/<default-branch>`. No remote: a base
  the user names, or `HEAD` for uncommitted changes only.

The change is base to working tree in those paths, with untracked files.
Use one diff command all rounds. State intent and out-of-scope in 1-2
sentences. Run covering checks and ensure you have **observed proof** that the
change actually works on its real path (run the reproduction, CLI, endpoint, or
app/UI — not just static checks or mocked tests). If observed proof already
covers the current behavior diff (from an `implement` worker or earlier in this
session), reuse it instead of re-running; otherwise exercise the change before
starting Round 1. Do not send code this change breaks or unverified behavior to
review. Note missing checks or verification limits in the brief.

## 2. Start the reviewer

### Pick the reviewer

The **authors** are every model family that wrote part of the change: you
when you edited it, an `implement` worker, any subagent that wrote code. The
fixer counts too, since its fixes join the change. For work you did not see
written, such as a PR or an earlier session, read the commits'
`Co-Authored-By` trailers and the PR body.

No family reviews its own code, whatever the version: Opus 5.4 does not
review Opus 5.5's work. The reviewer is the first family in this order that
is not an author and resolves at `high`:

| Order | Family | Native driver |
| --- | --- | --- |
| 1 | Gemini Neon | `antigravity` |
| 2 | Claude Opus | `claudeAgent` |
| 3 | Muse Wonder Full | `muse` |
| 4 | GPT Sol | `codex` |

Use the newest version of that family the live catalog lists, at `high`.
When a family has no runnable instance at `high`, take the next one and note
the skip for the report. When every family is an author or unavailable, tell
the user and stop.

The user can override any of this at any time: name the reviewer, version,
or effort, reorder the list, or let an author review. A calling skill passes
the user's choice through. A reviewer the user names is exact: when it is
unavailable, report the blocker instead of taking the next family.

Keep the same reviewer for every round.

### Delegate the review

In T3, call `orchestrator_capabilities` and resolve the reviewer to an exact
`providerInstanceId`, model `id`, and the reasoning-effort option the catalog
lists for it. Prefer the family's native driver over a proxy such as Pi, and
an instance with `canRunChildTask: true`. Use `delegate_task` every round
(`role: "review"`, `mode: "async"`). Save `taskId`. New `clientRequestId`
per round. `childThreadId` is storage, not the next target. Do not use
`t3_thread_send`, `create_threads`, or `t3_thread_launch` for review.

If T3 tools are not listed, try one direct capability call. Outside T3, use
a native subagent and keep its ID; it reaches only your own provider's
models, so apply the same order to those.

Do not edit scoped files while review runs. Wait for the notice. Do not
poll or start a second reviewer. Timeout, error, or no reply is not
approval. On failure, cancel, verify stop, restart with the ledger.

Round 1 brief (T3 children get no history):

```
Review only. Do not edit, commit, push, comment on PRs, or start subagents.
Repo: <abs path> Base: <sha> Intent: <intent> Out of scope: <scope> Checks: <results> Proof: <what was run and observed>
See: git diff <base> [-- <paths>]; git status --short (read untracked).
Read surrounding code. Find bugs, broken callers, mismatch with intent.
Skip style unless it hides a bug. Hold to the smallest change. Flag code,
tests, or guards the intent does not need. Other paths, rare cases, small
perf, extra compat: nits.
blocker = intended case wrong. should = real bug callers will hit, in intent. nit = rest.
Reply:
VERDICT: APPROVE or CHANGES
S1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion> (stable ids)
```

## 3. Answer findings

Check each finding and severity yourself against the code, a test, or a
non-mutating reproduction. Another path, rare case, or small cost is a nit,
whatever label it came with.

- Agree: smallest fix. Prefer delete or narrow over new lock, cache,
  helper, or option. Fix the case that happened. Add one focused test
  that fails without the fix, if intent needs it.
- Disagree: say why, with evidence (file:line, test, output).
- Out of scope or nit: decline in one line. List as follow-up.

When the fixer is an `implement` thread, send it the agreed findings, each
with its location, failure scenario, and suggested fix, and confirm each fix
against the code once it commits.

Update the ledger. Re-run checks, re-verify any behavior a fix touched, and run
`git diff --shortstat <base>`. If review grew the diff, cut first. Do not agree
just to end the loop.

## 4. Next round

Start one only if budget remains and a blocker or should is open, behavior code
changed, or approval does not cover the current behavior diff. Use a fresh
`delegate_task` in T3, or follow up the saved native ID. Send the round 1 brief,
the ledger (`fixed:` / `disagree:` / `declined:` + evidence), the same base
diff, and the change since last round. Tell the reviewer: open ids and changed
code only. Mark each old id `resolved` or `still open: <reason>`.

## 5. Stop and ship

Agreed: APPROVE on the current behavior diff, no blocker or should open,
no concern of your own. Stuck: an item stays disputed after two replies,
or budget ends. Show both sides in 2-3 lines each. The user decides.
Budget end is not approval.

Do not push during the loop. Push after agreement only if the user asked
to push, ship, or update the PR. If you push to a PR, add above the model
blurb:

`Reviewed with review-loop: <N> rounds with <model> on <effort>. Verdict: approved`.

Drop `on <effort>` unless verified.

Report: rounds, reviewer model and effort, families skipped and why, what the
review changed, diff size before/after, fixed and declined findings with
reasons, usage if exposed (else say not), pushed or not.
