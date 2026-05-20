---
keyword: macro
synonyms: [宏, 宏定义, macro definition, 宏展开, macro expansion, 元编程, metaprogramming]
related: [annotation, reflect, 编译期, compile-time]
category: language-feature
---

# 宏 (Macro)

## 中文描述
宏是编译期的代码生成机制,允许在编译时进行代码转换和生成。宏可以接收代码片段作为参数,进行语法树级别的操作,实现元编程功能。

## English Description
Macro is a compile-time code generation mechanism that allows code transformation and generation during compilation. Macros can receive code fragments as parameters and perform syntax tree-level operations to implement metaprogramming functionality.

## 使用场景
- 编译期代码生成
- 语法糖实现
- DSL(领域特定语言)
- 代码模板

## 相关实现
- 宏调用解析在 Parse/ParseMacro.cpp
- 宏展开在 Macro/MacroExpansion.cpp
- 宏评估在 Macro/MacroEvaluation.cpp
- 关键类: MacroCall, MacroExpander, MacroEvaluator

## 代码示例

### 示例 1: IsNodeInOriginalMacroCallNodes
文件: `include/cangjie/AST/ASTContext.h:202`

```cpp
bool IsNodeInOriginalMacroCallNodes(AST::Decl& decl) const;
};

/**
 * This structure is used for lsp dot completion.
 * Since std::variant cannot perform correctly in windows, we chose to use this custom type.
 */
struct Candidate {
    std::vector<Ptr<AST::Decl>> decls;
    std::unordered_set<Ptr<AST::Ty>> tys;
    bool hasDecl;
    explicit Candidate(const std::vector<Ptr<AST::Decl>>& decls) : decls(decls), hasDecl(true)
    {
    }
    explicit Candidate(const std::unordered_set<Ptr<AST::Ty>>& tys) : tys(tys), hasDecl(false)
    {
    }
    Candidate() = default;
};
} // namespace Cangjie
```

### 示例 2: CloneMacroInvocation
文件: `include/cangjie/AST/Clone.h:27`

```cpp
MacroInvocation CloneMacroInvocation(const MacroInvocation& me);
OwnedPtr<Generic> CloneGeneric(const Generic& generic, const VisitFunc& visitor = DefaultVisitFunc);
class ASTCloner {
public:
    template <typename T>
    static std::vector<OwnedPtr<T>> CloneVector(const std::vector<OwnedPtr<T>>& nodes)
    {
        std::vector<OwnedPtr<T>> resNodes;
        for (auto& it : nodes) {
            (void)resNodes.emplace_back(Clone(it.get()));
        }
        return resNodes;
    }

    template <typename T> static OwnedPtr<T> Clone(Ptr<T> node, const VisitFunc& visitFunc = DefaultVisitFunc)
    {
        OwnedPtr<Node> clonedNode = ASTCloner().CloneWithRearrange(node, visitFunc);
        return OwnedPtr<T>(static_cast<T*>(clonedNode.release()));
    }
```

### 示例 3: GetMacroCallPos
文件: `include/cangjie/AST/Node.h:463`

```cpp
Position GetMacroCallPos(Position originPos, bool isLowerBound = false) const;

    /**
     * Get the new Position of macrocall in curfile by originPos before the macro is expanded, for lsp.
     * @return new Position of macrocall in curfile if the Node is MacroExpandExpr/MacroExpandDecl or in macrocall,
     *  INVALID_POSITION otherwise.
     */
    Position GetMacroCallNewPos(const Position& originPos);

    /**
     * For debug,
     * get the original Position of the node if it is from MacroCall in curfile,
     * curPos otherwise.
     */
    Position GetDebugPos(const Position& curPos) const;

    const std::string& GetFullPackageName() const;

protected:
    explicit Node(ASTKind kind) : astKind(kind)
```

## 概念关系图谱

- **同义词**: 宏, 宏定义, macro definition, 宏展开, macro expansion, 元编程, metaprogramming
- **相关概念**: annotation, reflect, 编译期, compile-time
- **相关模块**: ast, basic, chir, frontendtool, include, macro, modules, parse, sema, unittests

## 常见问题

### macro 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 macro？

请参考下面的代码示例部分。

### macro 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

