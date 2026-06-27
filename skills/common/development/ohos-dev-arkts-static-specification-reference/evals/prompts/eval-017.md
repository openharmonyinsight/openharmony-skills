# Eval 017: async/await 与 Promise 返回类型

## User Prompt

```typescript
async function loadValue(): int {
    return 1
}
```

ArkTS 中 async 函数可以直接声明返回 `int` 吗？还是应该返回 `Promise<int>`？

## Evaluation Criteria

1. 必须说明 async 函数返回值与 Promise 语义相关
2. 必须指出应按规范声明 Promise 包装后的返回类型
3. 必须引用 `spec/concurrency.md` 或 `spec/stdlib.md`
4. 不得把 async 函数当普通同步函数处理
