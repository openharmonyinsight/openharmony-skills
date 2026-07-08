# 数据对象迁移：@Observed / @ObjectLink / @Track

## 涵盖的迁移点

| V1 | V2 | 说明 |
|----|-----|------|
| @Observed | @ObservedV2 | V2 本身无观察能力，需配合 @Trace |
| @ObjectLink | 不再需要 | V2 @Trace 支持深度观测，无需子组件分解 |
| @Track | @Trace | 直接替换，精确更新属性 |
| $$ | !! | 绑定语法替换 |

## 文件说明

- `before.ets` — V1 三层嵌套对象（User→Address→City），需要 3 个子组件 + @ObjectLink 才能观测深层属性
- `after.ets` — V2 等价实现，单组件直接观测任意深度属性，无需子组件分解

## 迁移注意

- @Observed 和 @ObservedV2 **不能**同时装饰同一个类
- V2 中 @Trace 支持任意深度嵌套观测，这是最大的简化点
- 嵌套对象的每一层都需要 @ObservedV2 + @Trace
- @Component 中不能使用 @ObservedV2 配合 V1 装饰器；反之亦然
