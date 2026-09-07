# Error or exception tracking

## Evidence

Grouped issues, individual events, stack traces, release correlations, affected versions, user context, and engineer comments can reveal the failures that motivated corrective code.

## Search

1. Identify the organization, project, service, and release naming scheme.
2. Search by exception class, message, function, file, feature term, and linked issue URL.
3. Inspect first-seen, last-seen, frequency, environment, affected release, tags, and representative events.
4. Compare the event window with the target's merge and deployment dates.
5. Check for regrouped or renamed issues after an apparent resolution.
6. Read human comments and resolution notes separately from generated analyses.

Use the runtime's connector schema and read-only operations. Treat generated root-cause summaries as hypotheses until event data or human evidence supports them.

## Strong evidence

A stack reaches the target and an attributed comment or review links the issue to the change. An error stopping after a release supports correlation but does not identify which commit fixed it without additional evidence.

## Pitfalls

- grouping can change after refactors;
- one release contains many changes;
- “resolved” may be a manual status;
- upstream changes can stop an error without the target change;
- sampling distorts event counts;
- generated analyses can overstate causation.

## Return

Give issue identifier and link, project, timestamps, counts and sampling when known, releases, representative stack excerpt, author comments, and the exact temporal relationship to the change.

**Complete when:** target symbols, errors, and affected release windows have been searched, representative events for each candidate have been inspected, and grouping or sampling gaps are named.
