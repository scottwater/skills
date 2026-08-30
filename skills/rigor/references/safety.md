# Change safely

- **Design retry behavior.** Give state-mutating operations an explicit duplicate and partial-run contract. Use idempotence, idempotency keys, transactional boundaries, or clearly non-retryable semantics as the operation requires.
- **Separate shared writers first.** Give concurrent workers separate files, branches, worktrees, keys, or ownership boundaries. Serialize only when one shared target is a real invariant.
- **Converge migrations.** For coordinated internal APIs, inventory callers, migrate them, and remove the old path in the same bounded effort. Preserve compatibility for an actual external or staged migration contract, and time-box transitional code.
- **Encode recurring lessons.** When a failure or instruction recurs, prefer a test, type, lint, check, or tool that makes the desired behavior structural. Keep judgment-heavy guidance as prose with a concrete failure example.

**Complete when:** retries have declared semantics, each shared mutable target has either an isolated owner or an explicit serialization boundary, migrations name their convergence and compatibility boundaries, and recurring failures have either a structural prevention or an explicit reason they still require judgment.
