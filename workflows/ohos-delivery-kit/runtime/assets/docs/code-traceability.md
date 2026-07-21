# Code Traceability

## 目标

本文件定义 `ohos-delivery-kit` 的代码映射可追溯机制。核心问题是：

**如何确保 spec 中的每条 AC、plan 中的每个 Task、最终代码变更和验证证据之间能互相对齐，形成完整的追溯链。**

这不是「写完代码后的总结」，而是**从 spec 阶段就建立的结构化映射骨架，随流程推进逐步填充**。

---

## 追溯链模型

```
proposal AC ──→ spec AC ──→ execution-plan Task ──→ code_refs ──→ commit
                     │              │                    │            │
                     │              │                    │            │
                     ▼              ▼                    ▼            ▼
               spec.md        execution-plan.md     git log
               AC + 验证映射   AC-Task 追溯 + 代码范围映射  commits
                     │              │                    │
                     └──────────────┴────────────────────┘
                                          │
                                          ▼
                                    evidence/reviews/ (optional)
                                    可选验证证据
                                    (AC 覆盖率、代码一致性)
```

### 每阶段的追溯产物

| 阶段 | 产出 | 追溯内容 |
|------|------|---------|
| Define | `proposal.md` | 初始 AC 列表（AC-001, AC-002...） |
| Specify | `spec.md` §验证映射 | AC → 验证方式 |
| Plan | `execution-plan.md` §AC-Task 追溯 | AC → Task → 目标文件 |
| Implement | `execution-plan.md` §代码范围映射 | Task → 实际改动文件和代码 |
| Review | `evidence/reviews/spec-compliance.md` (optional) | 代码是否符合 spec AC（逐项） |
| Review | `evidence/reviews/code-review.md` (optional) | 代码质量 + 是否超出 spec 范围 |

### 追溯链完整性判据

```
追溯链完整 ≡
  spec 中的每条 AC 都能找到对应的 Task
  ∧ 每个 Task 都能找到对应的文件变更
  ∧ 如存在 evidence/reviews/，其中有每 AC 的验证证据
```

---

## 代码映射（已迁至 execution-plan.md）

> **#90 方案 D 变更**：代码映射（AC → 文件 + Task + 验证状态）已从 `spec.md` 迁至 `execution-plan.md`——「AC 到 Task 追溯」（AC → Task + 验证状态 Pass/Fail/Blocked）+「代码范围映射」（Task → 实际文件）。下方 spec.md 旧格式仅作历史参考，不再使用；当前机制见下节 [execution-plan.md: Task-to-File 映射](#execution-planmd-task-to-file-映射)。

### 旧格式（spec.md §代码映射，已废弃）

```markdown
## 代码映射

| AC 编号 | 验收标准摘要 | 预期实现模块/文件 | 实际实现文件 | 关联 Task | 验证证据 |
|---------|-------------|------------------|-------------|-----------|---------|
| AC-001 | 组件获得焦点时触发 onFocus 回调 | frameworks/arkui/component/xyz/ | xyz_focus.cpp:42-128 | TASK-001 | evidence/reviews/spec-compliance-*.md#ac-001 |
| AC-002 | 焦点移出时触发 onBlur 回调 | frameworks/arkui/component/xyz/ | xyz_focus.cpp:130-180 | TASK-002 | evidence/reviews/spec-compliance-*.md#ac-002 |
| AC-003 | 编程式 focus() 请求正确切换焦点 | frameworks/arkui/component/xyz/ | xyz_focus.cpp:182-250 | TASK-001 | evidence/reviews/spec-compliance-*.md#ac-003 |
```

### 映射表生命周期

| 阶段 | 列状态 |
|------|--------|
| Specify (spec.md 生成时) | AC 编号 + 摘要 + 预期实现模块（预填），其余空 |
| Plan (execution-plan 生成时) | 关联 Task 列填入 |
| Implement (代码完成后) | 实际实现文件列填入 |
| Review (review 完成后) | 验证证据列填入 |

### 规则

1. **AC 编号不可变**: 一旦在 proposal/spec 阶段确定，后续阶段只追加引用，不重编号
2. **预期 vs 实际**: 「预期实现模块」是 plan 阶段的估计，「实际实现文件」是 implement 后的事实——两者可以不同，但差异必须在 review 中解释
3. **映射表不允许有空行**: 归档前（Level D），每条 AC 的「实际实现文件」和「验证证据」必须有值
4. **AC 生命周期管理**:
   - 新增: 新编号（如 AC-004），不插入已有编号之间
   - 废弃: 标记 `deprecated`，保留在映射表中（标注废弃原因和日期），**不回收编号**
   - 拆分: 原编号标记 `superseded-by: AC-004, AC-005`，保留在映射表中；新增子 AC
   - 合并: 原编号标记 `superseded-by: AC-006`，新增合并 AC
   - 禁止: 重编号、回收已废弃编号、修改 AC 含义但不改编号

---

## execution-plan.md: Task-to-File 映射

### 强制格式

```markdown
## AC 到 Task 追溯

| AC | 来源 | Task | 验证方式 | 是否覆盖 |
|----|------|------|---------|---------|
| AC-001 | spec.md §用户故事 US-01 | TASK-001 | 单元测试: XYZFocusTest.verifyOnFocus | ✓ |
| AC-002 | spec.md §用户故事 US-01 | TASK-002 | 单元测试: XYZFocusTest.verifyOnBlur | ✓ |
| AC-003 | spec.md §用户故事 US-02 | TASK-001 | 集成测试: XYZFocusIntegrationTest | ✓ |

## Task 列表

### TASK-001: 实现焦点获取与切换逻辑

- **关联 AC**: AC-001, AC-003
- **代码范围**:
  - 新增: `frameworks/arkui/component/xyz/xyz_focus.cpp`
  - 修改: `frameworks/arkui/component/xyz/BUILD.gn`
  - 测试: `test/arkui/component/xyz/xyz_focus_test.cpp`
- **完成判据**: 所有关联 AC 的单元测试通过
- **验证命令**: `./build.sh --target xyz_focus_test && ./out/xyz_focus_test`
```

### 规则

1. **AC-Task 追溯表是必须项**: 每个 execution-plan 必须包含此表
2. **每个 Task 必须声明代码范围**: 文件路径级别，不能只是模块名
3. **「是否覆盖」列**: 确保没有遗漏的 AC
4. **Task 依赖与验证**: 允许声明 Task 间依赖（`depends_on: TASK-001`），但每个 Task 必须有**独立可验证的完成判据**

---

## evidence/reviews/: 可选验证证据要求

### 最小评审产物

```
.codespec/changes/<id>/evidence/reviews/
├── spec-compliance-YYYYMMDD.md    # spec 符合性审查
├── code-review-YYYYMMDD.md        # 代码质量审查
└── verification-YYYYMMDD.md       # 最终验证记录
```

### spec-compliance.md 强制内容

```markdown
## 需求覆盖

| AC | 是否实现 | 证据 | 结论 |
|----|---------|------|------|
| AC-001 | 是 | xyz_focus.cpp:42-128, 单测通过 | 符合 |
| AC-002 | 是 | xyz_focus.cpp:130-180, 单测通过 | 符合 |
| AC-003 | 是 | xyz_focus.cpp:182-250, 集成测试通过 | 符合 |

## 额外实现

| 文件 | 描述 | 是否在 spec 范围内 |
|------|------|-------------------|
| xyz_focus_logger.cpp | 调试日志辅助类 | 否（实现便利性添加，已确认不破坏兼容性） |

## 理解偏差

| spec 原文 | 实现理解 | 是否一致 |
|-----------|---------|---------|
| ... | ... | 一致 / 偏差（已修复 / 已更新 spec） |

## 结论
- [ ] 实现完全符合 spec，无多无少无误解
- [ ] 存在偏差但已修复/已更新 spec（见上表）
- [ ] 存在未解决偏差，阻塞合并
```

### code-review.md 强制检查项

除常规代码质量检查外，必须包含：
1. **代码范围检查**: 实际改动文件是否在 execution-plan Task 的代码范围内
2. **Scope 外代码**: 是否存在 plan/spec 未声明的额外改动
3. **代码结构一致性**: 实现结构是否与 design.md 的模块划分一致

### verification.md 强制内容

```markdown
## 验证执行记录

| 验证项 | 命令 | 结果 | 证据 |
|--------|------|------|------|
| 单元测试 | `./out/xyz_focus_test` | 通过 (12/12) | 输出见附件 |
| AC-001 行为验证 | 手动验证 / 自动化脚本 | 通过 | 截图/日志 |
| ... | ... | ... | ... |

## 代码与 spec 一致性结论
[必须显式声明: 一致 / 不一致（附说明）]
```

---

## 各插件代码映射回填方案

### OpenSpec

OpenSpec 的 tasks.md 是 checkbox 列表，无 AC 体系。回填路径：

1. **spec 阶段**: kit 的 ohos-spec-driven schema 强制每条 Requirement 有编号，Scenario 有 AC 编号
2. **plan 阶段**: tasks.md 模板预置 AC-Task 追溯表，每个 Task 标注关联 AC
3. **implement 阶段**: 在 kit 的 `execution-plan.md`「代码范围映射」中回填「实际文件」
4. **review 阶段**: 如需要保留过程证据，按 kit 的 `evidence/reviews/` 格式输出
5. **归档前**: validator 检查 AC → Task → code 链完整

### Superpowers

Superpowers 的 plan 已有精确文件列表，优势在 Task-to-file 映射，但缺 AC 体系。

1. **spec 阶段**: kit wrapper 在转写 brainstorming 输出时创建 AC 编号
2. **plan 阶段**: writing-plans 的 Task 文件列表直接作为代码范围；补充 AC 关联列
3. **implement 阶段**: TDD 测试用例即验证证据，可按需记录到 `evidence/reviews/`
4. **review 阶段**: code review 报告（会话内瞬时内容）→ wrapper 可按需持久化到 `evidence/reviews/`

**Superpowers 特殊处理**: 由于 review 是 wrapper 事后回填的，validator 只在 `evidence/reviews/` 存在时检查其内容是否有实质证据。

### MatrixSpec

MatrixSpec 有 validation.md（交叉覆盖检查），这是一个天然优势。

1. **delta-spec 阶段**: 每条 ADDED/MODIFIED 规则有编号，作为代码映射键
2. **tasks 阶段**: 补充文件级代码范围（MatrixSpec 原生 tasks 分层结构只到模块级）
3. **implement 阶段**: 在 execution-plan「代码范围映射」中回填实际文件
4. **validation 阶段**: 原生 validation.md 增加「代码一致性」检查维度

---

## validator 追溯完整性校验

### Phase 1 (MVP): 基本存在性

```
check: .codespec/changes/<id>/execution-plan.md 包含「AC 到 Task 追溯」+「代码范围映射」
check: 如存在 .codespec/changes/<id>/evidence/reviews/，目录非空（至少 1 个文件）
```

### Phase 2: 交叉一致性

```
check: execution-plan.md「AC 到 Task 追溯」的每条 AC 有 Task 和验证方式
check: execution-plan.md「代码范围映射」的每个被追溯 Task 有非空文件
check: 如存在 evidence/reviews/spec-compliance.md，覆盖了所有 AC（逐条有结论）
```

### Phase 3: 完整性

```
check: execution-plan.md「AC 到 Task 追溯」无空行（所有 AC 有 Task + 验证状态），「代码范围映射」每个 Task 有非空文件
check: 没有「AC 覆盖但无 Task」「Task 存在但无代码变更」的孤立项
check: 如存在 evidence/reviews/，其中有「代码与 spec 一致性结论」且为「一致」
```

### 校验通过标准

| 阶段 | 追溯通过标准 |
|------|-------------|
| Level B (Draft) | execution-plan.md 有「AC 到 Task 追溯」+「代码范围映射」表头（可部分空） |
| Level C (Review) | AC-Task 追溯表无空行；如存在 evidence/reviews/，内容需非空 |
| Level D (Archive) | 所有映射表无空行，交叉一致性通过；如存在 evidence/reviews/，需有明确一致性结论 |

---

## Git 集成

### Commit Message 规范

每个 commit message 必须包含关联的 issue 编号，确保 AC → Task → code → commit 追溯链可反查：

```
feat(arkui): add XYZ focus management (#12345)

Implements AC-001, AC-002, AC-003.

Task: TASK-001, TASK-002
```

---

## 追溯链完整性总览

```
                proposal.md              spec.md
                ┌──────────┐            ┌──────────────────────┐
                │ AC-001   │───────────→│ AC-001               │
                │ AC-002   │           │   预期: xyz_focus.cpp │
                │ AC-003   │           │   实际: xyz_focus.cpp │
                └──────────┘           │   Task: TASK-001      │
                                       │   证据: evidence/...  │
                                       └──────┬───────────────┘
                                              │
                execution-plan.md              │
                ┌──────────────────────┐       │
                │ AC-001 → TASK-001    │◄──────┘
                │   代码: xyz_focus.cpp│
                │   验证: unit test    │
                └──────┬───────────────┘
                       │
                       │
                evidence/reviews/
                ┌──────────────────────┐
                │ spec-compliance.md   │
                │  AC-001: 符合 ✓      │
                │  AC-002: 符合 ✓      │
                │  AC-003: 符合 ✓      │
                │ code-review.md       │
                │ verification.md      │
                └──────────────────────┘
```

如果这个图中的任何一根线断裂（AC 无 Task、Task 无文件、commit 无 review），追溯链就不完整，归档条件就不满足。
