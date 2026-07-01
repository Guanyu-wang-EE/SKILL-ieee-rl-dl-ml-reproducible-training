#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
目的：验证单个 RL/DRL run folder 是否包含技能要求的 trace 文件。
创建日期：2026-06-29.
输入文件/CSV：run folder，必要时读取 progress.csv、eval_episodes.csv 等。
输出文件：stdout 校验结果和进程退出码。
依赖脚本/模块：Python 标准库。
运行示例：python scripts/validate_run_trace.py runs/example --require-eval
复现说明：只做结构与 schema 冒烟检查，不替代科学 gate。
'''

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    'config.json',
    'run_command.txt',
    'progress.csv',
    'episodes.csv',
    'updates.csv',
    'summary.json',
    'stdout.log',
]

EVAL_REQUIRED_FILES = [
    'eval_config.json',
    'eval_command.txt',
    'eval_episodes.csv',
    'eval_summary.json',
]

PROGRESS_REQUIRED_COLUMNS = [
    'timestamp',
    'algo',
    'seed',
    'env',
    'step',
    'episode',
    'reward',
    'cost',
    'violation',
    'actor_loss',
    'critic_loss',
    'fps',
    'elapsed_sec',
]

ALPHA_LAMBDA_OPTIONS = ['alpha', 'lambda', 'alpha_lambda']
FINAL_MODEL_KEYS = ['final_model_file', 'model_file', 'policy_file', 'actor_file', 'final_policy_file']


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Validate required trace artifacts for one RL/DRL run folder.')
    parser.add_argument('run_folder', type=Path, help='Run folder to validate')
    parser.add_argument('--require-eval', action='store_true', help='Require eval_config/eval_command/eval_episodes/eval_summary artifacts')
    return parser.parse_args()


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def load_csv(path: Path, failures: list[str]) -> list[dict[str, str]]:
    try:
        with path.open('r', encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                fail(f'{path.name}: missing header', failures)
                return []
            return list(reader)
    except Exception as exc:  # noqa: BLE001 - validation should report all readable failures.
        fail(f'{path.name}: cannot read CSV: {exc}', failures)
        return []


def load_json(path: Path, failures: list[str]) -> Any:
    try:
        with path.open('r', encoding='utf-8-sig') as handle:
            return json.load(handle)
    except Exception as exc:  # noqa: BLE001 - validation should report malformed JSON.
        fail(f'{path.name}: invalid JSON: {exc}', failures)
        return None


def numeric_is_bad(value: str) -> bool:
    text = str(value).strip()
    if text == '':
        return False
    lowered = text.lower()
    if lowered in {'nan', '+nan', '-nan', 'inf', '+inf', '-inf', 'infinity', '+infinity', '-infinity'}:
        return True
    try:
        number = float(text)
    except ValueError:
        return False
    return math.isnan(number) or math.isinf(number)


def validate_progress(path: Path, failures: list[str]) -> None:
    rows = load_csv(path, failures)
    if not rows:
        fail('progress.csv: no data rows', failures)
        return

    columns = set(rows[0].keys())
    missing = [column for column in PROGRESS_REQUIRED_COLUMNS if column not in columns]
    if missing:
        fail('progress.csv: missing required columns: ' + ', '.join(missing), failures)

    if not any(column in columns for column in ALPHA_LAMBDA_OPTIONS):
        fail('progress.csv: missing alpha/lambda column', failures)

    for field in ['algo', 'seed', 'env']:
        if field in columns:
            values = {row.get(field, '') for row in rows if row.get(field, '') != ''}
            if len(values) > 1:
                fail(f'progress.csv: inconsistent {field}: ' + ', '.join(sorted(values)), failures)

    previous_step = None
    for index, row in enumerate(rows, start=2):
        if not row.get('timestamp'):
            fail(f'progress.csv: missing timestamp at line {index}', failures)
        step_text = row.get('step', '')
        if step_text != '':
            try:
                step = float(step_text)
            except ValueError:
                fail(f'progress.csv: nonnumeric step at line {index}', failures)
                step = None
            if step is not None:
                if previous_step is not None and step < previous_step:
                    fail(f'progress.csv: step decreases at line {index}', failures)
                previous_step = step
        for column, value in row.items():
            if numeric_is_bad(value):
                fail(f'progress.csv: NaN/Inf in {column} at line {index}', failures)


def has_named_checkpoint(checkpoint_dir: Path, prefix: str) -> bool:
    return any(path.name.lower().startswith(prefix) for path in checkpoint_dir.iterdir())


def validate_checkpoints(run_folder: Path, config: Any, failures: list[str]) -> None:
    checkpoint_dir = run_folder / 'checkpoints'
    if not checkpoint_dir.exists() or not checkpoint_dir.is_dir():
        fail('missing required checkpoint directory: checkpoints', failures)
        return
    if not any(checkpoint_dir.iterdir()):
        fail('checkpoints: directory is empty', failures)
        return
    if not has_named_checkpoint(checkpoint_dir, 'latest'):
        fail('checkpoints: missing latest* checkpoint', failures)
    if not has_named_checkpoint(checkpoint_dir, 'best'):
        fail('checkpoints: missing best* checkpoint', failures)

    actor = run_folder / 'actor.pt'
    if actor.exists():
        return

    replacement = None
    if isinstance(config, dict):
        for key in FINAL_MODEL_KEYS:
            value = config.get(key)
            if isinstance(value, str) and value.strip():
                replacement = value.strip()
                break
    if replacement is None:
        fail('missing final actor.pt or config final model replacement', failures)
        return

    replacement_path = Path(replacement)
    if not replacement_path.is_absolute():
        replacement_path = run_folder / replacement_path
    if not replacement_path.exists():
        fail(f'configured final model replacement does not exist: {replacement}', failures)


def validate_nonempty_file(path: Path, failures: list[str]) -> None:
    if path.exists() and path.is_file() and path.stat().st_size == 0:
        fail(f'{path.name}: file is empty', failures)


def validate_eval(run_folder: Path, require_eval: bool, failures: list[str]) -> None:
    eval_present = any((run_folder / name).exists() for name in EVAL_REQUIRED_FILES)
    if not require_eval and not eval_present:
        return
    for filename in EVAL_REQUIRED_FILES:
        path = run_folder / filename
        if not path.exists():
            fail(f'missing required eval file: {filename}', failures)

    eval_config_path = run_folder / 'eval_config.json'
    eval_config = load_json(eval_config_path, failures) if eval_config_path.exists() else None
    if isinstance(eval_config, dict):
        policy_mode = str(eval_config.get('policy_mode') or eval_config.get('policy') or '').lower()
        if policy_mode not in {'deterministic', 'stochastic'}:
            fail('eval_config.json: policy_mode must be deterministic or stochastic', failures)
        if not (eval_config.get('test_seeds') or eval_config.get('seeds')):
            fail('eval_config.json: missing test_seeds/seeds', failures)
        if not (eval_config.get('checkpoint') or eval_config.get('checkpoint_source')):
            fail('eval_config.json: missing checkpoint/checkpoint_source', failures)

    eval_summary_path = run_folder / 'eval_summary.json'
    eval_summary = load_json(eval_summary_path, failures) if eval_summary_path.exists() else None
    if isinstance(eval_summary, dict) and 'feasible_rate' not in eval_summary:
        fail('eval_summary.json: missing feasible_rate', failures)

    for csv_name in ['eval_episodes.csv']:
        path = run_folder / csv_name
        if path.exists():
            rows = load_csv(path, failures)
            if not rows:
                fail(f'{csv_name}: no data rows', failures)


def main() -> int:
    args = parse_args()
    run_folder = args.run_folder
    failures: list[str] = []

    if not run_folder.exists() or not run_folder.is_dir():
        print(f'FAIL: run folder does not exist or is not a directory: {run_folder}')
        return 1

    for filename in REQUIRED_FILES:
        path = run_folder / filename
        if not path.exists():
            fail(f'missing required file: {filename}', failures)
        else:
            validate_nonempty_file(path, failures)

    config = load_json(run_folder / 'config.json', failures) if (run_folder / 'config.json').exists() else None
    if (run_folder / 'summary.json').exists():
        load_json(run_folder / 'summary.json', failures)

    validate_checkpoints(run_folder, config, failures)

    progress = run_folder / 'progress.csv'
    if progress.exists():
        validate_progress(progress, failures)

    for csv_name in ['episodes.csv', 'updates.csv']:
        path = run_folder / csv_name
        if path.exists():
            rows = load_csv(path, failures)
            if not rows:
                fail(f'{csv_name}: no data rows', failures)

    validate_eval(run_folder, args.require_eval, failures)

    if failures:
        print('FAIL')
        for item in failures:
            print(f'- {item}')
        return 1

    print('PASS: run trace is complete and internally consistent')
    return 0


if __name__ == '__main__':
    sys.exit(main())
