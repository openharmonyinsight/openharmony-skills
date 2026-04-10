# 测试用例生成流程

> **文档版本**: 1.0.0
> **创建日期**: 2026-03-03
> **模块信息**: L3_Generation
> **适用范围**: 测试用例生成流程

---

## 一、概述

本文档定义了从 API 声明生成测试用例的完整流程，涵盖了从解析 .d.ts 文件到生成测试用例代码的各个步骤。

**与其他模块的配合**：
- 依赖 `L2_Analysis/api_parser.md` 进行 API 解析和错误码提取
- 依赖 `L2_Analysis/api_parameter_optional_rules.md` 进行参数分类和规则应用
- 与 `L3_Generation/test_generator.md` 配合，应用测试用例模板

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

#### 3.1.5.1 概述

当任务明确说明是 arkts-dynamic 或 arkts-static 语法任务时，在 API 解析流程中应关注支持该语法类型的 API，将支持该语法类型的 API 提取出来。

#### 3.1.5.2 语法类型标识

在 OpenHarmony API 声明文件（.d.ts）中，存在以下语法类型标识：

| 语法类型 | 标识模式 | 说明 |
|---------|---------|------|
| **动态+静态** | `@since X dynamic` + `@since Y static` | 同时支持两种语法 |
| **仅动态** | `@since X dynamic` 或 `@since X dynamiconly` | 仅支持动态语法 |
| **仅静态** | `@since Y static` 或 `@since Y staticonly` | 仅支持静态语法 |

#### 3.1.5.3 API 语法类型分类

根据语法类型标识，将 API 分类为：

| 分类 | 条件 | 说明 |
|------|--------|------|
| **both** | 同时存在 `@since X dynamic` 和 `@since Y static` | 同时支持两种语法 |
| **dynamic** | 只存在 `@since X dynamic` 或 `@since X dynamiconly` | 仅支持动态语法 |
| **static** | 只存在 `@since Y static` 或 `@since Y staticonly` | 仅支持静态语法 |
| **unknown** | 没有语法类型标识 | 需要人工确认 |

#### 3.1.5.4 API 语法类型信息结构

每个 API 现在包含完整的语法支持信息：

```typescript
interface APIInfoWithSyntax {
  className: string;
  methodName: string;
  signature: string;
  parameters: ParameterInfo[];
  returnType: string;
  errorCodes: string[];
  
  // API 语法支持信息
  syntaxSupport?: {
    dynamic: {
      supported: boolean;
      sinceVersion?: string;
    };
    static: {
      supported: boolean;
      sinceVersion?: string;
    };
  };
  
  // 语法类型（方便快速查询）
  syntaxType?: 'both' | 'dynamic' | 'static' | 'unknown';
}
```

**字段说明**：
- `syntaxSupport.dynamic.supported`: 是否支持动态语法
- `syntaxSupport.dynamic.sinceVersion`: 动态语法支持起始版本
- `syntaxSupport.static.supported`: 是否支持静态语法
- `syntaxSupport.static.sinceVersion`: 静态语法支持起始版本
- `syntaxType`: 语法类型（dynamic/static/both/unknown）

#### 3.1.5.5 语法类型过滤逻辑

**根据任务类型过滤 API**：

```typescript
/**
 * 根据任务语法类型过滤 API
 *
 * @param apis API 信息数组
 * @param taskSyntaxType 任务语法类型（'dynamic' 或 'static'）
 * @returns 过滤后的 API 信息数组
 */
function filterAPIsBySyntaxType(
  apis: APIInfoWithSyntax[],
  taskSyntaxType: 'dynamic' | 'static'
): APIInfoWithSyntax[] {
  return apis.filter((api) => {
    if (!api.syntaxSupport) {
      // 没有语法支持信息的 API，默认保留
      console.warn(`API ${api.className}.${api.methodName} 缺少语法支持信息`);
      return true;
    }

    const syntaxType = api.syntaxType || 'unknown';
    return (
      syntaxType === 'both' ||
      syntaxType === taskSyntaxType
    );
  });
}
```

**根据任务类型过滤未覆盖测试项**：

```typescript
/**
 * 根据任务语法类型过滤未覆盖测试项
 *
 * @param uncoveredItems 未覆盖测试项数组
 * @param apiInfoMap API 信息映射
 * @param taskSyntaxType 任务语法类型（'dynamic' 或 'static'）
 * @returns 过滤后的未覆盖测试项数组
 */
function filterUncoveredItemsBySyntaxType(
  uncoveredItems: any[],
  apiInfoMap: Map<string, APIInfoWithSyntax>,
  taskSyntaxType: 'dynamic' | 'static'
): any[] {
  return uncoveredItems.filter((item) => {
    const apiKey = `${item.class}.${item.method}`;
    const apiInfo = apiInfoMap.get(apiKey);

    if (!apiInfo) {
      // 未找到 API 信息，默认保留
      console.warn(`未找到 API 信息: ${apiKey}`);
      return true;
    }

    if (!apiInfo.syntaxSupport) {
      // 没有语法支持信息，默认保留
      console.warn(`API ${apiKey} 缺少语法支持信息`);
      return true;
    }

    const syntaxType = apiInfo.syntaxType || 'unknown';
    return (
      syntaxType === 'both' ||
      syntaxType === taskSyntaxType
    );
  });
}
```

#### 3.1.5.6 语法类型统计

```typescript
/**
 * 生成 API 语法支持报告
 *
 * @param apis API 信息数组
 * @returns 语法支持报告
 */
interface SyntaxSupportReport {
  total: number;
  dynamicOnly: number;
  staticOnly: number;
  both: number;
  unknown: number;
}

function generateSyntaxSupportReport(apis: APIInfoWithSyntax[]): SyntaxSupportReport {
  const report: SyntaxSupportReport = {
    total: apis.length,
    dynamicOnly: 0,
    staticOnly: 0,
    both: 0,
    unknown: 0,
  };

  for (const api of apis) {
    if (!api.syntaxSupport) {
      report.unknown++;
      continue;
    }

    const syntaxType = api.syntaxType || 'unknown';
    switch (syntaxType) {
      case 'dynamic':
        report.dynamicOnly++;
        break;
      case 'static':
        report.staticOnly++;
        break;
      case 'both':
        report.both++;
        break;
      case 'unknown':
        report.unknown++;
        break;
    }
  }

  return report;
}
```

#### 3.1.5.7 自动化验证

```typescript
/**
 * 验证生成的测试用例是否符合语法类型要求
 *
 * @param testCases 测试用例数组
 * @param apiInfoMap API 信息映射
 * @param taskSyntaxType 任务语法类型（'dynamic' 或 'static'）
 * @returns 验证结果
 */
interface ValidationResult {
  valid: boolean;
  invalidCases: Array<{
    testCase: string;
    api: string;
    reason: string;
  }>;
}

function validateTestCasesSyntaxType(
  testCases: any[],
  apiInfoMap: Map<string, APIInfoWithSyntax>,
  taskSyntaxType: 'dynamic' | 'static'
): ValidationResult {
  const invalidCases: Array<{
    testCase: string;
    api: string;
    reason: string;
  }> = [];

  for (const testCase of testCases) {
    const apiKey = `${testCase.className}.${testCase.methodName}`;
    const apiInfo = apiInfoMap.get(apiKey);

    if (!apiInfo) {
      continue;
    }

    if (!apiInfo.syntaxSupport) {
      continue;
    }

    const syntaxType = apiInfo.syntaxType || 'unknown';
    if (
      syntaxType !== 'both' &&
      syntaxType !== taskSyntaxType
    ) {
      invalidCases.push({
        testCase: testCase.name,
        api: apiKey,
        reason: `API 仅支持 ${syntaxType} 语法，但任务要求 ${taskSyntaxType} 语法`,
      });
    }
  }

  return {
    valid: invalidCases.length === 0,
    invalidCases,
  };
}
```

#### 3.1.5.8 使用示例

**示例 1：ArkTS-static 语法任务**

```typescript
// 任务配置
{
  subsystem: 'testfwk',
  module: 'UiTest',
  syntaxType: 'static',
  version: '23'
}

// API 解析结果
{
  "On": {
    "text": {
      "syntaxSupport": {
        "dynamic": { "supported": true, "sinceVersion": "11" },
        "static": { "supported": true, "sinceVersion": "23" }
      },
      "syntaxType": "both"
    }
  }
}

// 过滤后的 API
{
  "On": {
    "text": {
      "syntaxSupport": {
        "static": { "supported": true, "sinceVersion": "23" }
      },
      "syntaxType": "both"
    }
  }
}
```

**示例 2：ArkTS-dynamic 语法任务**

```typescript
// 任务配置
{
  subsystem: 'testfwk',
  module: 'UiTest',
  syntaxType: 'dynamic',
  version: '12'
}

// 过滤后的 API
{
  "UIEventObserver": {
    "once": {
      "syntaxSupport": {
        "dynamic": { "supported": true, "sinceVersion": "11" }
      },
      "syntaxType": "dynamic"
    }
  }
}
```

#### 3.1.5.9 对测试用例生成的影响

**对于 ArkTS-static 语法任务**：

| 指标 | 数值 | 说明 |
|------|------|------|
| 可用的 API | 106 个（同时支持动态和静态） | 只生成支持静态语法的 API 测试用例 |
| 不可用的 API | 10 个（仅支持动态） | 避免使用这些 API，防止编译错误 |
| 影响 | 只生成支持静态语法的测试用例 | 提高测试用例质量和成功率 |

**对于 ArkTS-dynamic 语法任务**：

| 指标 | 数值 | 说明 |
|------|------|------|
| 可用的 API | 116 个（全部 API） | 可以使用所有 API 生成测试用例 |
| 不可用的 API | 0 个 | 无 API 限制 |
| 影响 | 充分利用 API 功能 | 提高测试覆盖率 |

#### 3.1.5.10 常见问题和解决方案

**问题 1：使用了不支持目标语法的 API**

- **现象**：生成的测试用例使用了仅支持动态语法的 API，但在静态语法任务中
- **影响**：编译错误、测试执行失败
- **解决方案**：使用 `filterAPIsBySyntaxType()` 过滤 API，仅生成支持目标语法的测试用例

**问题 2：缺少语法类型信息**

- **现象**：API 信息中没有语法支持信息，无法过滤
- **影响**：可能生成不正确的测试用例
- **解决方案**：确保 API 解析步骤中正确提取语法类型信息

**问题 3：验证不通过**

- **现象**：生成的测试用例中有使用不支持目标语法的 API
- **影响**：需要手动修复
- **解决方案**：使用 `validateTestCasesSyntaxType()` 验证生成的测试用例

---

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

| 错误码范围 | 说明 | 示例 |
|----------|------|------|
| **201-299** | 权限和系统级错误 | 201: Permission denied |
| **401** | 通用参数错误 | Parameter error |
| **401-999** | 特定场景错误 | 402: Container is empty |
| **8XXXXXX** | 子系统特定错误码 | 8300001: 参数错误 |
| **102XXXXX** | Utils 子系统错误码 | 10200001: 参数越界 |

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
    await component.inputText(null as unknown as string);
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
    await component.scrollToTop(null as unknown as number);
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

### 6.1 与 L2_Analysis 模块配合

| L2_Analysis 模块 | 提供的信息 | 在生成流程中的作用 |
|-----------------|------------|------------------|
| **api_parser.md** | API 语法类型、错误码提取 | 步骤1、步骤4 |
| **api_parameter_optional_rules.md** | 参数类型识别、子系统特殊规则 | 步骤3、步骤5 |
| **project_parser.md** | 工程语法类型识别 | 确定生成静态或动态测试用例 |

### 6.2 与 L3_Generation 模块配合

| L3_Generation 模块 | 提供的信息 | 在生成流程中的作用 |
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

1. **必须从 jsdoc 中提取实际错误码**
   - ❌ **错误**：假设所有参数错误都抛出 401
   - ✅ **正确**：读取 `@throws` 标记，提取该 API 声明的具体错误码

2. **错误码与触发条件对应**
   - 一个 API 可能声明多个错误码
   - 每个错误码对应特定的触发条件
   - 生成测试用例时需要精确匹配触发条件

### 8.2 参数类型判断注意事项

1. **区分显式可选和隐式可选**
   - 显式可选：参数名带 `?` 标记
   - 隐式可选：通过方法重载判断

2. **子系统特殊规则优先**
   - 优先应用子系统配置中的特殊规则
   - 如 testfwk 的空字符串规则

### 8.3 语法类型注意事项

1. **确定 API 语法类型**
   - 根据 `@since` 标签判断 API 类型
   - 确定工程兼容性

2. **生成对应语法类型的测试用例**
   - 静态工程：生成静态调用方式的测试用例
   - 动态工程：生成动态调用方式的测试用例

---

## 九、参考文档

- **API 解析器**: `modules/L2_Analysis/api_parser.md`
- **参数可选规则**: `modules/L2_Analysis/api_parameter_optional_rules.md`
- **测试生成器**: `modules/L3_Generation/test_generator.md`
- **模板文件**: `modules/L3_Generation/templates.md`
- **testfwk 子系统配置**: `references/subsystems/testfwk/_common.md`
- **通用错误码**: `docs/en/application-dev/onlyfortest/reference/errorcode-universal.md`
