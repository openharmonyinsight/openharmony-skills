# Eval 010: 接口继承方法优先级

## User Prompt

```typescript
interface ParentA {
    run(x: number): string
}

interface ParentB {
    run(x: string): string
}

interface Child extends ParentA, ParentB {
    run(x: int): string
}
```

如果接口继承链上当前接口和父接口都有同名方法，候选方法应该按什么顺序进入方法集合？当前接口方法和父接口方法谁优先？

## Evaluation Criteria

1. 必须说明当前接口声明的方法优先于父接口继承的方法
2. 必须说明多个父接口按 `extends` 列表顺序参与
3. 必须说明同名等价签名需要去重或冲突检查
4. 必须引用 `spec/interfaces.md` 和/或 `spec/semantics.md`
