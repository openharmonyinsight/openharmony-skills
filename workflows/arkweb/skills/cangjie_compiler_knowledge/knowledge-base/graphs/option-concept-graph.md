# 概念关系图谱

```mermaid
graph TD
    option["option"]
    style option fill:#f9f,stroke:#333,stroke-width:4px
    可选类型["可选类型"]
    option -.同义词.- 可选类型
    optional_type["optional type"]
    option -.同义词.- optional_type
    enum["enum"]
    option -->|相关| enum
    pattern_match["pattern-match"]
    option -->|相关| pattern_match
    null["null"]
    option -->|相关| null
    codegen{"codegen模块"}
    option -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    driver{"driver模块"}
    option -->|使用于| driver
    style driver fill:#bbf,stroke:#333
    frontend{"frontend模块"}
    option -->|使用于| frontend
    style frontend fill:#bbf,stroke:#333
    include{"include模块"}
    option -->|使用于| include
    style include fill:#bbf,stroke:#333
    option{"option模块"}
    option -->|使用于| option
    style option fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
