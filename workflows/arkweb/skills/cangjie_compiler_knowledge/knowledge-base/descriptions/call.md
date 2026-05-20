---
keyword: call
synonyms: []
related: []
category: compiler-feature
---

# Call

## 中文描述
call 是仓颉编译器中的一个重要概念。

## English Description
call is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, basic, chir, codegen, include
- 主要类: CallExpr, CallExpr, CallGraph, CallGraphAnalysis, FuncCallContext
- 主要函数: IsNodeInOriginalMacroCallNodes, GetMacroCallPos, GetMacroCallNewPos, RecoverCallFromArrayExpr, RecoverJArrayCtorCall

## 代码示例

### 示例 1: IsNodeInOriginalMacroCallNodes
文件: `include/cangjie/AST/ASTContext.h:202`

```cpp
// 代码示例待提取
```

### 示例 2: GetMacroCallPos
文件: `include/cangjie/AST/Node.h:463`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: ast, basic, chir, codegen, include, macro, modules, parse, sema

## 常见问题

### call 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 call？

请参考上面的代码示例部分。

### call 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
