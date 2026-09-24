---
name: problem-diag
description: 工作流 Phase 7 ★ 逃生舱（任意阶段可切入）——诊断嵌入式 OS 适配过程中的任何问题：编译错误、链接错误、内核启动失败、HardFault、驱动加载失败、烧录问题、环境故障。触发症状：用户说"报错了"、"编译不过"、"起不来"、"HardFault"、"链接失败"、"undefined reference"、"调试"、"为什么失败"。
license: MIT
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: lite
  capability: problem-diag
  version: 0.1.0
  status: trial
  category: workflow-step-problem-diag
  primary_reference: skills/ohos-issue-lite-diagnose/SKILL.md
  upstream_trigger: ../04-build-verify/SKILL.md (Step F = P7-from-P4 fast-path)
---

# Phase 7: 问题诊断与修复 ★ 逃生舱

> **本步骤只做工作流编排**：何时切入诊断、诊断完回到哪里、何时该升级。
> **诊断知识本体（故障分类、修复流程、案例库、日志获取、调试工具）统一收录在
> `skills/ohos-issue-lite-diagnose/`**——它是诊断知识的唯一权威源。
> 本步骤是工作流的一环，负责把出错的现场路由到诊断 skill，再把修复结论路由回出错阶段。

## 契约（来自编排器 `skills/ohos-dev-workflow-router/SKILL.md` v0.1.0）

| 属性 | 值 |
|------|-----|
| **输入** | 错误现象描述 + 完整日志 + 现场状态 + 出错阶段 + 环境信息 |
| **产出** | ① 根因定位 (具体到 file:line) ② 修复方案 ③ **Patch Manifest** (如修改 GT) ④ **Experiment Record** (如尝试性修复) ⑤ 回归断点（含 `return_phase` + `return_step`）⑥ `same_error_rounds` 记录 |
| **门控** | 无（诊断即服务） |
| **特殊性** | 不是顺序流程一步 → **任意阶段的逃生舱** |
| **难度** | ★★★★★ 全工作流最高 — 需跨领域推理 + 排除法 + 根因分析 |
| **诊断知识权威源** | `skills/ohos-issue-lite-diagnose/SKILL.md` + 其 `references/` |

## 知识检索（可用时优先知识检索服务如 project-brain MCP；不可用按 skill 知识检索降级链：本地 references → 联网搜索 → 询问用户）

本步骤的本地代码分析，可用时优先使用（可选）project-brain 等知识检索服务 MCP：
- `impact_analysis` — 改某文件前评估波及面（P7 改动前必用）
- `get_call_graph` — 追根因调用链（谁调了出错的符号）
- `get_related_tests` — 找相关测试验证修复
- `get_history` — 看某符号的修改历史（回归定位）

> MCP 调失败或未装 → 按 skill 知识检索降级链回退。

## 决策分级（问用户 ↔ 自决平衡，诊断阶段适用）

> **实测教训**：①执行者在用户未明确决策时被主 agent 默认推进业务决策；②执行者把技术决策（binder/MTD/patch 适用性/工具链路径/构建路径当只有一条可行）转发用户烦用户。P7 是全工作流最高难度阶段（跨领域推理 + 排除法 + 根因分析），决策密集（修复策略选择、patch category 判定、N 轮无进展后是否交还用户、是否升级 Oracle/问厂商），遇决策先按本表分级再决定转发还是自决。完整版见编排器 `skills/ohos-dev-workflow-router/SKILL.md`「决策分级 + 术语大白话」节。

| 级别 | 含义 | 处理方式 | P7 典型例子 |
|------|------|---------|---------|
| **业务决策** | 物理板型 / scope 取舍 / trade-off 代价 / 归档路径 / 是否人工介入 / 是否换硬件 / 经验回填开关——需用户拍板的选择 | **停下转发用户，不默认推进**（含主 agent 也不能替用户默认，实测教训） | N 轮无进展后人工介入 vs AI 继续、是否请教专家/换硬件、boot_image 缺失后是否终止、是否升级 Oracle/问厂商、归档路径、经验回填开关 |
| **技术执行** | 修复策略（GT patch vs framework patch vs experiment）、patch 适用性、工具链路径、内核 config 调整、按工作流教训可定的——执行者按工作流教训+验证自决 | **执行者自决，不转发用户**（实测教训） | 错误分类（A-H 8 类）、修复策略选择（Patch #001-#010 模式）、defconfig 开 MTD、加 BINDER_IPC_32BIT 宏、SDK 二进制指纹锁禁用、-Werror warning 修复路径、Wrapper script 注入 |

> **执行纪律（问用户与自决平衡）**：遇决策先按上表分级。业务决策必须停下转发等明确答复，绝不默认推进（哪怕主 agent 给"默认值"，只要用户没明确说也停下问）。技术执行按工作流教训+验证自决，不拿技术决策烦用户。判别口诀：**"这是真的应该由用户决定的问题吗？"**——是→停转发；否（按工作流教训+验证可定）→自决。P7 的特殊情况：**N 轮无进展暂停**（见 Step 7）触发时是**业务决策**（交还用户决定人工介入 vs AI 继续），不能自决继续循环。

## 何时切入

由编排器路由规则 R2 自动触发：
- 任何阶段遇到**无法自行解决的阻塞**
- 用户主动报告错误
- 门控检查点未通过且原因不明
- **P4 Step F (Compiler Fix Loop)** 是最常见的切入路径

## P7 与普通阶段的根本区别

| 维度 | 普通阶段 (P1~P6) | P7 (逃生舱) |
|------|----------------:|:----------:|
| 触发时机 | 拓扑序中的固定位置 | **任意时刻**（错误时切入） |
| 输入来源 | 前序阶段产出 | **出错现场**: 日志/现象/状态 |
| 输出去向 | 下一阶段 | **返回断点**（回到出错阶段） |
| 执行次数 | 1 次 | **0~N 次**（可能反复切入） |
| Agent 难度 | 领域专家 | **最高** — 跨领域推理 |

---

## 诊断执行 —— 委托给 ohos-issue-lite-diagnose skill

切入后，**诊断分析本身由 `skills/ohos-issue-lite-diagnose/` 承载**。本步骤不重复其内容，只做路由与衔接。

### 诊断 skill 入口

| 诊断需求 | 入口文件（相对本步骤） |
|---------|--------------------|
| **诊断工作流总入口**（意图判断→环境检测→获取日志→分类→匹配→修复方案→回归验证） | `skills/ohos-issue-lite-diagnose/SKILL.md` |
| 匹配已知故障模式（编译/链接/启动/驱动/运行时/功耗 6 大类） | `skills/ohos-issue-lite-diagnose/references/fault-knowledge-base.md` |
| 参照真实诊断案例（Hi3861/STM32F407/BES2600W + Hi3516CV610 烧录实战 §8） | `skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md` |
| 引导用户获取诊断信息（串口/JTAG/HardFault 现场捕获/环形日志） | `skills/ohos-issue-lite-diagnose/references/log-acquisition-guide.md` |
| 调试工具指南（OpenOCD/JTAG/arm-gcc size-nm-objdump） | `skills/ohos-issue-lite-diagnose/references/debug-tools-guide.md` |
| 故障速查表（精简版） | `skills/ohos-issue-lite-diagnose/references/fault-cheatsheet.md` |
| 诊断报告输出模板 | `skills/ohos-issue-lite-diagnose/references/diagnostic-report-template.md` |
| 外部参考资料链接 | `skills/ohos-issue-lite-diagnose/references/bibliography.md` |

### 工作流与诊断 skill 的衔接

1. 编排器按 R2 触发 P7 → 本步骤接管现场。
2. 本步骤收集 `error_report`（见下方"现象捕获"最小清单）并判定出错阶段。
3. **委托 `skills/ohos-issue-lite-diagnose/` 执行 7 步诊断**（现象捕获→日志分析→假设生成→逐项排除→根因确认→修复设计→回归验证）。
   - ⚠️ **诊断先联网搜 + 再查源码/加打印验证**（实测教训，诊断 skill Step 2.5）：拿到报错先联网检索（宿主 WebSearch 或等价物 / 备选检索 CLI 如 opencode）搜"报错原文 + 芯片/SDK/场景"看别人遇到过吗，再查参考仓源码/加打印验证（网上方案是线索不是定论，搜完必须验证，源码/加打印为准）。别钻牛角尖直接源码+加打印多轮不搜，也别盲信网上不验证就照搬。联网检索失败降级备选检索 CLI（如 opencode）/curl（见 skill 知识检索降级链兜底）。
4. 诊断 skill 产出根因 + 修复方案 +（如需）patch manifest / experiment record。
5. 本步骤按下方"断点映射表"把控制权交回出错阶段。

### 现象捕获最小清单（交诊断 skill 前必须备齐）

```yaml
error_report:
  timestamp: "ISO-8601"
  error_message: "完整的第一行错误信息 (verbatim copy)"
  exit_code: {integer}
  signal: null | "{SIGSEGV/SIGABRT/etc}"

  command: "导致错误的完整命令"
  working_dir: "{absolute_path}"

  environment:
    os: "{linux/windows/mac}"
    python_version: "x.y.z"
    hb_version: "x.y.z or BROKEN"
    gn_version: "x.y.z"
    toolchain: "{prefix}gcc x.y.z"
    ninja_version: "x.y.z"

  reproducible: true | false
  first_appear_phase: "P1/P2/P3/P4/P5/P6"
  frequency: "always / intermittent / once"

  full_log_path: "/path/to/build.log"  # 或内联关键片段
  related_files: []  # 可能涉及的文件列表
```

> 完整的诊断流程、错误分类 taxonomy（A-H 共 8 类）、修复流程（GT Patch Archive / Framework Patch / Experiment Tracking / Toolchain 决策树）**全部在 `skills/ohos-issue-lite-diagnose/SKILL.md` 中定义**，本步骤不复制。

---

## 编译/工具链问题的补充入口

实测中 P7 最常处理的是编译/链接/工具链问题，除了诊断 skill 外，还有一份专门的编译修复知识库：

| 用途 | 路径（相对本步骤） |
|------|----------------|
| **★ 编译修复 playbook** — 9 个 GT patch 复现 + Wrapper v3 recipe + Decision Tree + 18 条 Findings F-001~F-018 | `skills/ohos-dev-build-config/references/compiler_fix_playbook.md` |
| GN 语法 / error cheatsheet | `skills/ohos-dev-build-config/` |
| Kconfig / 内核样本 | `skills/ohos-dev-kernel-source-query/` |

> 遇到编译/链接/工具链问题时，先查 `compiler_fix_playbook.md` 的 Decision Tree 再动手。

---

## Step 7: 回归断点 + Stuck 检测

### 证据失效与重建

P7 修复任何上游输入后，必须先在 `verification_manifest` 标记受影响的下游证据为 `INVALIDATED`，并记录修复提交/源码快照、原因和影响范围。至少重新计算受影响产物 SHA256，作废相关构建/测试/审查结论及 GATE-B、GATE-T、GATE-R 状态；从 `return_phase`/`return_step` 回归完成后才能以新日志和哈希重新签发门控。不得保留修复前的 PASS 作为修复后的证据。

### 断点映射表

| 出错阶段 | 返回断点 | 继续动作 |
|---------|---------|---------|
| P1 (env-prep) | P1 Step 2 (工具链安装) | 重新安装/修复 |
| P2 (kernel-port) | 具体子步骤 (2pre/2a/2b/2c/2d/2e[/2f if 厂商内核]) | 修复该子步骤后继续 |
| P3 (driver-dev) | 3b (驱动生成) | 修复该驱动后继续 |
| P4 (build-verify) | P4 Step 2 (重编译) | 修复后全量重编 |
| P5 (test-gen) | P5 Step 测试执行 | 修复后重跑测试套件 |
| P6 (doc-review) | P6 Step 文档/审查 | 修复后重审对应产物 |
| Unknown | 最后一个通过的 GATE | 从该 GATE 之后重新开始 |

### Stuck 检测 (★ 3 轮阈值)

| 信号 | 含义 | 动作 |
|------|------|------|
| 同一错误 **3+ 轮**没修好 | Fix 没命中根因 | **STOP**. 切换假设. Consult Oracle if available. |
| 每轮修复引入**新错误** | 级联失败 / 错误分类错了 | **STOP**. 重新从诊断 skill Step 3 做假设生成. 可能需要 total revert. |
| Patch 超过 **20 行** | 在 over-patching | **STOP**. 考虑完全替代策略. |
| 环境反复 break | 基础设施不稳定 | **PAUSE**. 先单独修环境, 不混入代码修复. |

### N 轮无进展暂停 (★ max_auto_rounds 阈值，交还用户)

> **与 Stuck 检测的区别**：Stuck 检测针对"单点错误修不好"（3 轮同错误）；本规则针对"卡在同一个问题上无进展"（同一问题 N 轮无实质突破）。两者叠加：单点 3 轮卡住 → 切换假设；同一问题累计 N 轮无进展 → 暂停交还用户。

- **阈值**：`workflow_config.yaml` → `diagnostic.max_auto_rounds`（默认 5，用户可调）。
- **"无进展" = 卡在同一个问题上无进展**（同一问题反复尝试无实质突破：未定位根因/未解决/反复同一类假设无新结论）。
- **不算无进展（不累计触发）**：跨不同子问题各有进展——每个子问题在推进或已解决时，N 轮计数按"同一问题"归零重计，不累计跨子问题的总轮数。判别示例：GSL/uboot code/-10B 各解决=有进展不累计；0x81 卡住多轮无突破=同一问题无进展才计数。
- **触发条件**：同一问题累计无进展轮数 ≥ 阈值（"无进展"完整定义见 `skills/ohos-issue-lite-diagnose/SKILL.md` §N 轮无进展暂停机制）。
- **触发后 MUST DO**（不要继续自动循环）：
  1. 立即停止自动编译/烧录/验证尝试
  2. 向用户汇报：①卡在哪个问题上 N 轮无进展 ②已尝试的 N 轮和结论 ③当前卡点 ④请用户决定：人工介入（请教专家/换硬件）还是 AI 继续分析
  3. 等待用户决策，不自行发起下一轮

> 背景：裸烧 boot_image 诊断曾跑 10+ 轮 agent 陷入反复重构建重烧循环。此规则确保 AI 在合适时机交还用户，避免无限自动循环。

### Escalate 协议

连续 stuck 时:

1. **Revert 到最后已知-good 状态** (`git checkout` 或 undo edits)
2. **Document the wall** (什么试过了, 都没用)
3. **Consult Oracle** (如果可用) — 带完整 error log + history
4. **Ask user** for domain expertise (可能涉及芯片手册/厂商支持)

### 诊断报告 / 根因回填（消费 `workflow_config.yaml.experience.accumulation`）

> **定位**：经验积累机制的一部分——诊断闭环后（根因确认 + 修复验证通过），按用户前置采集的 `experience.accumulation` 模式决定要不要把本次诊断经验（根因、修复方案、patch manifest、experiment record）回填进工作流的 references / lessons-learned。前置采集见 `01-env-prep` Step 0b「经验积累模式采集」节。**P-失败回填的用户可控开关**：失败/回退的实验和成功的一样有价值，但回填必须受用户开关控制，不能默认自动写入。

**读 `workflow_config.yaml.experience.accumulation` 字段**，按值分支：

| 值 | 行为 | P7 诊断经验回填动作 |
|----|------|------------------|
| `manual`（默认） | 不自动回填，问用户是否回填 + 回填哪些 | 向用户问："本次诊断经验（根因 + 修复方案 + patch manifest + experiment record）要不要回填进工作流？要回填哪些（如新故障模式 / 新 patch 复现 / 失败实验避免重复 / 决策分级案例）"——**用户不主动 yes 就不回填**（P-失败回填的用户可控开关） |
| `auto` | 自动回填 | 自动把本阶段诊断经验写入工作流 references：① A 类方法→正文（如新故障分类 taxonomy 条目、新 Decision Tree 分支、新 Stuck 检测信号）② B 类语料→`skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md`（如本次诊断案例，按 BG00N 格式追加）+ `skills/ohos-issue-lite-diagnose/references/fault-knowledge-base.md`（新故障模式） |
| `off` | 跳过 | 不回填，即使有可回填的诊断经验也不写 |

**回填时打个性化标签**：每条回填的诊断经验末尾加标签 `（来源：芯片 @ iter, 日期）`，如 `（来源：hi3516cv610 @ iterN, 2026-07-27）`，让下次跑工作流 load 时能识别经验的来源上下文（不同芯片/迭代可能有差异，标签避免盲目照搬）。

**P7 可回填的诊断经验类型**（参考）：
- A 类（方法→正文）：新故障分类 taxonomy 条目（A-H 8 类之外的扩展）、新 Decision Tree 分支、新 Stuck 检测信号、新 N 轮无进展判定规则
- B 类（语料→references）：本次诊断案例（按 `diagnostic-cases.md` BG00N 格式：现象/根因/修复/验证）、新故障模式（按 `fault-knowledge-base.md` 格式）、patch manifest 复现（patch_id / 文件 / diff / 根因）、experiment record（EXP-NNN 格式，含失败实验避免重复）
- 失败回填（P-失败回填）：诊断失败 / 修复引入新错误 / N 轮无进展交还用户 → 分类失败（错误分类错了 / 假设生成不足 / 验证不充分 / patch 过大）→ 回溯本应抓住的诊断步 → 补该步检查进诊断 skill 或 Stuck 检测信号表

**与 P4 构建侧联动**：P7 的诊断报告/根因回填与 P4 的 Compiler Fix Loop 都接同一个 `experience.accumulation` 机制（见编排器 `skills/ohos-dev-workflow-router/SKILL.md` 的最终 GATE-交付经验回填环节）。P4 回填的是"构建侧踩坑"，P7 回填的是"诊断侧根因"，两者互补——P4 的 patch 复现可被 P7 的 fault-knowledge-base 引用，P7 的根因分析可被 P4 的 Compiler Fix Decision Tree 引用。

> **回填时机**：诊断闭环后（根因确认 + 修复验证通过 + 回归断点返回出错阶段继续）触发回填动作，不是诊断过程中实时回填。`auto` 模式下诊断闭环时触发回填；`manual` 模式下问用户后触发；`off` 不触发。

---

## Agent Dispatch Spec

### 分发规格

| 属性 | 值 |
|------|-----|
| **agent_role** | `diagnostician` |
| **category** | 由 `workflow_config.yaml.workflow.p7_escalation` 的 `auto` 策略在派发前调用 `p7_dispatch_category(error_context)` 决定：常规为 `unspecified-high`，仅 HardFault、启动挂起或间歇性失败升级为 `ultrabrain`；`DECISIONS.md` 仅记录该选择 |
| **load_skills** | `[ohos-issue-lite-diagnose, ohos-dev-build-config]` |
| **dispatch_mode** | **直接执行** (强顺序: 分析→定位→修复, 不可并行) |
| **parallel_groups** | 无 (诊断本身不可拆分) |

### Agent Prompt 模板

```
1. TASK:
   对 {chip_model} 嵌入式 OS 适配过程中的问题进行诊断和修复。
   你是工作流的逃生舱 —— 当其他阶段遇到无法解决的问题时被调用。
   实测中你被调用 9+ 轮, 产出了 9 个 GT patches + 1 个 framework patch + 2 个实验。

2. 诊断执行:
   完整诊断流程（7 步：现象捕获→日志分析→假设生成→逐项排除→根因确认→修复设计→回归验证）
   和错误分类 taxonomy（A-H 共 8 类）由 `skills/ohos-issue-lite-diagnose/SKILL.md` 定义。
   严格按该 skill 执行，不要凭直觉跳步。

3. 修复按类别（详见诊断 skill Step 6）:
   A (workflow-gen): 直接修, 重生成
   B (GT file): ★ Patch Archive 流程 (备份→最小改→diff→manifest→用户批准)
   C (framework): 记录 + 建议告知
   D (third-party): 记录 + 建议告知
   E (toolchain): Wrapper / replace / inform user
   F (environment): 直接修
   G (memory layout): ★ 用户必须批准
   H (runtime): 调试分析

4. ★ 编译/工具链问题补充参考: compiler_fix_playbook.md
   (`skills/ohos-dev-build-config/references/compiler_fix_playbook.md`)
   它包含: 9 个实际 patch 复现指南 + Wrapper v3 recipe + Decision Tree + 18 条 Findings
   遇到编译/链接/工具链问题时先查 Decision Tree 再动手!

5. Experiment Tracking:
   尝试性修复必须用 EXP-NNN 格式记录.
   失败/回退的实验和成功的一样有价值 (避免下次重复).

6. Stuck Detection:
   连续 3 轮同一错误 → STOP, 切换假设.
   每轮引入新错误 → STOP, 重新分类.
   Patch >20 行 → STOP, 考虑替代策略.
   同一问题累计 N 轮 (config diagnostic.max_auto_rounds, 默认 5) 无进展 → STOP, 暂停交还用户 (汇报卡在哪个问题 + N 轮结论 + 卡点 + 请用户决定人工介入 vs AI 继续). 跨子问题各有进展不累计.

7. EXPECTED OUTCOMES:
   ① 根因定位 (file:line + category)
   ② 修复方案 (具体代码或操作步骤)
   ③ patch_manifest.json (如有 GT/framework 修改)
   ④ experiments.yaml (如有尝试性修复)
   ⑤ return_point (回到哪个阶段)

8. MUST DO:
   - [ ] 诊断流程严格按 skills/ohos-issue-lite-diagnose/SKILL.md 执行
   - [ ] 编译问题先查 compiler_fix_playbook.md Decision Tree (不要凭直觉修!)
   - [ ] GT 修改必须走完整 Archive 流程 (备份→diff→manifest→批准)
   - [ ] 每轮修复后全量重编 (不用增量编译)
   - [ ] 实验 must track (不管成败)
   - [ ] 3 轮 stuck → stop + escalate
   - [ ] 找第一个 error, 不要被级联 error 干扰
   - [ ] 同一问题 N 轮 (max_auto_rounds) 无进展 → stop + 暂停交还用户 (不要无限自动循环; 跨子问题各有进展不累计)

9. MUST NOT DO:
   - [ ] 不要跳过假设生成直接修第一个猜测 (实测证明这会浪费轮次)
   - [ ] 不要一次性改多个不相关文件来"试试"
   - [ ] 不要忘记录 experiment (失败的也是知识)
   - [ ] 不要在没备份的情况下改 GT 文件
   - [ ] 不要超过 3 轮还在同一错误上 (stuck → escalate)
   - [ ] 不要把 framework patch 和 GT patch 混为一谈 (不同审批级别)
   - [ ] 不要超过 N 轮 (max_auto_rounds) 同一问题无进展还自动循环 (→ 暂停交还用户; 跨子问题各有进展不累计)
```

## MUST DO (实测血泪教训)

- [ ] **★ 遇决策先分级** (决策分级) — 业务决策（N 轮无进展后人工介入 vs AI 继续 / 是否换硬件 / 是否升级 Oracle/问厂商 / 经验回填开关）停转发用户；技术执行（错误分类 A-H / 修复策略 Patch #001-#010 模式 / patch 适用性 / defconfig / 工具链路径 / Wrapper 注入）自决不转发。N 轮无进展暂停触发时是业务决策，不能自决继续循环
- [ ] **诊断流程走 `skills/ohos-issue-lite-diagnose/SKILL.md`** — 诊断知识唯一权威源，本步骤不复制
- [ ] **诊断先联网搜 + 再查源码/加打印验证** — 拿到报错先联网检索（WebSearch 或等价物 / 备选检索 CLI 如 opencode）搜"报错原文+芯片/SDK/场景"，再查参考仓源码/加打印验证（网上方案是线索不是定论，搜完必须验证，源码/加打印为准）。别钻牛角尖直接源码多轮不搜，也别盲信网上不验证就照搬。联网检索失败降级备选检索 CLI（如 opencode）/curl（见诊断 skill Step 2.5 + skill 知识检索降级链兜底）
- [ ] **编译问题先查 compiler_fix_playbook Decision Tree** — 9 个 patch 的经验已经结构化了
- [ ] **GT 修改必须走完整 Archive 流程** — 备份→最小改→diff→manifest→用户批准, 缺一不可
- [ ] **每轮全量重编** — 增量编译隐藏依赖问题
- [ ] **实验必须跟踪 (EXP-NNN)** — 不管成败, 避免 repeat
- [ ] **找 FIRST error** — 后面的都是 symptom 不是 cause
- [ ] **≥3 个假设** — 不要第 1 个猜测就动手
- [ ] **3 轮 stuck → stop** — 不要死磕, 换思路或 escalate
- [ ] **同一问题 N 轮无进展 → 暂停交还用户** — 达到 config `diagnostic.max_auto_rounds`（默认 5）且**卡在同一个问题上**仍无进展，停止自动循环，汇报卡在哪个问题+N 轮结论+卡点，请用户决定人工介入 vs AI 继续。跨子问题各有进展不累计触发
- [ ] **区分 patch category** — GT ≠ Framework ≠ Experiment (不同审批级别)

## MUST NOT DO (实测血泪教训)

- ❌ 不要在本步骤里复制诊断 skill 的故障分类/修复流程/案例库——它们已在 `skills/ohos-issue-lite-diagnose/` 权威维护
- ❌ 不要跳过备份直接改 GT 文件
- ❌ 不要把 LTO 用于单体库 (EXP-007 证实必 undefined refs)
- ❌ 不要期望 stack-protector 移除解决大溢出 (EXP-008 证实效果微弱)
- ❌ 不要一次改多个不相关文件
- ❌ 不要忘记记录 experiment (失败的也是宝贵数据)
- ❌ 不要混淆 workflow-gen 错误和 GT 错误 (前者自责后者需批准)
- ❌ 不要在 stuck 时继续同方向尝试 (3 轮是硬限)
- ❌ 不要超过 N 轮 (config diagnostic.max_auto_rounds, 默认 5) 同一问题无进展还自动循环 (→ 必须暂停交还用户; 跨子问题各有进展不累计)
