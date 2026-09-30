# Correction-only verifier prompt

Use only when the repair pass changed code, preferably by resuming the initial reviewer. Skip this step when no repairs were needed or all repairs were blocked without changes.

Use the shared [reviewer prompt](../tracer-implement/ticket-reviewer-prompt.md) in correction mode. Supply original acceptance and safety limits, initial findings and controller dispositions, repair report, and the correction diff from the repair's starting SHA to final HEAD. Include the original delivery package for reference, not a new broad audit.

Verify accepted corrections, affected behavior, and preserved invariants using focused checks where existing evidence is insufficient. Save `.tracer/implement/review-2.md` with checked HEAD, finding status, actual evidence, and unresolved concerns. This step neither runs an automatic full suite nor starts a separate proof protocol. The controller owns final evidence for the agreed verification scope.

Return findings without implementation repairs or nested agents. Report any correction-induced regressions and stop; remaining material defects make the delivery Blocked rather than authorizing another repair pass.
