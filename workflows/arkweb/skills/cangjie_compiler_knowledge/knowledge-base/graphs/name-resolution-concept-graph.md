# 概念关系图谱

```mermaid
graph TD
    name_resolution["name-resolution"]
    style name_resolution fill:#f9f,stroke:#333,stroke-width:4px
    名称解析["名称解析"]
    name_resolution -.同义词.- 名称解析
    符号解析["符号解析"]
    name_resolution -.同义词.- 符号解析
    symbol_resolution["symbol resolution"]
    name_resolution -.同义词.- symbol_resolution
    identifier_resolution["identifier resolution"]
    name_resolution -.同义词.- identifier_resolution
    标识符解析["标识符解析"]
    name_resolution -.同义词.- 标识符解析
    symbol_table["symbol-table"]
    name_resolution -->|相关| symbol_table
    scope["scope"]
    name_resolution -->|相关| scope
    sema["sema"]
    name_resolution -->|相关| sema
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
