# Figure Template Catalog

Each id maps to a bundled script under `scripts/templates/`.

| id | script | figure |
| --- | --- | --- |
| `multiclass-shap-combo` | `make_multiclass_shap_combo.py` | 多分类 SHAP 柱状图与蜂群图组合图 |
| `paired-raincloud` | `make_paired_raincloud.py` | 配对云雨图 |
| `cv-roc-ci` | `make_cv_roc_ci.py` | 交叉验证 ROC 曲线与置信区间图 |
| `taylor-diagram` | `make_taylor_diagram.py` | 多模型评价泰勒图 |
| `correlation-pairgrid` | `make_correlation_pairgrid.py` | 数据分布、拟合线、置信区间、相关系数组合图 |
| `prediction-marginal-grid` | `make_prediction_marginal_grid.py` | 预测值与真实值边缘分布组合图 |
| `rf-tpe-surface` | `make_rf_tpe_surface.py` | TPE 优化 RF 模型 3D 曲面图 |
| `grouped-corr-split-violin` | `make_grouped_corr_split_violin.py` | 下三角相关矩阵 + 特征分组与半边小提琴图 |
| `grouped-circular-heatmap` | `make_grouped_circular_heatmap.py` | 分组环形热图 |
| `urban-park-cooling-combo` | `make_urban_park_cooling_combo.py` | 堆叠图 + 云雨图 + 箱线图组合图 |
| `nature-chord-diagram` | `make_nature_chord_diagram.py` | Nature 风格和弦图 |
| `land-diurnal-lst-maps` | `make_land_diurnal_lst_maps.py` | 昼夜与季节地表温度地图及分布组合图 |
| `land-morphology-lst-linear` | `make_land_morphology_lst_linear.py` | 城市形态指标与地表温度线性关系小多图 |
| `land-morphology-lst-nonlinear` | `make_land_morphology_lst_nonlinear.py` | 城市形态指标与地表温度非线性响应小多图 |
| `land-diurnal-feature-importance` | `make_land_diurnal_feature_importance.py` | 昼夜特征重要性气泡组合图 |
| `land-shap-interactions` | `make_land_shap_interactions.py` | 多面板 SHAP 交互效应图 |
| `land-model-prediction-comparison` | `make_land_model_prediction_comparison.py` | 多模型训练与测试预测对比图 |
| `sr-weather-model-evaluation-map` | `make_sr_weather_model_evaluation_map.py` | 韩国区域多模型 RMSE、R²、MBE 空间评估地图 |
| `sr-weather-downscaling-map` | `make_sr_weather_downscaling_map.py` | 约 25 km 到 1 km 的四季气温降尺度地图 |
| `karst-es-sdg-sankey` | `make_karst_es_sdg_sankey.py` | 生态系统服务—SDG target—SDG 三层桑基/河流图 |
| `karst-land-use-scenarios` | `make_karst_land_use_scenarios.py` | 三种 SSP 情景土地利用地图与局部放大图 |
| `karst-ecosystem-services-atlas` | `make_karst_ecosystem_services_atlas.py` | 历史年份与 2035 情景的四类生态系统服务地图图集 |
| `karst-es-hotspot-scenarios` | `make_karst_es_hotspot_scenarios.py` | 总生态系统服务与 Getis–Ord Gi* 冷热点情景地图 |
| `esv-grid-zone-scenarios` | `make_esv_grid_zone_scenarios.py` | 1990–2020 生态系统服务价值五级格网地图 |
| `esv-local-moran-scenarios` | `make_esv_local_moran_scenarios.py` | 1990–2020 四期局部空间自相关聚类地图 |
| `landslide-shap-decision-heatmaps` | `make_landslide_shap_decision_heatmaps.py` | 双组 SHAP 决策热图与模型输出曲线 |
| `landslide-pdp-interaction-grid` | `make_landslide_pdp_interaction_grid.py` | 单变量 PDP 与双变量交互等值图 |
| `biodiversity-global-delta-atlas` | `make_biodiversity_global_delta_atlas.py` | 全球分级地图、纬向剖面与 KDE 分布组合图 |
| `biodiversity-global-correlation-atlas` | `make_biodiversity_global_correlation_atlas.py` | 全球相关地图、纬向剖面与分区回归系数组合图 |

Prompts from MathModel should include `/mathmodel-figure-templates` and the human-readable figure title. The agent should convert that title to one of the ids above and call `scripts/render_template.py`.

The Land, SR-Weather, Karst, and ESV entries are original deterministic Python replicas promoted from Scibox. They reproduce reusable visual structure and evidence logic, not the papers' original measurements. Source provenance remains in the Scibox repository registry and is not bundled as publisher imagery. The Karst and Ganjiang Upstream Basin templates use bundled geoBoundaries-derived CHN ADM2 boundaries under PDDL 1.0.

The landslide and biodiversity entries are deterministic Python replicas promoted from Scibox. The biodiversity templates use a simplified Natural Earth public-domain boundary; all internal analytical values are reproducible reconstruction data.
