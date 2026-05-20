# search.py - 搜索脚本文档

## 概述

`search.py` 是仓颉编译器知识库的搜索主脚本，供 AI 助手查询编译器实现细节。它整合了查询解析、搜索引擎、结果排序和格式化输出等功能。

## 功能特性

- ✅ 中英文混合查询支持
- ✅ 模糊匹配（基于编辑距离）
- ✅ 同义词扩展
- ✅ 多种输出格式（文本/JSON）
- ✅ 多语言输出（中文/英文）
- ✅ 智能错误处理和建议
- ✅ 交叉引用显示（模块依赖、函数调用）

## 使用方法

### 基本用法

```bash
python3 scripts/search.py <query> [options]
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query` | 搜索查询字符串（必需） | - |
| `--index-path PATH` | 索引文件路径 | `../knowledge-base/search-index.json` |
| `--max-results N` | 最大结果数 | 10 |
| `--no-fuzzy` | 禁用模糊匹配 | 启用 |
| `--json` | 输出 JSON 格式 | 文本格式 |
| `--lang {zh,en}` | 输出语言 | zh |
| `--include-unittest` | 包含 unittest 相关结果 | 不包含 |
| `--verbose` | 显示详细信息 | 关闭 |

## 使用示例

### 1. 基本搜索

```bash
# 搜索 lambda
python3 scripts/search.py "lambda"

# 搜索类型推断
python3 scripts/search.py "类型推断"

# 搜索 TypeChecker 类
python3 scripts/search.py "TypeChecker"
```

### 2. 限制结果数量

```bash
# 只显示前 5 个结果
python3 scripts/search.py "lambda" --max-results 5
```

### 3. JSON 格式输出

```bash
# 输出 JSON 格式（便于程序处理）
python3 scripts/search.py "lambda" --json

# 结合 jq 工具美化输出
python3 scripts/search.py "lambda" --json | jq .
```

### 4. 英文输出

```bash
# 使用英文输出
python3 scripts/search.py "lambda" --lang en
```

### 5. 禁用模糊匹配

```bash
# 只进行精确匹配和同义词匹配
python3 scripts/search.py "lambda" --no-fuzzy
```

### 6. 详细模式

```bash
# 显示详细的处理过程
python3 scripts/search.py "lambda" --verbose
```

### 7. 过滤 unittest 结果

```bash
# 默认不包含 unittest 结果（推荐用于实际开发）
python3 scripts/search.py "lambda"

# 包含 unittest 结果（用于查看测试用例）
python3 scripts/search.py "lambda" --include-unittest
```

### 8. 自定义索引路径

```bash
# 使用自定义索引文件
python3 scripts/search.py "lambda" --index-path /path/to/search-index.json
```

## 输出格式

### 文本格式（默认）

```
找到 1 个结果：
================================================================================

结果 1:
概念: lambda
描述: Lambda 表达式的解析和语义分析
匹配类型: exact (相关性: 0.92)
同义词: 匿名函数, anonymous function, closure
相关概念: function, closure, capture

相关模块:
  - parse
  - sema

相关类:
  - LambdaExpr (src/Parse/Lambda.h:45)
  - LambdaAnalyzer (src/Sema/Lambda.h:23)

相关函数:
  - BuildLambdaClosure (src/Sema/Lambda.cpp:156)
  - TypeCheckLambda (src/Sema/Lambda.cpp:234)

模块依赖:
  parse 依赖: basic, lex
  parse 被依赖: sema, frontend

调用链路:
  TypeCheckLambda 调用: BuildLambdaClosure, InferType
  TypeCheckLambda 被调用: TypeCheckExpr, AnalyzeFunction
--------------------------------------------------------------------------------
```

### JSON 格式

```json
{
  "count": 1,
  "results": [
    {
      "keyword": "lambda",
      "description": "Lambda 表达式的解析和语义分析",
      "description_en": "Parsing and semantic analysis of lambda expressions",
      "match_type": "exact",
      "relevance_score": 0.92,
      "tfidf_score": 0.85,
      "synonyms": ["匿名函数", "anonymous function", "closure"],
      "related": ["function", "closure", "capture"],
      "modules": ["parse", "sema"],
      "classes": [
        {
          "name": "LambdaExpr",
          "file": "src/Parse/Lambda.h",
          "line": 45
        }
      ],
      "functions": [
        {
          "name": "BuildLambdaClosure",
          "file": "src/Sema/Lambda.cpp",
          "line": 156
        }
      ],
      "module_dependencies": {
        "parse": {
          "depends_on": ["basic", "lex"],
          "depended_by": ["sema", "frontend"]
        }
      },
      "function_calls": {
        "TypeCheckLambda": {
          "calls": ["BuildLambdaClosure", "InferType"],
          "called_by": ["TypeCheckExpr", "AnalyzeFunction"]
        }
      }
    }
  ]
}
```

## 搜索机制

### 1. 查询解析

- 自动检测查询语言（中文/英文/混合）
- 中文分词（使用 jieba）
- 英文分词和驼峰命名拆分
- 停用词过滤

### 2. 搜索策略

搜索按以下优先级进行：

1. **精确匹配**：关键词完全匹配（权重 1.0）
2. **同义词匹配**：匹配同义词列表（权重 0.9）
3. **模糊匹配**：基于编辑距离（权重 0.7-0.8）

### 3. 结果排序

综合考虑以下因素：

- 匹配类型（30%）
- TF-IDF 得分（30%）
- 关键词匹配度（20%）
- 内容丰富度（20%）

### 4. 模糊匹配

- 使用 Levenshtein 编辑距离算法
- 最大编辑距离：2
- 示例：`lambdaa` → `lambda`

## 错误处理

### 索引文件不存在

```bash
$ python3 scripts/search.py "lambda"
错误: 索引文件不存在: ../knowledge-base/search-index.json

提示: 请先运行以下命令生成知识库:
  python3 scripts/generate_knowledge.py
```

### 索引文件损坏

```bash
$ python3 scripts/search.py "lambda"
错误: 索引文件格式错误: ...

提示: 索引文件可能已损坏，请重新生成知识库:
  python3 scripts/generate_knowledge.py
```

### 搜索结果为空

```bash
$ python3 scripts/search.py "xyznotfound"
未找到匹配 'xyznotfound' 的结果。

您是否要搜索:
  - lambda
  - function
  - class
```

## 性能优化

- 索引文件在首次使用时加载到内存
- 搜索响应时间 < 100ms（索引已加载）
- 支持限制结果数量以提高性能

## 集成到 AI 工作流

### 在 AI 助手中使用

```python
import subprocess
import json

def search_compiler_knowledge(query, max_results=5):
    """搜索编译器知识库"""
    result = subprocess.run(
        ['python3', 'scripts/search.py', query, '--json', '--max-results', str(max_results)],
        cwd='/path/to/cangjie_compiler_knowledge',
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        return {'error': result.stderr}

# 使用示例
results = search_compiler_knowledge("lambda")
for result in results['results']:
    print(f"找到: {result['keyword']}")
    print(f"描述: {result['description']}")
```

### 触发场景

AI 助手应在以下场景触发搜索：

1. 用户询问特定语言特性的实现位置
   - "lambda 在哪实现"
   - "泛型如何实例化"

2. 用户询问特定类或函数的位置
   - "TypeChecker 在哪"
   - "ParseLambda 函数在哪"

3. 用户询问编译器模块或流程
   - "AST 模块在哪里"
   - "语义分析在哪个模块"

4. 用户询问关键字实现
   - "extend 关键字如何实现"
   - "match 表达式如何解析"

## 测试

运行测试脚本验证功能：

```bash
python3 scripts/test_search.py
```

测试覆盖：
- ✅ 基本搜索
- ✅ JSON 输出
- ✅ 模糊匹配
- ✅ 禁用模糊匹配
- ✅ 中文查询
- ✅ 英文输出
- ✅ 帮助信息

## 依赖

- Python 3.8+
- jieba（中文分词）
- 其他标准库模块

## 相关文档

- [generate_knowledge.py](README_GENERATE_KNOWLEDGE.md) - 知识库生成脚本
- [AI_MAINTENANCE_GUIDE.md](../AI_MAINTENANCE_GUIDE.md) - AI 维护指南
- [SKILL.md](../SKILL.md) - 技能说明文档

## 常见问题

### Q: 为什么搜索结果为空？

A: 可能的原因：
1. 知识库未生成或已过期
2. 查询关键词不在索引中
3. 禁用了模糊匹配且没有精确匹配

解决方法：
- 运行 `generate_knowledge.py` 重新生成知识库
- 尝试使用同义词或相关术语
- 启用模糊匹配（默认启用）

### Q: 如何提高搜索准确性？

A: 建议：
1. 使用更具体的关键词
2. 使用编译器术语（如类名、函数名）
3. 查看建议的相似关键词
4. 在 descriptions/ 目录添加更多描述文件

### Q: 搜索速度慢怎么办？

A: 优化方法：
1. 限制结果数量（--max-results）
2. 禁用模糊匹配（--no-fuzzy）
3. 确保索引文件在 SSD 上
4. 首次搜索会加载索引，后续搜索会更快

## 维护

### 更新索引

当编译器源码更新后，需要重新生成索引：

```bash
# 完整重新生成
python3 scripts/generate_knowledge.py

# 增量更新
python3 scripts/generate_knowledge.py --incremental
```

### 添加描述

在 `knowledge-base/descriptions/` 目录下添加 Markdown 文件：

```bash
# 创建新的描述文件
cat > knowledge-base/descriptions/new_concept.md << 'EOF'
---
keyword: new_concept
synonyms: [同义词1, 同义词2]
related: [相关概念1, 相关概念2]
---

# 新概念

## 中文描述
详细的中文描述...

## English Description
Detailed English description...
EOF

# 重新生成索引
python3 scripts/generate_knowledge.py
```
