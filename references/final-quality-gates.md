# Final Quality Gates

Use this reference before claiming any substantial RL/DRL training, pilot, long run, report, or artifact package is complete. It exists because agents often follow the training loop but forget presentation, reproducibility, or readability requirements.

## Required Audit Order

1. Check code headers.
2. Check live run/evaluation records.
3. Check reports and reader usability.
4. Check figures, figure README, figure quality audit, and tables.
5. Check manifests and indexes.
6. Check cleanup/exclusion records.
7. State remaining missing items instead of silently omitting them.

## Code Header Gate

For generated or substantially rewritten Python experiment files:

- Require the Chinese overview header fields from `assets/python_file_header_templates.md`.
- Require the Buddha blessing block for generated `main.py`, `run_*.py`, `train_*.py`, and long-running orchestration scripts.
- Keep comments useful: reward/cost definitions, constraint thresholds, seed fixing, checkpoint strategy, data filtering, and non-obvious algorithm logic.

If a legacy file lacks these headers and the task does not authorize editing it, mention the gap instead of silently ignoring it.

## Run Record Gate

Each credible run should have:

```text
config.json
run_command.txt
git_commit.txt
stdout.log
progress.csv
episodes.csv
updates.csv
tensorboard/ or tb/ with event files
summary.json
diagnostic.json or gate_debug_report.md
checkpoints/latest
checkpoints/best
```

If evaluation has been run, also require:

```text
eval_config.json
eval_command.txt
eval_episodes.csv
eval_summary.json
```

Training and evaluation metrics must remain separate.
Long training must include TensorBoard event files and a recorded dashboard/logdir command. If MATLAB live monitoring is used, it must read generated CSV files such as `progress.csv` and remain a backup viewer rather than replacing TensorBoard.

Reward comparisons, algorithm rankings, PPT takeaways, and paper-facing claims must use same-tier raw environment reward delta, such as environment `step()` reward or `eval_episodes.csv:reward` on one scale. If only shaped training-objective rewards exist, mark the comparison `NOT READY` and keep those curves diagnostic-only.

## Markdown Gate

Reports must be Chinese-first unless the user asks otherwise. They must be usable by a technically literate engineering colleague without the chat transcript.

Require:

- direct conclusion;
- experiment objective and evidence tier;
- environment and solver status;
- algorithm labels and source verdict;
- configuration, seeds, steps, and budgets;
- train/eval separation;
- tables with key metrics;
- figure index;
- links to figure quick-start README, table directory, risk report, manifest, and validation logs when these exist;
- warnings and excluded runs;
- limitations and next plan.

Avoid vague status text such as `looks good` or `training complete` without artifact paths and verification evidence.

For substantial post-training packages, require a reader path that an engineering colleague can follow without the chat transcript:

```text
README/index -> main report -> summary -> risk report -> figures README -> tables -> manifest -> validation logs
```

## Figure Gate

Use `references/ieee-plot-style.md`. Before finalizing figures, check:

- PNG/PDF/SVG export exists when data exists;
- same-stem PNG/PDF pairs exist for final figures;
- same-stem PNG/SVG pairs exist for final figures;
- SVG font mode, font evidence, and vector geometry checks are recorded;
- font is Times New Roman or a reasonable serif fallback;
- axis labels include metric names and units when available;
- x/y limits are not misleading and do not hide important variance;
- legends do not cover curves;
- colors are restrained and color-blind safe;
- captions/report text explain metric, threshold, seed count, and evidence tier;
- representative core/risk figures have been visually inspected for text overlap, legend occlusion, blank output, and unreadable density;
- missing columns are recorded in `missing_figures.md`;
- `figures*/README.md` tells colleagues which PDF figures to use and how to explain risks;
- `figure_quality_audit.md` and `figure_quality_audit.csv` exist when a final figure package exists, or the reason they are missing is recorded.

## Table Gate

At minimum, produce or explicitly mark missing:

```text
run_summary.csv
episode_summary.csv
eval_summary.csv
constraint_violation_summary.csv
algorithm_comparison_summary.csv
checkpoint_roundtrip_summary.csv
warning_summary.csv
artifact_index.csv
```

If a table cannot be generated, write `missing_tables.md` with required columns, available columns, missing columns, upstream artifact, and recommended instrumentation.

## Manifest And PPT Gate

Require:

```text
reproducibility_manifest.json
artifact_index.csv
ppt_index.md or colleague_briefing.md
```

The reproducibility manifest must include SHA256 and byte counts for Markdown reports, figures, tables, validation logs, and checkpoints that are part of the final package.

The PPT index or colleague briefing must map each slide to a figure, table, takeaway, claim boundary, and artifact path.

## Cleanup Gate

Do not delete credible successful run records. For failed, debug, half-finished, or misleading artifacts:

- exclude them in the report/manifest by default;
- delete them only if user/project instructions authorize cleanup;
- record the reason and handling action.

## Optional Machine Audit

When the project root is available, run:

```bash
python <skill_root>/scripts/audit_reproducible_training_project.py --project-root <repo> --results-dir <repo>/results/<project_tag>
```

Treat the script as a smoke audit, not a replacement for domain judgment.
