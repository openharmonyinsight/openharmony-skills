# Expected Output: eval-007

## Key Points (必须包含)

1. **两种赋值都不合法**，都是 compile-time error。
2. `FixedArray<T>` 和 `Array<T>`（ResizableArray）是**两种不同的类型**，互不可赋值。
3. `FixedArray` 是固定长度数组，没有 Array 的方法（如 push、pop、splice 等）。
4. `Array`（ResizableArray）是可变长度数组，拥有完整的数组方法。
5. 依据：`spec/types.md` — FixedArray 和 Array 相关章节。

## Anti-Pattern (不得出现)

- "都是数组可以互相赋值" — 错误
- "FixedArray 有 push/pop 方法" — 错误
- 未区分两种数组类型的本质差异
