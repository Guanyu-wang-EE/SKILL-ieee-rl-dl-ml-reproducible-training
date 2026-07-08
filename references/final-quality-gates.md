# Final Quality Gates

Use this reference before claiming any substantial RL/DRL training, pilot, long run, report, or artifact package is complete. It exists because agents often follow the training loop but forget presentation, reproducibility, or readability requirements.

For non-RL, affine-only, DL-only, or paper-style numerical reproduction packages, apply the recordkeeping, figure/table, manifest, cleanup, and final closure checks. Mark RL-only rows such as TensorBoard, reward, episodes, policy mode, train/eval rollouts, alpha/lambda, and feasible-rate metrics as `NOT APPLICABLE` unless the project explicitly defines them.

## Required Audit Order

1. Check code headers.
2. Check live run/evaluation records.
3. Check reports and reader usability.
4. Check figures, figure README, figure quality audit, and tables.
5. Check manifests and indexes.
6. Check `skill_compliance_audit.md`.
7. Check reviewer-driven closure when code, tests, execution configs, experiments, plots, reports, metrics, or debug patches changed.
8. Check cleanup/exclusion records.
9. State remaining missing items instead of silently omitting them.

## Code Header Gate

For generated or substantially rewritten Python experiment files:

- Load `assets/python_file_header_templates.md` before auditing or editing headers.
- Require the Chinese overview header fields from that template for all generated `.py` files; do not require or add a literal `# 中文为主总览：` line.
- Require the Buddha blessing block only for generated `main.py`, `run_*.py`, `train_*.py`, long-running launchers, and equivalent project entrypoints.
- Keep comments useful: reward/cost definitions, constraint thresholds, seed fixing, checkpoint strategy, data filtering, non-obvious algorithm logic, and important or innovative design blocks. Use concise Chinese comments for those design blocks.

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

If any gate, test, or training failure triggered debug cycles, `diagnostic.json` or `gate_debug_report.md` must record each cycle with `cycle, symptom, source_artifact_or_file, first_incorrect_value, consequence, hypothesis, minimal_test_command, patch_summary, rerun_command, verdict, next_action`. Missing fields fail the debug audit gate.

Reward comparisons, algorithm rankings, PPT takeaways, and paper-facing claims must use same-tier raw environment reward delta, such as environment `step()` reward or `eval_episodes.csv:reward` on one scale. If only shaped training-objective rewards exist, mark the comparison `NOT READY` and keep those curves diagnostic-only.

`algorithm_comparison_summary.csv` must include `algorithm, tier, seed_count, raw_reward_source, raw_env_reward_mean, raw_env_reward_std, delta_vs_same_tier_baseline, shaped_reward_used_for_claim`. Any `shaped_reward_used_for_claim=true` row fails the reward comparison gate.

## Markdown Gate

Reports must be Chinese-first unless the user asks otherwise. They must be usable by a technically literate engineering colleague without the chat transcript.

Root `README.md` must be a navigation page, not only an introduction or changelog. It must use relative links that resolve locally and cover reports, figures, tables, code, configs, runs, validation logs, manifests, audit files, and missing-output notes, or mark unavailable categories as `NOT AVAILABLE` with a reason.

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
same_tier_raw_reward_delta.csv
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
skill_compliance_audit.md
```

The reproducibility manifest must include SHA256 and byte counts for Markdown reports, figures, tables, validation logs, and checkpoints that are part of the final package.

The PPT index or colleague briefing must map each slide to a figure, table, takeaway, claim boundary, and artifact path.

`skill_compliance_audit.md` must include a Markdown table with `gate_id, requirement, evidence_path, command, verdict, missing_reason` so final readiness is machine-checkable.

## Closure Review Gate

Run this gate when the work changed code, tests, execution-affecting configs, experiments, plots, tables, reports, metric definitions, or debug patches. For documentation-only result packaging with no claim, metric, figure, or table change, state `NOT APPLICABLE`.

1. Mainline pass: the main agent implements the smallest coherent change, keeps the research objective explicit, and preserves unrelated user changes.
2. Reviewer loop: run three review-fix-review cycles by default for substantial changes. Review the staged or current diff/artifact set independently and classify findings as `P0`, `P1`, or `P2`. On the third cycle, close only if no `P0` or `P1` remains; otherwise continue until those findings are cleared or explicitly blocked with evidence.
3. Brooks pass: material code/design findings must record `Symptom`, `Source`, `Consequence`, and `Remedy`. Use test-quality review only when the reviewed object is an existing test suite or test strategy.
4. Plot/table/metric pass: verify row grain, grouping keys, metric direction, normalization, and duplicate-counting risk before plotting or scoring. Do not connect rows across independent scenarios, seeds, folds, ranks, episodes, or timestamps unless that is the intended statistical unit. Add scenario-level or slice-level tables when aggregate figures can hide heterogeneity.
5. Ponytail pass: every changed file maps to the failed gate or requested output; no new dependency, abstraction, config surface, or broad refactor was added unless required.
6. Residual risk pass: record accepted, rejected, and deferred reviewer findings with file paths and evidence. Fix accepted `P0`/`P1` findings before completion; fix `P2` only when cheap and aligned with the objective. If Brooks Lint is already available, it may be used for this review; do not install it only to satisfy this gate.

For paper-style artifact packages, also run a contract closure audit: compare stage contract wording, report claims, figure axes/legends/text, and actual output files. Verify visual inspection evidence, `git diff --check`, generated Python headers, and staged-path boundaries before claiming completion.

## Cleanup Gate

Do not delete credible successful run records. Only reproducible temporary artifacts such as language caches and local test caches may be auto-cleaned. For failed, debug, half-finished, or misleading artifacts:

- exclude them in the report/manifest by default;
- delete them only if user/project instructions authorize cleanup;
- record the reason and handling action.

## Optional Machine Audit

When the project root is available, run:

```bash
python <skill_root>/scripts/audit_reproducible_training_project.py --project-root <repo> --results-dir <repo>/results/<project_tag>
```

Treat the script as a smoke audit, not a replacement for domain judgment.
