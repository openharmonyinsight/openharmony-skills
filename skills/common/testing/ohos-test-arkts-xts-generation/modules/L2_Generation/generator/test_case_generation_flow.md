# 测试用例生成流程

> **文档版本**: 1.0.0
> **创建日期**: 2026-03-03
> **模块信息**: L2_Generation
> **适用范围**: 测试用例生成流程

---

## 一、概述

本文档定义了从 API 声明生成测试用例的完整流程，涵盖了从解析 .d.ts 文件到生成测试用例代码的各个步骤。

**与其他模块的配合**：
- 依赖 `L1_Analysis/parser/unified_api_parser.md` 进行 API 解析和错误码提取
- 依赖 `L1_Analysis/analyzer/api_parameter_optional_rules.md` 进行参数分类和规则应用
- 与 `L2_Generation/generator/test_generator.md` 配合，应用测试用例模板

---

## 二、生成流程概览

```
步骤1：解析 .d.ts 文件
   ↓
步骤2：检查方法重载
   ↓
步骤3：确定参数类型
   ↓
步骤4：提取错误码
   ↓
步骤5：应用子系统特殊规则
   ↓
步骤6：生成测试用例
```

---

## 三、详细步骤

### 3.1 步骤1：解析 .d.ts 文件

读取 API 声明文件，提取以下信息：

1. **方法签名和参数列表**
   - 方法名称
   - 参数名称、类型、是否可选
   - 返回值类型

2. **`@throws` 标记中的错误码和触发条件**
   - 错误码列表
   - 每个错误码的触发条件
   - 参数相关的错误码

3. **`@since` 标签判断 API 语法类型（动态/静态）**
    - 解析 @since 标签内容
    - 判断 API 类型：DYNAMIC_ONLY、STATIC_ONLY、HYBRID、DYNAMIC、STATIC

---

### 3.1.5 步骤1.5：过滤 API 语法类型

> **权威来源**: API 语法类型过滤的完整定义（类型标识、分类、TypeScript 接口、过滤函数、验证函数、使用示例）见 `modules/L1_Analysis/unified_api_parser.md` 第十章。

#### 3.1.5.1 概述

当任务明确说明是 arkts-dynamic 或 arkts-static 语法任务时，在 API 解析流程中应关注支持该语法类型的 API，将支持该语法类型的 API 提取出来。

#### 3.1.5.2 快速参考

| 分类 | 条件 | 静态项目 | 动态项目 |
|------|--------|---------|---------|
| **both** | `@since X dynamic` + `@since Y static` | 兼容 | 兼容 |
| **dynamic** | 仅 `@since X dynamic` | 不兼容 | 兼容 |
| **static** | 仅 `@since Y static` | 兼容 | 不兼容 |
| **unknown** | 无语法类型标识 | 人工确认 | 人工确认 |

#### 3.1.5.3 在生成流程中的集成

```
步骤1: 解析 .d.ts → 提取 API 信息（含 @since 标签）
  ↓
步骤1.5: 过滤语法类型 → filterAPIsBySyntaxType(apiList, targetSyntax)
  ↓  （详细函数签名和实现见 unified_api_parser_syntax_filter.md §10.3）
步骤2: 检查重载 → 仅对过滤后的 API 操作
  ↓
步骤3-6: 参数分类 → 错误码提取 → 子系统规则 → 生成测试
```

#### 3.1.5.4 对测试用例生成的影响

**对于 ArkTS-static 语法任务**：仅生成同时支持动态和静态的 API 测试用例（避免使用仅支持动态的 API，防止编译错误）。

**对于 ArkTS-dynamic 语法任务**：所有 API 均可使用，无限制。

#### 3.1.5.5 常见问题

| 问题 | 解决方案 |
|------|----------|
| 使用了不支持目标语法的 API | 使用 `filterAPIsBySyntaxType()` 过滤（见 unified_api_parser_syntax_filter.md §10.3） |
| 缺少语法类型信息 | 确保 API 解析步骤中正确提取 `@since` 标签 |
| 验证不通过 | 使用 `validateTestCasesSyntaxType()` 验证（见 unified_api_parser_syntax_filter.md §10.5） |

> **完整的函数定义、TypeScript 接口和使用示例**: `modules/L1_Analysis/unified_api_parser.md` 第十章


### 3.1.6 步骤2：检查方法重载

4. **是否存在方法重载**
   - 检查同名方法是否有多个版本
   - 识别隐式可选参数

**输入来源**：
- API 声明文件：`interface/sdk-js/api/@ohos.xxx.d.ts`
- 子系统配置：`references/subsystems/{Subsystem}/_common.md`

**输出**：
```typescript
{
  "methodName": "inputText",
  "parameters": [
    { "name": "text", "type": "string", "optional": false },
    { "name": "mode", "type": "InputTextMode", "optional": false, "implicitOptional": true }
  ],
  "returnType": "Promise<void>",
  "errorCodes": [401, 801],
  "syntaxType": "HYBRID",
  "hasOverloads": true
}
```

### 3.2 步骤2：检查方法重载

查找同一方法是否存在多个重载版本：

```typescript
// 存在两个重载
inputText(text: string): Promise<void>;
inputText(text: string, mode: InputTextMode): Promise<void>;

// 结论：mode 是隐式可选参数
```

**判断规则**：
- 如果同名方法存在参数数量不同的版本
- 则参数较多的版本中新增的参数是隐式可选参数
- 优先调用参数较少的版本（旧版本）

**输出**：
```typescript
{
  "hasOverloads": true,
  "overloads": [
    { "paramCount": 1, "version": 11 },
    { "paramCount": 2, "version": 20 }
  ],
  "implicitOptionalParams": ["mode"]
}
```

### 3.3 步骤3：确定参数类型

对每个参数进行分类：

1. **显式可选**：参数名带 `?` 标记
2. **隐式可选**：通过方法重载判断
3. **必填参数**：不属于上述两种情况

**参数类型分类表**：

| 参数类型 | 标识方式 | 示例 |
|---------|---------|------|
| **显式可选** | 参数名带 `?` | `speed?: number` |
| **隐式可选** | 方法重载判断 | API 11/20 版本差异 |
| **必填参数** | 不属于上述两种 | `from: Point` |

**输出**：
```typescript
{
  "parameters": [
    {
      "name": "text",
      "type": "string",
      "optional": false,
      "optionalType": "REQUIRED"
    },
    {
      "name": "mode",
      "type": "InputTextMode",
      "optional": false,
      "optionalType": "IMPLICIT_OPTIONAL"
    },
    {
      "name": "speed",
      "type": "number",
      "optional": true,
      "optionalType": "EXPLICIT_OPTIONAL"
    }
  ]
}
```

### 3.4 步骤4：提取错误码

从 `@throws` 标记中提取该 API 声明的错误码：

1. **记录错误码列表**
2. **记录每个错误码的触发条件**
3. **确定哪些错误码与参数相关**

**错误码类型**：

> **完整错误码参考表**: 见 `test_generator.md` §3.1。

**输出**：
```typescript
{
  "errorCodes": [
    {
      "code": 401,
      "description": "Parameter error",
      "triggers": [
        "Mandatory parameters left unspecified",
        "Incorrect parameter types",
        "Parameter verification failed"
      ],
      "relatedToParams": true
    },
    {
      "code": 801,
      "description": "Input text mode not supported",
      "triggers": ["Invalid mode parameter"],
      "relatedToParams": true
    }
  ]
}
```

### 3.5 步骤5：应用子系统特殊规则

根据子系统配置应用特殊规则：

**testfwk 子系统特殊规则**：
- **空字符串规则**：testfwk 子系统的字符串参数，空字符串 `''` 是合法参数
- **配置位置**：`references/subsystems/testfwk/_common.md`
- **配置项**：`parameterTestingRules.stringEmpty`

**规则应用示例**：
```typescript
// 检查是否是 testfwk 子系统
if (subsystem === 'testfwk') {
  // 检查是否是 string 类型参数
  if (paramType === 'string') {
    // 应用空字符串规则
    generateEmptyStringTest(paramName); // 合法参数测试
    skipError401Test(paramName); // 不生成 ERROR 测试
  }
}
```

**其他子系统规则**：
- 参考对应的子系统配置文件
- 应用子系统特定的参数测试规则
- 应用子系统特定的错误码处理规则

### 3.6 步骤6：生成测试用例

根据参数类型和 API 语法类型生成相应的测试用例。

> **测试用例模板和断言规则**: 见 `test_generator.md`。本节描述如何在生成流程中应用这些模板。

#### 3.6.1 对于必填参数：

1. **生成 null 测试**（预期抛出错误码，从 @throws 提取）
2. **生成 undefined 测试**（预期抛出错误码，从 @throws 提取）
3. **生成边界值测试**（如适用）
4. **生成空字符串测试**（如果是 string 类型且是 testfwk 子系统）

**测试用例示例**：
```typescript
/**
 * @tc.name testInputTextNull401
 * @tc.number SUB_testfwk_Component_inputText_ERROR_401_001
 * @tc.desc Test inputText with null parameter - 401
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL3
 */
it('testInputTextNull401', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (): Promise<void> => {
  console.log(`${TestTag}, testInputTextNull401 start`);
  await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility');
  await driver.delayMs(1000);
  
  try {
    let driver = Driver.create();
    let component = await driver.findComponent(ON.type('TextInput'));
    await component.inputText(null);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(401);
  }
  
  await stopApplication('com.uitestScene.acts');
  console.log(`${TestTag}, testInputTextNull401 end`);
});
```

#### 3.6.2 对于可选参数（显式和隐式）：

1. **生成 null 测试**（预期不抛出错误码，使用默认值/调用重载）
2. **生成 undefined 测试**（预期不抛出错误码，使用默认值/调用重载）
3. **生成边界值测试**（验证可选参数功能）
4. **生成功能测试**（验证新增参数的作用）

> **重要**：可选参数传入 `null` 的行为必须从 `@throws` 声明确认，不能一概假设"不抛错"。某些可选参数传入 `null` 仍可能触发 401 错误码。

**测试用例示例**：
```typescript
/**
 * @tc.name testScrollToTopOptionalParam
 * @tc.number SUB_testfwk_Component_scrollToTop_PARAM_001
 * @tc.desc Test scrollToTop with optional parameter
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL3
 */
it('testScrollToTopOptionalParam', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (): Promise<void> => {
  console.log(`${TestTag}, testScrollToTopOptionalParam start`);
  await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility');
  await driver.delayMs(1000);
  
  try {
    let driver = Driver.create();
    let component = await driver.findComponent(ON.type('List'));
    // 可选参数传入 null，预期不抛出错误
    await component.scrollToTop(null);
    // 正常执行
    expect(true).assertTrue();
  } catch (error) {
    expect().assertFail();
  }
  
  await stopApplication('com.uitestScene.acts');
  console.log(`${TestTag}, testScrollToTopOptionalParam end`);
});
```

---

## 四、语法规则应用

### 4.1 ArkTS-Dynamic 语法规则

- ✅ 直接传入 `null` 或 `undefined`
- ❌ 禁止使用类型断言：`null as unknown as Type`、`undefined as unknown as Type`
- ✅ ArkTS-Dynamic 不会因此发生类型错误

### 4.2 ArkTS-Static 语法规则

- ❌ 必填参数无需生成 null/undefined 测试（编译时检查）
- ✅ 可选参数仍需生成测试用例
- ✅ 所有类型必须有显式注解

**ArkTS-Static 类型校验特性**：
- 编译时对所有类型注解进行严格检查
- 函数参数类型必须与声明完全匹配
- 类型错误在编译阶段暴露，不会运行时抛出错误码
- 因此必填参数的 null/undefined 测试在编译环节拦截，无需生成用例

---

## 五、完整生成示例

### 5.1 示例：Component.inputText()

**.d.ts 声明**：
```typescript
/**
 * @throws { BusinessError } 401 - Parameter error.
 * @since 11 dynamic
 * @since 23 static
 */
inputText(text: string): Promise<void>;

/**
 * @throws { BusinessError } 401 - Parameter error.
 * @throws { BusinessError } 801 - Input text mode not supported.
 * @since 11 dynamic
 * @since 23 static
 */
inputText(text: string, mode: InputTextMode): Promise<void>;
```

**生成流程**：

```
步骤1：解析 .d.ts 文件
   ↓
   - 方法名：inputText
   - 参数：text (string), mode (InputTextMode)
   - 错误码：401, 801
   - 语法类型：HYBRID
   ↓
步骤2：检查方法重载
   ↓
   - 存在两个重载版本
   - mode 是隐式可选参数
   ↓
步骤3：确定参数类型
   ↓
   - text: 必填参数
   - mode: 隐式可选参数
   ↓
步骤4：提取错误码
   ↓
   - 401: 参数错误
   - 801: 输入文本模式不支持
   ↓
步骤5：应用子系统特殊规则
   ↓
   - testfwk 子系统
   - text 是 string 参数
   - 应用空字符串规则
   ↓
步骤6：生成测试用例
   ↓
   - text: null 测试 (401)
   - text: undefined 测试 (401)
   - text: 空字符串测试 (合法)
   - mode: null 测试 (不抛出 401)
   - mode: undefined 测试 (不抛出 401)
```

**生成的测试用例**：
1. `testInputTextNull401` - 测试 text 参数为 null
2. `testInputTextUndefined401` - 测试 text 参数为 undefined
3. `testInputTextEmptyString` - 测试 text 参数为空字符串
4. `testInputTextModeNull` - 测试 mode 参数为 null
5. `testInputTextModeUndefined` - 测试 mode 参数为 undefined

### 5.2 示例：Driver.waitForComponent()

**.d.ts 声明**：
```typescript
/**
 * @throws { BusinessError } 401 - Parameter error.
 * @throws { BusinessError } 17000002 - Async call not awaited.
 * @since 11 dynamic
 * @since 23 static
 */
waitForComponent(on: On, time: number): Promise<Component>;
```

**生成流程**：

```
步骤1：解析 .d.ts 文件
   ↓
   - 方法名：waitForComponent
   - 参数：on (On), time (number)
   - 错误码：401, 17000002
   - 语法类型：HYBRID
   ↓
步骤2：检查方法重载
   ↓
   - 无重载
   ↓
步骤3：确定参数类型
   ↓
   - on: 必填参数
   - time: 必填参数
   ↓
步骤4：提取错误码
   ↓
   - 401: 参数错误
   - 17000002: 异步调用未使用 await
   ↓
步骤5：应用子系统特殊规则
   ↓
   - 无特殊规则应用
   ↓
步骤6：生成测试用例
   ↓
   - on: null 测试 (401)
   - on: undefined 测试 (401)
   - time: null 测试 (401)
   - time: undefined 测试 (401)
   - time: 0 边界值测试
```

**生成的测试用例**：
1. `testWaitForComponentOnNull401` - 测试 on 参数为 null
2. `testWaitForComponentOnUndefined401` - 测试 on 参数为 undefined
3. `testWaitForComponentTimeNull401` - 测试 time 参数为 null
4. `testWaitForComponentTimeUndefined401` - 测试 time 参数为 undefined
5. `testWaitForComponentTimeZero` - 测试 time 参数为 0

---

## 六、与其他模块的配合

### 6.1 与 L1_Analysis 模块配合

| L1_Analysis 模块 | 提供的信息 | 在生成流程中的作用 |
|-----------------|------------|------------------|
| **unified_api_parser.md** | API 语法类型、错误码提取 | 步骤1、步骤4 |
| **api_parameter_optional_rules.md** | 参数类型识别、子系统特殊规则 | 步骤3、步骤5 |
| **project_parser.md** | 工程语法类型识别 | 确定生成静态或动态测试用例 |

### 6.2 与 L2_Generation 模块配合

| L2_Generation 模块 | 提供的信息 | 在生成流程中的作用 |
|-----------------|------------|------------------|
| **test_generator.md** | 测试用例模板、策略 | 步骤6 应用模板 |
| **templates.md** | 具体的代码模板 | 步骤6 代码生成 |
| **design_doc_generator.md** | 测试设计文档生成 | 生成配套文档 |

---

## 七、输出文件组织

### 7.1 测试用例文件结构

```
{TestModule}/
├── List.test.ets              # 测试套件入口
├── {Module}Test.test.ets       # 功能测试用例
├── {Module}ErrorCode.test.ets   # 错误码测试用例
├── {Module}Static.test.ets     # 静态语法测试用例
└── Util.test.ets               # 工具函数
```

### 7.2 测试用例分类

> **describe 代码结构**: 见 `test_generator.md` §6.1。

**按测试类型分类**：
- `PARAM` - 参数测试
- `ERROR` - 错误码测试
- `RETURN` - 返回值测试
- `BOUNDARY` - 边界值测试

**按参数类型分类**：
- 必填参数测试
- 可选参数测试
- 边界值测试

---

## 八、注意事项

### 8.1 错误码提取注意事项

> **错误码提取规则和参考表**: 见 `test_generator.md` 第三章。

- 生成测试用例时需要精确匹配触发条件
- **禁止生成无法触发的错误码测试**：
  - 201（权限被拒绝）：XTS 测试通常已配置权限，通常不可触发
  - 202（非系统应用调用系统API）：XTS 测试通常是系统应用，通常不可触发
  - 子系统特有错误码：需要具体分析触发条件是否可在测试环境构造
- 如果错误码在 XTS 测试环境中无法构造触发条件，跳过该错误码并在设计文档中注明原因

### 8.2 参数类型判断注意事项

1. **区分显式可选和隐式可选**
   - 显式可选：参数名带 `?` 标记
   - 隐式可选：通过方法重载判断

2. **子系统特殊规则优先**
   - 优先应用子系统配置中的特殊规则
   - 如 testfwk 的空字符串规则

3. **枚举越界值注意事项**
   - ArkTS-Dyn：可测试 null、undefined 触发 401（如果 @throws 有 401）
   - ArkTS-Sta：只测试有效枚举值，跳过 null/undefined/无效值（编译时检查）
   - 禁止使用 `as` 强转传入无效枚举值（`"invalidValue" as SomeEnum`）

### 8.3 语法类型注意事项

1. **确定 API 语法类型**
   - 根据 `@since` 标签判断 API 类型
   - 确定工程兼容性

2. **生成对应语法类型的测试用例**
   - 静态工程：生成静态调用方式的测试用例
   - 动态工程：生成动态调用方式的测试用例

---

## 九、参考文档

- **API 解析器**: `modules/L1_Analysis/unified_api_parser.md`
- **参数可选规则**: `modules/L1_Analysis/analyzer/api_parameter_optional_rules.md`
- **测试生成器**: `modules/L2_Generation/generator/test_generator.md`
- **模板文件**: `modules/L2_Generation/generator/templates.md`
- **testfwk 子系统配置**: `references/subsystems/testfwk/_common.md`
- **通用错误码**: `docs/en/application-dev/onlyfortest/reference/errorcode-universal.md`
