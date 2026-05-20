# 概念关系图谱

```mermaid
graph TD
    type_inference["type-inference"]
    style type_inference fill:#f9f,stroke:#333,stroke-width:4px
    类型推断["类型推断"]
    type_inference -.同义词.- 类型推断
    type_inference["type inference"]
    type_inference -.同义词.- type_inference
    类型推导["类型推导"]
    type_inference -.同义词.- 类型推导
    type_deduction["type deduction"]
    type_inference -.同义词.- type_deduction
    infer["infer"]
    type_inference -.同义词.- infer
    type["type"]
    type_inference -->|相关| type
    generic["generic"]
    type_inference -->|相关| generic
    lambda["lambda"]
    type_inference -->|相关| lambda
    var["var"]
    type_inference -->|相关| var
    类型系统["类型系统"]
    type_inference -->|相关| 类型系统
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
