---
keyword: cffi
synonyms: [C FFI, foreign function interface, 外部函数接口, C interop, C互操作]
related: [extern, 外部函数, foreign, 类型映射, type mapping]
category: language-feature
---

# C FFI (C Foreign Function Interface)

## 中文描述
C FFI 允许仓颉代码调用 C 语言函数,实现与 C 库的互操作。支持 C 类型映射、外部函数声明、内存管理等特性,可以直接使用现有的 C 生态。

## English Description
C FFI allows Cangjie code to call C language functions, enabling interoperability with C libraries. Supports C type mapping, external function declarations, memory management, etc., allowing direct use of existing C ecosystem.

## 使用场景
- 调用 C 库函数
- 系统编程
- 性能关键代码
- 复用现有 C 代码

## 相关实现
- C FFI 代码生成在 CodeGen/CFFI.cpp
- 外部函数类型检查在 Sema 模块
- 关键类: ExternFuncDecl, CFFITypeMapper

## 代码示例

### 示例 1: CFFIFuncWrapper
文件: `include/cangjie/CHIR/CHIR.h:175`

```cpp
void CFFIFuncWrapper();
    void ReplaceSrcCodeImportedValueWithSymbol();
    void Canonicalization();
    void UpdateMemberVarPath();

    template <typename T>
    std::pair<Value*, Apply*> DoCFFIFuncWrapper(T& curFunc, bool isForeign, bool isExternal = true);

    template <typename T> bool IsAllApply(const T* curFunc);

    CompilerInstance& ci;
    const GlobalOptions& opts;
    TypeManager* typeManager;
    SourceManager& sourceManager;
    ImportManager& importManager;
    const GenericInstantiationManager* gim;
    DiagnosticEngine& diagEngine;
    const std::string& cangjieHome;
    AST::Package& pkg;
    std::string outputPath;
```

### 示例 2: IsCFFIWrapper
文件: `include/cangjie/CHIR/IR/Value/Value.h:667`

```cpp
bool IsCFFIWrapper() const;
    void SetCFFIWrapper(bool isWrapper);

    FuncBase* GetParamDftValHostFunc() const;
    void SetParamDftValHostFunc(FuncBase& hostFunc);
    void ClearParamDftValHostFunc();

    // ===--------------------------------------------------------------------===//
    // Signature Infomation
    // ===--------------------------------------------------------------------===//
    void SetOriginalLambdaInfo(const FuncSigInfo& info);
    FuncType* GetOriginalLambdaType() const;
    std::vector<GenericType*> GetOriginalGenericTypeParams() const;

    size_t GetNumOfParams() const;
    FuncType* GetFuncType() const;
    Type* GetReturnType() const;

    const std::vector<GenericType*>& GetGenericTypeParams() const;
```

### 示例 3: SetCFFIWrapper
文件: `include/cangjie/CHIR/IR/Value/Value.h:668`

```cpp
void SetCFFIWrapper(bool isWrapper);

    FuncBase* GetParamDftValHostFunc() const;
    void SetParamDftValHostFunc(FuncBase& hostFunc);
    void ClearParamDftValHostFunc();

    // ===--------------------------------------------------------------------===//
    // Signature Infomation
    // ===--------------------------------------------------------------------===//
    void SetOriginalLambdaInfo(const FuncSigInfo& info);
    FuncType* GetOriginalLambdaType() const;
    std::vector<GenericType*> GetOriginalGenericTypeParams() const;

    size_t GetNumOfParams() const;
    FuncType* GetFuncType() const;
    Type* GetReturnType() const;

    const std::vector<GenericType*>& GetGenericTypeParams() const;

    // ===--------------------------------------------------------------------===//
```

## 概念关系图谱

- **同义词**: C FFI, foreign function interface, 外部函数接口, C interop, C互操作
- **相关概念**: extern, 外部函数, foreign, 类型映射, type mapping
- **相关模块**: chir, codegen, include, sema

## 常见问题

### cffi 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 cffi？

请参考下面的代码示例部分。

### cffi 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

