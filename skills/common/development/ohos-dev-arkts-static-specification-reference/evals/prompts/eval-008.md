# Eval 008: overload 顺序与遮蔽

## User Prompt

```typescript
function pick(x: number): string {
    return "number"
}

function pick(x: int): string {
    return "int"
}

let r = pick(1)
```

这个调用应该优先匹配 `int` 版本吗？如果宽类型 `number` 写在前面，会不会影响后面的窄类型重载？

## Evaluation Criteria

1. 必须说明 ArkTS 重载选择与 overload set 的文本/列表顺序有关
2. 必须指出先出现的宽类型可能遮蔽后续窄类型
3. 必须说明后续永远不可达重载应产生 warning 或诊断
4. 必须引用 `spec/semantics.md`
5. 不得简单套用 TypeScript 重载习惯
