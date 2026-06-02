# IEEE Plot Style

Use this reference for figures intended to resemble IEEE Transactions on Smart Grid or IEEE Transactions on Power Systems. The goal is publishable scientific clarity, not visual decoration.

## Figure Geometry

| Item | Rule |
|---|---|
| Single-column width | About 3.45 in |
| Double-column width | About 7.16 in |
| Height | Choose by information density; do not stretch curves for appearance |
| Fonts | Prefer Times New Roman; otherwise use a serif font consistent with IEEE papers |
| Text size | Single-column figures about 8-9 pt; double-column figures about 8-10 pt |
| Axis labels | Slightly larger than tick labels |
| Code or file names | Do not place them inside final figures |

## Lines, Markers, And Colors

- Use a dark solid line for the main method.
- Use dashed or dash-dot lines for baselines.
- Use line widths around 1.2-1.8 pt.
- Use sparse markers; do not mark every sample.
- Use color-blind-friendly, low-saturation, clearly separated colors.
- Prefer a restrained black, blue, red, green, and purple palette.
- Check grayscale readability before treating a color plot as final.
- Avoid decorative gradients.

## Axes

- Use linear axes by default for reward, cost violation, constraint violation, and threshold sweeps.
- Use log axes only when values span multiple orders of magnitude and the paper/report interpretation benefits from it.
- Candidate log-axis metrics include loss, alpha/lambda, and gradient norm.
- Do not switch to log scale only because it looks better.
- Explain every log-axis choice in the report.

## Uncertainty And Seeds

- For multiple seeds, show mean plus/minus std or 95 percent confidence interval.
- State the number of seeds in the caption or report.
- Do not hide unstable seeds without a documented risk-gate or cleanup record.

## Legend, Grid, Ticks, Caption

- Put legends in unused interior space such as upper right or lower left when they do not cover curves.
- Move the legend outside above the plot when curves are dense.
- Keep legends quiet; they must not dominate the data.
- Use light gray, thin grid lines only as reading aids.
- Keep tick density readable at the target IEEE figure size.
- Do not write long explanatory sentences inside the figure.
- Put hypothesis, metric, threshold, and seed interpretation in the paper caption or `output.md`.

## Export And Manifest

Export final figures as:

- `PDF` for paper use.
- `EPS` for paper use when required.
- `SVG` with font information retained or embedded when the toolchain supports it.
- `PNG` only as a preview.

For SVG output, prefer genuine font-preserving or font-embedded SVG. If the plotting backend cannot truly embed fonts, use a path-converted SVG fallback and record `svg_font_mode=path_fallback` in the manifest. If fonts are retained or embedded, record `svg_font_mode=embedded`.

Each figure manifest must record:

- Figure file paths for PDF, EPS, SVG, and PNG preview.
- Data sources.
- SHA256 values for figure files and data sources.
- Generation command.
- Generation time.
- SVG font mode: `embedded` or `path_fallback`.
- Font family and SVG backend.
- `font_embedding_checked=true` after SVG contents or conversion logs have been inspected.
- Conversion toolchain when `svg_font_mode=path_fallback`.

Recommended manifest shape:

```text
{
  'files': {'pdf': 'plot.pdf', 'eps': 'plot.eps', 'svg': 'plot.svg', 'png': 'plot.png'},
  'sha256': {'pdf': '...', 'eps': '...', 'svg': '...', 'png': '...'},
  'data_sources': [{'path': 'data.csv', 'sha256': '...'}],
  'generation_command': 'python make_figures.py',
  'generation_time': '2026-06-03T12:00:00+08:00',
  'svg_font_mode': 'embedded',
  'font_family': 'Times New Roman',
  'svg_backend': 'matplotlib',
  'font_embedding_checked': true
}
```
