---
keyword: const
synonyms: [常量, constant, 不可变, immutable, let, 常量表达式, constant expression]
related: [var, 变量, variable, 编译期, compile-time]
category: language-feature
---

# 常量 (Const)

## 中文描述
const 关键字用于声明编译期常量,其值必须在编译时确定。常量是不可变的,可以用于数组大小、枚举值等需要编译期常量的场景。

## English Description
The const keyword is used to declare compile-time constants whose values must be determined at compile time. Constants are immutable and can be used in scenarios requiring compile-time constants such as array sizes and enum values.

## 使用场景
- 编译期常量定义
- 常量表达式求值
- 数组大小声明
- 配置常量

## 相关实现
- const 声明解析在 Parse/ParseDecl.cpp
- 常量求值在 Sema/ConstEvaluationChecker.cpp
- 关键类: ConstExpr, ConstEvaluator

## 代码示例

### 示例 1: IsConst
文件: `include/cangjie/AST/Node.h:1027`

```cpp
bool IsConst() const;

    /**
     * Get the desugar decl of this decl
     * @return the ptr of desugar decl if it exist, nullptr otherwise.
     */
    Ptr<FuncDecl> GetDesugarDecl() const;

    bool IsCommonOrSpecific() const;

    bool IsCommonMatchedWithSpecific() const;

protected:
    Decl(ASTKind kind) : Node(kind)
    {
    }
};

struct InheritableDecl : public Decl {
    Position upperBoundPos;                     /**< Position of <:. */
```

### 示例 2: InitializeLitConstValue
文件: `include/cangjie/AST/Utils.h:99`

```cpp
void InitializeLitConstValue(AST::LitConstExpr& lce);

struct FloatTypeInfo {
    uint64_t inf;
    std::string min;
    std::string max;
};
FloatTypeInfo GetFloatTypeInfoByKind(AST::TypeKind kind);

void SetOuterFunctionDecl(AST::Decl& decl);
bool IsInDeclWithAttribute(const AST::Decl& decl, AST::Attribute attr);

/**
 * Iterate all toplevel decls in given 'pkg', and perform the function 'process' on each of toplevel decl.
 */
inline void IterateToplevelDecls(const Package& pkg, const std::function<void(OwnedPtr<Decl>&)>& process)
{
    for (auto& file : pkg.files) {
        (void)std::for_each(file->decls.begin(), file->decls.end(), process);
        (void)std::for_each(file->exportedInternalDecls.begin(), file->exportedInternalDecls.end(), process);
```

### 示例 3: AnalysisGlobalVarsAndLocalConstVarsDependency
文件: `include/cangjie/CHIR/AST2CHIR/GlobalDeclAnalysis.h:58`

```cpp
void AnalysisGlobalVarsAndLocalConstVarsDependency(const InitOrder& initOrder);
    void AnalysisDependency(const ElementList<Ptr<const AST::Decl>>& nodesWithDeps);
    void AdditionalAnalysisDepOfNonStaticCtor(const AST::FuncDecl& func,
        std::vector<Ptr<const AST::Decl>>& dependencies, std::vector<Ptr<const AST::Decl>>& localConstVarDeps);
    void AdditionalAnalysisDepOfStaticInit(
        const Ptr<const AST::FuncDecl>& staticInit, std::vector<Ptr<const AST::Decl>>& dependencies) const;

    void WalkAndCollectDep(const AST::Node& curNode, std::vector<Ptr<const AST::Decl>>& dependencies,
        std::vector<Ptr<const AST::Decl>>& localConstVarDeps);
    void AnalysisDepOf(const AST::Decl& rootDecl, std::vector<Ptr<const AST::Decl>>& dependencies,
        std::vector<Ptr<const AST::Decl>>& localConstVarDeps);
    void ParseVarWithPatternDecl(const AST::VarWithPatternDecl& root);
    void ParsePattern(const AST::VarWithPatternDecl& rootDecl, AST::Pattern& pattern);
    void AddDependencyImpl(const AST::Decl& depDecl, std::vector<Ptr<const AST::Decl>>& dependencies) const;
    void AddDependency(const AST::Decl& depDecl, std::vector<Ptr<const AST::Decl>>& dependencies);
    AST::VisitAction VisitExprAction(const AST::Expr& expr, std::vector<Ptr<const AST::Decl>>& dependencies,
        std::vector<Ptr<const AST::Decl>>& localConstVarDeps);
    AST::VisitAction CollectDepInCallExpr(
        const AST::CallExpr& callExpr, std::vector<Ptr<const AST::Decl>>& dependencies);
    AST::VisitAction CollectDepInLitConstExpr(
```

## 概念关系图谱

- **同义词**: 常量, constant, 不可变, immutable, let, 常量表达式, constant expression
- **相关概念**: var, 变量, variable, 编译期, compile-time
- **相关模块**: chir, codegen, include, incrementalcompilation, modules, parse, sema, unittests

## 常见问题

### const 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 const？

请参考下面的代码示例部分。

### const 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

