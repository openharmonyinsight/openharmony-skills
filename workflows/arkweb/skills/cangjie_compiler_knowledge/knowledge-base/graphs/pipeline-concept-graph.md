# 概念关系图谱

```mermaid
graph TD
    pipeline["pipeline"]
    style pipeline fill:#f9f,stroke:#333,stroke-width:4px
    管道运算符["管道运算符"]
    pipeline -.同义词.- 管道运算符
    pipeline_operator["pipeline operator"]
    pipeline -.同义词.- pipeline_operator
    |>["|>"]
    pipeline -.同义词.- |>
    pipe["pipe"]
    pipeline -.同义词.- pipe
    管道["管道"]
    pipeline -.同义词.- 管道
    function["function"]
    pipeline -->|相关| function
    operator["operator"]
    pipeline -->|相关| operator
    composition["composition"]
    pipeline -->|相关| composition
    ast{"ast模块"}
    pipeline -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    sema{"sema模块"}
    pipeline -->|使用于| sema
    style sema fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
