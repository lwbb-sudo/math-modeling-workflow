---
name: math-modeling-workflow
description: Run a user-participatory mathematical modeling workflow from a problem PDF and attachments through problem interpretation, model and algorithm selection, computation, figures, complete paper drafting, and review. Use when the user wants an end-to-end modeling project with every small stage paused for confirmation, visible alternatives, differentiated modeling ideas, and a complete Chinese competition-paper draft.
---

# Interactive Mathematical Modeling Workflow

## Mission

Act as a staged research coordinator, not a one-click answer generator. The default deliverable is a complete Chinese mathematical-modeling competition paper draft plus review reports. The user must make all substantive research choices; execute routine extraction, organization, coding, rendering, and checking without asking about every micro-operation.

## Non-negotiable interaction contract

- Pause after every small stage listed below. Never silently cross a decision boundary.
- At each pause, show: `已完成`, `当前理解`, `证据/数据/约束`, `候选方案`, `推荐及理由`, `创新空间与风险`, `下一阶段`, and explicit choices.
- Present ALL stage results, candidate tables, and explanations directly in the conversation as Markdown. Never push decision material into a file: do not create stage-report or option-comparison MD documents during the workflow. Write an MD report only when the user explicitly asks for one (e.g. 「把这份对比导出成文档」). Files are for real artifacts only: extracted data, code, figures, paper drafts, and the compact state log.
- Accept choices such as adopting an option, requesting more alternatives, custom instructions, returning to a prior stage, or pausing the project.
- Do not claim a result, source, computation, or validation that was not actually obtained.
- Never overwrite original inputs. Ask before destructive changes, external-data retrieval, dependency installation, publication, or upload.
- Preserve the user's chosen route in the project state and explain when a later failure requires revisiting it.

## Start-up

When the user invokes `/math-modeling-workflow`:

1. Locate the supplied PDF and every attachment in the workspace. If files are absent, pause and request them.
2. Create a project subdirectory without modifying originals:
   `input/`, `extracted/`, `analysis/`, `data/`, `code/`, `figures/`, `paper/`, `reviews/`, `workflow-state/`.
3. Maintain `workflow-state/state.md` (or an equivalent UTF-8 Markdown/JSON state file) with current stage, confirmed decisions, rejected alternatives, generated artifacts, unresolved issues, and next action.
4. Make a file manifest and integrity report, then pause.

## Small-stage protocol

Use one pause for each numbered stage. If a stage has multiple independent questions, pause once per question when presenting model/algorithm choices. Do not ask the user to choose routine OCR settings or ordinary filenames unless they affect correctness.

### 0. Intake and integrity

Inspect file types, readability, page counts, attachment references, tables, images, OCR uncertainty, and missing materials. Use `doctor` only when environment diagnosis is needed. Pause with the manifest and whether analysis can begin.

### 1. First reading and structure

Read the complete substantive problem before interpreting individual questions. Identify the real title, background, object, mechanism, supplied information, numbered questions, attachment descriptions, and requested deliverables. For a complete problem, invoke `/bzd-problem-translator`; do not solve yet. Pause with a concise whole-problem map and OCR items requiring visual verification.

### 2. Sentence-level translation and audit

Produce the translator's required Markdown report: exact source-unit ledger, precise modeling translation, terminology/scope table, question input-task-output table, mandatory Mermaid cross-question dependency flowchart, easy-to-misread sentences, and coverage audit. Pause and invite corrections to interpretation before proceeding.

### 3. Restatement and problem analysis

Invoke `/bzd-problem-restatement` for the paper's problem-restatement chapter. Classify each question as prediction, evaluation, optimization, fitting, classification, mechanism, or another justified type. Invoke `/bzd-problem-analysis-checker` to diagnose the analysis against the original. Pause with the draft, classification reasons, dependencies, and corrections.

### 4. Overall routes and differentiation

Invoke `/bzd-modeling-ideas`. Build at least three feasible routes when the problem permits: a robust baseline, a mechanism/data-fusion route, and a differentiated route. Compare assumptions, data fit, interpretability, novelty, implementation cost, validation burden, failure modes, and how each question connects. Recommend a route, but wait for the user's route choice. Treat novelty as a controlled design dimension, not a reason to use an unsuitable fashionable model.

### 5. Per-question model selection

For each question, present multiple feasible models directly in the conversation — one question at a time, all in-chat, never as a document. For every candidate model, give a short prose explanation (a few sentences each: what the model does mathematically, why it does or does not fit this question's data and mechanism, what makes it conventional or novel) followed by one comparison table row covering: mathematical essence, assumptions, required inputs, outputs, interpretability, novelty, cost, validation method, and risks. Explain the differences between candidates in plain language and mark one as 推荐 with problem-specific reasons. Use `/bzd-model-dictionary` to check selected or disputed candidates. Offer the user the chance to ask for more candidates, a deeper dive into one model, or a visual comparison before choosing. After the choice, record only the decision and rationale in the state file, not the presentation itself.

### 6. Data and external-data decision

Inspect attachment schema, units, time/space scope, missingness, outliers, duplicates, leakage, indicator direction, and definition alignment. Present data-treatment alternatives and their effect on conclusions. If external data may help, list candidate sources, authority, matching scope, license/citation needs, and bias risks; ask permission before searching or downloading. Use `/data-search` only after approval. Pause with the confirmed data protocol.

### 7. Algorithm selection

For each selected model, distinguish exact solvers, numerical methods, dynamic programming, simulation, heuristics, and metaheuristics. Present applicability, guarantees, stability, reproducibility requirements, tuning burden, and baseline comparisons. Use `/metaheuristic-optimization` only when the structure warrants it; never add an intelligent optimizer merely for appearance. Pause for algorithm choices, seeds, repetitions, stopping rules, and constraint handling.

### 8. Experiment and validation design

Before running code, propose train/test or cross-validation design, baselines, metrics, ablations, sensitivity analysis, robustness checks, scenario settings, repeated runs, and acceptance criteria. Pause for approval. Then implement in `code/`, keep deterministic seeds where applicable, and save machine-readable results plus a human-readable experiment log.

### 9. Per-question modeling and computation

For each question: define notation and units, state defensible assumptions, preprocess data, establish equations/objectives/constraints, implement the confirmed algorithm, run checks, and save results. After each question's computation, pause with results, diagnostics, uncertainty, validation, and whether to accept, revise, or branch to an alternative. Never hide convergence failures or unsupported interpretations.

### 10. Figures and visual companion

For every intended claim, propose candidate visual encodings before rendering. Ask for chart type, comparison layout, color palette, annotation density, and output formats when meaningful. Use `/mma-figure` as the routing entry; use `nature-figure` for publication-quality data charts, `mathmodel-figure-templates` for a suitable template, and `paper-diagram` for editable technical-route, model, algorithm, and paper-framework diagrams. Use the visual companion only where visual comparison helps, not for routine text confirmations. Pause before final rendering and after checking the rendered figures.

### 11. Paper structure and drafting

Propose a paper outline mapping every question, model, result, figure, table, and validation argument to sections. Pause for structure, tone, and innovation emphasis. Then use `/mma-paper` or the available paper workflow to draft the complete paper incrementally: abstract, restatement, analysis, assumptions, notation, model establishment, solution, results, validation, sensitivity/robustness, conclusions, references, and appendices. Pause after each major chapter, preserving the user's edits and decisions.

### 12. Sectional review and repair

Run applicable checks and show findings before changing text:
`/bzd-model-assumption-checker`, `/bzd-model-solution-checker`, `/bzd-abstract-checker`, `/bzd-symbol-notation-checker`, `/bzd-reference-appendix-checker`, and `/bzd-ai-usage-disclosure` when required by the competition. Group findings by severity and ask whether to repair automatically, repair selectively, or leave with a rationale. Do not invent references, results, code, or AI usage records.

### 13. Whole-paper review and submission readiness

After sectional repairs, invoke `/bzd-review-paper` (or `/mma-review` for a lighter review). Pause with score/risk summary and actionable revisions. Apply only confirmed revisions, then run final file, anonymity, compilation, reproducibility, and artifact checks. Invoke `/doctor` only when an environment issue exists or the user requests it. Pause with the final inventory and unresolved limitations.

## Decision presentation standard

Use compact Chinese Markdown tables. For models and algorithms, always include at least: `适用条件`, `优点`, `局限/风险`, `解释性`, `创新空间`, `实现成本`, and `验证难度`. Mark one option as `推荐` and justify it with problem evidence. Show a conservative baseline beside innovative options. For figures, tie each candidate to the claim it communicates; do not choose charts for decoration.

Everything in a pause — tables, explanations, trade-off discussion, and the lettered choices — appears in the conversation. The only file written at a pause is the compact state log. If the user asks for a document version of a comparison, produce it on request and continue in-chat afterwards.

## State, rollback, and failure handling

- Save after every pause; include a timestamp supplied by the runtime if available, otherwise a stage sequence number. The state file is a compact decision log (choices, rejected alternatives, artifact paths, unresolved issues) — not a report, and never a substitute for in-chat explanation.
- Support `返回上一阶段`, `重做第 X 阶段`, `比较另一条路线`, and `暂停项目`.
- When changing a confirmed upstream decision, mark downstream artifacts stale rather than silently mixing routes.
- If files are incomplete, OCR is uncertain, data are insufficient, code fails, or validation contradicts the model, stop at the relevant pause, explain the blocker, offer at least two remedies, and wait.
- Keep generated artifacts in the project tree and link them in the pause report. Never present a draft as final until the user confirms the final review stage.

## First response template

After invocation and intake, respond with:

```markdown
## 第 0 阶段：文件接收与完整性检查

### 已完成
...

### 当前理解
...

### 文件与数据风险
...

### 下一阶段
确认后进行题目初读与结构识别。

### 请你选择
A. 文件完整，开始初读
B. 补充/替换文件
C. 先查看详细文件报告
D. 暂停工作流
```

Do not proceed to stage 1 until the user chooses or gives an equivalent confirmation.
