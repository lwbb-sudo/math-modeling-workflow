# math-modeling-workflow

**交互式数学建模全流程工作流 + 完整离线配套技能套装**。

从题目 PDF 和附件出发，经过题意拆解、问题分析、建模路线比较、模型与算法选择、计算求解、图表制作，直到完整论文初稿与系统审查。每个小阶段暂停等你确认，所有关键研究决策由你来做。

> 设计原则：**AI 负责读题、整理信息、提出选项、解释差异和执行已确认的方案；你负责在每个关键决策点选择方向。**
>
> 本仓库现已把总控工作流及其全部显式递归依赖一起打包。克隆一次即可离线安装 24 个 Skill，不再要求从 app 安装目录逐个复制。

---

## ✨ 特性

- **全程参与**：14 个小阶段，每阶段完成一个任务后暂停，展示结果、证据、候选方案、推荐与风险；
- **对话内呈现**：候选路线、模型、算法和图表方案直接在对话中给出，不用文件替代决策过程；
- **差异化设计**：默认比较“稳健基线 / 机理与数据融合 / 差异化路线”；
- **完整技能套装**：总控 + 23 个配套技能，包含 BZD 检查器、MMA 论文模板、科研绘图、流程图、文献检索、数据检索和环境诊断；
- **完整运行资源**：包含 LaTeX 模板、字体、脚本、绘图预览、地理数据、图标和 BZD 模型字典；
- **状态与回滚**：保存已确认决策、被放弃方案、生成文件和未解决问题；
- **安全边界**：永不覆盖原始输入；外部数据、依赖安装和发布上传必须单独确认；不虚构文献、结果或 AI 使用记录。

完整套装约 **215 MiB 以上**（随上游资源更新而变化），其中主要体积来自 `mma-paper` 模板、`mathmodel-figure-templates` 和 `nature-figure`。

---

## 🔄 工作流总览

| 阶段 | 内容 | 暂停时你会看到 |
|---|---|---|
| 0 | 文件接收与完整性检查 | 文件清单、缺失/OCR 风险、能否开始分析 |
| 1 | 题目初读与结构识别 | 整题概览、研究对象、全部编号任务、歧义点 |
| 2 | 逐句拆题与完整性核验 | 逐句翻译表、术语口径表、各问输入—任务—输出、漏读审计 |
| 3 | 问题重述与问题分析 | 重述草稿、每问任务分类（预测/评价/优化/拟合等） |
| 4 | 总体路线与差异化比较 | ≥3 条候选路线对比表 + 推荐 |
| 5 | 逐问模型选择 | 每问多候选模型对比表 |
| 6 | 数据方案与外部数据决策 | 附件结构、异常/缺失/口径问题、外部数据候选源 |
| 7 | 算法选择 | 精确算法、数值方法、启发式与智能优化对比 |
| 8 | 实验与验证设计 | 基线、指标、消融、敏感性、验收标准 |
| 9 | 逐问建模与计算 | 每问结果、诊断、不确定性、验证结论 |
| 10 | 图表与可视化伴侣 | 图表类型、配色、布局与渲染结果 |
| 11 | 论文结构与逐章撰写 | 目录框架与逐章草稿 |
| 12 | 分项审查与修复 | 假设、求解、摘要、符号、参考文献、AI 声明问题清单 |
| 13 | 整篇评审与提交就绪 | 评分、风险、修改建议、最终文件清单 |

每个暂停节点使用：`已完成` → `当前理解` → `证据/数据/约束` → `候选方案` → `推荐及理由` → `创新空间与风险` → `下一阶段` → `请你选择`。

---

## 📦 套装内容（24 个 Skill）

### 总控

- `math-modeling-workflow`（仓库根 `SKILL.md`）

### 题意、建模与审查

- `bzd-problem-translator`
- `bzd-problem-restatement`
- `bzd-problem-analysis-checker`
- `bzd-modeling-ideas`
- `bzd-model-dictionary`
- `bzd-model-assumption-checker`
- `bzd-model-solution-checker`
- `bzd-abstract-checker`
- `bzd-symbol-notation-checker`
- `bzd-reference-appendix-checker`
- `bzd-ai-usage-disclosure`
- `bzd-review-paper`
- `bzd-paper-format-checker`

### 论文、图表、检索与环境

- `mma-paper`
- `mma-figure`
- `mma-review`
- `nature-figure`
- `mathmodel-figure-templates`
- `paper-diagram`
- `paper-search`
- `data-search`
- `metaheuristic-optimization`
- `doctor`

依赖和来源记录在 [`bundle/skills-manifest.json`](bundle/skills-manifest.json)。

---

## 🚀 一次性安装

本仓库无需构建，只需 Python 3.9+。

```bash
git clone https://github.com/lwbb-sudo/math-modeling-workflow.git
cd math-modeling-workflow
python scripts/install.py --dry-run
python scripts/install.py
```

默认安装到：

```text
~/.claude/skills/
```

也可显式指定任意宿主的技能根目录：

```bash
python scripts/install.py --target /path/to/skills
```

Windows 示例：

```powershell
python scripts/install.py --target "$env:USERPROFILE\.claude\skills"
```

安装器默认**不覆盖**已有同名技能。先查看冲突，确认确实要更新后再使用：

```bash
python scripts/install.py --target /path/to/skills --force
```

其他命令：

```bash
# 只列出套装中的 24 个技能
python scripts/install.py --list

# 只预览，不写文件
python scripts/install.py --target /path/to/skills --dry-run
```

安装完成后重启会话，输入：

```text
/math-modeling-workflow
```

并附上题目 PDF 和全部附件。

### mathmodel 桌面端

把 `scripts/install.py --target` 指向 mathmodel 当前使用的技能根目录，或通过 app 的技能导入入口逐个导入根技能与 `skills/` 下的目录。某些带 `.disabled-by-default` 上游标记的技能，在个别版本中仍可能需要在技能面板手动启用。

### Codex CLI

Codex 的 skill 目录通常为 `~/.codex/skills/`：

```bash
python scripts/install.py --target ~/.codex/skills
```

如果使用只读取单文件 prompt 的旧版 Codex，可继续单独把根 `SKILL.md` 放入其 prompts 目录；这种方式不会自动获得配套技能。

### 其他读取 AGENTS.md 的智能体

根目录的 `AGENTS.md` 是工作流正文版本。可复制到项目规则位置；如宿主支持技能目录，仍建议用安装器安装完整套装。

---

## 📁 仓库结构

```text
math-modeling-workflow/
├── SKILL.md                    # 总控技能
├── AGENTS.md                   # 供读取 AGENTS.md 的智能体使用
├── skills/                     # 23 个完整配套技能
│   ├── mma-paper/
│   ├── nature-figure/
│   ├── bzd-model-dictionary/
│   └── ...
├── bundle/
│   └── skills-manifest.json    # 来源、目标、依赖和许可备注
├── scripts/
│   ├── install.py              # 跨平台安装器
│   ├── sync-skills.py          # 从本机权威来源刷新套装
│   └── verify-bundle.py        # 完整性/依赖/许可/泄密检查
├── THIRD_PARTY_NOTICES.md
└── LICENSE                     # 仅覆盖仓库自有 MIT 部分
```

工作流实际启动后会为建模任务创建：

```text
数学建模项目/
├── input/
├── extracted/
├── analysis/
├── data/
├── code/
├── figures/
├── paper/
├── reviews/
└── workflow-state/
```

---

## 🔄 维护者：从本机 app 刷新套装

同步脚本默认自动定位 Windows 上的 mathmodel 内置技能与 BZD plugin 技能：

```bash
python scripts/sync-skills.py --dry-run
python scripts/sync-skills.py
```

也可覆盖来源根目录：

```bash
python scripts/sync-skills.py \
  --builtin-root /path/to/builtin-skills \
  --bzd-root /path/to/bzd-skills
```

同步会排除 `__pycache__`、`*.pyc`、日志、临时文件、嵌套 `.git` 和已知重复/处理报告；不会把本机绝对来源路径写进发布内容。

同步后运行：

```bash
python scripts/verify-bundle.py
```

验证器检查技能数量、frontmatter 名称、清单依赖闭包、关键模板/脚本/素材、BZD 声明、第三方许可、缓存、嵌套仓库、疑似密钥和本机绝对路径。

---

## ⚖️ 许可与再分发边界

根 [`LICENSE`](LICENSE) 的 MIT 许可只覆盖本仓库自有的总控、安装/同步/验证脚本和自有文档。`skills/` 中的第三方或受限材料按各自声明授权，**完整套装不能整体视为纯 MIT**。

尤其注意：

- `bzd-model-dictionary` 数据由 **BZD数模社**制作，声明仅限个人学习、数学建模竞赛研究和非商业交流，禁止商用、倒卖及引流；
- `nature-figure` 保留 Apache-2.0 许可证；
- `paper-diagram` 保留 Tabler Icons attribution 和许可证；
- `mma-paper` 的赛事模板与 `.cls` 文件可能受 LPPL、原作者版权或文件内其他声明约束；
- 地图、字体、预览和示例素材应继续遵循各自来源条款。

详见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) 以及每个技能目录内的原始声明。

---

## 📄 免责声明

工作流用于建模研究、竞赛辅助和学习交流。模型选择、数据合法性、结论正确性、竞赛合规性以及最终提交责任仍由使用者承担。请遵守对应比赛关于 AI 工具、引用、匿名和原创性的最新规定。
