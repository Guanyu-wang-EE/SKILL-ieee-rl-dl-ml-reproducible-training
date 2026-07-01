"""中文概览: RL/DRL 复现实验最终产物轻量审计.

用途: 检查实验项目是否遗漏中文 Python 头注释、佛头、根 README 导航、PPT-ready
报告、图表、表格、figure quality audit、manifest、artifact index 和 PPT/colleague briefing index.
创建日期: 2026-06-29.
输入文件/CSV: 项目根目录和 results 目录.
输出文件: 可选 JSON 审计报告.
依赖脚本/模块: Python 标准库.
运行示例: python scripts/audit_reproducible_training_project.py --project-root . --results-dir results/power_uc_omnisafe.
复现说明: Buddha bless this audit; it is a smoke gate, not a scientific validator.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


HEADER_MARKERS = ("中文概览",)
HEADER_FIELDS = ("目的", "创建日期", "输入文件/CSV", "输出文件", "依赖脚本/模块", "运行示例", "复现说明")
BUDDHA_MARKERS = ("佛祖保佑", "Buddha")
COMPLIANCE_COLUMNS = {"gate_id", "requirement", "evidence_path", "command", "verdict", "missing_reason"}
ALGORITHM_COMPARISON_COLUMNS = {
    "algorithm",
    "tier",
    "seed_count",
    "raw_reward_source",
    "raw_env_reward_mean",
    "raw_env_reward_std",
    "delta_vs_same_tier_baseline",
    "shaped_reward_used_for_claim",
}
HIGH_RISK_CLAIMS = (
    "exact cppo",
    "paper-level proof",
    "converged",
    "optimal",
    "safe policy",
    "state-of-the-art",
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
README_NAVIGATION_CATEGORIES = {
    "figures": ("figures", "figure_quality_audit", "missing_figures"),
    "tables": ("tables", "algorithm_comparison", "run_summary", "eval_summary", "constraint_violation", "artifact_index"),
    "scripts": ("scripts",),
    "src": ("src",),
    "configs": ("configs", "commands", "config"),
    "runs": ("runs", "progress.csv", "stdout.log", "checkpoints", "tensorboard"),
    "results": ("results", "index.md", "report", "summary"),
    "validation": ("validation_logs", "skill_compliance_audit", "completion_audit"),
    "manifest": ("reproducibility_manifest", "artifact_index"),
}


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
    findings.extend(check_root_readme_navigation(root))
    findings.extend(check_results(root, results))
    verdict = "PASS"
    if any(item.get("severity") == "FAIL" for item in findings):
        verdict = "FAIL"
    elif findings:
        verdict = "WARN"
    payload = {
        "project_root": str(root),
        "results_dir": str(results),
        "verdict": verdict,
        "findings": findings,
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text)
    raise SystemExit(0 if verdict == "PASS" else 1)


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
            has_header_marker = any(marker in head for marker in HEADER_MARKERS)
            has_header_fields = all(field in head for field in HEADER_FIELDS)
            if not (has_header_marker or has_header_fields):
                findings.append(finding("WARN", "legacy_missing_python_chinese_header", rel))
            if is_entry_script(path) and not any(marker in head for marker in BUDDHA_MARKERS):
                findings.append(finding("FAIL", "generated_entry_missing_buddha_header", rel))
    return findings


def is_entry_script(path: Path) -> bool:
    name = path.name.lower()
    return name == "main.py" or name.startswith("run_") or name.startswith("train_") or "long" in name


def check_results(root: Path, results: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not results.exists():
        return [finding("FAIL", "missing_results_dir", str(results))]

    if not find_any(results, ["*reproducibility_manifest.json", "*manifest*.json"]):
        findings.append(finding("FAIL", "missing_reproducibility_manifest", str(results)))
    if not find_any(results, ["artifact_index.csv"]):
        findings.append(finding("FAIL", "missing_artifact_index", str(results)))
    if not find_any(results, ["ppt_index.md", "*colleague*briefing*.md", "*briefing*.md"]):
        findings.append(finding("FAIL", "missing_ppt_or_colleague_briefing", str(results)))
    compliance_files = list(results.rglob("skill_compliance_audit.md"))
    if not compliance_files:
        findings.append(finding("FAIL", "missing_skill_compliance_audit", str(results)))
    else:
        findings.extend(check_skill_compliance_audit(compliance_files[0]))
    if not find_any(results, ["progress.csv"]) and not find_any(root, ["progress.csv"]):
        findings.append(finding("FAIL", "missing_progress_csv_for_live_monitoring", str(results)))
    if not find_any(results, ["events.out.tfevents*", "*.tfevents*"]) and not find_any(root, ["events.out.tfevents*", "*.tfevents*"]):
        findings.append(finding("FAIL", "missing_tensorboard_event_files", str(results)))

    md_files = list(results.rglob("*.md"))
    if not md_files:
        findings.append(finding("FAIL", "missing_markdown_reports", str(results)))
    elif not any("风险" in read_text(path) or "risk" in path.name.lower() for path in md_files):
        findings.append(finding("FAIL", "missing_explicit_risk_analysis", str(results)))
    findings.extend(check_claim_boundaries(md_files, results))

    figure_dirs = [path for path in results.rglob("*") if path.is_dir() and (any(path.glob("*.png")) or any(path.glob("*.pdf")))]
    if not figure_dirs and not find_any(results, ["missing_figures.md"]):
        findings.append(finding("FAIL", "missing_figures_or_missing_figures_note", str(results)))
    for figures in figure_dirs:
        pngs = list(figures.glob("*.png"))
        pdfs = {path.stem for path in figures.glob("*.pdf")}
        svgs = {path.stem for path in figures.glob("*.svg")}
        for png in pngs:
            if png.stem not in pdfs:
                findings.append(finding("FAIL", "missing_same_stem_pdf", str(png)))
            if png.stem not in svgs:
                findings.append(finding("FAIL", "missing_same_stem_svg", str(png)))
        if pngs and not (figures / "README.md").exists():
            findings.append(finding("FAIL", "missing_figure_quickstart_readme", str(figures)))
        if pngs and not (figures / "figure_quality_audit.md").exists():
            findings.append(finding("FAIL", "missing_figure_quality_audit_md", str(figures)))
        if pngs and not find_any(results, ["figure_quality_audit.csv"]):
            findings.append(finding("FAIL", "missing_figure_quality_audit_csv", str(results)))

    has_tables = any(path.name != "artifact_index.csv" for path in results.rglob("*.csv"))
    if not has_tables and not find_any(results, ["missing_tables.md"]):
        findings.append(finding("FAIL", "missing_tables_or_missing_tables_note", str(results)))
    findings.extend(check_algorithm_comparison(results))
    findings.extend(check_missing_notes(results))
    return findings


def check_root_readme_navigation(root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    readme = root / "README.md"
    if not readme.exists():
        return [finding("FAIL", "missing_root_readme_navigation", str(readme))]

    text = read_text(readme)
    links = list(extract_markdown_links(text))
    if not links:
        findings.append(finding("FAIL", "root_readme_has_no_navigation_links", str(readme)))

    local_targets: list[str] = []
    for raw_target in links:
        target = normalize_markdown_target(raw_target)
        if not target or is_external_or_anchor(target):
            continue
        if is_absolute_local_link(target):
            findings.append(finding("FAIL", "root_readme_uses_non_relative_link", str(readme), target))
            continue
        local_targets.append(target.lower().replace("\\", "/"))
        path_part = strip_fragment_and_query(target)
        if not path_part:
            continue
        candidate = (readme.parent / unquote(path_part)).resolve()
        if not candidate.exists():
            findings.append(finding("FAIL", "root_readme_broken_relative_link", str(readme), target))

    link_blob = "\n".join(local_targets)
    text_blob = text.lower()
    for category, tokens in README_NAVIGATION_CATEGORIES.items():
        if any(token in link_blob for token in tokens):
            continue
        if has_not_available_reason(text_blob, category, tokens):
            continue
        findings.append(finding("FAIL", "root_readme_missing_navigation_category", str(readme), category))
    return findings


def check_skill_compliance_audit(path: Path) -> list[dict[str, str]]:
    text = read_text(path)
    header = next((line for line in text.splitlines() if "gate_id" in line and "requirement" in line), "")
    columns = {cell.strip().lower() for cell in header.strip("|").split("|")}
    if not COMPLIANCE_COLUMNS.issubset(columns):
        return [finding("FAIL", "skill_compliance_audit_missing_columns", str(path))]
    return []


def check_algorithm_comparison(results: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    paths = list(results.rglob("algorithm_comparison_summary.csv"))
    if not paths:
        if not find_any(results, ["missing_tables.md"]):
            findings.append(finding("FAIL", "missing_algorithm_comparison_summary", str(results)))
        return findings
    for path in paths:
        try:
            with path.open(newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)
                columns = {name.strip() for name in (reader.fieldnames or [])}
                if not ALGORITHM_COMPARISON_COLUMNS.issubset(columns):
                    findings.append(finding("FAIL", "algorithm_comparison_missing_raw_reward_columns", str(path)))
                    continue
                for index, row in enumerate(reader, start=2):
                    value = (row.get("shaped_reward_used_for_claim") or "").strip().lower()
                    if value in {"true", "1", "yes", "y"}:
                        findings.append(finding("FAIL", "shaped_reward_used_for_claim", str(path), f"line={index}"))
        except OSError as exc:
            findings.append(finding("FAIL", "cannot_read_algorithm_comparison_summary", str(path), str(exc)))
    return findings


def check_claim_boundaries(md_files: list[Path], results: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    pattern = re.compile("|".join(re.escape(term) for term in HIGH_RISK_CLAIMS), re.IGNORECASE)
    for path in md_files:
        text = read_text(path)
        match = pattern.search(text)
        if match:
            findings.append(finding("WARN", "high_risk_claim_term", str(path.relative_to(results)), match.group(0)))
    return findings


def check_missing_notes(results: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for name in ("missing_figures.md", "missing_tables.md"):
        for path in results.rglob(name):
            text = read_text(path).lower()
            if "missing columns" not in text and "缺" not in text:
                findings.append(finding("WARN", "missing_note_lacks_column_reason", str(path)))
    return findings


def find_any(root: Path, patterns: list[str]) -> bool:
    return any(any(root.rglob(pattern)) for pattern in patterns)


def extract_markdown_links(text: str):
    for match in MARKDOWN_LINK_RE.finditer(text):
        yield match.group(1)


def normalize_markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1:target.index(">")]
    elif ' "' in target:
        target = target.split(' "', 1)[0]
    elif " '" in target:
        target = target.split(" '", 1)[0]
    return target.strip()


def is_external_or_anchor(target: str) -> bool:
    if target.startswith("#"):
        return True
    scheme = urlsplit(target).scheme.lower()
    return scheme in {"http", "https", "mailto", "tel"}


def is_absolute_local_link(target: str) -> bool:
    return Path(target).is_absolute() or bool(re.match(r"^[a-zA-Z]:[\\/]", target))


def strip_fragment_and_query(target: str) -> str:
    return target.split("#", 1)[0].split("?", 1)[0].strip()


def has_not_available_reason(text: str, category: str, tokens: tuple[str, ...]) -> bool:
    if "not available" not in text:
        return False
    window = re.compile(r"not available.{0,120}(" + "|".join(re.escape(token) for token in (category, *tokens)) + ")", re.IGNORECASE | re.DOTALL)
    reverse = re.compile(r"(" + "|".join(re.escape(token) for token in (category, *tokens)) + r").{0,120}not available", re.IGNORECASE | re.DOTALL)
    return bool(window.search(text) or reverse.search(text))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def finding(severity: str, finding_type: str, path: str, detail: str = "") -> dict[str, str]:
    item = {"severity": severity, "type": finding_type, "path": path}
    if detail:
        item["detail"] = detail
    return item


if __name__ == "__main__":
    main()
