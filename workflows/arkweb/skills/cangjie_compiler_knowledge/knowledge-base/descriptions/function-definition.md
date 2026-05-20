---
keyword: function definition
synonyms: [function]
related: [lambda, closure, overload, generic, 参数, parameter, 返回值, return]
category: compiler-feature
---

# Function Definition

## 中文描述
函数是仓颉语言中的基本代码组织单元,支持命名函数、匿名函数(lambda)、闭包、高阶函数、函数重载等特性。函数可以作为一等公民传递和返回。

## English Description
Function is the basic code organization unit in Cangjie language, supporting named functions, anonymous functions (lambda), closures, higher-order functions, function overloading, etc. Functions can be passed and returned as first-class citizens.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, basic, chir, codegen, conditionalcompilation
- 主要类: FunctionInline, CGFunctionType, CGFunction, CGFunctionType, CGFunction
- 主要函数: GetIdentifier, GetReturnType, IsFunctionLike, IsValid, MatchSuffix

## 代码示例

### 示例 1: GetIdentifier
文件: `demangler/Demangler.h:127`

```cpp
// 代码示例待提取
```

### 示例 2: GetReturnType
文件: `demangler/Demangler.h:134`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: function
- **相关概念**: lambda, closure, overload, generic, 参数, parameter, 返回值, return
- **相关模块**: ast, basic, chir, codegen, conditionalcompilation, demangler, driver, frontend, frontendtool, include

## 常见问题

### function definition 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 function definition？

请参考上面的代码示例部分。

### function definition 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
