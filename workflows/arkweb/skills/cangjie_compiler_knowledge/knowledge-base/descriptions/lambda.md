---
keyword: lambda
synonyms: [匿名函数, anonymous function, closure]
related: [function, closure, capture]
category: language-feature
---

# Lambda 表达式

## 中文描述
Lambda 表达式是仓颉语言中的匿名函数特性，支持捕获外部变量。Lambda 表达式可以作为参数传递给高阶函数，也可以赋值给变量。

## English Description
Lambda expressions are anonymous function features in Cangjie language, supporting variable capture. Lambda expressions can be passed as arguments to higher-order functions or assigned to variables.

## 使用场景
- 函数式编程
- 回调函数
- 高阶函数参数
- 事件处理器

## 相关实现
- LambdaExpr 类 (src/Parse/Lambda.h) - Lambda 表达式的 AST 节点
- BuildLambdaClosure 函数 (src/Sema/Lambda.cpp) - 构建 Lambda 闭包
- TypeCheckLambda 函数 (src/Sema/Lambda.cpp) - Lambda 类型检查

## 代码示例

### 示例 1: TryLambdaPath
文件: `demangler/DeCompression.h:259`

```cpp
size_t TryLambdaPath(T& mangled, size_t& count, size_t idx, size_t entityId, size_t change);

    /**
     * @brief Try to decompress generic prefix path.
     *
     * @param mangled The compressed name will be updated.
     * @param count Record the number of new elements added to the treeIdMap.
     * @param curMangled The origin compressed name.
     * @param rParams A tuple consisting of the start index, entity id and the end index.
     * @return size_t The end index which the compressed name has been updated.
     */
    size_t TryGenericPrefixPath(T& mangled, size_t& count, T& curMangled, std::tuple<size_t, size_t, size_t> rParams);

    /**
     * @brief Try to decompress name prefix path.
     *
     * @param mangled The compressed name will be updated.
     * @param count Record the number of new elements added to the treeIdMap.
     * @param curMangled The origin compressed name.
     * @param rParams A tuple consisting of the start index, entity id and the change.
```

### 示例 2: CreateLambdaExpr
文件: `include/cangjie/AST/Create.h:80`

```cpp
OwnedPtr<LambdaExpr> CreateLambdaExpr(OwnedPtr<FuncBody> funcBody);
OwnedPtr<AssignExpr> CreateAssignExpr(
    OwnedPtr<Expr> leftValue, OwnedPtr<Expr> rightExpr, Ptr<Ty> ty = nullptr);
OwnedPtr<FuncArg> CreateFuncArg(OwnedPtr<Expr> expr, const std::string& argName = "", Ptr<Ty> ty = nullptr);
OwnedPtr<FuncDecl> CreateFuncDecl(
    const std::string& funcName, OwnedPtr<FuncBody> body = nullptr, Ptr<Ty> ty = nullptr);
OwnedPtr<FuncBody> CreateFuncBody(std::vector<OwnedPtr<FuncParamList>> paramLists,
    OwnedPtr<Type> retType, OwnedPtr<Block> body, Ptr<Ty> ty = nullptr);
OwnedPtr<FuncParam> CreateFuncParam(const std::string& paramName, OwnedPtr<Type> paramType = nullptr,
    OwnedPtr<Expr> paramValue = nullptr, Ptr<Ty> ty = nullptr);
OwnedPtr<FuncParamList> CreateFuncParamList(std::vector<OwnedPtr<FuncParam>> params, Ptr<Ty> ty = nullptr);
OwnedPtr<Block> CreateBlock(std::vector<OwnedPtr<Node>> nodes, Ptr<Ty> ty = nullptr);
OwnedPtr<IfExpr> CreateIfExpr(OwnedPtr<Expr> condExpr, OwnedPtr<Block> body,
    OwnedPtr<Block> elseBody = nullptr, Ptr<Ty> semaType = nullptr);
OwnedPtr<VarDecl> CreateVarDecl(
    const std::string& varName, OwnedPtr<Expr> initializer = nullptr, Ptr<Type> type = nullptr);
OwnedPtr<ThrowExpr> CreateThrowExpr(Decl& var);
OwnedPtr<PerformExpr> CreatePerformExpr(Decl& var);
OwnedPtr<ResumeExpr> CreateResumeExpr(Decl& var);
OwnedPtr<TypePattern> CreateTypePattern(OwnedPtr<Pattern>&& pattern, OwnedPtr<Type>&& type, Expr& selector);
```

### 示例 3: lambda
文件: `include/cangjie/Basic/Match.h:80`

```cpp
return lambda();
    }

    // Invoke the function with 1 argument.
    template <typename Lambda>
    auto Invoke0(Lambda& lambda) -> std::enable_if_t<Signature<Lambda>::numArgs == 1, RetT<Lambda>>
    {
        using TargetT = std::remove_reference_t<typename Signature<Lambda>::template Argument<0>>;
        // Add const if Type has const.
        if (auto* p = dynamic_cast<TargetT*>(&node)) {
            return std::invoke(lambda, *p);
        }
    }

    // Invoke the last lambda.
    template <typename Lambda> auto Invoke(Lambda& lambda) -> RetT<Lambda>
    {
        return Invoke0(lambda);
    }
```

## 概念关系图谱

- **同义词**: 匿名函数, anonymous function, closure
- **相关概念**: function, closure, capture
- **相关模块**: basic, chir, codegen, demangler, include, incrementalcompilation, macro, modules, parse, sema

## 常见问题

### lambda 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 lambda？

请参考下面的代码示例部分。

### lambda 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

