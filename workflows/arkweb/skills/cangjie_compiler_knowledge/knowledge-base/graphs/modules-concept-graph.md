# 概念关系图谱

```mermaid
graph TD
    modules["modules"]
    style modules fill:#f9f,stroke:#333,stroke-width:4px
    模块系统["模块系统"]
    modules -.同义词.- 模块系统
    module_system["module system"]
    modules -.同义词.- module_system
    import["import"]
    modules -.同义词.- import
    export["export"]
    modules -.同义词.- export
    package_management["package management"]
    modules -.同义词.- package_management
    package["package"]
    modules -->|相关| package
    import["import"]
    modules -->|相关| import
    dependency["dependency"]
    modules -->|相关| dependency
    codegen{"codegen模块"}
    modules -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    frontendtool{"frontendtool模块"}
    modules -->|使用于| frontendtool
    style frontendtool fill:#bbf,stroke:#333
    include{"include模块"}
    modules -->|使用于| include
    style include fill:#bbf,stroke:#333
    modules{"modules模块"}
    modules -->|使用于| modules
    style modules fill:#bbf,stroke:#333
    sema{"sema模块"}
    modules -->|使用于| sema
    style sema fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
