# Post-Training Reporting And PPT-Ready Artifacts

Use this reference after valid RL/DRL training or evaluation packages, especially T2/T3/T4 pilot or long-run packages. Training is not complete until the reporting package exists, `references/final-quality-gates.md` is checked, or missing outputs are explicitly documented.

## Table Of Contents

- Completion rule
- Output roots
- Verification log
- Markdown reports
- Figures
- Tables
- Missing output protocol
- Reproducibility manifest
- Artifact index
- PPT index
- Recommended script pattern
- Status vocabulary

## Completion Rule

A run package is complete only when it has:

- training/evaluation artifacts validated or failure recorded;
- PPT-ready Markdown reports;
- IEEE-style figures in PNG and PDF when data exists;
- CSV summary tables;
- reproducibility manifest with SHA256 and byte counts;
- artifact index;
- PPT index;
- `missing_figures.md` or `missing_tables.md` for any required output that cannot be generated from available columns.

Do not fabricate plots, columns, metrics, or statistical claims. Missing data is a reporting result.

## Output Roots

Use the project's reporting root. Common layout:

```text
results/<project_tag>/
results/<project_tag>/figures/
results/<project_tag>/tables/
results/<project_tag>/validation_logs/
```

For Power-UC OmniSafe, use:

```text
results/power_uc_omnisafe/
```

## Verification Log

Write:

```text
results/<project_tag>/validation_logs/post_run_verification.txt
```

Record each attempted command:

```text
command
exit_code
stdout/stderr summary
verdict
artifact path
```

Run real checks only. If a repository does not contain a named validator, record `SCRIPT_NOT_FOUND` and use the closest real check.

Typical checks:

```bash
python -m compileall -q src scripts
git diff --check
python scripts/validate_run_trace.py --require-eval <run_dir>
python scripts/check_ieee_plot_manifest.py <figure_manifest.json>
```

## Markdown Reports

Generate at minimum:

```text
report_single_seed_or_pilot.md
report_single_seed_or_pilot_summary.md
debug_and_change_log.md
index.md
```

For a group-meeting long run, also generate:

```text
report_group_meeting_long.md
report_group_meeting_long_summary.md
```

Main report sections:

1. experiment purpose;
2. evidence tier: smoke, pilot, or long run;
3. why the evidence is or is not paper-level proof;
4. environment and domain setting;
5. wrapper or simulator setting;
6. algorithm route and labels;
7. source-code verdict for the target algorithm;
8. dependency source commit and license when relevant;
9. solver/license status when relevant;
10. resource report;
11. training configuration;
12. fixed tier, steps, episodes, and seeds;
13. inherited passed gates;
14. reward curve summary;
15. cost curve summary;
16. constraint-violation summary;
17. evaluation by budget or threshold;
18. constrained-algorithm dynamics;
19. recovery/switch diagnostics when available;
20. ratio/KL/clipping diagnostics when available;
21. checkpoint round-trip;
22. warnings and anomalies;
23. stop-early checks;
24. limitations;
25. next pilot, long-run, or ablation plan.

Debug/change log sections:

```text
chronological debugging history
major scientific gate decisions
why weak tiers cannot prove performance
why unavailable exact algorithms are not claimed
why approximations are labelled as inspired or approximate
why the wrapper/simulator mode is used
config changes from previous runs
stop-rule relaxations and rationale
fixed seeds
failed or excluded runs
known remaining risks
```

## Figures

Use `references/ieee-plot-style.md` for styling. Generate PNG and PDF when feasible.

Core figures:

```text
training_reward_curve
training_cost_curve
constraint_violation_curve
eval_reward_by_algorithm
eval_cost_by_algorithm
eval_violation_by_algorithm
ppo_vs_constrained_cost_curve
ppo_vs_constrained_reward_curve
episode_cost_distribution
episode_reward_distribution
checkpoint_roundtrip_bar
```

Constrained/CPPO-style diagnostics when columns exist:

```text
recovery_switch_timeline
recovery_switch_rate_curve
ratio_tracking_loss_curve
policy_loss_curve
value_loss_curve
cost_margin_dprime_curve
ratio_min_max_curve
clip_fraction_curve
```

Domain/control figures when columns exist:

```text
daily_action_heatmap
action_dimension_profiles
storage_soc_profiles
hydrogen_soc_profiles
cumulative_carbon_curve
carbon_budget_tracking
market_status_timeline
load_shedding_reserve_shortage
reward_cost_tradeoff_scatter
pareto_reward_cost_violation
pipeline_diagram
```

## Tables

Generate under `tables/`:

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

Optional tables when diagnostics exist:

```text
recovery_switch_summary.csv
ratio_tracking_summary.csv
cost_margin_summary.csv
clip_summary.csv
action_summary.csv
soc_summary.csv
carbon_summary.csv
market_status_summary.csv
physical_safety_summary.csv
```

## Missing Output Protocol

If a figure or table cannot be generated, write:

```text
missing_figures.md
missing_tables.md
```

For each missing output include:

```text
name
required columns
available columns
missing columns
upstream artifact expected
recommended instrumentation
```

## Reproducibility Manifest

Write:

```text
reproducibility_manifest.json
```

Include:

```text
git_head
branch
source dependency commits
target algorithm source verdict
source environment path or commit
config paths
run dirs
seeds
solver mode and license status
resource report
dry-run manifest when available
checkpoint paths
evaluation artifacts
figures with SHA256 and bytes
tables with SHA256 and bytes
Markdown reports with SHA256 and bytes
validation logs with SHA256 and bytes
verification commands and results
known limitations
```

## Artifact Index

Write a human-readable CSV:

```text
artifact_index.csv
```

Columns:

```text
relative_path, artifact_type, bytes, sha256, created_at, source_run, included_in_report
```

## PPT Index

Write:

```text
ppt_index.md
```

Use this slide map unless the project defines a better one:

```text
Slide 1: Goal and route
Slide 2: Environment and wrapper/simulator setting
Slide 3: Source verdict and dependency provenance
Slide 4: Baseline sanity
Slide 5: Constrained method or inspired method
Slide 6: Training reward/cost curves
Slide 7: Evaluation reward/cost/violation
Slide 8: Recovery or ratio diagnostics
Slide 9: Main comparison table
Slide 10: Limitations and next plan
```

For each slide list:

```text
recommended figure
recommended table
one-sentence takeaway
artifact path
```

## Recommended Script Pattern

Prefer one project script:

```text
scripts/generate_<project_tag>_artifacts.py
```

The script should read run dirs and generate figures, tables, Markdown reports, manifests, artifact index, PPT index, and missing-output notes. Keep plotting/report code in one place unless the repository already has a cleaner pattern.

## Status Vocabulary

Use one reporting status:

```text
SMOKE ARTIFACT REPORT PASSED
PILOT ARTIFACT REPORT PASSED
T4 GROUP-MEETING LONG REPORT PASSED
ARTIFACT REPORT COMPLETED WITH WARNINGS
NOT READY: <first hard failing gate and evidence>
```

Do not claim paper-level multi-seed proof, statistical superiority, exact target-algorithm reproduction, or final algorithm performance unless the experiment tier and validation protocol actually support that claim.
