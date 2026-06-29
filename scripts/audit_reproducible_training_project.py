"""中文概览: RL/DRL 复现实验最终产物轻量审计.

用途: 检查实验项目是否遗漏中文 Python 头注释、佛头、PPT-ready 报告、图表、
表格、manifest、artifact index 和 PPT index.
创建日期: 2026-06-29.
输入文件/CSV: 项目根目录和 results 目录.
输出文件: 可选 JSON 审计报告.
依赖脚本/模块: Python 标准库.
运行示例: python scripts/audit_reproducible_training_project.py --project-root . --results-dir results/power_uc_omnisafe.
复现说明: Buddha bless this audit; it is a smoke gate, not a scientific validator.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HEADER_MARKERS = ("中文概览", "中文为主总览")
BUDDHA_MARKERS = ("佛祖保佑", "Buddha")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    results = Path(args.results_dir).resolve()
    findings = []
    findings.extend(check_python_headers(root))
    findings.extend(check_results(results))
    payload = {
        "project_root": str(root),
        "results_dir": str(results),
        "verdict": "PASS" if not findings else "WARN",
        "findings": findings,
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text)
    raise SystemExit(0 if not findings else 1)


def check_python_headers(root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for folder_name in ("scripts", "src", "code"):
        folder = root / folder_name
        if not folder.exists():
            continue
        for path in folder.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            head = path.read_text(encoding="utf-8", errors="ignore")[:1200]
            rel = str(path.relative_to(root))
            if not any(marker in head for marker in HEADER_MARKERS):
                findings.append({"type": "missing_python_chinese_header", "path": rel})
            if is_entry_script(path) and not any(marker in head for marker in BUDDHA_MARKERS):
                findings.append({"type": "missing_buddha_header", "path": rel})
    return findings


def is_entry_script(path: Path) -> bool:
    name = path.name.lower()
    return name == "main.py" or name.startswith("run_") or name.startswith("train_") or "long" in name


def check_results(results: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    required_files = [
        "reproducibility_manifest.json",
        "artifact_index.csv",
        "ppt_index.md",
    ]
    for rel in required_files:
        if not (results / rel).exists():
            findings.append({"type": "missing_required_reporting_artifact", "path": rel})

    md_files = list(results.glob("*.md")) if results.exists() else []
    if not md_files:
        findings.append({"type": "missing_markdown_reports", "path": str(results)})

    figures = results / "figures"
    has_png = figures.exists() and any(figures.glob("*.png"))
    has_pdf = figures.exists() and any(figures.glob("*.pdf"))
    if not (has_png and has_pdf) and not (results / "missing_figures.md").exists():
        findings.append({"type": "missing_figures_or_missing_figures_note", "path": str(figures)})

    tables = results / "tables"
    has_tables = tables.exists() and any(tables.glob("*.csv"))
    if not has_tables and not (results / "missing_tables.md").exists():
        findings.append({"type": "missing_tables_or_missing_tables_note", "path": str(tables)})
    return findings


if __name__ == "__main__":
    main()
