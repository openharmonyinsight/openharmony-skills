# Skill 质量评测报告：ohos-dev-security-code-check

> 评测框架：Skill Judge（基于官方 Skill 提炼的 8 维度评测体系，满分 120 分）
> 评测对象：`skills/domain/security/development/ohos-dev-security-code-check/`
> 评测日期：2026-09-09

---

## 一、总览

| 指标 | 数值 |
|------|------|
| **总分** | **93 / 120（77.5%）** |
| **等级** | **B（良好 — 可用于生产的专家 Skill，有改进空间）** |
| **设计模式** | Tool 模式（脚本驱动 + 决策树 + 低自由度脆弱操作），融合轻量 Process 要素（5 步工作流） |
| **知识密度** | E:A:R ≈ 65:30:5（Expert:Activation:Redundant） |
| **一句话结论** | 将 C/C++ 可维护性检查从"拍脑袋看行数"外部化为有效行计数 + GN include 图谱遍历的脚本化检查，知识增量集中在"有效行"定义与循环依赖检测算法，满足 B 级入库门槛。 |

### 文件规模概览

| 目录 | 行数 | 说明 |
|------|------|------|
| `SKILL.md` | 102 | 核心文件，Agent 触发后加载（<500 行 ✓） |
| `references/` | 241（2 文件） | 重构指引 + 循环依赖参考 |
| `scripts/` | 1,031（2 文件） | scan_cpp_size.py（461 行）+ circular_header_check.py（570 行） |
| `evals/` | 496 | 5 个 case + 3 个 fixture 工作区 + 评测报告 |

---

## 二、各维度评分

| 维度 | 得分 | 满分 | 简评 |
|------|------|------|------|
| D1：知识增量 | 14 | 20 | "有效行"定义与 GN include 路径解析属专家知识；SKILL.md 本身知识密度偏低 |
| D2：思维范式 + 领域流程 | 11 | 15 | 5 步工作流清晰但偏机械；思维范式引导弱 |
| D3：反模式质量 | 7 | 15 | 无显式 NEVER 章节，反模式隐含在 references |
| D4：规范合规（尤其 description） | 13 | 15 | description 含 WHAT + WHEN 场景 + 关键词；metadata 完整 |
| D5：渐进式披露 | 11 | 15 | 两层结构清晰（SKILL.md + scripts/references）；缺 MANDATORY 触发标注 |
| D6：自由度校准 | 12 | 15 | 脚本调用低自由度合理；阈值配置给用户自由度恰当 |
| D7：模式识别 | 11 | 10 | Tool 模式选择正确，与任务脆弱性匹配（评分已封顶） |
| D8：实用可用性 | 14 | 15 | 决策树、阈值表、文件扩展名清单、重构指引表全覆盖 |

---

## 三、关键问题

**无阻塞性问题。** 该 Skill 可直接用于生产环境，满足入库 B 级要求。

---

## 四、Top 3 改进建议

### 建议 1：增加显式反模式章节

**问题**：SKILL.md 无 `## Anti-Patterns` 或 `NEVER` 章节。反模式知识（如"不要用 `wc -l` 当行数""不要把系统头文件算进模块依赖""不要为凑发现而建议风格性改动"）散落在 references 和脚本注释中，Agent 加载 SKILL.md 时不可见。

**改进**：在 SKILL.md 增加 `## Anti-Patterns` 章节，列 Top 5 NEVER：

```markdown
## Anti-Patterns

- NEVER 用 `wc -l` 或原始行数判断文件/函数大小——有效行排除空行、注释、预处理指令，脚本已实现该计数逻辑。
- NEVER 把 `#include <string>` 等系统头文件计入模块间循环依赖——循环检测仅针对项目内部目录模块。
- NEVER 在 clean-code 场景强行编造发现——无发现时应输出已验证检查类别 + 残余风险。
- NEVER 修改源文件来做重构——skill 只提供重构建议入口，不改代码。
- NEVER 跳过 GN 构建文件解析就做循环检测——include 路径依赖 GN 文件解析才能正确分组模块。
```

**预期收益**：D3 从 7 升至 ~12，反模式可见性提升，降低误用风险。

---

### 建议 2：为 references 大文件添加分段读取指引

**问题**：`scripts/scan_cpp_size.py`（461 行）和 `scripts/circular_header_check.py`（570 行）在 SKILL.md 中仅以"运行脚本"方式引用，未说明 Agent 是否需要读取脚本源码、读哪段。Agent 若完整读取 1,031 行脚本会消耗大量上下文。

**改进**：在 SKILL.md 的脚本引用处增加标注：

```markdown
## Size Analysis

scripts/scan_cpp_size.py <path> [options]
<!-- Agent 不需要读取脚本源码；脚本可执行，仅需按下方 Options 传参 -->
```

并在 references 引用处增加章节级指引：

```markdown
| Large functions | references/refactoring.md §1-§3（提取函数策略）|
| Circular dependencies | references/circular-deps.md §2（依赖反转模式）|
```

**预期收益**：减少 ~60% 脚本文件上下文消耗，D5 提升。

---

### 建议 3：补强思维范式引导

**问题**：5 步工作流（识别目标→确定检查类型→运行→展示→协助）偏机械执行，缺乏"怎么想"的引导。例如：何时该同时跑尺寸 + 循环检测？何时只跑其一？大规模仓库如何分批？

**改进**：在 Workflow 前增加简短决策引导：

```markdown
## Check Type Decision

- 用户只问"文件太大/函数太长" → 仅运行 scan_cpp_size.py
- 用户只问"循环依赖/模块耦合" → 仅运行 circular_header_check.py
- 用户问"代码质量/可维护性"（默认） → 两者都跑
- 仓库 >500 文件 → 建议分目录批次扫描，避免单次扫描超时
```

**预期收益**：D2 从 11 升至 ~13，思维范式与领域流程更平衡。

---

## 五、详细分析

### D1：知识增量（14/20）— 中上

**专家知识示例**：

| 知识点 | 位置 | 价值 |
|--------|------|------|
| "有效行"定义（排除空行、注释、预处理指令） | SKILL.md L98 | Claude 默认用 `wc -l`，不知道"effective lines"语义 |
| C/C++ 文件扩展名全集（.inl/.inc/.hxx/.c++ 等 12 种） | SKILL.md L101 | 比常见认知更全 |
| GN 构建文件（BUILD.gn/*.gni）解析 include 路径 | scripts | 循环检测依赖此映射，属 OpenHarmony 构建系统知识 |
| src/ 和 include/ 视为同一组件的分组规则 | SKILL.md L73 | 模块边界判定逻辑，Claude 不会自发推导 |

**扣分点**：SKILL.md 本体知识密度偏低（102 行中约 40% 是命令示例和表格），真正的专家知识集中在 scripts 和 references 中，Agent 若不读 references 则知识增量有限。

### D2：思维范式 + 领域流程（11/15）— 合格

**领域流程**：5 步工作流清晰（识别→确定→运行→展示→协助），最后"Offer help"步连接到重构协助是好的闭环。

**思维范式弱项**：缺乏"何时跑两者、何时跑其一、大规模仓库怎么办"的决策引导。工作流更接近"机械执行步骤"而非"引导思考"。

### D3：反模式质量（7/15）— 主要短板

无显式 NEVER 章节。反模式隐含在 references（refactoring.md 有"避免过早抽象"等）和脚本逻辑中。Agent 加载 SKILL.md 时反模式不可见，无法在操作前规避常见误用。

这是本 Skill 的主要扣分项，但非阻塞性——脚本本身实现了正确逻辑，反模式缺失不会导致功能错误，只影响误用防护。

### D4：规范合规（13/15）— 良好

**Frontmatter 合规**：name/description/metadata（author/scope/stage/domain/capability/version/status/tags）完整，与目录位置一致 ✓

**description 分析**：

| 要素 | 内容 | 评价 |
|------|------|------|
| WHAT | "Scan C/C++ codebases for code quality issues including extra large files/functions and circular dependencies" | 功能清晰 ✓ |
| WHEN | 5 条触发场景（check file sizes/find oversized functions/detect circular dependencies/analyze code complexity/find code smells/identify maintainability issues） | 场景充分 ✓ |
| KEYWORDS | security, code-check, cpp, code-quality, circular-dependencies | 关键词适中 ✓ |

**扣分**：description 未说明"支持单个文件或整个目录扫描"（在正文中），但已在描述中覆盖核心场景。metadata.tags 与 website metadata 一致 ✓

### D5：渐进式披露（11/15）— 合格

**两层结构**：
- Layer 1：name + description（常驻）✓
- Layer 2：SKILL.md 102 行（触发后加载）<500 行 ✓
- Layer 3：scripts（1,031 行）+ references（241 行）按需加载 ✓

**缺口**：SKILL.md 未标注哪些文件"Agent 必须读"、哪些"仅人类参考"、哪些"脚本可执行不需读源码"。脚本文件（461+570 行）是否需要 Agent 读取源码不明确，存在上下文浪费风险。

### D6：自由度校准（12/15）— 良好

| 任务类型 | 自由度 | 评价 |
|----------|--------|------|
| 脚本执行（脆弱） | 低 | 精确命令 + 参数 ✓ |
| 阈值配置 | 中 | 给用户选择空间，附默认值 rationale ✓ |
| 重构建议 | 中 | 引用 references，不自动改代码 ✓ |
| 检查类型选择 | 中 | 默认两者都跑，用户可指定 ✓ |

**扣分**：大规模仓库分批策略未约束自由度（无"建议分批"指引），可能导致 Agent 对超大树一次性扫描超时。

### D7：模式识别（11/10）— 封顶

**Tool 模式对照**：

| 特征 | 体现 |
|------|------|
| 脚本驱动 | scan_cpp_size.py / circular_header_check.py |
| 决策树 | 检查类型选择 + 重构指引表 |
| 低自由度 | 精确命令、参数、默认阈值 |
| 代码示例 | 完整 bash 示例含 -o/-f/-F 参数 |

Tool 模式选择正确：任务脆弱性高（扫描结果必须可复现）→ 低自由度脚本驱动。评分封顶于满分。

### D8：实用可用性（14/15）— 全面

| 可用性要素 | 覆盖 | 评价 |
|-----------|------|------|
| 决策树 | 检查类型选择；重构指引表 | ✓ |
| 代码示例 | 两个脚本的完整 bash 调用示例 | ✓ |
| 阈值表 | "What Counts as Large?" 表含默认值 + rationale | ✓ |
| 文件扩展名 | 全 12 种 C/C++ 扩展名列出 | ✓ |
| 边缘场景 | 可配置阈值、跳过 GN（--no-gn）、输出文件 | ✓ |
| 重构闭环 | 发现→引用 references→询问是否重构 | ✓ |

**轻微缺口**：无错误处理指引（脚本失败时怎么办），扣 1 分。

---

## 六、元问题检验

> **"该领域的专家看到这个 Skill，会说'这捕捉了我花多年才学会的知识'吗？"**

**部分会。** 以下知识有专家价值：

1. **"有效行"而非原始行**——这是代码质量度量中常被忽略的区分
2. **GN 构建文件解析 include 路径**——OpenHarmony 构建系统专属
3. **src/ 和 include/ 同组件分组**——模块边界判定逻辑
4. **12 种 C/C++ 扩展名全集**——比常见认知更全

但 SKILL.md 本体知识密度偏低，专家知识集中在脚本实现中。若 Agent 只加载 SKILL.md 不读脚本，知识增量有限。这符合 Tool 模式特征（脚本承载知识，SKILL.md 是调用入口），但仍使 D1 评分受限于"SKILL.md 可见知识"。

---

## 七、与官方模式对照

| 模式 | ~行数 | 契合度 |
|------|-------|--------|
| Tool | ~300 | ✓ 主模式（脚本驱动、决策树、低自由度） |

本 Skill 以 **Tool 模式**为主，102 行 SKILL.md + 脚本实现，模式选择与任务特征（可复现的静态扫描）高度匹配。

---

## 八、最终结论

**93/120（77.5%，B 级）**——满足入库 B 级要求，可用于生产环境。

核心价值：将 C/C++ 可维护性检查从主观判断外部化为有效行计数 + include 图谱遍历的脚本化检查，反模式章节缺失是主要短板但非阻塞性。三条改进建议（显式反模式、分段读取指引、思维范式引导）可提升至 B+/A-，但不影响当前入库资格。

该 Skill 通过 Skill Judge B 级检验。
