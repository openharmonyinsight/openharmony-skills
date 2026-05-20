# 概念关系图谱

```mermaid
graph TD
    enum["enum"]
    style enum fill:#f9f,stroke:#333,stroke-width:4px
    枚举["枚举"]
    enum -.同义词.- 枚举
    枚举类型["枚举类型"]
    enum -.同义词.- 枚举类型
    enumeration["enumeration"]
    enum -.同义词.- enumeration
    枚举值["枚举值"]
    enum -.同义词.- 枚举值
    enum_value["enum value"]
    enum -.同义词.- enum_value
    pattern_match["pattern-match"]
    enum -->|相关| pattern_match
    option["option"]
    enum -->|相关| option
    case["case"]
    enum -->|相关| case
    分支["分支"]
    enum -->|相关| 分支
    chir{"chir模块"}
    enum -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    enum -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    include{"include模块"}
    enum -->|使用于| include
    style include fill:#bbf,stroke:#333
    macro{"macro模块"}
    enum -->|使用于| macro
    style macro fill:#bbf,stroke:#333
    mangle{"mangle模块"}
    enum -->|使用于| mangle
    style mangle fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
