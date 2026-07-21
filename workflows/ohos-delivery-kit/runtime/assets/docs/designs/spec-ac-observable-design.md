# Spec AC 可观测性与内部实现分离 — 设计记录

**状态**: 已实施（P1，分支 `feat/spec-ac-observable-p1`，详见该分支 git log）
**关联**: [#90](https://gitcode.com/oshunter/ohos-delivery-kit/issues/90)（方案 issue）/ [#56](https://gitcode.com/oshunter/ohos-delivery-kit/issues/56)（原始问题）/ #38（已合，本设计撤其 Path B）/ #43（[DT] 思路被本设计否定）

## 背景

### 问题（#56）

偏内部实现规格描述的 spec 缺典型用户场景与操作描述，测试设计环节难生成高质量测试步骤与检查点；proposal 也缺用户场景化描述。

验证 #56 真实存在：example `spec.md` 的 `AC-1.1`（THEN="注册到焦点管理器节点表"）、`AC-3.1`（THEN="从注册表移除、焦点链转移"）是部件内部实现，非用户可观测。

### 既有方案冲突（#38 vs #43）

| PR | 方案 | 哲学 |
|---|---|---|
| **#38**（已合） | proposal 加用户场景 + spec-for-validation 派生，spec.md 保持纯契约 | 分离派：spec 做不好用户场景 → 放 proposal + spec-for-validation |
| **#43**（open） | spec.md 加 `[DT]` 标记内部实现 + 补充用户场景 AC | 强化派：spec.md 就地修（标记 + 补场景） |

两者互斥。本设计（方案 D）基于业界调研提出第三路线。

## 业界调研依据

调研 GitHub spec-kit（ODK profiles 借鉴源）、Kiro (AWS)、OpenSpec，三方共识：

- **spec-kit**：`spec.md` = WHAT/WHY，**禁止实现细节**（languages/frameworks/APIs/code structure）；`plan.md` = HOW；用户场景（Given/When/Then）在 spec 内；quality checklist 明文 "No implementation details leak into specification"；标记机制只有 `[NEEDS CLARIFICATION]`（标模糊，不标内部实现）
- **Kiro**：EARS 需求语法 + user stories/AC + design 分离；"outcomes matter more than implementation details"
- **OpenSpec**：behavior-first，spec = behavior contract（Requirements + Scenarios），design/tasks = how

### 关键发现

**业界主流不在 spec 内标记"内部实现"——而是禁止它进 spec，把实现细节移到 design/plan。** 没有任何主流工具用"在 spec 内标记内部实现"的方式。这直接否定了 #43 的 `[DT]` 标记思路（业界是移除实现而非标记）。

## 设计（方案 D）

### 核心原则

1. **spec = 接口可观测行为契约**：AC 描述通过接口边界可观测的行为，禁部件内部实现
2. **内部实现移 design**：状态机/注册表/内部流程/算法归 design「状态归属与不变量」
3. **三层验收**：proposal 系统级 / spec 接口级 / design 内部级（白盒 TDD）

### 12 条边界规则（定稿）

| # | 规则 | 内容 |
|---|---|---|
| 1 | 可观测边界 | public/system API + **innerAPI**（部件间交互契约）+ 终端用户可感知 = 可观测 |
| 2 | 内部实现去向 | 部件内部数据结构/状态机/流程/算法 → 移 design |
| 3 | innerAPI 切分 | innerAPI **契约**（签名+行为）留 spec；**实现**移 design |
| 4 | AC 格式 | Given/When/Then（补 Given，对齐业界） |
| 5 | proposal SC 边界 | 写到接口签名/参数/错误码 = 越界 → 下放 spec AC |
| 6 | proposal US | 降级保留 = 业务上下文层（why：业务触发/角色/价值），无 AC 级操作序列 |
| 7 | BR / 异常表 | **放宽**——约束声明 + 简短内部线索可留 spec；详细内部展开移 design |
| 8 | design 验证 | **不显式白盒验证**；内部实现靠 TDD 验证（execution-plan 单测） |
| 9 | spec-for-validation | **保留**——旁路产物，测试设计用，非代码生成主流程；做集成/系统验证场景，不搬 proposal US |
| 10 | 代码映射（Z） | 接口契约（接口变更分析）留 spec；代码映射（AC→实现文件）移 **execution-plan**（非 design） |
| 11 | proposal SC | 系统级能力达成（可观察、可量化，禁内部实现 + 禁接口细节） |
| 12 | `[DT]` 标记 | 放弃（业界是移除实现而非标记） |

### 三层验收模型

| 层 | 产物 | 验收什么 | 怎么验证 | 可观察要求 |
|---|---|---|---|---|
| 系统级 | proposal 成功标准 | 业务价值达成 | 系统级可观察指标 | 可观察、可量化（禁内部实现） |
| 接口级 | spec AC | 接口行为契约 | 黑盒（调接口看返回/回调） | 三层接口边界可观测 |
| 内部级 | design 状态归属与不变量 | 内部不变量保持 | 白盒 TDD（execution-plan 单测） | 内部不变量可验证 |

### 代码映射迁移（决策 Z）

代码映射（AC → 实现文件 + Task + 验证状态）原在 `spec.md §代码映射`。迁移目标三选：

- ~~移 design.md~~ — ❌ design 是架构决策层，代码映射是执行追溯层，职责错；且 design 实现前生成、代码映射实现后才完整，时序别扭
- ~~留 spec.md~~ — ⚠ 冗余（execution-plan 已有 AC-Task 追溯 + 代码范围映射）
- **移 execution-plan.md** — ✅ execution-plan 已 owns `ac_task_traceability` + `file_scope` + `actual_results`，已有「AC 到 Task 追溯」+「代码范围映射」章节，代码映射信息本就在那

落地：`execution-plan.md`「AC 到 Task 追溯」的"覆盖？"列升级为"验证状态（Pass/Fail/Blocked）"，承接归档就绪判定；validate Level C/D 改读 execution-plan。

## 与既有 PR 的关系

- **#38**（已合）：本设计撤其 Path B（spec-for-validation 从 proposal US 派生 → 改从 spec AC 派生）+ proposal US 降级（典型操作序列 → 业务价值）。#38 的 proposal conditional「用户场景与业务触发」机制保留（降级为业务上下文）
- **#43**（open）：`[DT]` 标记思路被业界调研否定，待关闭；其 Step 5"用户场景进 spec"方向对，但用本设计的"强化 spec US 章节 + AC 可观测规范"实现

## 改动范围（P1，19 文件）

| 层 | 文件 | 改动 |
|---|---|---|
| 核心模板 | spec.md / proposal.md / execution-plan.md / spec-for-validation.md | AC Given/When/Then+三层可观测；BR 放宽；代码映射移 execution-plan；execution-plan 列扩验证状态；proposal US 降级+SC 系统级；spec-for-validation 撤 #38 Path B |
| 契约/校验 | artifacts.yaml / validate-artifacts-contract.py | spec 去"代码映射"；validate Level C/D 改读 execution-plan（含 TASK_RE 拆分多 Task + 代码范围映射文件校验） |
| SKILL | odk-spec / odk-design / odk-propose / odk-spec-for-validation | AC 写作规范；design 承接内部实现+TDD；proposal SC 系统级；spec-for-validation 回归本职 |
| docs | code-traceability / contracts / quick-start / validator | 代码映射机制迁 execution-plan 的全文同步（含 code-traceability 核心机制重构） |
| 示范 | arkui spec/proposal/execution-plan + issue-002 spec/execution-plan | AC 可观测化；US 业务价值；SC 系统级；execution-plan 验证状态+代码范围映射口径 |

## 验证

- `check-examples.sh`: Passed 10 / Failed 0（Warnings 6 是 #38 遗留 conditional section，非本次引入）
- `validate-doc-drift.sh`: 3 passed / 0 failed
- `validate-artifacts-contract.py`: syntax OK，archive 模式校验「AC 到 Task 追溯」验证状态 +「代码范围映射」文件覆盖

## OS 场景适配说明

OpenHarmony 是基础 OS 设施（大量子系统/部件），不能完全套用业界普通软件开发规范。本设计的 OS 适配点：
- **innerAPI 留 spec**：部件间交互契约是 spec 的一部分（业界普通软件无此层）
- **接口变更分析留 spec**：OpenHarmony 重接口契约，接口签名表留 spec（业界 spec 纯行为无技术细节）
- **BR/异常分类保留**：OS 错误码/边界规则重要，BR/异常表是 spec 必需章节（业界统一 Requirements）
- **spec-for-validation 保留**：OS 测试设计需要集成/系统验证旁路（业界 spec scenarios 直接派生测试）

## 后续

- **#43 关闭**：`[DT]` 思路否定，建议关闭/大改
- **#90 讨论**：本设计与 @Lyuxin @l00555582 对齐边界后落地
- **code-traceability.md 总览图**：ASCII art 总览图（L278-304）本轮用文字改核心机制，图形重绘留后续
- **P2 可选**：check-examples 加 AC 可观测性 warn 检查（软约束）
