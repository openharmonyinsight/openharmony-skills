---
keyword: pipeline
synonyms: [管道运算符, pipeline operator, |>, pipe, 管道]
related: [function, operator, composition, 函数组合]
category: language-feature
---

# 管道运算符 (Pipeline Operator)

## 中文描述
管道运算符 |> 用于函数链式调用,将左侧表达式的值作为右侧函数的第一个参数。这种语法使得数据处理流程更加清晰易读,常用于函数式编程风格。

## English Description
The pipeline operator |> is used for chaining function calls, passing the value of the left expression as the first argument to the right function. This syntax makes data processing pipelines clearer and more readable, commonly used in functional programming style.

## 使用场景
- 数据处理管道
- 函数链式调用
- 集合操作(map, filter, reduce)
- 函数组合

## 相关实现
- 管道运算符解析在 Parse 模块
- 语法糖展开(desugaring)
- 类型检查和重载解析

## 代码示例

### 示例 1: RecoverToPipelineExpr
文件: `src/AST/RecoverDesugar.cpp:119`

```cpp
RecoverToPipelineExpr(be);
        return;
    } else if (be.op == TokenKind::COMPOSITION) {
        RecoverToCompositionExpr(be);
        return;
    }
    // Recover to BinaryExpr.
    auto callExpr = StaticCast<CallExpr*>(be.desugarExpr.get());
    auto ma = StaticCast<MemberAccess*>(callExpr->baseFunc.get());
    be.leftExpr = std::move(ma->baseExpr);
    be.rightExpr = std::move(callExpr->args[0]->expr);
    if (auto nre = DynamicCast<NameReferenceExpr*>(be.leftExpr.get())) {
        UnsetCallExprOfNode(*nre);
    }
    CJC_NULLPTR_CHECK(be.curFile);
    be.curFile->trashBin.emplace_back(std::move(be.desugarExpr));
    be.desugarExpr = OwnedPtr<Expr>();
}

void RecoverToAssignExpr(AssignExpr& ae)
```

### 示例 2: DesugarPipelineExpr
文件: `src/Sema/Desugar/DesugarInTypeCheck.cpp:291`

```cpp
DesugarPipelineExpr(ctx, fe);
    } else if (fe.op == TokenKind::COMPOSITION) {
        DesugarCompositionExpr(ctx, fe);
    }
}

void DesugarOperatorOverloadExpr(ASTContext& ctx, BinaryExpr& be)
{
    if (be.desugarExpr != nullptr || !be.leftExpr || !be.rightExpr) {
        return;
    }
    auto callExpr = MakeOwnedNode<CallExpr>();
    CopyBasicInfo(&be, callExpr.get());
    ctx.RemoveTypeCheckCache(*callExpr);
    auto callBase = MakeOwnedNode<MemberAccess>();
    CopyBasicInfo(&be, callBase.get());
    ctx.RemoveTypeCheckCache(*callBase);
    callBase->baseExpr = std::move(be.leftExpr);
    callBase->field = SrcIdentifier{TOKENS[static_cast<int64_t>(be.op)]};
    callBase->field.SetPos(be.operatorPos, be.operatorPos + strlen(TOKENS[static_cast<int64_t>(be.op)]));
```

## 概念关系图谱

- **同义词**: 管道运算符, pipeline operator, |>, pipe, 管道
- **相关概念**: function, operator, composition, 函数组合
- **相关模块**: ast, sema

## 常见问题

### pipeline 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 pipeline？

请参考下面的代码示例部分。

### pipeline 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

