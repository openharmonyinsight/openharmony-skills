# Validation Specification Template — Design Notes

**状态**: 已实施（已从 `odk-test-spec` / `test-spec.md` 重命名为 `odk-spec-for-validation` / `spec-for-validation.md`）  
**关联 Issue**: [#12](https://gitcode.com/oshunter/ohos-delivery-kit/issues/12)

> **2026-06 重命名说明**: 原名"测试规格"(test-spec)改为"验证规格"(spec-for-validation)，
> 以区分验证活动（what to validate）与测试设计活动（how to test）。
> 文档中保留历史设计决策原文，仅更新产物名称引用。

## 设计约束

1. 验证模板是 spec + design 的**派生产出**，不作为代码生成主流程
2. **不污染主上下文** — 模板和技能不自动注入，仅在用户显式调用时加载
3. 若内容对代码生成有帮助 → 晋升到 spec 模板；若无帮助 → 独立模板承载
4. 命名为"验证规格"(spec-for-validation)而非"测试规格"(test-spec)，避免与测试设计活动的测试规格概念混淆

## 内容分析：代码生成价值 vs 测试关注点

对 #12 模板各章节逐一评估：

| #12 模板章节 | 类型 | 处理方式 |
|-------------|------|----------|
| 模板前置说明（文档结构） | meta | 独立模板保留 |
| Gherkin 语法示例 + 案例对比 | 写作指导 | blockquote 引导（类似 #11 模式） |
| 规范简要说明 + 标签 | 验证元信息 | 独立模板保留 |
| 同源绑定要求（输入源清单） | 追溯性 | **删除** — spec.md 验证映射 + execution-plan 代码映射已覆盖此职责 |
| 验证重点/非验证重点 | 范围界定 | 独立模板保留 |
| 环境前置与公共配置 | 验证基础设施 | 独立模板保留 |
| 场景：正常流程 (Happy Path) | 验证 | **删除** — spec.md AC 已覆盖，只保留引用说明 |
| 场景：异常流程 (Error) | 验证 | **删除** — spec.md 异常与边界规则已覆盖 |
| 场景：兼容性验证 | 验证 | 独立模板保留（spec.md 兼容性声明是设计视角，验证矩阵是验证视角） |
| 场景：性能验证 | 验证 | 独立模板保留 |
| 场景：功耗验证 | 验证 | 独立模板保留 |
| 场景：安全与权限 | 验证 | 独立模板保留（错误码已在 spec.md，但安全验证场景是验证视角） |
| 概念定义 (Concepts) | 验证复用 | 独立模板保留 |
| 变更历史 | meta | 独立模板保留 |

### 不需向 spec.md 晋升任何内容

理由：
- Gherkin Given/When/Then — spec.md 的 WHEN/THEN 已覆盖，WHEN 本身隐含前置条件
- 错误码触发场景 — spec.md 错误码定义表已有"触发条件"列
- 兼容性矩阵 — spec.md 兼容性声明已覆盖，验证矩阵是衍生验证

---

## 架构设计

### 文件布局

```
core/templates/
├── ai/                          # 主流程模板（using-odk 自动注入上下文时引用）
│   ├── proposal.md
│   ├── design.md
│   ├── spec.md
│   └── execution-plan.md
├── test/                        # 测试模板（独立，不自动注入）
│   └── spec-for-validation.md   # 新增（原 test-spec.md）
└── review/                      # 评审模板
    ├── spec-compliance.md
    ├── code-review.md
    └── verification.md
```

关键：验证模板放在 `core/templates/test/` 而非 `core/templates/ai/`，表示它不属于主流程 AI 模板集。

> **⚠ 实际实现偏差**：最终模板放在了 `core/templates/ai/spec-for-validation.md`（与主流程模板同目录），
> 技能命名为 `odk-spec-for-validation`（原 `odk-test-spec`，原 `odk-test`）。
> 目录物理隔离的设计意图未执行，
> 但通过 `contracts/artifacts.yaml` 中 `required: false` + `bypass: true` 实现了等效的逻辑隔离。

### 技能设计: `odk-spec-for-validation`

作为**可选技能**，不加入主流程。

```
核心流程（不变）:
  odk-init → odk-propose → odk-spec → odk-design → odk-plan → [实现] → odk-review → odk-validate

可选派生流程:
  odk-spec + odk-design → odk-spec-for-validation → spec-for-validation.md
```

`odk-spec-for-validation` 不在 README 工作流程图中列出（避免混淆主流程），仅在"可用命令"表中标记为可选。

### 输入输出

```
输入:  spec.md (AC、错误码、异常规则、兼容性声明)
       design.md (架构、模块影响)
输出:  .codespec/changes/<id>/spec-for-validation.md
```

### 上下文隔离

- `using-odk` **不**引用验证模板 — 主流程不会加载验证模板内容
- `distribute-skills.sh` 照常生成 `odk-spec-for-validation` 技能到三平台
- 仅在用户显式调用 `odk-spec-for-validation` 时，AI 才读取 `core/templates/ai/spec-for-validation.md`
- 模板文件放在 `core/templates/ai/` 下，通过 `contracts/artifacts.yaml` 中 `required: false` + `bypass: true` 实现逻辑隔离
- `using-odk` 的 Available Phase Skills 表**不**列出 `odk-spec-for-validation`（避免膨胀主上下文）

---

## 模板设计

基于上述分析，模板应**删减**与 spec.md 重复的章节，**保留**测试独有的内容：

### 保留的章节

| 章节 | 理由 |
|------|------|
| 规范简要说明 + 全局标签 | 测试元信息，方便过滤执行 |
| 验证重点/非验证重点 | 验证范围界定 |
| 环境前置与公共配置 | 验证基础设施，spec.md 无对应 |
| 兼容性验证场景 | 验证视角的兼容性矩阵，比 spec.md 声明更细粒度 |
| 性能验证场景 | 运行时指标，spec.md 不覆盖 |
| 功耗验证场景 | 同上 |
| 安全与权限验证场景 | 验证视角，验证 401/403 而非定义错误码 |
| 概念定义 (Concepts) | 测试步骤复用 |
| 数据驱动表（场景内嵌，条件性） | 多边界值场景的测试数据；简单场景参数内联 |
| 变更历史 | 版本追溯 |

### 删除的章节（spec.md 已覆盖）

| 章节 | 替代方式 |
|------|----------|
| 同源绑定要求 | spec.md 验证映射 + execution-plan 代码映射已有追溯链 |
| 正常流程场景 | 引导说明："spec.md AC 已覆盖正常流程，此处不重复" |
| 异常流程场景 | 引导说明："spec.md 异常与边界规则已覆盖，此处仅补充集成验证角度的并发/重放等场景" |

### 数据驱动表关联策略（#60）

PR #35 曾在 SKILL Step 4 要求 "each table MUST be associated with a specific SC-N"，
但模板 `## 数据驱动` 是独立通用示例表、未体现关联，且简单场景被强塞表反而冗余。

决策（#60）：数据驱动表改为**条件性、场景内嵌** —— 仅当某 SC-N 含多组边界值参数组合、
内联累赘时，才在该场景块内部嵌一张表；表随场景，关联由位置隐含，无需独立节或关联列；
简单场景参数内联于 Given/When/Then。与同模板"性能/功耗/安全条件块"模式一致。

### 精简后模板结构

```markdown
# [特性名称] 验证规格

> 基于 spec.md 和 design.md 派生。spec.md 已描述的正常流程、异常规则、
> 错误码不在此重复，仅补充集成/系统验证视角的增量场景。
> 场景必须关联 spec.md AC 编号，保持追溯链完整。

## 概述

| 属性 | 值 |
|------|-----|
| 关联 AC | AC-1.1 ~ AC-2.3 |
| 验证层级 | L2/L3/L4 |

标签: `smoke` `regression` `api`

## 验证范围

**验证重点**: 用户可感知的行为和公开接口的输入输出，而非内部实现细节。

**非验证重点**: 单元测试覆盖的内容；内部接口实现。

## 环境前置与公共配置

- [公共验证环境初始化步骤]

## 场景

### SC-1: [场景标题]

标签: `compatibility`

* Given [前置条件]
* When [操作]
* Then [可观测结果]
* And [附加校验]

> 场景编号 (SC-N) 需关联 spec.md AC 编号。spec AC 已覆盖的正常/异常流程
> 不重复，此处只补充集成验证角度的增量场景（并发、重放、跨组件交互等）。
> 通过标签区分场景类型：`happy-path` `negative` `compatibility` `performance` `security` 等。
> 数据驱动表为条件性：仅当某 SC-N 含多组边界值参数时，在该场景下嵌一张表（内联或 CSV）；
> 简单场景参数内联于 Given/When/Then。表随场景，关联由位置隐含，不单设 `## 数据驱动` 节。

## 概念定义

* **概念: [可复用步骤组合]**
  * Given ...
  * When ...
  * Then ...

## 变更历史

| 版本 | 日期 | 作者 | 描述 |
|------|------|------|------|
```

对比 #12 原始模板（15 个章节/示例），精简后约 6-7 个核心章节。

---

## 对 odk-validate 的影响

| Level | 变更 |
|-------|------|
| Level A | 不变 — spec-for-validation.md 不在必选文件列表中 |
| Level B | 不变 — 不检查 spec-for-validation.md 章节 |
| Level C | 可选检查：如 `spec-for-validation.md` 存在，检查是否有实质内容（warn 级别，不阻止通过） |
| Level D | 不变 — spec-for-validation.md 不参与归档就绪判定 |

---

## 实施清单

| 优先级 | 改动 | 说明 |
|--------|------|------|
| P0 | 新增 `core/templates/ai/spec-for-validation.md` | 精简后的验证模板（原 `test-spec.md`） |
| P0 | 新增 `core/skills/odk-spec-for-validation/SKILL.md` | 可选技能，读取 spec+design 生成验证规格（原 `odk-test-spec`） |
| P1 | 运行 `scripts/distribute-skills.sh` | 生成三平台 odk-spec-for-validation 技能文件 |
| P1 | 更新三平台 README "可用命令" 表 | 新增 `odk-spec-for-validation` 行，标注"可选" |
| P2 | 更新 `odk-validate` Level C | spec-for-validation.md 存在性为 warn 级别检查 |

### 不改动的

- 主流程工作流图不加入 odk-spec-for-validation
- `using-odk` 不引用验证模板
- spec.md 模板不做任何修改（无需晋升内容）
- Level A/B/D 校验不做任何修改
