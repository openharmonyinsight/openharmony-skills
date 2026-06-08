## Phase 3: Targeted API Info Parsing

---

> **`knowledge_root` 降级**：下文中所有 `{knowledge_root}/...` 路径，若 `knowledge_root` 未配置或路径不存在，则降级从 `{skill_root}/modules/` 和 `{skill_root}/references/` 加载对应内置知识。完整映射表见 `system.md`「知识库路径与降级规则」。

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{knowledge_root}/common/xts_experience/09_methodology/01_api_parsing.md` | API 解析方法论（多源整合、信息优先级、降级策略） | 解析策略不确定、信息源缺失需要降级处理时 |

---

### ⚙️ 按需加载（根据任务需求）

以下模块仅在你执行对应任务时才需要加载：

| 任务 | 加载文件 | 说明 |
|------|---------|------|
| 需要判断语法类型时 | `{knowledge_root}/common/xts_experience/09_methodology/02_syntax_filter.md` | 检查 API 的支持语法类型 |
| 需要项目特定解析时 | `{knowledge_root}/common/xts_experience/09_methodology/03_project_parsing.md` | 项目特定的解析规则 |

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
{knowledge_root}/common/xts_experience/09_methodology/ 下的 L2_Generation 相关文件（08~18号文件）
{knowledge_root}/common/xts_experience/09_methodology/ 下的 L3_Validation 相关文件（19~25号文件）
{knowledge_root}/common/xts_experience/ 下的 01_framework、02_arkts、03_standards、04_project、05_patterns 规范文件
```

---

**加载模块**: `{knowledge_root}/common/xts_experience/09_methodology/01_api_parsing.md`

**核心目标**：深入学习未覆盖 API 的详细信息，包括方法签名、参数类型、返回值、错误码、使用场景等，为后续测试用例生成提供完整的 API 知识基础。

**关键理解**：
- ❌ **误解**：Phase 3 仅仅是提取未覆盖 API 列表
- ✅ **正确**：Phase 3 是构建完整的 API 知识库，每个 API 都有深度解析

**关键说明**：此阶段在 Phase 2 识别出未覆盖的 API 之后执行，主要任务不是简单的列表提取，而是通过多源信息收集，构建每个未覆盖 API 的完整知识库。

### 信息源优先级

```
.d.ts 文件（最高）→ 官方文档 → 现有测试 → 子系统配置
```

### 解析范围

**仅解析 Phase 2 识别出的未覆盖或部分覆盖的 API**，深度学习每个 API 的详细信息：

| 覆盖状态 | 深度学习重点 | 测试生成优先级 |
|---------|-------------|--------------|
| 完全未测试 | - 完整的类型信息和签名<br>- 所有错误码和使用场景<br>- 最佳实践和限制条件<br>- 类似 API 的参考测试 | HIGH（首先生成测试） |
| 部分测试 | - 缺失的场景详情（null/undefined、边界值、错误码）<br>- 未覆盖的参数组合<br>- 缺失的断言类型<br>- 错误处理的不足 | MEDIUM（补充测试） |
| 测试不完整 | - 现有测试的质量分析<br>- 缺失的断言验证<br>- 缺失的负向测试<br>- 测试覆盖的盲点 | LOW（完善测试） |

### 解析步骤

#### 1. 获取未覆盖 API 列表（基础数据）

**Flow A / Flow B**：已在 Phase 2 的「解析覆盖率结果」章节中通过 `extract_uncovered.py` 获取。如需调整筛选条件重新提取，请参考 Phase 2 该章节。

**Flow C**（跳过了 Phase 2）：直接使用用户提供的全部新增 API 作为未覆盖列表，所有 API 缺口级别默认为 HIGH。

**批量模式**：如果用户选择分批执行，先运行 `python {skill_root}/scripts/batch_manager.py plan` 生成分批计划，然后通过 `start <batch_id>` 获取当前批次的 API 列表。当前批次仅需解析这 ≤10 个 API 的信息。

**输出文件**（由 `extract_uncovered.py` 生成到 `.coverage_data/iter-{N}/`）：

| 文件 | 内容 |
|------|------|
| `uncovered_apis_{timestamp}.json` | 真正未覆盖的 API（仅含"未覆盖"状态的维度） |
| `manual_confirm_{timestamp}.json` | 需人工确认的 API（`err_desc` = "工具暂不能识别返回值类型，请人工确认"） |

**`uncovered_apis.json` 输出结构**：

```json
{
  "ets1.1": {
    "methods": [
      {
        "module": "text", "class": "TextAttribute", "method": "orphanCharOptimization",
        "type": "Method", "func": "orphanCharOptimization(value: OrphanCharOptimization): TextAttribute",
        "kit": "ArkUI", "file_path": "component\\text.d.ts", "subsystem": "ArkUI开发框架",
        "error_codes": "", "start_version": "14",
        "stage_label": "stagemodelonly",
        "interface_covered_status": "否",
        "coverage": {
          "call": { "status": "未覆盖" },
          "param": { "status": "未覆盖" },
          "return_value": { "status": "未覆盖", "err_desc": "无用例覆盖" }
        }
      }
    ],
    "interfaces": [],
    "properties": []
  },
  "metadata": {
    "ets_versions": ["ets1.1"],
    "generated_at": "2026-05-27 14:43:35",
    "summary": { "ets1.1": { "methods": 573, "interfaces": 0, "properties": 263 } }
  }
}
```

**`manual_confirm.json` 输出结构**：

```json
{
  "manual_confirm": [
    {
      "module": "ohos.arkui.UIContext", "class": "DynamicSyncScene", "method": "getFrameRateRange",
      "func": "getFrameRateRange(): ExpectedFrameRateRange;",
      "file_path": "api\\@ohos.arkui.UIContext.d.ts", "subsystem": "ArkUI开发框架", "kit": "ArkUI",
      "return_value": { "status": "需人工确认", "err_desc": "工具暂不能识别返回值类型，请人工确认" }
    }
  ],
  "count": 78
}
```

#### 2. 深入学习未覆盖 API 信息（核心环节）

针对每个未覆盖 API，通过多源信息收集构建完整知识库：

**a) 读取 .d.ts 文件（精确类型信息）**

关键信息：interface/class 完整声明、方法签名/参数类型/返回类型、方法重载列表、Promise 与 AsyncCallback 双模式、@throws 错误码、@since 版本、枚举定义、可选参数、参数范围约束。

**废弃状态提取（必选）**：解析 .d.ts 时，同时提取以下信息并写入每个 API 知识库条目：
- `deprecated: boolean` — 是否标记了 `@deprecated`
- `deprecated_since: string` — 废弃版本（如 `@deprecated since 12`）
- `useinstead: string` — `@useinstead` 标签指向的替代接口名称
- 后续 Phase 4/5 可通过读取知识库判断接口废弃状态，无需重新解析 .d.ts

**b) 查阅官方 API 文档（使用场景和限制）**

补充信息：API 功能描述、使用示例、调用顺序/依赖关系、使用限制、性能注意事项、兼容性说明。

**c) 分析现有测试用例（实际使用模式）**

参考信息：相似 API 的测试模式、常见参数组合、错误处理方式、断言方法选择、异步测试处理。

**d) 查阅子系统配置（特殊规则）**

规则信息：子系统特定测试要求、命名规范、必需测试场景、特殊错误码处理、权限要求。

#### 2.5 信息源降级策略

多源信息收集过程中，可能遇到部分信息源不可用。按以下策略处理：

| 不可用的信息源 | 处理方式 | 对知识库的影响 | 恢复动作 |
|---------------|---------|---------------|---------|
| **.d.ts 文件缺失** | **终止该 API 解析**——.d.ts 缺失意味着无法 import 接口，生成的代码无法编译，继续解析毫无意义 | 无法生成测试 | 向用户报告缺失的 .d.ts 路径，提示检查配置（`interface_path` 或 `OH_ROOT`）。用户修正后重新执行 Phase 3 |
| **官方文档缺失** | 降级：仅使用 .d.ts + 现有测试 + 子系统配置生成知识库 | 缺少使用场景、限制条件、性能注意事项。`usage_info` 标记 `"doc_available": false`，Phase 4 设计文档中标注"缺少官方文档参考" | — |
| **现有测试为空** | 降级：跳过测试模式参考，使用 `{knowledge_root}/common/xts_experience/09_methodology/12_code_templates.md` 中的通用模板 | 缺少代码风格参考和常见用法模式。`test_patterns` 填入 `"existing_patterns": []`，`"template_fallback": true` | — |
| **子系统配置缺失** | 降级：仅使用 `{knowledge_root}/common/xts_experience/09_project_data/subsystem_config_spec.md` 核心配置 | 缺少子系统特有规则和特殊错误码处理。标记 `"subsystem_config": "core_only"`，Phase 5 跳过子系统特有规则 | — |
| **所有信息源均缺失** | **终止该 API 解析** | 无法生成任何有用信息 | 向用户报告，提示检查环境配置 |

**降级标记与下游感知**：

1. 每个降级的 API 在知识库中标记 `"degraded": true` 和 `"missing_sources": ["doc", "existing_tests"]`
2. Phase 4 读取降级标记，对降级 API 仅生成 PARAM 和 RETURN 类型测试，不生成 ERROR 类型（缺少错误码来源时）
3. Phase 3 结束时向用户汇总：`"X 个 API 完整解析，Y 个 API 降级解析（缺少：文档 Z 个、测试参考 W 个），K 个 API 终止（.d.ts 缺失）"`

#### 2.7 ArkTS 动态语法约束检测（仅动态项目 ArkTS-Dyn）

**目的**：在解析阶段预检测 API 签名中的特征模式，查表获取对应的 ArkTS 动态语法约束，避免 Phase 5 生成代码时因语法违规导致编译失败。

**步骤**：

1. **查表**：读取 `{skill_root}/references/arkts_api_pattern_rules.md`，对照每个 API 的 .d.ts 签名检测特征模式（Promise、泛型、回调、集合、对象、类/接口、@Sendable 等 10 类模式）
2. **写入约束**：命中的约束写入该 API 知识库条目的 `arkts_constraints` 数组（示例见下方输出结构）
3. **未命中**：保持 `arkts_constraints: []`，表示该 API 无特殊语法约束

**约束传递**：
- Phase 5 从每个 API 的 `arkts_constraints` 读取约束，生成代码时逐条遵守
- Phase 7 验证时，`arkts_constraints` 中的约束可作为校验依据

> **兜底机制**：`arkts_api_pattern_rules.md` 覆盖 10 类常见模式（约 99% 场景）。若 Phase 8 编译失败且错误码不在映射表范围内，调用 `arkts-skill` 的 `search_docs.py` 兜底查询（详见 Phase 8）。

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
  
  "deprecation": {
    "deprecated": false,
    "deprecated_since": "",
    "useinstead": ""
  },
  
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
  
  "arkts_constraints": [
    {
      "pattern": "Promise<T>",
      "rules": ["catch 不标注类型", "throw 只能抛 Error 实例", "finally 禁止 return/throw"],
      "error_codes": [10605079, 10605087]
    },
    {
      "pattern": "Array<T>",
      "rules": ["禁止 for...in", "展开运算符仅限数组", "数组字面量必须可推断类型"],
      "error_codes": [10605080, 10605099]
    }
  ],
  
  "reference_sources": {
    "dts_file": "path/to/module.d.ts",
    "doc_url": "https://docs.example.com/api/...",
    "similar_tests": ["test1.ets", "test2.ets"]
  }
}
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
    "source_data": "iter-1/uncovered_apis_20260417103500.json",
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

**输出结构包含 coverage 维度信息**：
- 每个 API 条目的 `coverage` 字段记录未覆盖的具体维度（call/param/param_spec/return_value/error_code/permission/stage/meta）
- `metadata.summary` 包含各版本的未覆盖 API 统计
- 若存在需人工确认的 API，同目录下会生成 `manual_confirm_timestamp.json`

**使用方式**：
- Phase 4 基于完整的 API 知识库生成测试设计文档
- 每个 API 的 `coverage_gaps` 指导测试场景设计
- `test_patterns` 提供现有测试的参考模式
- `error_codes` 确保错误码测试的完整性

**对后续阶段的影响**：
- **Phase 4（设计）**：知识库中的 `signature_info` 和 `error_codes` 直接影响测试设计
- **Phase 5（生成）**：`usage_info` 和 `test_patterns` 指导测试用例代码生成
- **Phase 7（验证）**：知识库中的类型信息用于验证生成的测试用例
- **Phase 10（覆盖率）**：`coverage_gaps` 用于验证新增测试的覆盖效果

**质量保证**：
- 每个 API 的知识库条目都经过多源信息验证
- 冲突信息按优先级解决，确保准确性
- 支持人工审查和修正，提升知识库质量
