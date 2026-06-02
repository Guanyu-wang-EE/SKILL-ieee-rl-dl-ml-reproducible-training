---
name: ieee-rl-reproducible-training
description: Use when working on RL/DRL paper reproduction, long training, train/test evaluation, case studies, ablation studies, IEEE Transactions plots, real-time CSV/MATLAB monitoring, traceable outputs, Chinese-first project documentation, reproducible run records, or cleanup of failed training outputs.
---

# IEEE RL Reproducible Training

## Overview

Use this skill to make RL/DRL reproduction runs traceable while producing IEEE Transactions-style figures, train/test evaluation records, real-time monitoring artifacts, Chinese-first project documentation, and clean final experiment directories.

Keep this `SKILL.md` lightweight. Load the specific reference file needed for the current task instead of copying all detailed rules into context.

## Standard Workflow

1. Define the experiment hypothesis and minimum reproduction path: algorithms, environments, seeds, steps, metrics, and stopping rules.
2. Build the real-time trace structure before long training starts: stdout interval, CSV interval, MATLAB monitor, checkpoints, plan summary, and manifest.
3. Run a small smoke test to verify the environment, CSV writes, stdout summary, MATLAB readability, and checkpoint writes.
4. Start long training only after the smoke test passes; print PowerShell/Python training summaries every 10 episodes or at a fixed step interval.
5. Apply mid-run risk gates; stop and record when NaN, alpha/lambda explosion, unreasonable constraint violation, performance collapse, or environment interaction errors appear.
6. After training, run a separate evaluation/test pass with explicit checkpoint selection, test seeds, policy mode, metrics, and evaluation artifacts.
7. Generate IEEE figures, manifests, `threshold_summary.csv`, and a Chinese-first `output.md` report.
8. Verify completeness before cleanup; delete failed outputs and redundant exploratory files, but keep trustworthy successful runs.

## Resource Map

| Need | Load or use |
|---|---|
| IEEE Transactions on Smart Grid / Power Systems plot style, export formats, captions, SVG/font manifest rules | `references/ieee-plot-style.md` |
| Real-time training trace, stdout format, CSV files, MATLAB monitoring, checkpoints | `references/realtime-training-monitoring.md` and `assets/monitor_training_template.m` |
| Train/test evaluation records, checkpoint choice, deterministic/stochastic policy mode, test seeds | `references/realtime-training-monitoring.md` and `references/reproducibility-recordkeeping.md` |
| Chinese-first README/requirements/output report, environment and SHA256 records, Python file header rules | `references/reproducibility-recordkeeping.md`, `assets/python_file_header_templates.md`, and `assets/output_report_template.md` |
| Early stop gates for NaN/Inf, OOM, alpha/lambda, constraints, reward collapse, CSV/fps anomalies | `references/early-stop-risk-gates.md` |
| Stage cleanup, failed-run deletion, successful-run preservation, naming discipline | `references/project-hygiene-cleanup.md` |
| Deterministic run trace verification | `scripts/validate_run_trace.py` |
| Deterministic IEEE figure manifest verification | `scripts/check_ieee_plot_manifest.py` |

## Operating Rules

- Do not wait until a run ends to write artifacts. Create real-time `progress.csv`, episode/update logs, stdout summaries, `stdout.log`, checkpoints, and plan-level summaries.
- Treat IEEE style as publishable scientific communication, not decoration. Use fixed dimensions, fonts, line widths, axis rules, export formats, and manifest records.
- Keep generated project documentation Chinese-first with bilingual technical terms at first mention.
- Stop clearly bad runs early and record why. Do not let bad runs contaminate aggregate summaries.
- Clean only after verification. Delete failed or exploratory artifacts, but preserve successful multi-seed, multi-algorithm, and repeated validation runs with time/seed/script naming.
- Do not create extra documentation inside this skill folder. Project `README.md`, `requirements.txt`, and `output.md` are outputs guided by the skill, not skill-internal README files.

## Verification Commands

Run these when the corresponding artifacts exist:

```bash
python scripts/validate_run_trace.py path/to/run-folder
python scripts/check_ieee_plot_manifest.py path/to/figure_manifest.json
```

After editing this skill itself, validate the skill folder with the skill-creator validator.
