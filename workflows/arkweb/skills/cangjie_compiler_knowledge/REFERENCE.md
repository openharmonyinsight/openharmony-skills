# Cangjie Compiler Knowledge Reference

## Script Arguments

脚本：`scripts/search.py`。可选 `--base-dir <path>` 覆盖知识库根目录。

| 子命令 | 参数 | 说明 |
|--------|------|------|
| `search` | `<query>`（中英文） | 在知识库中检索概念、模块、类、函数等 |
| `module` | `<module_name>` | 显示指定模块的详细信息 |
| `concept` | `<concept_name>` | 显示指定概念的详细说明 |
| `graph` | `<concept_name>` | 显示概念关系图 |

可选全局参数：
- `--compiler-path <path>` — 指向 cangjie_compiler 仓库根目录
- `--format {text|json}` — 输出格式（默认 text）
- `--limit <n>` — 限制搜索结果数量（默认 10）

## 知识库结构

| 目录 | 说明 |
|------|------|
| `knowledge-base/descriptions/` | 概念描述文档（Markdown） |
| `knowledge-base/modules/` | 模块信息（JSON） |
| `knowledge-base/graphs/` | 概念关系图（Mermaid） |
| `knowledge-base/search-index.json` | 搜索索引 |
| `knowledge-base/cross-references.json` | 交叉引用索引 |

## 检索策略

1. **关键词搜索**：使用 `search` 命令搜索任意关键词
   - 支持中英文混合搜索
   - 自动匹配概念、模块、类名、函数名
   - 返回相关度排序的结果

2. **模块查询**：使用 `module` 命令查看模块详情
   - 显示模块的源码目录、依赖关系
   - 列出模块中的主要类和函数
   - 提供相关概念链接

3. **概念查询**：使用 `concept` 命令查看概念说明
   - 显示概念的详细描述
   - 列出相关的源码位置
   - 提供交叉引用链接

4. **关系图查询**：使用 `graph` 命令查看概念关系
   - 显示概念之间的依赖关系
   - 可视化模块间的交互
   - 帮助理解编译器架构

## 覆盖范围

- **模块数量**：18 个核心模块
- **概念文档**：60+ 个编译器概念
- **源码文件**：714 个 C++ 源文件
- **类定义**：1036 个类/结构体
- **关系图**：多个概念关系图和模块依赖图

## 使用示例

```bash
# 搜索类型检查相关内容
python scripts/search.py search "类型检查"

# 查看 sema 模块详情
python scripts/search.py module sema

# 查看 lambda 概念说明
python scripts/search.py concept lambda

# 显示 sema 模块的概念关系图
python scripts/search.py graph sema
```

## 维护指南

详见 `AI_MAINTENANCE_GUIDE.md`，包含：
- 知识库更新流程
- 索引重建方法
- 概念文档编写规范
- 关系图生成工具使用
