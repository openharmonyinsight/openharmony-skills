# CrossRefBuilder - 交叉引用构建器

## 概述

CrossRefBuilder 是知识库系统的索引构建层组件，负责构建模块依赖和函数调用的双向交叉引用。它接收来自 DependencyAnalyzer 的依赖图和调用图，生成结构化的交叉引用数据，支持快速查询模块和函数的上下游关系。

## 功能特性

- **模块依赖交叉引用**: 构建模块之间的双向依赖关系（depends_on 和 depended_by）
- **函数调用交叉引用**: 构建函数之间的双向调用关系（calls 和 called_by）
- **JSON 输出**: 生成符合设计规范的 cross-references.json 文件
- **数据完整性**: 确保双向引用的一致性

## 数据结构

### ModuleReference

表示单个模块的交叉引用：

```python
@dataclass
class ModuleReference:
    depends_on: List[str]    # 该模块依赖的其他模块列表
    depended_by: List[str]   # 依赖该模块的其他模块列表
```

### FunctionReference

表示单个函数的交叉引用：

```python
@dataclass
class FunctionReference:
    calls: List[str]         # 该函数调用的其他函数列表
    called_by: List[str]     # 调用该函数的其他函数列表
```

### CrossReference

完整的交叉引用数据：

```python
@dataclass
class CrossReference:
    module_dependencies: Dict[str, ModuleReference]
    function_calls: Dict[str, FunctionReference]
```

## 输出格式

生成的 `cross-references.json` 文件格式：

```json
{
  "module_dependencies": {
    "parse": {
      "depends_on": ["basic", "lex"],
      "depended_by": ["sema", "frontend"]
    },
    "sema": {
      "depends_on": ["parse", "chir"],
      "depended_by": ["frontend"]
    }
  },
  "function_calls": {
    "TypeCheckLambda": {
      "calls": ["BuildLambdaClosure", "InferType"],
      "called_by": ["TypeCheckExpr", "AnalyzeFunction"]
    },
    "BuildLambdaClosure": {
      "calls": [],
      "called_by": ["TypeCheckLambda"]
    }
  }
}
```

## 使用方法

### 基本用法

```python
from cross_ref_builder import CrossRefBuilder
from dependency_analyzer import DependencyAnalyzer

# 创建构建器
builder = CrossRefBuilder()

# 假设已经有了依赖图和调用图
dep_graph = dep_analyzer.analyze_module_dependencies(tree, parsed_files)
call_graph = dep_analyzer.analyze_function_calls(parsed_files)

# 构建交叉引用
cross_ref = builder.build(dep_graph, call_graph)

# 保存到文件
builder.save_to_file(cross_ref, "knowledge-base/cross-references.json")
```

### 单独构建模块引用

```python
# 只构建模块依赖的交叉引用
module_refs = builder.build_module_refs(dep_graph)

# 访问特定模块的引用
parse_ref = module_refs["parse"]
print(f"parse depends on: {parse_ref.depends_on}")
print(f"parse depended by: {parse_ref.depended_by}")
```

### 单独构建函数引用

```python
# 只构建函数调用的交叉引用
function_refs = builder.build_function_refs(call_graph)

# 访问特定函数的引用
func_ref = function_refs["TypeCheckLambda"]
print(f"TypeCheckLambda calls: {func_ref.calls}")
print(f"TypeCheckLambda called by: {func_ref.called_by}")
```

### 转换为 JSON

```python
# 转换为 JSON 字符串
json_str = builder.to_json(cross_ref)
print(json_str)

# 或者直接保存到文件
builder.save_to_file(cross_ref, "output.json")
```

## 命令行测试

可以直接运行脚本进行测试：

```bash
# 分析指定目录的代码并生成交叉引用
python3 cross_ref_builder.py /path/to/cangjie_compiler

# 输出示例：
# 解析 1234 个文件...
# 构建模块树...
# 分析依赖关系...
# 构建交叉引用...
# 
# 模块交叉引用（前 5 个）:
# 
# parse:
#   depends_on: lex, basic
#   depended_by: sema, frontend
# 
# 函数交叉引用（前 5 个）:
# 
# TypeCheckLambda:
#   calls: BuildLambdaClosure, InferType
#   called_by: TypeCheckExpr
# 
# 交叉引用已保存到: cross-references.json
```

## 运行测试

```bash
# 运行所有测试
python3 test_cross_ref_builder.py

# 运行详细测试
python3 test_cross_ref_builder.py -v

# 运行特定测试
python3 test_cross_ref_builder.py TestCrossRefBuilder.test_build_module_refs_simple
```

## 测试覆盖

测试套件包含以下测试用例：

### CrossRefBuilder 测试
- `test_build_module_refs_empty`: 空依赖图
- `test_build_module_refs_simple`: 简单模块依赖
- `test_build_function_refs_empty`: 空调用图
- `test_build_function_refs_simple`: 简单函数调用
- `test_build_complete_cross_reference`: 完整交叉引用
- `test_to_json_format`: JSON 格式验证
- `test_save_to_file`: 文件保存功能
- `test_bidirectional_references`: 双向引用一致性
- `test_complex_dependency_graph`: 复杂依赖图

### 数据类测试
- `TestModuleReference`: 测试 ModuleReference 数据类
- `TestFunctionReference`: 测试 FunctionReference 数据类
- `TestCrossReference`: 测试 CrossReference 数据类

## 设计要点

### 双向引用

交叉引用的核心价值在于提供双向查询能力：

- **正向查询**: 给定模块 A，查询它依赖哪些模块（depends_on）
- **反向查询**: 给定模块 A，查询哪些模块依赖它（depended_by）

这种双向引用使得搜索引擎可以：
- 回答"parse 模块依赖哪些模块？"
- 回答"哪些模块依赖 parse 模块？"
- 分析模块的影响范围
- 追踪函数调用链路

### 数据一致性

构建器确保双向引用的一致性：
- 如果 A depends_on B，则 B 的 depended_by 必须包含 A
- 如果 F1 calls F2，则 F2 的 called_by 必须包含 F1

测试套件中的 `test_bidirectional_references` 验证了这一点。

### JSON 格式

输出的 JSON 格式严格遵循设计文档规范：
- 使用 `depends_on` 和 `depended_by` 表示模块依赖
- 使用 `calls` 和 `called_by` 表示函数调用
- 使用 UTF-8 编码，支持中文
- 使用 2 空格缩进，便于阅读

## 与其他组件的集成

### 输入来源

CrossRefBuilder 接收来自 DependencyAnalyzer 的数据：

```
DependencyAnalyzer
    ├── analyze_module_dependencies() → DependencyGraph
    └── analyze_function_calls() → CallGraph
                                        ↓
                                CrossRefBuilder
                                        ↓
                                CrossReference
                                        ↓
                            cross-references.json
```

### 输出使用

生成的交叉引用数据被搜索引擎使用：

```
cross-references.json
        ↓
    SearchEngine
        ↓
显示模块依赖关系和函数调用链路
```

## 性能考虑

- **时间复杂度**: O(M + F)，其中 M 是模块数，F 是函数数
- **空间复杂度**: O(M + F)，存储所有模块和函数的引用
- **构建速度**: 对于大型代码库（1000+ 模块），构建时间通常 < 1 秒

## 扩展性

### 支持更多引用类型

可以扩展 CrossReference 数据类以支持更多类型的引用：

```python
@dataclass
class CrossReference:
    module_dependencies: Dict[str, ModuleReference]
    function_calls: Dict[str, FunctionReference]
    class_inheritance: Dict[str, ClassReference]  # 新增：类继承关系
    interface_implementations: Dict[str, InterfaceReference]  # 新增：接口实现
```

### 支持更细粒度的引用

可以为引用添加更多元数据：

```python
@dataclass
class DetailedModuleReference:
    depends_on: List[Dict[str, Any]]  # 包含文件路径、行号等信息
    depended_by: List[Dict[str, Any]]
```

## 相关文档

- [DependencyAnalyzer 文档](README_DEPENDENCY_ANALYZER.md) - 依赖分析器

## 需求映射

该组件实现了以下需求：

- **需求 5.3**: 存储每个模块依赖的其他模块列表
- **需求 5.4**: 存储每个模块被哪些模块依赖
- **需求 6.3**: 存储每个函数调用的其他函数列表
- **需求 6.4**: 存储每个函数被哪些函数调用

## 维护指南

### 添加新的引用类型

1. 在 `cross_ref_builder.py` 中定义新的引用数据类
2. 在 `CrossReference` 中添加新字段
3. 在 `CrossRefBuilder` 中添加构建方法
4. 更新 `to_json()` 方法以包含新字段
5. 添加相应的测试用例

### 修改 JSON 格式

如果需要修改输出的 JSON 格式：

1. 更新 `to_json()` 方法
2. 更新设计文档中的数据模型
3. 更新测试用例中的格式验证
4. 确保搜索引擎能够解析新格式

## 常见问题

### Q: 为什么需要双向引用？

A: 双向引用支持正向和反向查询，使得搜索引擎可以回答"谁依赖我"和"我依赖谁"两类问题，这对于理解代码结构和影响分析非常重要。

### Q: 如何处理循环依赖？

A: CrossRefBuilder 不检测或处理循环依赖，它只是如实记录依赖关系。循环依赖的检测应该在 DependencyAnalyzer 或更高层的组件中进行。

### Q: 函数调用关系是否精确？

A: 函数调用关系基于 DependencyAnalyzer 的启发式分析，可能存在误报（false positive）。对于更精确的分析，需要使用 clang static analyzer。

### Q: 如何优化大型代码库的性能？

A: CrossRefBuilder 本身已经很高效（O(M + F)）。性能瓶颈通常在 DependencyAnalyzer 的分析阶段。可以考虑：
- 使用增量更新，只处理修改的文件
- 并行处理多个文件
- 缓存中间结果
