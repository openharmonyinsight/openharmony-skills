# 概念关系图谱

```mermaid
graph TD
    var["var"]
    style var fill:#f9f,stroke:#333,stroke-width:4px
    chir{"chir模块"}
    var -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    var -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    demangler{"demangler模块"}
    var -->|使用于| demangler
    style demangler fill:#bbf,stroke:#333
    frontendtool{"frontendtool模块"}
    var -->|使用于| frontendtool
    style frontendtool fill:#bbf,stroke:#333
    include{"include模块"}
    var -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
