#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_MAP = {
    "multiclass-shap-combo": "make_multiclass_shap_combo.py",
    "paired-raincloud": "make_paired_raincloud.py",
    "cv-roc-ci": "make_cv_roc_ci.py",
    "taylor-diagram": "make_taylor_diagram.py",
    "correlation-pairgrid": "make_correlation_pairgrid.py",
    "prediction-marginal-grid": "make_prediction_marginal_grid.py",
    "rf-tpe-surface": "make_rf_tpe_surface.py",
    "grouped-corr-split-violin": "make_grouped_corr_split_violin.py",
    "grouped-circular-heatmap": "make_grouped_circular_heatmap.py",
    "urban-park-cooling-combo": "make_urban_park_cooling_combo.py",
    "nature-chord-diagram": "make_nature_chord_diagram.py",
    "land-diurnal-lst-maps": "make_land_diurnal_lst_maps.py",
    "land-morphology-lst-linear": "make_land_morphology_lst_linear.py",
    "land-morphology-lst-nonlinear": "make_land_morphology_lst_nonlinear.py",
    "land-diurnal-feature-importance": "make_land_diurnal_feature_importance.py",
    "land-shap-interactions": "make_land_shap_interactions.py",
    "land-model-prediction-comparison": "make_land_model_prediction_comparison.py",
    "sr-weather-model-evaluation-map": "make_sr_weather_model_evaluation_map.py",
    "sr-weather-downscaling-map": "make_sr_weather_downscaling_map.py",
    "karst-es-sdg-sankey": "make_karst_es_sdg_sankey.py",
    "karst-land-use-scenarios": "make_karst_land_use_scenarios.py",
    "karst-ecosystem-services-atlas": "make_karst_ecosystem_services_atlas.py",
    "karst-es-hotspot-scenarios": "make_karst_es_hotspot_scenarios.py",
    "esv-grid-zone-scenarios": "make_esv_grid_zone_scenarios.py",
    "esv-local-moran-scenarios": "make_esv_local_moran_scenarios.py",
    "landslide-shap-decision-heatmaps": "make_landslide_shap_decision_heatmaps.py",
    "landslide-pdp-interaction-grid": "make_landslide_pdp_interaction_grid.py",
    "biodiversity-global-delta-atlas": "make_biodiversity_global_delta_atlas.py",
    "biodiversity-global-correlation-atlas": "make_biodiversity_global_correlation_atlas.py",
}

ALIASES = {
    "shap": "multiclass-shap-combo",
    "multiclass-shap": "multiclass-shap-combo",
    "raincloud": "paired-raincloud",
    "roc": "cv-roc-ci",
    "cv-roc": "cv-roc-ci",
    "taylor": "taylor-diagram",
    "pairgrid": "correlation-pairgrid",
    "correlation": "correlation-pairgrid",
    "pred-true": "prediction-marginal-grid",
    "prediction": "prediction-marginal-grid",
    "surface": "rf-tpe-surface",
    "tpe": "rf-tpe-surface",
    "split-violin": "grouped-corr-split-violin",
    "circular-heatmap": "grouped-circular-heatmap",
    "urban-cooling": "urban-park-cooling-combo",
    "chord": "nature-chord-diagram",
    "circos": "nature-chord-diagram",
    "diurnal-lst": "land-diurnal-lst-maps",
    "morphology-linear": "land-morphology-lst-linear",
    "morphology-nonlinear": "land-morphology-lst-nonlinear",
    "feature-importance": "land-diurnal-feature-importance",
    "shap-interactions": "land-shap-interactions",
    "model-comparison": "land-model-prediction-comparison",
    "weather-evaluation-map": "sr-weather-model-evaluation-map",
    "weather-downscaling-map": "sr-weather-downscaling-map",
    "sr-weather-figure-2": "sr-weather-model-evaluation-map",
    "sr-weather-figure-5": "sr-weather-downscaling-map",
    "es-sdg": "karst-es-sdg-sankey",
    "karst-sankey": "karst-es-sdg-sankey",
    "karst-land-use": "karst-land-use-scenarios",
    "karst-es-atlas": "karst-ecosystem-services-atlas",
    "karst-hotspot": "karst-es-hotspot-scenarios",
    "esv-zones": "esv-grid-zone-scenarios",
    "lisa-map": "esv-local-moran-scenarios",
    "local-moran": "esv-local-moran-scenarios",
    "shap-decision-heatmap": "landslide-shap-decision-heatmaps",
    "pdp-interaction": "landslide-pdp-interaction-grid",
    "global-delta-atlas": "biodiversity-global-delta-atlas",
    "global-correlation-atlas": "biodiversity-global-correlation-atlas",
}

CJK_HINTS = {
    "多分类": "multiclass-shap-combo",
    "shap交互": "land-shap-interactions",
    "shap": "multiclass-shap-combo",
    "云雨": "paired-raincloud",
    "roc": "cv-roc-ci",
    "泰勒": "taylor-diagram",
    "相关矩阵组合": "correlation-pairgrid",
    "拟合线": "correlation-pairgrid",
    "模型预测对比": "land-model-prediction-comparison",
    "预测": "prediction-marginal-grid",
    "真实": "prediction-marginal-grid",
    "tpe": "rf-tpe-surface",
    "曲面": "rf-tpe-surface",
    "半边小提琴": "grouped-corr-split-violin",
    "环形热图": "grouped-circular-heatmap",
    "城市公园": "urban-park-cooling-combo",
    "堆叠": "urban-park-cooling-combo",
    "和弦": "nature-chord-diagram",
    "circos": "nature-chord-diagram",
    "昼夜地表温度": "land-diurnal-lst-maps",
    "形态线性": "land-morphology-lst-linear",
    "形态非线性": "land-morphology-lst-nonlinear",
    "特征重要性": "land-diurnal-feature-importance",
    "气象模型评估地图": "sr-weather-model-evaluation-map",
    "气象超分辨率": "sr-weather-downscaling-map",
    "天气降尺度": "sr-weather-downscaling-map",
    "生态系统服务与sdg": "karst-es-sdg-sankey",
    "喀斯特土地利用": "karst-land-use-scenarios",
    "生态系统服务图集": "karst-ecosystem-services-atlas",
    "喀斯特热点": "karst-es-hotspot-scenarios",
    "生态系统服务价值分级": "esv-grid-zone-scenarios",
    "局部空间自相关": "esv-local-moran-scenarios",
    "局部莫兰": "esv-local-moran-scenarios",
    "shap决策热图": "landslide-shap-decision-heatmaps",
    "pdp交互": "landslide-pdp-interaction-grid",
    "双变量交互等值图": "landslide-pdp-interaction-grid",
    "全球温度差异图集": "biodiversity-global-delta-atlas",
    "全球相关地图": "biodiversity-global-correlation-atlas",
}

KOREA_DATA_TEMPLATE_IDS = {
    "sr-weather-model-evaluation-map",
    "sr-weather-downscaling-map",
}

KARST_DATA_TEMPLATE_IDS = {
    "karst-land-use-scenarios",
    "karst-ecosystem-services-atlas",
    "karst-es-hotspot-scenarios",
}

GUB_DATA_TEMPLATE_IDS = {
    "esv-grid-zone-scenarios",
    "esv-local-moran-scenarios",
}

WORLD_DATA_TEMPLATE_IDS = {
    "biodiversity-global-delta-atlas",
    "biodiversity-global-correlation-atlas",
}

DATA_TEMPLATE_IDS = KOREA_DATA_TEMPLATE_IDS | KARST_DATA_TEMPLATE_IDS | GUB_DATA_TEMPLATE_IDS

TIFF_TEMPLATE_IDS = DATA_TEMPLATE_IDS | {"karst-es-sdg-sankey"}


def normalize(value: str) -> str:
    value = value.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9\-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def resolve_template(value: str) -> str:
    raw = value.strip()
    key = normalize(raw)
    if key in SCRIPT_MAP:
        return key
    if key in ALIASES:
        return ALIASES[key]
    lowered = raw.lower()
    for hint, template_id in CJK_HINTS.items():
        if hint.lower() in lowered:
            return template_id
    raise SystemExit(
        f"Unknown template: {value}\nAvailable ids: " + ", ".join(sorted(SCRIPT_MAP))
    )


def output_suffixes(template_id: str) -> tuple[str, ...]:
    suffixes = (".png", ".pdf", ".svg")
    if template_id in TIFF_TEMPLATE_IDS:
        suffixes += (".tiff",)
    return suffixes


def prepare_template_assets(skill_root: Path, project: Path, template_id: str) -> None:
    if template_id in KOREA_DATA_TEMPLATE_IDS:
        source_data = skill_root / "assets" / "data" / "korea_srtm_dem.npz"
        target_data = project / "data" / source_data.name
        target_data.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_data, target_data)

        source_cartopy = skill_root / "assets" / "cartopy"
        target_cartopy = project / ".cartopy"
        shutil.copytree(source_cartopy, target_cartopy, dirs_exist_ok=True)

    if template_id in KARST_DATA_TEMPLATE_IDS:
        source_data = skill_root / "assets" / "data" / "karst_southeast_yunnan_boundary.json"
        target_data = project / "data" / source_data.name
        target_data.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_data, target_data)

    if template_id in GUB_DATA_TEMPLATE_IDS:
        source_data = skill_root / "assets" / "data" / "ganjiang_upstream_basin_boundary.json"
        target_data = project / "data" / source_data.name
        target_data.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_data, target_data)

    if template_id in WORLD_DATA_TEMPLATE_IDS:
        source_data = skill_root / "assets" / "data" / "natural_earth_world_simplified.geojson"
        target_data = project / "data" / source_data.name
        target_data.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_data, target_data)


def write_readme(project: Path, template_id: str, script_path: Path) -> None:
    readme = project / "README.md"
    output_stem = project / "outputs" / f"{script_path.stem.removeprefix('make_')}_replica"
    output_lines = "\n".join(
        f"- `{output_stem.with_suffix(suffix).as_posix()}`"
        for suffix in output_suffixes(template_id)
    )
    block = f"""
## {template_id}

Generated from the bundled MathModel figure-template skill.

```bash
python3 {script_path.as_posix()}
```

Outputs:

{output_lines}
""".strip()
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        marker = f"## {template_id}"
        if marker in text:
            return
        readme.write_text(text.rstrip() + "\n\n" + block + "\n", encoding="utf-8")
    else:
        readme.write_text("# 绘图复刻\n\n" + block + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a bundled MathModel figure template.")
    parser.add_argument("template", nargs="?", help="Template id, alias, or Chinese title fragment")
    parser.add_argument("--project", default="绘图复刻", help="Output project directory, default: 绘图复刻")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing copied workspace script")
    parser.add_argument("--list", action="store_true", help="List supported template ids")
    args = parser.parse_args()

    if args.list:
        for template_id in sorted(SCRIPT_MAP):
            print(template_id)
        return
    if not args.template:
        parser.error("template is required unless --list is used")

    template_id = resolve_template(args.template)
    skill_root = Path(__file__).resolve().parents[1]
    src = skill_root / "scripts" / "templates" / SCRIPT_MAP[template_id]
    if not src.exists():
        raise SystemExit(f"Bundled script missing: {src}")

    project = Path(args.project).expanduser().resolve()
    scripts_dir = project / "scripts"
    outputs_dir = project / "outputs"
    mpl_dir = project / ".mplconfig"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)
    mpl_dir.mkdir(parents=True, exist_ok=True)

    dst = scripts_dir / src.name
    if dst.exists() and not args.overwrite:
        print(f"Using existing workspace script: {dst}")
    else:
        shutil.copy2(src, dst)
        print(f"Copied template script: {dst}")

    prepare_template_assets(skill_root, project, template_id)

    result = subprocess.run([sys.executable, str(dst)], cwd=str(project), check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    write_readme(project, template_id, dst)

    stem = dst.stem.removeprefix("make_")
    for suffix in output_suffixes(template_id):
        path = outputs_dir / f"{stem}_replica{suffix}"
        print(path)


if __name__ == "__main__":
    main()
