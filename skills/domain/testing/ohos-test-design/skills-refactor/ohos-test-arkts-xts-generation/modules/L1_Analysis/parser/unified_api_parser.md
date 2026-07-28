# 统一API信息解析器

> **模块信息**
> - 层级：L1_Analysis
> - 优先级：按需加载
> - 适用范围：API定义和文档的统一解析
> - 依赖：conventions
> - 整合模块：api_parser.md + doc_reader.md

---

## 一、模块概述

统一API信息解析器负责从多个来源整合API信息，包括：
- `.d.ts` 文件中的类型定义
- OpenHarmony官方文档中的API说明
- 已有测试用例中的使用模式
- 错误码和异常处理信息

通过统一解析，避免重复工作，提供一致的API信息视图。

---

## 二、信息来源与整合

### 2.1 信息来源优先级

```
1. .d.ts 文件（最高优先级）
   ├─ 接口定义
   ├─ 方法签名
   ├─ 参数类型
   ├─ 返回值类型
   ├─ @since 标记（API 语法类型）
   └─ @throws 标记（错误码）

2. 官方API文档
   ├─ 功能描述
   ├─ 使用示例
   ├─ 前置条件
   ├─ 注意事项
   └─ 兼容性信息

3. 已有测试用例
   ├─ 实际使用模式
   ├─ 代码风格
   ├─ 测试覆盖情况
   └─ 最佳实践

4. 子系统配置
   ├─ 特殊约定
   ├─ 测试路径
   ├─ 命名规范
   └─ 导入语句
```

### 2.2 信息整合流程

```
启动解析
     ↓
并行获取信息
     ├─ 解析 .d.ts 文件 → 类型定义信息、语法类型信息
     ├─ 读取官方文档 → 功能描述信息
     ├─ 分析已有测试 → 实际使用信息
     └─ 加载子系统配置 → 特殊约定信息
     ↓
信息合并与验证
     ├─ 冲突检测与解决
     ├─ 信息完整性验证
     ├─ 一致性检查
     └─ 缺失信息标记
     ↓
生成统一视图
     ├─ API完整定义
     ├─ API 语法类型（static/dynamic）
     ├─ 测试用例生成信息
     ├─ 错误码映射
     └─ 最佳实践建议
     ↓
输出解析结果
     └─ 结构化的API信息对象
```

---

## 三、API信息结构

解析过程产出以下关键数据结构，供后续 Phase 使用：

### 3.1 统一API信息对象（UnifiedAPIInfo）

每个 API 解析完成后，产出包含以下维度的信息对象：

| 维度 | 来源 | 关键字段 |
|------|------|---------|
| 基础信息 | .d.ts | name, namespace, module, since, deprecated |
| 语法类型 | @since 标签 | syntaxType（见 §4.1.1） |
| 接口定义 | .d.ts | methods（名称、参数、返回值、async、throws）, properties |
| 文档信息 | 官方文档 | 功能描述、使用示例、前置条件、注意事项 |
| 测试信息 | 已有测试 | 已覆盖方法、代码风格、使用模式 |
| 配置信息 | 子系统配置 | importPath, testPath, namingRules |
| 错误码 | @throws 标记 | errorCode, triggerCondition（见 §4.1.2） |

### 3.2 方法定义（MethodDefinition）

每个方法提取：name、parameters（名称+类型+可选性）、returnType、isAsync、throws（错误码列表）、syntaxType（可选，仅当方法级语法类型与接口级不同时）。

---

## 四、解析策略

### 4.1 .d.ts 文件解析

从 .d.ts 文件提取两类信息：**接口级**（接口名、继承、泛型、命名空间、@since、@deprecated）和**方法级**（方法名、参数列表、返回值、isAsync、@throws、@since）。

#### 4.1.1 API 语法类型解析

> **详细规则和算法**：参见 `api_parameter_optional_rules.md` 第四章

**规则概述**：
API 语法类型用于识别 API 支持的 ArkTS 语法类型（动态/静态），这是生成测试用例的重要依据。

**语法类型**：
- `DYNAMIC_ONLY`: 动态API独有（已废弃）
- `STATIC_ONLY`: 静态API独有
- `DYNAMIC`: 动态API（存在对应静态接口）
- `STATIC`: 静态API（存在对应动态接口）
- `HYBRID`: 动态API&静态API（同时支持）

**判断依据**：
从 `.d.ts` 文件最后一段 JSDOC 的 `@since` 标签提取。

#### 4.1.2 错误码提取策略

> **详细规则和算法**：参见 `api_parameter_optional_rules.md` 第三章

**规则概述**：
从 `.d.ts` 文件的 `@throws { BusinessError }` 标记中提取该 API 声明的错误码和触发条件。

**提取内容**：
- 错误码列表
- 每个错误码的触发条件
- 错误码相关的参数

**重要原则**：
- **必须从 jsdoc 中提取实际错误码**，不能假设所有参数错误都抛出 401（假设错误码会导致断言值与实际运行时错误码不匹配，测试必然 fail 且无法通过修改测试代码解决——必须使用正确的错误码）
- 不同 API 的错误码可能不同
- 错误码与触发条件需要精确对应



```typescript
// 从 @throws 标记提取错误码
interface ThrowDeclaration {
  errorCode: number;            // 错误码数字
  errorName: string;            // 错误名称
  triggerCondition: string;      // 触发条件
  description: string;          // 详细描述
}

// 提取示例
/**
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 401 - Parameter error. Possible causes: 1. Mandatory parameters are left unspecified; 2. Incorrect parameter types.
 * @throws { BusinessError } 10200010 - Container is empty.
 */
function popFirst(): T;

// 提取结果
const throwDeclarations: ThrowDeclaration[] = [
  {
    errorCode: 201,
    errorName: 'Permission denied',
    triggerCondition: 'Permission check failed',
    description: 'User does not have required permission'
  },
  {
    errorCode: 401,
    errorName: 'Parameter error',
    triggerCondition: 'Mandatory parameters are left unspecified or Incorrect parameter types',
    description: 'Parameter validation failed'
  },
  {
    errorCode: 10200010,
    errorName: 'Container is empty',
    triggerCondition: 'Container is empty',
    description: 'Cannot perform operation on empty container'
  }
];
```

### 4.2 官方文档路径解析

文档路径按子系统自动推导：

```
docs/zh-cn/application-dev/reference/apis-{subsystem}/{module}.md       # API参考
docs/zh-cn/application-dev/{subsystem}/{module}.md                     # 开发指南
docs/zh-cn/application-dev/reference/errorcode-{subsystem}.md          # 错误码
```

从官方文档提取：功能描述、使用示例、前置条件、权限要求、兼容性信息。

### 4.3 已有测试分析

扫描目标目录中的 `.test.ets` 文件，分析：已覆盖的 API 方法、代码风格（命名、导入、断言模式）、常用测试数据构造方式。

---

## 五、冲突解决策略

多来源信息不一致时的解决原则（按优先级）：

| 冲突类型 | 解决规则 | 原因 |
|----------|---------|------|
| 签名冲突（参数类型/返回值/方法缺失） | **.d.ts 优先** | .d.ts 是编译时的真实类型定义，文档可能滞后 |
| 文档冲突（描述/示例不一致） | **文档优先，测试补充** | 文档描述API意图，测试展示实际用法，两者结合最准确 |
| 配置冲突（导入路径/命名/测试路径） | **子系统配置优先** | 子系统配置是特定环境的实际规则，通用默认值可能不适用 |

**冲突处理流程**：
1. 检测冲突 → 记录冲突来源和内容
2. 按上述规则自动解决 → 无法自动解决则标记为 `manualReviewRequired`
3. 将所有冲突记录到解析结果的 `conflictReport` 中，Phase 10 输出时告知用户

---

## 六、输出格式

解析结果供 Phase 4（测试设计）和 Phase 5（测试生成）使用，关键输出字段：

| 输出字段 | 用途 | 消费阶段 |
|----------|------|---------|
| apiName, modulePath, importStatement | 确定被测API和导入语句 | Phase 5 |
| syntaxType | 判断生成动态/静态测试 | Phase 5 |
| methods[].parameters | 参数测试场景设计 | Phase 4, 5 |
| methods[].throws | 错误码测试场景设计 | Phase 4, 5 |
| methods[].returnType | 返回值测试场景设计 | Phase 4, 5 |
| configuration.testPath, suiteName | 测试文件路径和套件命名 | Phase 5, 6 |
| errorCodes | 错误码覆盖检查 | Phase 4, 9 |

---

## 七、API 语法类型过滤

> **按需加载**: 当任务涉及 `arkts-dynamic` / `arkts-static` 语法类型时，加载 `unified_api_parser_syntax_filter.md`。
>
> 该文件包含：语法类型标识表、分类规则、过滤函数（`filterAPIsBySyntaxType`、`filterUncoveredItemsBySyntaxType`）、统计函数（`generateSyntaxSupportReport`）、验证函数（`validateTestCasesSyntaxType`）和使用示例。
>
> **语法类型判断算法**: 见 `api_parameter_optional_rules.md` 第四章。

---

## 八、解析示例

以解析 TreeSet API 为例，展示解析流程和产出：

1. **读取 .d.ts** → 提取接口 `TreeSet<T>`，方法 `add`, `remove`, `getFirst`, `popFirst` 等
2. **提取 @throws** → `popFirst` 声明 `401`（参数错误）和 `10200010`（容器为空）
3. **提取 @since 语法类型** → `DYNAMIC`（仅动态语法可用）或 `HYBRID`（双语法可用）
4. **读取已有测试** → 发现 `add` 已有测试，`popFirst` 未覆盖
5. **读取子系统配置** → 路径 `test/xts/acts/utils/`，导入 `@kit.ArkTS`
6. **输出** → `apiName: "TreeSet"`, `methods: [...]`, `errorCodes: [...]`, `syntaxType: {...}`, `configuration: {...}`

