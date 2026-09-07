# Issue or ticket tracking

## Evidence

Tickets can capture product triggers, customer requests, incident follow-ups, compliance constraints, deadlines, scope changes, and parent initiatives.

## Search

1. Fetch ticket IDs linked from commits or reviews.
2. Read descriptions, comments, status history, attachments, labels, and relationships.
3. Follow parent, duplicate, blocking, and sibling links that may contain the broader rationale.
4. Search feature names, symbols, errors, customer-facing terms, and author names across the target window.
5. Inspect project or initiative context attached to relevant tickets.

Discover search and fetch operations from the available connector rather than assuming method names.

## Strong evidence

A ticket or comment explicitly identifies the problem, decision, alternative, affected customer, incident, or external requirement and can be tied to the target change.

## Pitfalls

- ticket scope can drift after creation;
- boilerplate “why” fields may add no evidence;
- old plans may differ from the shipped implementation;
- duplicate chains can hide the canonical discussion;
- inaccessible or deleted tickets are gaps, not null results.

## Return

For each relevant ticket, provide identifier, title, link, author and dates, exact rationale text, relationships, and status at the target's ship date. Record all queries and bounded null results.

**Complete when:** every linked ticket and its rationale-bearing ancestors or duplicates have been read, and at least the target's names, symbols, and user-facing terms have been searched within the time window.
