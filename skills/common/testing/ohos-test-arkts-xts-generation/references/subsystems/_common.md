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

以下规范由 `references/conventions/` 下的文件定义，此处仅列出规则要点和来源，具体格式、示例和反模式请参见对应文件。

| 规则 | 要点 | 详细定义 |
|------|------|---------|
| 测试用例编号 | `SUB_[子系统]_[模块]_[API]_[类型]_[序号]`，全局唯一 | [test_conventions §1](../conventions/test_conventions.md#一测试用例编号规范) |
| it() 命名 | 小驼峰 camelCase，禁止大写下划线和特殊标点 | [test_conventions §2](../conventions/test_conventions.md#二测试用例命名规范) |
| it() 第二参数 | 必须包含 `Level.LEVEL*`，使用枚举形式 | [test_conventions §2](../conventions/test_conventions.md#二测试用例命名规范) |
| hypium 导入 | 从 `@ohos/hypium` 导入，按实际使用选择符号 | [hypium_framework §四](../conventions/hypium_framework.md#四导入语句规范) |
| @tc 注释块 | 每个it()前必须包含完整JSDoc，字段与it()参数一致 | [test_conventions §3](../conventions/test_conventions.md#三jsdoc-注释规范) |
| 断言方法 | 仅使用 Hypium 定义的23种方法，禁止编造 | [hypium_framework §二-三](../conventions/hypium_framework.md#二断言方法列表) |
| 测试级别/类型/粒度 | Level0-4, TestType, Size 的枚举值和含义 | [hypium_framework §五-七](../conventions/hypium_framework.md#五测试级别说明) |
| ETS 版本命名 | 目录名/bundleName/hap_name/用例名必须匹配 1.1/1.2/Interop 版本差异矩阵 | [ets_version_naming](../conventions/ets_version_naming.md) |
| 工程配置关联 | Test.json module-name="entry"，test-file-name=hap_name，BUILD.gn 模板函数匹配 ETS 版本 | [project_structure](../conventions/project_structure.md) |

---

## 三、核心默认规范（可覆盖）

测试级别（Level0-4）、测试类型（Function/Performance/Reliability/Security）、测试粒度（Small/Medium/LargeTest）的详细定义和枚举标识，见 [hypium_framework §五-七](../conventions/hypium_framework.md#五测试级别说明)。

### 3.1 默认 Kit 映射

```typescript
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