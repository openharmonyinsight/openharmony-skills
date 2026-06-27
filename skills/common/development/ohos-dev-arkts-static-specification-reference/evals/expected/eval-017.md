# Expected Output: eval-017

## Key Points (必须包含)

1. `async` 函数不能按普通同步函数返回值理解。
2. `async` 返回会进入 Promise 语义；返回 `1` 的异步函数应表达为 `Promise<int>` 或规范要求的 Promise 形式。
3. 示例应改为：
   ```typescript
   async function loadValue(): Promise<int> {
       return 1
   }
   ```
4. 依据：`spec/concurrency.md` — async/await；必要时结合 `spec/stdlib.md` 的 Promise 定义。

## Anti-Pattern (不得出现)

- “async function 可以直接返回 int” — 错误
- “async 和同步函数没有区别” — 错误
- 未提 Promise
