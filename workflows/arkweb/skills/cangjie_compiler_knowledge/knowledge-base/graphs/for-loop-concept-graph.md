# 概念关系图谱

```mermaid
graph TD
    for_loop["for-loop"]
    style for_loop fill:#f9f,stroke:#333,stroke-width:4px
    for["for"]
    for_loop -.同义词.- for
    循环["循环"]
    for_loop -.同义词.- 循环
    loop["loop"]
    for_loop -.同义词.- loop
    for_in["for-in"]
    for_loop -.同义词.- for_in
    迭代["迭代"]
    for_loop -.同义词.- 迭代
    iterator["iterator"]
    for_loop -->|相关| iterator
    collections["collections"]
    for_loop -->|相关| collections
    break["break"]
    for_loop -->|相关| break
    continue["continue"]
    for_loop -->|相关| continue
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
