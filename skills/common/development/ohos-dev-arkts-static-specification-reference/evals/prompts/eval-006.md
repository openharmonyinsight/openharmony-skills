# Eval 006: as cast 表达式的运行时行为

## User Prompt

```typescript
class Animal {}
class Dog extends Animal { bark(): void {} }
class Cat extends Animal { meow(): void {} }

let pet: Animal = new Cat()
let dog: Dog = pet as Dog
dog.bark()
```

这段 ArkTS 代码 `pet as Dog` 一定成功吗？如果实际运行时 pet 是 Cat，会怎样？

## Evaluation Criteria

1. 必须指出非字面量 cast 走 Runtime Checking 路径
2. 必须指出类型不匹配时抛出 ClassCastError
3. 不得说 "as cast 一定成功" 或 "as 只是类型声明"
4. 必须引用 spec/expressions.md
