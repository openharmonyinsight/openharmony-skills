# 概念关系图谱

```mermaid
graph TD
    inline["inline"]
    style inline fill:#f9f,stroke:#333,stroke-width:4px
    内联["内联"]
    inline -.同义词.- 内联
    内联函数["内联函数"]
    inline -.同义词.- 内联函数
    inline_function["inline function"]
    inline -.同义词.- inline_function
    inlining["inlining"]
    inline -.同义词.- inlining
    函数内联["函数内联"]
    inline -.同义词.- 函数内联
    optimization["optimization"]
    inline -->|相关| optimization
    function["function"]
    inline -->|相关| function
    lambda["lambda"]
    inline -->|相关| lambda
    codegen["codegen"]
    inline -->|相关| codegen
    chir{"chir模块"}
    inline -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    inline -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    include{"include模块"}
    inline -->|使用于| include
    style include fill:#bbf,stroke:#333
    modules{"modules模块"}
    inline -->|使用于| modules
    style modules fill:#bbf,stroke:#333
    sema{"sema模块"}
    inline -->|使用于| sema
    style sema fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
