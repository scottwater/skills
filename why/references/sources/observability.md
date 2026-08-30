# Infrastructure observability

## Evidence

Metrics, monitors, dashboards, logs, traces, incident records, and operational notebooks show runtime conditions near a change. They can support why a timeout, retry, limit, or defensive path appeared.

## Search

1. Identify the owning service and its upstream and downstream dependencies.
2. Search monitors, dashboards, and incidents by service, feature, symbol, and error text.
3. Inspect metric definitions and thresholds matching constants in the code.
4. Query a bounded window around the target change for trends, spikes, and recoveries.
5. Search logs and traces with service, environment, and time filters before sampling events.
6. Record monitor and dashboard creation dates when they bear on chronology.

Discover query operations and retention limits from the connector. Prefer aggregate evidence before raw high-volume events.

## Strong evidence

An incident or operational note explicitly links the runtime condition to the change. Matching thresholds and pre-change spikes provide supported or inferred evidence when paired with source history.

## Pitfalls

- temporal correlation does not establish causation;
- dashboards reflect an author's framing;
- renamed or expired telemetry creates a gap rather than a null result;
- common log strings create noisy false matches;
- instrumentation may have changed at the same time as behavior.

## Return

For each relevant item, give type, stable identifier, owner and dates, exact query or condition, bounded numerical summary, and the strength of its connection to the target.

**Complete when:** the owning service's available incidents, monitors, relevant metrics, and bounded logs or traces have been searched for the target window or marked unavailable.
