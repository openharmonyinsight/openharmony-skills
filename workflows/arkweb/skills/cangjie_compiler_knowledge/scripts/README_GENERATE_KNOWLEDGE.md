# generate_knowledge.py - 知识库生成脚本

## 概述

`generate_knowledge.py` 是知识库生成的主脚本，整合所有组件从编译器源码自动提取结构化信息，构建可搜索的知识库索引。

## 功能特性

- **自动化提取**: 扫描和解析 C++ 源码，提取类、函数、模块等信息
- **模块分析**: 根据文件路径推断模块结构，构建模块依赖图
- **依赖分析**: 分析模块间依赖和函数调用关系
- **关键词提取**: 从代码元素中提取中英文搜索关键词
- **描述合并**: 读取 AI 维护的 Markdown 描述文件并合并到索引
- **并行处理**: 支持多线程并行解析文件，提高处理速度
- **增量更新**: 只处理修改过的文件，节省时间
- **错误处理**: 优雅处理解析失败，记录错误但继续处理

## 使用方法

### 基本用法

```bash
# 在 scripts 目录下执行
cd cangjie_ace_skills/cangjie_compiler_knowledge/scripts

# 生成完整知识库（使用默认路径）
python3 generate_knowledge.py
```

### 命令行参数

```
--source-dir PATH       编译器源码目录 (默认: ../../../cangjie_compiler)
--output-dir PATH       输出目录 (默认: ../knowledge-base)
--incremental           增量更新模式（只处理修改过的文件）
--verbose               显示详细日志
--parallel N            并行处理文件数 (默认: 4)
```

### 使用示例

```bash
# 指定源码目录
python3 generate_knowledge.py --source-dir /path/to/cangjie_compiler

# 增量更新（只处理修改过的文件）
python3 generate_knowledge.py --incremental

# 并行处理（8 个线程）
python3 generate_knowledge.py --parallel 8

# 显示详细日志
python3 generate_knowledge.py --verbose

# 组合使用
python3 generate_knowledge.py --source-dir ../../../cangjie_compiler --output-dir ../knowledge-base --parallel 8 --verbose
```

## 工作流程

1. **验证源码目录**: 检查编译器源码目录是否存在
2. **扫描文件**: 递归扫描所有 `.h` 和 `.cpp` 文件
3. **解析文件**: 并行解析文件，提取类、函数、#include 等信息
4. **构建模块树**: 根据文件路径推断模块结构
5. **分析依赖**: 分析模块依赖和函数调用关系
6. **加载描述**: 读取 `descriptions/` 目录下的 Markdown 文件
7. **构建索引**: 提取关键词，构建搜索索引
8. **构建交叉引用**: 构建模块和函数的交叉引用
9. **保存输出**: 生成 JSON 文件

## 输出文件

脚本会在输出目录下生成以下文件：

```
knowledge-base/
├── search-index.json           # 搜索索引（关键词 -> 代码元素）
├── cross-references.json       # 交叉引用（模块依赖、函数调用）
├── modules/                    # 模块数据目录
│   ├── parse.json             # parse 模块数据
│   ├── sema.json              # sema 模块数据
│   └── ...                    # 其他模块
├── descriptions/               # AI 维护的描述文件（不会被覆盖）
│   ├── lambda.md
│   ├── generic.md
│   └── ...
└── .last_generated            # 上次生成时间戳（用于增量更新）
```

## 数据格式

### search-index.json

```json
{
  "keywords": {
    "lambda": {
      "description": "lambda 表达式的解析和语义分析",
      "description_en": "Parsing and semantic analysis of lambda expressions",
      "synonyms": ["匿名函数", "anonymous function"],
      "related": ["function", "closure"],
      "modules": ["parse", "sema"],
      "classes": [
        {"name": "LambdaExpr", "file": "src/Parse/Lambda.h", "line": 45}
      ],
      "functions": [
        {"name": "ParseLambda", "file": "src/Parse/Lambda.cpp", "line": 156}
      ],
      "tfidf_score": 0.85
    }
  }
}
```

### cross-references.json

```json
{
  "module_dependencies": {
    "parse": {
      "depends_on": ["basic", "lex"],
      "depended_by": ["sema", "frontend"]
    }
  },
  "function_calls": {
    "TypeCheckLambda": {
      "calls": ["BuildLambdaClosure", "InferType"],
      "called_by": ["TypeCheckExpr"]
    }
  }
}
```

### modules/parse.json

```json
{
  "name": "parse",
  "path": "src/Parse",
  "files": ["src/Parse/Lambda.cpp", "src/Parse/Lambda.h"],
  "classes": [
    {"name": "LambdaExpr", "file": "src/Parse/Lambda.h", "line": 45}
  ],
  "functions": [
    {"name": "ParseLambda", "file": "src/Parse/Lambda.cpp", "line": 156}
  ],
  "submodules": []
}
```

## 性能优化

- **并行处理**: 使用 `--parallel` 参数指定线程数，默认 4 个线程
- **增量更新**: 使用 `--incremental` 只处理修改过的文件
- **进度显示**: 每处理 100 个文件显示一次进度

## 错误处理

- **源码目录不存在**: 输出错误信息并退出（退出码 1）
- **文件解析失败**: 记录警告但继续处理其他文件
- **保存文件失败**: 输出错误信息并退出（退出码 1）
- **用户中断**: 捕获 Ctrl+C，优雅退出（退出码 130）

## 日志级别

- **普通模式**: 只显示关键信息（INFO 级别）
- **详细模式** (`--verbose`): 显示调试信息（DEBUG 级别）

## 依赖组件

- `file_scanner.py` - 文件扫描器
- `cpp_parser.py` - C++ 解析器
- `module_analyzer.py` - 模块分析器
- `dependency_analyzer.py` - 依赖分析器
- `keyword_extractor.py` - 关键词提取器
- `markdown_parser.py` - Markdown 解析器
- `search_index_builder.py` - 搜索索引构建器
- `cross_ref_builder.py` - 交叉引用构建器

## 注意事项

1. **首次运行**: 首次运行会扫描所有文件，可能需要几分钟
2. **增量更新**: 增量更新依赖 `.last_generated` 时间戳文件
3. **描述文件**: `descriptions/` 目录下的 Markdown 文件不会被覆盖
4. **内存使用**: 大型代码库可能需要较多内存，建议至少 2GB 可用内存

## 故障排除

### 问题：源码目录不存在

```
错误: 源码目录不存在: ../../../cangjie_compiler
```

**解决方法**: 使用 `--source-dir` 参数指定正确的路径

### 问题：解析失败过多

```
解析失败 100 个文件
```

**解决方法**: 使用 `--verbose` 查看详细错误信息，检查文件编码或格式问题

### 问题：内存不足

**解决方法**: 减少 `--parallel` 参数值，或分批处理文件

## 示例输出

```
============================================================
开始生成知识库
============================================================
12:34:56 - INFO - 源码目录: /path/to/cangjie_compiler
12:34:56 - INFO - 扫描源码文件...
12:34:57 - INFO - 找到 1234 个文件
12:34:57 - INFO - 解析 1234 个文件...
12:35:10 - INFO - 进度: 100/1234
12:35:23 - INFO - 进度: 200/1234
...
12:36:45 - INFO - 成功解析 1230 个文件
12:36:45 - WARNING - 解析失败 4 个文件
12:36:45 - INFO - 构建模块树...
12:36:46 - INFO - 找到 25 个模块
12:36:46 - INFO - 分析模块依赖...
12:36:47 - INFO - 分析函数调用...
12:36:50 - INFO - 加载 Markdown 描述...
12:36:50 - INFO - 加载了 15 个描述
12:36:50 - INFO - 构建搜索索引...
12:36:52 - INFO - 合并描述信息...
12:36:52 - INFO - 索引包含 3456 个关键词
12:36:52 - INFO - 构建交叉引用...
12:36:53 - INFO - 保存输出文件...
12:36:53 - INFO - 已保存: /path/to/knowledge-base/search-index.json
12:36:53 - INFO - 已保存: /path/to/knowledge-base/cross-references.json
12:36:54 - INFO - 已保存 25 个模块文件到: /path/to/knowledge-base/modules
============================================================
知识库生成完成！耗时: 118.23 秒
============================================================
```
