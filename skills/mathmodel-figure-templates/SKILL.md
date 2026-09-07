---
name: mathmodel-figure-templates
description: Use this skill in MathModel projects when the user invokes /mathmodel-figure-templates or asks to reproduce a bundled scientific visualization template, including SHAP, raincloud, ROC, Taylor, correlation, circular, chord, land-temperature, model-comparison, weather-downscaling, Sankey, land-use, ecosystem-service, hotspot, Local Moran, landslide PDP, and biodiversity-atlas figures. It provides deterministic Python scripts, lawful runtime data, and previews bundled inside the skill.
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# MathModel Figure Templates

This skill ships with MathModel and contains ready-to-run Python/matplotlib scripts for the
figure templates exposed in the MathModel gallery and Improve workflow. Resolve paths relative to
the directory containing this `SKILL.md`; do not depend on a fixed home-directory or sandbox path.

## Fast Path

1. Match the requested chart in `references/figure-catalog.md`.
2. From the current project, run the renderer with the template id. Replace `<skill-directory>`
   with the actual directory containing this `SKILL.md`:

```bash
python3 "<skill-directory>/scripts/render_template.py" paired-raincloud --project "./绘图复刻"
```

3. The renderer copies the bundled template script into `绘图复刻/scripts/`, runs it there, and writes outputs to `绘图复刻/outputs/`.
4. Return the generated PNG/PDF/SVG paths and the copied script path to the user.

Use `--list` to show supported ids:

```bash
python3 "<skill-directory>/scripts/render_template.py" --list
```

## Output Contract

- Work under the current workspace unless the user gives another path.
- Default project folder: `绘图复刻`.
- Script path: `绘图复刻/scripts/make_<template>.py`.
- Outputs: `绘图复刻/outputs/<template>_replica.png`, `.pdf`, `.svg`.
- Use the bundled scripts as the first choice; edit the copied workspace script only when the user requests customization.
- The bundled scripts use deterministic simulated data. Do not claim simulated values reproduce a source study exactly.

## Template Ids

- `multiclass-shap-combo`
- `paired-raincloud`
- `cv-roc-ci`
- `taylor-diagram`
- `correlation-pairgrid`
- `prediction-marginal-grid`
- `rf-tpe-surface`
- `grouped-corr-split-violin`
- `grouped-circular-heatmap`
- `urban-park-cooling-combo`
- `nature-chord-diagram`
- `land-diurnal-lst-maps`
- `land-morphology-lst-linear`
- `land-morphology-lst-nonlinear`
- `land-diurnal-feature-importance`
- `land-shap-interactions`
- `land-model-prediction-comparison`
- `sr-weather-model-evaluation-map`
- `sr-weather-downscaling-map`
- `karst-es-sdg-sankey`
- `karst-land-use-scenarios`
- `karst-ecosystem-services-atlas`
- `karst-es-hotspot-scenarios`
- `esv-grid-zone-scenarios`
- `esv-local-moran-scenarios`
- `landslide-shap-decision-heatmaps`
- `landslide-pdp-interaction-grid`
- `biodiversity-global-delta-atlas`
- `biodiversity-global-correlation-atlas`

## Data-backed templates

- The SR-Weather templates copy a bundled SRTM elevation grid and Natural Earth country geometry; they require `scipy`, `cartopy`, and `shapely`.
- The Karst templates copy a southeastern-Yunnan boundary derivative, and the ESV templates copy a Ganjiang Upstream Basin boundary derivative.
- The biodiversity atlases copy a simplified Natural Earth public-domain world boundary.
- Data-backed SR-Weather, Karst, and ESV templates export TIFF in addition to PNG/PDF/SVG. Biodiversity atlases export PNG/PDF/SVG.
- Internal grids, classes, coefficients, and simulated measurements are deterministic reconstructions. Never present them as the source papers' measured values.

## When Customizing

If the user asks for changes, copy/run the nearest template first, then edit the copied file in `绘图复刻/scripts/`. Preserve:

- `MPLCONFIGDIR` before importing matplotlib.
- deterministic seeds for simulated data.
- PNG/PDF/SVG export.
- readable labels, legends, and high-DPI output.

Use `references/plot-recipes.md` for implementation patterns.
