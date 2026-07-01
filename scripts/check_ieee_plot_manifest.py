#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
目的：验证 IEEE figure manifest 是否覆盖 PDF/SVG/PNG 导出、SHA256、数据源、生成命令、SVG 字体证据和矢量几何。
创建日期：2026-06-29.
输入文件/CSV：figure manifest JSON.
输出文件：stdout 校验结果和进程退出码。
依赖脚本/模块：Python 标准库。
运行示例：python scripts/check_ieee_plot_manifest.py figures/manifest.json
复现说明：只做图件清单与导出质量 smoke audit，不替代人工视觉审查。
'''

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


REQUIRED_FORMATS = ['pdf', 'svg', 'png']
OPTIONAL_FORMATS = ['eps']
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

    if manifest.get('svg_vector_geometry_checked') is not True:
        failures.append('svg_vector_geometry_checked must be true')
    validate_svg_geometry(svg_path, svg_text, failures)


def validate_svg_geometry(svg_path: Path, svg_text: str, failures: list[str]) -> None:
    try:
        root = ET.fromstring(svg_path.read_text(encoding='utf-8', errors='ignore'))
    except Exception as exc:  # noqa: BLE001 - report malformed SVG.
        failures.append(f'invalid SVG XML: {exc}')
        return

    if not root.tag.lower().endswith('svg'):
        failures.append('SVG root element is not svg')

    view_box = root.attrib.get('viewBox') or root.attrib.get('viewbox')
    if view_box:
        values = parse_numbers(view_box)
        if len(values) >= 4 and (values[2] <= 0 or values[3] <= 0):
            failures.append('SVG viewBox has nonpositive width or height')

    vector_tags = ('<path', '<polyline', '<polygon', '<line', '<rect', '<circle', '<ellipse')
    if not any(tag in svg_text for tag in vector_tags):
        failures.append('SVG has no vector geometry tags')
    if '<image' in svg_text and not any(tag in svg_text for tag in ('<path', '<polyline', '<line')):
        failures.append('SVG appears raster-only')

    path_values = []
    for match in re.finditer(r'\sd=["\']([^"\']+)["\']', svg_text):
        path_values.extend(parse_numbers(match.group(1)))
    for match in re.finditer(r'\spoints=["\']([^"\']+)["\']', svg_text):
        path_values.extend(parse_numbers(match.group(1)))
    if not path_values:
        failures.append('SVG lacks path/polyline numeric geometry')
        return
    if not all(math.isfinite(value) for value in path_values):
        failures.append('SVG path/polyline geometry contains nonfinite coordinates')
    if max(path_values) == min(path_values):
        failures.append('SVG path/polyline geometry has zero numeric range')


def parse_numbers(text: str) -> list[float]:
    values = []
    for item in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', text):
        try:
            values.append(float(item))
        except ValueError:
            continue
    return values


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

    for fmt in OPTIONAL_FORMATS:
        value = files.get(fmt)
        if not value:
            continue
        path = as_path(base, value)
        if not path.exists():
            failures.append(f'file does not exist for optional {fmt}: {path}')
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
