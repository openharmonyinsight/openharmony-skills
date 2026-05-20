# 概念关系图谱

```mermaid
graph TD
    codegen["codegen"]
    style codegen fill:#f9f,stroke:#333,stroke-width:4px
    代码生成["代码生成"]
    codegen -.同义词.- 代码生成
    code_generation["code generation"]
    codegen -.同义词.- code_generation
    code_emit["code emit"]
    codegen -.同义词.- code_emit
    chir["chir"]
    codegen -->|相关| chir
    llvm["llvm"]
    codegen -->|相关| llvm
    compiler["compiler"]
    codegen -->|相关| compiler
    backend["backend"]
    codegen -->|相关| backend
    optimization["optimization"]
    codegen -->|相关| optimization
    codegen{"codegen模块"}
    codegen -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    frontendtool{"frontendtool模块"}
    codegen -->|使用于| frontendtool
    style frontendtool fill:#bbf,stroke:#333
    include{"include模块"}
    codegen -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
