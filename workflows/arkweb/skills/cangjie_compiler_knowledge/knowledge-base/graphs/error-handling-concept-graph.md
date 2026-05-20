# 概念关系图谱

```mermaid
graph TD
    error_handling["error-handling"]
    style error_handling fill:#f9f,stroke:#333,stroke-width:4px
    异常["异常"]
    error_handling -.同义词.- 异常
    exception["exception"]
    error_handling -.同义词.- exception
    错误处理["错误处理"]
    error_handling -.同义词.- 错误处理
    error_handling["error handling"]
    error_handling -.同义词.- error_handling
    try["try"]
    error_handling -.同义词.- try
    option["option"]
    error_handling -->|相关| option
    result["result"]
    error_handling -->|相关| result
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
