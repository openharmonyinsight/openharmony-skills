# 简单组件迁移：@State / @Prop

## 涵盖的迁移点

| V1 | V2 | 说明 |
|----|-----|------|
| @Component | @ComponentV2 | 容器装饰器替换 |
| @State | @Local | 内部状态，V2 禁止外部初始化 |
| @Prop | @Param | 父传子，V2 引用传递、只读 |

## 文件说明

- `before.ets` — V1 计数器，使用 @State 内部状态 + @Prop 子组件接收
- `after.ets` — V2 等价实现，@Local 替代 @State，@Param 替代 @Prop

## 迁移注意

- @Local **禁止**外部初始化。如需从父组件传入初始值，用 `@Param @Once`
- @Param 是引用传递（非深拷贝），如需深拷贝需手动 `.clone()`
- @Param 是只读的，子组件不能直接修改
