# 概念关系图谱

```mermaid
graph TD
    pattern_match["pattern-match"]
    style pattern_match fill:#f9f,stroke:#333,stroke-width:4px
    模式匹配["模式匹配"]
    pattern_match -.同义词.- 模式匹配
    pattern_matching["pattern matching"]
    pattern_match -.同义词.- pattern_matching
    match["match"]
    pattern_match -.同义词.- match
    匹配["匹配"]
    pattern_match -.同义词.- 匹配
    case["case"]
    pattern_match -.同义词.- case
    enum["enum"]
    pattern_match -->|相关| enum
    option["option"]
    pattern_match -->|相关| option
    exhaustiveness["exhaustiveness"]
    pattern_match -->|相关| exhaustiveness
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
