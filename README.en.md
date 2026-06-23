# IEEE RL Reproducible Training Skill

English | [Simplified Chinese](README.md)

## Skill Name

`ieee-rl-reproducible-training`

This repository is the public GitHub version of a Codex skill for reproducible reinforcement learning (RL) and deep reinforcement learning (DRL) experiment workflows. Keep Git version control in this standalone repository rather than inside the active Codex skills installation directory, so Codex skill discovery stays lightweight.

## Trigger Scope

Use this skill for DRL/RL paper reproduction, long training runs, case studies, ablation studies, IEEE Transactions-style plotting, real-time training monitoring, experiment traceability, Chinese-first project documentation, reproducible run records, and cleanup of failed outputs.

## Structure

- `SKILL.md`
- `agents/openai.yaml`
- `references/ieee-plot-style.md`
- `references/realtime-training-monitoring.md`
- `references/reproducibility-recordkeeping.md`
- `references/project-hygiene-cleanup.md`
- `assets/monitor_training_template.m`
- `assets/python_file_header_templates.md`
- `assets/output_report_template.md`
- `scripts/validate_run_trace.py`
- `scripts/check_ieee_plot_manifest.py`

## Core Capabilities

- IEEE Transactions-style plotting rules for publication-grade figures.
- Real-time training traces through CSV/JSONL files, stdout summaries, TensorBoard dashboards, optional MATLAB inspection, checkpoints, and manifests.
- Reproducibility records for Python, conda, CUDA/PyTorch, GPU/CPU, seeds, commands, paths, and SHA256 manifests.
- Cleanup discipline that preserves trustworthy successful runs while deleting failed, half-finished, junk, and misleading exploratory outputs after verification.

## Validation Scripts

Run `python scripts/validate_run_trace.py path/to/run-folder` to check run traces. Run `python scripts/check_ieee_plot_manifest.py path/to/figure_manifest.json` to check IEEE figure manifests.

## Recommended Maintenance Workflow

Use `git pull`, edit the skill files, inspect `git status`, then commit and push from this standalone repository clone. The active Codex skills installation directory should stay lightweight and should not contain Git metadata.
