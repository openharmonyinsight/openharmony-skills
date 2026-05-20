# 概念关系图谱

```mermaid
graph TD
    struct["struct"]
    style struct fill:#f9f,stroke:#333,stroke-width:4px
    结构体["结构体"]
    struct -.同义词.- 结构体
    值类型["值类型"]
    struct -.同义词.- 值类型
    value_type["value type"]
    struct -.同义词.- value_type
    structure["structure"]
    struct -.同义词.- structure
    class["class"]
    struct -->|相关| class
    interface["interface"]
    struct -->|相关| interface
    generic["generic"]
    struct -->|相关| generic
    member["member"]
    struct -->|相关| member
    ast{"ast模块"}
    struct -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    basic{"basic模块"}
    struct -->|使用于| basic
    style basic fill:#bbf,stroke:#333
    chir{"chir模块"}
    struct -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    struct -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    demangler{"demangler模块"}
    struct -->|使用于| demangler
    style demangler fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
