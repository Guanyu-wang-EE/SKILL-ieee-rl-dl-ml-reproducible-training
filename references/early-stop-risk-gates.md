# Early Stop Risk Gates

Use this reference to decide when a run should stop or require manual review.

## Stop Or Review Triggers

Trigger stop or manual review when any of these occur:

- NaN or Inf appears in reward, cost, losses, alpha/lambda, gradients, or summary metrics.
- OOM or repeated memory pressure invalidates timing or checkpoint reliability.
- Alpha/lambda explodes or exceeds the configured safe range.
- Constraint violation does not decline over a sustained window.
- Reward collapses for a sustained window or diverges from expected behavior.
- Reward and cost trends clearly contradict the experiment hypothesis over consecutive windows.
- Environment interaction throws repeated errors or produces invalid transitions.
- `progress.csv` stops updating during an active run.
- FPS becomes abnormal enough to suggest a stalled process, bad device placement, or data pipeline failure.
- Checkpoints cannot be written or read back.

## Required Stop Record

When stopping, record in `output.md` or a stage log:

- Time.
- Run folder.
- Algorithm, environment, and seed.
- Trigger condition.
- Evidence from stdout/CSV.
- Handling action.
- Whether artifacts were deleted or retained.

## Cleanup After Stop

Failed or contaminated run folders should be deleted after the stop record is written, unless there is a concrete debugging reason to preserve a small diagnostic artifact. Keep only the MD event record for failed or corrective runs that should not enter final analysis.

Do not delete successful multi-seed, multi-algorithm, or repeated validation runs because another run failed.
