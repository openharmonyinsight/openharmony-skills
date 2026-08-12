## Phase 5: Generate Test Cases

---

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{skill_root}/modules/L2_Generation/generator/test_generator.md` | 测试代码生成方法论（生成流程、用例结构、断言模式） | 生成策略不确定、用例结构模板需要参考时 |
| `{skill_root}/modules/L2_Generation/generator/templates.md` | 代码模板库（PARAM/ERROR/RETURN/BOUNDARY 各类型模板） | 需要具体代码模板作为生成参考时 |
| `{skill_root}/modules/L2_Generation/generator/quality_constraints.md` | 质量约束规则（命名、断言、导入规范） | 不确定编码规范、需要校验生成代码质量时 |

---

### ⚙️ 按需加载（根据任务需要）

以下模块仅在你执行对应任务时才需要加载：

| 任务 | 加载文件 | 说明 |
|------|---------|------|
| 生成参数/返回值/边界值测试 | `{skill_root}/modules/L2_Generation/generator/param_test.md` | 参数测试详细规则 |
| 生成错误码测试 | `{skill_root}/modules/L2_Generation/generator/error_test.md` | 错误码提取和测试规则 |
| 需要状态机/生命周期等特有场景 | `{skill_root}/modules/L2_Generation/design/HarmonyOS_Test_Design_Spec.md` | HarmonyOS 特有测试知识 |
| ArkTS-Sta 静态项目 | `{skill_root}/modules/L2_Generation/generator/arkts_static_constraints.md` | 静态语法约束 |
| 需要 ArkTS 语法参考 | `{skill_root}/references/ArkTS_Dynamic_Syntax_Rules.md` | 语法规范 |
| 需要命名参考 | `{skill_root}/references/conventions/test_conventions.md` | 命名规范 |
| **子系统测试** | `{skill_root}/references/subsystems/{Subsystem}/_common.md` | 子系统分类模型+约束+子文件索引。加载后按其内部分类决策树和文件索引表加载对应子文件 |

> **注意**：
> 1. 静态项目（ArkTS-Sta）时，使用 `arkts_static_constraints.md` 约束摘要，**不要在生成阶段调用完整的** `ohos-dev-arkts-static-specification-reference` 技能（token 开销大）。
> 2. 子系统测试时，**必须先加载** `{Subsystem}/_common.md`，按其内部分类决策树和文件索引表加载对应子文件。

---

---

**加载模块**:
- `{skill_root}/modules/L2_Generation/generator/test_generator.md`
- `{skill_root}/modules/L2_Generation/generator/templates.md`
- `{skill_root}/modules/L2_Generation/generator/quality_constraints.md`
- `{skill_root}/modules/L2_Generation/generator/param_test.md`（生成参数/返回值/边界值测试时按需加载）
- `{skill_root}/modules/L2_Generation/generator/error_test.md`（生成错误码测试时按需加载）
- `{skill_root}/modules/L2_Generation/design/HarmonyOS_Test_Design_Spec.md`（需要状态机/生命周期/兼容性/安全性等特有场景知识时按需加载）
- `ohos-dev-arkts-static-specification-reference` 技能（仅静态项目 ArkTS-Sta 时加载，使用以下约束摘要替代全量加载）
- `{skill_root}/modules/L2_Generation/generator/arkts_static_constraints.md`（仅静态项目 ArkTS-Sta 时加载）

**关键变更**：此阶段仅生成测试用例代码，严格依据测试设计文档执行。设计驱动生成确保测试用例的完整性和一致性。

> **Flow E 特殊处理**：当用户提供测试设计文档时（Flow E），跳过 Phase 4，此阶段直接读取**用户提供的测试设计文档** + Phase 3 API 解析结果（方法签名、参数类型、错误码、枚举等）生成代码。用户设计文档中的用例列表、测试类型、控件 ID 契约等直接作为生成依据，Phase 3 的 API 签名信息用于补充设计文档中可能省略的细节（如具体参数类型、错误码值、枚举成员）。

### 生成范围

| 条件 | 生成范围 | 说明 |
|------|---------|------|
| Flow A（用户提供了覆盖率报告） | 仅生成报告中的未覆盖项 | 精准：严格按照报告列出的未覆盖项生成 |
| Flow B（无覆盖率报告） | 依据设计文档生成所有目标 API 的测试 | 基于 Phase 4 设计文档生成 |
| **批量模式** | 仅生成当前批次的 ≤10 个 API 的测试 | 由 `batch_manager.py start <batch_id>` 指定范围 |

**批量模式检测**：检查 `batch_workspace/batch_plan.json` 是否存在。如果存在且当前有 `start` 的批次，则仅生成该批次的测试用例。批次完成后执行 `python {skill_root}/scripts/batch_manager.py complete <batch_id>`。

### 生成流程

> **⚠️ 生成前必读**：以下 8 条类型规范约束来源于实际编译错误（问题 6），违反将导致编译失败。在生成**每一行代码**时必须逐条对照检查。**Subagent 禁止"优化"模板中的任何类型注解、Level 值或 import 路径**（问题 10）。

| # | 约束 | 禁止 | 正确 | 错误码 |
|---|------|------|------|--------|
| T1 | 禁止 `Function` 类型 | `done: Function` | `done: () => void` | 10605008 |
| T2 | 禁止 `any` 类型 | `let x: any` | 使用具体类型 | 10605008 |
| T3 | 禁止 `unknown` 类型 | `let x: unknown` | 使用具体类型 | 10605008 |
| T4 | 禁止隐式 any | `let pages = router.getState()` | `let pages: router.RouterState = router.getState()` | 10605008 |
| T5 | router 模块路径 | `@ohos/router` (斜杠) | `@ohos.router` (点号) | 10505001 |
| T6 | JSON.parse 类型 | `Record<string, Object>` | `ESObject`（与现有代码风格一致） | — |
| T7 | Level 枚举值 | `Level.Level0` | `Level.LEVEL0` ~ `Level.LEVEL4` | — |
| T8 | Promise resolve 类型 | `resolve: Function` | `resolve: (value: void \| PromiseLike<void>) => void` | 10605008 |

1. **读取 Phase 4 设计文档**：
   - 解析每个测试用例的设计字段
   - 确认用例编号、预置条件、测试步骤、预期结果
   - 了解场景、类型、级别、依赖关系

2. **应用语法规范**：
   - 从 Phase 2 获取代码风格（导入顺序、describe/it 结构、断言方法、错误处理模式）
   - 加载 `{skill_root}/references/conventions/arkts_standards.md`（语法参考）
   - 加载 `{skill_root}/references/conventions/test_conventions.md`（命名参考）
   - **动态项目（ArkTS-Dyn）**：从 Phase 3 每个 API 知识库条目的 `arkts_constraints` 数组读取预检测的语法约束，生成代码时逐条遵守。这些约束来源于 `{skill_root}/references/arkts_api_pattern_rules.md` 的特征模式匹配，覆盖 Promise、泛型、回调、集合、对象等 10 类常见场景
   - **静态项目（ArkTS-Sta）**：加载 `{skill_root}/modules/L2_Generation/generator/arkts_static_constraints.md`，严格遵循 ArkTS 静态语法约束（禁止 any/unknown、字段初始化、不生成 ERROR_401 类型测试等）。不要在生成阶段调用完整的 `ohos-dev-arkts-static-specification-reference` 技能（token 开销大），仅在 Phase 7 验证阶段调用

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
| PARAM | PARAM_0100, 002... | 测试不同参数值（正常值、空值、undefined、边界值） |
| ERROR | ERROR_0100, 002... | 预期捕获特定错误码，使用 assertEqual 验证 |
| RETURN | RETURN_0100, 002... | 验证返回值类型和格式 |
| BOUNDARY | BOUNDARY_0100, 002... | 测试边界值条件 |
| EVENT | EVENT_0100, 002... | 监听和验证事件（ArkUI） |

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
- **801 全局防护**：如果 API 的 `@throws` 声明了 801，该 API 的所有用例（含 PARAM/RETURN/BOUNDARY）必须包裹 801 防护（try 正常逻辑，catch 中 801→正常通过，其他→assertFail），详见 `error_test.md` 第七章

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
 * @tc.number SUB_MODULE_METHOD_PARAM_0100
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
it('normalValueParamTest001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  // 测试代码
});
```

### 关键约束

1. **严格遵循设计文档**：不能偏离或跳过设计文档中的任何内容（设计文档是测试可追溯性的唯一蓝图，偏离会导致 Phase 7 设计一致性检查失败，且评审人员无法将代码映射回需求）
   - 用例编号必须完全一致（不多不少一位）
   - 预期结果不能被改写
   - 不能跳过某些设计用例不生成代码
   - 测试步骤顺序不能打乱
   - **组件id 必须与设计文档中预定义的一致，三方（设计文档、Demo页面、测试代码）必须完全一致**
2. **必须包含 @tc 注解**：每个测试用例必须包含完整的 @tc 注解块
3. **语法规范**：符合 ArkTS 静态检查要求
4. **框架规范**：符合 Hypium 测试框架要求
5. **子系统规则**：遵循 Phase 1 配置中的子系统特有规则
6. **代码质量约束**：生成的代码必须满足 `quality_constraints.md` 中的全部规则（R002-R029 + R201-R205），确保天然通过 ohos-test-xts-code-quality 扫描
7. **语法类型统一**：整个文件必须统一使用目标语法类型的规范（动态或静态），禁止混合使用
8. **已废弃接口处理**：不为 .d.ts 中标记 @deprecated 的接口生成用例（除非用户明确要求）；新生成的测试代码中禁止调用已废弃接口，参考历史代码发现废弃接口时使用已知新接口替代（不修改历史代码）
9. **测试价值分级**：按 API 特征决定测试深度
   - **P0 必测**：有可观察行为的 API（返回值、状态变更、事件触发）、生命周期/资源管理 API（create/destroy/open/close）→ 完整覆盖 PARAM + RETURN + ERROR + BOUNDARY + 资源泄漏检查
   - **P1 重点**：权限/安全相关 API、异步/回调 API → 错误码 + 权限缺失 + 超时 + 取消 + 并发
   - **P2 基础**：简单属性读写 API → 正常值 + 边界值（不扩展参数组合）
   - **跳过**：纯类型定义、interface、type alias
10. **停止扩展信号** — 以下情况停止增加用例：
    - 参数组合产生的用例不增加**行为覆盖**（只是换了个合法值）
    - ERROR 用例的错误码在 .d.ts @throws 中未声明
    - BOUNDARY 用例的边界值无文档依据

### 代码生成模板（动态项目标准骨架）

```typescript
import { afterEach, beforeEach, describe, expect, it, Level } from "@ohos/hypium";
import router from '@ohos.router';  // 注意：点号，不是斜杠！

function sleep(time: number) {
  return new Promise<void>((resolve: (value: void | PromiseLike<void>) => void) => {
    setTimeout(() => { resolve(); }, time * 1000);
  }).then(() => { console.info(`sleep ${time} over...`); })
}

export default function XxxTest() {
  describe('XxxTest', () => {
    beforeEach(async (done: () => void) => {
      let options: router.RouterOptions = {
        url: 'MainAbility/pages/xxx',
      }
      try {
        router.clear();
        let pages: router.RouterState = router.getState();
        if (!("XxxPage" == pages.name)) {
          await router.pushUrl(options);
        }
      } catch (err) {
        console.error("push page error " + JSON.stringify(err));
      }
      await sleep(2);
      done();
    });

    afterEach(async (done: () => void) => {
      await sleep(1);
      done();
    });

    /**
      * @tc.name   xxxTest010
      * @tc.number SUB_ARKUI_XXX_PARAM_0010
      * @tc.desc   Test ...
      * @tc.type   FUNCTION
      * @tc.size   MEDIUMTEST
      * @tc.level  LEVEL1
      */
    it('xxxTest010', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done: () => void) => {
      let strJson: string = getInspectorByKey('component_id');
      let obj: ESObject = JSON.parse(strJson);
      expect(obj.$attrs.property).assertEqual('expected_value');
      done();
    });
  });
}
```

### 代码生成模板（静态项目 ArkTS-Sta 标准骨架）

> 第二轮生成时使用此模板包裹迁移后的测试代码。`[sta-only]` 用例也使用此模板。

```typescript
import { afterEach, beforeEach, describe, expect, it, Level } from "../../../hypium/index";
// 路径规则：hypium 固定位于 entry/src/hypium/index
// 测试文件位于 entry/src/main/src/test/ 下，深度决定 ../ 数量：
//   test/Xx.test.ets        → "../../../hypium/index"（3 层）
//   test/ui/Xx.test.ets     → "../../../../hypium/index"（4 层）
//   test/ui/sub/Xx.test.ets → "../../../../../hypium/index"（5 层）
import router from '@ohos.router';

function sleep(time: number): Promise<void> {
  return new Promise<void>((resolve: (value: void | PromiseLike<void>) => void) => {
    setTimeout(() => { resolve(); }, time * 1000);
  }).then(() => { console.info(`sleep ${time} over...`); })
}

export default function XxxTest(): void {
  describe('XxxTest', () => {
    beforeEach(async (done: () => void): Promise<void> => {
      const options: router.RouterOptions = {
        url: 'MainAbility/pages/xxx',
      }
      try {
        router.clear();
        const pages: router.RouterState = router.getState();
        if (!("XxxPage" == pages.name)) {
          await router.pushUrl(options);
        }
      } catch (err) {
        console.error("push page error " + JSON.stringify(err));
      }
      await sleep(2);
      done();
    });

    afterEach(async (done: () => void): Promise<void> => {
      await sleep(1);
      done();
    });

    /**
      * @tc.number SUB_ARKUI_XXX_PARAM_0010
      * @tc.name ...
      * @tc.desc ...
      * @tc.type FUNCTION
      * @tc.size MEDIUMTEST
      * @tc.level LEVEL1
      */
    it('xxxTest010', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done: () => void): Promise<void> => {
      const strJson: string = getInspectorByKey('component_id');
      const obj: ESObject = JSON.parse(strJson);
      expect(obj.$attrs.property).assertEqual('expected_value');
      done();
    });
  });
}
```

**静态与动态模板关键差异**：

| 差异项 | 动态（ets1.1） | 静态（ets1.2） |
|-------|---------------|---------------|
| hypium 导入 | `from "@ohos/hypium"` | `from "{相对路径}/hypium/index"`，hypium 固定位于 `entry/src/hypium/index`，按测试文件深度计算 `../` 数量 |
| `export default function` 返回类型 | 省略 | `: void` |
| `beforeEach`/`afterEach` 返回类型 | `async (done: () => void) =>` | `async (done: () => void): Promise<void> =>` |
| `it` 回调返回类型 | `async () =>`（旧写法 `async function()` 不推荐） | `async (done: () => void): Promise<void> =>` |
| `let` vs `const` | `let pages` | `const pages`（所有非重新赋值的变量使用 const） |
| 错误码 401 测试 | 生成 | 不生成（编译时已检查） |

> **⚠️ 警告**：生成代码时必须严格使用上述模板中的类型注解。禁止 subagent 自行"优化"为其他类型（如 `Record<string, Object>`, `Level.Level0`, `Function` 等）。这些"优化"会导致 ArkTS 编译器报错。

### 统计集成（Phase 完成后执行）

```bash
# 保存原始快照（用于后续按行采纳率计算）
mkdir -p {output_dir}/snapshots/phase5
cp {生成的所有.test.ets文件} {output_dir}/snapshots/phase5/

# 记录生成情况
python {skill_root}/scripts/adoption_stats.py --action record_phase5 \
  --design-doc {design_doc_path} \
  --generated-files {生成的所有.test.ets文件路径} \
  --output-dir {output_dir}
```
