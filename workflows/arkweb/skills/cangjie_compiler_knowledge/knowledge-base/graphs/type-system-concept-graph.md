# 概念关系图谱

```mermaid
graph TD
    type_system["type-system"]
    style type_system fill:#f9f,stroke:#333,stroke-width:4px
    类型系统["类型系统"]
    type_system -.同义词.- 类型系统
    type_system["type system"]
    type_system -.同义词.- type_system
    类型检查["类型检查"]
    type_system -.同义词.- 类型检查
    type_checking["type checking"]
    type_system -.同义词.- type_checking
    类型安全["类型安全"]
    type_system -.同义词.- 类型安全
    type_inference["type-inference"]
    type_system -->|相关| type_inference
    generic["generic"]
    type_system -->|相关| generic
    class["class"]
    type_system -->|相关| class
    interface["interface"]
    type_system -->|相关| interface
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
