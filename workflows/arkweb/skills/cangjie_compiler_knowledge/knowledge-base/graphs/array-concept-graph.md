# 概念关系图谱

```mermaid
graph TD
    array["array"]
    style array fill:#f9f,stroke:#333,stroke-width:4px
    ast{"ast模块"}
    array -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    chir{"chir模块"}
    array -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    array -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    demangler{"demangler模块"}
    array -->|使用于| demangler
    style demangler fill:#bbf,stroke:#333
    include{"include模块"}
    array -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
