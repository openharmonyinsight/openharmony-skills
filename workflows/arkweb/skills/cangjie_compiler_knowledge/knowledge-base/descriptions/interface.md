---
keyword: interface
synonyms: [接口, 接口定义, interface definition, 抽象, abstract, 契约, contract]
related: [class, struct, extend, implement, 实现]
category: language-feature
---

# 接口 (Interface)

## 中文描述
接口定义了一组方法签名的契约,类和结构体可以实现接口来提供具体实现。接口支持多接口实现,是实现多态和解耦的重要机制。

## English Description
Interface defines a contract of method signatures that classes and structs can implement to provide concrete implementations. Interfaces support multiple interface implementation and are an important mechanism for achieving polymorphism and decoupling.

## 使用场景
- 定义类型契约
- 实现多态
- 依赖注入
- 多接口实现

## 相关实现
- 接口声明解析在 Parse/ParseDecl.cpp
- 接口实现检查在 Sema/TypeCheckClassLike.cpp
- 关键类: InterfaceDecl, InterfaceType

## 代码示例

### 示例 1: GetSuperInterfaceTys
文件: `include/cangjie/AST/Node.h:1048`

```cpp
std::set<Ptr<InterfaceTy>> GetSuperInterfaceTys() const;
    std::vector<Ptr<InterfaceTy>> GetStableSuperInterfaceTys() const;
    // guarantees sub-types always exist before super-types
    std::vector<Ptr<AST::ClassLikeDecl>> GetAllSuperDecls();

protected:
    InheritableDecl(ASTKind kind) : Decl(kind)
    {
    }
};

enum class BuiltInType : uint8_t {
    ARRAY,
    POINTER,
    CSTRING,
    CFUNC,
    VARRAY,
    // Will have other builtin types.
};
```

### 示例 2: GetStableSuperInterfaceTys
文件: `include/cangjie/AST/Node.h:1049`

```cpp
std::vector<Ptr<InterfaceTy>> GetStableSuperInterfaceTys() const;
    // guarantees sub-types always exist before super-types
    std::vector<Ptr<AST::ClassLikeDecl>> GetAllSuperDecls();

protected:
    InheritableDecl(ASTKind kind) : Decl(kind)
    {
    }
};

enum class BuiltInType : uint8_t {
    ARRAY,
    POINTER,
    CSTRING,
    CFUNC,
    VARRAY,
    // Will have other builtin types.
};

/**
```

### 示例 3: IsInterface
文件: `include/cangjie/AST/Types.h:187`

```cpp
bool IsInterface() const;
    /** Return whether a ty is intersection.
     * U: Sema.
     */
    bool IsIntersection() const;
    /** Return whether a ty is union.
     * U: Sema.
     */
    bool IsUnion() const;
    /** Return whether a ty is nominal.
     * U: Sema.
     */
    bool IsNominal() const;
    /** Return whether a ty is built-in RawArray.
     * U: Sema, GenericInstantiator, HLIRCodeGen, LLVMCodeGen, Utils.
     */
    bool IsArray() const;
    /** Return whether a ty is struct Array that defined in core package.
     * U: Sema, GenericInstantiator, HLIRCodeGen, LLVMCodeGen, Utils.
     */
```

## 概念关系图谱

- **同义词**: 接口, 接口定义, interface definition, 抽象, abstract, 契约, contract
- **相关概念**: class, struct, extend, implement, 实现
- **相关模块**: chir, codegen, include, macro, modules, parse, sema

## 常见问题

### interface 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 interface？

请参考下面的代码示例部分。

### interface 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

