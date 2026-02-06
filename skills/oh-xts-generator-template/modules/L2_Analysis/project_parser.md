# 工程配置解析器

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载
> - 适用范围：工程配置解析和识别
> - 依赖：L1_Framework
> - 相关模块：build_workflow.md（BUILD.gn 配置和编译流程）

---

## 一、模块概述

工程配置解析器用于识别 OpenHarmony 测试工程的配置信息，包括工程语法类型、测试路径、依赖关系等。

### 1.1 核心功能

- **工程语法类型识别**：识别工程使用的是静态语法还是动态语法
- **工程结构识别**：识别工程的目录结构和组织方式
- **配置文件解析**：解析 build-profile.json5 等配置文件
- **工程信息提取**：提取子系统名称、部件名称、测试套名称等

### 1.2 应用场景

1. 生成测试用例前，需要识别工程的语法类型
2. 分析现有测试工程的结构和配置
3. 确定测试文件的存放位置
4. 识别工程依赖关系

### 1.3 与其他模块的关系

- **build_workflow.md**：BUILD.gn 配置和编译流程的详细指导
- **api_parser.md**：API 类型判断与工程类型匹配

---

## 二、工程语法类型识别

### 2.1 概述

OpenHarmony 支持两种 ArkTS 语法类型：
- **静态语法 (ArkTS-Sta)**：编译时静态链接，性能更好，API 23+ 支持
- **动态语法 (ArkTS-Dyn)**：运行时动态加载，兼容性更好，早期 API 支持

识别工程语法类型对于生成正确的测试用例至关重要。

### 2.2 识别方法

**关键配置文件**：工程根目录下的 `build-profile.json5`

**位置**：
```
{工程根目录}/build-profile.json5
```

### 2.3 判断规则

读取 `build-profile.json5` 文件，检查 `arkTSVersion` 字段：

```json5
{
  "app": {
    "products": [
      {
        "name": "default",
        "compileSdkVersion": "23",
        "compatibleSdkVersion": "16",
        "arkTSVersion": "1.2",        // ← 静态语法标识
        "runtimeOS": "OpenHarmony"
      }
    ]
  }
}
```

| 配置项 | 工程类型 | 说明 |
|--------|---------|------|
| 存在 `"arkTSVersion": "1.2"` | **静态语法工程** | 使用 ArkTS 静态语法 |
| 不存在 `arkTSVersion` 字段 | **动态语法工程** | 使用 ArkTS 动态语法 |
| `arkTSVersion` 为其他值 | 需进一步确认 | 可能是实验性语法或配置错误 |

### 2.4 解析算法

```javascript
/**
 * 识别工程的语法类型
 * @param {string} projectPath - 工程根目录路径
 * @returns {object} - { type: string, description: string, config: object }
 */
function identifyProjectSyntax(projectPath) {
  const configPath = `${projectPath}/build-profile.json5`;

  try {
    const config = readJsonFile(configPath);
    const products = config.app?.products || [];

    if (products.length === 0) {
      return {
        type: 'UNKNOWN',
        description: '无法确定：无产品配置',
        config: null
      };
    }

    // 检查第一个产品的 arkTSVersion 配置
    const firstProduct = products[0];

    if (firstProduct.arkTSVersion === '1.2') {
      return {
        type: 'STATIC',
        description: '静态语法工程（arkTSVersion: 1.2）',
        config: firstProduct
      };
    }

    // 不存在 arkTSVersion 字段或值不是 '1.2'
    return {
      type: 'DYNAMIC',
      description: '动态语法工程（无 arkTSVersion 配置）',
      config: firstProduct
    };

  } catch (error) {
    return {
      type: 'ERROR',
      description: `读取配置文件失败: ${error.message}`,
      config: null
    };
  }
}
```

### 2.5 实际示例

#### 示例 1：静态语法工程

**文件**：`test/xts/acts/testfwk/uitestStatic/build-profile.json5`

```json5
{
  "app": {
    "products": [
      {
        "name": "default",
        "compatibleSdkVersion": "20",
        "compileSdkVersion": "23",
        "arkTSVersion": "1.2",        // ← 静态语法
        "runtimeOS": "OpenHarmony"
      }
    ]
  }
}
```

**解析结果**：
```javascript
{
  type: 'STATIC',
  description: '静态语法工程（arkTSVersion: 1.2）',
  config: { /* ... */ }
}
```

#### 示例 2：动态语法工程

**文件**：`test/xts/acts/testfwk/uitest/build-profile.json5`

```json5
{
  "app": {
    "products": [
      {
        "name": "default",
        "compileSdkVersion": "23",
        "compatibleSdkVersion": "16",
        // ← 无 arkTSVersion 字段
        "runtimeOS": "OpenHarmony"
      }
    ]
  }
}
```

**解析结果**：
```javascript
{
  type: 'DYNAMIC',
  description: '动态语法工程（无 arkTSVersion 配置）',
  config: { /* ... */ }
}
```

### 2.6 解析输出

工程语法类型识别结果应包含以下信息：

```typescript
{
  "project_path": "/path/to/project",
  "syntax_type": {
    "type": "STATIC",  // 或 "DYNAMIC", "UNKNOWN", "ERROR"
    "description": "静态语法工程（arkTSVersion: 1.2）",
    "config": {
      "compileSdkVersion": "23",
      "compatibleSdkVersion": "16",
      "arkTSVersion": "1.2"
    }
  }
}
```

---

## 三、测试用例生成策略

根据工程语法类型和 API 类型，选择相应的测试用例生成策略：

### 3.1 兼容性矩阵

| 工程类型 | API类型 | 生成策略 | 文件命名 | 用例命名 |
|---------|---------|---------|---------|---------|
| 静态语法工程 | 静态API | ✅ 直接生成 | 原始文件名 | 原始用例名 + `_static` |
| 静态语法工程 | 动态API | ⚠️ 不兼容 | - | - |
| 静态语法工程 | 混合API | ✅ 生成静态调用方式 | 原始文件名 | 原始用例名 + `_static` |
| 动态语法工程 | 动态API | ✅ 直接生成 | 原始文件名 | 原始用例名 |
| 动态语法工程 | 静态API | ⚠️ 不兼容 | - | - |
| 动态语法工程 | 混合API | ✅ 生成动态调用方式 | 原始文件名 | 原始用例名 |

**说明**：
- ✅ 兼容：可以生成测试用例
- ⚠️ 不兼容：API 类型与工程类型不匹配，需提示用户或跳过

### 3.2 文件命名规则详解

#### 3.2.1 动态语法工程

```typescript
// 文件命名
uitest.test.ets          // 保持原始文件名

// 用例命名
it('testWakeUpDisplay', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  // 测试代码
});
```

#### 3.2.2 静态语法工程

```typescript
// 文件命名
uitest.test.ets          // 保持原始文件名（无 _static 后缀）

// 用例命名
it('testWakeUpDisplay_static', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  // 测试代码
});
```

**重要说明**：
- 静态语法工程的 **ets 文件名** 不需要添加 `_static` 后缀
- 仅在 **it() 中的用例名** 后添加 `_static` 后缀
- 这与 XTS 测试框架的约定一致

### 3.3 兼容性检查流程

```javascript
/**
 * 检查 API 类型与工程类型是否兼容
 * @param {string} apiType - API 类型（从 api_parser 获取）
 * @param {string} projectType - 工程类型（从本模块获取）
 * @returns {object} - { compatible: boolean, strategy: string, message: string }
 */
function checkCompatibility(apiType, projectType) {
  const compatibilityMatrix = {
    'STATIC_ONLY': {
      'STATIC': { compatible: true, strategy: '直接生成' },
      'DYNAMIC': { compatible: false, strategy: '不兼容', message: '静态API仅支持静态语法工程' }
    },
    'DYNAMIC_ONLY': {
      'DYNAMIC': { compatible: true, strategy: '直接生成' },
      'STATIC': { compatible: false, strategy: '不兼容', message: '动态API仅支持动态语法工程' }
    },
    'HYBRID': {
      'STATIC': { compatible: true, strategy: '生成静态调用方式' },
      'DYNAMIC': { compatible: true, strategy: '生成动态调用方式' }
    }
  };

  return compatibilityMatrix[apiType]?.[projectType] || {
    compatible: false,
    strategy: '未知',
    message: '未知的 API 或工程类型'
  };
}
```

---

## 四、工程结构识别

### 4.1 目录结构识别

标准的 XTS 测试工程目录结构：

```
{测试套名}/
├── entry/                    # 主测试工程
│   ├── src/
│   │   └── main/
│   │       ├── ets/
│   │       │   ├── test/     # 测试用例目录
│   │       │   │   ├── List.test.ets
│   │       │   │   ├── Types.test.ets
│   │       │   │   └── Util.test.ets
│   │       │   └── ...
│   │       └── resources/
│   ├── build-profile.json5   # 工程配置
│   └── BUILD.gn              # 编译配置
└── {测试套名}Scene/          # 辅助工程（可选）
    └── ...
```

### 4.2 关键文件识别

| 文件 | 作用 | 提取信息 |
|------|------|---------|
| `build-profile.json5` | 工程配置 | 语法类型、SDK 版本 |
| `BUILD.gn` | 编译配置 | 测试套名、依赖关系 |
| `module.json5` 或 `config.json` | 模块配置 | Bundle 名称、权限 |
| `List.test.ets` | 测试列表 | 已注册的测试文件 |

### 4.3 工程信息提取

```javascript
/**
 * 提取工程关键信息
 * @param {string} projectPath - 工程根目录
 * @returns {object} - 工程信息对象
 */
function extractProjectInfo(projectPath) {
  const buildProfilePath = `${projectPath}/entry/build-profile.json5`;
  const buildGnPath = `${projectPath}/entry/BUILD.gn`;

  const result = {
    project_path: projectPath,
    syntax_type: null,
    test_suite_name: null,
    subsystem_name: null,
    part_name: null,
    bundle_name: null,
    test_entry: {
      test_dir: 'entry/src/main/ets/test',
      list_file: 'entry/src/main/ets/test/List.test.ets'
    }
  };

  // 读取 build-profile.json5
  const profile = readJsonFile(buildProfilePath);
  result.syntax_type = identifyProjectSyntax(projectPath);

  // 解析 BUILD.gn 提取测试套名
  const buildGnContent = readFile(buildGnPath);
  const match = buildGnContent.match(/ohos_js_app_suite\("([^"]+)"\)/);
  if (match) {
    result.test_suite_name = match[1];
  }

  // 提取 subsystem_name 和 part_name
  const subsystemMatch = buildGnContent.match(/subsystem_name\s*=\s*"([^"]+)"/);
  const partMatch = buildGnContent.match(/part_name\s*=\s*"([^"]+)"/);

  if (subsystemMatch) result.subsystem_name = subsystemMatch[1];
  if (partMatch) result.part_name = partMatch[1];

  return result;
}
```

---

## 五、解析输出格式

### 5.1 完整的工程配置信息

```typescript
{
  "project": {
    "path": "/path/to/project",
    "name": "ActsUiTest",
    "syntax_type": {
      "type": "DYNAMIC",
      "description": "动态语法工程（无 arkTSVersion 配置）"
    }
  },
  "build_config": {
    "test_suite_name": "ActsUiTest",
    "part_name": "arkxtest",
    "subsystem_name": "testfwk"
  },
  "test_entry": {
    "test_dir": "entry/src/main/ets/test",
    "list_file": "entry/src/main/ets/test/List.test.ets"
  }
}
```

### 5.2 用于测试生成

解析结果将用于：
1. 确定测试用例的命名规则（静态 vs 动态）
2. 检查 API 与工程的兼容性
3. 生成正确的测试文件路径
4. 识别辅助工程的依赖关系

---

## 六、与 API 解析的配合使用

### 6.1 兼容性检查流程

```
步骤1：解析 API 类型
  ↓
  使用 api_parser.md
  ↓
  输出：{ type: 'HYBRID', compatible: ['dynamic', 'static'] }
  ↓
步骤2：解析工程类型
  ↓
  使用 project_parser.md
  ↓
  输出：{ type: 'STATIC', description: '静态语法工程' }
  ↓
步骤3：兼容性匹配
  ↓
  检查：'STATIC' 是否在 ['dynamic', 'static'] 中
  ↓
  结果：✅ 兼容，生成静态调用方式的测试用例
```

### 6.2 完整解析示例

```javascript
// 步骤1：解析 API
const apiInfo = parseApiSyntaxType(['@since 11 dynamic', '@since 23 static']);
// apiInfo = { type: 'HYBRID', compatible: ['dynamic', 'static'] }

// 步骤2：解析工程
const projectInfo = identifyProjectSyntax('/path/to/project');
// projectInfo = { type: 'STATIC', description: '静态语法工程' }

// 步骤3：兼容性检查
const compatibility = checkCompatibility(apiInfo.type, projectInfo.type);
// compatibility = { compatible: true, strategy: '生成静态调用方式' }

// 步骤4：生成测试用例
if (compatibility.compatible) {
  generateTestCases({
    naming: {
      file: 'original.test.ets',
      testCase: 'testCaseName_static'
    },
    calling: 'static'
  });
}
```

---

## 七、常见问题

### 7.1 如何处理未知类型的工程？

**问题**：`build-profile.json5` 中既没有 `arkTSVersion`，也无法确定为动态语法工程

**处理**：
```javascript
if (projectInfo.type === 'UNKNOWN') {
  // 尝试其他识别方法
  // 1. 检查测试用例文件的命名（是否包含 _static 后缀）
  // 2. 检查参考历史用例
  // 3. 询问用户确认
}
```

### 7.2 如何处理多个 product 配置？

**问题**：`app.products` 数组中有多个配置项

**处理**：通常检查第一个产品配置即可。如果需要更精确的判断，可以：
1. 检查所有产品的 `arkTSVersion` 是否一致
2. 询问用户选择使用哪个配置

### 7.3 如何识别辅助工程的类型？

**方法**：
1. 检查 BUILD.gn 中的构建类型（`ohos_app_assist_suite` vs `ohos_js_app_suite`）
2. 检查目录名称是否包含 `Scene` 后缀
3. 检查是否存在 UI 组件和界面

---

## 八、参考路径

### 8.1 参考示例

| 工程类型 | 参考路径 | 说明 |
|---------|---------|------|
| 静态语法工程 | `${OH_ROOT}/test/xts/acts/testfwk/uitestStatic` | 静态语法 UI 测试工程 |
| 动态语法工程 | `${OH_ROOT}/test/xts/acts/testfwk/uitest` | 动态语法 UI 测试工程 |

### 8.2 参考文档

- **BUILD.gN 配置和编译流程**：`modules/L2_Analysis/build_workflow.md`
- **通用配置**：`references/subsystems/_common.md`

---

## 九、版本历史

- **v1.1.0** (2025-01-31):
  - **重构**：将 BUILD.gn 配置解析、辅助工程识别、编译命令等内容移至 build_workflow.md
  - **优化**：专注于工程配置解析，包括语法类型识别、工程结构识别、配置信息提取
  - **改进**：明确与 build_workflow.md 的职责划分
- **v1.0.0** (2025-01-31): 初始版本，定义工程配置解析器的完整功能
