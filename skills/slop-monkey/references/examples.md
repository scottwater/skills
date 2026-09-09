# Before-and-after examples

Each revision targets a diagnosed pattern while preserving the source's intended claim. A real edit must also preserve facts, uncertainty, audience, and voice.

## 1. Throat-clearing and manufactured contrast

**Before**

> Here's the thing: building products is hard. Not because the technology is complex. Because people are complex. Let that sink in.

**After**

> Building products is hard because teams bring conflicting needs, incentives, and assumptions to the work.

**Why**

The revision removes the opener and reaction cue, then replaces a broad contrast with the mechanism behind the difficulty.

## 2. Vague generalization

**Before**

> It turns out that most teams struggle with alignment. The uncomfortable truth is that nobody wants to admit they're confused. And that's okay.

**After**

> In the three project retrospectives, team members described different goals for the same release and avoided asking for clarification in planning meetings.

**Why**

The revision replaces an unsupported population claim and permission-granting ending with the available scope, behavior, and setting. If the writer lacks that evidence, they should qualify the original claim rather than invent specifics.

## 3. Jargon stack

**Before**

> Moving forward, we need to lean into this challenge and navigate the changing security landscape.

**After**

> This quarter, the security team will replace shared credentials and require hardware keys for administrators.

**Why**

A time bound, actor, and actions replace vague motion and business shorthand.

## 4. Dramatic fragmentation

**Before**

> Speed. Quality. Cost. You can only pick two. That's it. That's the trade-off.

**After**

> The six-week deadline forces the team to cut scope or accept a higher defect rate; the budget cannot cover more engineers.

**Why**

The revision names the actual constraints instead of presenting a familiar slogan as a universal law.

## 5. Rhetorical setup

**Before**

> What if the best teams don't optimize for productivity? Here's what I mean: they optimize for learning. Think about it.

**After**

> The team measures how quickly an experiment resolves a product question, rather than counting tickets closed.

**Why**

The revision removes the staged reveal and makes “learning” observable.

## 6. Hidden actor

**Before**

> After the data was reviewed, the decision emerged to pause the launch.

**After**

> After reviewing the failed load test, the release manager paused the launch.

**Why**

The actor, evidence, and action make responsibility and causality visible.

## 7. Overcorrection

**Before**

> The samples were stored at 4°C and analyzed by an independent laboratory.

**Bad revision**

> A technician stored the samples at 4°C, and an independent laboratory analyzed them.

**Better decision**

> Keep the original unless the technician's identity matters.

**Why**

The passive construction keeps attention on the samples and conditions. Surface rules should not override the genre's information priorities.

## 8. Clean but generic agent-speak

**Before**

> The implementation introduces a robust caching mechanism that enhances performance while ensuring data consistency. Additionally, comprehensive error handling provides a seamless experience in failure scenarios.

**After**

> The client now keeps successful responses for five minutes, cutting repeated requests during page navigation. Failed requests bypass the cache, so a temporary outage cannot leave users with a stored error.

**Why**

The revision replaces praise with behavior, timing, and a failure guarantee. A reader can now evaluate what the change does instead of accepting the writer's description of how it feels.

## 9. Polite but distant answer

**Before**

> Great question! There are several factors to consider. Both approaches offer meaningful benefits, and the optimal choice ultimately depends on your specific requirements. I hope this helps!

**After**

> Keep the existing queue. Your workload is small, and the migration would add another service without fixing a measured problem. Reconsider it if queue latency reaches the 500 ms limit.

**Why**

The revision answers the decision, gives the evidence and trade-off, and names the condition that would change the recommendation. It sounds human because it exercises judgment, not because it adds casual language.

## 10. Over-structured short response

**Before**

> ## Summary
>
> The deployment failed because the token expired.
>
> ## Root cause
>
> The authentication token had exceeded its validity period.
>
> ## Next steps
>
> Generate a new token and deploy again.

**After**

> The deployment token expired. Generate a new one, then rerun the deployment.

**Why**

The headings repeat information that fits in two sentences. The revision follows the reader's task: explain the failure and say what to do next.
