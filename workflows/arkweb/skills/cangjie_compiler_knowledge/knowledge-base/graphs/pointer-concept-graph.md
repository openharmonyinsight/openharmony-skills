# 概念关系图谱

```mermaid
graph TD
    pointer["pointer"]
    style pointer fill:#f9f,stroke:#333,stroke-width:4px
    指针["指针"]
    pointer -.同义词.- 指针
    指针类型["指针类型"]
    pointer -.同义词.- 指针类型
    pointer_type["pointer type"]
    pointer -.同义词.- pointer_type
    raw_pointer["raw pointer"]
    pointer -.同义词.- raw_pointer
    *["*"]
    pointer -.同义词.- *
    reference["reference"]
    pointer -->|相关| reference
    type_system["type-system"]
    pointer -->|相关| type_system
    cffi["cffi"]
    pointer -->|相关| cffi
    unsafe["unsafe"]
    pointer -->|相关| unsafe
    chir{"chir模块"}
    pointer -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    pointer -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    demangler{"demangler模块"}
    pointer -->|使用于| demangler
    style demangler fill:#bbf,stroke:#333
    frontend{"frontend模块"}
    pointer -->|使用于| frontend
    style frontend fill:#bbf,stroke:#333
    include{"include模块"}
    pointer -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
