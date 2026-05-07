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

> **按需加载**: 当任务涉及 `arkts-dynamic` / `arkts-static` 语法类型时，加载 `unified_api_parser_syntax_filter.md`。
>
> 该文件包含：语法类型标识表、分类规则、TypeScript 接口（`APIInfoWithSyntax`）、过滤函数（`filterAPIsBySyntaxType`、`filterUncoveredItemsBySyntaxType`）、统计函数（`generateSyntaxSupportReport`）、验证函数（`validateTestCasesSyntaxType`）和使用示例。
>
> **语法类型判断算法**: 见 `api_parameter_optional_rules.md` 第四章。

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

