---
keyword: struct
synonyms: [结构体, 值类型, value type, structure]
related: [class, interface, generic, 成员, member]
category: language-feature
---

# 结构体 (Struct)

## 中文描述
结构体是仓颉语言中的值类型,用于定义轻量级的数据结构。与类不同,结构体采用值语义,在赋值和传参时会进行拷贝。结构体可以实现接口但不支持继承。

## English Description
Struct is a value type in Cangjie language, used to define lightweight data structures. Unlike classes, structs use value semantics and are copied during assignment and parameter passing. Structs can implement interfaces but do not support inheritance.

## 使用场景
- 定义简单的数据结构
- 需要值语义的场景
- 性能敏感的小型对象
- 不可变数据类型

## 相关实现
- 结构体声明解析在 Parse/ParseDecl.cpp
- 类型检查在 Sema/TypeCheckClassLike.cpp
- 关键类: StructDecl, StructType

## 代码示例

### 示例 1: IsStruct
文件: `include/cangjie/AST/Types.h:171`

```cpp
bool IsStruct() const;
    /** Return whether a ty is enum.
     * U: Sema, GenericInstantiator, LLVMCodeGen.
     */
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
```

### 示例 2: IsStructArray
文件: `include/cangjie/AST/Types.h:207`

```cpp
bool IsStructArray() const;
    /** Return whether a ty is CPointer.
     * U: Sema, HLIRCodeGen, LLVMCodeGen, CHIR.
     */
    bool IsPointer() const;
    /** Return whether a ty is CFunc.
     * U: Sema, HLIRCodeGen, LLVMCodeGen.
     */
    virtual bool IsCFunc() const
    {
        return false;
    };
    /** Return whether a ty is C char *.
     * U: Sema, CodeGen, AST, CHIR
     */
    bool IsCString() const;
    /** Return whether a ty is erase generic.
     * U: Sema.
     */
    bool IsEraseGeneric() const;
```

### 示例 3: StructTy
文件: `include/cangjie/AST/Types.h:1108`

```cpp
StructTy(const std::string& name, StructDecl& sd, const std::vector<Ptr<Ty>>& typeArgs);
    /** Return the unique name of a ty.
     * U: ImportManager, Sema, AST2CHIR, CHIR, HLIRCodeGen, LLVMCodeGen.
     */
    std::string String() const override;
    /** Return all the super interface types.
     * U: Sema, GenericInstantiator.
     */
    std::set<Ptr<InterfaceTy>> GetSuperInterfaceTys() const;
    /**
     * Generic struct type pointer.
     * W: ImportManager, Sema.
     * R: Sema.
     */
    Ptr<StructTy> GetGenericTy() const;
    size_t Hash() const override;
    bool operator==(const Ty& other) const override;
};

bool CompTyByNames(Ptr<const Ty> ty1, Ptr<const Ty> ty2);
```

## 概念关系图谱

- **同义词**: 结构体, 值类型, value type, structure
- **相关概念**: class, interface, generic, 成员, member
- **相关模块**: ast, basic, chir, codegen, demangler, driver, frontend, include, incrementalcompilation, lex, macro, main-chir-dis.cpp, main-macrosrv.cpp, mangle, modules, parse, sema, unittests, utils

## 常见问题

### struct 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 struct？

请参考下面的代码示例部分。

### struct 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

