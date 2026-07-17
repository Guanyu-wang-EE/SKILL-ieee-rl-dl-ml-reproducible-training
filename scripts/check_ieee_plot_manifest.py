#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
目的：验证 IEEE figure manifest 是否覆盖科学语义、精确版式、最终尺寸目检、PDF/SVG/PNG、SHA256、SVG 字体证据和矢量几何。
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
VALID_LAYOUTS = {'single_column', 'double_column', 'custom'}
PROFILE_21PC = 'ieee_pes_single_column_21pc'
PNG_DIMENSION_TOL_PX = 2
PDF_DIMENSION_TOL_IN = 0.02
PROFILE_21PC_EXPECTED = {
    'width_in': 3.487,
    'axis_label_pt': 8.0,
    'tick_label_pt': 7.0,
    'legend_pt': 7.0,
    'main_line_width_pt': 1.2,
    'raw_line_width_pt': 0.32,
    'axis_line_width_pt': 0.65,
}


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


def parse_png_size(path: Path) -> tuple[int, int] | None:
    try:
        with path.open('rb') as handle:
            header = handle.read(24)
    except OSError:
        return None
    if len(header) < 24 or header[:8] != b'\x89PNG\r\n\x1a\n' or header[12:16] != b'IHDR':
        return None
    width = int.from_bytes(header[16:20], 'big')
    height = int.from_bytes(header[20:24], 'big')
    if width <= 0 or height <= 0:
        return None
    return width, height


def parse_pdf_media_box_size(path: Path) -> tuple[float, float] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if not data.startswith(b'%PDF'):
        return None
    pattern = re.compile(
        rb'/MediaBox\s*\[\s*'
        rb'([-+]?(?:\d*\.\d+|\d+))\s+'
        rb'([-+]?(?:\d*\.\d+|\d+))\s+'
        rb'([-+]?(?:\d*\.\d+|\d+))\s+'
        rb'([-+]?(?:\d*\.\d+|\d+))\s*\]'
    )
    for match in pattern.finditer(data):
        x0, y0, x1, y1 = (float(part) for part in match.groups())
        width_in = abs(x1 - x0) / 72.0
        height_in = abs(y1 - y0) / 72.0
        if width_in > 0 and height_in > 0:
            return width_in, height_in
    return None


def validate_export_dimensions(manifest: dict[str, Any], resolved_files: dict[str, Path], failures: list[str]) -> None:
    style = manifest.get('style_contract')
    if not isinstance(style, dict):
        return
    try:
        width_in = float(style.get('width_in'))
        height_in = float(style.get('height_in'))
        png_dpi = float(style.get('png_dpi'))
    except (TypeError, ValueError):
        return
    if not all(math.isfinite(value) and value > 0 for value in (width_in, height_in, png_dpi)):
        return

    png_path = resolved_files.get('png')
    if png_path:
        png_size = parse_png_size(png_path)
        if png_size is None:
            failures.append('PNG has invalid header or dimensions')
        else:
            actual_width, actual_height = png_size
            expected_width = round(width_in * png_dpi)
            expected_height = round(height_in * png_dpi)
            if abs(actual_width - expected_width) > PNG_DIMENSION_TOL_PX:
                failures.append(f'PNG width {actual_width}px does not match style contract {expected_width}px')
            if abs(actual_height - expected_height) > PNG_DIMENSION_TOL_PX:
                failures.append(f'PNG height {actual_height}px does not match style contract {expected_height}px')

    pdf_path = resolved_files.get('pdf')
    if pdf_path:
        pdf_size = parse_pdf_media_box_size(pdf_path)
        if pdf_size is None:
            failures.append('PDF is missing a readable positive MediaBox')
        else:
            actual_width, actual_height = pdf_size
            if abs(actual_width - width_in) > PDF_DIMENSION_TOL_IN:
                failures.append(f'PDF width {actual_width:.3f}in does not match style contract {width_in:.3f}in')
            if abs(actual_height - height_in) > PDF_DIMENSION_TOL_IN:
                failures.append(f'PDF height {actual_height:.3f}in does not match style contract {height_in:.3f}in')


def positive_number(mapping: dict[str, Any], key: str, label: str, failures: list[str]) -> float | None:
    value = mapping.get(key)
    try:
        number = float(value)
    except (TypeError, ValueError):
        failures.append(f'{label}.{key} must be a positive number')
        return None
    if not math.isfinite(number) or number <= 0:
        failures.append(f'{label}.{key} must be a positive finite number')
        return None
    return number


def validate_plot_contract(manifest: dict[str, Any], failures: list[str]) -> None:
    if manifest.get('plot_contract_version') != 1:
        failures.append('plot_contract_version must be 1')

    style = manifest.get('style_contract')
    if not isinstance(style, dict):
        failures.append('missing style_contract object')
        style = {}

    for key in ['profile', 'template_source', 'layout', 'grid_color']:
        if not style.get(key):
            failures.append(f'missing style_contract.{key}')
    if style.get('layout') not in VALID_LAYOUTS:
        failures.append('style_contract.layout must be single_column, double_column, or custom')
    if style.get('internal_title') is not False:
        failures.append('style_contract.internal_title must be false')

    numeric_style = {}
    for key in [
        'width_in',
        'height_in',
        'png_dpi',
        'axis_label_pt',
        'tick_label_pt',
        'legend_pt',
        'main_line_width_pt',
        'raw_line_width_pt',
        'axis_line_width_pt',
        'grid_line_width_pt',
        'grid_alpha',
    ]:
        numeric_style[key] = positive_number(style, key, 'style_contract', failures)
    grid_alpha = numeric_style.get('grid_alpha')
    if grid_alpha is not None and grid_alpha > 1:
        failures.append('style_contract.grid_alpha must be <= 1')

    palette = style.get('palette')
    if not isinstance(palette, list) or not palette:
        failures.append('style_contract.palette must be a nonempty list')
    elif any(not re.fullmatch(r'#[0-9A-Fa-f]{6}', str(color)) for color in palette):
        failures.append('style_contract.palette entries must be six-digit hex colors')

    if style.get('profile') == PROFILE_21PC:
        if style.get('layout') != 'single_column':
            failures.append(f'{PROFILE_21PC} requires single_column layout')
        for key, expected in PROFILE_21PC_EXPECTED.items():
            actual = numeric_style.get(key)
            if actual is not None and not math.isclose(actual, expected, rel_tol=0.0, abs_tol=0.005):
                failures.append(f'{PROFILE_21PC} requires style_contract.{key}={expected}')
        dpi = numeric_style.get('png_dpi')
        if dpi is not None and dpi < 600:
            failures.append(f'{PROFILE_21PC} requires style_contract.png_dpi>=600')

    scientific = manifest.get('scientific_contract')
    if not isinstance(scientific, dict):
        failures.append('missing scientific_contract object')
        scientific = {}
    for key in [
        'evidence_tier',
        'row_grain',
        'x_metric',
        'y_metric',
        'direction',
        'normalization_scope',
        'aggregation',
        'smoothing',
        'claim_boundary',
    ]:
        if not scientific.get(key):
            failures.append(f'missing scientific_contract.{key}')
    axis_limits = scientific.get('axis_limits')
    if not isinstance(axis_limits, list) or len(axis_limits) != 2:
        failures.append('scientific_contract.axis_limits must contain [lower, upper]')
    else:
        try:
            lower, upper = (float(value) for value in axis_limits)
            if not all(math.isfinite(value) for value in (lower, upper)) or lower >= upper:
                raise ValueError
        except (TypeError, ValueError):
            failures.append('scientific_contract.axis_limits must be finite and increasing')
    if scientific.get('no_clipped_valid_points') is not True:
        failures.append('scientific_contract.no_clipped_valid_points must be true')

    visual = manifest.get('visual_inspection')
    if not isinstance(visual, dict):
        failures.append('missing visual_inspection object')
        visual = {}
    for key in [
        'inspected_at_final_size',
        'no_overlap_or_clipping',
        'legend_clear',
        'grid_neutral',
        'color_and_grayscale_checked',
        'axis_limits_honest',
    ]:
        if visual.get(key) is not True:
            failures.append(f'visual_inspection.{key} must be true')


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
    validate_plot_contract(manifest, failures)
    validate_export_dimensions(manifest, resolved_files, failures)

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

    print('PASS: IEEE scientific/style contracts, exports, SVG evidence, and hashes are complete')
    return 0


if __name__ == '__main__':
    sys.exit(main())
