---
keyword: pointer
synonyms: [指针, 指针类型, pointer type, raw pointer, *, 裸指针]
related: [reference, type-system, cffi, unsafe]
category: type-system
---

# 指针 (Pointer)

## 中文描述

指针是仓颉类型系统中的一种类型，主要用于 C FFI 互操作和底层编程。编译器需要解析指针类型声明、检查指针操作的安全性、生成指针相关的代码。指针类型在语法树中由 PointerExpr、PointerTy 等节点表示。

指针的主要特性：
- 指针类型声明（`*T` 表示指向 T 的指针）
- 指针解引用操作
- 指针算术运算（如果支持）
- 空指针检查
- 指针类型转换

指针主要用于与 C 代码互操作，允许直接操作内存地址。编译器在语义分析阶段检查指针操作的类型安全性，并在代码生成阶段生成相应的指针操作指令。

## English Description

Pointer is a type in Cangjie's type system, primarily used for C FFI interoperability and low-level programming. The compiler needs to parse pointer type declarations, check pointer operation safety, and generate pointer-related code. Pointer types are represented by nodes such as PointerExpr and PointerTy in the AST.

Main features of pointers:
- Pointer type declaration (`*T` represents pointer to T)
- Pointer dereference operations
- Pointer arithmetic (if supported)
- Null pointer checking
- Pointer type conversion

Pointers are mainly used for interoperating with C code, allowing direct memory address manipulation. The compiler checks pointer operation type safety during semantic analysis and generates corresponding pointer operation instructions during code generation.

## 使用场景

- C FFI 互操作（调用 C 函数、传递指针参数）
- 指针类型声明
- 指针解引用
- 指针算术运算
- 底层内存操作
- 与外部库交互

## 相关实现

- **主要模块**: `src/Parse/`, `src/Sema/`, `src/AST/`, `src/CodeGen/`
- **核心类**:
  - `PointerExpr` - 指针表达式
  - `PointerTy` - 指针类型（AST）
  - `PointerType` - 指针类型（CHIR）
  - `CPointerType` - C 指针类型
- **关键文件**:
  - `src/Parse/ParseExpr.cpp` - 指针表达式解析
  - `src/AST/Types.cpp` - 指针类型定义
  - `src/Sema/TypeChecker.cpp` - 指针类型检查
  - `src/CodeGen/` - 指针代码生成
- **依赖模块**: AST, Type System, CFFI
- **被依赖**: Sema, CodeGen, CFFI

## 代码示例

### 示例 1: DemangleCPointer
文件: `demangler/Demangler.h:260`

```cpp
DemangleInfo<T> DemangleCPointer();
    DemangleInfo<T> DemangleFunction();
    DemangleInfo<T> DemanglePrimitive();
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
```

### 示例 2: DemangleCPointer
文件: `demangler/Demangler.cpp:1451`

```cpp
return DemangleCPointer();
        case '_':
            break;
        case 'A':
            return DemangleRawArray();
        case 'V':
            return DemangleVArray();
        case 'k':
            return DemangleCStringType();
        case 'G':
            return DemangleGenericType();
        default:
            if (IsCurrentCharDigit(ch)) {
                return DemangleInfo<T>{ DemangleStringName(), TypeKind::NAME, isValid };
            } else if (IsPrimitive<T>(ch)) {
                return DemanglePrimitive();
            } else if (IsOperatorName()) {
                auto di = DemangleInfo<T>{ GetOperatorNameMap<T>(mangledName.SubStr(currentIndex, SPECIAL_NAME_LEN)),
                                           TypeKind::NAME, isValid };
                currentIndex += SPECIAL_NAME_LEN;
```

### 示例 3: ForwardCPointer
文件: `demangler/DeCompression.h:88`

```cpp
size_t ForwardCPointer(T& mangled, size_t& cnt, size_t idx);

    /**
     * @brief Get the index at the end of Array type.
     *
     * @param mangled The name needs to decompress.
     * @param cnt Record the number of new elements added to the treeIdMap.
     * @param idx The start index of the demangled name.
     * @return size_t The end index of the demangled name.
     */
    size_t ForwardArrayType(T& mangled, size_t& cnt, size_t idx);

    /**
     * @brief Get the index at the end of Generic type. e.g. G<type>
     *
     * @param mangled The name needs to decompress.
     * @param cnt Record the number of new elements added to the treeIdMap.
     * @param idx The start index of the demangled name.
     * @return size_t The end index of the demangled name.
     */
```

## 概念关系图谱

- **同义词**: 指针, 指针类型, pointer type, raw pointer, *, 裸指针
- **相关概念**: reference, type-system, cffi, unsafe
- **相关模块**: chir, codegen, demangler, frontend, include, mangle, modules, sema

## 常见问题

### pointer 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 pointer？

请参考下面的代码示例部分。

### pointer 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

