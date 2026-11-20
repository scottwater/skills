---
name: council
description: Review work with a four-provider council (Opus, Sol, Muse, Neon) through T3 Code, looping until every member is satisfied. Use when the user says council.
---

# Council

The **council** is four delegates from four providers, run through T3 Code. Each **round**, every member reviews the same work and scores it. You verify their findings, fix the ones you accept, and run another round until every present member is satisfied, for at most seven rounds. The council needs a **quorum** of three members to carry on.

## 1. Prepare the work

Address outstanding PR comments, fix known issues, and run the relevant checks before the first round. The council reviews the implementation you would ship, not one with fixes still pending. When the user wants to discard the implementation and explore new ideas, skip fixes to code being replaced.

**Complete when:** no known issue is waiting on the review, and you can state the scope, the intent, and the check results.

## 2. Seat the council

| Member | Native driver |
| --- | --- |
| Claude Opus 5.5 | `claudeAgent` |
| GPT Sol 6.1 | `codex` |
| Muse Wonder Full | `muse` |
| Gemini 4 Neon | `antigravity` |

Every member runs at `high` reasoning effort. When the user names other members or another effort, use those.

Call `orchestrator_capabilities` and resolve each member to an exact `providerInstanceId` and model `id` in the live catalog. Pick the native driver over a proxy such as Pi, and only an instance with `canRunChildTask: true`. Set the effort with the reasoning-effort option id and value the catalog lists for that model.

The council runs only through T3 delegation. When the T3 tools are missing, tell the user and stop. Never substitute a model or fall back to native subagents.

### Quorum

A member is **absent** when it cannot resolve at the requested effort, or when its review is missing from a round (see step 3). With three or four members present, carry on and name any absent member in your round summary and score table. With fewer than three, tell the user who is absent and why, and stop. The user can override the quorum either way: approve a smaller council, or require all four members.

**Complete when:** each present member has a `providerInstanceId`, a model `id`, and an effort option, and the quorum holds or the user has overridden it.

## 3. Run a round

Start every seated member in parallel, one `delegate_task` each, including a member absent from the previous round:

- `target`: the resolved `providerInstanceId`, `model`, and effort option
- `role`: `"review"`
- `runtimeMode`: `"inherit"` and `interactionMode`: `"inherit"`
- `mode`: `"async"`
- `title`: `Council: <short scope> (<member>)`
- `clientRequestId`: unique to this round and member, reused on retries of it
- `task`: the brief below

Members start with no conversation history, so the brief carries everything:

```text
Review only. Do not edit, commit, push, comment on PRs, or start subagents.

Repository: <absolute path>
Scope: <exact diff command, range, PR, or file list>
Intent: <what the change should do, in one or two sentences>
Out of scope: <what this change deliberately leaves alone>
Checks: <commands run and their results>

Read the surrounding code. Find bugs, broken callers, and gaps against the intent.
Skip style unless it hides a bug.

Rank findings most severe first. For each, give path:line, the problem, a
concrete failure scenario, and a fix.
End with: SCORE: <n>/10
```

For feedback on something other than code, keep the first line and replace the review instructions with the user's question.

From round 2 on, append the prior findings, what you changed, and the objections you still hold. Start every round with fresh `delegate_task` calls. Never continue a member through `t3_thread_send` on its `childThreadId`.

Retain each `taskId` with its member, then end your turn. Each completion wakes this thread. A task that ends `failed`, `cancelled`, or `interrupted`, or returns no review, is a missing review: report it and retry once under a new `clientRequestId`. A member whose retry also fails is absent for the round; apply the **quorum**. A missing review is never approval.

**Complete when:** every member has a usable review or is recorded absent, and the quorum holds.

## 4. Weigh the findings

Check every finding against the code yourself. Accept it only when the source, a test, or a reproduction confirms it. Summarize the accepted findings, where members disagree, and the next steps.

Fix each accepted finding with the smallest change that covers the intended case, re-run the checks, and start the next round.

Guard against scope creep: review loops grow a change one cheap-looking fix at a time. Decline findings outside the intent in one line each, and list them as follow-ups.

**Complete when:** every present member is satisfied with the current change.

### When the council circles

Each round should bring the council closer to consensus. Before starting another round, check whether it is **circling** instead:

- A disagreement between members survives two rounds.
- A finding you fixed or declined comes back.
- One member's fix undoes another's, or a fix reverts an earlier one.
- Scores hold flat or drop across two rounds while new findings keep arriving.
- Round 7 ends without consensus. Seven rounds is the cap, however close the last one looked.

When the council circles, stop running rounds and ask the user for help. Show where it stalled: each side of the disagreement in two or three lines, what you have tried, and the decision you need from the user. Resume only on their call.

## 5. Record the scores

Keep each member's score for every round. When a member gives no score, write `no score`; when it was absent, write `absent`.

When the work ends in a pull request, add this section to the PR description, at the end of the collapsed `<details>` block (or just before the closing model and harness line when there is no block). Edit the description of an open PR rather than posting a comment. Without a PR, put the table in your final reply.

```markdown
## Council review

Rounds: 2

| Member | Round 1 | Round 2 |
| --- | --- | --- |
| Claude Opus 5.5 | 7/10 | 9/10 |
| GPT Sol 6.1 | 8/10 | 10/10 |
| Muse Wonder Full | 7/10 | 9/10 |
| Gemini 4 Neon | absent | 9/10 |
```

**Complete when:** the table lists every round and member, and sits in the PR description or the final reply.
