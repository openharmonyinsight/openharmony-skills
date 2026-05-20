---
keyword: expr
synonyms: []
related: []
category: compiler-feature
---

# Expr

## 中文描述
expr 是仓颉编译器中的一个重要概念。

## English Description
expr is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, chir, codegen, conditionalcompilation, include
- 主要类: Expr, CallExpr, RefExpr, NameReferenceExpr, LitConstExpr
- 主要函数: DeleteDesugarExpr, CreateUnitExpr, CreateBreakExpr, CreateRefExpr, CreateRefExprInCore

## 代码示例

### 示例 1: DeleteDesugarExpr
文件: `include/cangjie/AST/ASTContext.h:86`

```cpp
// 代码示例待提取
```

### 示例 2: CreateUnitExpr
文件: `include/cangjie/AST/Create.h:27`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: ast, chir, codegen, conditionalcompilation, include, incrementalcompilation, macro, modules, parse, sema

## 常见问题

### expr 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 expr？

请参考上面的代码示例部分。

### expr 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
