# API 语法类型过滤

> 本文件从 `unified_api_parser.md` 第十章拆分而来，仅在语法类型相关任务时按需加载。
> **完整 API 解析器**: `unified_api_parser.md`
> **语法类型判断算法**: `api_parameter_optional_rules.md` 第四章

---


## 十、API 语法类型过滤

### 10.1 概述

当任务明确说明是 arkts-dynamic 或 arkts-static 语法任务时，在 API 解析流程中应关注支持该语法类型的 API，将支持该语法类型的 API 提取出来。

#### 10.1.1 语法类型标识

在 OpenHarmony API 声明文件（.d.ts）中，存在以下语法类型标识：

| 语法类型 | 标识模式 | 说明 |
|---------|---------|------|
| **动态+静态** | `@since X dynamic` + `@since Y static` | 同时支持两种语法 |
| **仅动态** | `@since X dynamic` 或 `@since X dynamiconly` | 仅支持动态语法 |
| **仅静态** | `@since Y static` 或 `@since Y staticonly` | 仅支持静态语法 |

#### 10.1.2 语法类型分类

根据语法类型标识，将 API 分类为：

| 分类 | 条件 | 说明 |
|------|--------|------|
| **both** | 同时存在 `@since X dynamic` 和 `@since Y static` | 同时支持两种语法 |
| **dynamic** | 只存在 `@since X dynamic` 或 `@since X dynamiconly` | 仅支持动态语法 |
| **static** | 只存在 `@since Y static` 或 `@since Y staticonly` | 仅支持静态语法 |
| **unknown** | 没有语法类型标识 | 需要人工确认 |

### 10.2 API 语法类型信息结构

在 API 信息中添加语法类型支持信息：

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

### 10.3 语法类型过滤逻辑

#### 10.3.1 根据任务类型过滤 API

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

#### 10.3.2 根据任务类型过滤未覆盖测试项

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

### 10.4 语法类型统计

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

### 10.5 自动化验证

#### 10.5.1 验证生成的测试用例是否符合语法类型要求

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

### 10.6 使用示例

#### 10.6.1 ArkTS-static 语法任务

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

// 过滤后的 API（仅支持静态语法）
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

#### 10.6.2 ArkTS-dynamic 语法任务

```typescript
// 任务配置
{
  subsystem: 'testfwk',
  module: 'UiTest',
  syntaxType: 'dynamic',
  version: '12'
}

// 过滤后的 API（支持动态语法）
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

### 10.7 UiTest 模块 API 语法类型统计

根据 UiTest API 的解析结果，语法类型分布如下：

| 语法类型 | 数量 | 占比 | 说明 |
|---------|------|------|------|
| **仅支持动态** | 10 | 8.6% | 只在 ArkTS 动态语法中可用 |
| **仅支持静态** | 0 | 0% | 只在 ArkTS 静态语法中可用 |
| **同时支持** | 106 | 91.4% | 同时支持动态和静态语法 |
| **未知** | 0 | 0% | 无法确定语法类型 |

**按类分布**:

| 类 | 总数 | 动态 | 静态 | 同时支持 | 未知 |
|---|------|------|------|---------|------|
| On | 19 | 0 | 0 | 19 | 0 |
| Component | 28 | 1 | 0 | 27 | 0 |
| Driver | 52 | 8 | 0 | 44 | 0 |
| UiWindow | 17 | 1 | 0 | 16 | 0 |

#### 10.7.1 仅支持动态语法的 API（10 个）

这些 API **不能**用于 ArkTS-static 语法测试用例：

1. `Component.scrollSearch`
2. `Driver.findComponent`
3. `Driver.findWindow`
4. `Driver.waitForComponent`
5. `Driver.findComponents`
6. `Driver.triggerCombineKeys`
7. `Driver.mouseScroll`
8. `Driver.mouseLongClick`
9. `Driver.mouseDrag`
10. `UiWindow.isActived`

### 10.8 对测试用例生成的影响

#### 10.8.1 ArkTS-static 语法任务

**可用的 API**: 106 个（同时支持动态和静态）
**不可用的 API**: 10 个（仅支持动态）

**影响**:
- 生成的测试用例不应使用 10 个仅支持动态语法的 API
- 如果使用了这些 API，会导致编译错误

#### 10.8.2 ArkTS-dynamic 语法任务

**可用的 API**: 116 个（全部 API）
**不可用的 API**: 0 个

**影响**:
- 可以使用所有 API
- 充分利用 API 功能
- 提高测试覆盖率

### 10.9 测试用例生成流程更新建议

在测试用例生成流程中添加语法类型过滤步骤：

```typescript
// 步骤 1: 确定 API 语法支持
const apiSyntaxSupport = extractSyntaxSupport(apiInfo);

// 步骤 2: 根据任务类型过滤 API
const taskSyntaxType: 'dynamic' | 'static' = getTaskSyntaxType();
const filteredAPIs = filterAPIsBySyntaxType(allAPIs, taskSyntaxType);

// 步骤 3: 根据语法类型过滤未覆盖测试项
const filteredUncoveredItems = filterUncoveredItemsBySyntaxType(
  uncoveredItems,
  apiInfoMap,
  taskSyntaxType
);

// 步骤 4: 生成测试用例
generateTestCases(filteredAPIs, filteredUncoveredItems);

// 步骤 5: 验证生成的测试用例
const validation = validateTestCasesSyntaxType(
  testCases,
  apiInfoMap,
  taskSyntaxType
);

if (!validation.valid) {
  console.error('存在使用不支持目标语法类型的 API:');
  validation.invalidCases.forEach(c => {
    console.error(`  ${c.testCase}: ${c.api} - ${c.reason}`);
  });
}
```

### 10.10 实现文件

| 文件 | 路径 | 说明 |
|------|------|------|
| API 解析脚本 | `/tmp/parse_api_with_syntax.js` | 解析 .d.ts 文件，提取语法类型信息 |
| API 信息文件 | `/tmp/api_info_with_syntax.json` | 包含语法类型的 API 信息 |
| 过滤工具 | `./modules/L1_Analysis/parser/unified_api_parser_syntax_filter.md` | 提供语法类型过滤函数 |

---
