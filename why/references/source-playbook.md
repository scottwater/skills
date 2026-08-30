# Source playbook index

After building the runtime coverage map, load only the playbooks for sources that will be searched.

| Evidence category | Playbook |
| --- | --- |
| Source control and code review | [source-control.md](sources/source-control.md) |
| Issue or ticket tracking | [issue-tracker.md](sources/issue-tracker.md) |
| Long-form documents | [documents.md](sources/documents.md) |
| Real-time team discussion | [team-chat.md](sources/team-chat.md) |
| Infrastructure observability | [observability.md](sources/observability.md) |
| Error or exception tracking | [error-tracking.md](sources/error-tracking.md) |
| Product analytics or warehouse data | [analytics-warehouse.md](sources/analytics-warehouse.md) |

For defensive code, also load [incident-context.md](sources/incident-context.md). It adds an incident-focused search angle across the available categories rather than defining another category.

Each playbook describes evidence, search strategy, pitfalls, and a completion bound. Discover connector names, authentication state, and query schemas from the runtime; do not assume a vendor or fixed tool method.
