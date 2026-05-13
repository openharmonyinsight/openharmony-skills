# Good Example 003: 正确解释 cast 表达式运行时行为

## User Question

```typescript
class Base {}
class Derived extends Base { greet(): void { console.log("hi") } }

let obj: Base = new Base()
let d: Derived = obj as Derived
d.greet()
```

这段 ArkTS 代码运行时会怎样？

## Good Answer

运行时会抛出 **`ClassCastError`**。

**原因**：
1. `obj` 实际类型是 `Base`，不是 `Derived`。
2. ArkTS 中 `as` cast 分两种路径：
   - **字面量 cast**：编译期处理，不会失败。
   - **非字面量 cast**（本例）：走 **Runtime Checking** 路径，运行时检查实际类型。
3. 运行时发现 `Base` 不是 `Derived` 的实例，抛出 `ClassCastError`。

**安全做法**：

```typescript
let obj: Base = new Base()
if (obj instanceof Derived) {
    let d: Derived = obj as Derived
    d.greet()
}
```

依据：`spec/expressions.md` — Cast Expression、Runtime Checking in Cast Expression 章节。

## Why This Is Good

- 明确指出运行时异常
- 解释了 cast 的两种路径
- 给出安全的替代写法
- 引用了依据文件
