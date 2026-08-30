# Review

1. **Resolve the fixed point.** Identify the exact range or files, changed behavior, and requirements or intent source. Do not infer a whole-repository review.
   **Complete when:** the review scope and expected behavior can be stated exactly.
2. **Choose the lenses.** Always inspect correctness and regression risk. Add tests, failure modes, security, performance, compatibility, or simplification only when the change makes that lens material. Use independent fresh reviewers when the risk or breadth justifies them.
   **Complete when:** every selected lens has a concrete risk in the scoped change and no material risk class lacks coverage.
3. **Gather candidates.** Apply the loaded Evidence rules. Retain reachable failures, contract contradictions, missing requirements, and material maintainability costs; reject style-only, speculative, pre-existing, and out-of-scope complaints.
   **Complete when:** every candidate states its trigger, impact, and source evidence or has been rejected.
4. **Verify each finding.** Trace callers and safeguards, inspect covering tests, and reproduce when proportionate. Separate verified, partially verified, unresolved, and rejected candidates. A second reviewer counts as corroboration only when it adds independent evidence.
   **Complete when:** every retained candidate has a verification status, method, and report destination.
5. **Report by consequence.** Lead with a merge or readiness verdict. Give exact locations, trigger, impact, evidence, and smallest fix direction for each material finding. Put important unresolved claims in open questions with the evidence needed to settle them.
   **Complete when:** the verdict depends only on material verified findings and every open question names the evidence needed to settle it.

Do not edit reviewed files or begin remediation. A fix is a separately authorized Rigor task. For a heavyweight multi-reviewer milestone review, the user can invoke `/code-quorum` directly.

**Done when:** every reported finding is material, located, evidence-backed, and separated from unresolved questions and optional suggestions.
