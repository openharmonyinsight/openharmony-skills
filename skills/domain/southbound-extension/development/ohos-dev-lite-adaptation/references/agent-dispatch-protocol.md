# Agent 调度协议（子代理 Dispatch）— 完整协议

> **本文件是 `skills/ohos-dev-workflow-router/SKILL.md` §Agent 调度协议（摘要）的下沉细节**（Progressive Disclosure references 层）。
>
> **读取条件**：仅当 `workflow_config.yaml.workflow.dispatch_mode` 为 `enabled` 或 `required`（调度器模式）时 MUST READ 本文件全文；单 Agent 模式（`single`，默认）**不读取**本文件——编排器按 `skills/ohos-dev-workflow-router/SKILL.md`「路由规则」顺序执行。`DECISIONS.md` 只用于人工对账。
>
> A1-A7 的结构化映射和技术定义见 `skills/ohos-dev-workflow-router/SKILL.md` §Agent 调度协议摘要；`DECISIONS.md` 保存人类可读的决策记录；向用户提问/汇报时的转译表述见 `skills/ohos-dev-workflow-router/SKILL.md` §决策分级 + 术语大白话。

## 调度模式总览

```
┌─────────────────────────────────────────────────────────────┐
│                    编排器 / 调度器                            │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐              │
│  │ Phase 1  │ → │ Phase 2  │ → │ Phase 3  │   ← 阶段级串行  │
│  │ (direct) │   │ (dispatch)│   │ (dispatch)│     （拓扑序）  │
│  └──────────┘   └────┬─────┘   └────┬─────┘              │
│                     │               │                      │
│              ┌──────┴──────┐ ┌──────┴──────┐             │
│              │ 2a+2b 并行  │ │ 3a→3b 串行  │  ← 子步骤级关系 │
│              │ (2 agents)  │ │ (2 agents)  │             │
│              └──────┬──────┘ └──────┬──────┘             │
│                     │               │                      │
│              ┌──────┴───────────────┴──────┐             │
│              │      Phase 4 (dispatch)      │             │
│              │    GN+linker 配置并行        │             │
│              └────────────┬───────────────┘             │
│                             │                             │
│              ┌──────────────┼──────────────┐             │
│                         ▼                                 │
│                  Phase 5 → Phase 6                         │
│                   (P6: 6a‖6b only when isolated)           │
│                                                             │
│  P7 is an on-demand escape hatch from any blocked phase.   │
└─────────────────────────────────────────────────────────────┘
```

## 阶段 Agent 分发表

每个阶段的分发规格——编排器据此构造 `task()` 调用：

| 阶段 | Agent Role | category | load_skills | 分发模式 | 可并行子步骤 |
|------|:----------:|:--------:|:-----------:|:-------:|:-----------:|
| **P1** env-prep | `infra-specialist` | unspecified-high | [ohos-dev-build-config] | **顺序执行** (Step 1→2→3→4→5 强依赖) | — |
| **P2** kernel-port | `kernel-expert` | deep | [ohos-dev-kernel-source-query, ohos-dev-soc-spec-parse, ohos-dev-build-config, ohos-dev-kernel-trim-config] | **条件并行** | 2a‖2b (都依赖 P1)；2c→2d→2e 串行 |
| **P3** driver-device | `driver-expert` | deep | [ohos-dev-soc-spec-parse, ohos-dev-board-config-gen, ohos-dev-build-config, ohos-dev-hal-skeleton-gen, ohos-dev-rtos-migrate] | **推荐并行** | 先固定共享规格、接口和绑定名称；之后不同外设可并行。3b/HCS 与 3a 驱动有绑定依赖，默认串行；3c 依赖前两者；3d 可选独立。⚠️ 多外设并行时不能同时写 BUILD.gn → 协调 agent 合并 sources |
| **P4** build-verify | `build-expert` | deep | [ohos-dev-build-config, ohos-ci-lite-deploy-burn, ohos-dev-cross-toolchain] | **部分并行** | GN配置‖linker配置；编译串行；修复循环；**烧录验证（ohos-ci-lite-deploy-burn，需用户确认硬件）** |
| **P5** test-gen | `test-expert` | unspecified-high | [ohos-test-lite-ut-gen, ohos-test-lite-adapt-verify] | 直接执行 | **XTS 验证（ohos-test-lite-adapt-verify，需用户确认硬件）** |
| **P6** doc-review | **双 Agent（宿主支持隔离时）** | writing + unspecified-high | [ohos-design-ref-retrieval(6a), ohos-dev-driver-review(6b)] | **完全并行（条件）** | 6a(doc) ‖ 6b(review)；不支持隔离会话则记录 `UNVERIFIED_INDEPENDENCE`，GATE-R 不得 PASS |
| **P7** problem-diag | `diagnostician` | **unspecified-high** (routine) / **ultrabrain** (escalated) | [ohos-dev-build-config, ohos-issue-lite-diagnose] | 直接执行（强顺序: 分析→定位→修复, 不可并行） | — |

> **category 说明**：对应 `task()` 的 category 参数，决定使用哪个优化模型。
> `deep` 用于需要深度领域推理的阶段（P2/P3/P4）；`ultrabrain` 用于 P7 中**真正未知的诊断**（HardFault/启动挂起/间歇性失败）；
> P7 的**常规诊断**（编译 warning 修复 / GT patch / 工具链适配）使用 `unspecified-high` 即可——实测证明 95% 的 P7 调用是模式匹配工作。
> `writing` 用于文档生成（P6a）；`unspecified-high/low` 用于通用任务。
>
> **Runtime 可移植性**：`task(category=..., load_skills=...)` 是与具体 Agent runtime 无关的逻辑接口，宿主映射表见 `DECISIONS.md` §Runtime 可移植性 (F-07)。

## 上下文打包协议

编排器向 子代理 派发任务时，必须传递以下上下文。**这是 StageContext 的序列化格式：**

```yaml
# === 编排器生成的派发上下文 ===
dispatch_context:
  task_id: "P2-kernel-port-{timestamp}"       # 唯一标识
  phase_id: "P2"
  agent_role: "kernel-expert"
  mode: "full"  # full=完整阶段 / partial=单子步骤

target:
  name: "{target.name}"                          # 来自 P1 或用户输入
  arch: "riscv32" | "arm-cortex-m4" | "xtensa"
  ram_size: "{bytes}"
  flash_size: "{bytes}"
  system_type: "mini" | "small"   # mini=L0 轻量 / small=L1 小型
  product_type: "{target.product_type}"
  oh_version: "{version}"

upstream_artifacts:                               # 前序阶段产出（文件路径列表）
  P1:
    - "device/board/{vendor}/{board}/"           # 目录结构
    - "device/board/{vendor}/{board}/config.json"
    - "device/board/{vendor}/{board}/config.gni"

this_phase_scope:                                  # 本阶段契约（来自编排器 §各阶段契约）
  inputs: ["P1_项目骨架", "芯片内核规格"]
  expected_outputs:
    - "Kconfig适配链文件列表"
    - "BUILD.gn编译入口"
    - "startup_S启动代码"
    - "C库适配文件"
    - "linker.ld"
  gate_checklist: ["GATE-K确认项..."]
  tools_available:
    - "skills/ohos-dev-kernel-source-query"
    - "skills/ohos-dev-soc-spec-parse"

execution_constraints:
  retry_policy: "diagnostic.max_auto_rounds"      # 同一错误无进展达到阈值后转交用户
  gate_interaction: "present_all; wait_only_business"
  parallel_siblings: []                            # 同步执行的兄弟 task_id（如有）
```

## 子代理产出格式

子代理 完成后必须返回结构化结果（写入 artifact 文件 + 向编排器报告）：

```yaml
# === 子代理 产出报告 ===
agent_result:
  task_id: "P2-kernel-port-{timestamp}"
  phase_id: "P2"
  status: "success" | "partial" | "failed"        # partial=部分完成（如2a成功但2c失败）

artifacts_produced:                                 # 实际产出的文件路径
  - "device/board/{vendor}/soc/{soc_name}/Kconfig"
  - "device/board/{vendor}/soc/{soc_name}/BUILD.gn"
  - "device/board/{vendor}/soc/{soc_name}/src/startup_S.s"
  # ...

gate_result:                                       # 门控自检结果
  gate_id: "GATE-K"
  self_check:
    Kconfig链完整: true
    BUILD.gn被发现: true
    启动代码链接无undefined: true
    linker地址范围正确: true
    内核可启动到main: "待用户验证"                   # 需要硬件或用户确认的项

blockers:                                          # 未解决的问题（如有）
  - "C库vprintf实现未测试——需P4编译验证"

next_phase_recommendation: "P3"                    # 建议下一阶段
```

## 并行组定义

以下子步骤组可在同一 phase 内**并行派发**给不同 Agent：

### P2 kernel-port 并行组

```
Group P2-G1 (可并行): ──→ 2a(Kconfig) + 2b(BUILD.gn)
  条件: 都只依赖 P1 的目录结构和 config.gni
  Agent: 同一个 kernel-expert（两个轻量任务不需要分开）
  合并: 无冲突（写不同文件）

Group P2-G2 (串行): ──→ 2c(启动代码) → 2d(C库) → 2e(linker)
  条件: 2c+2d 依赖 2a+2d 的 Kconfig 和 BUILD.gn 结果
  Agent: 同一个 kernel-expert
```

### P3 driver-device 并行组

```
Group P3-G1 (默认串行): ──→ 3a(HAL驱动) → 3b(HCS配置)
  条件: 两者共享已确认的接口和绑定名称；HCS 节点必须与驱动实际注册一致
  并行例外: 共享规格/命名冻结后，不同外设的 driver + HCS 成对任务可并行
  协调: 每个任务只提交自身 sources 片段，由编排器统一写入 BUILD.gn

Group P3-G2 (依赖 G1): ──→ 3c(设备树)
  条件: 依赖 3a 的驱动接口定义 + 3b 的 HCS 节点命名

Group P3-G3 (可选,独立): ──→ 3d(RTOS迁移)
  条件: 完全独立，可与 G1 同时进行
  Agent: 可单独派发（不同领域知识）
```

### P6 doc-review 并行组（★ 最重要）

```
Group P6-G1 (完全并行, 独立 Agent): ──→ 6a(文档生成) ‖ 6b(代码审查)

  6a → doc-expert Agent (category: writing, load_skills: [])
    输入: P1~P5 全部产出文件
    产出: 适配手册 + API参考 + 移植指南

  6b → ohos-dev-driver-review Agent (category: unspecified-high, load_skills: [])
    输入: P1~P5 全部产出文件（特别是 P2/P3 的源码）
    产出: 6类规则引擎主分组（FUNC/SEC/EMB/MAINT/STYLE/MISRA）+ 6类↔8维交叉矩阵双视图审查报告

  ★ 宿主支持隔离会话时：6b 必须独立且不知道 6a 的存在（避免"文档说没问题"的偏见）
  ★ 宿主不支持时：记录 UNVERIFIED_INDEPENDENCE，不能签发 GATE-R PASS
```

## 派发伪代码

> **示意代码，不是可直接执行的宿主实现**。`DECISIONS.md` 是人类可读的决策记录，不能被 Markdown 解析器当作运行时配置。宿主适配器必须从显式的结构化配置加载 A1-A7，并把其值与 `DECISIONS.md` 记录对应；缺失映射必须报错或使用声明过的默认值。

```python
def execute_workflow_with_dispatch(project_config, progress):
    """调度模式下的工作流执行"""

    # ═════════ 0. 由宿主适配器加载结构化配置 ═════════
    decisions = host_adapter.load_dispatch_config(project_config)
    host_adapter.validate_decision_mapping(decisions)  # A1-A7 与 DECISIONS.md 对账

    # ═════════ 1. 模式判定 ═════════
    dispatch_mode = decisions.get("A5", "不需要")
    # 单 Agent 模式也可执行 P6；是否能给出独立审查结论取决于宿主能力。
    if dispatch_mode == "不需要":
        return execute_sequential(project_config, progress)

    # ═════════ 2. 阶段级串行（拓扑序不变）═════════
    # P7 是按需切入的诊断逃生舱，不属于下面的正常阶段遍历；失败时由路由器单独调用。
    for phase in [P1, P2, P3, P4, P5, P6]:
        if should_skip(phase, decisions):
            phase_result = normalized_skipped_result(phase, decisions)
        else:
            phase_result = execute_phase(phase, DISPATCH_TABLE[phase], host_adapter)

        # ═════════ 3. 门控检查 (所有模式共用) ═════════
        handle_phase_result(phase, phase_result)
        if phase.gate:
            handle_gate(phase.gate, phase_result.gate_result.self_check)

    generate_completion_report()

def execute_phase(phase, spec, host_adapter):
    """每个分支都返回同一 phase-result schema。"""
    if spec.mode == "完全并行":
        if host_adapter.supports_isolated_sessions():
            return normalize_phase_result(
                phase, collect_all([dispatch_p6_doc(), dispatch_p6_review_isolated()]))
        return normalize_phase_result(
            phase, execute_p6_single_session(),
            independence_status="UNVERIFIED_INDEPENDENCE")
    if spec.mode == "推荐并行":
        results = dispatch_independent_peripherals_and_merge_build_gn(phase, spec)
        return normalize_phase_result(phase, results)
    if spec.mode in ("条件并行", "部分并行"):
        results = execute_parallel_groups_and_merge(phase, spec)
        return normalize_phase_result(phase, results)
    return normalize_phase_result(phase, dispatch_single(phase, spec, build_context(phase)))

def dispatch_p7(error_context, project_config):
    """P7 不在正常 phase loop 中；在派发前按 A6 决定 category。"""
    category = p7_dispatch_category(error_context)  # A6 的确定性规则
    return dispatch_single(P7, DISPATCH_TABLE[P7]._replace(category=category), error_context)
```

## should_dispatch() 判定函数

> 完整定义见 `DECISIONS.md` §A5。此处为摘要:

```python
def should_dispatch(phase_id, decisions):
    conditional = {"P2": True, "P3": True, "P4": True}  # 有并行收益的阶段
    return phase_id in conditional and decisions["A5"] != "不需要"
```

## 各阶段 Agent Prompt 模板结构

每个阶段 SKILL.md 中的 **Agent 分发规格**章节（§Agent Dispatch Spec）定义了如何构造 `task()` 的 prompt。

通用 6-section prompt 结构：

```
1. TASK:        （阶段目标 + 子步骤清单 + 产出要求）
2. EXPECTED:    （具体交付物文件列表 + 通过标准）
3. TOOLS:       （load_skills 列表 + 每个 tool 的用途说明）
4. MUST DO:     （强制执行规则：检查清单、格式要求、禁忌事项）
5. MUST NOT DO: （禁止行为：不修改的文件、不做的事、不做的假设）
6. CONTEXT:     （上游产出路径、项目参数、当前进度状态）
```

> 各阶段的具体 Prompt 内容见 `{{ASSET_ROOT}}/workflow/steps/NN-name/SKILL.md` 中的 **§Agent Dispatch Spec**。
