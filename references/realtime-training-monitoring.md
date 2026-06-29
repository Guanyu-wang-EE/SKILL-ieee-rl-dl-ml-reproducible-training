# Real-Time Training Monitoring

Use this reference before launching long RL/DRL runs. Do not design training code that only saves artifacts at run end.

## Monitoring Stack

Use a layered monitoring stack instead of binding reproducibility to one viewer:

| Layer | Status | Role |
|---|---|---|
| CSV/JSONL artifacts | Required | Authoritative reproducibility record for audit, recovery, aggregation, and final figures |
| stdout and `stdout.log` | Required | Lightweight live status, warnings, FPS, and elapsed-time diagnosis |
| Checkpoints | Required | Recovery and model provenance through `latest`, `best`, and final model files |
| TensorBoard | Required for long training | Default online dashboard for multi-run, multi-seed, loss, constraint, and hyperparameter inspection |
| MATLAB `.m` monitor | Backup | CSV-reading fallback viewer for MATLAB-centered inspection or when TensorBoard access is blocked |

For long training, do not run end-to-end blind: create TensorBoard event files and a launch/view command before the run starts. TensorBoard must not replace the authoritative CSV/JSONL records or final IEEE figure generation. MATLAB monitoring reads the generated CSV files as the backup live supervision path; it does not justify omitting TensorBoard unless the blocker is explicit and approved.

## Required Run Files

Every run must write artifacts during training:

| File | Timing | Required role |
|---|---|---|
| `progress.csv` | Real time | Step/episode progress for monitoring and recovery |
| `episodes.csv` | Episode level | Episode-level outcomes |
| `updates.csv` | Update-batch level | Losses, alpha/lambda, and update statistics |
| `summary.json` | Final | Final status and aggregate metrics |
| `config.json` | Start | Reproducible configuration |
| `run_command.txt` | Start | Exact launch command |
| `stdout.log` | Real time | Console trace retained for diagnosis |
| `tensorboard/` or `tb/` | During long training | TensorBoard event files for online dashboards, not the sole scientific record |
| `checkpoints/` | During run | `latest` and `best` model states |

`progress.csv` must include at least:

```text
timestamp, algo, seed, env, step, episode, reward, cost, violation, alpha/lambda, actor_loss, critic_loss, fps, elapsed_sec
```

Use separate columns such as `alpha` and `lambda` when both exist; do not create ambiguous merged semantics in the actual CSV.

## Stdout Discipline

Print a plan line before training:

```text
[plan] algorithms=... seeds=... steps=... out=...
```

Print a training summary every 10 episodes or at a fixed step interval:

```text
[train] env=CarCircle algo=ccpo seed=0 step=12000 ep=38 reward=-34.2 cost=1.8 cv=0.03 alpha=0.72 fps=820 elapsed=00:14:21
```

Use `[warn]` for project-defined abnormal events. Accept `[progress]` for non-episode progress summaries.

Warn on abnormalities defined by the current project, such as metric instability, artifact update failures, abnormal fps, or environment interaction errors.

## TensorBoard Dashboard

- Require TensorBoard as the default online dashboard for long training when the project uses PyTorch, TensorFlow, Stable-Baselines, CleanRL, RLlib, or another compatible training stack.
- Record the TensorBoard log directory and launch command, for example `tensorboard --logdir <run-root>`, in the run README, `run_command.txt`, or monitoring notes.
- Log reward, cost, constraint violation, alpha/lambda, actor loss, critic loss, entropy/KL or equivalent policy diagnostics, FPS, and elapsed time using stable tag names.
- Keep TensorBoard run directories grouped by algorithm, environment, seed, and timestamp so multi-run comparisons remain interpretable.
- Flush events at a real-time interval that is useful for monitoring without turning event writes into a training bottleneck.
- Do not treat TensorBoard event files as the only record; mirror scalar values into CSV/JSONL artifacts for reproducibility, aggregation, and publication plots.

## Backup MATLAB Monitor

- Use a `.m` monitor that reads lightweight CSV files as the backup live viewer when MATLAB-based inspection is useful or TensorBoard access is blocked.
- Plot reward, cost/constraint violation, alpha/lambda, and fps/elapsed as four core views.
- Keep it visually clean but separate from final IEEE figure generation.
- Do not depend on the Python training process ending.
- Do not lock training files or block CSV writers.
- Use `assets/monitor_training_template.m` as the starting template when enabling this backup monitor.

## Monitoring Modes To Avoid

- Do not rely on final-only plots after training completes.
- Do not use notebook polling as the primary long-run monitor.
- Do not rely only on terminal progress bars without structured logs.
- Do not treat MATLAB as a replacement for TensorBoard in normal long training. It is a CSV-based backup viewer.

## Checkpoints

- Save more than the final model.
- Keep `latest` and `best` checkpoints during training.
- Final artifacts must let a reviewer explain model provenance from `actor.pt`, `summary.json`, `config.json`, and `run_command.txt`.

Use project-conventional names such as `checkpoints/latest.pt`, `checkpoints/best.pt`, and final `actor.pt`. If the algorithm is not actor-based, `config.json` must explicitly name the replacement final model file.

## Evaluation / Test Pass

Training and testing artifacts must be separated. After training, run an evaluation/test pass that records:

| File | Required role |
|---|---|
| `eval_config.json` | Evaluation environment, episode count, seeds, checkpoint choice, deterministic/stochastic policy mode |
| `eval_command.txt` | Exact evaluation launch command |
| `eval_episodes.csv` | Per-test-episode reward, cost, violation, length, seed, and checkpoint source |
| `eval_summary.json` | Aggregate test metrics, feasible rate, checkpoint source, and policy mode |

Evaluation rules:

- State whether the policy is deterministic or stochastic.
- State whether evaluation loads `best`, `latest`, or another named checkpoint.
- Use explicit test seeds; do not silently reuse training seeds without recording that choice.
- Keep training metrics and evaluation metrics in separate files and separate report tables.
- Log whether evaluation uses the same thresholds as training.

## Plan And Threshold Summaries

At plan/report level, write `plan_summary.json` after the planned batch finishes or is interrupted. Include algorithms, environments, seeds, steps, output directories, completed runs, failed/interrupted runs, and retained/excluded artifacts.

For PPT-ready reports, manifests, artifact indexes, and missing-figure/table notes, use `references/post-training-reporting.md`.

During figure/report generation, write `threshold_summary.csv` when threshold sweeps or feasibility summaries are used. Recommended columns:

```text
algo, seed_count, threshold, reward_mean, reward_std, cv_mean, feasible_rate
```

## Smoke Test Before Long Training

Before long training, run a small smoke test that verifies:

- Environment creation and one or more interactions.
- CSV files are created and updated.
- Stdout summaries print in the agreed format.
- TensorBoard event files are created and readable.
- MATLAB can read `progress.csv` while training is active or simulated when the backup MATLAB monitor is used.
- Checkpoint directory is writable.
