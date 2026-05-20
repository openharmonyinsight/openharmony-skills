# 概念关系图谱

```mermaid
graph TD
    reflection["reflection"]
    style reflection fill:#f9f,stroke:#333,stroke-width:4px
    反射["反射"]
    reflection -.同义词.- 反射
    注解["注解"]
    reflection -.同义词.- 注解
    annotation["annotation"]
    reflection -.同义词.- annotation
    元数据["元数据"]
    reflection -.同义词.- 元数据
    metadata["metadata"]
    reflection -.同义词.- metadata
    macro["macro"]
    reflection -->|相关| macro
    type["type"]
    reflection -->|相关| type
    attribute["attribute"]
    reflection -->|相关| attribute
    codegen{"codegen模块"}
    reflection -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    include{"include模块"}
    reflection -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
