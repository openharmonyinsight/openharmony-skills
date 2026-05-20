# 概念关系图谱

```mermaid
graph TD
    lambda["lambda"]
    style lambda fill:#f9f,stroke:#333,stroke-width:4px
    匿名函数["匿名函数"]
    lambda -.同义词.- 匿名函数
    anonymous_function["anonymous function"]
    lambda -.同义词.- anonymous_function
    closure["closure"]
    lambda -.同义词.- closure
    function["function"]
    lambda -->|相关| function
    closure["closure"]
    lambda -->|相关| closure
    capture["capture"]
    lambda -->|相关| capture
    basic{"basic模块"}
    lambda -->|使用于| basic
    style basic fill:#bbf,stroke:#333
    chir{"chir模块"}
    lambda -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    lambda -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    demangler{"demangler模块"}
    lambda -->|使用于| demangler
    style demangler fill:#bbf,stroke:#333
    include{"include模块"}
    lambda -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
