# 概念关系图谱

```mermaid
graph TD
    string["string"]
    style string fill:#f9f,stroke:#333,stroke-width:4px
    字符串["字符串"]
    string -.同义词.- 字符串
    字符串字面量["字符串字面量"]
    string -.同义词.- 字符串字面量
    string_literal["string literal"]
    string -.同义词.- string_literal
    字符串插值["字符串插值"]
    string -.同义词.- 字符串插值
    rune["rune"]
    string -->|相关| rune
    char["char"]
    string -->|相关| char
    字符["字符"]
    string -->|相关| 字符
    character["character"]
    string -->|相关| character
    text["text"]
    string -->|相关| text
    ast{"ast模块"}
    string -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    basic{"basic模块"}
    string -->|使用于| basic
    style basic fill:#bbf,stroke:#333
    chir{"chir模块"}
    string -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    string -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    conditionalcompilation{"conditionalcompilation模块"}
    string -->|使用于| conditionalcompilation
    style conditionalcompilation fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
