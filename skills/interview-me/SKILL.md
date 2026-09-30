---
name: interview-me
description: A relentless interview that asks every frontier question at once, round by round, until you and the user reach a shared understanding.
disable-model-invocation: true
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask *now* without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

Go deep. Follow each branch until it bottoms out; a vague answer is a new question, not a settled decision. Stay on the topic the user brought — don't drift into adjacent work or start solving.

Finding *facts* is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch one fresh exploration sub-agent to find it — don't ask the user for anything you could look up yourself. That explorer owns the lookup; its returned evidence satisfies this fact-finding step. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the rest of the frontier now. The *decisions* are the user's — put each to them and wait.

The interview writes nothing. The design tree lives in the conversation, and the output is the shared understanding itself.

## Done

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Summarize the settled tree and ask the user to confirm it. Do not act on it until the user confirms you have reached a shared understanding.
