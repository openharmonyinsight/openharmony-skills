# 装饰器映射与组件内状态变量迁移

## 完整映射表

| V1 | V2 | 关键差异 |
|----|-----|---------|
| @Component | @ComponentV2 | 容器装饰器，V1/V2装饰器不可混用 |
| @State | @Local / @Param+@Once | @Local禁止外部初始化；需@ObservedV2+@Trace观察复杂类型 |
| @Prop | @Param | @Param是引用非深拷贝，@Param是只读的 |
| @Link | @Param + @Event | 需手动回调模式实现双向同步 |
| @Observed + @ObjectLink | @ObservedV2 + @Trace | V2深度观测无需子组件分解 |
| @Track | @Trace | 直接替换，精确更新属性 |
| @Provide / @Consume | @Provider / @Consumer | V2需`()`语法；alias为唯一匹配键；@Provider禁止外部初始化 |
| @Watch | @Monitor | V2异步，支持多变量监听，提供before/after值 |
| 无 | @Computed | V2新增，避免重复计算 |
| $$ 绑定 | !! 绑定 | 语法替换 |
| @Reusable | @ReusableV2 | aboutToReuse无参数；自动重置状态变量；reuse()替代reuseId() |
| ForEach | Repeat (全量) | Repeat替代ForEach和LazyForEach |
| LazyForEach | Repeat + .virtualScroll() | 内置懒加载 |

## @State -> @Local / @Param

### 简单类型
直接替换 `@State` → `@Local`

### 复杂类型
V1的@State可观察第一层属性，V2的@Local只能观察自身。需在类上加 `@ObservedV2`，属性加 `@Trace`。

```typescript
// V1
@Component
struct Example {
  @State child: Child = new Child();
}

// V2
@ObservedV2
class Child {
  @Trace public value: number = 10;
}
@ComponentV2
struct Example {
  @Local child: Child = new Child();
}
```

### 外部初始化
V2的@Local禁止外部初始化。需使用 `@Param @Once` 替代。

```typescript
// V1: @State可从外部初始化
@Component
struct Child {
  @State value: number = 0;
}
Parent: Child({ value: 30 })

// V2: 用@Param @Once
@ComponentV2
struct Child {
  @Param @Once value: number = 0;
}
Parent: Child({ value: 30 })
```

## @Prop -> @Param

### 简单类型
直接替换 `@Prop` → `@Param`

### 复杂类型（单向数据绑定）
@Param是引用传递，如需深拷贝需手动clone：
```typescript
Child({ fruit: this.parentFruit.clone() })
```

### 子组件需修改参数
使用 `@Param @Once`，但只同步一次。如需父组件后续更新仍同步，用 `@Param` + `@Monitor`：
```typescript
@ComponentV2
struct Child {
  @Local localValue: number = 0;
  @Param value: number = 0;
  @Monitor('value')
  onValueChange(mon: IMonitor) {
    this.localValue = this.value;
  }
}
```

## @Link -> @Param + @Event

```typescript
// V1: @Link双向同步
@Component struct Child {
  @Link val: number;
}
Parent: Child({ val: this.myVal })

// V2: @Param + @Event回调
@ComponentV2 struct Child {
  @Param val: number = 0;
  @Event addOne: () => void;
}
Parent: Child({ val: this.myVal, addOne: () => this.myVal++ })
```

## @Provide/@Consume -> @Provider/@Consumer

关键差异：
- V2必须加 `()`，即使不指定alias
- alias是唯一匹配key
- @Provider禁止外部初始化（用@Param @Once接收再赋值）
- @Consumer支持本地初始化（找不到@Provider时用默认值）
- @Provider默认支持重载（无需allowOverride）

```typescript
// V1
@Provide('text') message: string = 'Hello';
@Consume('text') childMessage: string;

// V2
@Provider('text') message: string = 'Hello';
@Consumer('text') childMessage: string = 'default';
```

## @Watch -> @Monitor

```typescript
// V1: 单变量监听
@State @Watch('onAppleChange') apple: number = 0;
onAppleChange(): void { ... }

// V2: 支持多变量 + before/after
@Local apple: number = 0;
@Local orange: number = 0;
@Monitor('apple','orange')
onFruitChange(monitor: IMonitor) {
  monitor.dirty.forEach((name: string) => {
    // monitor.value(name)?.before / .now
  });
}
```

## $$ -> !!

直接替换 `$$this.text` → `this.text!!`

## @Computed（V2新增）

```typescript
@Entry
@ComponentV2
struct Index {
  @Local firstName: string = 'Li';
  @Local lastName: string = 'Hua';
  @Computed
  get fullName() {
    return this.firstName + ' ' + this.lastName;
  }
}
```
