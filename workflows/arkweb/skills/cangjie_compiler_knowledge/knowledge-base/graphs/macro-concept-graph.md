# 概念关系图谱

```mermaid
graph TD
    macro["macro"]
    style macro fill:#f9f,stroke:#333,stroke-width:4px
    宏["宏"]
    macro -.同义词.- 宏
    宏定义["宏定义"]
    macro -.同义词.- 宏定义
    macro_definition["macro definition"]
    macro -.同义词.- macro_definition
    宏展开["宏展开"]
    macro -.同义词.- 宏展开
    macro_expansion["macro expansion"]
    macro -.同义词.- macro_expansion
    annotation["annotation"]
    macro -->|相关| annotation
    reflect["reflect"]
    macro -->|相关| reflect
    ast{"ast模块"}
    macro -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    basic{"basic模块"}
    macro -->|使用于| basic
    style basic fill:#bbf,stroke:#333
    chir{"chir模块"}
    macro -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    frontendtool{"frontendtool模块"}
    macro -->|使用于| frontendtool
    style frontendtool fill:#bbf,stroke:#333
    include{"include模块"}
    macro -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
