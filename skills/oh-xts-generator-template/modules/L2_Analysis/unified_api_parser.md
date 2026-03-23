# 统一API信息解析器

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载
> - 适用范围：API定义和文档的统一解析
> - 依赖：L1_Framework
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

### 3.1 统一API信息对象

```typescript
interface UnifiedAPIInfo {
  // 基础信息
  name: string;
  namespace: string;
  module: string;
  version: string;
  deprecated?: boolean;
  since: string;
  
  // API 语法类型（从 @since 标签解析）
  syntaxType: {
    type: 'DYNAMIC_ONLY' | 'STATIC_ONLY' | 'DYNAMIC' | 'STATIC' | 'HYBRID';
    description: string;
    compatible: ('dynamic' | 'static')[];
    sinceTags: string[];
  };
  
  // 接口定义（来自.d.ts）
  interface: {
    name: string;
    extends?: string[];
    generics?: string[];
    methods: MethodDefinition[];
    properties: PropertyDefinition[];
  };
  
  // 文档信息（来自官方文档）
  documentation: {
    description: string;
    usage: string[];
    prerequisites: string[];
    notes: string[];
    examples: CodeExample[];
    compatibility: CompatibilityInfo;
  };
  
  // 测试信息（来自已有测试）
  testing: {
    existingTests: TestCaseInfo[];
    coverage: CoverageInfo;
    codeStyle: CodeStyleInfo;
    commonPatterns: PatternInfo[];
  };
  
  // 配置信息（来自子系统配置）
  configuration: {
    importPath: string;
    testPath: string;
    namingRules: NamingRules;
    specialRules: SpecialRule[];
  };
  
  // 错误码信息（综合多个来源）
  errorCodes: ErrorCodeInfo[];
}
```

### 3.2 方法定义结构

```typescript
interface MethodDefinition {
  name: string;
  parameters: ParameterDefinition[];
  returnType: TypeDefinition;
  isAsync: boolean;
  visibility: 'public' | 'private' | 'protected';
  throws: ErrorCodeReference[];
  documentation: string;
  
  // API 语法类型（从 @since 标签解析）
  syntaxType?: {
    type: 'DYNAMIC_ONLY' | 'STATIC_ONLY' | 'DYNAMIC' | 'STATIC' | 'HYBRID';
    description: string;
    compatible: ('dynamic' | 'static')[];
    sinceTags: string[];
  };
}
```

---

## 四、解析策略

### 4.1 .d.ts 文件解析

#### 4.1.1 接口级别提取

```typescript
// 提取目标
interface ExtractionTargets {
  // 接口信息
  interfaceName: string;           // 接口名称
  extendsRelations: string[];       // 继承关系
  genericParameters: string[];      // 泛型参数
  namespace: string;              // 命名空间
  
  // 文档注释
  sinceVersion: string;           // @since 标记
  deprecationInfo: string;        // @deprecated 标记
  description: string;           // 描述信息

  // API 语法类型（从 @since 标签解析）
  syntaxType?: {
    type: 'DYNAMIC_ONLY' | 'STATIC_ONLY' | 'DYNAMIC' | 'STATIC' | 'HYBRID';
    description: string;
    compatible: ('dynamic' | 'static')[];
    sinceTags: string[];
  };
}
```

#### 4.1.2 方法级别提取

```typescript
// 提取内容
interface MethodExtraction {
  // 基础签名
  methodName: string;
  parameterList: Parameter[];
  returnType: TypeReference;
  isAsyncMethod: boolean;
  accessModifier: string;
  
  // 文档注释
  throwsDeclarations: ThrowDeclaration[];
  sinceVersion: string;
  methodDescription: string;
  
  // API 语法类型（从 @since 标签解析）
  syntaxType?: {
    type: 'DYNAMIC_ONLY' | 'STATIC_ONLY' | 'DYNAMIC' | 'STATIC' | 'HYBRID';
    description: string;
    compatible: ('dynamic' | 'static')[];
    sinceTags: string[];
  };
}
```

#### 4.1.3 API 语法类型解析

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

#### 4.1.4 错误码提取策略

> **详细规则和算法**：参见 `api_parameter_optional_rules.md` 第三章

**规则概述**：
从 `.d.ts` 文件的 `@throws { BusinessError }` 标记中提取该 API 声明的错误码和触发条件。

**提取内容**：
- 错误码列表
- 每个错误码的触发条件
- 错误码相关的参数

**重要原则**：
- **必须从 jsdoc 中提取实际错误码**，不能假设所有参数错误都抛出 401
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

### 4.2 官方文档解析

#### 4.2.1 文档位置识别

```typescript
// 文档路径映射
interface DocumentationPaths {
  apiReference: string;         // API参考文档路径
  developerGuide: string;       // 开发指南路径
  sampleCode: string;          // 示例代码路径
  errorCodes: string;          // 错误码文档路径
  compatibility: string;       // 兼容性文档路径
}

// 自动路径解析
function resolveDocumentationPaths(apiInfo: APIInfo): DocumentationPaths {
  const subsystem = apiInfo.subsystem;
  const moduleName = apiInfo.module;
  const apiName = apiInfo.name;
  
  return {
    apiReference: `docs/zh-cn/application-dev/reference/apis-${subsystem}/${moduleName}.md`,
    developerGuide: `docs/zh-cn/application-dev/${subsystem}/${moduleName}.md`,
    sampleCode: `docs/zh-cn/application-dev/${subsystem}/${moduleName}-example.md`,
    errorCodes: `docs/zh-cn/application-dev/reference/errorcode-${subsystem}.md`,
    compatibility: `docs/zh-cn/application-dev/reference/compatibility-${subsystem}.md`
  };
}
```

#### 4.2.2 文档内容提取

```typescript
// 提取目标
interface DocumentationExtraction {
  // 功能描述
  functionality: {
    purpose: string;
    features: string[];
    limitations: string[];
  };
  
  // 使用信息
  usage: {
    prerequisites: string[];
    permissions: string[];
    environment: string[];
  };
  
  // 示例代码
  examples: {
    basicExample: CodeBlock;
    advancedExample: CodeBlock;
    commonUseCases: CodeBlock[];
  };
  
  // 注意事项
  considerations: {
    performance: string[];
    security: string[];
    compatibility: string[];
    bestPractices: string[];
  };
}
```

### 4.3 测试用例分析

#### 4.3.1 现有测试扫描

```typescript
// 扫描策略
interface TestScanningStrategy {
  scanPaths: string[];          // 扫描路径
  filePatterns: string[];       // 文件模式
  exclusionPatterns: string[];   // 排除模式
  depth: number;               // 扫描深度
}

// 分析内容
interface TestAnalysis {
  // 测试覆盖
  coverage: {
    totalAPIs: number;
    testedAPIs: number;
    coveragePercentage: number;
    untestedAPIs: string[];
  };
  
  // 代码风格
  codeStyle: {
    namingConvention: NamingStyle;
    importPattern: ImportStyle;
    assertionPattern: AssertionStyle;
    errorHandlingStyle: ErrorHandlingStyle;
  };
  
  // 使用模式
  patterns: {
    commonSetup: CodePattern;
    commonTeardown: CodePattern;
    commonTestData: TestDataPattern;
    commonAssertions: AssertionPattern[];
  };
}
```

---

## 五、冲突解决策略

### 5.1 冲突类型识别

```typescript
interface ConflictType {
  // 签名冲突
  signatureConflict: {
    parameterTypeMismatch: string[];
    returnTypeMismatch: string[];
    methodMissing: string[];
    extraMethod: string[];
  };
  
  // 文档冲突
  documentationConflict: {
    descriptionMismatch: string[];
    requirementMismatch: string[];
    exampleMismatch: string[];
  };
  
  // 配置冲突
  configurationConflict: {
    importPathMismatch: string[];
    namingRuleConflict: string[];
    testPathConflict: string[];
  };
}
```

### 5.2 解决策略

```typescript
interface ConflictResolution {
  // 解决原则
  principles: {
    dtsOverridesDocs: boolean;      // .d.ts 优先于文档
    existingTestsOverrideNew: boolean; // 现有测试优先于新规范
    systemConfigOverridesDefault: boolean; // 系统配置优先于默认
  };
  
  // 解决方法
  resolutionMethods: {
    signatureConflicts: 'dts' | 'docs' | 'tests' | 'merge';
    documentationConflicts: 'docs' | 'tests' | 'combine';
    configurationConflicts: 'system' | 'user' | 'fallback';
  };
  
  // 冲突报告
  conflictReport: {
    detectedConflicts: ConflictType[];
    resolutions: ConflictResolution[];
    unresolvedConflicts: string[];
    manualReviewRequired: string[];
  };
}
```

---

## 六、输出格式

### 6.1 标准输出对象

```typescript
interface ParsedAPIOutput {
  // 元数据
  metadata: {
    version: string;
    timestamp: string;
    sources: string[];
    confidence: number;
  };
  
  // API信息
  api: {
    // 基础信息
    name: string;
    namespace: string;
    module: string;
    version: string;
    since: string;
    
    // API 语法类型
    syntaxType: {
      type: 'DYNAMIC_ONLY' | 'STATIC_ONLY' | 'DYNAMIC' | 'STATIC' | 'HYBRID';
      description: string;
      compatible: ('dynamic' | 'static')[];
      sinceTags: string[];
    };
    
    // 接口定义
    interface: {
      name: string;
      methods: MethodDefinition[];
      properties: PropertyDefinition[];
    };
    
    // 文档信息
    documentation: DocumentationInfo;
    
    // 测试信息
    testing: TestingInfo;
    
    // 错误码信息
    errorCodes: ErrorCodeInfo[];
  };
  
  // 质量指标
  quality: {
    completeness: number;        // 完整性分数
    consistency: number;        // 一致性分数
    reliability: number;        // 可靠性分数
  };
  
  // 建议
  recommendations: {
    testSuggestions: TestSuggestion[];
    documentationUpdates: DocumentationUpdate[];
    configurationChanges: ConfigurationChange[];
  };
}
```

### 6.2 测试用例生成友好格式

```typescript
interface TestGenerationInfo {
  // API基础信息
  apiName: string;
  modulePath: string;
  importStatement: string;
  
  // API 语法类型（用于确定生成静态或动态测试）
  syntaxType: {
    type: 'DYNAMIC_ONLY' | 'STATIC_ONLY' | 'DYNAMIC' | 'STATIC' | 'HYBRID';
    description: string;
    compatible: ('dynamic' | 'static')[];
  };
  
  // 测试生成信息
  testScenarios: TestScenario[];
  errorCodes: ErrorCodeTestInfo[];
  parameterTypes: ParameterTypeInfo[];
  returnTypeInfo: ReturnTypeInfo;
  
  // 样式信息
  codeStyle: {
    namingConvention: NamingStyle;
    importStyle: ImportStyle;
    assertionStyle: AssertionStyle;
  };
  
  // 配置信息
  testConfiguration: {
    testPath: string;
    fileName: string;
    suiteName: string;
  };
}
```

---

## 七、使用方式

### 7.1 基本使用

```typescript
// 创建解析器实例
const parser = new UnifiedAPIParser();

// 配置解析选项
const options: ParserOptions = {
  sources: ['dts', 'docs', 'tests', 'config'],
  conflictResolution: {
    dtsOverridesDocs: true,
    existingTestsOverrideNew: false
  },
  outputPath: './generated/api-info/'
};

// 执行解析
const result = await parser.parseAPI('TreeSet', options);

// 获取测试生成友好的信息
const testInfo = result.getTestGenerationInfo();
```

### 7.2 批量解析

```typescript
// 批量解析多个API
const batchResult = await parser.parseBatch([
  'TreeSet', 'ArrayList', 'HashMap'
], options);

// 获取覆盖率报告
const coverageReport = batchResult.getCoverageReport();

// 获取冲突报告
const conflictReport = batchResult.getConflictReport();
```

---

## 八、性能优化

### 8.1 缓存策略

```typescript
interface CacheStrategy {
  // 文件缓存
  fileCache: {
    dtsFiles: Map<string, ParsedDTS>;
    docFiles: Map<string, ParsedDocumentation>;
    testFiles: Map<string, ParsedTests>;
  };
  
  // 结果缓存
  resultCache: {
    apiInfo: Map<string, UnifiedAPIInfo>;
    testGenerationInfo: Map<string, TestGenerationInfo>;
  };
  
  // 缓存策略
  policy: {
    ttl: number;               // 生存时间
    maxSize: number;           // 最大缓存大小
    evictionPolicy: 'lru' | 'lfu' | 'fifo';
  };
}
```

### 8.2 并行处理

```typescript
// 并行解析策略
interface ParallelProcessing {
  // 文件级并行
  fileLevelParallelism: {
    dtsParsing: boolean;
    docParsing: boolean;
    testScanning: boolean;
  };
  
  // API级并行
  apiLevelParallelism: {
    batchProcessing: boolean;
    maxConcurrency: number;
  };
  
  // 信息合并并行
  mergeParallelism: {
    parallelMerge: boolean;
    dependencyResolution: boolean;
  };
}
```

---

## 九、错误处理

### 9.1 错误类型

```typescript
interface ParserErrorTypes {
  // 文件错误
  fileErrors: {
    fileNotFound: string[];
    fileParseError: string[];
    permissionDenied: string[];
  };
  
  // 解析错误
  parseErrors: {
    syntaxError: string[];
    typeError: string[];
    referenceError: string[];
  };
  
  // 冲突错误
  conflictErrors: {
    unresolvableConflict: string[];
    missingInformation: string[];
    inconsistentData: string[];
  };
}
```

### 9.2 错误恢复策略

```typescript
interface ErrorRecovery {
  // 恢复策略
  strategies: {
    skipMissingFiles: boolean;
    useDefaultValue: boolean;
    fallbackToAlternateSource: boolean;
    partialProcessing: boolean;
  };
  
  // 错误报告
  errorReporting: {
    logLevel: 'error' | 'warn' | 'info' | 'debug';
    includeStackTrace: boolean;
    generateErrorReport: boolean;
  };
}
```

---

## 十、最佳实践

### 10.1 解析顺序建议

1. **优先解析 .d.ts 文件**：获取最准确的类型定义
2. **补充文档信息**：增加功能描述和使用指导
3. **分析现有测试**：了解实际使用模式和代码风格
4. **应用系统配置**：确保符合特定环境和约定
5. **冲突检测与解决**：处理不一致的信息
6. **质量验证**：确保解析结果的完整性和一致性

### 10.2 质量保证

- **完整性检查**：确保所有必要信息都已提取
- **一致性验证**：检查不同来源信息的一致性
- **准确性验证**：验证解析结果的正确性
- **性能监控**：监控解析过程的性能指标

### 10.3 维护建议

- **定期更新**：保持解析器与最新API文档同步
- **缓存管理**：合理管理解析结果缓存
- **错误监控**：监控和记录解析错误
- **性能优化**：持续优化解析性能

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
| 过滤工具 | `./modules/L2_Analysis/api_syntax_filter.ts` | 提供语法类型过滤函数 |

---

## 十一、示例

### 11.1 完整解析示例

```typescript
// 解析 TreeSet API
const treeSetInfo = await parser.parseAPI('TreeSet', {
  sources: ['dts', 'docs', 'tests'],
  subsystem: 'Utils',
  module: 'util'
});

// 输出结果
console.log('API名称:', treeSetInfo.name);
console.log('方法数量:', treeSetInfo.interface.methods.length);
console.log('错误码数量:', treeSetInfo.errorCodes.length);
console.log('测试覆盖率:', treeSetInfo.testing.coverage.percentage);
```

### 11.2 测试生成信息提取示例

```typescript
// 获取测试生成信息
const testInfo = treeSetInfo.getTestGenerationInfo();

// 生成参数测试
testInfo.testScenarios
  .filter(scenario => scenario.type === 'parameter')
  .forEach(scenario => {
    console.log(`生成参数测试: ${scenario.description}`);
  });

// 生成错误码测试
testInfo.errorCodes
  .forEach(errorCode => {
    console.log(`生成错误码测试: ${errorCode.code} - ${errorCode.description}`);
  });
```

---

**版本**: 1.3.1
**更新内容**: 新增第十章的交叉引用，指向 api_parameter_optional_rules.md 的 API 语法类型快速参考章节

---

## 十、API 语法类型过滤

> 📘 **快速参考**：API 语法类型识别、过滤和验证的快速参考和交叉索引请参阅 [api_parameter_optional_rules.md 第八章：API 语法类型快速参考](# 八、api-语法类型快速参考)

---


**创建日期**: 2026-02-05
**更新日期**: 2026-03-03
**基于**: api_parser.md v4.0.0 + doc_reader.md v1.0.0
**更新内容**: 新增第十章"API 语法类型过滤"，集成语法类型提取、过滤和验证功能
**更新内容**: 移除与 api_parameter_optional_rules.md 重复的规则内容，通过引用指向详细规则
