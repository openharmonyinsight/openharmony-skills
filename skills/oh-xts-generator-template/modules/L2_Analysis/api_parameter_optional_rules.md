# OpenHarmony API 参数规则参考

> **文档版本**: 6.0.0
> **更新日期**: 2026-03-03
> **适用范围**: oh-xts-generator-template - L2_Analysis 模块 - API 参数和语法规则

## 一、概述

本文档定义了 OpenHarmony API 的参数相关规则和语法类型判断规则，为测试用例生成提供详细的规范说明。

**与 L2_Analysis 模块其他文档的关系**：
- **unified_api_parser.md**: 定义统一的 API 信息接口和解析流程
- **api_parameter_optional_rules.md**: **本文档** - 定义具体的参数和语法规则
- **test_case_generation_flow.md** (L3): 定义测试用例生成流程

---

## 二、参数可选性识别

### 2.1 可选参数的类型

OpenHarmony API 中存在两种类型的可选参数：

#### 类型1：显式可选参数（带 `?` 标记）

在 `.d.ts` 文件中，参数名后带 `?` 标记的参数为可选参数。

**示例**：
```typescript
// speed 是可选参数
swipeBetween(from: Point, to: Point, speed?: int): Promise<void>;

// vertical 和 offset 都是可选参数
scrollSearch(on: On, vertical?: boolean, offset?: number): Promise<Component>;
```

#### 类型2：隐式可选参数（API 版本演进）

当同一方法存在多个重载，新版本增加了参数时，新增加的参数实际上是可选的。

**示例**：
```typescript
// API 11: 单参数版本
inputText(text: string): Promise<void>;

// API 20: 增加了 mode 参数（mode 实际是可选的）
inputText(text: string, mode: InputTextMode): Promise<void>;
```

**说明**：
- 虽然 API 20 的 `inputText(text: string, mode: InputTextMode)` 中 mode 在 `.d.ts` 文件中没有 `?` 标记
- 但由于存在单参数版本 `inputText(text: string)`，mode 参数实际上是可选的
- 当 mode 传入 `null` 或 `undefined` 时，会调用单参数版本，**不会抛出错误码 401**

**识别规则**：
- 检查是否存在方法重载
- 如果同名方法存在参数数量不同的版本，则参数较多的版本中新增的参数是隐式可选参数
- 优先调用参数较少的版本（旧版本）

### 2.2 必填参数识别

参数不属于上述两种可选参数类型的，即为必填参数。

**示例**：
```typescript
// from 和 to 是必填参数（没有 ? 标记，且不存在单参数版本）
swipeBetween(from: Point, to: Point, speed?: int): Promise<void>;

// time 是必填参数（没有 ? 标记）
waitForComponent(on: On, time: number): Promise<Component>;

// on, from, to 都是必填参数
isComponentPresentWhenSwipe(on: On, from: Point, to: Point, speed?: int): Promise<boolean>;
```

---

## 三、错误码识别规则

> **详细提取策略**: 与 unified_api_parser.md 配合使用

### 3.1 @throws 标记提取（重要）

**提取原则**：
- 从 `.d.ts` 文件的 `@throws { BusinessError }` 标记中提取
- 必须记录错误码和对应的触发条件
- 错误码类型范围：
  - **201-299**: 权限和系统级错误
  - **401**: 通用参数错误
  - **401-999**: 特定场景错误
  - **8XXXXXX**: 子系统特定错误码
  - **102XXXXX**: Utils 子系统错误码

**错误码映射**：
- 不同 API 在参数错误时可能抛出不同错误码
- 必须从 JSDOC 中提取实际错误码，不能假设固定值
- 例如：有些 API 参数错误抛出 401，有些抛出 17000007

### 3.2 错误码与参数测试的关系

| 参数类型 | 错误码来源 | 测试用例类型 |
|---------|------------|-------------|
| 必填参数 - null/undefined | 从 @throws 标记提取 | ERROR 测试 |
| 可选参数 - null/undefined | 通常不抛出错误码 | PARAM 测试（验证默认值/重载） |
| 参数类型错误 | 从 @throws 标记提取 | ERROR 测试 |

---

### 4.1 概述

OpenHarmony 的 ArkTS API 包含两种接口类型，生成测试用例前必须识别：

- **动态API (ArkTS-Dyn)**: 需要通过 NAPI 动态加载的接口
- **静态API (ArkTS-Sta)**: 编译时静态链接的接口

### 4.2 判断方法

**关键原则**：解析 API 声明文件（`.d.ts`）中**最后一段 JSDOC** 的 `@since` 标签。

#### 4.2.1 @since 标签格式

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

#### 4.2.2 判断规则表

| since标签内容 | API类型 | 说明 | 兼容性 |
|-------------|---------|------|--------|
| 仅包含 `dynamiconly` | **动态API** | ArkTS动态语法独有接口 | 仅动态语法工程 |
| 仅包含 `staticonly` | **静态API** | ArkTS静态语法独有接口 | 仅静态语法工程 |
| 仅包含 `dynamic` | **动态API** | 动态语法接口，存在对应的静态语法接口 | 仅动态语法工程 |
| 仅包含 `static` | **静态API** | 静态语法接口，存在对应的动态语法接口 | 仅静态语法工程 |
| 多标签：同时包含 `static` 和 `dynamic` | **动态API&静态API** | 动态和静态语法中接口声明一致 | 两种语法工程都支持 |
| 单标签：包含 `dynamic&static` | **动态API&静态API** | 起始版本相同，同时支持两种语法 | 两种语法工程都支持 |

#### 4.2.3 解析算法

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

### 4.3 与测试用例生成结合

| API 语法类型 | 静态工程测试策略 | 动态工程测试策略 |
|------------|------------------|------------------|
| DYNAMIC_ONLY | ❌ 不兼容，不生成 | ✅ 生成动态调用测试 |
| STATIC_ONLY | ✅ 生成静态调用测试 | ❌ 不兼容，不生成 |
| HYBRID | ✅ 生成静态调用测试 | ✅ 生成动态调用测试 |
| DYNAMIC | ❌ 不兼容，不生成 | ✅ 生成动态调用测试 |
| STATIC | ✅ 生成静态调用测试 | ❌ 不兼容，不生成 |

---

## 五、参数 null/undefined 测试规则

### 5.1 核心原则

**关键规则**：
1. **必填参数**传入 `null` 或 `undefined` 时：**会抛出错误码**（错误码从 @throws 标记提取）

2. **可选参数（显式）**传入 `null` 或 `undefined` 时：**不会抛出错误码**
   - 调用时不传该参数或传 `null/undefined`，使用默认值
   - API 正常运行
   - **需要生成测试用例**，验证此行为

3. **可选参数（隐式）**传入 `null` 或 `undefined` 时：**不会抛出错误码**
   - 会调用旧版本的重载方法
   - API 正常运行
   - **需要生成测试用例**，验证此行为

### 5.2 测试用例生成策略

#### 5.2.1 ArkTS-Dynamic

| 参数类型 | null/undefined 测试 | 测试目标 | 测试预期 |
|---------|---------------------|---------|---------|
| 必填参数 | ✅ 需要生成 | 验证传入 null/undefined 时抛出错误码 | 抛出错误码（从 @throws 提取） |
| 可选参数（显式） | ✅ 需要生成 | 验证传入 null/undefined 时不会抛出错误码，使用默认值 | 不抛出错误码，正常运行 |
| 可选参数（隐式） | ✅ 需要生成 | 验证传入 null/undefined 时调用旧版本重载 | 不抛出错误码，正常运行 |

**说明**：
- **所有参数类型**都需要生成 null/undefined 测试用例
- 区别在于**测试预期**不同：
  - 必填参数：预期抛出错误码（从 @throws 提取）
  - 可选参数（显式/隐式）：预期不抛出错误码，正常运行
- 测试目的：验证参数的可选性规则和错误码声明

#### 5.2.2 ArkTS-Static

| 参数类型 | null/undefined 测试 | 测试目标 | 测试预期 |
|---------|---------------------|---------|---------|
| 必填参数 | ❌ 无需生成 | 传入 null/undefined编译环节报错，无需测试| 编译环节报错 |
| 可选参数（显式） | ✅ 需要生成 | 验证传入 null/undefined 时不会抛出错误码，使用默认值 | 不抛出错误码，正常运行 |
| 可选参数（隐式） | ✅ 需要生成 | 验证传入 null/undefined 时调用旧版本重载 | 不抛出错误码，正常运行 |

**说明**：
- **必填参数**：ArkTS-Static 在编译环节进行类型检查，传入 `null/undefined` 会导致编译错误，无需生成运行时测试
- **可选参数**：仍需生成测试用例，验证使用默认值或调用重载的行为

**ArkTS-Static 类型校验特性**：
- 编译时对所有类型注解进行严格检查
- 函数参数类型必须与声明完全匹配
- 类型错误在编译阶段暴露，不会运行时抛出错误码
- 因此必填参数的 null/undefined 测试在编译环节拦截，无需生成用例

### 5.3 子系统特殊规则

**testfwk 子系统特殊规则**：
- testfwk 子系统字符串参数的特殊规则已在子系统配置文件中详细说明
- 配置位置：`references/subsystems/testfwk/_common.md`
- **空字符串规则**：testfwk 子系统的字符串参数，空字符串 `''` 是合法参数，不会抛出错误码 401
- 测试用例生成：只需要生成空字符串的合法参数测试用例，不生成 ERROR 测试用例
- 详细配置：参见 `testfwk/_common.md` 中的 `parameterRules` 和 `parameterTestingRules`

**关键要点**：
1. ✅ **必填参数**传入 null/undefined 时，**会抛出错误码**（错误码从 @throws 标记提取）
2. ✅ **可选参数（显式）**传入 null/undefined 时，**不会抛出错误码**，使用默认值
3. ✅ **可选参数（隐式）**传入 null/undefined 时，**不会抛出错误码**，调用旧版本重载
4. ✅ **可选参数（显式和隐式）都需要生成 null/undefined 测试用例**，但测试预期是**不会抛出错误码**
5. ✅ 可选参数有两种类型：显式（带 `?` 标记）和隐式（方法重载/API 版本演进）
6. ✅ testfwk 子系统的空字符串是合法参数，不会抛出错误码
7. ✅ **必须从 @throws 标记提取错误码**，不能假设所有参数错误都抛出 401

**测试用例生成原则**：
- **所有参数**（必填、可选）都需要生成 null/undefined 测试用例（ArkTS-Static 的必填参数除外）
- 必填参数：生成 null/undefined 测试（验证错误码，从 @throws 提取）
- 可选参数（显式/隐式）：生成 null/undefined 测试（验证不抛出错误码，使用默认值/调用重载）
- 数值参数：生成边界值测试
- testfwk 字符串参数：生成空字符串测试（合法参数）
- **从 @throws 提取实际错误码**，不要假设固定值

## 六、边界值测试规则

### 6.1 数值类型参数

对于 `number`、`int`、`double` 类型的参数，需要生成边界值测试。

**常见边界值**：
- 最小值：`0`
- 最大值：`2147483647`（int32 范围）
- 最小值 -1（如果允许负数）
- 最大值 +1（溢出测试）

**测试重点**：
- 最小值 `0` 是最常见的边界值测试

### 6.2 Point 类型参数

对于 `Point` 类型的参数（包含 x 和 y 坐标），需要测试坐标的边界值。

**示例**：
```typescript
// 测试最小坐标 (0, 0)
let point: Point = { x: 0, y: 0 };
await driver.swipeBetween(point, toPoint, speed);
```

---

## 七、参数类型识别表

| 参数类型 | 是否需要 null/undefined 测试 | 是否需要边界值测试 | 其他测试 |
|---------|---------------------------|---------------------|---------|
| 必填 - string | ✅ 是（抛出错误码） | ❌ 否 | 空字符串 '' 测试（testfwk） |
| 必填 - number/int/double | ✅ 是（抛出错误码） | ✅ 是（如 0） | - |
| 必填 - boolean | ✅ 是（抛出错误码） | ❌ 否 | - |
| 必填 - On/By/Point | ✅ 是（抛出错误码） | ⚠️ 可能（Point 的 0 坐标） | - |
| 必填 - InputTextMode | ✅ 是（抛出错误码） | ❌ 否 | - |
| 必填 - UiDirection | ✅ 是（抛出错误码） | ❌ 否 | - |
| 可选（显式）- 任意类型 | ✅ 是（验证不抛出错误码） | ✅ 是（测试可选参数功能） | - |
| 可选（隐式）- 任意类型 | ✅ 是（验证重载行为） | ✅ 是（测试新增参数功能） | - |

---

## 八、子系统特殊规则

- 详细配置：参见 `{subsystem}/_common.md` 中的 `parameterRules` 和 `parameterTestingRules`

**示例：testfwk 子系统特殊规则**：
- testfwk 子系统字符串参数的特殊规则已在子系统配置文件中详细说明
- 配置位置：`references/subsystems/testfwk/_common.md`
- **空字符串规则**：testfwk 子系统的字符串参数，空字符串 `''` 是合法参数，不会抛出错误码 401
- 测试用例生成：只需要生成空字符串的合法参数测试用例，不生成 ERROR 测试用例
- 详细配置：参见 `testfwk/_common.md` 中的 `parameterRules` 和 `parameterTestingRules`

### 示例1：Component.inputText()

**.d.ts 声明**：
```typescript
/**
 * @throws { BusinessError } 401 - Parameter error. Possible causes: 1. Mandatory parameters are left unspecified; 2. Incorrect parameter types; 3. Parameter verification failed.
 * @since 11 dynamic
 * @since 23 static
 */
// API 11
inputText(text: string): Promise<void>;

/**
 * @throws { BusinessError } 401 - Parameter error. Possible causes: 1. Mandatory parameters are left unspecified; 2. Incorrect parameter types; 3. Parameter verification failed.
 * @throws { BusinessError } 801 - Input text mode not supported.
 * @since 11 dynamic
 * @since 23 static
 */
// API 20
inputText(text: string, mode: InputTextMode): Promise<void>;
```

**参数分析**：
- `text`：必填参数（没有 ? 标记，且单参数版本也需要此参数）
- `mode`：**隐式可选参数**（存在单参数版本）
- **API 语法类型**：HYBRID（同时支持动态和静态）
- **错误码**：401（参数错误）、801（输入文本模式不支持）

**测试用例**：
1. `text` 传入 null：预期抛出 401 ✅
2. `text` 传入 undefined：预期抛出 401 ✅
3. `text` 传入空字符串 `''`：合法参数（testfwk 特殊规则）✅
4. `mode` 传入 null：**预期不抛出 401，调用单参数版本** ✅
5. `mode` 传入 undefined：**预期不抛出 401，调用单参数版本** ✅

### 示例2：Component.scrollSearch()

**.d.ts 声明**：
```typescript
/**
 * @throws { BusinessError } 401 - Parameter error.
 * @since 11 dynamic
 * @since 23 static
 */
scrollSearch(on: On, vertical?: boolean, offset?: number): Promise<Component>;
```

**参数分析**：
- `on`：必填参数（没有 ? 标记）
- `vertical`：显式可选参数（带 ? 标记）
- `offset`：显式可选参数（带 ? 标记）
- **API 语法类型**：HYBRID（同时支持动态和静态）
- **错误码**：401（参数错误）

**测试用例**：
1. `on` 传入 null：预期抛出 401 ✅
2. `on` 传入 undefined：预期抛出 401 ✅
3. `vertical` 传入 null：**预期不抛出 401（可选参数，使用默认值）** ✅
4. `offset` 传入 null：**预期不抛出 401（可选参数，使用默认值）** ✅
5. `offset` 传入 0：边界值测试 ✅

### 示例3：Driver.waitForComponent()

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

**参数分析**：
- `on`：必填参数（没有 ? 标记）
- `time`：必填参数（没有 ? 标记）
- **API 语法类型**：HYBRID（同时支持动态和静态）
- **错误码**：401（参数错误）、17000002（异步调用未使用 await）

**测试用例**：
1. `on` 传入 null：预期抛出 401 ✅
2. `on` 传入 undefined：预期抛出 401 ✅
3. `time` 传入 null：预期抛出 401 ✅
4. `time` 传入 undefined：预期抛出 401 ✅
5. `time` 传入 0：边界值测试 ✅

---

## 十、模块级测试用例生成

### 10.1 概述

支持批量解析整个模块的所有 API，为模块中的所有 API 生成测试用例。

### 10.2 模块识别方法

#### 10.2.1 从子系统配置获取模块映射

**配置位置**：`references/subsystems/{SubsystemName}/_common.md`

**配置格式**：
```markdown
### 1.3 模块映射配置

| 模块名称 | API 声明文件 | 主要 API | 说明 |
|---------|-------------|---------|------|
| **Component** | @ohos.UiTest.d.ts | Component, On, By | UI 组件 |
| **Driver** | @ohos.UiTest.d.ts | Driver, UiDriver | UI 驱动 |
```

### 10.3 模块级测试用例组织

#### 10.3.1 按类组织测试文件

```typescript
/**
 * Component 类测试
 */
describe('Component Test', () => {
  // 测试所有 Component 类的方法
  it('testInputText001', ...);
  it('testClick002', ...);
});

/**
 * Driver 类测试
 */
describe('Driver Test', () => {
  // 测试所有 Driver 类的方法
  it('testFindComponent001', ...);
  it('testDelayMs002', ...);
});
```

#### 10.3.2 按功能分组测试

```typescript
describe('UiTest Module Test', () => {
  // 组件操作组
  describe('Component Operations', () => {
    it('testClick001', ...);
    it('testInputText002', ...);
  });

  // 查找方法组
  describe('Component Finding', () => {
    it('testFindComponent001', ...);
    it('testFindComponents002', ...);
  });
});
```

## 十一、常见错误

### 错误1：为可选参数生成错误测试预期

**错误表现**：
```typescript
// ❌ 错误：可选参数传入null，预期抛出401
it('testOptionalParamNull', async () => {
  try {
    await (component as Component).method(param1, null)
    expect().assertFail();
  } catch (e) {
    expect(e.code).assertEqual(401); // ❌ 可选参数不应该抛出错误码
  }
});
```

**正确做法**：
```typescript
// ✅ 正确：可选参数传入null，预期不抛出错误码
it('testOptionalParamNull', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  console.log(`${TestTag}, testOptionalParamNull start`);
  await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility')
  await driver.delayMs(waitUiReadyMs)

  try {
    await (component as Component).method(param1, null)
    console.log('成功调用，使用默认值');
  } catch (e) {
    console.log('错误:', JSON.stringify(e));
    expect().assertFail(); // 可选参数不应该抛出错误
  }

  await stopApplication('com.uitestScene.acts')
  console.log(`${TestTag}, testOptionalParamNull end`);
});
```

### 错误2：忽略了可选参数的测试用例

**错误表现**：
```typescript
// ❌ 错误：可选参数不生成null/undefined测试
// mode是可选参数，应该生成测试用例
```

**正确做法**：
- 为所有可选参数（显式和隐式）生成 null/undefined 测试用例
- 测试预期：不会抛出错误码，正常运行/使用默认值/调用重载

### 错误3：未从 @throws 提取错误码

**错误表现**：
```typescript
// ❌ 错误：假设所有参数错误都抛出401
it('testMandatoryParamError', async () => {
  try {
    await component.method(null);
    expect().assertFail();
  } catch (e) {
    expect(e.code).assertEqual(401); // ❌ 未从 @throws 提取实际错误码
  }
});
```

**正确做法**：
```typescript
// ✅ 正确：从 @throws 标记提取实际错误码
// 假设 @throws { BusinessError } 17000007 - Invalid parameter value.
it('testMandatoryParamError', async () => {
  try {
    await component.method(null);
    expect().assertFail();
  } catch (e) {
    expect(e.code).assertEqual(17000007); // ✅ 使用提取的错误码
  }
});
```

### 错误4：ArkTS-Static 中为必填参数生成 null/undefined 测试

**错误表现**：
```typescript
// ❌ 错误：ArkTS-Static 中为必填参数生成 null 测试
// 会在编译阶段失败，无法运行
```

**正确做法**：
- ArkTS-Static 中不为必填参数生成 null/undefined 测试
- 仅对可选参数生成 null/undefined 测试
- 必填参数的类型错误在编译时检查

## 十二、参考文档

- **统一API解析器**: `modules/L2_Analysis/unified_api_parser.md`
- **API 解析器**: `modules/L2_Analysis/api_parser.md`
- **通用错误码**: `docs/en/application-dev/onlyfortest/reference/errorcode-universal.md`
- **testfwk 子系统配置**: `references/subsystems/testfwk/_common.md`
- **测试框架规范**: `modules/L1_Framework/hypium_framework.md`
- **ArkTS 静态语法规范**: `docs/ARKTS_STATIC_GUIDE.md`
- **项目解析器**: `modules/L2_Analysis/project_parser.md`
