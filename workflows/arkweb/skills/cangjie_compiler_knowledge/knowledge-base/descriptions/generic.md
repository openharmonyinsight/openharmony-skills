---
keyword: generic
synonyms: [泛型, generics, template, 模板, type parameter, 类型参数, parametric polymorphism]
related: [type, class, interface, function, instantiation, 实例化]
category: language-feature
---

# 泛型 (Generics)

## 中文描述
泛型是一种参数化类型的机制,允许在定义类、接口或函数时使用类型参数,在使用时再指定具体类型。泛型提供了类型安全的代码复用,避免了类型转换和运行时错误。

## English Description
Generics are a mechanism for parameterized types, allowing type parameters to be used when defining classes, interfaces, or functions, with concrete types specified at usage time. Generics provide type-safe code reuse while avoiding type casts and runtime errors.

## 使用场景
- 泛型类(如 Array<T>, HashMap<K,V>)
- 泛型函数(如 map<T,R>, filter<T>)
- 泛型接口
- 类型约束(type constraints)
- 泛型实例化(generic instantiation)

## 相关实现
- 泛型参数解析在 Parse 模块
- 泛型约束检查在 Sema/TypeCheckGeneric.cpp
- 泛型实例化在 Sema/GenericInstantiation/ 目录
- 类型参数推断(type argument inference)

## 代码示例

### 示例 1: GetGenericConstraints
文件: `demangler/Demangler.h:152`

```cpp
T GetGenericConstraints() const;
    T GetGenericTypes() const;
    T GetFunctionName() const;
    T GetGenericConstraintsName() const;
    bool isValid{ true };
};

template<typename T>
class Demangler {
public:
    /**
     * @brief The constructor of class Demangler.
     *
     * @param mangled The name to be demangled.
     * @param stripUnderscore Whether the mangled name needs to strip underscore.
     * @param scopeRes The scope resolution.
     * @param genericParamFilter The function to filter generic param.
     * @return Demangler The instance of Demangler.
     */
    explicit Demangler(
```

### 示例 2: GetGenericTypes
文件: `demangler/Demangler.h:153`

```cpp
T GetGenericTypes() const;
    T GetFunctionName() const;
    T GetGenericConstraintsName() const;
    bool isValid{ true };
};

template<typename T>
class Demangler {
public:
    /**
     * @brief The constructor of class Demangler.
     *
     * @param mangled The name to be demangled.
     * @param stripUnderscore Whether the mangled name needs to strip underscore.
     * @param scopeRes The scope resolution.
     * @param genericParamFilter The function to filter generic param.
     * @return Demangler The instance of Demangler.
     */
    explicit Demangler(
        const T& mangled,
```

### 示例 3: GetGenericConstraintsName
文件: `demangler/Demangler.h:155`

```cpp
T GetGenericConstraintsName() const;
    bool isValid{ true };
};

template<typename T>
class Demangler {
public:
    /**
     * @brief The constructor of class Demangler.
     *
     * @param mangled The name to be demangled.
     * @param stripUnderscore Whether the mangled name needs to strip underscore.
     * @param scopeRes The scope resolution.
     * @param genericParamFilter The function to filter generic param.
     * @return Demangler The instance of Demangler.
     */
    explicit Demangler(
        const T& mangled,
        const bool stripUnderscore,
        const T& scopeRes, std::function<T(const T&)> genericParamFilter)
```

## 概念关系图谱

- **同义词**: 泛型, generics, template, 模板, type parameter, 类型参数, parametric polymorphism
- **相关概念**: type, class, interface, function, instantiation, 实例化
- **相关模块**: ast, basic, chir, codegen, demangler, driver, frontendtool, include, macro, mangle, modules, parse, sema, unittests

## 常见问题

### generic 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 generic？

请参考下面的代码示例部分。

### generic 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

