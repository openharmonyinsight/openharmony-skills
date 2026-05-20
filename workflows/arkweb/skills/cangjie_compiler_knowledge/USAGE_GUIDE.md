# Cangjie Compiler Knowledge Skill 使用指南

## 快速开始

### 1. 搜索概念

最简单的使用方式是通过搜索脚本：

```bash
cd cangjie_ace_skills/cangjie_compiler_knowledge
python3 scripts/search.py "lambda"
```

### 2. 查看描述文件

搜索结果会告诉你相关的描述文件，直接查看：

```bash
cat knowledge-base/descriptions/lambda.md
```

### 3. 生成关系图谱

可视化概念间的关系：

```bash
python3 scripts/visualize_concept_graph.py --keyword lambda --output graphs/lambda.md
```

## 主要功能

### 功能 1: 概念搜索

支持中英文搜索，自动匹配同义词和相关概念。

**示例**:
```bash
# 中文搜索
python3 scripts/search.py "类型推断"

# 英文搜索
python3 scripts/search.py "type inference"

# 模糊搜索
python3 scripts/search.py "infer"
```

**返回信息**:
- 概念描述（中英文）
- 相关模块
- 相关类和函数
- 模块依赖关系

### 功能 2: 代码示例

每个概念都包含真实的代码示例，直接从源码提取。

**查看方式**:

1. 打开描述文件
2. 查看"代码示例"部分
3. 根据文件路径和行号定位源码

### 功能 3: 概念关系图谱

可视化概念间的关系，包括：
- 同义词
- 相关概念
- 使用的模块
- 模块依赖

**生成图谱**:
```bash
# 概念关系图谱
python3 scripts/visualize_concept_graph.py --keyword lambda

# 模块依赖图谱
python3 scripts/visualize_concept_graph.py --module sema
```

### 功能 4: FAQ

每个概念都包含常见问题解答，快速了解核心要点。

## 高级用法

### 批量增强描述文件

为所有描述文件添加代码示例、FAQ、关系图谱：

```bash
python3 scripts/enhance_descriptions.py
```

### 生成新概念

基于搜索索引自动生成新的概念描述：

```bash
# 列出候选
python3 scripts/generate_new_descriptions.py --list

# 生成 20 个新概念
python3 scripts/generate_new_descriptions.py --count 20
```

### 更新知识库

当源码更新后，重新生成知识库：

```bash
python3 scripts/generate_knowledge.py \
  --source-dir /path/to/cangjie_compiler \
  --output-dir knowledge-base
```

## 最佳实践

### 学习新概念

1. 先搜索概念获取概览
2. 查看描述文件了解详情
3. 阅读代码示例理解实现
4. 查看关系图谱了解上下文
5. 参考 FAQ 解决常见疑问

### 调试问题

1. 搜索相关概念找到涉及的模块
2. 查看相关函数列表
3. 根据文件路径定位源码
4. 查看模块依赖了解调用链

### 贡献新内容

1. 使用 generate_new_descriptions.py 生成模板
2. 手动编辑和完善描述
3. 添加更详细的使用场景
4. 补充更好的代码示例
5. 重新生成知识库

## 工具参考

### search.py
搜索概念和代码

```bash
python3 scripts/search.py <关键词>
```

### enhance_descriptions.py
增强描述文件

```bash
python3 scripts/enhance_descriptions.py [--keyword <关键词>] [--no-examples] [--no-faq] [--no-graph]
```

### generate_new_descriptions.py
生成新描述文件

```bash
python3 scripts/generate_new_descriptions.py [--list] [--count <数量>] [--min-functions <最小函数数>]
```

### visualize_concept_graph.py
生成关系图谱

```bash
python3 scripts/visualize_concept_graph.py --keyword <关键词> [--output <文件>]
python3 scripts/visualize_concept_graph.py --module <模块> [--output <文件>]
```

### generate_knowledge.py
生成知识库

```bash
python3 scripts/generate_knowledge.py --source-dir <源码目录> --output-dir <输出目录>
```

## 常见问题

### Q: 搜索不到某个概念怎么办？

A: 可能是该概念还没有描述文件。使用 `generate_new_descriptions.py --list` 查看候选关键词，然后生成新的描述文件。

### Q: 代码示例不够详细？

A: 代码示例是自动提取的。你可以：
1. 根据文件路径和行号查看完整源码
2. 手动编辑描述文件添加更好的示例

### Q: 如何更新知识库？

A: 当源码更新后，运行 `generate_knowledge.py` 重新生成知识库，然后运行 `enhance_descriptions.py` 更新代码示例。

### Q: 关系图谱显示不全？

A: 默认只显示部分关系以保持清晰。你可以：
1. 修改 `visualize_concept_graph.py` 中的限制
2. 查看描述文件中的完整关系列表

## 总结

Cangjie Compiler Knowledge Skill 现在提供：

✅ 100+ 个概念的详细描述
✅ 中英文双语支持
✅ 真实代码示例
✅ 常见问题解答
✅ 概念关系图谱
✅ 模块依赖可视化
✅ 自动化维护工具

这使得 AI 能够快速、全面地了解仓颉编译器，大大提升学习效率！
