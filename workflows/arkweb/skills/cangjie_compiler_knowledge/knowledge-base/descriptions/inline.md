---
keyword: inline
synonyms: [内联, 内联函数, inline function, inlining, 函数内联]
related: [optimization, function, lambda, codegen]
category: compiler-optimization
---

# 内联 (Inline)

## 中文描述

内联是编译器优化技术，将函数调用替换为函数体代码，消除调用开销。仓颉编译器支持函数内联和 Lambda 内联，在代码生成阶段决定是否内联函数。

内联的主要优点：
- 消除函数调用开销（保存寄存器、跳转、返回）
- 提供更多优化机会（常量传播、死代码消除）
- 提高缓存局部性
- 减少指令数量

内联的主要考虑因素：
- 函数大小（小函数更适合内联）
- 调用频率（热点函数优先内联）
- 代码膨胀（过度内联会增加代码大小）
- 递归函数（通常不内联）

仓颉编译器中的内联实现：
- `FunctionInline` - 函数内联优化
- `LambdaInline` - Lambda 表达式内联
- 内联决策算法（基于函数大小、调用频率等）

## English Description

Inlining is a compiler optimization technique that replaces function calls with function body code, eliminating call overhead. The Cangjie compiler supports function inlining and lambda inlining, deciding whether to inline functions during code generation.

Main advantages of inlining:
- Eliminate function call overhead (saving registers, jumping, returning)
- Provide more optimization opportunities (constant propagation, dead code elimination)
- Improve cache locality
- Reduce instruction count

Main considerations for inlining:
- Function size (smaller functions are more suitable for inlining)
- Call frequency (hot functions prioritized for inlining)
- Code bloat (excessive inlining increases code size)
- Recursive functions (usually not inlined)

Inlining implementation in Cangjie compiler:
- `FunctionInline` - Function inlining optimization
- `LambdaInline` - Lambda expression inlining
- Inlining decision algorithm (based on function size, call frequency, etc.)

## 使用场景

- 小函数优化（getter/setter、简单计算函数）
- Lambda 表达式优化（避免闭包分配）
- 消除调用开销（提高性能）
- 提高执行效率（减少指令数量）
- 热点代码优化（频繁调用的函数）

## 相关实现

- **主要模块**: `src/CodeGen/`, `src/CHIR/`
- **核心类**:
  - `FunctionInline` - 函数内联优化器
  - `LambdaInline` - Lambda 内联优化器
- **关键文件**:
  - `src/CHIR/FunctionInline.h` - 函数内联定义
  - `src/CHIR/LambdaInline.h` - Lambda 内联定义
  - `src/CodeGen/` - 内联代码生成
- **依赖模块**: CHIR, CodeGen, Function
- **被依赖**: Optimization, CodeGen

## 代码示例

### 示例 1: TranslateConstructorFuncInline
文件: `include/cangjie/CHIR/AST2CHIR/TranslateASTNode/Translator.h:767`

```cpp
Ptr<Value> TranslateConstructorFuncInline(const AST::Decl& parent, const AST::FuncBody& funcBody);
    // Check whether the member of decl should be translated.
    bool ShouldTranslateMember(const AST::Decl& decl, const AST::Decl& member) const;

    Ptr<Value> Visit(const AST::ArrayExpr& array);
    Ptr<Value> Visit(const AST::ArrayLit& array);
    Ptr<Value> Visit(const AST::AssignExpr& assign);
    Ptr<Value> Visit(const AST::BinaryExpr& binaryExpr);
    Ptr<Value> Visit(const AST::Block& b);
    Ptr<Value> Visit(const AST::CallExpr& callExpr);
    Ptr<Value> Visit(const AST::ClassDecl& decl);
    Ptr<Value> Visit(const AST::DoWhileExpr& doWhileExpr);
    Ptr<Value> Visit(const AST::EnumDecl& decl);
    Ptr<Value> Visit(const AST::ExtendDecl& decl);
    Ptr<Value> Visit(const AST::FuncArg& arg);
    Ptr<Value> Visit(const AST::FuncBody& funcBody);
    Ptr<Value> Visit(const AST::FuncDecl& func);
    Ptr<Value> Visit(const AST::IfExpr& ifExpr);
    Ptr<Value> Visit(const AST::InterfaceDecl& decl);
    Ptr<Value> Visit(const AST::JumpExpr& jumpExpr);
```

### 示例 2: RunFunctionInline
文件: `include/cangjie/CHIR/CHIR.h:155`

```cpp
void RunFunctionInline(DevirtualizationInfo& devirtInfo);
    void RunArrayLambdaOpt();
    void RunRedundantFutureOpt();
    void RunSanitizerCoverage();
    bool RulesChecking();
    void RunOptimizationPass();
    void RunUnitUnify();
    void OptimizeFuncReturnType();
    DevirtualizationInfo CollectDevirtualizationInfo();
    bool RunConstantEvaluation();
    bool RunIRChecker(const Phase& phase);
    void UpdatePosOfMacroExpandNode();
    void RecordCodeInfoAtTheBegin();
    void RecordCodeInfoAtTheEnd();
    void RecordCHIRExprNum(const std::string& suffix);
    bool RunAnalysisForCJLint();
    void RunConstantAnalysis();
    // run semantic checks that have to be performed on CHIR
    bool RunAnnotationChecks();
    void EraseDebugExpr();
```

### 示例 3: DoFunctionInline
文件: `include/cangjie/CHIR/Optimization/FunctionInline.h:56`

```cpp
void DoFunctionInline(const Apply& apply, const std::string& name);

private:
    bool CheckCanRewrite(const Apply& apply);
    void RecordEffectMap(const Apply& apply);
    void ReplaceFuncResult(LocalVar* resNew, LocalVar* resOld);

    std::pair<BlockGroup*, LocalVar*> CloneBlockGroupForInline(
        const BlockGroup& other, Func& parentFunc, const Apply& apply);

    void SetGroupDebugLocation(BlockGroup& group, const DebugLocation& loc);

    void InlineImpl(BlockGroup& bg);

    CHIRBuilder& builder;
    const GlobalOptions::OptimizationLevel& optLevel;
    bool debug{false};
    Func* globalFunc{nullptr};
    std::unordered_map<Func*, size_t> inlinedCountMap;
    std::unordered_map<Func*, size_t> funcSizeMap;
```

## 概念关系图谱

- **同义词**: 内联, 内联函数, inline function, inlining, 函数内联
- **相关概念**: optimization, function, lambda, codegen
- **相关模块**: chir, codegen, include, modules, sema

## 常见问题

### inline 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 inline？

请参考下面的代码示例部分。

### inline 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

