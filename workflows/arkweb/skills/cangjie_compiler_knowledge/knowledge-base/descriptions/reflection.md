---
keyword: reflection
synonyms: [反射, 注解, annotation, 元数据, metadata, 运行时类型信息, RTTI]
related: [macro, 类型, type, 属性, attribute]
category: language-feature
---

# 反射和注解 (Reflection and Annotation)

## 中文描述
反射提供运行时类型信息查询能力,注解用于为代码元素添加元数据。注解可以在编译期或运行时被处理,用于实现依赖注入、序列化等功能。

## English Description
Reflection provides runtime type information query capabilities, and annotations are used to add metadata to code elements. Annotations can be processed at compile-time or runtime, used to implement dependency injection, serialization, etc.

## 使用场景
- 运行时类型查询
- 注解处理
- 依赖注入
- 序列化/反序列化

## 相关实现
- 注解解析在 Parse/ParseAnnotation.cpp
- 注解分析在 Sema/AnnotationAnalysis.cpp
- 关键类: Annotation, AnnotationDecl, ReflectionInfo

## 代码示例

### 示例 1: ReprocessReflectionOption
文件: `include/cangjie/Option/Option.h:1179`

```cpp
bool ReprocessReflectionOption();
    bool CheckScanDependencyOptions() const;
    bool CheckSanitizerOptions() const;
    bool CheckLtoOptions() const;
    bool CheckOutputModeOptions();
    bool CheckCompileAsExeOptions() const;
    bool CheckPgoOptions() const;
    bool CheckCompileMacro() const;
    void RefactJobs();
    void RefactAggressiveParallelCompileOption();
    void DisableStaticStdForOhos();

    bool ProcessInputs(const std::vector<std::string>& inputs);
    bool HandleArchiveExtension(DiagnosticEngine& diag, const std::string& value);
    bool HandleCJOExtension(DiagnosticEngine& diag, const std::string& value);
    bool HandleCJExtension(DiagnosticEngine& diag, const std::string& value);
    bool HandleCHIRExtension(DiagnosticEngine& diag, const std::string& value);
    bool HandleCJDExtension(DiagnosticEngine& diag, const std::string& value);
    bool HandleBCExtension(DiagnosticEngine& diag, const std::string& value);
    bool HandleNoExtension(DiagnosticEngine& diag, const std::string& value);
```

### 示例 2: GenReflectionOfTypeInfo
文件: `src/CodeGen/Base/CGTypes/CGCustomType.h:32`

```cpp
llvm::Constant* GenReflectionOfTypeInfo() override;

    llvm::Constant* GenNameOfTypeTemplate();
    llvm::Constant* GenKindOfTypeTemplate();
    llvm::Constant* GenTypeArgsNumOfTypeTemplate();

    bool IsSized() const;

    virtual void PreActionOfGenTypeTemplate() {}
    virtual void PostActionOfGenTypeTemplate() {}
    virtual llvm::Constant* GenFieldsNumOfTypeTemplate();
    virtual llvm::Constant* GenFieldsFnsOfTypeTemplate();
    virtual llvm::Constant* GenSuperFnOfTypeTemplate();
    virtual llvm::Constant* GenFinalizerOfTypeTemplate();

private:
    CGCustomType() = delete;
    void GenTypeTemplate() override;
};
} // namespace CodeGen
```

### 示例 3: GenerateReflectionMetadata
文件: `src/CodeGen/CJNative/CJNativeMetadata.h:285`

```cpp
void GenerateReflectionMetadata(CGModule& module, const SubCHIRPackage& subCHIRPkg);

} // namespace CodeGen
} // namespace Cangjie
#endif
```

## 概念关系图谱

- **同义词**: 反射, 注解, annotation, 元数据, metadata, 运行时类型信息, RTTI
- **相关概念**: macro, 类型, type, 属性, attribute
- **相关模块**: codegen, include

## 常见问题

### reflection 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 reflection？

请参考下面的代码示例部分。

### reflection 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

