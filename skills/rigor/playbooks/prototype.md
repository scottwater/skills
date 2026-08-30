# Prototype

1. **Name the decision.** State the single question, the alternatives worth distinguishing, and the observation that would decide among them.
   **Complete when:** the prototype has a decision to produce rather than a feature to ship.
2. **Choose disposable isolation.** Prefer a scratch directory, disposable branch, temporary route, or clearly marked prototype location that cannot be mistaken for production code. Use the lightest available stack that can reproduce the deciding behavior.
   **Complete when:** the prototype can run without altering production data or being mistaken for a supported implementation.
3. **Build only the probe.** Apply the loaded Alternatives rules. Keep the artifact to the code needed for the deciding observation, including persistence or error behavior only when either is under test.
   **Complete when:** every line serves the deciding observation and the variants satisfy the Alternatives reference.
4. **Observe the real question.** Drive the interaction, print the state, capture the timing, or compare screenshots on the relevant surface. Do not treat compilation as the observation.
   **Complete when:** the evidence distinguishes the alternatives or proves the prototype inconclusive.
5. **Record the decision.** Present the variants, evidence, tradeoffs, recommendation, and artifact location. State plainly that the code is throwaway. Remove it unless the user wants the primary-source artifact retained outside production history.
   **Complete when:** the answer survives independently of the disposable code and the artifact's retention state is explicit.

**Done when:** the question has an evidence-backed answer or a precise explanation of what the probe could not settle. Production implementation requires a new Feature task.
