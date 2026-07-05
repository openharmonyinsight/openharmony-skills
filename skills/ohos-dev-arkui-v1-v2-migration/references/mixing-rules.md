# V1/V2 混用规则

> 迁移过程中V1与V2必然存在共存，需严格遵循混用规则避免编译错误和运行时问题。

## 判断API版本（关键前置步骤）

迁移前必须检测应用API版本：
- `build-profile.json5` → `compatibleSdkVersion` / `targetSdkVersion`
- `AppScope/app.json5` → `minAPIVersion`
- `module.json5` → `minAPIVersion`

**API < 19**: 严格混用约束，复杂类型不可跨V1/V2传递
**API >= 19**: 放宽约束，提供 enableV2Compatibility 和 makeV1Observed API

---

## API < 19 混用规则

### 通用限制
- V1和V2装饰器**不允许**在同一个组件内混用（编译报错）
- @Observed 和 @ObservedV2 **不能**共存于同一个类
- 多个装饰器不允许装饰同一个变量（@Watch/@Once/@Require除外）

### V1 -> V2 传递
- 不传变量：V1可以使用V2组件
- 传递普通变量（未装饰）：V2用 @Param 接收
- 传递状态变量：仅限简单类型（boolean/number/string/null/undefined），V2用 @Param 接收
- **禁止**传递：@Observed装饰的class、内置类型（Array/Map/Set/Date）

### V2 -> V1 传递
- 不传变量：V2可以使用V1组件
- V1接收仅限：@State、@Prop、@Provide（不用装饰器也行）
- **禁止**V1接收：内置类型（Array/Set/Map/Date）、Function
- @Link 只能被V1状态变量初始化

### 桥接模式（V1传@Observed class给V2）
当V1需要传递@Observed装饰的class给V2组件时，需使用桥接组件：

```
V1Comp → V1BridgeComponent(@Component) → V2Comp(@ComponentV2)
```

桥接组件是**纯 V1 组件**（不得用 V1 装饰器持有 `@ObservedV2` class）：把 `@Observed` class 拆成简单类型字段，逐个传给 V2 子组件的 `@Param`。如需多组件共享同一份数据，改用独立的 `@ObservedV2`/`@Trace` 单例，由 V1 直接写入属性、V2 用 `@Local`+`@Monitor` 读取（见 `templates/bridge-pattern-template.ets` 方案三）。
`@Watch` 用于在变量被重新赋值时触发回调副作用，须装饰在被监听的变量上、参数为回调方法名；嵌套 `@Track` 属性变化靠 `build()` 中的读取自动刷新，无需手动同步。

---

## API >= 19 混用规则

### 新增API

#### UIUtils.makeV1Observed()
将不可观察对象包装为V1可观察对象，等价于 @Observed。返回值可初始化 @ObjectLink。
- 不支持 collections类型 和 @Sendable 装饰的class
- 不支持非object/undefined/null
- 不支持 @ObservedV2 装饰的类

#### UIUtils.enableV2Compatibility()
将V1状态变量使能V2观察能力，使其在 @ComponentV2 中可观察变化。
- 会递归遍历class属性、Array/Set/Map子项
- 建议在V2组件构造处调用

### V1 -> V2 传递（API >= 19）
简单类型：直接传递
复杂类型：在V2组件构造处调用 enableV2Compatibility
```typescript
SubComponentV2({ param: UIUtils.enableV2Compatibility(this.state) })
```

### V2 -> V1 传递（API >= 19）
共享的 class 必须是【普通 class 或 @Observed+@Track 装饰的 class】，**不能是 @ObservedV2**（makeV1Observed 不支持 @ObservedV2，且 V1 不能用装饰器接收 @ObservedV2 class）。V2 侧用 `makeV1Observed` 包成 V1 状态变量、再 `enableV2Compatibility` 使其在 V2 可观察；V1 侧用 `@ObjectLink` 接收（不能用 @State）：
```typescript
// 普通 class：需 makeV1Observed + enableV2Compatibility
@Local model: Model = UIUtils.enableV2Compatibility(UIUtils.makeV1Observed(new Model()));
// 已是 @Observed 装饰的 class：无需 makeV1Observed
@Local model: ObservedModel = UIUtils.enableV2Compatibility(new ObservedModel());

// V1 子组件用 @ObjectLink 接收（makeV1Observed 返回值 / @Observed 实例可初始化 @ObjectLink）
@ObjectLink data: Model;
```

### 关键规则
- 使用 `enableV2Compatibility(makeV1Observed(...))` 拉齐 V1/V2 观察能力、避免双重代理；若类已是 @Observed 装饰则省略 makeV1Observed
- 新增数据到已使能V2的集合时，新数据也需是V1状态变量
- @Track装饰的属性在V1和V2均可观察；非@Track属性在V2不崩溃但不更新

### @ObservedV2/@Trace 限制（所有API版本）
- V1装饰器不能和 @ObservedV2 一起使用
- V1不支持用装饰器接收 @ObservedV2 装饰的class
