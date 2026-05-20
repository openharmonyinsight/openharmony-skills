---
keyword: info
synonyms: []
related: []
category: compiler-feature
---

# Info

## 中文描述
info 是仓颉编译器中的一个重要概念。

## English Description
info is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, basic, chir, codegen, conditionalcompilation
- 主要类: DemangleInfo, FloatTypeInfo, DiagnosticInfo, InstCalleeInfo, LeftValueInfo
- 主要函数: CopyBasicInfo, CopyNodeScopeInfo, GetFloatTypeInfoByKind, GetDiagnosticInfo, CollectStaticInitFuncInfo

## 代码示例

### 示例 1: CopyBasicInfo
文件: `include/cangjie/AST/Clone.h:26`

```cpp
// 代码示例待提取
```

### 示例 2: CopyNodeScopeInfo
文件: `include/cangjie/AST/Create.h:23`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: ast, basic, chir, codegen, conditionalcompilation, demangler, driver, frontend, frontendtool, include

## 常见问题

### info 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 info？

请参考上面的代码示例部分。

### info 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
