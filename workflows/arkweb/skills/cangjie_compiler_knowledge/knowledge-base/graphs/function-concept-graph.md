# 概念关系图谱

```mermaid
graph TD
    function["function"]
    style function fill:#f9f,stroke:#333,stroke-width:4px
    函数["函数"]
    function -.同义词.- 函数
    func["func"]
    function -.同义词.- func
    方法["方法"]
    function -.同义词.- 方法
    method["method"]
    function -.同义词.- method
    函数定义["函数定义"]
    function -.同义词.- 函数定义
    lambda["lambda"]
    function -->|相关| lambda
    closure["closure"]
    function -->|相关| closure
    overload["overload"]
    function -->|相关| overload
    generic["generic"]
    function -->|相关| generic
    parameter["parameter"]
    function -->|相关| parameter
    return["return"]
    function -->|相关| return
    ast{"ast模块"}
    function -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    basic{"basic模块"}
    function -->|使用于| basic
    style basic fill:#bbf,stroke:#333
    chir{"chir模块"}
    function -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    function -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    conditionalcompilation{"conditionalcompilation模块"}
    function -->|使用于| conditionalcompilation
    style conditionalcompilation fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
