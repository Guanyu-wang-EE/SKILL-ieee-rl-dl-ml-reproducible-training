# Real-Time Training Monitoring

Use this reference before launching long RL/DRL runs. Do not design training code that only saves artifacts at run end.

## Required Run Files

Every run must write artifacts during training:

| File | Timing | Required role |
|---|---|---|
| `progress.csv` | Real time | Step/episode progress for monitoring and recovery |
| `episodes.csv` | Episode level | Episode-level outcomes |
| `updates.csv` | Update-batch level | Losses, alpha/lambda, and update statistics |
| `summary.json` | Final | Final status and aggregate metrics |
| `plan_summary.json` | Plan final | Plan-level algorithms, seeds, steps, outputs, stop records, and aggregate status |
| `config.json` | Start | Reproducible configuration |
| `run_command.txt` | Start | Exact launch command |
| `stdout.log` | Real time | Console trace retained for diagnosis |
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

Use risk-event lines with `[warn]`, and stop lines with `[stop]`. Accept `[progress]` for non-episode progress summaries.

Warn on alpha/lambda explosion, long reward collapse, NaN/Inf, constraint violation that does not decline, abnormal fps, CSV not updating, or environment interaction errors.

## MATLAB Monitor

- Use a `.m` monitor that reads lightweight CSV files.
- Plot reward, cost/constraint violation, alpha/lambda, and fps/elapsed as four core views.
- Keep it visually clean but separate from final IEEE figure generation.
- Do not depend on the Python training process ending.
- Do not lock training files or block CSV writers.
- Use `assets/monitor_training_template.m` as the starting template.

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

At plan level, write `plan_summary.json` after the planned batch finishes or stops. Include algorithms, environments, seeds, steps, output directories, completed runs, failed/stopped runs, and retained/deleted artifacts.

During figure/report generation, write `threshold_summary.csv` when threshold sweeps or feasibility summaries are used. Recommended columns:

```text
algo, seed_count, threshold, reward_mean, reward_std, cv_mean, feasible_rate
```

## Smoke Test Before Long Training

Before long training, run a small smoke test that verifies:

- Environment creation and one or more interactions.
- CSV files are created and updated.
- Stdout summaries print in the agreed format.
- MATLAB can read `progress.csv` while training is active or simulated.
- Checkpoint directory is writable.
