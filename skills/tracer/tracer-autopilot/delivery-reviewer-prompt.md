# Delivery reviewer prompt

Use the shared [reviewer prompt](../tracer-implement/ticket-reviewer-prompt.md) in initial mode once after the cohesive delivery is implemented. One review covers all accepted tickets/tasks; task boundaries do not multiply reviews.

Supply the original scope and safety limits, short plan, implementation evidence, and cumulative `BASE..REVIEW_HEAD` package. Save `.tracer/implement/review-1.md`. The controller adjudicates findings. If no repairs are accepted, proceed to final evidence without a closing-verifier agent.
