# 概念关系图谱

```mermaid
graph TD
    package["package"]
    style package fill:#f9f,stroke:#333,stroke-width:4px
    包["包"]
    package -.同义词.- 包
    模块["模块"]
    package -.同义词.- 模块
    module["module"]
    package -.同义词.- module
    import["import"]
    package -.同义词.- import
    导入["导入"]
    package -.同义词.- 导入
    namespace["namespace"]
    package -->|相关| namespace
    dependency["dependency"]
    package -->|相关| dependency
    chir{"chir模块"}
    package -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    package -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    demangler{"demangler模块"}
    package -->|使用于| demangler
    style demangler fill:#bbf,stroke:#333
    frontend{"frontend模块"}
    package -->|使用于| frontend
    style frontend fill:#bbf,stroke:#333
    frontendtool{"frontendtool模块"}
    package -->|使用于| frontendtool
    style frontendtool fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
