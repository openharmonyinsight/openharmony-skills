---
keyword: parser
synonyms: [解析器, 语法解析, syntax parsing, AST, 抽象语法树, parse tree]
related: [lexer, 词法分析, syntax, 语法, token]
category: compiler-module
---

# 解析器 (Parser)

## 中文描述
解析器负责将 Token 流转换为抽象语法树(AST)。解析器实现了仓颉语言的完整语法规则,处理表达式、语句、声明等各种语法结构。

## English Description
Parser is responsible for converting token stream into Abstract Syntax Tree (AST). The parser implements the complete grammar rules of Cangjie language, handling various syntax structures such as expressions, statements, declarations, etc.

## 使用场景
- 语法分析
- AST 构建
- 语法错误检测
- 语法糖展开

## 相关实现
- 解析器实现在 Parse 模块
- 表达式解析在 Parse/ParseExpr.cpp
- 声明解析在 Parse/ParseDecl.cpp
- 类型解析在 Parse/ParseType.cpp
- 关键类: Parser, ParserImpl

## 代码示例

### 示例 1: parser
文件: `unittests/AST/WalkerTest.cpp:28`

```cpp
Parser parser(code, diag, sm);
        file = parser.ParseTopLevel();
    }

    DiagnosticEngine diag;
    SourceManager sm;
    OwnedPtr<File> file;
};

TEST_F(WalkerTest, WalkPair)
{
    int count = 0;

    Walker walker(
        file.get(),
        [&count](Ptr<Node> node) -> VisitAction {
            ++count;
            return VisitAction::WALK_CHILDREN;
        },
        [&count](Ptr<Node> node) -> VisitAction {
```

### 示例 2: parser
文件: `unittests/AST/ASTToSourceTest.cpp:41`

```cpp
Parser parser(srcVarDecl, diag, sm);
        OwnedPtr<File> file = parser.ParseTopLevel();
        EXPECT_EQ(srcVarDecl, file->decls[0]->ToString());
    }

    srcVarDecl = R"(var cc    = "hello world!")";
    {
        Parser parser(srcVarDecl, diag, sm);
        OwnedPtr<File> file = parser.ParseTopLevel();
        EXPECT_EQ(srcVarDecl, file->decls[0]->ToString());
    }

    srcVarDecl = R"(public

                      let

                    a :
                    String

                      =
```

### 示例 3: parser
文件: `unittests/AST/ASTToSourceTest.cpp:48`

```cpp
Parser parser(srcVarDecl, diag, sm);
        OwnedPtr<File> file = parser.ParseTopLevel();
        EXPECT_EQ(srcVarDecl, file->decls[0]->ToString());
    }

    srcVarDecl = R"(public

                      let

                    a :
                    String

                      =

                    "hello world!")";
    {
        Parser parser(srcVarDecl, diag, sm);
        OwnedPtr<File> file = parser.ParseTopLevel();
        EXPECT_EQ(srcVarDecl, file->decls[0]->ToString());
    }
```

## 概念关系图谱

- **同义词**: 解析器, 语法解析, syntax parsing, AST, 抽象语法树, parse tree
- **相关概念**: lexer, 词法分析, syntax, 语法, token
- **相关模块**: ast, include, parse, unittests

## 常见问题

### parser 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 parser？

请参考下面的代码示例部分。

### parser 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

