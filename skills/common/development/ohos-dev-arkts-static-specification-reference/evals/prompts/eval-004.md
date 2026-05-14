# Eval 004: 泛型约束默认值

## User Prompt

```typescript
class Container<T> {
    value: T
    constructor(value: T) {
        this.value = value
    }
    getValue(): T {
        return this.value
    }
}
let c = new Container("hello")
c.getValue().length  // 能调用 .length 吗？
```

这段 ArkTS 代码有什么问题？

## Evaluation Criteria

1. 必须指出无显式约束时泛型参数默认 extends Any
2. 必须指出 Any 没有方法和字段，因此 .length 不可用
3. 必须给出添加约束的修正方案
4. 必须引用 spec/generics.md
