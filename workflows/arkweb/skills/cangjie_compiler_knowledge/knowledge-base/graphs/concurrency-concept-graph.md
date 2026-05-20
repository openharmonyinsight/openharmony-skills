# 概念关系图谱

```mermaid
graph TD
    concurrency["concurrency"]
    style concurrency fill:#f9f,stroke:#333,stroke-width:4px
    并发["并发"]
    concurrency -.同义词.- 并发
    协程["协程"]
    concurrency -.同义词.- 协程
    coroutine["coroutine"]
    concurrency -.同义词.- coroutine
    async["async"]
    concurrency -.同义词.- async
    await["await"]
    concurrency -.同义词.- await
    future["future"]
    concurrency -->|相关| future
    lock["lock"]
    concurrency -->|相关| lock
    include{"include模块"}
    concurrency -->|使用于| include
    style include fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
