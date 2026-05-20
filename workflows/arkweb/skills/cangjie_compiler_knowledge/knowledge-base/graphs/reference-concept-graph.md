# 概念关系图谱

```mermaid
graph TD
    reference["reference"]
    style reference fill:#f9f,stroke:#333,stroke-width:4px
    引用["引用"]
    reference -.同义词.- 引用
    引用类型["引用类型"]
    reference -.同义词.- 引用类型
    reference_type["reference type"]
    reference -.同义词.- reference_type
    ref["ref"]
    reference -.同义词.- ref
    &["&"]
    reference -.同义词.- &
    pointer["pointer"]
    reference -->|相关| pointer
    type_system["type-system"]
    reference -->|相关| type_system
    variable["variable"]
    reference -->|相关| variable
    codegen{"codegen模块"}
    reference -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    include{"include模块"}
    reference -->|使用于| include
    style include fill:#bbf,stroke:#333
    modules{"modules模块"}
    reference -->|使用于| modules
    style modules fill:#bbf,stroke:#333
    sema{"sema模块"}
    reference -->|使用于| sema
    style sema fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
