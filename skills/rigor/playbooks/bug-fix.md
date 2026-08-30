# Bug fix

1. **Establish the symptom.** Reproduce it on the reported surface when practical. Otherwise capture the strongest available failing artifact, trace, log, test, or state transition and name why direct reproduction is unavailable.
   **Complete when:** there is a stable observation that distinguishes broken from working behavior.
2. **Root cause.** Apply the loaded Evidence rules while tracing the affected path. Use history when a regression boundary or old constraint matters.
   **Complete when:** one supported mechanism explains the observation and every credible alternative is eliminated or remains explicitly unresolved.
3. **Stop for diagnosis-only work.** Report the symptom, confirmed or best-supported root cause, evidence, impact, and the smallest fix direction. Keep product code unchanged.
   **Complete when:** the diagnosis distinguishes confirmed evidence from remaining hypotheses and names what would settle every material gap.
4. **Fix the cause.** For diagnose-and-fix work, create a practical regression check when one is missing, then make the smallest coherent change that removes the mechanism. Leave unrelated hardening outside the task.
   **Complete when:** any new regression check demonstrates sensitivity to the defect and the implementation addresses the evidenced cause.
5. **Verify on the same boundary.** Re-run the original observation, focused tests, and required repository checks. Inspect the final diff for speculative guards, unrelated cleanup, and changed contracts.
   **Complete when:** the original symptom no longer occurs at the proving boundary and behavioral evidence supports the completion claim.

**Done when:** diagnosis-only work has a supported mechanism and named gaps, or fixed work has failing-then-passing evidence against the original symptom.
