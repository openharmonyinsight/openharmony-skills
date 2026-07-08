# 部分迁移与混用场景

## 涵盖的迁移点

| V1 | V2 | 说明 |
|----|-----|------|
| ForEach | Repeat | 全量加载模式 |
| LazyForEach + IDataSource | Repeat + .virtualScroll() | 懒加载模式 |
| IDataSource / BasicDataSource | @Local 数组 | 直接修改即自动更新 |
| @Observed + @Prop | @ObservedV2 + @Param | 数据对象传递 |
| V1→V2 传复杂类型 (API<19) | 桥接模式 | V1Bridge 中转 |
| V1→V2 传复杂类型 (API>=19) | enableV2Compatibility | 放宽约束 |

## 文件说明

- `before.ets` — V1 列表页，使用 ForEach + LazyForEach + IDataSource，部分 V2 子组件（API<19 只传简单类型）
- `after.ets` — V2 等价实现，Repeat 替代 ForEach/LazyForEach，@Local 数组替代 IDataSource

## 迁移注意

- Repeat 的 `.each()` 回调参数为 `RepeatItem<T>`，通过 `ri.item` 访问数据
- Repeat + `.virtualScroll()` 替代 LazyForEach，不再需要 IDataSource
- 数据更新直接修改 @Local 数组即可，无需 notifyDataAdd/notifyDataDelete
- API < 19 下 V1→V2 传递限制严格：只允许简单类型，复杂类型需桥接模式
- API >= 19 使用 `UIUtils.enableV2Compatibility()` 可放宽约束
