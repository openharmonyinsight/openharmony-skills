---
keyword: collect
synonyms: []
related: []
category: compiler-feature
---

# Collect

## 中文描述
collect 是仓颉编译器中的一个重要概念。

## English Description
collect is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, basic, chir, codegen, frontend
- 主要类: Collector, CollectLocalConstDecl, ConstMemberVarCollector, MacroCollector, CollectedInfo
- 主要函数: CollectTargets, Collect, CollectImplicitFuncs, CollectImportedDecls, CollectDeclsInCurPkg

## 代码示例

### 示例 1: CollectTargets
文件: `include/cangjie/AST/Cache.h:78`

```cpp
// 代码示例待提取
```

### 示例 2: Collect
文件: `include/cangjie/CHIR/AST2CHIR/CollectLocalConstDecl/CollectLocalConstDecl.h:23`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: ast, basic, chir, codegen, frontend, frontendtool, include, incrementalcompilation, lex, macro

## 常见问题

### collect 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 collect？

请参考上面的代码示例部分。

### collect 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
