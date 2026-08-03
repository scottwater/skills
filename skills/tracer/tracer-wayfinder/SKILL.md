---
name: tracer-wayfinder
description: Plan an effort too large and foggy for one agent session as a shared map of decision tickets, then resolve them one at a time until the route to a spec is clear.
disable-model-invocation: true
---

# Wayfinder

Use this for a loose idea that is too large for one agent session and whose route is still unclear. Wayfinding names the **destination**, charts a **map** on the repo's issue tracker, and works its **decision tickets** — questions whose resolution is a decision, not slices of a build to execute — until the route is clear.

This is a situational on-ramp to the tracer flow, not its default entry. A feature whose decisions fit in one session belongs in `/tracer-interview-me` instead.

## Plan, don't do

Wayfinder plans. Its destination is a spec-ready set of decisions, and each decision ticket ends in an answer. The map is complete when nothing remains to decide before someone builds the work.

The urge to start building means you have reached the destination. Hand the cleared map to `/tracer-to-spec`; never send a multi-session map directly to `/tracer-implement`, which would skip the step that collapses its distributed detail.

## Refer by name

Every map and ticket has a title. In narration and in **Decisions so far**, refer to an issue by its linked name, never by a bare id, number, path, or slug. Identifiers still appear inside links; they do not stand in for names.

## The map

The map is one issue labelled `wayfinder:map`, or the local equivalent documented by the tracker. Its decision tickets are children of that map.

The map is an **index, not a store**. A decision lives in exactly one place — its ticket's resolution — and the map carries only a one-line gist and link. Open tickets are discovered through the tracker's child/frontier query, not copied into the map body.

Read `docs/agents/issue-tracker.md` for this repo's **Wayfinding operations**: map creation, child linkage, blocking, frontier queries, claiming, resolution, and index updates. If that file exists but lacks those operations, run `/tracer-setup` to update it before charting. If no tracker is configured, use the local `.tracer/` convention from `/tracer-setup`. Before creating local state, run `git check-ignore -q .tracer`; if it is not ignored, add `/.tracer/` to the repository's root `.gitignore`.

### Map body

```markdown
## Destination

<One or two lines describing the spec-ready body of decisions this map must produce.>

## Notes

<Domain, skills each session should consult, and standing preferences for this effort.>

## Decisions so far

<!-- One line per resolved ticket: enough to judge relevance, with the linked ticket holding the detail. -->

- [<resolved ticket title>](link) — <one-line gist of the answer>

## Not yet specified

<!-- In-scope fog that cannot yet be phrased as a precise question. -->

## Out of scope

<!-- Work consciously ruled beyond this destination. It never graduates. -->
```

### Decision tickets

Each decision ticket is a child of the map, sized to fit one fresh agent session:

```markdown
## Question

<The decision or investigation this ticket resolves.>
```

Each carries one type label: `wayfinder:research`, `wayfinder:prototype`, `wayfinder:interview`, or `wayfinder:task` (or the local tracker's equivalent field).

The map coordinator claims a ticket **before any work** using the configured tracker's assignment or status operation. A named ticket must belong to this map and be open, unblocked, and either unclaimed or already allocated to this worker; otherwise stop. Blocking uses the tracker's native relationship where available. The **frontier** is the map's open, unblocked, unclaimed children.

Do not let workers race a frontier query and claim. One coordinator allocates distinct tickets before parallel sessions start. Record answers as resolution comments or the local equivalent. Assets are linked from the ticket, never pasted into the map.

## Ticket types

Every ticket is either **HITL** — worked live with the human, who speaks for their side — or **AFK** — driven by an agent alone. An agent never answers the human side of a HITL ticket.

- **Research** (AFK): answer a question that needs a source-backed note rather than a simple repository lookup. Run one background worker with `/tracer-research`; the worker researches directly and returns one cited note. Link that note from the ticket.
- **Prototype** (HITL): create a cheap, rough artifact to react to when the question is how something should look or behave. Use a fresh `/tracer-prototype` session, bridged with `/tracer-handoff`, and link the throwaway branch or commit from the ticket. The answer is the decision the prototype exposed, not production code.
- **Interview** (HITL): the default. Use `/tracer-interview-me`'s discipline, scoped to this one ticket: ask each round's whole answerable frontier with recommended answers, delegate factual lookups, and leave decisions to the human. Do not follow that skill's normal `/tracer-to-spec` handoff while this ticket remains part of a map. Apply `/tracer-domain-modeling` as terms and durable decisions settle.
- **Task** (HITL or AFK): manual work required before a decision can be made — provisioning access, signing up for a service, or moving sample data so its shape can be inspected. It earns its place only by unblocking a decision, not by delivering the destination. Resolve it with what was done and the resulting facts later tickets need.

## Fog of war

The map is deliberately incomplete. **Not yet specified** holds in-scope questions you can see coming but cannot phrase precisely yet. Resolving tickets pushes the frontier outward and may make that fog precise enough to graduate into new decision tickets.

The test is sharpness, not answerability:

- Create a **ticket** when you can state its question precisely now, even if another ticket blocks it.
- Keep **fog** when you cannot yet state the question precisely. Do not pre-slice it; one fog patch may later become several tickets or none.

Remove a fog entry as soon as it graduates so the question lives in one place only.

## Out of scope

Fog lies toward the destination. Work beyond it belongs in **Out of scope**, never in **Not yet specified**, and never graduates.

If an existing ticket turns out to lie beyond the destination, close it without treating it as a route decision. Add one linked line to **Out of scope** explaining why. Do not add it to **Decisions so far**.

## Session and concurrency invariants

No ticket worker answers more than one decision ticket. Exactly one **map coordinator** at a time owns frontier allocation and map-body writes for a map. Parallel ticket workers update only their assigned child ticket and return a map delta; the coordinator applies those deltas serially.

A charting session creates and wires the map. It may dispatch several AFK research workers in parallel, one pre-claimed ticket per worker, then record their returned answers. This is concurrency across worker sessions, not several questions in one worker's context.

If a worker disappears, its ticket stays claimed. The coordinator may release or reassign it only after confirming that the session is no longer active; ask the human when that cannot be established. Never run two un-ticketed coordinator sessions against the same map.

## Invocation

### Chart the map

The user invokes `/tracer-wayfinder` with a loose idea.

1. **Name the destination.** Run a destination-scoped interview using tracer's frontier-round discipline and `/tracer-domain-modeling`: settle what this map is finding its way to before creating tickets. The destination fixes scope.
2. **Map breadth-first.** Continue across the whole space rather than diving down one thread. Surface precise decisions that can be ticketed now, their blocking relationships, and coarse fog beyond them. Unlike a normal `/tracer-interview-me`, stop at the ticketable questions — do not resolve the whole tree in this session. If no fog appears and the route already fits one session, stop before creating a map and ask whether to continue with `/tracer-interview-me` instead.
3. **Create the map.** Fill Destination and Notes, leave Decisions-so-far empty, and sketch the remaining fog under Not yet specified.
4. **Create then wire.** Create every decision ticket whose question is precise now as a child of the map. In a second pass, add blocking edges after all tickets have identities. Leave everything still imprecise in Not yet specified.
5. **Dispatch frontier research.** Query the new frontier and claim each unblocked research ticket before dispatch. Launch one worker per ticket with `/tracer-research`, passing the low-resolution map, full Question, and capture branch explicitly; use isolated worktrees for persisted branch artifacts. Each worker researches directly, writes one cited note on a unique `research/<map-slug>/<ticket-slug>` branch, and returns its answer, context pointer, and `## Map delta` without editing the map. Never run concurrent branch checkouts in one worktree. If background workers or isolation are unavailable, leave the tickets open for fresh AFK sessions.
6. **Record returned research serially.** For each completed worker, the coordinator posts the answer, asset pointer, and Map delta on its child ticket, closes it, then applies that delta using the same index/fog/scope/new-ticket rules as work-through step 5. With a local `.tracer/` map, only the coordinator touches map or ticket files because isolated worktrees cannot see git-ignored state. If research outlives this session, the next coordinator records and applies the completed outputs before allocating new work.
7. Stop. Charting answers no HITL ticket.

### Work through the map

The user invokes `/tracer-wayfinder` with a map URL, number, or local path. Naming a ticket is optional.

1. **Load the low-resolution map** and orient to its Destination and Notes. In coordinator mode, compare every resolved child with Decisions so far and Out of scope; reconcile missing entries before allocating work.
2. **Validate and choose one ticket.** A user-named ticket must belong to this map and be open, unblocked, and unclaimed, unless the coordinator already allocated it to this worker. Otherwise stop and report why. Without a named ticket, the coordinator takes the first frontier ticket and claims it before deeper reading or discussion.
3. **Resolve it.** Zoom into related tickets and assets only as needed. Follow the skills named in Notes. Default to the ticket-scoped interview and domain-modeling discipline above.
4. **Record the child resolution.** Produce the answer and a `## Map delta` describing the exact index, fog, scope, and new-ticket changes it implies. On a shared tracker, the worker posts both and closes the child. For a local `.tracer/` map, the worker returns both and the coordinator records them in the coordinating checkout. A parallel ticket worker stops here; it never edits the map body.
5. **Advance the map as coordinator.** Apply completed deltas one at a time. Append each linked gist to Decisions so far, create-then-wire newly precise tickets, remove graduated fog, move beyond-destination work to Out of scope, and update invalidated tickets or rule them out of scope so every closed child remains accounted for. Ticket workers never replace the map body.
6. **Check completion.** Re-query every child and verify that each resolved child appears in Decisions so far or Out of scope. The map is clear only when no open, claimed, or in-flight decision tickets remain, no resolved child is unindexed, and Not yet specified is empty. Then hand off with: `Invoke /tracer-to-spec with the cleared map <URL-or-path>.`

Run only one coordinator session per map. To work frontier tickets in parallel, have that coordinator claim distinct tickets first, launch or hand off named worker sessions, then apply their returned deltas serially.
