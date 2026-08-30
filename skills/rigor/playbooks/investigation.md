# Investigation

1. **Frame the question.** Identify the target, the exact answer or decision requested, and the boundary of the investigation. State the best-supported interpretation rather than asking about a referent the repository can resolve.
   **Complete when:** different plausible interpretations would not produce different investigations.
2. **Trace the evidence.** Follow actual entry points, symbols, data flow, callers, and effects. Search history and decision records when the question asks why rather than how. Divide broad systems into independent read-only angles only when it improves coverage.
   **Complete when:** every material step or claim has a source citation and every untraced edge is named.
3. **Test consequential uncertainty.** Run safe, non-mutating checks when behavior can be observed. Separate direct evidence, supported inference, plausible hypothesis, and unknowns.
   **Complete when:** the recommendation does not depend on an unlabelled assumption.
4. **Synthesize.** Answer the question directly. Include the working model or alternatives, tradeoffs, risks, and the smallest useful next action. Do not modify product code or drift into implementation.
   **Complete when:** the answer resolves the framed question, preserves confidence distinctions, and exposes every material gap.

**Done when:** the user can verify the answer from the cited evidence and can see what remains unknown.
