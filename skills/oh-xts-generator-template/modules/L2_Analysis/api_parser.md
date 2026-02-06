# API 定义解析器

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载
> - 适用范围：API定义解析
> - 依赖：L1_Framework

---

## 一、模块概述

API 定义解析器用于从 `.d.ts` 文件中提取 API 的完整定义信息，包括接口、方法、属性、参数、返回值、错误码等。

---

## 二、解析目标

### 2.1 接口级别信息

- 接口名称（interface name）
- 继承关系（extends）
- 泛型参数（generics）
- 命名空间（namespace）

### 2.2 方法级别信息

- 方法名称（method name）
- 参数列表（parameters）
- 返回类型（return type）
- 是否异步（async）
- 可访问性（public/private/protected）
- 文档注释（@throws 标记的错误码）
- @since 标记（API 版本）
- @deprecated 标记（已弃用）

### 2.3 属性级别信息

- 属性名称
- 属性类型
- 可选/必需（optional）
- 默认值
- 只读状态（readonly）

---

## 三、解析步骤

### 3.1 定位目标文件

```bash
# API 定义文件通常位于
${ohRoot}/interface/sdk-js/api/

# 常见路径示例
interface/sdk-js/api/@ohos.util.d.ts
interface/sdk-js/api/@ohos.net.d.ts
interface/sdk-js/api/@ohos.file.d.ts
```

### 3.2 读取并解析

使用 Read 工具读取 `.d.ts` 文件：

```
请读取并分析以下文件：
${ohRoot}/interface/sdk-js/api/@ohos.util.d.ts

提取 TreeSet 接口的完整定义
```

### 3.3 提取关键信息

解析后应提取以下结构化信息：

```json
{
  "interface": "TreeSet",
  "namespace": "@ohos.util",
  "type_parameters": ["T"],
  "extends": null,
  "methods": [
    {
      "name": "add",
      "parameters": [{"name": "value", "type": "T", "optional": false}],
      "return_type": "boolean",
      "async": false,
      "throws": [],
      "since": null,
      "deprecated": false
    },
    {
      "name": "popFirst",
      "parameters": [],
      "return_type": "T | undefined",
      "async": false,
      "throws": [{"code": 401, "description": "if container is empty"}],
      "since": null,
      "deprecated": false
    }
  ]
}
```

---

## 四、特殊标记识别

### 4.1 @throws 标记（错误码）

> **重要**：不同的 API 在入参异常时抛出的错误码**并非相同**，必须从 jsdoc 的 `@throws { BusinessError }` 标记中提取具体的错误码和触发条件。

#### 4.1.1 @throws 标记格式

```typescript
/**
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 202 - Non-system applications use system APIs.
 * @throws { BusinessError } 401 - Parameter error. Possible causes: 1. Mandatory parameters are left unspecified; 2. Incorrect parameter types; 3. Parameter verification failed.
 * @throws { BusinessError } 8300001 - Invalid parameter value.
 * @throws { BusinessError } 8300002 - Operation failed. Cannot connect to service.
 * @throws { BusinessError } 8300003 - System internal error.
 */
remove(value: T): boolean;
```

#### 4.1.2 提取信息

解析后应提取：
- **错误码列表**：[201, 202, 401, 8300001, 8300002, 8300003]
- **触发条件**：
  - 201: Permission denied
  - 202: Non-system applications use system APIs
  - 401: Parameter error (Mandatory parameters left unspecified, incorrect types, parameter verification failed)
  - 8300001: Invalid parameter value
  - 8300002: Operation failed
  - 8300003: System internal error

#### 4.1.3 错误码类型说明

| 错误码范围 | 说明 | 示例 |
|----------|------|------|
| **201-299** | 权限和系统级错误 | 201: Permission denied, 202: Non-system applications use system APIs |
| **401** | 通用参数错误 | Parameter error. Possible causes: Mandatory parameters left unspecified, incorrect types |
| **401-999** | 特定场景错误 | 402: Container is empty, 403: Resource not found |
| **8XXXXXX** | 子系统特定错误码 | 8300001: Telephony 参数错误, 2100001: Network 参数错误 |
| **102XXXXX** | Utils 子系统错误码 | 10200001: 参数范围越界, 10200010: 容器为空 |

#### 4.1.4 解析注意事项

1. **必须从 jsdoc 中提取实际错误码**：
   - ❌ **错误**：假设所有参数错误都抛出 401
   - ✅ **正确**：读取 `@throws` 标记，提取该 API 声明的具体错误码

2. **错误码与触发条件对应**：
   - 一个 API 可能声明多个错误码
   - 每个错误码对应特定的触发条件
   - 生成测试用例时需要精确匹配触发条件

3. **参考文档**：
   - **通用错误码**：参见 `docs/en/application-dev/onlyfortest/reference/errorcode-universal.md`
     - 201: Permission Denied
     - 202: Permission Verification Failed for Calling a System API
     - 401: Parameter Check Failed
     - 801: API Not Supported
   - **子系统特有错误码**：参见 `docs/zh-cn/application-dev/reference/apis-xxx/errorcode-xxx.md`
     - Utils: `errorcode-utils.md` (10200001-10200301)
     - Network: `errorcode-network.md` (2100001-2100003)
     - Telephony: `errorcode-telephony.md` (8300001-8300999)

#### 4.1.5 不同 API 的不同错误码示例

```typescript
// 示例 1：Utils TreeSet API - 参数错误抛出 401
/**
 * @throws { BusinessError } 401 - Parameter error.
 */
function popFirst(): T;
// 参数错误抛出：401

// 示例 2：Utils API - 容器为空抛出 10200010
/**
 * @throws { BusinessError } 10200010 - Container is empty.
 */
function popLast(): T;
// 容器为空抛出：10200010

// 示例 3：Network Connection API - 参数错误可能抛出多个错误码
/**
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 202 - Non-system applications use system APIs.
 * @throws { BusinessError } 401 - Parameter error.
 * @throws { BusinessError } 2100001 - Invalid parameter value.
 */
function createNetConnection(): void;
// 参数错误可能抛出：201, 202, 401, 或 2100001

// 示例 4：Telephony SMS API - 多种错误码
/**
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 202 - Non-system applications use system APIs.
 * @throws { BusinessError } 401 - Parameter error. Possible causes: 1. Mandatory parameters are left unspecified. 2. Incorrect parameter types.
 * @throws { BusinessError } 8300001 - Invalid parameter value.
 * @throws { BusinessError } 8300002 - Operation failed. Cannot connect to service.
 * @throws { BusinessError } 8300003 - System internal error.
 * @throws { BusinessError } 8300999 - Unknown error code.
 */
function sendSms(): void;
// 参数错误可能抛出：201, 202, 401, 或 8300001
```

### 4.2 @since 标记（API 版本）

```typescript
/**
 * @since 10
 * @since 11 新增 optional 参数
 */
```

提取信息：
- 最低版本：10
- 版本变更：11 新增 optional 参数

### 4.3 @deprecated 标记（已弃用）

```typescript
/**
 * @deprecated since 12
 * @use {@link newMethod} instead
 */
oldMethod(): void;
```

提取信息：
- 弃用版本：12
- 替代方法：newMethod

---

## 五、API 语法类型判断（动态 vs 静态）

> **重要性**：OpenHarmony 的 ArkTS API 包含两种接口类型，生成测试用例前必须识别

### 5.1 概述

OpenHarmony 的 ArkTS API 包含两种接口类型：
- **动态API (ArkTS-Dyn)**: 需要通过 NAPI 动态加载的接口
- **静态API (ArkTS-Sta)**: 编译时静态链接的接口

### 5.2 判断方法

**关键原则**：解析 API 声明文件（`.d.ts`）中**最后一段 JSDOC** 的 `@since` 标签。

#### 5.2.1 @since 标签格式

@since 标签的可能格式：
```typescript
/**
 * 格式1: 仅动态语法
 * @since 8 dynamiconly
 */

/**
 * 格式2: 仅静态语法
 * @since 12 staticonly
 */

/**
 * 格式3: 先动态后静态（常见）
 * @since 11 dynamic
 * @since 23 static
 */

/**
 * 格式4: 同时支持（单标签）
 * @since 23 dynamic&static
 */
```

#### 5.2.2 判断规则表

| since标签内容 | API类型 | 说明 | 兼容性 |
|-------------|---------|------|--------|
| 仅包含 `dynamiconly` | **动态API** | ArkTS动态语法独有接口 | 仅动态语法工程 |
| 仅包含 `staticonly` | **静态API** | ArkTS静态语法独有接口 | 仅静态语法工程 |
| 仅包含 `dynamic` | **动态API** | 动态语法接口，存在对应的静态语法接口 | 仅动态语法工程 |
| 仅包含 `static` | **静态API** | 静态语法接口，存在对应的动态语法接口 | 仅静态语法工程 |
| 多标签：同时包含 `static` 和 `dynamic` | **动态API&静态API** | 动态和静态语法中接口声明一致 | 两种语法工程都支持 |
| 单标签：包含 `dynamic&static` | **动态API&静态API** | 起始版本相同，同时支持两种语法 | 两种语法工程都支持 |

#### 5.2.3 解析算法

```javascript
/**
 * 解析 API 声明的动静态类型
 * @param {string[]} sinceTags - 最后一段 JSDOC 中的所有 @since 标签内容数组
 * @returns {object} - { type: string, description: string, compatible: string[] }
 */
function parseApiSyntaxType(sinceTags) {
  if (!sinceTags || sinceTags.length === 0) {
    return {
      type: 'STATIC',
      description: '默认静态API（无since标签）',
      compatible: ['static']
    };
  }

  // 收集所有标签标记
  const hasDynamicOnly = sinceTags.some(tag => tag.includes('dynamiconly'));
  const hasStaticOnly = sinceTags.some(tag => tag.includes('staticonly'));
  const hasHybrid = sinceTags.some(tag =>
    tag.includes('dynamic&static') || tag.includes('static&dynamic')
  );
  const hasDynamic = sinceTags.some(tag => tag.includes('dynamic'));
  const hasStatic = sinceTags.some(tag => tag.includes('static'));

  // 优先级判断
  if (hasDynamicOnly) {
    return {
      type: 'DYNAMIC_ONLY',
      description: '动态API独有（已废弃）',
      compatible: ['dynamic']
    };
  }
  if (hasStaticOnly) {
    return {
      type: 'STATIC_ONLY',
      description: '静态API独有',
      compatible: ['static']
    };
  }
  if (hasHybrid || (hasDynamic && hasStatic)) {
    return {
      type: 'HYBRID',
      description: '动态API&静态API（同时支持）',
      compatible: ['dynamic', 'static']
    };
  }
  if (hasDynamic) {
    return {
      type: 'DYNAMIC',
      description: '动态API（存在对应静态接口）',
      compatible: ['dynamic']
    };
  }
  if (hasStatic) {
    return {
      type: 'STATIC',
      description: '静态API（存在对应动态接口）',
      compatible: ['static']
    };
  }

  return {
    type: 'STATIC',
    description: '默认静态API',
    compatible: ['static']
  };
}
```

#### 5.2.4 实际示例

```typescript
/**
 * 示例1: 仅动态语法
 * @syscap SystemCapability.Test.UiTest
 * @since 8 dynamiconly
 * @deprecated since 9
 */
declare class UiComponent {
  click(): Promise<void>;
}
// 解析结果: { type: 'DYNAMIC_ONLY', compatible: ['dynamic'] }

/**
 * 示例2: 同时支持动态和静态语法
 * @syscap SystemCapability.Test.UiTest
 * @atomicservice
 * @since 11 dynamic
 * @since 23 static
 */
declare enum MatchPattern {
  EQUALS = 0,
  CONTAINS = 1
}
// 解析结果: { type: 'HYBRID', compatible: ['dynamic', 'static'] }

/**
 * 示例3: 同时支持（单标签）
 * @syscap SystemCapability.Test.UiTest
 * @crossplatform
 * @since 23 dynamic&static
 */
function findById(id: string): Component;
// 解析结果: { type: 'HYBRID', compatible: ['dynamic', 'static'] }

/**
 * 示例4: 仅动态
 * @since 11 dynamic
 */
function getDynamicAPI(): string;
// 解析结果: { type: 'DYNAMIC', compatible: ['dynamic'] }

/**
 * 示例5: 无标签
 */
function getDefaultAPI(): number;
// 解析结果: { type: 'DYNAMIC', compatible: ['dynamic'] }
```

### 5.3 解析输出

API 语法类型判断结果应包含在解析输出中：

```typescript
{
  "api": "Component",
  "syntax_type": {
    "type": "HYBRID",
    "description": "动态API&静态API（同时支持）",
    "compatible": ["dynamic", "static"],
    "since_tags": ["@since 11 dynamic", "@since 23 static"]
  },
  "definition": {...}
}
```

### 5.4 与工程类型匹配

解析 API 语法类型后，需要与工程语法类型进行兼容性检查，以确定正确的测试用例生成策略。

#### 5.4.1 工程语法类型识别

**概述**：OpenHarmony 工程支持两种 ArkTS 语法类型：
- **静态语法工程**：使用 `arkTSVersion: "1.2"` 配置
- **动态语法工程**：无 `arkTSVersion` 配置

**识别方法**：读取工程根目录下的 `build-profile.json5` 配置文件。

**详细内容**：参见 `modules/L2_Analysis/project_parser.md` 中的"二、工程语法类型识别"章节。

#### 5.4.2 兼容性检查矩阵

解析 API 语法类型后，需要与工程语法类型进行兼容性检查：

| API 类型 | 静态语法工程 | 动态语法工程 | 说明 |
|---------|-------------|-------------|------|
| DYNAMIC_ONLY | ❌ 不兼容 | ✅ 兼容 | 动态API仅支持动态语法工程 |
| STATIC_ONLY | ✅ 兼容 | ❌ 不兼容 | 静态API仅支持静态语法工程 |
| DYNAMIC | ❌ 不兼容 | ✅ 兼容 | 动态API，存在对应静态接口 |
| STATIC | ✅ 兼容 | ❌ 不兼容 | 静态API，存在对应动态接口 |
| HYBRID | ✅ 兼容（静态调用） | ✅ 兼容（动态调用） | 同时支持两种语法 |

**详细内容**：参见 `modules/L2_Analysis/project_parser.md` 中的"三、测试用例生成策略"章节。

#### 5.4.3 完整解析流程

```
步骤1：解析 API 语法类型
  ↓
  使用本模块的 parseApiSyntaxType() 函数
  ↓
  输出：{ type: 'HYBRID', compatible: ['dynamic', 'static'] }
  ↓
步骤2：解析工程语法类型
  ↓
  使用 project_parser.md 模块的 identifyProjectSyntax() 函数
  ↓
  输出：{ type: 'STATIC', description: '静态语法工程' }
  ↓
步骤3：兼容性匹配
  ↓
  检查：工程类型是否在 API 的 compatible 列表中
  ↓
  结果：✅ 兼容 或 ⚠️ 不兼容
  ↓
步骤4：生成测试用例
  ↓
  根据兼容性结果选择生成策略：
  - 静态工程 + 混合API → 生成静态调用方式
  - 动态工程 + 混合API → 生成动态调用方式
  - 不兼容 → 提示用户或跳过
```

#### 5.4.4 配合使用示例

```javascript
// 完整的 API 和工程类型解析示例

// 步骤1：解析 API 类型
const apiInfo = parseApiSyntaxType(['@since 11 dynamic', '@since 23 static']);
// apiInfo = {
//   type: 'HYBRID',
//   description: '动态API&静态API（同时支持）',
//   compatible: ['dynamic', 'static']
// }

// 步骤2：解析工程类型（需要引用 project_parser.md）
// const projectInfo = identifyProjectSyntax('/path/to/project');
// projectInfo = {
//   type: 'STATIC',
//   description: '静态语法工程（arkTSVersion: 1.2）'
// }

// 步骤3：兼容性检查
const isCompatible = apiInfo.compatible.includes('STATIC'); // true

// 步骤4：生成测试用例
if (isCompatible) {
  // 生成静态调用方式的测试用例
  generateStaticTestCases(apiInfo);
}
```

**注意**：`identifyProjectSyntax()` 函数的详细实现请参见 `modules/L2_Analysis/project_parser.md`。

---

## 六、模块级解析

> **重要性**：支持解析整个模块的所有 API，批量生成测试用例

### 6.1 概述

OpenHarmony 子系统通常包含多个模块，每个模块对应一个或多个 API 声明文件：

```
子系统（如 ArkUI）
  ├── Component 模块
  │   └── @ohos.arkui.d.ts → Component, Column, Row, Text, Button 等 API
  ├── Animator 模块
  │   └── @ohos.animator.d.ts → animateTo, getAnimator 等 API
  └── Router 模块
      └── @ohos.router.d.ts → pushUrl, back, replaceUrl 等 API
```

**三种解析粒度**：
- **API 级解析**：解析单个 API（如 Component.onClick）
- **模块级解析**：解析整个模块的所有 API（如 Animator 模块）
- **子系统级解析**：解析整个子系统的所有模块和 API

### 6.2 模块识别方法

#### 6.2.1 从子系统配置获取模块映射

**配置位置**：`references/subsystems/{SubsystemName}/_common.md`

**配置格式**：
```markdown
### 1.3 模块映射配置

| 模块名称 | API 声明文件 | 主要 API | 说明 |
|---------|-------------|---------|------|
| **Component** | @ohos.arkui.d.ts | Component, Column, Row 等 | 基础组件 |
| **Animator** | @ohos.animator.d.ts | animateTo, getAnimator 等 | 动画接口 |
| **Router** | @ohos.router.d.ts | pushUrl, back, clear 等 | 路由导航 |
```

**实际示例**：
```
references/subsystems/ArkUI/_common.md     # ArkUI 子系统通用配置
references/subsystems/ArkUI/Component.md   # Component 模块配置
references/subsystems/ArkUI/Animator.md    # Animator 模块配置
references/subsystems/ArkUI/Router.md      # Router 模块配置
```

#### 6.2.2 从 API 声明文件推断模块

如果子系统配置中没有模块映射，可以通过以下方式推断：

1. **从 .d.ts 文件名推断**：
   - `@ohos.animator.d.ts` → Animator 模块
   - `@ohos.router.d.ts` → Router 模块

2. **从命名空间推断**：
   - `declare namespace Animator` → Animator 模块
   - `declare namespace Router` → Router 模块

3. **从类名推断**：
   - `class Component` → Component 模块
   - `class Router` → Router 模块

### 6.3 模块级解析流程

```
步骤1：确定目标模块
  ↓
  从子系统配置获取模块列表
  或通过 .d.ts 文件推断模块
  ↓
步骤2：定位模块的 API 声明文件
  ↓
  根据模块映射配置找到对应的 .d.ts 文件
  如：Animator 模块 → @ohos.animator.d.ts
  ↓
步骤3：解析模块中的所有 API
  ↓
  使用本模块的 API 解析方法
  提取所有接口、方法、属性
  ↓
步骤4：生成模块测试套件
  ↓
  为模块中的每个 API 生成测试用例
  组织到一个测试文件中
```

### 6.4 模块级解析输出

```typescript
{
  "subsystem": "ArkUI",
  "module": "Animator",
  "dts_file": "@ohos.animator.d.ts",
  "apis": [
    {
      "name": "animateTo",
      "parameters": [...],
      "return_type": "AnimatorResult",
      "syntax_type": {
        "type": "HYBRID",
        "compatible": ["dynamic", "static"]
      }
    },
    {
      "name": "getAnimator",
      "parameters": [],
      "return_type": "Animator",
      "syntax_type": {
        "type": "STATIC",
        "compatible": ["static"]
      }
    }
    // ... 更多 API
  ]
}
```

### 6.5 模块级测试用例生成策略

#### 6.5.1 单个测试文件包含整个模块

```typescript
/**
 * @tc.name Animator Module Test
 * @tc.number SUB_ARKUI_ANIMATOR_0100
 * @tc.desc Animator 模块完整测试
 */
describe('Animator Module Test', () => {

  // API 1: animateTo
  it('testAnimateTo001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
    // 测试代码
  });

  // API 2: getAnimator
  it('testGetAnimator001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
    // 测试代码
  });

  // ... 更多 API 测试
});
```

#### 6.5.2 按功能分组测试

```typescript
describe('Animator Module Test', () => {

  // 动画方法组
  describe('Animation Methods', () => {
    it('testAnimateTo001', ...);
    it('testAnimateXXX002', ...);
  });

  // 查询方法组
  describe('Query Methods', () => {
    it('testGetAnimator001', ...);
    it('testGetState001', ...);
  });
});
```

### 6.6 模块与工程类型的兼容性

解析模块时，需要考虑模块中各个 API 的语法类型：

| 模块 | API 类型分布 | 静态工程 | 动态工程 | 处理策略 |
|------|------------|---------|---------|---------|
| **Component** | 混合API | ✅ 静态调用 | ✅ 动态调用 | 分别生成 |
| **Animator** | 静态API | ✅ 兼容 | ❌ 不兼容 | 仅静态工程 |
| **Router** | 动态API | ❌ 不兼容 | ✅ 兼容 | 仅动态工程 |
| **Window** | 混合API | ✅ 兼容 | ✅ 兼容 | 分别生成 |

**处理策略**：
1. 检查模块中所有 API 的语法类型
2. 根据工程类型筛选兼容的 API
3. 对不兼容的 API 给出提示或跳过
4. 生成兼容 API 的测试用例

### 6.7 批量解析子系统

**输入**：子系统名称（如 "ArkUI"）

**流程**：
```
1. 读取子系统配置
   ↓
2. 获取模块映射配置
   ↓
3. 遍历每个模块：
   ├─ 定位 .d.ts 文件
   ├─ 解析所有 API
   ├─ 检查兼容性
   └─ 生成测试用例
   ↓
4. 输出完整测试套件
```

---

## 七、API 子系统识别

> **重要**：严禁仅根据 API 名称推测子系统归属，必须通过 SDK 分析确认

### 6.1 识别方法

1. **查找 .d.ts 文件**：在 `interface` 目录下搜索 API 定义文件
2. **查看 Kit 模块**：确认 API 所在的 Kit 模块
3. **参考开发指南**：查阅 `docs` 目录下对应子系统的开发指南

### 6.2 常见 Kit 模块映射

| Kit 模块 | 子系统 | 示例 API |
|---------|--------|----------|
| @kit.ArkTS | UTILS | TreeSet, TreeMap, List, Vector |
| @kit.NetworkKit | NETWORK | http, tcp, socket |
| @kit.ArkData | DATA | relationalStore, preferences |
| @kit.CoreFileKit | FILE | picker, fileIO |
| @kit.ArkGraphics | GRAPHICS | image, pixelMap |
| @kit.ArkUI | UI | Component, Animator |

### 6.3 子系统识别流程

```
输入：API 名称
  ↓
步骤1：在 interface/ 目录搜索 .d.ts 文件
  ↓
步骤2：读取文件，查看模块声明
  ↓
步骤3：确定 Kit 模块和子系统
  ↓
步骤4：在 docs/ 验证子系统归属
  ↓
输出：子系统名 + 模块名
```

---

## 七、与文档配合使用

### 7.1 API Reference 文档

位置：`docs/zh-cn/application-dev/reference/apis-*/`

作用：
- 获取 API 的详细说明
- 理解参数的具体含义和取值范围
- 查看错误码的触发条件
- 参考官方示例代码

### 7.2 开发指南文档

位置：`docs/zh-cn/application-dev/[子系统]/`

作用：
- 了解子系统的整体架构
- 理解 API 的使用场景
- 学习最佳实践

### 7.3 综合使用示例

```
任务：为 @ohos.util.TreeSet 生成测试用例

步骤1：解析 .d.ts
- 文件：interface/sdk-js/api/@ohos.util.d.ts
- 提取：接口定义、方法签名、参数类型

步骤2：查阅 API Reference
- 文件：docs/zh-cn/application-dev/reference/apis-arkdata/js-apis-util.md
- 获取：API 说明、参数约束、错误码含义

步骤3：综合信息
- 结合 .d.ts 的类型定义
- 参考 API Reference 的功能说明
- 生成准确的测试用例
```

---

## 八、解析输出格式

### 8.1 结构化输出

```typescript
// API 解析结果
{
  "api": "TreeSet",
  "subsystem": "UTILS",
  "module": "util",
  "kit": "@kit.ArkTS",
  "definition": {
    "interface": "TreeSet<T>",
    "extends": null,
    "methods": [...]
  },
  "reference": {
    "api_doc": "docs/zh-cn/application-dev/reference/apis-arkdata/js-apis-util.md",
    "dev_guide": "docs/zh-cn/application-dev/arkdata/"
  }
}
```

### 8.2 用于测试生成

解析结果将用于：
1. 生成测试用例编号（SUB_[子系统]_[模块]_...）
2. 确定导入语句（import from '@kit.XXX'）
3. 设计测试场景（基于参数类型和错误码）
4. 生成断言（基于返回值类型）
