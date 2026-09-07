# Incident context

Use this cross-cutting angle when the target contains retries, timeouts, guards, limits, fallbacks, circuit breaking, resource protection, or other defensive behavior.

Across every available source, search for:

- incident and postmortem identifiers near the target's history;
- the feature, service, symbol, error text, and changed constant;
- incident labels, reliability follow-ups, reversions, and emergency changes;
- monitor, error, and product-event changes around the ship window;
- action items that link directly to the target review or commit.

Fetch complete incident timelines and postmortems. Preserve the distinction between the trigger, contributing conditions, remediation, and later preventive work. Several sources may describe different phases of the same incident.

Corroboration across source categories strengthens a claim only when identifiers, dates, or quoted links show that the records concern the same event. Similar timing alone remains inference.

Return incident identifiers, chronology, decisive quotations, linked changes, action items, and any mismatch between the documented fix and the code that shipped.

**Complete when:** incident terms and target identifiers have been searched across every accessible category, and each discovered incident has been followed through its linked action items and changes.
