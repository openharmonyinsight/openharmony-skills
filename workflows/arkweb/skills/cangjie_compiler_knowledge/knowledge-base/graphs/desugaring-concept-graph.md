# 概念关系图谱

```mermaid
graph TD
    desugaring["desugaring"]
    style desugaring fill:#f9f,stroke:#333,stroke-width:4px
    去糖化["去糖化"]
    desugaring -.同义词.- 去糖化
    desugar["desugar"]
    desugaring -.同义词.- desugar
    脱糖["脱糖"]
    desugaring -.同义词.- 脱糖
    sugar_elimination["sugar elimination"]
    desugaring -.同义词.- sugar_elimination
    语法糖消除["语法糖消除"]
    desugaring -.同义词.- 语法糖消除
    syntax_sugar["syntax-sugar"]
    desugaring -->|相关| syntax_sugar
    parser["parser"]
    desugaring -->|相关| parser
    sema["sema"]
    desugaring -->|相关| sema
    ast["ast"]
    desugaring -->|相关| ast
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
