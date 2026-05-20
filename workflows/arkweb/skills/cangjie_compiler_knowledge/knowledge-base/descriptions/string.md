---
keyword: string
synonyms: [字符串, String, 字符串字面量, string literal, 字符串插值, string interpolation]
related: [rune, char, 字符, character, 文本, text]
category: language-feature
---

# 字符串 (String)

## 中文描述
String 是仓颉的字符串类型,支持 UTF-8 编码、字符串字面量、字符串插值、多行字符串等特性。字符串是不可变的引用类型。

## English Description
String is Cangjie's string type, supporting UTF-8 encoding, string literals, string interpolation, multi-line strings, etc. Strings are immutable reference types.

## 使用场景
- 文本处理
- 字符串拼接和格式化
- 字符串插值
- 多行字符串

## 相关实现
- 字符串字面量解析在 Parse/ParseAtom.cpp
- 字符串类型处理在 Sema 模块
- 关键类: StringType, StringLiteral

## 代码示例

### 示例 1: DemangleStringName
文件: `demangler/Demangler.h:239`

```cpp
T DemangleStringName();
    T DemangleProp();
    size_t DemangleManglingNumber();
    void DemangleFileNameNumber();
    T UIntToString(size_t value) const;
    void SkipPrivateTopLevelDeclHash();
    void DemangleFileName();
    void SkipLocalCounter();
    T DemangleArgTypes(const T& delimiter, uint32_t size = -1);
    DemangleInfo<T> DemangleNestedDecls(bool isClass = false, bool isParamInit = false);
    uint32_t DemangleLength();
    DemangleInfo<T> Reject(const T& reason = T{});
    DemangleInfo<T> DemangleNextUnit(const T& message = T{});
    DemangleInfo<T> DemangleByPrefix();
    DemangleInfo<T> DemangleClass(TypeKind typeKind);
    DemangleInfo<T> DemangleCFuncType();
    DemangleInfo<T> DemangleTuple();
    DemangleInfo<T> DemangleCommonDecl(bool isClass = false);
    DemangleInfo<T> DemangleDecl();
    DemangleInfo<T> DemangleRawArray();
```

### 示例 2: UIntToString
文件: `demangler/Demangler.h:243`

```cpp
T UIntToString(size_t value) const;
    void SkipPrivateTopLevelDeclHash();
    void DemangleFileName();
    void SkipLocalCounter();
    T DemangleArgTypes(const T& delimiter, uint32_t size = -1);
    DemangleInfo<T> DemangleNestedDecls(bool isClass = false, bool isParamInit = false);
    uint32_t DemangleLength();
    DemangleInfo<T> Reject(const T& reason = T{});
    DemangleInfo<T> DemangleNextUnit(const T& message = T{});
    DemangleInfo<T> DemangleByPrefix();
    DemangleInfo<T> DemangleClass(TypeKind typeKind);
    DemangleInfo<T> DemangleCFuncType();
    DemangleInfo<T> DemangleTuple();
    DemangleInfo<T> DemangleCommonDecl(bool isClass = false);
    DemangleInfo<T> DemangleDecl();
    DemangleInfo<T> DemangleRawArray();
    DemangleInfo<T> DemangleVArray();
    DemangleInfo<T> DemangleCPointer();
    DemangleInfo<T> DemangleFunction();
    DemangleInfo<T> DemanglePrimitive();
```

### 示例 3: DemangleCStringType
文件: `demangler/Demangler.h:263`

```cpp
DemangleInfo<T> DemangleCStringType();
    DemangleInfo<T> DemangleGenericType();
    DemangleInfo<T> DemangleDefaultParamFunction();
    DemangleInfo<T> DemangleInnerFunction();
    DemangleInfo<T> DemangleType();
    DemangleInfo<T> DemangleGenericTypes();
    DemangleInfo<T> DemangleFunctionParameterTypes();
    DemangleInfo<T> DemangleGlobalInit();
    DemangleInfo<T> DemangleParamInit();
    DemangleInfo<T> DemangleWrappedFunction();

    bool IsFileName() const;
    bool IsProp() const;
    bool IsInnerFunction() const;
    bool IsMaybeDefaultFuncParamFunction() const;
    bool IsOperatorName() const;
    bool IsGlobalInit() const;
    bool IsParamInit() const;
    bool IsCFunctionWrapper() const;
    bool IsWrappedFunction() const;
```

## 概念关系图谱

- **同义词**: 字符串, String, 字符串字面量, string literal, 字符串插值, string interpolation
- **相关概念**: rune, char, 字符, character, 文本, text
- **相关模块**: ast, basic, chir, codegen, conditionalcompilation, demangler, driver, include, incrementalcompilation, lex, macro, mangle, option, parse, sema, unittests, utils

## 常见问题

### string 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 string？

请参考下面的代码示例部分。

### string 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

