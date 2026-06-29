# IEEE RL Reproducible Training Skill

<p align="right"><strong>English</strong> | <a href="README_zh.md">简体中文</a></p>

A reproducible reinforcement-learning training skill for traceable experiments, separated train/test records, IEEE-style figures, and final artifact audits.

This repository is the Git-backed source mirror for the skill. Repository documentation belongs here; installed runtime copies should stay lean and contain only files needed for execution.

## What It Does

- Defines live CSV/JSONL/stdout/checkpoint records for long training runs.
- Separates training evidence from evaluation evidence and post-training reports.
- Routes figure style, report packages, manifests, cleanup, and final audits through dedicated references and scripts.

## When To Use

Use this skill when the task matches the description in `SKILL.md`. Read `SKILL.md` first, then follow its routing table before opening references, scripts, assets, or indexed resources.

Typical use cases:

- Run a smoke test before long training and create unique output folders.
- Write live records during training and run a separate evaluation pass afterward.
- Generate reports, figures, manifests, risk notes, and final quality-gate evidence before completion claims.

## Repository Contents

- `agents/`
- `assets/`
- `references/`
- `scripts/`
- `SKILL.md`

## Operating Contract

- Do not fabricate metrics, plots, baselines, or completion claims.
- Keep training and evaluation records separate.
- Preserve successful run records and mark failed artifacts rather than silently mixing them.

## Validation And Review

- Check `SKILL.md` frontmatter before changing skill discovery metadata.
- Keep `## Hard Gates`, `## Reference Routing`, and `## Verification` aligned with the actual files in this repository.
- If a `references/final-quality-gates.md` file exists, use it before any final, ready, published, submitted, or complete claim.
- If a skill-specific audit script exists, run it after changing routed files or deterministic helpers.

## Maintenance Notes

- Keep `SKILL.md` as the entry point and router.
- Keep detailed domain material in `references/` when the skill has reference files.
- Keep deterministic helpers in `scripts/` or `tools/` and validate them after edits.
- Update `README.md` and `README_zh.md` together so both languages describe the same scope and gates.
- Do not move repository-only documentation into installed runtime copies.

## Language Parity

`README_zh.md` is the Simplified Chinese counterpart of this file. When one README changes, update the other in the same commit.
