# Project Hygiene And Cleanup

Use this reference at the end of each stage and before final delivery of an RL/DRL reproduction project.

## Stage Order

At each stage:

1. Verify outputs.
2. Clean and slim the workspace only when project/user instructions authorize deletion; otherwise mark misleading artifacts as excluded.
3. Move to the next stage.

Do not clean first and verify later.

## Delete

Delete artifacts that would confuse final reproduction only when deletion is explicitly authorized:

- Temporary test figures.
- Exploratory plots.
- Failed run outputs.
- Half-finished or broken run folders.
- Old incorrect scripts.
- Caches.
- Unexplained JSON/CSV files.
- Duplicate debug files.
- Early-stage scripts, JSON, or plots that no longer serve the final reproducible experiment.

## Do Not Delete

Do not delete credible successful records, including:

- Normal multi-seed successful runs.
- Multi-algorithm successful runs.
- Repeated successful validation runs.

These must be distinguishable by time, seed, and script name.

## Naming

Recommended run folder pattern:

```text
runs/20260603_1530_car_circle_ccpo_seed0_train_main/
```

Recommended plan-level pattern:

```text
runs/car_circle_50k_agent_v1/20260603_1530_seed0_ccpo/
```

Equivalent names are acceptable if they preserve time, seed, algorithm, environment, and script identity.

## Failed Or Corrective Runs

For failed, half-finished, or corrective runs, prefer exclusion records unless cleanup is explicitly authorized. Record one MD event line in `output.md`, `debug_and_change_log.md`, or a stage log. The line must include time, reason, and handling action.

## Successful Runs

Successful run folders must retain:

```text
config.json, run_command.txt, progress.csv, episodes.csv, updates.csv, summary.json, checkpoints, stdout.log
```

When evaluation/test has been run, also retain:

```text
eval_config.json, eval_command.txt, eval_episodes.csv, eval_summary.json
```

At plan/report level, retain `plan_summary.json` and `threshold_summary.csv` when they exist.

The final directory should serve reproducible experiments rather than preserve every early exploration artifact.
