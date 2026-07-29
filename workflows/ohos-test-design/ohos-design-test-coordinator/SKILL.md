---
name: ohos-design-test-coordinator
description: Use when 需要把 Approved 需求文档转化为完整测试用例集——需求解析、测试点设计、用例细化、验证导出五阶段编排。当用户需要设计测试用例、生成测试点、分析测试覆盖，或提及 test case design / test point / coverage / test strategy 时使用；可协调 ohos-design-test-demo-pipeline 产出验证 Demo。Do NOT use before spec is Approved（先跑 ohos-spec），或用于 execution-plan 任务已覆盖的单元测试设计。
---

# 测试设计协调器

## 平台工具映射与降级（三平台契约，本 skill 集真相源）

本 skill 集（ohos-test-design / ohos-design-test-coordinator / ohos-design-test-demo-pipeline 及其 `orchestration/`、`phases/`、`rules/`、`templates/` 子文件）描述的动作一律为**平台无关动作**。文中出现的 `AskUserQuestion`、`spawn Agent`、`Task`、`Read`、`Edit`、`Glob` 等为 **Claude 工具记法别名**，仅作示意，运行时必须按当前平台映射到对应工具；任何平台不得将这些别名视为硬依赖，也不得因别名不存在而无法启动或只能忽略强制约束。

| 平台无关动作 | Claude | Codex | OpenCode | 能力探测 / 降级 |
|---|---|---|---|---|
| 请求用户确认（单选/多选/填空） | AskUserQuestion | 交互提问 | question 工具 | 无对应工具→降级为：将问题写入返回摘要，由上游/用户在文本中作答后再继续；不得静默跳过 |
| 创建或更新任务 | Task | 任务管理 | Task 工具 | 无任务工具→降级为：在 timing.json / 返回摘要中记录阶段状态，串行推进 |
| 派发子Agent（阶段/批次执行） | Task(spawn subagent) | 派发子代理 | Task 工具(spawn subagent) | 无子代理能力→**串行降级**：协调器自身顺序执行各阶段/批次，parallel_limit 强制为 1 |
| 并行派发（上限 4） | 多个 Task 并行 spawn | 多个子代理并行 | 多个 Task 并行 spawn | 无并行→parallel_limit=1 串行；仍遵守 ≤4 上限 |
| 读取文件 | Read | read_file | read 工具 | 必备；缺失则阻塞告警 |
| 写入/编辑文件 | Edit / Write | write_file / edit | edit / write 工具 | 必备；缺失则阻塞告警 |
| 搜索文件名 | Glob | 文件列举 | glob 工具 | 不可用时改为：已知路径直接 Read；不得以 Grep/Glob 兜底 `api-reference`（见 Demo 流水线 NEVER） |
| MCP 能力探测 | knowledge-search MCP | 同 | 同 | 启动时先探测；不可用→local（本地经验文件）/ none，记录到配置上下文 |

**执行约束：**
- 启动流程前先做一次**能力探测**：记录当前平台可用工具集（用户确认 / 任务 / 子Agent / 并行 / MCP），写入配置上下文；后续 NEVER/门禁按探测结果选择路径，不假定固定工具名存在。
- 子Agent（协调器调用模式）**禁止自行发起用户确认**：将需确认项写入返回摘要，由协调器统一发起「请求用户确认」。
- 派发子Agent 失败、超时或返回残缺摘要→不重复 spawn 同一 Agent（见 NEVER「流程阻塞时反复执行」）；改告警并「请求用户确认」是否终止/跳过。
- 任何降级路径必须把降级状态（如 `parallel_limit=1`、`pairwise=skipped`、`mcp=none`）写入结果/timing.json，供门禁决定是否继续，不得静默降质。

## NEVER（执行约束）

- **NEVER 跳过用户确认流程**（平台无关动作「请求用户确认」；别名 `AskUserQuestion` 见「平台工具映射与降级」）
  - 原因：用户配置（输入/输出路径、领域、编号、知识库模式）决定后续所有Phase的文件路径与经验库范围
  - 正确做法：必须先收集用户配置，完成确认后才能启动Phase任务
  - 后果：配置缺失引发跨阶段路径漂移，已生成文件无法被下游阶段定位
- **NEVER 跳过phase流程**
  - 原因：阶段间存在数据依赖链（Phase1→Phase2→Phase4），跳过会断链
  - 正确做法：必须完整执行
  - 后果：下游阶段因缺输入而生成空结果或臆造内容，无法追溯
- **NEVER 自检未通过时进入下一阶段**
  - 原因：自检（self_check_rules.md）是各阶段输出的格式/语义守门员，未通过即存在结构性缺陷
  - 正确做法：必须先完成校验，修正自检告警后再推进
  - 后果：缺陷向下游传播，修复成本随阶段递增
- **NEVER 流程阻塞时反复执行**
  - 原因：阻塞多为环境/数据问题，反复spawn同一Agent会重复触发同一失败点并消耗上下文
  - 正确做法：流程进行中出现问题需及时告警，人工确认是否进入下一阶段
  - 后果：反复执行产生大量无效批次，timing被污染且无法收敛
- **NEVER 多Agent并行时超出parallel_limit≤4**
  - 原因：实测超过4个并行subagent会触发上下文窗口溢出，导致摘要丢失关键字段
  - 正确做法：Phase2/4并行执行时parallel_limit≤4
  - 后果：批次摘要残缺，merge_batch_mds无法还原完整测试点/用例
- **NEVER 经验库为空时跳过分批规划**
  - 原因：分批规划是批次均衡与去重的关键步骤，依赖前置摘要做跨批次依赖裁剪
  - 正确做法：规划Agent必须完成分批规划和前置摘要提取（仅跳过匹配步骤）
  - 后果：空经验库直接spawn会导致批次不均衡、测试点重复，下游Phase4合并冲突

> 门控处理框架（各阶段门控检查点、触发时机、未通过处理）详见 `rules/gate_rules.md`。

---

## 启动流程

按以下决策树逐项确认后启动（任一项缺失/未通过则阻塞并告警，不进入阶段1）：

1. **输入路径?** → 请求用户确认·问1（①当前工作目录 / ②自定义）→ 读取验证目录存在 → 扫描识别需求文档（获取文件名）
2. **输出路径?** → 请求用户确认·问2（①与输入相同 / ②自定义）→ 创建目录（如不存在）
3. **领域?** → 请求用户确认·问3 → ①默认：仅通用经验库（general/下三层知识目录），不加载领域经验库，无需用户确认 → ②领域：通用固定加载 + 用户选择领域及层级（详见 `orchestration/startup_orchestration.md`） → ③自定义：验证用户输入的路径
4. **用例编号?** → 请求用户确认·问4（不允许包含%）→ ①case_id_temp_001 / ②自定义
5. **知识库模式?** → 调用 `knowledge-service_health_check` → MCP可用→mcp；MCP不可用但本地有文件→local；均不可用→none。记录到配置上下文供各Phase使用
6. **启动阶段编排** → 创建阶段任务（Phase1→Phase2→Phase2Adv→Phase3→Phase4→Phase4Adv→Phase5）→ 初始化timing.json记录pipeline_started_at（详见 `rules/timing_rules.md`）→ 进入阶段1

> 领域选择与确认的详细步骤（领域列表、知识库范围、检索路径限定）见 [`orchestration/startup_orchestration.md`](orchestration/startup_orchestration.md)。

### 用户确认问题配置（平台无关；别名 AskUserQuestion 见「平台工具映射与降级」）

| 序号 | header | 问题内容 | 选项 |
|------|--------|---------|------|
| 1 | 输入路径 | 需求文档所在目录路径？ | ① 使用当前工作目录 ② 自定义 |
| 2 | 输出路径 | 测试设计输出目录路径？ | ① 与输入路径相同 ② 自定义 |
| 3 | 领域选择 | 需求是否涉及特定领域？ | ① 默认（不加载领域经验库，仅通用） ② 领域（通用+领域，用户选择领域） ③ 自定义 |
| 4 | 用例编号 | 用例编号起始值（不允许包含%）？ | ① 默认case_id_temp_001 ② 自定义 |

---

## 阶段执行模式

每个阶段按以下模式执行：

| 步骤 | 动作 | 计时机 |
|------|------|--------|
| 1 | 派发子Agent（阶段） | T1: phase_started_at |
| 2 | 等待子Agent返回摘要 | T2: agent_completed_at |
| 3 | 请求用户确认 | T3/T4: confirmation时间（仅Phase1/2Adv/4Adv需要） |
| 4 | 标记任务完成 | T6: phase_completed_at |

> 计时协议、确认策略、timing.json结构、计时报告格式详见 `rules/timing_rules.md`。

## 关键决策思维框架（Before X, ask yourself）

编排器在以下决策点必须先自问再行动，任一未满足则阻塞：

- **Before spawn 规划 Agent**：经验库是否已匹配（空时已标注0条）？批次划分是否均衡（主单元/测试点粒度对齐）？前置摘要是否注入（有前置依赖时）？
- **Before 进入下一阶段**：自检是否通过（无⚠️/未通过）？门控数据是否非空（主单元/场景/测试点/用例数>0）？确认是否完成（需确认阶段已获"正确，继续"）？
- **Before 委托 Demo 流水线**：是否存在非 XTS 测试点（黑盒自动化/API性能/手工）？领域是否已确认（有领域名或已询问用户）？

---

## 阶段1：需求解析

> **IBO（Input-Boundary-Output，输入-边界-输出）分析法**：黑盒测试视角的需求解析方法，从需求文档中提取三要素——**输入参数**（外部可触发的外部入口：API入参/CLI参数/配置项/用户操作）、**边界条件**（影响输出的隐式上下文：权限/角色/状态前置/异常触发条件）、**预期输出**（外部可观测的输出：返回值/UI变化/回调/错误码）。凡内部接口、内部状态、编译时配置均过滤。详细过滤规则见 `rules/phase1_rules.md` §2.1。

> **MANDATORY - 进入本阶段前完整读取** [`orchestration/phase1_orchestration.md`](orchestration/phase1_orchestration.md)：spawn/等待/澄清交互等编排步骤与注入清单。
> **Do NOT Load** `orchestration/phase2_orchestration.md`、`orchestration/phase3_orchestration.md`、`orchestration/phase4_orchestration.md`、`orchestration/phase5_orchestration.md`。

### 决策树：自检分支与路由（Read requirement_analysis.md 自检部分后判定）

| 判定 | 条件 | 动作 |
|------|------|------|
| 自检结果 | 含"⚠️"或"未通过" | 必须立即处理，不得进入下一阶段 |
| 自检项"输入可控制性" | "⚠️" | 必须追问参数来源，执行答疑流程 |
| 自检项"Inner接口过滤" | 标记"已删除"但§2.1仍有来自InnerApi的参数 | 必须追问并要求重新过滤 |
| 用户最终确认 | "正确，继续" | 进入Phase2 |

| 配置项 | 说明 |
|--------|------|
| **骨架文件** | phases/phase1_requirement.md |
| **详细规则** | rules/phase1_rules.md（Agent自行Read） |
| **交互流程** | rules/phase1_clarify_rules.md（编排器按需Read） |
| **输入** | 需求文档路径列表 |
| **输出** | requirement_analysis.md + knowledge_match.md |
| **确认** | 需要（含待确认项答疑） |
| **计时** | T1→T2→T3→T4→T6，详见rules/timing_rules.md |
| **门控** | 完成后检查数据空值（主单元数=0且被测场景数=0），详见rules/gate_rules.md |
| **Do NOT Load** | `rules/phase2_rules.md`、`rules/phase4_rules.md`、`phases/phase4_testcase.md`、test-experience/case-refinement 知识层级（仅读 domain-knowledge） |

---

## 阶段2：测试点生成

> **MANDATORY - 进入本阶段前完整读取** [`orchestration/phase2_orchestration.md`](orchestration/phase2_orchestration.md)：测试技术预处理→规划Agent→多轮并行spawn→合并→对抗脚本的编排步骤与注入清单。
> **Do NOT Load** `orchestration/phase1_orchestration.md`、`orchestration/phase3_orchestration.md`、`orchestration/phase4_orchestration.md`、`orchestration/phase5_orchestration.md`。

### 决策树：对抗评估达标

| 判定 | 条件 | 动作 |
|------|------|------|
| 对抗评估结果 | 达标 | 自动进入 Phase3 |
| 对抗评估结果 | 不达标 | 用户确认后循环补充（详见 phases/phase2_testpoint_adv.md） |

| 配置项 | 说明 |
|--------|------|
| **骨架文件** | phases/phase2_testpoint.md |
| **详细规则** | rules/phase2_rules.md（Agent自行Read） |
| **经验库匹配时机** | 规划Agent执行（分批规划前） |
| **匹配输出** | 追加到knowledge_match.md（测试经验匹配结果表格） |
| **执行方式** | 多轮并行（详见rules/phase2_rules.md） |
| **注入文件** | requirement_analysis.md + knowledge_match.md + testing_technology.json + phase2_rules.md + 骨架文件 + 前置摘要(有前置依赖时) |
| **测试技术脚本** | phase2_testing_technology.py --technique generate_all |
| **合并脚本** | phase2_testpoint_utils.py --action merge_batch_mds |
| **对抗脚本** | phase2_adversary.py |
| **对抗报告** | 创建adversarial_report.md第一部分 |
| **确认** | 仅不达标时确认 |
| **计时** | T1→T2→T6（Phase2生成），T1→T2→T3→T4→T6（Phase2Adv），详见rules/timing_rules.md |
| **门控** | Phase2完成后检查质量不达标（覆盖率<70%），Phase2Adv完成后检查对抗评分，详见rules/gate_rules.md |
| **Do NOT Load** | `rules/phase1_clarify_rules.md`、`phases/phase5_validate.md`、domain-knowledge/case-refinement 知识层级（仅读 test-experience） |

---

## 阶段3：Demo流水线（委托ohos-design-test-demo-pipeline）

> **MANDATORY - 进入本阶段前完整读取** [`orchestration/phase3_orchestration.md`](orchestration/phase3_orchestration.md)：委托 prompt 构造方式、SDK过低/HVIGORW_NOT_FOUND/BUILD FAILED 三个异常子流程、临时文件清理。
> **Do NOT Load** 本协调器 phase1/2/4/5 orchestration 文件。

### 决策树 A：是否执行 Demo 流水线

读取 test_point_design.md 汇总区"按执行方式统计"表，统计非 XTS 测试点数量（黑盒自动化 + API性能自动化 + 手工）：

| 条件 | 动作 |
|------|------|
| 所有测试点均为 XTS | 跳过 Demo 流水线，直接进入 Phase4 |
| 存在非 XTS 测试点 | 请求用户确认 是否生成验证 Demo（问题："检测到非XTS测试点，是否生成验证Demo？"；选项①生成Demo(推荐) ②跳过直接进入Phase4）；选择生成→执行 Demo 流水线，仅为非 XTS 测试点生成 Demo，从 test_point_design.md 提取黑盒自动化/手工测试点写入临时文件 `{输出目录}/demo_test_points.md` 作为输入；选择跳过→直接进入 Phase4 |

### 决策树 B：领域确认

| 条件 | 动作 |
|------|------|
| 上下文已含领域名称 | 直接使用 |
| 无领域名称 | 请求用户确认 询问用户 API 所属领域（问题："Demo流水线需要确定API所属领域，请选择或输入领域："；选项从 ohos-design-test-demo-pipeline 的 `reference/domains.yaml` 读取所有领域 display_name 列出 + "查看支持的领域列表"；用户输入后与 domains.yaml 的 keywords 匹配，不区分大小写） |

### 决策树 C：编译状态分支（强制执行）

检查返回摘要中的编译状态字段，按状态分支处理：

| 编译状态 | 协调器动作 |
|---------|-----------|
| BUILD SUCCESSFUL | 正常继续，记录T6，进入Phase4 |
| SDK版本过低 | **必须请求用户确认**（详见 orchestration/phase3_orchestration.md §SDK版本过低处理流程） |
| HVIGORW_NOT_FOUND | **必须请求用户确认**（详见 orchestration/phase3_orchestration.md §HVIGORW_NOT_FOUND处理流程） |
| BUILD FAILED | 记录告警，请求用户确认询问重试或跳过（详见 orchestration/phase3_orchestration.md §BUILD FAILED处理流程） |

> **NEVER** 忽略返回摘要中的编译状态字段直接进入Phase4
> **NEVER** 在协调器调用模式下让 ohos-design-test-demo-pipeline 子Agent 自行发起用户确认（别名 AskUserQuestion，见「平台工具映射与降级」）

| 配置项 | 说明 |
|--------|------|
| **骨架文件** | phases/phase3_demo_pipeline.md |
| **执行方式** | 委托ohos-design-test-demo-pipeline skill |
| **输入** | demo_test_points.md + requirement_analysis.md |
| **输出** | demo_design.md |
| **确认** | 不需要（Demo流水线自动执行） |
| **计时** | T1→T2→T6（跳过确认），跳过时耗时为0，详见rules/timing_rules.md |
| **Do NOT Load** | 本协调器 phase1/2/4/5 rules 与骨架（Phase3 委托 ohos-design-test-demo-pipeline skill，不加载本协调器阶段规则） |

---

## 阶段4：测试用例细化

> **MANDATORY - 进入本阶段前完整读取** [`orchestration/phase4_orchestration.md`](orchestration/phase4_orchestration.md)：规划Agent→多轮并行spawn→合并→对抗脚本的编排步骤与注入清单。
> **Do NOT Load** `orchestration/phase1_orchestration.md`、`orchestration/phase2_orchestration.md`、`orchestration/phase3_orchestration.md`、`orchestration/phase5_orchestration.md`。

### 决策树：对抗评估达标

| 判定 | 条件 | 动作 |
|------|------|------|
| 对抗评估结果 | 达标 | 自动进入 Phase5 |
| 对抗评估结果 | 不达标 | 用户确认后循环补充（详见 phases/phase4_testcase_adv.md） |

| 配置项 | 说明 |
|--------|------|
| **骨架文件** | phases/phase4_testcase.md |
| **详细规则** | rules/phase4_rules.md（Agent自行Read） |
| **经验库匹配时机** | 规划Agent执行（分批规划前） |
| **匹配输出** | 追加到knowledge_match.md（细化步骤匹配结果表格） |
| **执行方式** | 多轮并行（详见rules/phase4_rules.md） |
| **注入文件** | requirement_analysis.md + test_point_design.md + knowledge_match.md + phase4_rules.md + 骨架文件 |
| **合并脚本** | phase4_testcase_utils.py --action merge_batch_mds |
| **对抗脚本** | phase4_adversary.py |
| **对抗报告** | 追加adversarial_report.md第二部分 |
| **确认** | 仅不达标时确认 |
| **计时** | T1→T2→T6（Phase4生成），T1→T2→T3→T4→T6（Phase4Adv），详见rules/timing_rules.md |
| **门控** | Phase4Adv完成后检查对抗评分不达标，详见rules/gate_rules.md |
| **Do NOT Load** | `rules/phase1_rules.md`、`rules/phase1_clarify_rules.md`、`phases/phase1_requirement.md`、`phases/phase5_validate.md`、domain-knowledge/test-experience 知识层级（仅读 case-refinement） |

---

## 阶段5：验证与导出

> **MANDATORY - 进入本阶段前完整读取** [`orchestration/phase5_orchestration.md`](orchestration/phase5_orchestration.md)：导出脚本调用与空字段门控处理。
> **Do NOT Load** `orchestration/phase1/2/3/4_orchestration.md`。

| 配置项 | 说明 |
|--------|------|
| **骨架文件** | phases/phase5_validate.md |
| **详细规则** | rules/phase5_rules.md（Agent自行Read） |
| **输入** | test_cases.md + test_point_design.md + 用例编号起始值 |
| **输出** | validation_report.md + test_cases.xlsx |
| **导出脚本** | phase5_export.py --output {output_dir} |
| **确认** | 不需要 |
| **计时** | T1→T2→T6（跳过确认），详见rules/timing_rules.md |
| **门控** | 导出后检查空字段（>20%），详见rules/gate_rules.md |
| **Do NOT Load** | `rules/phase1_clarify_rules.md`、`phases/phase1_requirement.md`、`phases/phase2_testpoint.md`（仅读 phase5_rules + 已生成的 test_cases.md/test_point_design.md） |

---

## 完成后

1. 记录pipeline_completed_at到timing.json
2. 打印计时报告（格式详见 `rules/timing_rules.md`）

---

## Agent Prompt模板（统一）

> **MANDATORY - spawn Agent 前完整读取** [`templates/agent_prompt_template.md`](templates/agent_prompt_template.md)：获取统一模板与占位符对齐校验规则。

---

## 脚本调用方式

| 脚本 | 调用时机 | 命令示例 |
|------|---------|---------|
| **phase2_testing_technology.py** | Phase2生成测试点前 | `python phase2_testing_technology.py --technique generate_all --requirement requirement_analysis.md --output testing_technology.json` |
| **phase2_testpoint_utils.py** | Phase2合并 | `python phase2_testpoint_utils.py --action merge_batch_mds --batch-dir {dir} --requirement {path} --output {md_path}` |
| **phase2_adversary.py** | Phase2对抗评估 | `python phase2_adversary.py --testpoint {test_point_design.md} --requirement {requirement_analysis.md} --knowledge-match {knowledge_match.md} --output {phase2_adversary.json}` |
| **phase4_testcase_utils.py** | Phase4合并 | `python phase4_testcase_utils.py --action merge_batch_mds --batch-dir {dir} --testpoint {path} --requirement {requirement_analysis.md} --output {md_path}` |
| **phase4_adversary.py** | Phase4对抗评估 | `python phase4_adversary.py --testcases {test_cases.md} --testpoint {test_point_design.md} --output {phase4_adversary.json}` |
| **phase5_export.py** | Phase5导出时 | `python phase5_export.py --output {dir} --start-id {case_id_temp_001} --testpoint {path}` |

---

## 目录结构

```
ohos-design-test-coordinator/
├── SKILL.md（路由 + 决策树 + 触发器）
├── orchestration/（协调器执行步骤层——进入对应阶段时 Read）
├── phases/（Agent 骨架层——spawn 时注入 Prompt）
├── rules/（Agent 规则层——Agent 自行 Read）
├── templates/（ui-templates.md + agent_prompt_template.md）
├── assets/（脚本）
├── experience_library/（本地经验库，三层知识层级）
└── adversary/（对抗评估规则和策略）
```