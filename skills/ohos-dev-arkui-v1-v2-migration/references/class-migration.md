# 数据对象迁移：@Observed/@ObjectLink/@Track -> @ObservedV2/@Trace

## 核心映射

| V1 | V2 | 说明 |
|----|-----|------|
| @Observed | @ObservedV2 | @ObservedV2本身无观察能力，需配合@Trace |
| @ObjectLink | @ObservedV2 + @Trace | V2深度观测，不再需要子组件分解 |
| @Track | @Trace | 直接替换 |

## 嵌套对象属性观察

V1中只能观察第一层属性，嵌套对象需要通过 @ObjectLink + 自定义组件逐层拆解。
V2中 @ObservedV2 + @Trace 可以直接深度观察，无需子组件分解。

```typescript
// V1: 需要拆分子组件
@Observed
class Address {
  public city: string;
}
@Observed
class User {
  public name: string;
  public address: Address;
}
// 需要AddressView子组件 + @ObjectLink才能观察address.city

// V2: 直接深度观察
@ObservedV2
class Address {
  @Trace public city: string;
}
@ObservedV2
class User {
  @Trace public name: string;
  @Trace public address: Address;
}
@ComponentV2
struct UserProfile {
  @Local user: User = new User('Alice', new Address('NY'));
  // 可直接观察 this.user.address.city
}
```

## 类属性精确更新

```typescript
// V1
@Observed
class User {
  @Track public name: string;
  @Track public age: number;
}

// V2
@ObservedV2
class User {
  @Trace public name: string;
  @Trace public age: number;
}
```

## 关键规则

1. @Observed 和 @ObservedV2 **不能**同时装饰同一个类
2. @Component 中不能使用 @ObservedV2 装饰的类型配合 V1 装饰器
3. @ComponentV2 中不能使用 @Observed 装饰的类型配合 V2 装饰器
4. @Trace 装饰的属性无论嵌套多少层都能被观测
5. @ObservedV2 + @Trace 可在 @Component 中独立使用（不与V1装饰器混用）
