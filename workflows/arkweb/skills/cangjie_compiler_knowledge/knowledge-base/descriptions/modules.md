---
keyword: modules
synonyms: [模块系统, module system, import, export, package management, 包管理]
related: [package, import, dependency, compilation-unit]
category: compiler-module
---

# 模块系统 (Modules)

## 中文描述

模块系统负责管理仓颉程序的模块化组织、包依赖、导入导出等功能。模块系统是编译器的基础设施，贯穿编译的各个阶段。主要功能包括：
- 包的加载和解析
- 模块依赖图的构建和验证
- 符号的导入和导出管理
- 模块接口的序列化和反序列化
- 增量编译支持
- 循环依赖检测

模块系统的核心概念：
- **Package（包）**: 代码的顶层组织单元，对应一个独立的编译单元
- **Module（模块）**: 包内的逻辑组织单元，通常对应一个源文件
- **Import（导入）**: 引用其他包或模块的符号
- **Export（导出）**: 声明对外可见的符号

## English Description

The Modules system manages the modular organization, package dependencies, import/export functionality of Cangjie programs. The module system is the infrastructure of the compiler, spanning all compilation stages. Main functions include:
- Package loading and parsing
- Module dependency graph construction and validation
- Symbol import and export management
- Module interface serialization and deserialization
- Incremental compilation support
- Circular dependency detection

Core concepts of the module system:
- **Package**: Top-level code organization unit, corresponding to an independent compilation unit
- **Module**: Logical organization unit within a package, usually corresponding to a source file
- **Import**: Reference symbols from other packages or modules
- **Export**: Declare publicly visible symbols

## 使用场景

- 管理大型项目的代码组织
- 处理包之间的依赖关系
- 实现符号的可见性控制
- 支持增量编译和并行编译
- 生成和加载模块接口文件
- 检测和报告循环依赖

## 相关实现

- **主要模块**: `src/Modules/`
- **核心类**:
  - `Package` - 包的表示
  - `Module` - 模块的表示
  - `PackageManager` - 包管理器
  - `ImportManager` - 导入管理器
  - `DependencyGraph` - 依赖图
  - `ModuleInterface` - 模块接口
- **关键函数**:
  - `LoadPackage()` - 加载包
  - `ResolveImport()` - 解析导入
  - `BuildDependencyGraph()` - 构建依赖图
  - `SerializeModule()` - 序列化模块接口
  - `CheckCircularDependency()` - 检测循环依赖
- **相关文件**:
  - `schema/ModuleFormat.fbs` - 模块序列化格式
  - `schema/PackageFormat.fbs` - 包序列化格式
- **依赖模块**: Basic, AST
- **被依赖**: Parse, Sema, Frontend, Driver

## 代码示例

### 示例 1: ClearPackageModules
文件: `include/cangjie/CodeGen/EmitPackageIR.h:50`

```cpp
void ClearPackageModules(std::vector<std::unique_ptr<llvm::Module>>& packageModules);
} // namespace Cangjie::CodeGen

#endif // CANGJIE_EMITPACKAGEIR_H
```

### 示例 2: DetectCangjieModules
文件: `include/cangjie/Frontend/CompilerInstance.h:579`

```cpp
bool DetectCangjieModules();

    // Merged source packages and imported packages.
    std::vector<Ptr<AST::Package>> pkgs;

    // Package to ASTContext map.
    std::unordered_map<Ptr<AST::Package>, std::unique_ptr<ASTContext>> pkgCtxMap;

    std::vector<std::string> depPackageInfo;

    virtual void UpdateCachedInfo();
    bool WriteCachedInfo();
    bool ShouldWriteCacheFile() const;

#ifdef CANGJIE_CODEGEN_CJNATIVE_BACKEND
    std::vector<HANDLE> pluginHandles;
#endif
};
} // namespace Cangjie
#endif // CANGJIE_FRONTEND_COMPILERINSTANCE_H
```

### 示例 3: ReleaseLLVMModules
文件: `src/CodeGen/CGPkgContext.h:81`

```cpp
std::vector<std::unique_ptr<llvm::Module>> ReleaseLLVMModules();

#ifdef CANGJIE_CODEGEN_CJNATIVE_BACKEND
    void AddLocalizedSymbol(const std::string& symName);
    const std::set<std::string>& GetLocalizedSymbols();
#endif

    void CollectSubTypeMap();
    bool NeedOuterTypeInfo(const CHIR::ClassType& classType);

    CHIR::Value* FindCHIRGlobalValue(const std::string& mangledName);

    CHIR::CHIRBuilder& chirBuilder;

private:
    const CHIRData& chirData;
    const GlobalOptions& options;
    const bool enableIncrement;
    CachedMangleMap correctedCachedMangleMap;
```

## 概念关系图谱

- **同义词**: 模块系统, module system, import, export, package management, 包管理
- **相关概念**: package, import, dependency, compilation-unit
- **相关模块**: codegen, frontendtool, include, modules, sema, unittests

## 常见问题

### modules 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 modules？

请参考下面的代码示例部分。

### modules 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

