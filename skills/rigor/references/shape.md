# Shape the system

- **Model the domain.** Name the data shape and its invariants before writing branching logic. Prefer a state machine, discriminated model, table, reducer, registry, or appropriate collection when it removes scattered rules or invalid states. Keep local code when no structure earns its cost.
- **Validate at boundaries.** Convert external input into trusted domain values where it enters. Keep business logic focused. Internal assertions remain appropriate where types cannot establish an invariant.
- **Use types as proof.** Make illegal states hard to represent, distinguish semantic values that should not be interchangeable, exhaust known variants, and replace uncertainty with validation or narrowing instead of a cast.
- **Redesign only when foundational.** When a requirement invalidates an existing assumption, design as though it had existed from the start. When an established extension point fits, use it.

**Complete when:** every changed shape has an owner and invariant, and every new abstraction removes a demonstrated branch, invalid state, leak, or duplicated rule.
