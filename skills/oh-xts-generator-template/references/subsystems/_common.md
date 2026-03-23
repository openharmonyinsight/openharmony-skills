# 核心配置系统

> **适用范围**: 所有子系统
> **版本**: 2.0.0
> **更新日期**: 2026-02-05
> **设计原则**: 核心配置 + 最小化差异化

---

## 一、配置架构

### 1.1 配置层级

```
核心配置 (_common.md)
├─ 强制规范（不可覆盖）
├─ 默认规范（可覆盖）
└─ 扩展接口（子系统扩展）

子系统配置 ({Subsystem}/_common.md）
├─ 基础信息（必须）
├─ 子系统差异化配置（仅覆盖不同部分）
└─ 特殊规则（仅子系统特有）

模块配置 ({Subsystem}/{Module}.md）
├─ 基础信息（必须）
├─ 模块差异化配置（仅覆盖不同部分）
└─ 特殊规则（仅模块特有）
```

### 1.2 配置优先级

```
用户自定义配置 > 子系统配置 > 核心配置
```

**特殊规则**：核心强制规范不可被任何层级覆盖

---

## 二、核心强制规范（不可覆盖）

### 2.1 测试用例编号格式

```
格式: SUB_[子系统]_[模块]_[API]_[类型]_[序号]

类型标识：
- PARAM    参数测试
- ERROR    错误码测试
- RETURN   返回值测试
- BOUNDARY 边界值测试
- EVENT    事件测试（仅ArkUI）

示例：
SUB_UTILS_UTIL_TREESET_ADD_PARAM_001
SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_401_001
SUB_ARKUI_BUTTON_ONCLICK_EVENT_001
```

### 2.2 命名强制规范

#### it() 函数第一个参数（用例名称）
- ✅ **必须使用小驼峰命名（camelCase）**
- ❌ **禁止使用大写下划线命名**
- ❌ **禁止使用特殊标点符号**（如 `[]`、`.` 等）

#### it() 函数第二个参数（测试类型）
- ✅ **必须使用**：`TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3`
- ❌ **禁止使用**：`0` 或其他简写形式

### 2.3 hypium 导入规范（强制）

详见：[Hypium 测试框架基础 - 导入语句规范](../modules/L1_Framework/hypium_framework.md#四导入语句规范)

### 2.4 @tc 注释块规范（强制）

- `@tc.name`：必须使用小驼峰命名，必须与 `it()` 第一个参数完全一致
- `@tc.number`：格式为 `{describe名}_{序号}`，序号从001开始补零对齐
- `@tc.desc`：格式为 `{API名} {错误码/场景} test.`，必须以 `. ` 结尾
- `@tc.type`、`@tc.size`、`@tc.level`：必须与 `it()` 第二个参数中的值一致

---

## 三、核心默认规范（可覆盖）

### 3.1 测试级别定义

| 级别 | 名称 | 说明 | 适用场景 |
|-----|------|------|---------|
| Level0 | 冒烟测试 | 基本功能验证 | 核心API的基本功能 |
| Level1 | 基础测试 | 常用输入场景 | 常用参数组合 |
| Level2 | 主要测试 | 常用+错误场景 | 正常+异常场景 |
| Level3 | 常规测试 | 所有功能 | 完整功能覆盖 |
| Level4 | 罕见测试 | 极端场景 | 边界值、极端输入 |

### 3.2 测试类型定义

| 类型 | 说明 | 标识 |
|-----|------|------|
| Function | 功能测试 | TestType.FUNCTION |
| Performance | 性能测试 | TestType.PERFORMANCE |
| Reliability | 可靠性测试 | TestType.RELIABILITY |
| Security | 安全测试 | TestType.SECURITY |

### 3.3 测试粒度定义

| 粒度 | 说明 | 执行时间 | 标识 |
|-----|------|---------|------|
| SmallTest | 小型测试 | < 5秒 | Size.SMALLTEST |
| MediumTest | 中型测试 | 5-30秒 | Size.MEDIUMTEST |
| LargeTest | 大型测试 | > 30秒 | Size.LARGETEST |

### 3.4 默认 Kit 映射

```typescript
// 默认导入映射
import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';

import {APIName} from '@kit.BaseKitName';

```

---

## 四、子系统配置接口

### 4.1 基础信息结构

```typescript
interface SubsystemBasicInfo {
  // 必须字段
  name: string;                 // 子系统名称
  kitPackage: string;           // Kit包名
  testPath: string;             // 测试路径
  apiDeclarationPath: string;    // API声明路径
  documentationPath: string;    // 文档路径
  
  // 可选字段
  version?: string;
  apiType?: 'dynamic' | 'static' | 'dynamic&static';
  specialRequirements?: string[];
}
```

### 4.2 差异化配置结构

```typescript
interface DifferentialConfig {
  // 路径差异化
  paths?: {
    testPath?: string;
    apiPath?: string;
    docPath?: string;
  };
  
  // 命名差异化
  naming?: {
    testFilePattern?: string;
    testSuitePattern?: string;
    apiNaming?: NamingRule;
  };
  
  // 导入差异化
  imports?: {
    kitPackage?: string;
    additionalImports?: string[];
    conditionalImports?: string[];
  };
  
  // 特殊规则
  specialRules?: {
    testTypeExtensions?: string[];    // 额外的测试类型
    namingExtensions?: NamingRule[];  // 额外的命名规则
    apiSpecific?: APISpecificRule[];  // API特定规则
  };
}
```

### 4.3 配置文件模板

```markdown
# {子系统名称} 配置

> **版本**: {版本号}
> **更新日期**: {日期}
> **基于核心配置**: _common.md v2.0.0

---

## 一、基础信息

```json
{
  "name": "{子系统名称}",
  "kitPackage": "@kit.{Kit名}",
  "testPath": "{测试路径}",
  "apiDeclarationPath": "{API声明路径}",
  "documentationPath": "{文档路径}",
  "apiType": "dynamic|static|dynamic&static"
}
```

---

## 二、差异化配置

### 2.1 路径差异化

```json
{
  "paths": {
    "testPath": "{自定义测试路径}",
    "apiPath": "{自定义API路径}",
    "docPath": "{自定义文档路径}"
  }
}
```

### 2.2 导入差异化

```json
{
  "imports": {
    "kitPackage": "@kit.{自定义Kit名}",
    "additionalImports": ["{额外导入}"],
    "conditionalImports": ["{条件导入}"]
  }
}
```

### 2.3 特殊规则

```json
{
  "specialRules": {
    "testTypeExtensions": ["{扩展测试类型}"],
    "namingExtensions": [
      {
        "type": "文件命名",
        "rule": "{规则描述}",
        "example": "{示例}"
      }
    ],
    "apiSpecific": [
      {
        "api": "{API名称}",
        "rule": "{特定规则}",
        "description": "{规则说明}"
      }
    ]
  }
}
```

---

## 三、API映射表（可选）

### 3.1 Kit组件映射

| API名称 | Kit导入 | 组件路径 | 说明 |
|---------|---------|----------|------|
| {API1} | @kit.{Kit} | {路径} | {说明} |
| {API2} | @kit.{Kit} | {路径} | {说明} |

### 3.2 测试套映射

| 功能模块 | 测试套名称 | 测试文件路径 | 说明 |
|---------|-----------|-------------|------|
| {模块1} | {套件名} | {文件路径} | {说明} |
| {模块2} | {套件名} | {文件路径} | {说明} |

---

## 四、使用示例

```typescript
// 使用子系统配置生成测试用例
const config = loadSubsystemConfig('ArkUI');
const testGenerator = new TestGenerator(config);

// 生成测试用例
const testCases = testGenerator.generate('Component.onClick', {
  testType: ['PARAM', 'ERROR', 'EVENT'],
  level: ['Level1', 'Level2']
});
```

---

## 五、配置验证

### 5.1 必须验证项目

- [ ] 基础信息完整性
- [ ] 路径有效性
- [ ] 导入语句正确性
- [ ] 命名规范一致性
- [ ] 特殊规则合法性

### 5.2 验证结果

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "suggestions": []
}
```