# Reproducibility Recordkeeping

Use this reference when creating or auditing project documents, run records, script headers, and result reports for RL/DRL reproduction projects.

## Chinese-First Project Documents

Generated project documentation must be Chinese-first. At first mention, give key technical terms in bilingual form, for example:

- 约束违反 (constraint violation)
- 消融实验 (ablation study)

Required project documents:

| File | Required content |
|---|---|
| `README.md` | Chinese-first narrative, reproduction entry point, key terms with bilingual first mention |
| `requirements.txt` or environment document | Python, conda env, PyTorch, CUDA, GPU/CPU, package versions, and teammate-machine setup notes |
| `output.md` | Expert-level result analysis, hypotheses, configurations, tables, IEEE figure index, paper differences, risks, and next-step recommendations |

When useful for the local hardware context, include compatibility notes for 4070/i7H machines.

## Required Records

Every credible run or stage must record:

- What was done.
- Stage status and reason for continuation, interruption, or completion.
- Which outputs are trustworthy.
- Which outputs were deleted.
- Algorithm, environment, seed, steps, metrics, and thresholds.
- Train/test split, evaluation seeds, checkpoint choice, and deterministic/stochastic policy mode.
- CPU/GPU, CUDA, PyTorch, Python, and conda environment.
- Exact command, output paths, and SHA256 manifest entries when a reporting package is generated.
- Plan-level `plan_summary.json` and threshold-level `threshold_summary.csv` when applicable.

For PPT-ready Markdown packs, figure/table requirements, reproducibility manifests, artifact indexes, PPT indexes, and missing-output notes, use `references/post-training-reporting.md`.

Do not write as if long training has not happened when the true state is plan, running, stopped, failed, or completed. Keep the status explicit.

## `output.md` Expectations

`output.md` must include:

- Experiment objective and hypothesis.
- Configuration and environment.
- Seeds, metrics, thresholds, and project-defined success criteria.
- Evaluation/test setup, test seeds, policy mode, and whether `best` or `latest` checkpoint was loaded.
- Run summary and data tables.
- IEEE figure index when figures are generated.
- `threshold_summary.csv` rows when threshold sweeps are used.
- Comparison with the target paper or reproduction target.
- Differences from the paper and plausible causes.
- Abnormal events and handling.
- Expert risk assessment.
- Next-step recommendations.

Use `assets/output_report_template.md` when drafting this file.

## Python File Headers

All `.py` files generated for these projects should start with a Chinese-first overview header covering purpose, creation date, input files or CSVs, output files, dependent scripts/modules, run example, and reproducibility notes.

Large one-command main/run/long-training scripts additionally use the Buddha blessing ASCII header and English blessing specified in `assets/python_file_header_templates.md`.

Inside code, comment only non-obvious and reproducibility-relevant logic such as reward/cost normalization, constraint thresholds, alpha updates, seed fixing, and checkpoint strategy. Do not write empty comments for ordinary assignments or obvious logic.
