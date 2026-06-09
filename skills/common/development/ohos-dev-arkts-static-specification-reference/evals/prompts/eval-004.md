# Eval 004: 泛型约束默认值与成员访问

## User Prompt

```typescript
class Container<T> {
    value: T

    constructor(value: T) {
        this.value = value
    }

    getLength(): int {
        return this.value.length
    }
}
```

这段 ArkTS 代码能编译通过吗？`this.value.length` 为什么不能直接访问？

## Evaluation Criteria

1. 必须指出无显式约束时泛型参数默认 extends Any
2. 必须指出 Any 没有方法和字段，因此在泛型类体内 `T` 上不能直接访问 `.length`
3. 必须给出添加约束的修正方案
4. 必须引用 spec/generics.md 和 spec/types.md
5. 不得把该场景解释成实例化后 `T` 已经是 `string`
