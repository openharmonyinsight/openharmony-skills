# 概念关系图谱

```mermaid
graph TD
    syntax_sugar["syntax-sugar"]
    style syntax_sugar fill:#f9f,stroke:#333,stroke-width:4px
    语法糖["语法糖"]
    syntax_sugar -.同义词.- 语法糖
    syntactic_sugar["syntactic sugar"]
    syntax_sugar -.同义词.- syntactic_sugar
    sugar["sugar"]
    syntax_sugar -.同义词.- sugar
    糖["糖"]
    syntax_sugar -.同义词.- 糖
    语法便利["语法便利"]
    syntax_sugar -.同义词.- 语法便利
    desugaring["desugaring"]
    syntax_sugar -->|相关| desugaring
    parser["parser"]
    syntax_sugar -->|相关| parser
    enum["enum"]
    syntax_sugar -->|相关| enum
    sema["sema"]
    syntax_sugar -->|相关| sema
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
