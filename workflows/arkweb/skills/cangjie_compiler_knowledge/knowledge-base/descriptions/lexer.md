---
keyword: lexer
synonyms: [词法分析, lexical analysis, tokenizer, scanner, lex, 词法分析器, 扫描器]
related: [parser, token, keyword, identifier]
category: compiler-module
---

# 词法分析器 (Lexer)

## 中文描述

词法分析器（Lexer）是编译器的第一个阶段，负责将源代码文本转换为 Token 流。Lexer 读取字符序列，识别关键字、标识符、字面量、运算符、分隔符等词法单元，并为每个 Token 附加位置信息（文件名、行号、列号）用于错误报告。

词法分析器的主要功能：
- 识别关键字（class, func, if, for 等）
- 识别标识符和类型名
- 识别字面量（整数、浮点数、字符串、字符）
- 识别运算符和分隔符
- 处理注释和空白字符
- 处理字符串插值和转义序列
- 报告词法错误（非法字符、未闭合的字符串等）

## English Description

The Lexer is the first stage of the compiler, responsible for converting source code text into a Token stream. The Lexer reads character sequences, recognizes keywords, identifiers, literals, operators, delimiters, and other lexical units, and attaches position information (filename, line number, column number) to each Token for error reporting.

Main functions of the Lexer:
- Recognize keywords (class, func, if, for, etc.)
- Recognize identifiers and type names
- Recognize literals (integers, floats, strings, characters)
- Recognize operators and delimiters
- Handle comments and whitespace
- Handle string interpolation and escape sequences
- Report lexical errors (illegal characters, unclosed strings, etc.)

## 使用场景

- 编译的第一阶段，将源码转换为 Token 流
- 为语法分析器提供输入
- 识别和过滤注释
- 处理预处理指令（条件编译）
- 提供精确的错误位置信息

## 相关实现

- **主要模块**: `src/Lex/`
- **核心类**:
  - `Lexer` - 词法分析器主类
  - `LexerImpl` - 词法分析器实现
  - `Token` - Token 数据结构
  - `TokenKind` - Token 类型枚举
- **关键函数**:
  - `Lex()` - 读取下一个 Token
  - `LexIdentifier()` - 识别标识符
  - `LexNumericConstant()` - 识别数字字面量
  - `LexStringLiteral()` - 识别字符串字面量
- **依赖模块**: Basic
- **被依赖**: Parse, ConditionalCompilation

## 代码示例

### 示例 1: Lexer
文件: `include/cangjie/Lex/Lexer.h:83`

```cpp
Lexer(const std::string& input, DiagnosticEngine& diag, SourceManager& sm, bool cts = false, bool splitAmbi = true);
    Lexer(const std::string& input, DiagnosticEngine& diag, SourceManager& sm, const Position& pos, bool cts = false);
    Lexer(const std::string& input, DiagnosticEngine& diag, Source& s, const Position& pos, bool cts = false);
    /// Create Lexer with \ref inputTokens from successful macro func call.
    Lexer(const std::vector<Token>& inputTokens, DiagnosticEngine& diag, SourceManager& sm, bool cts = false);
    ~Lexer();

    // FrontendTool/SourceManager/Parse/Macro/stdlib/unittests.
    /// read and return next token
    Token Next();

    // Parse/unittests.
    /// Read and return the next \ref num tokens. If there are less than \ref num tokens left, all are returned.
    /// otherwise, comments are omitted.
    const std::list<Token>& LookAhead(size_t num);
    /// Returns true if the next token is any of the TokenKind's described by range \ref begin and \ref end.
    /// \param skipNewline whether to ignore NL
    bool Seeing(const std::vector<TokenKind>::const_iterator& begin, const std::vector<TokenKind>::const_iterator& end,
        bool skipNewline = false, bool skipComments = true);
    /// Returns true if the next token is any of \ref kinds.
```

### 示例 2: Lexer
文件: `include/cangjie/Lex/Lexer.h:84`

```cpp
Lexer(const std::string& input, DiagnosticEngine& diag, SourceManager& sm, const Position& pos, bool cts = false);
    Lexer(const std::string& input, DiagnosticEngine& diag, Source& s, const Position& pos, bool cts = false);
    /// Create Lexer with \ref inputTokens from successful macro func call.
    Lexer(const std::vector<Token>& inputTokens, DiagnosticEngine& diag, SourceManager& sm, bool cts = false);
    ~Lexer();

    // FrontendTool/SourceManager/Parse/Macro/stdlib/unittests.
    /// read and return next token
    Token Next();

    // Parse/unittests.
    /// Read and return the next \ref num tokens. If there are less than \ref num tokens left, all are returned.
    /// otherwise, comments are omitted.
    const std::list<Token>& LookAhead(size_t num);
    /// Returns true if the next token is any of the TokenKind's described by range \ref begin and \ref end.
    /// \param skipNewline whether to ignore NL
    bool Seeing(const std::vector<TokenKind>::const_iterator& begin, const std::vector<TokenKind>::const_iterator& end,
        bool skipNewline = false, bool skipComments = true);
    /// Returns true if the next token is any of \ref kinds.
    /// \param skipNewline whether to ignore NL
```

### 示例 3: Lexer
文件: `include/cangjie/Lex/Lexer.h:85`

```cpp
Lexer(const std::string& input, DiagnosticEngine& diag, Source& s, const Position& pos, bool cts = false);
    /// Create Lexer with \ref inputTokens from successful macro func call.
    Lexer(const std::vector<Token>& inputTokens, DiagnosticEngine& diag, SourceManager& sm, bool cts = false);
    ~Lexer();

    // FrontendTool/SourceManager/Parse/Macro/stdlib/unittests.
    /// read and return next token
    Token Next();

    // Parse/unittests.
    /// Read and return the next \ref num tokens. If there are less than \ref num tokens left, all are returned.
    /// otherwise, comments are omitted.
    const std::list<Token>& LookAhead(size_t num);
    /// Returns true if the next token is any of the TokenKind's described by range \ref begin and \ref end.
    /// \param skipNewline whether to ignore NL
    bool Seeing(const std::vector<TokenKind>::const_iterator& begin, const std::vector<TokenKind>::const_iterator& end,
        bool skipNewline = false, bool skipComments = true);
    /// Returns true if the next token is any of \ref kinds.
    /// \param skipNewline whether to ignore NL
    bool Seeing(const std::vector<TokenKind>& kinds, bool skipNewline = false, bool skipComments = true);
```

## 概念关系图谱

- **同义词**: 词法分析, lexical analysis, tokenizer, scanner, lex, 词法分析器, 扫描器
- **相关概念**: parser, token, keyword, identifier
- **相关模块**: include, lex, unittests

## 常见问题

### lexer 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 lexer？

请参考下面的代码示例部分。

### lexer 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

