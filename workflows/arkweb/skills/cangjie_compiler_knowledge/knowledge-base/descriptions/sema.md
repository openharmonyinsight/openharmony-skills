---
keyword: sema
synonyms: [语义分析, semantic analysis, 类型检查, type checking, 符号解析, symbol resolution]
related: [type-system, type-inference, scope, 作用域]
category: compiler-module
---

# 语义分析 (Semantic Analysis)

## 中文描述
语义分析(Sema)是编译器的核心阶段,负责类型检查、符号解析、作用域分析、语义验证等工作。确保程序在语义层面的正确性。

## English Description
Semantic Analysis (Sema) is the core phase of the compiler, responsible for type checking, symbol resolution, scope analysis, semantic validation, etc. Ensures the correctness of the program at the semantic level.

## 使用场景
- 类型检查
- 符号解析
- 作用域分析
- 语义错误检测

## 相关实现
- 语义分析在 Sema 模块
- 类型检查器在 Sema/TypeChecker.cpp
- 表达式检查在 Sema/TypeCheckExpr/
- 声明检查在 Sema/TypeCheckDecl.cpp
- 关键类: TypeChecker, TypeCheckerImpl

## 代码示例

### 示例 1: DesugarAfterSema
文件: `include/cangjie/Frontend/CompileStrategy.h:47`

```cpp
void DesugarAfterSema() const;
    bool ImportPackages() const;
    bool MacroExpand() const;
    virtual bool Sema() = 0;
    bool OverflowStrategy() const;
    StrategyType type{StrategyType::DEFAULT};

protected:
    /**
     * Desugar Syntactic sugar.
     */
    void PerformDesugar() const;
    /**
     * Do TypeCheck and Generic Instantiation.
     */
    void TypeCheck() const;
    /**
     * Interop config toml file check format.
     */
    void InteropConfigTomlCheck();
```

### 示例 2: Sema
文件: `include/cangjie/Frontend/CompileStrategy.h:89`

```cpp
bool Sema() override;

private:
    friend class FullCompileStrategyImpl;
    class FullCompileStrategyImpl* impl;
};
} // namespace Cangjie
#endif // CANGJIE_FRONTEND_COMPILESTRATEGY_H
```

### 示例 3: CacheSemaUsage
文件: `include/cangjie/Frontend/CompilerInstance.h:571`

```cpp
void CacheSemaUsage(SemanticInfo&& info);
    void UpdateMangleNameForCachedInfo();

private:
    // Guess the CANGJIE_HOME.
    bool DetectCangjieHome();

    // Guess the modules file path.
    bool DetectCangjieModules();

    // Merged source packages and imported packages.
    std::vector<Ptr<AST::Package>> pkgs;

    // Package to ASTContext map.
    std::unordered_map<Ptr<AST::Package>, std::unique_ptr<ASTContext>> pkgCtxMap;

    std::vector<std::string> depPackageInfo;

    virtual void UpdateCachedInfo();
    bool WriteCachedInfo();
```

## 概念关系图谱

- **同义词**: 语义分析, semantic analysis, 类型检查, type checking, 符号解析, symbol resolution
- **相关概念**: type-system, type-inference, scope, 作用域
- **相关模块**: frontendtool, include, incrementalcompilation, sema, unittests

## 常见问题

### sema 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 sema？

请参考下面的代码示例部分。

### sema 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

