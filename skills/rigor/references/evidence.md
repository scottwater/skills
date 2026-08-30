# Work from evidence

- **Fix root causes.** Establish the symptom, form competing hypotheses, instrument uncertain state, and change the mechanism that produces the failure. A defensive guard may be correct, but it is not a root-cause explanation by itself.
- **Prove the real outcome.** Exercise the actual path or closest practical boundary. Inspect delegated artifacts rather than trusting summaries. State environmental limits instead of upgrading partial evidence into certainty.
- **Sequence verifiable units.** Choose units small enough that a failed check identifies the responsible change. A unit may be one edit, one task, or one migration phase.
- **Build a lever when it pays.** Use a script, codemod, generator, query, or reproducible command when scale, repetition, consistency, or reviewability justifies it. Prefer an existing tool or direct change when a new artifact would cost more than it proves.

**Complete when:** every retained claim has an observation, every changed mechanism has a discriminating check, and every evidence gap remains visible.
