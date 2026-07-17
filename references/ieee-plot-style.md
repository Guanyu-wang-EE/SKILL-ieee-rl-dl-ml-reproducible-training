# IEEE Plot Style

Use this reference for IEEE Transactions on Smart Grid (TSG), IEEE Transactions on Power Systems (TPS), and IEEE Power & Energy Society (PES) paper figures. Treat style as a measurable scientific contract, not a cosmetic preference.

## Contents

1. Authority and failure lessons
2. Scientific figure contract
3. IEEE single-column profile
4. Curves, colors, axes, legends, and grids
5. Plot-type rules
6. Export and manifests
7. Mandatory figure gates

## Authority And Failure Lessons

Resolve conflicts in this order:

1. Project-supplied official IEEE/venue template and its measured column geometry.
2. Experiment-specific frozen scientific contract and active stage/index.
3. Project figure contract or explicit user instruction.
4. This reference's defaults.
5. Generic plotting-library defaults.

Do not infer single- versus double-column layout from information density. Inspect the local template first. A user request for an IEEE figure does not authorize a double-column canvas.

The v5.6 cross-method closeout exposed these reusable failure modes:

- Approximate guidance such as “about 3.45 in,” “8–9 pt,” or “1.2–1.8 pt” leaves enough freedom to produce visibly inconsistent figures. Use exact constants once a template is available.
- A correct 600 dpi image can still be wrong if its physical canvas is double-column. Verify PDF width or pixel width divided by DPI.
- Judge figures at final paper size. A line that looks acceptable in a zoomed PNG may disappear after single-column scaling; an oversized line may dominate.
- Do not mix style correction with metric invention. Fix row grain, direction, normalization population, aggregation, smoothing, and evidence tier before choosing colors.
- Per-method min-max normalization makes every method reach its own 100% and destroys cross-method plateau meaning. Use a shared normalization population or an explicitly declared common formal-test anchor; otherwise label the curve diagnostic-only.
- Endpoint-only values must not be stretched into smooth 4k learning curves. Preserve real training-progress observations and export the underlying points.
- Excessive smoothing erases learning dynamics; insufficient smoothing produces clipped, blocky traces. Export raw points, smooth only the display center line, declare the window/kernel, and retain visible real variation.
- Colored horizontal reference lines are easily mistaken for data. Use neutral grids; add a colored threshold only when scientifically necessary, labeled, and explained in the caption.
- Boxplot whiskers touching the top spine look clipped even when numerically valid. Leave headroom above the largest whisker.
- Hatching, separator lines, unequal opacity, or special treatment for one method creates visual bias. Apply the same box/line grammar to peers.
- Internal titles, footnotes, notes, filenames, and prose waste scarce single-column space. Put explanation in the paper caption. Retain only legends and structural `(a)`, `(b)`, `(c)` panel labels below multi-panel axes.
- `bbox_inches="tight"` can silently change the physical canvas. Use an exact figure size, manage margins explicitly, then verify the exported PDF/PNG dimensions.
- Calling a generic IEEE skill is not evidence of compliance. Record numeric geometry, inspect the rendered artifact, and pass every gate below.

## Scientific Figure Contract

Before plotting, write or identify a machine-readable contract with:

| Field | Required meaning |
|---|---|
| `figure_id` | Stable figure identifier |
| `evidence_tier` | training, validation, formal-test, diagnostic, or model-based |
| `data_sources` | Exact CSV/JSON/checkpoint paths and hashes |
| `row_grain` | One row means one episode, checkpoint-seed, scenario, timestamp, or other declared unit |
| `x_metric`, `y_metric` | Exact metric names and units |
| `direction` | higher-is-better, lower-is-better, or descriptive |
| `normalization_scope` | pooled methods/seeds/checkpoints, fixed external bounds, within-method, or none |
| `aggregation` | median/IQR, mean/CI, boxplot rule, or none |
| `smoothing` | kernel, window, causal/symmetric status, and center-line-only status |
| `axis_limits` | Numeric limits and evidence that no valid data are clipped |
| `no_clipped_valid_points` | Boolean assertion from data min/max or plotted-value checks |
| `claim_boundary` | What the figure proves and does not prove |

Fail before rendering if row grain, direction, normalization scope, or evidence tier is unknown. Do not connect independent scenarios, seeds, folds, or ranks as a time series.

For cross-method reward figures:

- Compare same-tier raw environment reward only when reward definitions and scales are identical.
- Keep incomparable shaped rewards diagnostic-only, preferably in separate panels.
- Use the frozen pooled Robust Operation Index (ROI) or formal-test `C_core` for formal performance claims when the experiment contract defines them.
- If a learning-attainment display is required, derive its shape from audited training progress and its plateau from one declared common anchor. Do not present it as raw reward, pooled ROI, or formal ranking.

## IEEE PES Single-Column Profile

Use the project template's measured dimensions. When the local IEEEtran/PES template specifies the validated 21 pc profile, use these exact defaults:

| Item | Exact default |
|---|---:|
| Canvas width | 3.487 in (21 pc project profile) |
| Standard single-panel height | 2.25 in |
| Tall/multi-panel height | Increase only as required; record the value |
| Font family | Times New Roman |
| Axis-label size | 8 pt |
| Tick-label size | 7 pt |
| Legend size | 7 pt |
| Main curve | 1.20 pt, solid |
| Raw/scenario trace | 0.32 pt, low opacity |
| Axis spines | 0.65 pt |
| Neutral grid | 0.45 pt, light gray, alpha about 0.5 |
| PNG preview | 600 dpi |
| Expected 600 dpi width | 2092 px after rounding |

Use double-column width only when the user, paper layout, or local template explicitly requires it. Never enlarge a single-column request to improve readability; simplify the figure instead.

Recommended Matplotlib base profile:

```python
IEEE_COLUMN_WIDTH_IN = 3.487
IEEE_LINE_FIGSIZE = (IEEE_COLUMN_WIDTH_IN, 2.25)
MAIN_LINE_WIDTH = 1.2
RAW_LINE_WIDTH = 0.32
AXIS_LINE_WIDTH = 0.65

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.linewidth": AXIS_LINE_WIDTH,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})
```

Use `fig.tight_layout(pad=0.35)` or explicit margins without changing the saved canvas. Verify that Times New Roman was actually resolved; record a serif fallback instead of silently claiming Times New Roman.

## Curves, Colors, Axes, Legends, And Grids

Use this color-blind-friendly, print-safe order unless the project already freezes colors:

| Role/order | Hex | Typical use |
|---|---|---|
| 1 | `#0077BB` | proposed/main method |
| 2 | `#EE7733` | first learned baseline |
| 3 | `#009988` | second learned baseline |
| 4 | `#CC3311` | controlled/vanilla baseline |
| 5 | `#666666` | model-based or neutral baseline |

Avoid weak pinks, neon colors, gradients, and rainbow palettes. Use the same method-color mapping in every figure and table preview. For episode curves at single-column size, prefer solid lines for all methods; introduce dashes or sparse markers only if grayscale inspection cannot distinguish them.

For training curves:

- Use `Training Episodes` on the horizontal axis when episodes are the actual x unit.
- Draw main center lines at 1.2 pt and raw/scenario traces at 0.32 pt with alpha about 0.08–0.15.
- Use uncertainty bands only for a declared population; alpha about 0.08–0.12 and no border is usually sufficient.
- Preserve all original points in an exported table. Apply smoothing only to the displayed center line.
- Prefer a causal rolling median for online-looking training progress; use symmetric Hann smoothing only as a declared post-hoc presentation variant.
- Do not smooth formal-test distributions, boxplots, thresholds, or values used for ranking.
- Use neutral light-gray grid lines. Remove colored horizontal lines unless they encode a necessary, labeled threshold.

For axes:

- Use metric-consistent units and direction. Never relabel a synthetic score as raw reward.
- Set limits from the contract and actual finite data. Add an assertion that all plotted values lie inside the chosen viewport.
- Remove unused headroom when it materially improves the single-column view, but keep honest ticks and document the occupied viewport.
- When a project explicitly defines a reward-equivalent score `R = S - 100`, use `Reward` and the contracted negative range; tightening `[-100, 0]` to `[-100, -20]` is valid only when no value exceeds `-20`.
- For normalized percentages, use `Normalized Reward` and percent ticks. Do not force each method independently to 100%. An occupied `0%..80%` viewport is valid for a formal-test-anchored diagnostic only when the contract and no-clipping assertion record it.
- Keep tick count readable at 3.487 in; four to six major y ticks is usually enough.

For legends:

- Use `frameon=False`.
- Prefer unused interior space; a two-column lower-center legend works when the lower region is empty.
- Do not cover curves, uncertainty bands, whiskers, or panel labels.
- Keep algorithm names scientifically exact and consistent across figures, tables, and reports.

## Plot-Type Rules

### Multi-Method Learning Curves

- Use the same 3.487 in canvas, font profile, palette, and method order across all episode-based figures.
- Show a gradual learning process only when supported by real progress data. Do not simulate intermediate progress from a final metric.
- Distinguish raw reward, shaped reward, normalized reward, ROI, and formal-test-anchored attainment in filenames, manifests, and captions.
- If reward definitions differ across algorithms, do not put native shaped rewards on one comparable-performance axis.

### Boxplots

- Build formal-test boxes from one auditable row per held-out scenario/seed. Do not substitute the final training checkpoint or an arbitrary tail of training episodes; state the scenario/seed count.
- Use one box per method with identical solid-fill treatment, black borders, median lines, and whisker grammar.
- Use the 1.5-IQR whisker rule unless the contract specifies another rule; state it in the caption.
- Show means with consistent open diamonds only when useful.
- Do not use hatch patterns, special shadows, group separators, background bands, or a grid.
- Set the upper axis limit above the largest whisker. For a 0–100 score whose whisker reaches 100, a 0–105 viewport with ticks ending at 100 is acceptable.
- If a model-based method has one deterministic value, show a point/short line rather than fabricating a distributional box.

### Tables Rendered As Figures

- Prefer native LaTeX/IEEE tables in the manuscript. Generate a figure preview only for review convenience.
- Keep result tables minimal: requested metrics and ranks only. Remove redundant `Pass`, `Train`, `Test`, `Role`, filenames, and prose already explained in the caption.
- Do not put internal titles, footnotes, or explanatory notes inside the preview.

### Multi-Panel Figures

- Use one shared style and aligned axes.
- Remove panel titles unless they are indispensable variable names.
- Place only `(a)`, `(b)`, `(c)` below the corresponding axes for manuscript cross-reference.
- Keep each panel legible at the final combined single-column size; otherwise split the figure.

## Export And Manifest

Export every final figure as:

- `PDF` for manuscript use;
- `SVG` for editable vector review;
- `PNG` at 600 dpi for visual inspection and Markdown preview;
- `EPS` only when explicitly required.

After export, verify:

- PDF physical width equals the contracted width, normally 3.487 in for this single-column profile, and the checker can read a positive MediaBox;
- PNG width and height match `style_contract.width_in * png_dpi` and `style_contract.height_in * png_dpi`, normally 2092 px wide at 600 dpi;
- PNG is not blank or clipped;
- SVG contains real finite vector geometry;
- fonts are embedded/retained or converted to paths with the mode recorded;
- same-stem PDF/SVG/PNG files exist;
- file and source-data SHA256 values match the manifest.

Each per-figure manifest must include the existing file/hash/font fields plus:

```text
{
  "plot_contract_version": 1,
  "files": {"pdf": "plot.pdf", "svg": "plot.svg", "png": "plot.png"},
  "sha256": {"pdf": "...", "svg": "...", "png": "..."},
  "data_sources": [{"path": "data.csv", "sha256": "..."}],
  "generation_command": "python make_figures.py",
  "generation_time": "2026-07-18T12:00:00+08:00",
  "font_family": "Times New Roman",
  "svg_backend": "matplotlib",
  "svg_font_mode": "embedded",
  "font_embedding_checked": true,
  "svg_vector_geometry_checked": true,
  "style_contract": {
    "profile": "ieee_pes_single_column_21pc",
    "template_source": "path/to/local/IEEEtran/template",
    "layout": "single_column",
    "width_in": 3.487,
    "height_in": 2.25,
    "png_dpi": 600,
    "axis_label_pt": 8,
    "tick_label_pt": 7,
    "legend_pt": 7,
    "main_line_width_pt": 1.2,
    "raw_line_width_pt": 0.32,
    "axis_line_width_pt": 0.65,
    "palette": ["#0077BB", "#EE7733", "#009988", "#CC3311", "#666666"],
    "grid_color": "#C7C7C7",
    "grid_line_width_pt": 0.45,
    "grid_alpha": 0.55,
    "internal_title": false
  },
  "scientific_contract": {
    "evidence_tier": "validation",
    "row_grain": "method-checkpoint-seed",
    "x_metric": "training_episode",
    "y_metric": "normalized_reward_percent",
    "direction": "higher_is_better",
    "normalization_scope": "declared pooled population",
    "aggregation": "median and IQR",
    "smoothing": "declared center-line-only rule",
    "axis_limits": [0, 100],
    "no_clipped_valid_points": true,
    "claim_boundary": "training-progress diagnostic; not formal ranking"
  },
  "visual_inspection": {
    "inspected_at_final_size": true,
    "no_overlap_or_clipping": true,
    "legend_clear": true,
    "grid_neutral": true,
    "color_and_grayscale_checked": true,
    "axis_limits_honest": true
  }
}
```

For final figure directories, produce `README.md`, `figure_quality_audit.md`, `figure_quality_audit.csv`, and `missing_figures.md`, or record why an item is unavailable.

## Mandatory Figure Gates

Advance only when the current gate is `PASS` from auditable evidence:

| Gate | Required evidence | Failure condition |
|---|---|---|
| F0 Scientific semantics | contract fields, source paths, row-grain check | unknown grain/direction/scope; fabricated or incomparable metric |
| F1 Template geometry | local template path, layout, width/height constants | guessed layout; single-column request rendered double-column |
| F2 Style constants | font, sizes, widths, palette, grid, legend plan | library defaults or approximate undocumented values |
| F3 Data integrity | finite counts, seed/scenario coverage, aggregation and smoothing checks | missing/duplicated rows; endpoint interpolation; hidden failed seeds |
| F4 Export | same-stem PDF/SVG/PNG, 600 dpi PNG, vector/font evidence | missing format; wrong physical width; raster-only SVG |
| F5 Machine audit | manifest checker, hashes, PDF/PNG dimensions, no-clipping assertions | any checker/hash/dimension/assertion failure |
| F6 Final-size visual QA | every paper-facing PNG/PDF inspected at 3.487 in | overlap, clipping, weak lines, excessive whitespace, misleading grid/reference lines |
| F7 Cross-artifact consistency | names, colors, units, ranks, captions, README/index | figure contradicts table, contract, or formal ranking |
| F8 Package closure | figure README, audit CSV/MD, missing notes, artifact index | unindexed or unexplained artifacts |

Run:

```bash
python scripts/check_ieee_plot_manifest.py path/to/figure_manifest.json
```

Do not mark the figure package complete from a successful script alone. F6 requires actual visual inspection of the rendered artifact at final paper size. Record every gate verdict and evidence path in `figure_quality_audit.csv`.
