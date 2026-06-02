# Eval 012: static 方法是否继承

## User Prompt

```typescript
class Base {
    static make(): string {
        return "base"
    }
}

class Derived extends Base {
}

let r = Derived.make()
```

ArkTS 中 `static` 方法会像实例方法一样被继承吗？`Derived.make()` 是否应该直接可用？

## Evaluation Criteria

1. 必须说明 static 方法不能按实例方法继承规则处理
2. 必须指出静态成员查找只看当前类静态上下文或规范明确允许的静态访问规则
3. 必须避免套用 JavaScript 原型继承直觉
4. 必须引用 `spec/classes.md` 或 `spec/semantics.md`
