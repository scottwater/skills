# Round 2 — Closing verifier prompt

Dispatch once after the consolidated repair, or directly after round 1 if repair was skipped. Fill every `[BRACKET]`.

```text
Subagent (general-purpose; closing verifier):
  description: "Verify corrections and prove delivery behavior"
  prompt: |
    Verify [FINAL_HEAD] in [DIRECTORY].
    Original scope, acceptance claims, and agreed limits: [SCOPE_AND_PLAN].
    Round-1 findings and dispositions: [FINDINGS_FILE].
    Repair report or skipped status: [FIX_REPORT_OR_STATUS].
    Correction diff [FIX_BASE]..[FINAL_HEAD]: [CORRECTION_PACKAGE].
    Prior delivery diff for reference: [DELIVERY_PACKAGE].
    Shared Convince Me proof protocol: [PROOF_PROTOCOL_FILE].
    Save results and command evidence to [CLOSING_REPORT_FILE].

    This is round 2, the final review and proof phase. Verify the accepted
    corrections, behavior affected by them, and the original goal. Follow
    callers and shared state as needed to check those contracts. Consult
    the prior delivery diff only when a named claim needs it; do not restart
    a full-branch search for unrelated findings.

    Read and follow the proof protocol for every agreed acceptance claim.
    Run the full suite and typecheck once where available; use focused
    checks for claims they leave unproven. Capture commands, observed
    results, checked HEAD, and environment limits.

    Preserve tracked files, index, and HEAD. Disposable fixtures/scripts and
    ignored evidence artifacts are allowed; clean them up safely. If useful
    permanent tests are missing, report that follow-up rather than changing
    the reviewed tree. Respect the protocol's approval boundaries for live
    calls, money, destructive actions, and external state. Missing approval
    means unverified, not permission to simulate a successful real run.

    Execute verification without implementation repairs. Mark failed claims
    disproven and inconclusive or unavailable checks unverified. Keep the
    agreed scope and proof requirements unchanged.

    Record newly observed material defects, especially regressions caused
    by the correction, without launching broader searches or fixing them.
    Where known, distinguish original defects from correction-induced ones;
    otherwise say provenance is uncertain. No nested review or fixer runs.

    Return:
    - Each accepted finding: resolved / unresolved / unverified, with evidence.
    - Claim | command/artifact and observed result | proven/disproven/unverified.
    - Newly demonstrated blockers and their trigger/consequence.
    - Non-blocking follow-ups: area, evidence or uncertainty, consequence,
      and suggested next action.
    - Exact checks, final HEAD, and confirmation the tracked tree is unchanged.

    Stop after the report even if defects remain. If a serious blocker makes
    further proof inappropriate, report it and mark unchecked claims unverified.
    The controller decides Complete / Complete with follow-ups / Blocked.
```

`[PROOF_PROTOCOL_FILE]` is the absolute path resolved from [Convince Me's shared protocol](../tracer-convince-me/proof-protocol.md). Resolve the other paths from the delivery ledger; pass `repair skipped` when no repair report exists.
