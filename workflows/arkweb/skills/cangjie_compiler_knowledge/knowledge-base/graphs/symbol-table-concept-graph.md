# 概念关系图谱

```mermaid
graph TD
    symbol_table["symbol-table"]
    style symbol_table fill:#f9f,stroke:#333,stroke-width:4px
    符号表["符号表"]
    symbol_table -.同义词.- 符号表
    symbol["symbol"]
    symbol_table -.同义词.- symbol
    符号["符号"]
    symbol_table -.同义词.- 符号
    标识符表["标识符表"]
    symbol_table -.同义词.- 标识符表
    identifier_table["identifier table"]
    symbol_table -.同义词.- identifier_table
    scope["scope"]
    symbol_table -->|相关| scope
    name_resolution["name-resolution"]
    symbol_table -->|相关| name_resolution
    sema["sema"]
    symbol_table -->|相关| sema
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
