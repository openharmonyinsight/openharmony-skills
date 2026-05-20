# 概念关系图谱

```mermaid
graph TD
    chir["chir"]
    style chir fill:#f9f,stroke:#333,stroke-width:4px
    中间表示["中间表示"]
    chir -.同义词.- 中间表示
    intermediate_representation["intermediate representation"]
    chir -.同义词.- intermediate_representation
    中间代码["中间代码"]
    chir -.同义词.- 中间代码
    ast["ast"]
    chir -->|相关| ast
    codegen["codegen"]
    chir -->|相关| codegen
    optimization["optimization"]
    chir -->|相关| optimization
    llvm["llvm"]
    chir -->|相关| llvm
    chir{"chir模块"}
    chir -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    chir -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    frontend{"frontend模块"}
    chir -->|使用于| frontend
    style frontend fill:#bbf,stroke:#333
    frontendtool{"frontendtool模块"}
    chir -->|使用于| frontendtool
    style frontendtool fill:#bbf,stroke:#333
    include{"include模块"}
    chir -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
