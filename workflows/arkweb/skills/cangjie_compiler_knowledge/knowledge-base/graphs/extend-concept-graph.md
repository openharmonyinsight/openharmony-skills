# 概念关系图谱

```mermaid
graph TD
    extend["extend"]
    style extend fill:#f9f,stroke:#333,stroke-width:4px
    扩展["扩展"]
    extend -.同义词.- 扩展
    extension["extension"]
    extend -.同义词.- extension
    扩展方法["扩展方法"]
    extend -.同义词.- 扩展方法
    extension_method["extension method"]
    extend -.同义词.- extension_method
    扩展接口["扩展接口"]
    extend -.同义词.- 扩展接口
    class["class"]
    extend -->|相关| class
    interface["interface"]
    extend -->|相关| interface
    method["method"]
    extend -->|相关| method
    方法["方法"]
    extend -->|相关| 方法
    chir{"chir模块"}
    extend -->|使用于| chir
    style chir fill:#bbf,stroke:#333
    codegen{"codegen模块"}
    extend -->|使用于| codegen
    style codegen fill:#bbf,stroke:#333
    demangler{"demangler模块"}
    extend -->|使用于| demangler
    style demangler fill:#bbf,stroke:#333
    include{"include模块"}
    extend -->|使用于| include
    style include fill:#bbf,stroke:#333
    incrementalcompilation{"incrementalcompilation模块"}
    extend -->|使用于| incrementalcompilation
    style incrementalcompilation fill:#bbf,stroke:#333
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
