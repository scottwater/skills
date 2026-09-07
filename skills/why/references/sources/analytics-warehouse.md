# Product analytics and warehouse data

## Evidence

Product events, experiments, feature exposures, usage or billing records, data-pipeline lineage, query history, and warehouse telemetry can show user behavior or data distributions near a decision.

## Search

1. Discover catalogs, schemas, tables, and retention before assuming names.
2. Prefer documented, typed, deduplicated datasets over raw events when their lineage and refresh lag fit the question.
3. Bound every query by the target window and partition keys.
4. Inspect distributions, counts, first and last seen, and variant exposure rather than dumping rows.
5. Check instrumentation and schema changes before interpreting a trend as behavior change.
6. Follow data lineage back to version-controlled transformations as a cross-source lead.

Use only read-only query operations. Record the exact query and fully qualified objects from the actual environment; the skill defines no fixed warehouse, schema, table, event, or column names.

## Strong evidence

A documented experiment decision or analysis explicitly ties data to the change. A matching threshold distribution, launch ramp, or post-change decline can support an inference when chronology and instrumentation are verified.

## Pitfalls

- instrumentation can create a step change without behavior changing;
- schemas and event properties drift;
- refresh lag can omit recent data;
- retention limits create gaps;
- product correlation cannot establish author intent alone;
- exploratory notebooks may be inaccessible to the query connector.

## Return

Provide dataset names, exact read-only queries, time window, compact numerical summary, instrumentation checks, temporal relation to the target, and confidence in the connection.

**Complete when:** relevant datasets were discovered rather than guessed, the target window was queried with reproducible SQL or equivalent, and retention, refresh, schema, and instrumentation limits are documented.
