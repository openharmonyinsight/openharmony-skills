# 概念关系图谱

```mermaid
graph TD
    sema["sema"]
    style sema fill:#f9f,stroke:#333,stroke-width:4px
    语义分析["语义分析"]
    sema -.同义词.- 语义分析
    semantic_analysis["semantic analysis"]
    sema -.同义词.- semantic_analysis
    类型检查["类型检查"]
    sema -.同义词.- 类型检查
    type_checking["type checking"]
    sema -.同义词.- type_checking
    符号解析["符号解析"]
    sema -.同义词.- 符号解析
    type_system["type-system"]
    sema -->|相关| type_system
    type_inference["type-inference"]
    sema -->|相关| type_inference
    scope["scope"]
    sema -->|相关| scope
    作用域["作用域"]
    sema -->|相关| 作用域
    frontendtool{"frontendtool模块"}
    sema -->|使用于| frontendtool
    style frontendtool fill:#bbf,stroke:#333
    include{"include模块"}
    sema -->|使用于| include
    style include fill:#bbf,stroke:#333
    incrementalcompilation{"incrementalcompilation模块"}
    sema -->|使用于| incrementalcompilation
    style incrementalcompilation fill:#bbf,stroke:#333
    sema{"sema模块"}
    sema -->|使用于| sema
    style sema fill:#bbf,stroke:#333
    unittests{"unittests模块"}
    sema -->|使用于| unittests
    style unittests fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
