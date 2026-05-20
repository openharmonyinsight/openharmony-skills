# 概念关系图谱

```mermaid
graph TD
    generic["generic"]
    style generic fill:#f9f,stroke:#333,stroke-width:4px
    泛型["泛型"]
    generic -.同义词.- 泛型
    generics["generics"]
    generic -.同义词.- generics
    template["template"]
    generic -.同义词.- template
    模板["模板"]
    generic -.同义词.- 模板
    type_parameter["type parameter"]
    generic -.同义词.- type_parameter
    type["type"]
    generic -->|相关| type
    class["class"]
    generic -->|相关| class
    interface["interface"]
    generic -->|相关| interface
    function["function"]
    generic -->|相关| function
    instantiation["instantiation"]
    generic -->|相关| instantiation
    ast{"ast模块"}
    generic -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    basic{"basic模块"}
    generic -->|使用于| basic
    style basic fill:#bbf,stroke:#333
    chir{"chir模块"}
    generic -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    generic -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    demangler{"demangler模块"}
    generic -->|使用于| demangler
    style demangler fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
