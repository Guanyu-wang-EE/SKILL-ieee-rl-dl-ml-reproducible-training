#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Validate an IEEE figure manifest for exported files, SHA256 values,
data sources, generation command, generation time, and SVG font evidence.
'''

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FORMATS = ['pdf', 'eps', 'svg', 'png']
VALID_SVG_FONT_MODES = {'embedded', 'path_fallback'}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Validate an IEEE figure manifest.')
    parser.add_argument('manifest', type=Path, help='Manifest JSON path')
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def as_path(base: Path, value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    return base / path


def collect_hash(manifest: dict[str, Any], key: str) -> str | None:
    hashes = manifest.get('sha256') or manifest.get('hashes') or {}
    if isinstance(hashes, dict):
        value = hashes.get(key)
        if value:
            return str(value).lower()
    return None


def check_hash(path: Path, expected: str | None, label: str, failures: list[str]) -> None:
    if not expected:
        if label.startswith('data source'):
            source_index = label.rsplit(maxsplit=1)[-1]
            failures.append(f'missing sha256 for data source {source_index}')
            return
        failures.append(f'missing sha256 for {label}')
        return
    actual = sha256_file(path)
    if actual.lower() != expected.lower():
        if label.startswith('data source'):
            source_index = label.rsplit(maxsplit=1)[-1]
            failures.append(f'sha256 mismatch for data source {source_index}: expected {expected.lower()}, got {actual.lower()}')
            return
        failures.append(f'sha256 mismatch for {label}: expected {expected.lower()}, got {actual.lower()}')


def data_source_hash_for(manifest: dict[str, Any], path_text: str) -> str | None:
    data_sha256 = manifest.get('data_sha256') or manifest.get('data_hashes') or {}
    if isinstance(data_sha256, dict):
        return data_sha256.get(path_text) or data_sha256.get(Path(path_text).name)
    return None


def validate_data_sources(manifest: dict[str, Any], base: Path, failures: list[str]) -> None:
    data_sources = manifest.get('data_sources')
    if not data_sources:
        failures.append('missing data_sources')
        return
    if not isinstance(data_sources, list):
        failures.append('data_sources must be a list')
        return

    for index, item in enumerate(data_sources):
        if isinstance(item, dict):
            if not item.get('path'):
                failures.append(f'data source {index}: missing path')
                continue
            path_text = str(item['path'])
            expected = item.get('sha256')
        else:
            path_text = str(item)
            expected = data_source_hash_for(manifest, path_text)

        path = as_path(base, path_text)
        if not path.exists():
            failures.append(f'data source {index} does not exist: {path}')
            continue
        check_hash(path, str(expected).lower() if expected else None, f'data source {index}', failures)


def validate_svg(manifest: dict[str, Any], svg_path: Path, failures: list[str]) -> None:
    svg_font_mode = manifest.get('svg_font_mode')
    if svg_font_mode not in VALID_SVG_FONT_MODES:
        failures.append('svg_font_mode must be embedded or path_fallback')
        return

    if not manifest.get('font_family'):
        failures.append('missing font_family')
    if not manifest.get('svg_backend'):
        failures.append('missing svg_backend')
    if manifest.get('font_embedding_checked') is not True:
        failures.append('font_embedding_checked must be true')

    try:
        svg_text = svg_path.read_text(encoding='utf-8', errors='ignore').lower()
    except Exception as exc:  # noqa: BLE001 - validation should report malformed SVG reads.
        failures.append(f'cannot read SVG for font inspection: {exc}')
        return

    if svg_font_mode == 'embedded':
        if 'font-family' not in svg_text and '@font-face' not in svg_text and '<font' not in svg_text:
            failures.append('embedded SVG lacks font-family, @font-face, or font definition evidence')
    elif svg_font_mode == 'path_fallback':
        if not (manifest.get('conversion_toolchain') or manifest.get('svg_conversion_toolchain')):
            failures.append('path_fallback SVG requires conversion_toolchain')


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest
    failures: list[str] = []

    if not manifest_path.exists():
        print(f'FAIL: manifest does not exist: {manifest_path}')
        return 1

    try:
        with manifest_path.open('r', encoding='utf-8-sig') as handle:
            manifest = json.load(handle)
    except Exception as exc:  # noqa: BLE001 - validation should report malformed manifests.
        print(f'FAIL: invalid JSON: {exc}')
        return 1

    if not isinstance(manifest, dict):
        print('FAIL: manifest root must be a JSON object')
        return 1

    base = manifest_path.parent
    files = manifest.get('files')
    if not isinstance(files, dict):
        failures.append('missing files object')
        files = {}

    resolved_files: dict[str, Path] = {}
    for fmt in REQUIRED_FORMATS:
        value = files.get(fmt)
        if not value:
            failures.append(f'missing files.{fmt}')
            continue
        path = as_path(base, value)
        if not path.exists():
            failures.append(f'file does not exist for {fmt}: {path}')
            continue
        resolved_files[fmt] = path
        check_hash(path, collect_hash(manifest, fmt), fmt, failures)

    validate_data_sources(manifest, base, failures)

    for key in ['generation_command', 'generation_time']:
        if not manifest.get(key):
            failures.append(f'missing {key}')

    svg_path = resolved_files.get('svg')
    if svg_path:
        validate_svg(manifest, svg_path, failures)

    if failures:
        print('FAIL')
        for item in failures:
            print(f'- {item}')
        return 1

    print('PASS: IEEE figure manifest is complete and hashes match')
    return 0


if __name__ == '__main__':
    sys.exit(main())
