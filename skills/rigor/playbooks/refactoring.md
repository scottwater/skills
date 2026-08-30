# Refactoring

1. **Define the preservation boundary.** Trace callers, outputs, errors, side effects, ordering, and supported edge cases. Pin them with existing tests, characterization tests, snapshots, recorded fixtures, or an equivalence harness.
   **Complete when:** “behavior preserved” is a checkable claim rather than an intention.
2. **Name the structural problem and target.** Identify the reader load, duplicated rule, invalid state, misplaced ownership, or unnecessary coupling being removed. State the target module, interface, data shape, or call graph.
   **Complete when:** the refactor has a measurable structural benefit and introduces no new product behavior.
3. **Burden.** Apply the loaded Burden rules inside the structural problem named in step 2. Leave adjacent cleanup outside the refactor.
   **Complete when:** the target satisfies the Burden reference and every deletion remains inside the preservation boundary.
4. **Move in verifiable units.** Keep the preservation check green after each unit. For coordinated internal API changes, migrate callers and remove the legacy path in the same bounded effort unless a real compatibility contract requires staging.
   **Complete when:** each unit preserves the pinned contract and leaves no accidental parallel old-and-new path.
5. **Prove equivalence.** Run the preservation harness and required repository checks. Inspect the diff for accidental behavior changes and speculative cleanup.
   **Complete when:** the before-and-after evidence covers the preservation boundary or each uncovered behavior is named.
6. **Confirm the improvement.** Compare before and after for layers, hidden state, branches, duplicated decisions, and public surface. Revert changes that only move complexity or add indirection.
   **Complete when:** the named structural burden is lower without a larger interface or hidden coordination cost.

**Done when:** behavior has fresh preservation evidence and the named structural burden is materially lower.
