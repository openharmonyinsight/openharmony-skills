## Phase 3: Targeted API Info Parsing

**加载模块**: `modules/L1_Analysis/parser/unified_api_parser.md`

**核心目标**：深入学习未覆盖 API 的详细信息，包括方法签名、参数类型、返回值、错误码、使用场景等，为后续测试用例生成提供完整的 API 知识基础。

**关键理解**：
- ❌ **误解**：Phase 3 仅仅是提取未覆盖 API 列表
- ✅ **正确**：Phase 3 是构建完整的 API 知识库，每个 API 都有深度解析

**关键说明**：此阶段在 Phase 2 识别出未覆盖的 API 之后执行，主要任务不是简单的列表提取，而是通过多源信息收集，构建每个未覆盖 API 的完整知识库。

**深度学习维度**：
1. **类型层面**：方法签名、参数类型、返回类型、重载列表
2. **功能层面**：API 用途、使用场景、调用顺序、依赖关系
3. **限制层面**：使用约束、性能考虑、兼容性要求
4. **错误层面**：错误码列表、错误条件、错误处理方式
5. **测试层面**：现有测试模式、最佳实践、常见问题

### 信息源优先级

```
.d.ts 文件（最高）→ 官方文档 → 现有测试 → 子系统配置
```

**信息收集策略**：
- **主信息源**：.d.ts 文件（精确的类型定义、方法签名）
- **辅助信息源**：官方文档（使用示例、注意事项、限制条件）
- **参考信息源**：现有测试（最佳实践、常见用法、错误处理）
- **补充信息源**：子系统配置（特殊规则、测试要求）

### 解析范围

**仅解析 Phase 2 识别出的未覆盖或部分覆盖的 API**，深度学习每个 API 的详细信息：

| 覆盖状态 | 深度学习重点 | 测试生成优先级 |
|---------|-------------|--------------|
| 完全未测试 | - 完整的类型信息和签名<br>- 所有错误码和使用场景<br>- 最佳实践和限制条件<br>- 类似 API 的参考测试 | HIGH（首先生成测试） |
| 部分测试 | - 缺失的场景详情（null/undefined、边界值、错误码）<br>- 未覆盖的参数组合<br>- 缺失的断言类型<br>- 错误处理的不足 | MEDIUM（补充测试） |
| 测试不完整 | - 现有测试的质量分析<br>- 缺失的断言验证<br>- 缺失的负向测试<br>- 测试覆盖的盲点 | LOW（完善测试） |

### 解析步骤

#### 1. 获取未覆盖 API 列表（基础数据）

使用 `scripts/extract_uncovered.py` 脚本提取未覆盖 API：

```bash
cd scripts/
python extract_uncovered.py --subsystem "子系统名" [--module-name "模块名"] [--iter-phase 1]
```

**批量模式**：如果用户选择分批执行，先运行 `python {skill_root}/scripts/batch_manager.py plan` 生成分批计划，然后通过 `start <batch_id>` 获取当前批次的 API 列表。当前批次仅需解析这 ≤10 个 API 的信息。

**该脚本功能**：
- 从 `.oh-xts-config.json` 读取 `ets_version` 配置
- 从迭代目录读取 CSV 覆盖率数据文件（`iter-{N}/before_generation_ets{X}_timestamp.csv`）
- 提取未覆盖的 API（方法、接口、属性）
- 生成结构化的 JSON 输出文件（`iter-{N}/uncovered_apis_timestamp.json`）
- 提供覆盖率分析统计（错误码、参数、返回值、权限等问题）

**脚本输出包含**：
- `ets1.1` / `ets1.2`: 各版本（ArkTS-Dyn / ArkTS-Sta）的未覆盖 API
- `methods`: 完全未测试的方法列表
- `interfaces`: 未覆盖的接口列表
- `properties`: 未覆盖的属性列表
- `coverage_analysis`: 详细的覆盖率问题分析

#### 2. 深入学习未覆盖 API 信息（核心环节）

针对每个未覆盖 API，通过多源信息收集构建完整知识库：

**a) 读取 .d.ts 文件（精确类型信息）**
```
关键信息：
- interface/class 完整声明
- 方法签名、参数类型、返回类型
- 方法重载（overload）列表
- Promise 与 AsyncCallback 双模式支持
- @throws 注解中的错误码列表
- @since 标签（版本兼容性）
- 枚举定义和类型别名
- 可选参数标记（?）
- 参数范围约束
```

**b) 查阅官方 API 文档（使用场景和限制）**
```
补充信息：
- API 功能描述和用途
- 使用示例和最佳实践
- 调用顺序和依赖关系
- 使用限制和约束条件
- 性能注意事项
- 兼容性说明
- 已知问题和解决方案
```

**c) 分析现有测试用例（实际使用模式）**
```
参考信息：
- 相似 API 的测试模式
- 常见的参数组合
- 典型的错误处理方式
- 断言方法的选择
- 测试前置条件准备
- 异步测试的处理方式
```

**d) 查阅子系统配置（特殊规则）**
```
规则信息：
- 子系统特定的测试要求
- 测试命名规范
- 必需的测试场景
- 特殊的错误码处理
- 权限相关要求
```

#### 3. 构建完整 API 知识库（输出结构）

为每个未覆盖 API 生成结构化的知识库条目：

```json
{
  "api_name": "methodName",
  "module": "@ohos.module",
  "class": "ClassName",
  "type": "Method",
  "coverage_status": "completely_untested",
  
  "signature_info": {
    "dts_declaration": "methodName(param1: string, param2: number): Promise<void>",
    "overloads": [
      "methodName(param1: string): Promise<void>",
      "methodName(param1: string, param2: number): Promise<void>"
    ],
    "async_modes": ["Promise", "AsyncCallback"],
    "is_optional_param": ["param2"],
    "param_ranges": {"param2": "1-100"}
  },
  
  "error_codes": [201, 401, 12300001],
  
  "usage_info": {
    "description": "API 功能描述",
    "prerequisites": ["前置条件1", "前置条件2"],
    "constraints": ["限制条件1", "限制条件2"],
    "best_practices": ["最佳实践1", "最佳实践2"]
  },
  
  "test_patterns": {
    "existing_patterns": ["现有测试模式1", "现有测试模式2"],
    "recommended_assertions": ["assertEqual", "assertTrue"],
    "error_handling": "expected error handling approach"
  },
  
  "coverage_gaps": {
    "missing_scenarios": ["normal", "null", "boundary", "error_code"],
    "priority": "HIGH",
    "estimated_tests": 5
  },
  
  "reference_sources": {
    "dts_file": "path/to/module.d.ts",
    "doc_url": "https://docs.example.com/api/...",
    "similar_tests": ["test1.ets", "test2.ets"]
  }
}
```

#### 4. 综合分析和冲突解决（多源信息整合）

```
冲突解决策略：
1. .d.ts 文件（最高优先级）：精确的类型定义
2. 官方文档：权威的功能说明
3. 现有测试：实际的使用验证
4. 子系统配置：项目特定的规则

处理冲突原则：
- 类型信息以 .d.ts 为准
- 功能说明以官方文档为准
- 实现细节以现有测试为准
- 特殊要求以子系统配置为准
```

### 语法类型过滤（如适用）

| API 类型 | 静态项目 | 动态项目 |
|---------|---------|---------|
| static_only | 兼容 | 不兼容 |
| dynamic_only | 不兼容 | 兼容 |
| hybrid | 使用静态语法 | 使用动态语法 |

### 输出

**核心输出**：完整的未覆盖 API 知识库（不仅仅是简单的 API 列表）

**输出结构**：
```json
{
  "metadata": {
    "ets_versions": ["ets1.1"],
    "generated_at": "2026-04-17 10:30:00",
    "source_data": "iter-1/before_generation_ets1.1_20260417103000.csv",
    "total_apis": 45,
    "uncovered_apis": 33
  },
  
  "api_knowledge_base": {
    "ets1.1": {
      "methods": [
        {
          // 完整的 API 知识库条目
          // 包含 signature_info, error_codes, usage_info, test_patterns, coverage_gaps, reference_sources 等
        }
      ],
      "interfaces": [...],
      "properties": [...]
    },
    "ets1.2": { /* 如果配置了多版本 */ }
  },
  
  "coverage_analysis": {
    "error_code_issues": 15,
    "param_issues": 12,
    "return_value_issues": 8,
    "permission_issues": 5,
    "specific_issues": [...]
  },
  
  "generation_priorities": {
    "high_priority": ["完全未测试的核心方法"],
    "medium_priority": ["部分测试但缺少场景的方法"],
    "low_priority": ["辅助功能的测试"]
  }
}
```

**输出文件位置**：`.coverage_data/iter-{N}/uncovered_apis_timestamp.json`

**使用方式**：
- Phase 4 基于完整的 API 知识库生成测试设计文档
- 每个 API 的 `coverage_gaps` 指导测试场景设计
- `test_patterns` 提供现有测试的参考模式
- `error_codes` 确保错误码测试的完整性

**对后续阶段的影响**：
- **Phase 4（设计）**：知识库中的 `signature_info` 和 `error_codes` 直接影响测试设计
- **Phase 5（生成）**：`usage_info` 和 `test_patterns` 指导测试用例代码生成
- **Phase 7（验证）**：知识库中的类型信息用于验证生成的测试用例
- **Phase 9（覆盖率）**：`coverage_gaps` 用于验证新增测试的覆盖效果

**质量保证**：
- 每个 API 的知识库条目都经过多源信息验证
- 冲突信息按优先级解决，确保准确性
- 支持人工审查和修正，提升知识库质量
