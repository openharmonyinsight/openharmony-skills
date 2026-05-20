---
keyword: function
synonyms: [函数, func, 方法, method, 函数定义, function definition, 函数调用, function call]
related: [lambda, closure, overload, generic, 参数, parameter, 返回值, return]
category: language-feature
---

# 函数 (Function)

## 中文描述
函数是仓颉语言中的基本代码组织单元,支持命名函数、匿名函数(lambda)、闭包、高阶函数、函数重载等特性。函数可以作为一等公民传递和返回。

## English Description
Function is the basic code organization unit in Cangjie language, supporting named functions, anonymous functions (lambda), closures, higher-order functions, function overloading, etc. Functions can be passed and returned as first-class citizens.

## 使用场景
- 定义可复用的代码块
- 函数式编程
- 回调和事件处理
- 高阶函数和函数组合

## 相关实现
- 函数声明解析在 Parse/ParseDecl.cpp
- Lambda 表达式解析在 Parse/ParseExpr.cpp
- 函数检查在 Sema/TypeCheckDecl.cpp
- 重载解析在 Sema 模块
- 关键类: FuncDecl, FunctionType, LambdaExpr

## 代码示例

### 示例 1: GetIdentifier
文件: `demangler/Demangler.h:127`

```cpp
T GetIdentifier() const;

    /**
     * @brief Get return type.
     *
     * @return T The return type name.
     */
    T GetReturnType() const;

    /**
     * @brief Check if it functions like a function.
     *
     * @return bool If yes, true is returned. Otherwise, false is returned.
     */
    bool IsFunctionLike() const;

    /**
     * @brief Check if the demangled name is valid.
     *
     * @return bool If yes, true is returned. Otherwise, false is returned.
```

### 示例 2: GetReturnType
文件: `demangler/Demangler.h:134`

```cpp
T GetReturnType() const;

    /**
     * @brief Check if it functions like a function.
     *
     * @return bool If yes, true is returned. Otherwise, false is returned.
     */
    bool IsFunctionLike() const;

    /**
     * @brief Check if the demangled name is valid.
     *
     * @return bool If yes, true is returned. Otherwise, false is returned.
     */
    bool IsValid() const;

private:
    bool MatchSuffix(const char pattern[], uint32_t len) const;
    T GetGenericConstraints() const;
    T GetGenericTypes() const;
```

### 示例 3: IsFunctionLike
文件: `demangler/Demangler.h:141`

```cpp
bool IsFunctionLike() const;

    /**
     * @brief Check if the demangled name is valid.
     *
     * @return bool If yes, true is returned. Otherwise, false is returned.
     */
    bool IsValid() const;

private:
    bool MatchSuffix(const char pattern[], uint32_t len) const;
    T GetGenericConstraints() const;
    T GetGenericTypes() const;
    T GetFunctionName() const;
    T GetGenericConstraintsName() const;
    bool isValid{ true };
};

template<typename T>
class Demangler {
```

## 概念关系图谱

- **同义词**: 函数, func, 方法, method, 函数定义, function definition, 函数调用, function call
- **相关概念**: lambda, closure, overload, generic, 参数, parameter, 返回值, return
- **相关模块**: ast, basic, chir, codegen, conditionalcompilation, demangler, driver, frontend, frontendtool, include, incrementalcompilation, lex, macro, main-chir-dis.cpp, main-frontend.cpp, main-macrosrv.cpp, main.cpp, mangle, metatransformation, modules, option, parse, sema, unittests, utils

## 常见问题

### function 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 function？

请参考下面的代码示例部分。

### function 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

