# 概念关系图谱

```mermaid
graph TD
    class["class"]
    style class fill:#f9f,stroke:#333,stroke-width:4px
    类["类"]
    class -.同义词.- 类
    类定义["类定义"]
    class -.同义词.- 类定义
    class_definition["class definition"]
    class -.同义词.- class_definition
    面向对象["面向对象"]
    class -.同义词.- 面向对象
    struct["struct"]
    class -->|相关| struct
    interface["interface"]
    class -->|相关| interface
    extend["extend"]
    class -->|相关| extend
    generic["generic"]
    class -->|相关| generic
    constructor["constructor"]
    class -->|相关| constructor
    ast{"ast模块"}
    class -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    basic{"basic模块"}
    class -->|使用于| basic
    style basic fill:#bbf,stroke:#333
    chir{"chir模块"}
    class -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    class -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    conditionalcompilation{"conditionalcompilation模块"}
    class -->|使用于| conditionalcompilation
    style conditionalcompilation fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
