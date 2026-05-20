# 概念关系图谱

```mermaid
graph TD
    overload["overload"]
    style overload fill:#f9f,stroke:#333,stroke-width:4px
    重载["重载"]
    overload -.同义词.- 重载
    overloading["overloading"]
    overload -.同义词.- overloading
    function_overload["function overload"]
    overload -.同义词.- function_overload
    函数重载["函数重载"]
    overload -.同义词.- 函数重载
    operator_overload["operator overload"]
    overload -.同义词.- operator_overload
    function["function"]
    overload -->|相关| function
    operator["operator"]
    overload -->|相关| operator
    type["type"]
    overload -->|相关| type
    resolution["resolution"]
    overload -->|相关| resolution
    parse{"parse模块"}
    overload -->|使用于| parse
    style parse fill:#bbf,stroke:#333
    sema{"sema模块"}
    overload -->|使用于| sema
    style sema fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
