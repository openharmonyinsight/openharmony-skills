## Phase 5: Generate Test Cases

---

### 📦 MANDATORY - 必须先加载以下模块

**在执行本 Phase 前，你必须完整阅读以下文件**（不得设置行数限制）：

```
{skill_root}/modules/L2_Generation/generator/test_generator.md
{skill_root}/modules/L2_Generation/generator/templates.md
{skill_root}/modules/L2_Generation/generator/quality_constraints.md
```

---

### ⚙️ 按需加载（根据任务需要）

以下模块仅在你执行对应任务时才需要加载：

| 任务 | 加载文件 | 说明 |
|------|---------|------|
| 生成参数/返回值/边界值测试 | `{skill_root}/modules/L2_Generation/generator/param_test.md` | 参数测试详细规则 |
| 生成错误码测试 | `{skill_root}/modules/L2_Generation/generator/error_test.md` | 错误码提取和测试规则 |
| 需要状态机/生命周期等特有场景 | `{skill_root}/modules/L2_Generation/generator/HarmonyOS_Test_Design_Spec.md` | HarmonyOS 特有测试知识 |
| ArkTS-Sta 静态项目 | `{skill_root}/modules/L2_Generation/generator/arkts_static_constraints.md` | 静态语法约束 |
| 需要 ArkTS 语法参考 | `{skill_root}/references/conventions/arkts_standards.md` | 语法规范 |
| 需要命名参考 | `{skill_root}/references/conventions/test_conventions.md` | 命名规范 |

> **注意**：静态项目（ArkTS-Sta）时，使用 `arkts_static_constraints.md` 约束摘要，**不要在生成阶段调用完整的** `arkts-static-spec` 技能（token 开销大）。

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有 L1_Analysis 模块（modules/L1_Analysis/）
所有 L3_Validation 模块（modules/L3_Validation/）
```

---

**加载模块**:
- `modules/L2_Generation/generator/test_generator.md`
- `modules/L2_Generation/generator/templates.md`
- `modules/L2_Generation/generator/quality_constraints.md`
- `modules/L2_Generation/generator/param_test.md`（生成参数/返回值/边界值测试时按需加载）
- `modules/L2_Generation/generator/error_test.md`（生成错误码测试时按需加载）
- `modules/L2_Generation/generator/HarmonyOS_Test_Design_Spec.md`（需要状态机/生命周期/兼容性/安全性等特有场景知识时按需加载）
- `arkts-static-spec` 技能（仅静态项目 ArkTS-Sta 时加载，使用以下约束摘要替代全量加载）
- `modules/L2_Generation/generator/arkts_static_constraints.md`（仅静态项目 ArkTS-Sta 时加载）

**关键变更**：此阶段仅生成测试用例代码，严格依据 Phase 4 生成的测试设计文档执行。设计驱动生成确保测试用例的完整性和一致性。

### 生成范围

| 条件 | 生成范围 | 说明 |
|------|---------|------|
| Flow A（用户提供了覆盖率报告） | 仅生成报告中的未覆盖项 | 精准：严格按照报告列出的未覆盖项生成 |
| Flow B（无覆盖率报告） | 依据设计文档生成所有目标 API 的测试 | 基于 Phase 4 设计文档生成 |
| **批量模式** | 仅生成当前批次的 ≤10 个 API 的测试 | 由 `batch_manager.py start <batch_id>` 指定范围 |

**批量模式检测**：检查 `batch_workspace/batch_plan.json` 是否存在。如果存在且当前有 `start` 的批次，则仅生成该批次的测试用例。批次完成后执行 `python {skill_root}/scripts/batch_manager.py complete <batch_id>`。

### 生成流程

1. **读取 Phase 4 设计文档**：
   - 解析每个测试用例的设计字段
   - 确认用例编号、预置条件、测试步骤、预期结果
   - 了解场景、类型、级别、依赖关系

2. **应用语法规范**：
   - 从 Phase 2 获取代码风格（导入顺序、describe/it 结构、断言方法、错误处理模式）
   - 加载 `references/conventions/arkts_standards.md`（语法参考）
   - 加载 `references/conventions/test_conventions.md`（命名参考）
   - **静态项目（ArkTS-Sta）**：加载 `modules/L2_Generation/generator/arkts_static_constraints.md`，严格遵循 ArkTS 静态语法约束（禁止 any/unknown、字段初始化、不生成 ERROR_401 类型测试等）。不要在生成阶段调用完整的 `arkts-static-spec` 技能（token 开销大），仅在 Phase 7 验证阶段调用

3. **应用子系统特有规则**（从 Phase 1 配置中获取）：
   - 使用子系统特有模板（如有）
   - 遵循特殊断言规则
   - 应用特殊错误处理模式

4. **依据设计文档生成测试用例**：
   - 按用例编号顺序生成
   - 严格遵循设计文档中的预置条件
   - 实现设计文档中的测试步骤
   - 实现设计文档中的预期结果（断言）
   - 标注场景、类型、级别、依赖关系

5. **生成测试文件**：
   - 文件命名: `{测试文件名}.test.ets`
   - 每个文件包含一个 describe 块
   - 每个 describe 块对应一个接口/方法
   - 每个 it 块对应一个测试用例

### 测试用例类型

| 类型 | 编号后缀 | 代码特征 |
|------|----------|----------|
| PARAM | PARAM_001, 002... | 测试不同参数值（正常值、空值、undefined、边界值） |
| ERROR | ERROR_001, 002... | 预期捕获特定错误码，使用 assertEqual 验证 |
| RETURN | RETURN_001, 002... | 验证返回值类型和格式 |
| BOUNDARY | BOUNDARY_001, 002... | 测试边界值条件 |
| EVENT | EVENT_001, 002... | 监听和验证事件（ArkUI） |

### 参数测试代码生成规则

根据设计文档中的参数场景生成代码：

| 参数类型 | 测试场景 | 代码示例 |
|----------|----------|----------|
| string | 正常值 | `await methodA("normalString")` |
| string | 空字符串 | `await methodA("")` |
| string | undefined | `await methodA(undefined)` |
| string | null | `await methodA(null)` |
| string | 超长字符串 | `await methodA("a".repeat(10000))` |

### 错误码测试代码生成规则

根据设计文档中的错误码生成代码：

```typescript
// 设计文档指定捕获错误码 401
try {
  await methodA(invalidParam);
} catch (error) {
  expect(error.code).assertEqual(401);
}
```

**重要规则**：
- 必须从 `.d.ts` 的 `@throws` 注解提取错误码
- 使用 `assertEqual` 精确匹配错误码
- 禁止使用范围断言或"或"表达式
- 遵循子系统配置中的特殊规则（如 testfwk 空字符串规则）

### 代码风格应用

从 Phase 2 获取的代码风格包括：

| 风格要素 | 说明 |
|---------|------|
| 导入顺序 | 先导入框架，再导入 Kit，最后导入工具函数 |
| describe/it 结构 | 使用标准嵌套结构 |
| 断言方法 | 使用 expect() 链式调用 |
| 错误处理 | 使用 try-catch 捕获异常 |
| 注释风格 | 简洁注释说明测试意图 |

### 输出

1. **测试用例代码文件**：`{测试文件名}.test.ets`
   - 完整的 ArkTS 测试代码
   - 符合 Hypium 框架规范
   - 包含标准 `@tc` 注解块
   - 每个测试用例对应设计文档中的一个条目

2. **@tc 注解块格式**：

```typescript
/**
 * @tc.number SUB_MODULE_METHOD_PARAM_001
 * @tc.name 正常值参数测试
 * @tc.desc 验证 methodA 在传入正常参数时是否正常工作.
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 3
 * @tc.require
 * @tc.precondition 已初始化测试环境，已导入 @kit.XXXKit
 * @tc.step 1. 调用 methodA(param1="test", param2=100)\n2. 等待 Promise 返回\n3. 验证无异常
 * @tc.expected 返回 void，无异常抛出
 */
it('normalValueParamTest001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async function () {
  // 测试代码
});
```

### 关键约束

1. **严格遵循设计文档**：不能偏离或跳过设计文档中的任何内容（设计文档是测试可追溯性的唯一蓝图，偏离会导致 Phase 7 设计一致性检查失败，且评审人员无法将代码映射回需求）
   - 用例编号必须完全一致（不多不少一位）
   - 预期结果不能被改写
   - 不能跳过某些设计用例不生成代码
   - 测试步骤顺序不能打乱
2. **必须包含 @tc 注解**：每个测试用例必须包含完整的 @tc 注解块
3. **语法规范**：符合 ArkTS 静态检查要求
4. **框架规范**：符合 Hypium 测试框架要求
5. **子系统规则**：遵循 Phase 1 配置中的子系统特有规则
6. **代码质量约束**：生成的代码必须满足 `quality_constraints.md` 中的全部规则（R002-R029），确保天然通过 check-test-code-quality 扫描
7. **语法类型统一**：整个文件必须统一使用目标语法类型的规范（动态或静态），禁止混合使用
