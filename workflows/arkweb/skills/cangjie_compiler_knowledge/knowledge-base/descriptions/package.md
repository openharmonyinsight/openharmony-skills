---
keyword: package
synonyms: [包, 模块, module, import, 导入, export, 导出, 包管理, package management]
related: [namespace, 命名空间, 依赖, dependency]
category: language-feature
---

# 包管理 (Package Management)

## 中文描述
包是仓颉的代码组织和模块化单元,使用 package 声明包名,使用 import 导入其他包。包系统支持依赖管理、版本控制、可见性控制等特性。

## English Description
Package is Cangjie's code organization and modularization unit, using package to declare package name and import to import other packages. The package system supports dependency management, version control, visibility control, etc.

## 使用场景
- 代码模块化
- 依赖管理
- 命名空间隔离
- 可见性控制

## 相关实现
- 包管理在 Modules/PackageManager.cpp
- 导入处理在 Modules/ImportManager.cpp
- 依赖图在 Modules/DependencyGraph.cpp
- 关键类: Package, Module, ImportDecl, PackageManager

## 代码示例

### 示例 1: DemanglePackageName
文件: `demangler/Demangler.h:238`

```cpp
DemangleInfo<T> DemanglePackageName();
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
```

### 示例 2: ForwardPackageName
文件: `demangler/DeCompression.h:118`

```cpp
size_t ForwardPackageName(T& mangled, size_t& cnt, size_t idx);

    /**
     * @brief Get the index at the end of the type.
     *
     * @param mangled The name needs to decompress.
     * @param cnt Record the number of new elements added to the treeIdMap.
     * @param idx The start index of the demangled name.
     * @return size_t The end index of the demangled name.
     */
    size_t ForwardType(T& mangled, size_t& cnt, size_t idx = 0);

    /**
     * @brief Get the index at the end of the types.
     *
     * @param mangled The name needs to decompress.
     * @param cnt Record the number of new elements added to the treeIdMap.
     * @param idx The start index of the demangled name.
     * @return size_t The end index of the demangled name.
     */
```

### 示例 3: IsSamePackage
文件: `include/cangjie/AST/Node.h:415`

```cpp
bool IsSamePackage(const Node& other) const;

    /**
     * Get node's targets decl.
     */
    std::vector<Ptr<Decl>> GetTargets() const;
    /**
     * Get node's target decl.
     */
    Ptr<Decl> GetTarget() const;
    /**
     * Set node's target decl.
     */
    void SetTarget(Ptr<Decl> target);

    /**
     * Get a MacroInvocation ptr.
     * @return MacroInvocation ptr if a node is MacroExpandExpr or MacroExpandDecl,
     *  nullptr otherwise.
     */
```

## 概念关系图谱

- **同义词**: 包, 模块, module, import, 导入, export, 导出, 包管理, package management
- **相关概念**: namespace, 命名空间, 依赖, dependency
- **相关模块**: chir, codegen, demangler, frontend, frontendtool, include, incrementalcompilation, mangle, modules, parse, sema, unittests, utils

## 常见问题

### package 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 package？

请参考下面的代码示例部分。

### package 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

