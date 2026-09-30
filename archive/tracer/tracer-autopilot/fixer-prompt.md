# Consolidated repair prompt

Use the shared [repair prompt](../tracer-implement/fixer-prompt.md) at most once for the delivery's accepted findings, preferably in the existing implementation context. Pass the original scope and safety limits, controller dispositions, actual report paths, repair starting SHA, and agreed focused checks.

Save `.tracer/implement/repair-report.md`. Recheck corrections only if code changed. Any unresolved material finding after the repair/recheck is Blocked; routine continuation does not authorize another repair or review cycle.
