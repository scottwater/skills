# Performance

1. **Fix the workload.** Reproduce the complaint with realistic inputs, state, concurrency, and environment. Select the metric, direction of improvement, correctness gate, and noise-handling method before changing code.
   **Complete when:** a repeatable baseline command or capture distinguishes the target problem from normal behavior.
2. **Mechanism.** Apply the loaded Evidence rules while tracing or profiling the running path. Test whether the measured work can be eliminated before optimizing it.
   **Complete when:** measured evidence identifies the work dominating the target metric, or the capture's inability to isolate it is explicit.
3. **Stop for diagnosis-only work.** Report the workload, baseline, measured mechanism, source attribution, confidence, and the smallest improvement direction. Keep product code unchanged.
   **Complete when:** the diagnosis separates measurement from inference and names what would resolve every material uncertainty.
4. **Run one hypothesis.** For diagnose-and-improve work, make the smallest change that tests one mechanism. Measure before and after with the fixed workload and run the correctness gate.
   **Complete when:** the result is clearly kept, reverted, or inconclusive based on the preselected metric.
5. **Choose the stopping mode.** For a one-off issue, stop after the evidenced fix. For an explicit hillclimb, repeat one hypothesis per iteration, keep a compact attempt log, pivot after plateaus, and measure each change before combining it with another.
   **Complete when:** the requested target is met, or the remaining hypotheses and reason for stopping are explicit.
6. **Verify the result.** Re-run enough samples to separate the delta from noise. Check user-visible behavior and resource tradeoffs alongside the target number.
   **Complete when:** the final comparison uses the fixed workload and includes correctness and tradeoff evidence.

**Done when:** diagnosis-only work has a measured mechanism and named gaps, or improved work reports the workload, baseline, final measurement, delta, correctness evidence, artifact or command, and every limitation that weakens the comparison.
