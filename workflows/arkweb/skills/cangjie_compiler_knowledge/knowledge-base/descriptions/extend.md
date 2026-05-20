---
keyword: extend
synonyms: [扩展, extension, 扩展方法, extension method, 扩展接口, extension interface]
related: [class, interface, method, 方法]
category: language-feature
---

# 扩展 (Extend)

## 中文描述
extend 关键字允许为现有类型添加新方法或实现新接口,而无需修改原类型定义。这是一种非侵入式的类型扩展机制,常用于为标准库类型添加自定义功能。

## English Description
The extend keyword allows adding new methods or implementing new interfaces for existing types without modifying the original type definition. This is a non-invasive type extension mechanism, commonly used to add custom functionality to standard library types.

## 使用场景
- 为现有类型添加方法
- 为类型实现新接口
- 扩展标准库类型
- 模块化功能扩展

## 相关实现
- 扩展声明解析在 Parse/ParseDecl.cpp
- 扩展检查在 Sema/TypeCheckExtend.cpp
- 关键类: ExtendDecl, ExtensionAnalyzer

## 代码示例

### 示例 1: TryExtendPath
文件: `demangler/DeCompression.h:247`

```cpp
size_t TryExtendPath(T& mangled, size_t& count, size_t idx, size_t entityId, T& curMangled);

    /**
     * @brief Try to decompress lambda path.
     *
     * @param mangled The compressed name will be updated.
     * @param count Record the number of new elements added to the treeIdMap.
     * @param idx The start index of the compressed name.
     * @param entityId The index of treeIdMap vector whose item needs to update the end index.
     * @param change Indicates whether the compressed name has been updated.
     * @return size_t The end index which the compressed name has been updated.
     */
    size_t TryLambdaPath(T& mangled, size_t& count, size_t idx, size_t entityId, size_t change);

    /**
     * @brief Try to decompress generic prefix path.
     *
     * @param mangled The compressed name will be updated.
     * @param count Record the number of new elements added to the treeIdMap.
     * @param curMangled The origin compressed name.
```

### 示例 2: CollectDeclsFromExtendDecl
文件: `include/cangjie/CHIR/AST2CHIR/AST2CHIR.h:266`

```cpp
void CollectDeclsFromExtendDecl(AST::ExtendDecl& extendDecl);
    void CollectDeclsFromClassLikeDecl(AST::ClassLikeDecl& classLikeDecl);
    void CollectDeclsFromStructDecl(const AST::StructDecl& structDecl);
    void CollectMemberDecl(AST::Decl& decl);
    void CollectFuncDecl(AST::FuncDecl& funcDecl);
    void CollectImportedFuncDeclAndDesugarParams(AST::FuncDecl& funcDecl);
    void CollectImportedGlobalOrStaticVarDecl(AST::VarDecl& varDecl);

    void CollectDeclToList(AST::Decl& decl, std::vector<Ptr<const AST::Decl>>& astNodes);
    void CollectFuncDeclToList(AST::FuncDecl& func, std::vector<Ptr<const AST::Decl>>& list);
    void CollectDesugarDecl(AST::Decl& decl);

    void CollectInstantiatedDecls(const AST::Decl& decl);
    void CollectVarandVarwithpatternDecl(AST::Decl& decl);

    /**
     * @brief create all top-level func decl's shell and var decls, cache them to global symbol table.
     */
    void CacheTopLevelDeclToGlobalSymbolTable();
    void CreateAnnoOnlyDeclSig(const AST::Decl& decl);
```

### 示例 3: SetExtendInfo
文件: `include/cangjie/CHIR/AST2CHIR/AST2CHIR.h:323`

```cpp
void SetExtendInfo();
    void UpdateExtendParent();

    Translator CreateTranslator();
    /* Micro refactoring for CJMP. */
    void TranslateFuncParams(const AST::FuncDecl& funcDecl, Func& func) const;
    void TranslateVecDecl(const std::vector<Ptr<const AST::Decl>>& decls, Translator& trans) const;

    /* Add methods for CJMP. */
    // Try to deserialize common part for CJMP.
    bool TryToDeserializeCHIR();
    // Check whether the decl is deserialized for CJMP.
    bool MaybeDeserialized(const AST::Decl& decl) const;
    // Try to get deserialized node from package including CustomTypeDef (excluding Extend), Func, GlobalVar,
    // ImportedValue.
    template<typename T>
    T* TryGetDeserialized(const AST::Decl& decl)
    {
        if (!MaybeDeserialized(decl)) {
            return nullptr;
```

## 概念关系图谱

- **同义词**: 扩展, extension, 扩展方法, extension method, 扩展接口, extension interface
- **相关概念**: class, interface, method, 方法
- **相关模块**: chir, codegen, demangler, include, incrementalcompilation, mangle, modules, parse, sema

## 常见问题

### extend 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 extend？

请参考下面的代码示例部分。

### extend 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

