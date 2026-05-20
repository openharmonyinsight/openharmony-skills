---
keyword: check
synonyms: []
related: []
category: compiler-feature
---

# Check

## 中文描述
check 是仓颉编译器中的一个重要概念。

## English Description
check is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, basic, chir, codegen, conditionalcompilation
- 主要类: TypeCheckCache, VarCirDepsChecker, FileCirDepsChecker, CHIRChecker, VarInitCheck
- 主要函数: ClearTypeCheckCache, RemoveTypeCheckCache, CheckOverflow, EnableCheckRangeErrorCodeRatherICE, DisableCheckRangeErrorCodeRatherICE

## 代码示例

### 示例 1: ClearTypeCheckCache
文件: `include/cangjie/AST/ASTContext.h:90`

```cpp
// 代码示例待提取
```

### 示例 2: RemoveTypeCheckCache
文件: `include/cangjie/AST/ASTContext.h:92`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: ast, basic, chir, codegen, conditionalcompilation, driver, frontend, frontendtool, include, incrementalcompilation

## 常见问题

### check 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 check？

请参考上面的代码示例部分。

### check 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
