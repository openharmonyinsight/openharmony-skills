# 概念关系图谱

```mermaid
graph TD
    interface["interface"]
    style interface fill:#f9f,stroke:#333,stroke-width:4px
    接口["接口"]
    interface -.同义词.- 接口
    接口定义["接口定义"]
    interface -.同义词.- 接口定义
    interface_definition["interface definition"]
    interface -.同义词.- interface_definition
    抽象["抽象"]
    interface -.同义词.- 抽象
    abstract["abstract"]
    interface -.同义词.- abstract
    class["class"]
    interface -->|相关| class
    struct["struct"]
    interface -->|相关| struct
    extend["extend"]
    interface -->|相关| extend
    implement["implement"]
    interface -->|相关| implement
    chir{"chir模块"}
    interface -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    interface -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    include{"include模块"}
    interface -->|使用于| include
    style include fill:#bbf,stroke:#333
    macro{"macro模块"}
    interface -->|使用于| macro
    style macro fill:#bbf,stroke:#333
    modules{"modules模块"}
    interface -->|使用于| modules
    style modules fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
