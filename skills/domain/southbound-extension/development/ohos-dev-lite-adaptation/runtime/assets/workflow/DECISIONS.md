# DECISIONS.md — 工作流决策记录

> **本文件是 skills/ohos-dev-workflow-router/SKILL.md (编排器) 的人类可读决策记录。**完整调度协议见 `skills/ohos-dev-workflow-router/references/agent-dispatch-protocol.md`。它不是机器可解析的运行时配置；宿主适配器必须从结构化配置显式映射 A1-A7，并将映射结果与本记录对账。

> **与 `workflow_config.yaml` 的关系（互补不互替）**：
> - **DECISIONS.md（本文件）** 记录 A1-A7 决策变量及其理由，供人类审核和宿主适配器对账。
> - **`workflow_config.yaml`** 装结构化配置（`target.*` / `workflow.*` / `intake.*` / `phases.*` / `experience.*`），由用户填 `{{ASSET_ROOT}}/workflow/workflow_config.template.yaml` 触发跳过询问；各 step 按需读取所需段。
> - 本文件中"见 `workflow_config.yaml.phases.*`"的引用（如 A4 `trim_components`）指向结构化配置，关系正确：DECISIONS 指策略变量，yaml 指结构化配置。

---

## A1: 项目模式

| 选项 | 值 | 含义 | 默认 |
|------|-----|------|:----:|
| `mode` | `full` | 完整 7 阶段工作流 (P1→P2→P3→P4→P5→P6；P7 为任意阶段可切入的诊断逃生舱) | ✅ |
| `mode` | `verify-only` | 仅 P4 编译验证 (Round-Trip Phase B 模式) | — |
| `mode` | `quick-prototype` | 跳过 P5/P6, 快速出固件 | — |

**当前值**: `full`

---

## A2: 目标系统

| 字段 | 值来源 | 示例 |
|------|--------|------|
| `target.system_type` | 用户输入 / chip-spec | `mini`=L0 轻量（liteos_m）/ `small`=L1 小型（liteos_a） |
| `target.arch` | 用户输入 / chip-spec | `riscv32` / `arm-cortex-m4` |
| `target.product_type` | 用户输入 / config.json | `wifiiot` / `camera` |

**影响**: L0 vs L1 决定 P2(C库)、P3(驱动模型)、P4(多产物) 的全部行为分支。

---

## A3: 可选阶段

| 阶段 | 默认行为 | 跳过条件 | 当前值 |
|------|---------|---------|:------:|
| P5 测试 | 执行 | `phases.p5_test_gen.enabled: false`（用户明确）；无 HIL 仅跳过 P5-B | **执行** |
| P6 文档+审查 | 执行 | `phases.p6_doc_review.enabled: false` 或 `workflow.mode: quick-prototype` | **执行** |
| P3d RTOS 迁移 | 跳过 | `phases.p3_driver_device.rtos_migration_enabled: true` 才执行 | **跳过** |

---

## A4: 内核裁剪策略（已合并入 P2）

> **原为独立决策项，v0.2 重构时将"内核裁剪"合并为 P2 Step 2a（Kconfig 适配）的子步骤。**
> 保留此占位以维持编号连续性。

| 字段 | 值 | 说明 |
|------|-----|------|
| `trim_strategy` | `"integrated"` | 裁剪逻辑已集成到 P2 Kconfig 配置阶段 |
| `trim_components` | `workflow_config.yaml.phases.p2_kernel_port.trim_components` | 按需启用的裁剪项 |

---

## A5: 子代理分发模式 ★ 核心决策

> **结构化来源是 `workflow_config.yaml.workflow.dispatch_mode`；本节记录其对应的人类决策和理由。**
>
> **值域映射（中文决策值 ↔ `workflow.dispatch_mode` 英文枚举）**：`single`="不需要" / `enabled`="可选(已启用)" / `required`="需要"。宿主适配器读英文枚举；下表中文值仅供人类阅读。

### 选项

| 值 | `workflow.dispatch_mode` | 含义 | 触发条件 |
|-----|------|------|---------|
| `"不需要"` | `single` | **单 Agent 顺序模式** — 编排器自己按路由规则顺序执行所有阶段 | 默认。小项目 / 首次适配 / 快速验证 |
| `"可选(已启用)"` | `enabled` | **调度器模式** — P2/P3/P4 派发给独立子代理并行执行 | 中大型项目 / 多外设 / 有并行收益 |
| `"需要"` | `required` | **强制调度器 + 全量并行** | 大型 SoC (10+ 外设) / CI/CD 自动化流水线 |

### 当前值

```yaml
A5: "不需要"   # = workflow.dispatch_mode: single
reason: "子代理调度模式从未实际运行过；在 Round-Trip 尚未通过单 Agent 模式验证前启用调度，违背方法论 §4.5.8 '先保证正确，再追求质量'。降级为单 Agent 顺序模式。P6 仅在宿主支持隔离会话时执行独立并行；否则记录 UNVERIFIED_INDEPENDENCE，不能签发 GATE-R PASS。待单 Agent Round-Trip 收敛后再考虑升级。"
```

### 运行时判定逻辑

编排器在每次进入阶段前执行:

```python
def should_dispatch(phase_id):
    """判断当前阶段是否应该派发为独立子代理"""
    
    # 1. 全局模式检查；P6 是否可隔离并行由宿主能力决定
    #    （decisions["A5"] 的值域即 workflow.dispatch_mode：
    #      "不需要"=single / "可选(已启用)"=enabled / "需要"=required）
    if decisions["A5"] == "不需要":
        return False

    # 2. 阶段级有条件规则
    conditional_dispatch = {
        "P2": True,   # P2 2a‖2b 有并行收益
        "P3": True,   # P3 多外设有并行收益 (需协调 BUILD.gn)
        "P4": True,   # P4 GN‖linker 配置有并行收益
    }
    if phase_id in conditional_dispatch and decisions["A5"] != "不需要":
        return True
    
    # 4. 默认: 不派发
    return False
```

---

## A6: P7 诊断级别自动升降级

> **解决 P7 category 过配问题**: 不是所有 P7 调用都需要 ultrabrain。

### 升级规则

```
P7 触入时:
│
├─ 错误类型匹配已知模式? (查 compiler_fix_playbook Decision Tree)
│   ├─ YES → category = **unspecified-high**, load_skills = [ohos-dev-build-config]
│   │         这是 routine fix (约 95% 的场景)
│   └─ NO  → 继续判断 ↓
│
├─ 连续 3 轮 stuck 在同一错误?
│   ├─ YES → category = **ultrabrain**, load_skills = [ohos-dev-build-config]
│   │         Escalate! 需要跨领域推理
│   └─ NO  → 继续判断 ↓
│
├─ 涉及 HardFault / 启动挂起 / 间歇性失败?
│   ├─ YES → category = **ultrabrain**, load_skills = [ohos-dev-build-config]
│   └─ NO  → category = **unspecified-high**, load_skills = [ohos-dev-build-config]
│             (常规诊断足以处理)
```

### 实现参考

```python
def p7_dispatch_category(error_context):
    """根据错误上下文决定 P7 的 category"""
    
    import re
    message = error_context.error_message.lower()

    # stuck 或未知运行时问题优先升级
    if error_context.same_error_count >= 3:
        return "ultrabrain"
    unknown_indicators = ["hardfault", "busfault", "usagefault", "hang", "timeout", "intermittent", "boot fail"]
    if any(i in message for i in unknown_indicators):
        return "ultrabrain"

    # 检查已知编译模式
    known_patterns = [
        r"undefined reference", r"warning.*error", r"region.*overflowed",
        r"unrecognized option", r"__attribute__", r"cast-function-type",
        r"nostartfiles", r"gcc_ver", r"csrr", r"csrw"
    ]
    if any(re.search(p, message) for p in known_patterns):
        return "unspecified-high"  # routine: 查 playbook Decision Tree 即可
    
    return "unspecified-high"
```

---

## A7: 经验积累模式（Experience Accumulation）★ 用户可控回填开关

> **P-失败回填原则的用户可控开关**（经验积累机制）：决定本次适配的根因/教训是否回填到工作流正文/语料。
> **默认 manual 不回填**——GATE-交付 时问用户是否回填 + 回填哪些，用户不主动说 yes 就不回填（避免污染通用工作流）。
> 结构化配置在 `workflow_config.yaml.experience`（见 `{{ASSET_ROOT}}/workflow/workflow_config.template.yaml` §13）。

### 选项

| 值 | 含义 | 触发条件 | 默认 |
|-----|------|---------|:----:|
| `manual` | **默认不回填**——GATE-交付 时停下问用户"本次适配有哪些值得回填的教训？要回填哪些？"，用户明确说 yes 才回填，不主动回填 | 默认。真实用户首次适配，保持工作流通用 | ✅ |
| `auto` | **自动回填**——各阶段收尾时自动把定位到的根因/教训写入对应 step SKILL.md / references/ | 调试追踪项目（多轮验证场景），主动积累教训 | — |
| `off` | **不回填**——显式关闭回填通道，即使阶段收尾有可回填的经验也不写 | 一次性原型 / 用户明确不想污染工作流 | — |

### 当前值

```yaml
A7: manual
reason: "默认 manual 不回填，避免真实用户首次适配的特定芯片教训污染通用工作流。GATE-交付 时问用户是否回填。调试追踪项目（多轮迭代）可改 auto 主动积累。"
```

### 回填范围（A7=auto 时生效，A7=manual 时问用户选哪些）

| 范围标签 | 回填目标 | 内容 |
|---------|---------|------|
| `cases` | `skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md` | 诊断案例（错误现象→根因→修复→验证） |
| `fault-kb` | `skills/ohos-issue-lite-diagnose/references/fault-knowledge-base.md` | 故障知识库条目（错误码/寄存器值→根因映射） |
| `methods` | 对应 step 的 `SKILL.md` 方法节 | 正文方法（如 GATE-0 加工具链全扫、GATE-B+ 加消费者验收） |

### 个性化标签

回填时在每条教训末尾打 `（来源：{chip} @ {iter}, {date}）`，区分通用教训 vs 个性化教训（特定芯片/特定迭代）。`workflow_config.yaml.experience.personalize_tag: true` 默认开启。

### 运行时判定逻辑

编排器在 GATE-交付 后执行经验回填环节：

```python
def experience_backfill(decisions, workflow_config):
    """GATE-交付 后置：经验回填环节"""
    
    mode = decisions.get("A7", "manual")
    scope = workflow_config.experience.scope  # [cases, fault-kb, methods]
    personalize = workflow_config.experience.personalize_tag
    
    if mode == "off":
        return  # 跳过
    
    if mode == "manual":
        # 停下问用户：是否回填 + 回填哪些
        user_choice = ask_user("本次适配有哪些值得回填的教训？要回填哪些？")
        if not user_choice.confirm:  # 用户不主动说 yes 就不回填
            return
        scope = user_choice.selected_scope
    
    if mode == "auto":
        # 自动回填所有定位到的根因/教训
        pass
    
    # 执行回填（manual 用户确认后 / auto 自动）
    for lesson in collected_lessons:
        tag = f"（来源：{chip} @ {iter}, {date}）" if personalize else ""
        if "cases" in scope:
            append_to("skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md", lesson + tag)
        if "fault-kb" in scope:
            append_to("skills/ohos-issue-lite-diagnose/references/fault-knowledge-base.md", lesson + tag)
        if "methods" in scope:
            append_to_corresponding_step_skill(lesson + tag)
```

### 回填纪律

- **manual 模式**：用户说 yes 才回填，说 no 就不回填——不准"我觉得有用就回填"。
- **auto 模式**：回填也要打个性化标签，避免通用工作流被特定芯片教训污染。
- **回填时机**：P6 文档审查之后、GATE-交付 收尾前完成。

---

## Agent Role 映射表

> **agent_role (语义名称) ↔ subagent_type (宿主子代理类型参数) + category 的正式映射。**
> 编排器和 Step SKILL 都引用此表保持一致。宿主 runtime 差异见下方"Runtime 可移植性 (F-07)"。

| agent_role | subagent_type | category | 典型 load_skills | 使用场景 |
|-----------|:-------------:|:--------:|:-----------------|---------|
| `generalist` | `general` | `unspecified-low` | `[]` | 简单任务（已废弃, 被 infra-specialist 替代） |
| **`infra-specialist`** | **`general`** | **`unspecified-high`** | **`[ohos-dev-build-config, ohos-dev-cross-toolchain]`** | **P1: 环境搭建 + GATE-0** |
| `kernel-expert` | `general` | `deep` | `[ohos-dev-kernel-source-query, ohos-dev-soc-spec-parse, ohos-dev-build-config, ohos-dev-kernel-trim-config]` | P2: 内核移植 |
| `driver-expert` | `general` | `deep` | `[ohos-dev-soc-spec-parse, ohos-dev-board-config-gen, ohos-dev-build-config, ohos-dev-hal-skeleton-gen, ohos-dev-rtos-migrate]` | P3: 驱动开发 |
| `build-expert` | `general` | `deep` | `[ohos-dev-build-config, ohos-ci-lite-deploy-burn, ohos-dev-cross-toolchain]` | P4: 构建验证 + 烧录 |
| `test-expert` | `general` | `unspecified-high` | `[ohos-test-lite-ut-gen, ohos-test-lite-adapt-verify]` | P5: 测试生成 + XTS 验证 |
| `doc-expert` | `general` | `writing` | `[ohos-design-ref-retrieval]` | P6a: 文档生成（注：ohos-design-ref-retrieval 实为参考资料检索助手） |
| `ohos-dev-driver-review` | `general` | `unspecified-high` | `[ohos-dev-driver-review]` | P6b: 代码审查 |
| **`diagnostician` (routine)** | **`general`** | **`unspecified-high`** | **`[ohos-dev-build-config, ohos-issue-lite-diagnose]`** | **P7: 常规诊断 (95%)** |
| **`diagnostician` (escalated)** | **`general`** | **`ultrabrain`** | **`[ohos-dev-build-config, ohos-issue-lite-diagnose]`** | **P7: 深度诊断 (5%)** |
| `explore` | `explore` | — | `[]` | 后台探索 (非阶段执行) |
| `librarian` | `librarian` | — | `[]` | 后台文献检索 (非阶段执行) |
| `oracle` | `oracle` | — | `[]` | 高难度咨询 (按需调用) |
| `metis` | `metis` | — | `[]` | 前规划咨询 (按需调用) |
| `momus` | `momus` | — | `[]` | 计划审查 (按需调用) |

**映射规则**:
1. 所有阶段执行 agent 的 `subagent_type` 都是 `general`（通用执行角色）
2. 区别在于 `category`（决定模型优化方向）和 `load_skills`（决定注入的 skill 知识）
3. 特殊 agent（explore/librarian/oracle/metis/momus）不参与阶段执行，作为**辅助工具**按需调用

### Runtime 可移植性（F-07）

> **`task(category=..., load_skills=...)` 是与具体 Agent runtime 无关的逻辑接口**，不是绑定 OpenCode 的 API。
> 编排器伪代码用 `task()` 表达"派发一个带特定能力配置的子任务"的语义；实际运行时由宿主 Agent runtime 实现。

| 宿主 runtime | `task()` 映射 | `category` 映射 | `load_skills` 映射 |
|---|---|---|---|
| OpenCode | `task(category=..., load_skills=...)` 原生 | 原生参数 | 原生参数 |
| Claude Code | `Agent` 工具 + `subagent_type` | 选对应 subagent type（如 `oh-my-claudecode:executor`）或省略 | 在 prompt 中注入"加载以下 SKILL：..."指令 |
| 单 Agent 模式（A5="不需要"，即 `dispatch_mode: single`） | 不派发，编排器自身顺序执行 | — | — |

> **当前状态**：A5 已降级为"不需要"（`dispatch_mode: single`，F-06），`task()` 暂不实际调用。未来启用调度时，按本表映射到宿主 runtime，无需改伪代码。

---

## 并发安全约束

### 文件写入冲突矩阵

| 文件 | 可能写入的阶段 | 并行风险 | 缓解策略 |
|------|:------------:|:-------:|---------|
| `config.json` | P1 | 🟢 低 (只写一次) | 无需协调 |
| `config.gni` | P1 | 🟢 低 (只写一次) | 无需协调 |
| `BUILD.gn` (board) | P1, **P3** | 🔴 **高** | **P3 并行时: 各 driver agent 输出 sources 列表片段 → 由协调 agent (或编排器) 合并后统一写入** |
| `BUILD.gn` (soc) | P2, **P3** | 🔴 **高** | 同上 |
| `linker.ld` | P2, P4 | 🟡 中 (P2 写初版, P4 可能调优) | P4 修改前确认 P2 不再写入 |
| `*.c` (hal_*) | P3 (各外设独立) | ✅ 无 (不同文件) | 安全并行 |
| `*.c` (kal_*) | P2 (各模块独立) | ✅ 无 (不同文件) | 安全并行 |
| `*.h` | P1-P3 (preserved) | ✅ 无 (不修改) | 安全 |
| `patches_manifest.json` | P7 | 🟡 中 (追加式写入) | 串行即可 (JSON append 是原子操作吗? → 用 file lock 更安全) |

### P3 并行协调协议

当 P3 以多外设并行模式执行时:

```
Option A (推荐): 编排器协调模式
  ├── 编排器自己负责 BUILD.gn 合并
  ├── 派发 N 个 driver agent (每个一个外设)
  │   └── 每个 agent: 只产出 hal_{name}.c + config.h (不写 BUILD.gn)
  ├── 收集所有产出
  └── 编排器: 合并 sources 列表 → 写入 BUILD.gn

Option B: 协调 agent 模式
  ├── 派发 1 个 coordinator agent + N 个 driver agent
  ├── Coordinator: 负责 BUILD.gn 合并 + 3c 配置
  ├── Driver agents: 只产出 .c 文件
  └── Coordinator 等待所有 Driver 完成后合并写入

Option C (简单): 串行 fallback
  └── 如果外设 ≤ 3 个, 直接串行生成 (并行收益不够抵消协调开销)
```

**当前推荐**: Option A（编排器自身协调，最简单可靠）。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1 | 2026-06-27 | 初版: 从编排器 dispatch 伪代码中提取, 补全运行时入口 |
| v0.2 | 2026-07-27 | 新增 A7 经验积累模式（manual 默认不回填 / auto 自动回填 / off 不回填）+ 回填范围 + 个性化标签 + 运行时判定逻辑。经验积累机制落地 |
