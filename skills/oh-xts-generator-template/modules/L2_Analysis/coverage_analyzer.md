# 测试覆盖率分析器

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载
> - 适用范围：测试覆盖分析
> - 依赖：L1_Framework, L2_Analysis/api_parser.md

---

## 一、模块概述

测试覆盖率分析器用于分析现有测试文件，识别已覆盖和未覆盖的 API，计算测试覆盖率，为补充测试用例提供依据。

---

## 二、分析目标

### 2.1 测试套件信息

- describe 块名称
- 测试函数（it）列表
- 测试级别分布

### 2.2 API 覆盖信息

- 已测试的方法列表
- 已测试的参数组合
- 已测试的错误码
- 已测试的边界值

### 2.3 测试模式识别

- 参数测试模式
- 错误码测试模式
- 返回值测试模式
- 边界值测试模式

---

## 三、分析步骤

### 3.1 定位测试文件

```bash
# 测试文件通常位于
${OH_ROOT}/test/xts/acts/

# 示例路径
test/xts/acts/util/test/TreeSet.test.ets
test/xts/acts/network/test/Http.test.ets
```

### 3.2 提取测试用例信息

使用 Grep 工具搜索测试文件中的模式：

```bash
# 搜索所有 it 函数
grep -r "it(" test/ --include="*.test.ets"

# 搜索特定 API 的测试
grep -r "TreeSet" test/ --include="*.test.ets"
```

### 3.3 构建测试覆盖图谱

```json
{
  "api": "TreeSet",
  "test_file": "test/xts/acts/util/test/TreeSet.test.ets",
  "methods": {
    "add": {
      "tested_scenarios": ["normal", "null", "undefined"],
      "tested_param_types": ["number", "string"],
      "tested_error_codes": [],
      "coverage": "partial"
    },
    "popFirst": {
      "tested_scenarios": ["empty_container"],
      "tested_error_codes": [401],
      "coverage": "full"
    },
    "getLast": {
      "tested_scenarios": [],
      "tested_error_codes": [],
      "coverage": "none"
    }
  },
  "overall_coverage": "60%"
}
```

---

## 四、测试模式识别

### 4.1 命名模式识别

| 测试类型 | 命名模式 | 示例 |
|---------|---------|------|
| 正常值测试 | `{method}{scenario}00[1-9]` | `addNormal001` |
| null 测试 | `{method}Null00[1-9]` | `addNull001` |
| undefined 测试 | `{method}Undefined00[1-9]` | `addUndefined001` |
| 边界值测试 | `{method}Boundary00[1-9]` | `addBoundary001` |
| 错误码测试 | `{method}Error{code}00[1-9]` | `popFirstError401001` |

### 4.2 describe 块识别

```typescript
// 参数测试
describe('TreeSetParameterTest', () => {})
describe('ParameterTest', () => {})

// 错误码测试
describe('TreeSetErrorCodeTest', () => {})
describe('ErrorCodeTest', () => {})

// 返回值测试
describe('TreeSetReturnValueTest', () => {})
describe('ReturnValueTest', () => {})
```

---

## 五、覆盖率计算方法

### 5.1 方法覆盖率

```typescript
已测试方法数 / 总方法数 × 100%

示例:
TreeSet 有 10 个方法，测试了 8 个
方法覆盖率 = 8/10 × 100% = 80%
```

### 5.2 参数场景覆盖率

```typescript
已测试参数场景 / 应测试参数场景 × 100%

示例:
add(value: T) 应测试: 正常值、null、undefined、边界值
实际测试: 正常值、null
参数覆盖率 = 2/4 × 100% = 50%
```

### 5.3 错误码覆盖率

```typescript
已测试错误码数 / 总错误码数 × 100%

示例:
popFirst() 有错误码: 401, 402
实际测试: 401
错误码覆盖率 = 1/2 × 100% = 50%
```

---

## 六、差距识别规则

### 6.1 完全未测试

```
条件: API 方法在测试文件中从未被调用
```

### 6.2 部分测试

```
条件: API 方法被调用，但缺少某些参数场景
- 缺少 null/undefined 测试
- 缺少边界值测试
- 缺少某些错误码测试
```

### 6.3 测试不完整

```
条件: 测试用例存在但不完整
- 有测试但没有断言
- 只有正向测试，缺少负向测试
- 断言方法使用不当
```

---

## 七、分析输出格式

### 7.1 覆盖率报告

```markdown
# API 测试覆盖率报告

## 总体情况
- API 名称: TreeSet
- 总方法数: 10
- 已测试方法: 8
- 未测试方法: 2
- 方法覆盖率: 80%

## 已测试方法
✅ add(value: T): boolean
   - 测试场景: 正常值、null、undefined
   - 错误码: 401
   - 覆盖率: 完整

✅ popFirst(): T | undefined
   - 测试场景: 空容器
   - 错误码: 401
   - 覆盖率: 完整

## 未测试方法
❌ getLast(): T | undefined
   - 缺少测试用例

❌ clear(): void
   - 缺少测试用例

## 测试文件位置
test/xts/acts/util/test/TreeSet.test.ets
```

### 7.2 差距列表

```json
{
  "api": "TreeSet",
  "gaps": [
    {
      "method": "getLast",
      "type": "method_not_tested",
      "priority": "high",
      "recommended_tests": [
        "SUB_UTILS_UTIL_TREESET_GETLAST_PARAM_001",
        "SUB_UTILS_UTIL_TREESET_GETLAST_RETURN_001",
        "SUB_UTILS_UTIL_TREESET_GETLAST_ERROR_401_001"
      ]
    },
    {
      "method": "add",
      "type": "partial_coverage",
      "priority": "medium",
      "missing_scenarios": ["boundary", "large_value"],
      "recommended_tests": [
        "SUB_UTILS_UTIL_TREESET_ADD_BOUNDARY_001"
      ]
    }
  ]
}
```

---

## 八、补充测试建议

### 8.1 优先级规则

| 优先级 | 条件 | 说明 |
|--------|------|------|
| HIGH | 完全未测试的核心方法 | 优先补充 Level0/Level1 测试 |
| MEDIUM | 部分测试的重要方法 | 补充缺失的测试场景 |
| LOW | 测试完整的边缘方法 | 可选补充 |

### 8.2 测试补充策略

1. **优先补充 Level0/Level1**：基本功能和常用输入
2. **然后补充 Level2**：错误场景
3. **最后补充 Level3/Level4**：边缘场景

---

## 九、覆盖率对比分析

### 9.1 更新前后对比

在生成新测试用例后，必须计算并输出更新前后的覆盖率对比：

```typescript
/**
 * 覆盖率对比数据结构
 */
interface CoverageComparison {
  before: CoverageData;
  after: CoverageData;
  improvement: {
    newlyCoveredApis: number;
    coverageIncrease: number;  // 百分点
    improvementPercent: number; // 相对提升百分比
  };
}

interface CoverageData {
  testedApis: number;
  untestedApis: number;
  totalApis: number;
  coverageRate: number;  // 百分比
}
```

### 9.2 覆盖率对比计算

```typescript
/**
 * 计算覆盖率对比
 * @param before 更新前覆盖率数据
 * @param after 更新后覆盖率数据
 * @returns 覆盖率对比结果
 */
function calculateCoverageComparison(before: CoverageData, after: CoverageData): CoverageComparison {
  return {
    before,
    after,
    improvement: {
      newlyCoveredApis: after.testedApis - before.testedApis,
      coverageIncrease: after.coverageRate - before.coverageRate,
      improvementPercent: before.coverageRate > 0
        ? ((after.coverageRate - before.coverageRate) / before.coverageRate) * 100
        : 100
    }
  };
}
```

### 9.3 覆盖率对比报告格式

```markdown
### 覆盖率对比
#### 更新前覆盖率
- 已测试 API：3 个
- 未测试 API：12 个
- 总 API 数：15 个
- 覆盖率：20%

#### 更新后覆盖率
- 已测试 API：11 个
- 未测试 API：4 个
- 总 API 数：15 个
- 覆盖率：73.3%

#### 覆盖率提升
- 新增覆盖 API：8 个
- 覆盖率提升：+53.3%
- 提升百分比：266.5%
```

### 9.4 可视化覆盖进度

支持使用 ASCII 字符展示覆盖率进度：

```markdown
### 覆盖率进度可视化

更新前：
[████████░░░░░░░░░░░░] 20% (3/15)

更新后：
[████████████████████] 73.3% (11/15)
```

### 9.5 覆盖率提升等级

| 提升幅度 | 等级 | 说明 |
|---------|------|------|
| > 50% | 优秀 | 显著提升测试覆盖 |
| 30% - 50% | 良好 | 有效补充测试用例 |
| 10% - 30% | 中等 | 部分改进测试覆盖 |
| < 10% | 较小 | 测试覆盖改进有限 |

---

## 十、与测试生成器配合

覆盖率分析器的输出将传递给测试生成器：

```
覆盖率分析器输出:
- 未测试方法列表
- 缺失的测试场景
- 推荐的测试用例编号
  ↓
测试生成器输入:
- 只生成缺失的测试用例
- 使用推荐的测试用例编号
- 优先生成高优先级测试
```
