---
keyword: with
synonyms: []
related: []
category: compiler-feature
---

# With

## 中文描述
with 是仓颉编译器中的一个重要概念。

## English Description
with is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: basic, chir, codegen, driver, include
- 主要类: VarWithPatternDecl, VarDeclWithPosition, ExpressionWithException, FuncCallWithException, ApplyWithException
- 主要函数: StoreOuterVarWithPatternDecl, CloneWithRearrange, CopyNodeWithFileID, IsCommonMatchedWithSpecific, GetImportedPackageNameWithIsDecl

## 代码示例

### 示例 1: StoreOuterVarWithPatternDecl
文件: `include/cangjie/AST/ASTContext.h:116`

```cpp
// 代码示例待提取
```

### 示例 2: CloneWithRearrange
文件: `include/cangjie/AST/Clone.h:59`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: basic, chir, codegen, driver, include, incrementalcompilation, macro, mangle, modules, parse

## 常见问题

### with 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 with？

请参考上面的代码示例部分。

### with 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
