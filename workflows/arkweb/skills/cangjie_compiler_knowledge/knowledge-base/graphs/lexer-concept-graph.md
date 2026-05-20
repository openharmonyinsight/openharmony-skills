# 概念关系图谱

```mermaid
graph TD
    lexer["lexer"]
    style lexer fill:#f9f,stroke:#333,stroke-width:4px
    词法分析["词法分析"]
    lexer -.同义词.- 词法分析
    lexical_analysis["lexical analysis"]
    lexer -.同义词.- lexical_analysis
    tokenizer["tokenizer"]
    lexer -.同义词.- tokenizer
    scanner["scanner"]
    lexer -.同义词.- scanner
    lex["lex"]
    lexer -.同义词.- lex
    parser["parser"]
    lexer -->|相关| parser
    token["token"]
    lexer -->|相关| token
    keyword["keyword"]
    lexer -->|相关| keyword
    identifier["identifier"]
    lexer -->|相关| identifier
    include{"include模块"}
    lexer -->|使用于| include
    style include fill:#bbf,stroke:#333
    lex{"lex模块"}
    lexer -->|使用于| lex
    style lex fill:#bbf,stroke:#333
    unittests{"unittests模块"}
    lexer -->|使用于| unittests
    style unittests fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
