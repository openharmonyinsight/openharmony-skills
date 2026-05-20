# 概念关系图谱

```mermaid
graph TD
    const["const"]
    style const fill:#f9f,stroke:#333,stroke-width:4px
    常量["常量"]
    const -.同义词.- 常量
    constant["constant"]
    const -.同义词.- constant
    不可变["不可变"]
    const -.同义词.- 不可变
    immutable["immutable"]
    const -.同义词.- immutable
    let["let"]
    const -.同义词.- let
    var["var"]
    const -->|相关| var
    变量["变量"]
    const -->|相关| 变量
    variable["variable"]
    const -->|相关| variable
    chir{"chir模块"}
    const -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    const -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    include{"include模块"}
    const -->|使用于| include
    style include fill:#bbf,stroke:#333
    incrementalcompilation{"incrementalcompilation模块"}
    const -->|使用于| incrementalcompilation
    style incrementalcompilation fill:#bbf,stroke:#333
    modules{"modules模块"}
    const -->|使用于| modules
    style modules fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
