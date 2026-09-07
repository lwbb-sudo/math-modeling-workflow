# Third-Party and Restricted-Material Notices

The repository's root `LICENSE` applies only to the original `math-modeling-workflow` orchestration skill, its installer/synchronization utilities, and documentation authored for this repository, unless a file or bundled directory states otherwise.

The `skills/` bundle contains components, datasets, templates, fonts, icons, examples, and other materials governed by their own notices. **The complete bundle is not uniformly MIT-licensed.** Users must follow the notice attached to each component.

## BZD companion skills and model dictionary

The bundled `bzd-*` skills come from the BZD mathematical-modeling skill collection. Attribution and use declarations embedded in those skills and assets must be retained.

In particular, `skills/bzd-model-dictionary/assets/model-dictionary.json` states, among other conditions:

- the material is produced, organized, and maintained by **BZD数模社**;
- it is limited to personal learning, mathematical-modeling competition research, and non-commercial exchange;
- commercial use, resale, paid redistribution, packaging into paid products, and marketing/traffic-acquisition use are prohibited;
- non-commercial redistribution must retain the `BZD数模社制作` attribution and the complete declaration;
- record-level `资料使用声明` fields are part of the notice and must not be removed.

The complete, controlling Chinese declaration remains embedded in the JSON file. This summary does not replace or weaken it. If the repository-level MIT license conflicts with that material's declaration, the BZD declaration controls for the BZD material.

## nature-figure

`skills/nature-figure` declares the Apache License 2.0. The complete license is preserved at:

- `skills/nature-figure/LICENSE.txt`

Its README and references describe source inspirations and bundled examples, including material related to the `figures4papers` project. Preserve the license, README, and source notices when redistributing or modifying this directory.

## paper-diagram and Tabler icons

`skills/paper-diagram` contains Tabler icon assets. The original attribution and license are preserved at:

- `skills/paper-diagram/ATTRIBUTION.md`
- `skills/paper-diagram/assets/icons/tabler/LICENSE`

The icon copyright belongs to its identified upstream author(s); the repository's MIT license does not replace the included icon license.

## mma-paper competition templates

`skills/mma-paper/assets/template/` contains LaTeX templates and class files from multiple competition communities and authors. Several class files include their own copyright, repository source, or LaTeX Project Public License (LPPL) terms. Those file-local notices remain controlling, including but not limited to templates for MCM/ICM and several Chinese mathematical-modeling competitions.

Do not remove copyright blocks, source URLs, LPPL text, font files, or template-local notices. Inclusion in this bundle does not claim authorship of those templates and does not relicense them under the repository's MIT license.

## mathmodel figure templates and data assets

`skills/mathmodel-figure-templates` includes rendering scripts, preview images, geographic boundaries, Natural Earth-derived shapefile data, and other example assets. Preserve attribution or provenance embedded in the files and comply with the terms of each underlying data source.

## General redistribution rule

When copying a single bundled skill, copy its entire directory so its `SKILL.md`, scripts, assets, licenses, and attribution files stay together. Do not infer that an absent top-level license file means a component is MIT-licensed. When in doubt, treat embedded notices and upstream terms as controlling and obtain permission before commercial redistribution.
