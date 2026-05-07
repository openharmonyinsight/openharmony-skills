# 测试用例生成策略

> **模块信息**
> - 层级：L2_Generation
> - 优先级：必须加载
> - 适用范围：测试用例生成总纲
> - 依赖：conventions, L1_Analysis
> - 子模块：`param_test.md`、`error_test.md`、`HarmonyOS_Test_Design_Spec.md`

---

## 一、模块概述

测试用例生成器根据 **Phase 4 生成的测试设计文档** 和 API 定义，自动生成符合 XTS 规范的测试用例代码。

> **核心原则：设计文档驱动生成**
>
> 测试用例必须严格按照 Phase 4 生成的设计文档（`{TestFile}.design.md`）内容来生成，包括：
> - 用例编号（`@tc.number`）必须与设计文档中的编号一致
> - 测试场景和步骤必须与设计文档中的描述对应
> - 预期结果必须与设计文档中的预期一致
> - 不得生成设计文档中未规划的测试用例
>
> 设计文档是测试用例生成的**唯一蓝图**，确保测试的可追溯性和完整性。

> **API 严格遵循原则**
>
> 所有生成的测试代码只使用 Phase 3 解析的 UnifiedAPIInfo 中列出的：
> - 方法名称和签名（不得编造 .d.ts 中不存在的方法）
> - 参数名称和类型（不得添加 API 声明中不存在的参数）
> - 返回值类型（不得猜测或修改返回值类型）
> - 错误码列表（不得为无 @throws 声明的 API 构造错误码测试）

---

## 二、生成约束（禁止项）

> **禁止以下过度生成行为**：

1. **禁止为 `.d.ts` 中未声明的 API 生成测试**：只使用 Phase 3 解析的 UnifiedAPIInfo 中列出的方法、参数和返回值，不得凭"常识"编造 API。（编造的 API 在编译环境中不存在，生成的代码无法编译）
2. **禁止为没有 `@throws` 声明的 API 强行构造错误码测试**：如果 `.d.ts` 中没有 `@throws` 标记，不要假设会抛出 401 或其他错误码。（API 不会在运行时抛出未声明的错误码，断言的 error.code 分支永远不会执行，测试无意义）
3. **禁止为仅支持动态语法的 API 在静态项目中生成测试**：如果 API 的 `@since` 标签只有 `dynamic` 没有 `static`，且目标项目是 ArkTS-Sta，则跳过该 API。（这些 API 在静态编译环境中不存在，生成后必然编译失败）
4. **禁止在 ArkTS-Sta 项目中生成 ERROR_401 类型测试**：类型错误在静态模式下由编译器拦截，不会运行时抛出 401。（静态编译器直接拒绝类型不匹配的代码，无法生成 HAP，更不可能运行到抛出 401 的逻辑）
5. **禁止为 TypeScript 编译器会拦截的参数类型错误生成测试**：如传 `number` 给 `string` 参数（编译错误而非运行时错误）。（这类代码连编译阶段都无法通过，无法生成可执行的测试）

---

## 三、测试隔离原则

> **每个测试用例必须独立可执行，不依赖其他用例的执行结果或执行顺序。**（Hypium 测试运行器可能并行或乱序执行用例，共享可变状态会导致间歇性失败，无法稳定复现）

```typescript
// ❌ 反模式：在 describe 顶层修改共享状态
describe('TreeSetTest', () => {
  let treeSet = new TreeSet<string>();
  treeSet.add("item1");  // describe 顶层修改状态
  it('testSize001', Level.LEVEL1, () => {
    expect(treeSet.length).assertEqual(1);  // 依赖前置状态
  });
});

// ✅ 正确：每个测试内部独立创建和清理状态
describe('TreeSetTest', () => {
  it('testAdd001', Level.LEVEL1, () => {
    let treeSet = new TreeSet<string>();  // 独立实例
    let result = treeSet.add("item");
    expect(result).assertTrue();
  });
});
```

---

## 四、测试套件组织

```typescript
export default function APINameTest() {
  describe('APINameParameterTest', () => {
    // 参数测试用例
  });

  describe('APINameErrorCodeTest', () => {
    // 错误码测试用例
  });

  describe('APINameReturnValueTest', () => {
    // 返回值测试用例
  });

  describe('APINameBoundaryTest', () => {
    // 边界值测试用例
  });
}
```

### 生成优先级

1. **Level0/Level1**：基本功能和常用输入（优先）
2. **Level2**：错误场景（次优先）
3. **Level3/Level4**：边缘场景（可选）

---

## 五、子模块索引

根据当前生成任务，按需加载对应的子模块：

| 子模块 | 内容 | 加载时机 |
|--------|------|---------|
| `param_test.md` | 参数/返回值/边界值测试规则、模板和示例 | Phase 5 生成参数/返回值/边界值测试时 |
| `error_test.md` | 错误码测试规则、模板、示例和反模式 | Phase 5 生成错误码测试时 |
| `HarmonyOS_Test_Design_Spec.md` | HarmonyOS 特有测试设计知识（状态机、生命周期、兼容性、安全性、UI场景等） | Phase 5 需要特有场景知识时 |

---

## 六、生成输出格式

### 6.1 完整测试文件

```typescript
/*
 * Copyright (c) {YEAR} Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';
import {APIName} from '@kit.BaseKitName';

export default function APINameTest() {
  describe('APINameParameterTest', () => {
    // 参数测试用例...
  });

  describe('APINameErrorCodeTest', () => {
    // 错误码测试用例...
  });

  describe('APINameReturnValueTest', () => {
    // 返回值测试用例...
  });
}
```

### 6.2 测试用例清单

生成测试用例后，应输出清单：

```markdown
# 生成的测试用例清单

## 参数测试 (5 个)
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_001 - 正常值
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_002 - null
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_003 - undefined
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_004 - 边界值
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_005 - 超长字符串

## 错误码测试 (2 个)
- SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_401_001 - 容器为空
- SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_402_001 - 参数无效

## 返回值测试 (3 个)
- SUB_UTILS_UTIL_TREESET_GETFIRST_RETURN_001 - 返回有效值
- SUB_UTILS_UTIL_TREESET_GETFIRST_RETURN_002 - 返回 undefined
- SUB_UTILS_UTIL_TREESET_GETFIRST_RETURN_003 - 返回值类型验证

总计: 10 个测试用例
```
