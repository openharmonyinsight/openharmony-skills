# Eval 009: 只返回类型不同不能构成重载

## User Prompt

```typescript
function parse(x: string): int {
    return 1
}

function parse(x: string): string {
    return x
}
```

这两个函数参数一样，只是返回类型不同，在 ArkTS 中可以作为重载吗？

## Evaluation Criteria

1. 必须指出不能仅依靠返回类型构成重载
2. 必须说明参数列表/签名等价会导致编译期错误
3. 必须说明调用点无法仅凭返回上下文区分这两个重载
4. 必须引用 `spec/semantics.md`
