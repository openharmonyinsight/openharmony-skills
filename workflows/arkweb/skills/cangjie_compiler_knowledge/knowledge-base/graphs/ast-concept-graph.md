# 概念关系图谱

```mermaid
graph TD
    ast["ast"]
    style ast fill:#f9f,stroke:#333,stroke-width:4px
    抽象语法树["抽象语法树"]
    ast -.同义词.- 抽象语法树
    abstract_syntax_tree["abstract syntax tree"]
    ast -.同义词.- abstract_syntax_tree
    syntax_tree["syntax tree"]
    ast -.同义词.- syntax_tree
    语法树["语法树"]
    ast -.同义词.- 语法树
    parse["parse"]
    ast -->|相关| parse
    sema["sema"]
    ast -->|相关| sema
    node["node"]
    ast -->|相关| node
    walker["walker"]
    ast -->|相关| walker
    visitor["visitor"]
    ast -->|相关| visitor
    ast{"ast模块"}
    ast -->|使用于| ast
    style ast fill:#bbf,stroke:#333
    chir{"chir模块"}
    ast -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    conditionalcompilation{"conditionalcompilation模块"}
    ast -->|使用于| conditionalcompilation
    style conditionalcompilation fill:#bbf,stroke:#333
    frontend{"frontend模块"}
    ast -->|使用于| frontend
    style frontend fill:#bbf,stroke:#333
    include{"include模块"}
    ast -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
