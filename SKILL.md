---
name: ieee-rl-reproducible-training
description: Use when RL/DRL paper reproduction or energy-system control work needs long training, traceable train/test evaluation, online-checkable CSV/JSONL/stdout records, IEEE TSG/TPS figures, Chinese-first colleague-readable reports, post-training PPT/report packs, figure/table quality audit, SHA256 manifests, artifact indexes, risk analysis, or cleanup/exclusion of failed or half-finished artifacts.
---

# IEEE RL Reproducible Training

## Overview

Use this skill to keep RL/DRL reproduction work traceable end to end: live training records, separate train/test evaluation, IEEE-style figures, Chinese-first colleague-readable reports, risk analysis, reproducibility manifests, and clean final experiment folders.

## Hard Router

| User task | Load |
|---|---|
| Set up or audit long training traces, stdout logs, CSV/JSONL, TensorBoard, checkpoints, smoke tests, or evaluation/test passes | `references/realtime-training-monitoring.md` |
| Write or audit README, requirements, `output.md`, run records, environment records, or Python headers | `references/reproducibility-recordkeeping.md` plus needed template in `assets/` |
| Generate PPT-ready post-training Markdown, figures, tables, reproducibility manifest, artifact index, PPT index, or missing-figure/table reports | `references/post-training-reporting.md`; also load `references/ieee-plot-style.md` for figure style |
| Generate or review IEEE Transactions on Smart Grid / Power Systems figures, captions, export formats, SVG fonts, or figure manifests | `references/ieee-plot-style.md`; use `scripts/check_ieee_plot_manifest.py` when a manifest exists |
| Final audit before declaring a run/project/report complete | `references/final-quality-gates.md`; optionally run `scripts/audit_reproducible_training_project.py` |
| Clean or close a project stage, exclude failed/half-finished/junk artifacts, or preserve successful runs | `references/project-hygiene-cleanup.md` |
| Use MATLAB for live CSV viewing | `references/realtime-training-monitoring.md` and `assets/monitor_training_template.m` |
| Verify an existing run folder | Use `scripts/validate_run_trace.py` |

Do not load every reference by default. Load only the routed files plus any directly required assets/scripts.

## Hard Gates

- Do not start long training without a smoke test, resource/GPU/Python/solver check when relevant, dry-run manifest, unique output directory, and live CSV/JSONL/stdout/checkpoint plan.
- Do not claim training/reporting completion until train and evaluation records are separated and the final quality gates are checked.
- Generated Markdown must be Chinese-first, technically explicit, cross-linked, and readable by an engineering colleague who did not watch the run.
- Post-training packs must include README or index entry, main/summary/debug reports, risk analysis, figure/table index, reproducibility manifest with SHA256 and bytes, and explicit missing-output notes.
- Figures must follow IEEE style, export PNG/PDF/SVG when data exists, validate SVG font handling and vector path geometry, avoid overlap/clutter, and pass a figure quality audit or record why audit is unavailable.
- Generated experiment Python files must have the Chinese overview header; generated `main.py`, `run_*.py`, `train_*.py`, and long-running entry scripts must also include the Buddha blessing header from `assets/python_file_header_templates.md`.
- Preserve successful run records. Delete failed/misleading artifacts only when user/project instructions authorize deletion; otherwise mark them excluded with evidence.
- Missing data is a result. Do not fabricate plots, tables, SOC traces, metrics, baselines, or paper-level claims.

## Minimal Workflow

1. Define the minimum reproducible path: hypothesis, algorithm, environment, seeds, steps, metrics, and outputs.
2. Before long training, create real-time records and run a smoke test.
3. During training, write live CSV/JSONL, stdout summaries, TensorBoard events when enabled, and checkpoints.
4. After training, run a separate evaluation/test pass with explicit checkpoint, policy mode, test seeds, and metrics.
5. After valid training/evaluation packages, generate PPT-ready reports, risk notes, figure/table packages, figure quality audit, manifests, and artifact indexes, or explicit missing-artifact notes.
6. Run the final quality gates, then clean or exclude misleading artifacts according to the project cleanup policy; keep trustworthy successful runs.

## Operating Rules

- Do not wait until a run ends to write artifacts.
- Treat CSV/JSON artifacts as the authoritative reproducibility record. TensorBoard is a dashboard; MATLAB is optional CSV viewing.
- Keep train and test records separate.
- Treat IEEE style as scientific communication, not decoration.
- Keep generated project documentation Chinese-first with bilingual technical terms at first mention.
- Do not invent generic training termination rules. Use project-defined criteria when the project provides them.
- Do not treat training as complete until post-training reporting artifacts are generated, cross-linked, quality-audited, or missing artifacts are documented.
- Do not delete run artifacts unless the user or project instructions explicitly authorize cleanup. If deletion is not authorized, mark failed or misleading outputs as excluded.
- Preserve successful multi-seed, multi-algorithm, and repeated validation runs with time/seed/script naming.
- Do not create extra documentation inside this skill folder. Project `README.md`, `requirements.txt`, and `output.md` are outputs guided by the skill, not skill-internal README files.

## Verification Commands

Run only the checks that match existing artifacts:

```bash
python scripts/validate_run_trace.py path/to/run-folder
python scripts/check_ieee_plot_manifest.py path/to/figure_manifest.json
```

After editing this skill itself, validate the skill folder structure and markdown formatting.
