# IEEE RL Reproducible Training Skill

<p align="right"><strong>English</strong> | <a href="README_zh.md">简体中文</a></p>

This repository is the Git-backed source mirror for an RL/DRL reproducible-training skill. It turns long-running reinforcement-learning experiments into auditable research packages: live training records, separated train/evaluation evidence, TensorBoard monitoring, same-tier raw reward comparisons, IEEE-style figures, artifact manifests, and final quality gates.

Repository documentation belongs here. Lean installed runtime copies should contain only files needed by the skill itself.

## Table Of Contents

- [Purpose](#purpose)
- [Repository Map](#repository-map)
- [How To Use The Skill](#how-to-use-the-skill)
- [Core Contracts](#core-contracts)
- [Reference Index](#reference-index)
- [Script Index](#script-index)
- [Asset Index](#asset-index)
- [Expected Project Outputs](#expected-project-outputs)
- [Generated Project README Contract](#generated-project-readme-contract)
- [Validation Commands](#validation-commands)
- [Maintenance Notes](#maintenance-notes)
- [Language Parity](#language-parity)

## Purpose

Use this skill for reproducible RL/DRL experiments where scientific claims must be traceable from command to final report. It is especially useful for energy-system control, smart-grid simulation, constrained RL, long unattended training, post-training artifact packaging, and group-meeting or paper-facing evidence audits.

The skill is intentionally strict. It treats missing data as a result, not as a reason to invent plots, metrics, baselines, or completion claims.

## Repository Map

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | Entry point, hard gates, routing table, and minimal workflow |
| [`references/`](references/) | Task-specific rules loaded only when needed |
| [`scripts/`](scripts/) | Deterministic validators and audit helpers |
| [`assets/`](assets/) | Templates and reusable output helpers |
| [`agents/`](agents/) | Optional UI-facing metadata |
| [`README.md`](README.md) | English repository navigation |
| [`README_zh.md`](README_zh.md) | Simplified Chinese repository navigation |

## How To Use The Skill

1. Read [`SKILL.md`](SKILL.md) first.
2. Use its `Reference Routing` table to load only the relevant reference files.
3. Run the deterministic script that matches the artifact under review.
4. Before any final or complete claim, load [`references/final-quality-gates.md`](references/final-quality-gates.md) and run the relevant audit command.

Do not load every reference by default. The skill is designed as a compact router plus focused references.

## Core Contracts

- Do not start long training without smoke tests, resource checks, live logging, checkpoints, and a TensorBoard dashboard plan.
- Do not claim completion until training records and evaluation records are separated.
- Do not advance a phase after a failed scientific gate; use the five-cycle debug rule and record evidence before marking `BLOCKED`.
- When code, tests, execution configs, or debug patches changed, close with Ponytail-style minimality review and Brooks-style code/test diagnosis.
- Do not compare shaped training-objective rewards across methods as performance evidence.
- Post-training reward comparisons must use same-tier raw environment reward delta, such as environment `step()` reward or `eval_episodes.csv:reward` on one scale.
- Root project `README.md` must be a navigation page with relative links to reports, figures, tables, code, configs, runs, validation logs, manifests, audits, and missing-output notes.
- Final reporting must include risk boundaries, missing-output notes, artifact indexes, SHA256 manifests, and quality-gate evidence.
- Failed, stopped, smoke, short, pilot, or infeasible runs must not be averaged into valid performance means.

## Reference Index

| Reference | Load When |
|---|---|
| [`references/realtime-training-monitoring.md`](references/realtime-training-monitoring.md) | Planning or auditing long training, live CSV/JSONL/stdout records, TensorBoard, checkpoints, scientific gates, five-cycle debugging, bad-run handling |
| [`references/reproducibility-recordkeeping.md`](references/reproducibility-recordkeeping.md) | Writing or auditing project `README.md`, `requirements.txt`, `output.md`, run records, Python headers, and reproducibility notes |
| [`references/post-training-reporting.md`](references/post-training-reporting.md) | Generating reports, figures, tables, artifact index, reproducibility manifest, PPT index, colleague briefing, missing-output notes |
| [`references/ieee-plot-style.md`](references/ieee-plot-style.md) | Creating or reviewing IEEE-style figures, captions, SVG/PDF/PNG exports, figure manifests |
| [`references/final-quality-gates.md`](references/final-quality-gates.md) | Final audit before declaring a run, report, package, or project complete; includes closure review when code/tests/debug patches changed |
| [`references/project-hygiene-cleanup.md`](references/project-hygiene-cleanup.md) | Cleaning or excluding failed, misleading, half-finished, or junk artifacts while preserving trustworthy successful runs |

## Script Index

| Script | Purpose |
|---|---|
| [`scripts/validate_run_trace.py`](scripts/validate_run_trace.py) | Validates run folders for required training records, progress schema, checkpoints, and optional evaluation artifacts |
| [`scripts/check_ieee_plot_manifest.py`](scripts/check_ieee_plot_manifest.py) | Checks figure manifests, export coverage, and IEEE figure package consistency |
| [`scripts/audit_reproducible_training_project.py`](scripts/audit_reproducible_training_project.py) | Performs final smoke/semantic audit: root README navigation, skill compliance matrix, raw reward comparison columns, shaped-reward claim failure, high-risk claim warnings, reports, figures, tables, TensorBoard events, manifests, artifact index, and generated-code header checks |

## Asset Index

| Asset | Purpose |
|---|---|
| [`assets/python_file_header_templates.md`](assets/python_file_header_templates.md) | Chinese-first Python file header and entry-script blessing template |
| [`assets/output_report_template.md`](assets/output_report_template.md) | Structured `output.md` report template |
| [`assets/monitor_training_template.m`](assets/monitor_training_template.m) | MATLAB CSV monitor template for backup live supervision |

## Expected Project Outputs

### Run Records

| Artifact | Requirement |
|---|---|
| `config.json`, `run_command.txt`, `git_commit.txt` | Reproducible launch context |
| `stdout.log`, `progress.csv`, `episodes.csv`, `updates.csv` | Live training and diagnostic records |
| `tensorboard/` or `tb/` event files | Required long-training dashboard evidence |
| `checkpoints/latest`, `checkpoints/best` | Recoverable model provenance |
| `summary.json`, `diagnostic.json` or `gate_debug_report.md` | Final status, gate/debug evidence, stopped-run reasons |

### Evaluation Records

| Artifact | Requirement |
|---|---|
| `eval_config.json`, `eval_command.txt` | Evaluation setup and exact command |
| `eval_episodes.csv`, `eval_summary.json` | Test seeds, checkpoint source, policy mode, feasible rate, and evaluation metrics |

### Post-Training Package

| Artifact | Requirement |
|---|---|
| Root `README.md` or result `index.md` | Navigation page, not only introduction or changelog |
| Main report, summary, risk report, debug/change log | Chinese-first technical evidence with clear claim boundaries |
| `figures/`, figure README, `figure_quality_audit.md`, `figure_quality_audit.csv` | IEEE-style figures and quality evidence |
| `tables/`, `algorithm_comparison_summary.csv`, `same_tier_raw_reward_delta.csv`, run/eval/constraint summaries | Machine-readable summaries |
| `reproducibility_manifest.json`, `artifact_index.csv` | SHA256/byte-count manifest and human-readable artifact index |
| `ppt_index.md` or `colleague_briefing.md` | Slide map, takeaway, claim boundary, and artifact path |
| `skill_compliance_audit.md`, `completion_audit.md` when used | Gate matrix and final readiness evidence |
| `missing_figures.md`, `missing_tables.md` | Explicit missing columns, upstream artifact, and instrumentation needs |

### Raw Reward Comparison Table

`algorithm_comparison_summary.csv` must include:

```text
algorithm, tier, seed_count, raw_reward_source, raw_env_reward_mean, raw_env_reward_std, delta_vs_same_tier_baseline, shaped_reward_used_for_claim
```

`shaped_reward_used_for_claim` must be `false` for performance rows. If it is `true`, the final audit fails.

## Generated Project README Contract

For each RL/DRL reproduction project using this skill, the project root `README.md` must be a navigation page with GitHub-safe relative links. It must index:

- subdirectory READMEs such as `figures/README.md` or TensorBoard event README files;
- reports: index, formal report, summary, PPT index, colleague briefing, risk report, debug/change log;
- figures: figure directory, figure README, figure quality audit, missing figures note;
- tables: table directory, algorithm comparison, run summary, evaluation summary, constraint violation summary, artifact index;
- code: `src/`, `scripts/`, training entry, evaluation entry, post-training artifact generation script;
- configs: `commands/configs/` or the project-specific config directory;
- runs: `runs/`, `progress.csv`, `stdout.log`, checkpoints, TensorBoard event directory;
- reproducibility and audit: manifest, artifact index, validation logs, skill compliance audit, completion audit;
- missing outputs: `missing_figures.md`, `missing_tables.md`.

If a category is not produced, the README must state `NOT AVAILABLE: <reason>` or link the relevant missing-output note. It must not silently omit the category.

## Validation Commands

Use the checks that match the artifact under review:

```bash
python path/to/quick_validate.py .
python scripts/validate_run_trace.py path/to/run-folder
python scripts/check_ieee_plot_manifest.py path/to/figure_manifest.json
python scripts/audit_reproducible_training_project.py --project-root path/to/repo --results-dir path/to/results
python -m py_compile scripts/validate_run_trace.py scripts/check_ieee_plot_manifest.py scripts/audit_reproducible_training_project.py
```

`audit_reproducible_training_project.py` returns `PASS`, `WARN`, or `FAIL`. `FAIL` means a final delivery gate is missing or scientifically unsafe; `WARN` means legacy debt or claim-risk text needs review.

## Maintenance Notes

- Keep [`SKILL.md`](SKILL.md) short and route details to references.
- Update reference files and audit scripts together when a requirement becomes machine-checkable.
- Keep repository-only documentation in this Git mirror, not in lean installed runtime copies.
- Validate scripts after edits and remove generated caches before publishing.
- Update [`README.md`](README.md) and [`README_zh.md`](README_zh.md) in the same commit.

## Language Parity

[`README_zh.md`](README_zh.md) is the Simplified Chinese counterpart of this file. The two READMEs should have the same sections, claims, gates, commands, and maintenance expectations.
