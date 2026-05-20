---
keyword: enum
synonyms: [枚举, 枚举类型, enumeration, 枚举值, enum value]
related: [pattern-match, option, case, 分支]
category: language-feature
---

# 枚举 (Enum)

## 中文描述
枚举类型用于定义一组命名的常量值。仓颉的枚举支持关联值,可以为每个枚举成员附加不同类型的数据,常与模式匹配配合使用。

## English Description
Enum type is used to define a set of named constant values. Cangjie enums support associated values, allowing different types of data to be attached to each enum member, often used with pattern matching.

## 使用场景
- 定义有限的状态集合
- 表示互斥的选项
- 与模式匹配结合使用
- 关联值的枚举

## 相关实现
- 枚举声明解析在 Parse/ParseDecl.cpp
- 枚举特性检查在 Sema/EnumSugarChecker.cpp
- 关键类: EnumDecl, EnumType, EnumConstructor

## 代码示例

### 示例 1: InsertEnumConstructor
文件: `include/cangjie/AST/ASTContext.h:137`

```cpp
void InsertEnumConstructor(const std::string& name, size_t argSize, AST::Decl& decl, bool enableMacroInLsp);
    bool IsEnumConstructor(const std::string& name) const;
    /**
     * @brief Find an enum constructor.
     * @details This function finds a constructor for an enum type with the specified name and argument size.
     *
     * @param name The name of the enum constructor.
     * @param argSize The size of the arguments for the enum constructor.
     * @return A vector of pointers to the declarations of the enum constructors that match the specified name and
     * argument size.
    */
    const std::vector<Ptr<AST::Decl>>& FindEnumConstructor(const std::string& name, size_t argSize) const;
    std::set<Ptr<AST::Decl>> Mem2Decls(const AST::MemSig& memSig);

    DiagnosticEngine& diag;
    Ptr<AST::Package> const curPackage{nullptr};
    const std::string fullPackageName;

    /** An unified table, contain all info. */
    std::list<std::unique_ptr<AST::Symbol>> symbolTable;
```

### 示例 2: IsEnumConstructor
文件: `include/cangjie/AST/ASTContext.h:138`

```cpp
bool IsEnumConstructor(const std::string& name) const;
    /**
     * @brief Find an enum constructor.
     * @details This function finds a constructor for an enum type with the specified name and argument size.
     *
     * @param name The name of the enum constructor.
     * @param argSize The size of the arguments for the enum constructor.
     * @return A vector of pointers to the declarations of the enum constructors that match the specified name and
     * argument size.
    */
    const std::vector<Ptr<AST::Decl>>& FindEnumConstructor(const std::string& name, size_t argSize) const;
    std::set<Ptr<AST::Decl>> Mem2Decls(const AST::MemSig& memSig);

    DiagnosticEngine& diag;
    Ptr<AST::Package> const curPackage{nullptr};
    const std::string fullPackageName;

    /** An unified table, contain all info. */
    std::list<std::unique_ptr<AST::Symbol>> symbolTable;
    InvertedIndex invertedIndex;
```

### 示例 3: IsEnum
文件: `include/cangjie/AST/Types.h:175`

```cpp
bool IsEnum() const;
    /** Return whether a ty is option.
     * U: Sema, CodeGen
     */
    bool IsCoreOptionType() const;
    /** Return whether a ty is class.
     * U: Sema.
     */
    bool IsClass() const;
    /** Return whether a ty is interface.
     * U: Sema.
     */
    bool IsInterface() const;
    /** Return whether a ty is intersection.
     * U: Sema.
     */
    bool IsIntersection() const;
    /** Return whether a ty is union.
     * U: Sema.
     */
```

## 概念关系图谱

- **同义词**: 枚举, 枚举类型, enumeration, 枚举值, enum value
- **相关概念**: pattern-match, option, case, 分支
- **相关模块**: chir, codegen, include, macro, mangle, modules, parse, sema, unittests

## 常见问题

### enum 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 enum？

请参考下面的代码示例部分。

### enum 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

