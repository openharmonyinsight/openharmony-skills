---
keyword: ast
synonyms: [抽象语法树, abstract syntax tree, syntax tree, AST node, 语法树]
related: [parse, sema, node, walker, visitor]
category: compiler-module
---

# 抽象语法树 (AST)

## 中文描述

抽象语法树（AST）是编译器中源代码的树状表示形式。AST 模块定义了所有语法节点的数据结构，包括声明节点、表达式节点、语句节点、类型节点等。AST 是连接前端（词法分析、语法分析）和后端（语义分析、代码生成）的关键数据结构。

AST 模块提供：
- 完整的节点类型定义（Decl, Expr, Stmt, Type 等）
- 节点创建和管理接口
- AST 遍历器（Walker）和访问者模式（Visitor）
- 节点序列化和反序列化（用于增量编译）
- 类型信息存储和查询

## English Description

The Abstract Syntax Tree (AST) is a tree representation of source code in the compiler. The AST module defines data structures for all syntax nodes, including declaration nodes, expression nodes, statement nodes, type nodes, etc. AST is the key data structure connecting the frontend (lexical analysis, parsing) and backend (semantic analysis, code generation).

The AST module provides:
- Complete node type definitions (Decl, Expr, Stmt, Type, etc.)
- Node creation and management interfaces
- AST walker and visitor pattern
- Node serialization and deserialization (for incremental compilation)
- Type information storage and querying

## 使用场景

- 语法解析器构建 AST 表示源代码结构
- 语义分析器遍历 AST 进行类型检查
- 代码生成器遍历 AST 生成中间代码
- 增量编译缓存和恢复 AST
- IDE 工具分析代码结构

## 相关实现

- **主要模块**: `src/AST/`
- **核心类**:
  - `Node` - AST 节点基类
  - `Decl` - 声明节点（ClassDecl, FuncDecl, VarDecl 等）
  - `Expr` - 表达式节点（BinaryExpr, CallExpr, LambdaExpr 等）
  - `Stmt` - 语句节点（IfStmt, ForStmt, ReturnStmt 等）
  - `Type` - 类型节点（ClassType, FunctionType, GenericType 等）
  - `Walker` - AST 遍历器
- **关键文件**:
  - `Node.cpp` - 节点基类实现
  - `Types.cpp` - 类型系统实现
  - `Create.cpp` - 节点创建工厂
  - `Walker.cpp` - 遍历器实现
- **依赖模块**: Basic
- **被依赖**: Parse, Sema, CHIR, CodeGen

## 代码示例

### 示例 1: ASTContext
文件: `include/cangjie/AST/ASTContext.h:76`

```cpp
ASTContext(DiagnosticEngine& diag, AST::Package& pkg);
    ~ASTContext() = default;

    /**
     * Delete desugar expr do two things:
     * 1. Recursively delete inverted indexes of the sub symbols of the symbol.
     * 2. Reset the desugar expr.
     *
     * @see DeleteInvertedIndexes
     */
    void DeleteDesugarExpr(OwnedPtr<AST::Expr>& desugar);
    void DeleteInvertedIndexes(Ptr<AST::Node> root);
    void DeleteCurrentInvertedIndexes(Ptr<const AST::Node> node);
    // recursively clear all cache entries of sub-tree
    void ClearTypeCheckCache(const AST::Node& root);
    // only remove cache for this node
    void RemoveTypeCheckCache(const AST::Node& node);
    // set a dummy last key so that the synthesize of the node will be skipped when possible
    void SkipSynForCorrectTy(const AST::Node& node);
    // Skip Syn for all nodes with correct ty
```

### 示例 2: CreateRefExprInAST
文件: `include/cangjie/AST/Create.h:54`

```cpp
OwnedPtr<RefExpr> CreateRefExprInAST(const std::string& name);
OwnedPtr<RefExpr> CreateRefExpr(Decl& vd);
/// \p pos copy begin and end from node \ref pos
OwnedPtr<RefExpr> CreateRefExpr(Decl& vd, const Node& pos);
/** Create RefType node */
OwnedPtr<RefType> CreateRefType(const std::string& refName, std::vector<Ptr<Type>> args = {});
OwnedPtr<RefType> CreateRefType(InheritableDecl& typeDecl, Ptr<Ty> instantTy = nullptr);
/** Create MemberAccess node with given target sema. */
OwnedPtr<MemberAccess> CreateMemberAccess(OwnedPtr<Expr> expr, Decl& field);
OwnedPtr<MemberAccess> CreateMemberAccess(OwnedPtr<Expr> expr, const std::string& field);
/** Create CType Generic Constraint */
OwnedPtr<GenericConstraint> CreateConstraintForFFI(const std::string& upperBound);
OwnedPtr<MatchCase> CreateMatchCase(OwnedPtr<Pattern> pattern, OwnedPtr<Expr> expr);
OwnedPtr<MatchExpr> CreateMatchExpr(OwnedPtr<Expr> selector,
    std::vector<OwnedPtr<MatchCase>> matchCases, Ptr<Ty> ty,
    Expr::SugarKind sugarKind = Expr::SugarKind::NO_SUGAR);
OwnedPtr<LitConstExpr> CreateLitConstExpr(
    LitConstKind kind, const std::string& val, Ptr<Ty> ty, bool needToMakeRef = false
);
OwnedPtr<TupleLit> CreateTupleLit(std::vector<OwnedPtr<Expr>> elements, Ptr<Ty> ty);
```

### 示例 3: GetIDsByASTKind
文件: `include/cangjie/AST/Searcher.h:236`

```cpp
std::set<AST::Symbol*> GetIDsByASTKind(const ASTContext& ctx, const std::string& astKind) const;
    std::vector<std::string> GetAstKindsBySuffix(const ASTContext& ctx, const std::string& suffix) const;
    std::set<AST::Symbol*> PerformSearch(const ASTContext& ctx, const Query& query);
    std::set<AST::Symbol*> GetIDs(const ASTContext& ctx, const Query& query) const;
    std::set<AST::Symbol*> GetIDsByPos(const ASTContext& ctx, const Query& query) const;
    std::set<AST::Symbol*> GetIDsByName(const ASTContext& ctx, const Query& query) const;
    std::set<AST::Symbol*> GetIDsByScopeLevel(const ASTContext& ctx, const Query& query) const;
    std::set<AST::Symbol*> GetIDsByScopeName(const ASTContext& ctx, const Query& query) const;
    std::set<AST::Symbol*> GetIDsByASTKind(const ASTContext& ctx, const Query& query) const;
    static std::set<AST::Symbol*> Intersection(const std::set<AST::Symbol*>& set1, const std::set<AST::Symbol*>& set2);
    static std::set<AST::Symbol*> Union(const std::set<AST::Symbol*>& set1, const std::set<AST::Symbol*>& set2);
    std::set<AST::Symbol*> Difference(const std::set<AST::Symbol*>& set1, const std::set<AST::Symbol*>& set2) const;
    bool InFiles(const std::unordered_set<uint64_t>& files, const AST::Symbol& id) const;
    std::pair<std::vector<AST::Symbol*>, bool> FindInSearchCache(
        const Query& query, const std::string& normalizedQuery);
    std::vector<AST::Symbol*> FilterAndSortSearchResult(
        const std::set<AST::Symbol*>& ids, const Query& query, const Order& order) const;
    std::unordered_map<std::string, std::vector<AST::Symbol*>> cache;
    friend class PosSearchApi;
};
```

## 概念关系图谱

- **同义词**: 抽象语法树, abstract syntax tree, syntax tree, AST node, 语法树
- **相关概念**: parse, sema, node, walker, visitor
- **相关模块**: ast, chir, conditionalcompilation, frontend, include, incrementalcompilation, macro, modules, parse, sema, unittests

## 常见问题

### ast 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 ast？

请参考下面的代码示例部分。

### ast 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

