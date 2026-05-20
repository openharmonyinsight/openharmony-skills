# 概念关系图谱

```mermaid
graph TD
    type["type"]
    style type fill:#f9f,stroke:#333,stroke-width:4px
    ast{"ast模块"}
    type -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    basic{"basic模块"}
    type -->|使用于| basic
    style basic fill:#bbf,stroke:#333
    chir{"chir模块"}
    type -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    type -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    conditionalcompilation{"conditionalcompilation模块"}
    type -->|使用于| conditionalcompilation
    style conditionalcompilation fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
