---
keyword: reference
synonyms: [引用, 引用类型, reference type, ref, &]
related: [pointer, type-system, borrow, variable]
category: type-system
---

# 引用 (Reference)

## 中文描述

引用是仓颉类型系统中的一种类型，表示对另一个值的间接访问。编译器需要解析引用类型声明、检查引用的有效性、处理引用的解引用操作。引用类型在语法树中由 NameReferenceExpr 等节点表示。

引用的主要特性：
- 引用类型声明和推断
- 引用传递参数（避免值拷贝）
- 引用解引用操作
- 引用的生命周期分析
- 引用的可变性检查

编译器在语义分析阶段检查引用的类型安全性，确保引用指向有效的对象，并在代码生成阶段生成相应的指针操作代码。

## English Description

Reference is a type in Cangjie's type system that represents indirect access to another value. The compiler needs to parse reference type declarations, check reference validity, and handle dereference operations. Reference types are represented by nodes such as NameReferenceExpr in the AST.

Main features of references:
- Reference type declaration and inference
- Reference parameter passing (avoiding value copying)
- Reference dereference operations
- Reference lifetime analysis
- Reference mutability checking

The compiler checks reference type safety during semantic analysis, ensuring references point to valid objects, and generates corresponding pointer operation code during code generation.

## 使用场景

- 引用类型声明
- 引用传递参数（高效传递大对象）
- 引用解引用
- 引用类型检查
- 引用生命周期分析

## 相关实现

- **主要模块**: `src/Parse/`, `src/Sema/`, `src/AST/`
- **核心类**:
  - `NameReferenceExpr` - 名称引用表达式
  - `ReferenceType` - 引用类型
  - `RefType` - 引用类型（CHIR）
- **关键文件**:
  - `src/Parse/ParseExpr.cpp` - 引用表达式解析
  - `src/Sema/TypeChecker.cpp` - 引用类型检查
  - `src/AST/Node.h` - 引用表达式节点定义
- **依赖模块**: AST, Type System
- **被依赖**: Sema, CodeGen

## 代码示例

### 示例 1: IsReferenceTypeWithRefDims
文件: `include/cangjie/CHIR/IR/Type/Type.h:343`

```cpp
bool IsReferenceTypeWithRefDims(size_t dims) const;

    bool IsValueOrGenericTypeWithRefDims(size_t dims) const;

    bool IsGenericRelated() const
    {
        if (IsGeneric()) {
            return true;
        }
        for (auto arg : GetTypeArgs()) {
            if (arg->IsGenericRelated()) {
                return true;
            }
        }
        return false;
    }

    /** @brief Get hash value. */
    virtual size_t Hash() const;
```

### 示例 2: IsReference
文件: `src/CodeGen/Base/CGTypes/CGType.h:119`

```cpp
bool IsReference() const;

    bool IsFuncPtrType() const
    {
        return IsPointerType() && GetPointerElementType()->GetLLVMType()->isFunctionTy();
    }

    bool IsCGEnum() const
    {
        return cgTypeKind == CGTypeKind::CG_ENUM;
    }

    bool IsOptionLikeRef() const;

    bool IsCGRef() const
    {
        return cgTypeKind == CGTypeKind::CG_REF;
    }

    bool IsCGFunction() const
```

### 示例 3: AddNullableReference
文件: `src/CodeGen/CGContext.h:321`

```cpp
void AddNullableReference(llvm::Value* value);

    void SetBasePtr(const llvm::Value* val, llvm::Value* basePtr);
    llvm::Value* GetBasePtrOf(llvm::Value* val) const;

    void SetBoxedValueMap(llvm::Value* boxedRefVal, llvm::Value* originalNonRefVal)
    {
        (void)nonRefBox2RefMap.emplace(boxedRefVal, originalNonRefVal);
    }

    llvm::Value* GetOriginalNonRefValOfBoxedValue(llvm::Value* boxedRefVal) const
    {
        auto itor = nonRefBox2RefMap.find(boxedRefVal);
        if (itor != nonRefBox2RefMap.end()) {
            return itor->second;
        } else {
            return nullptr;
        }
    }
#endif
```

## 概念关系图谱

- **同义词**: 引用, 引用类型, reference type, ref, &
- **相关概念**: pointer, type-system, borrow, variable
- **相关模块**: codegen, include, modules, sema

## 常见问题

### reference 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 reference？

请参考下面的代码示例部分。

### reference 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

