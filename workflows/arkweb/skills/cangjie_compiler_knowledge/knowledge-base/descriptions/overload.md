---
keyword: overload
synonyms: [重载, overloading, function overload, 函数重载, operator overload, 运算符重载]
related: [function, operator, type, resolution, 类型解析]
category: language-feature
---

# 函数重载 (Function Overload)

## 中文描述
函数重载是指在同一作用域内定义多个同名函数,通过参数类型、数量或顺序的不同来区分。编译器在调用时根据实参类型进行重载解析,选择最匹配的函数版本。

## English Description
Function overloading allows multiple functions with the same name to be defined in the same scope, distinguished by their parameter types, number, or order. The compiler performs overload resolution at call sites to select the best matching function version based on argument types.

## 使用场景
- 为同一操作提供不同类型的实现
- 运算符重载(operator overloading)
- 构造函数重载
- 泛型函数的特化

## 相关实现
- 重载解析算法在 Sema 模块中实现
- 候选函数收集和匹配度计算
- 类型转换和隐式转换处理

## 代码示例

### 示例 1: DiagInvalidOverloadedOperator
文件: `src/Parse/ParseDecl.cpp:955`

```cpp
DiagInvalidOverloadedOperator();
        Next();
        return INVALID_IDENTIFIER;
    }
    // operator function do not support generic, but we do error check in sema.
    if (!Seeing(TokenKind::LPAREN) && !Seeing(TokenKind::LT)) {
        DiagExpectCharacter("'('");
        Next();
        return INVALID_IDENTIFIER;
    }
    fd.identifier.SetPos(operatorTok.Begin(), operatorTok.End());
    fd.op = operatorTok.kind;
    return operatorTok.Value();
}

OwnedPtr<FuncDecl> ParserImpl::ParseFinalizer(
    ScopeKind scopeKind, const std::set<Modifier> modifiers, PtrVector<Annotation> annos)
{
    Next(); // skip ~
    auto tildeBegin{lastToken.Begin()};
```

### 示例 2: SkipAndReturnOverloadingOperator
文件: `src/Parse/ParserImpl.h:377`

```cpp
Token SkipAndReturnOverloadingOperator();
    /// Seeing IfAvailable Expr
    bool SeeingIfAvailable()
    {
        if (!Seeing(TokenKind::AT)) {
            return false;
        }
        // Get annotation identifier.
        auto tokens = lexer->LookAheadSkipNL(1);
        return !tokens.empty() && tokens.begin()->kind == TokenKind::IDENTIFIER &&
            tokens.begin()->Value() == IF_AVAILABLE;
    }
    /// A valid ifAvailable expression has the following form.
    /// @IfAvailable(paramName: arg, lambda1, lambda2)
    OwnedPtr<AST::IfAvailableExpr> ParseIfAvailable();
    bool SeeingDecl()
    {
        if (SeeingIfAvailable()) {
            return false;
        }
```

### 示例 3: DiagInvalidOverloadedOperator
文件: `src/Parse/ParserImpl.h:889`

```cpp
void DiagInvalidOverloadedOperator();
    void DiagRedundantArrowAfterFunc(const AST::Type& type);
    void DiagExpectedDeclaration(ScopeKind scopeKind);
    void DiagExpectedDeclaration(const Position& pos, const std::string& str);
    /**
        * Suggest keywords for expected declaration.
        * @param keywords keywords to suggest
        * @param minLevDis minimum Levenshtein distance to suggest
        * @param scopeKind scope kind to determine which keywords to suggest
    */
    void DiagAndSuggestKeywordForExpectedDeclaration(
        const std::vector<std::string>& keywords, size_t minLevDis = 1, ScopeKind scopeKind = ScopeKind::TOPLEVEL);
    void DiagUnExpectedModifierOnDeclaration(const AST::Decl& vd);
    void DiagConstVariableExpectedStatic(const Token& key);
    void DiagConstVariableExpectedInitializer(AST::Decl& vd);
    void DiagExpectedOneOfTypeOrInitializer(const AST::Decl& vd, const std::string& str);
    void DiagExpectedTypeOrInitializerInPattern(const AST::Decl& vd);
    void DiagExpectedInitializerForToplevelVar(const AST::Decl& vd);
    void DiagExpectedIdentifierOrPattern(bool isVar, const Position& pos, bool isConst = false);
    void DiagExpectedGetOrSetInProp(const Position& pos);
```

## 概念关系图谱

- **同义词**: 重载, overloading, function overload, 函数重载, operator overload, 运算符重载
- **相关概念**: function, operator, type, resolution, 类型解析
- **相关模块**: parse, sema

## 常见问题

### overload 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 overload？

请参考下面的代码示例部分。

### overload 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

