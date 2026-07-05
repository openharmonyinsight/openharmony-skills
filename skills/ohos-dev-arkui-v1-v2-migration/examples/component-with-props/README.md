# 复杂父子交互迁移：@Link / @Provide/@Consume / @Watch / $$

## 涵盖的迁移点

| V1 | V2 | 说明 |
|----|-----|------|
| @Link | @Param + @Event | V2 用回调模式实现双向同步 |
| @Provide / @Consume | @Provider / @Consumer | V2 需加 `()`，alias 为匹配键 |
| @Watch | @Monitor | 异步，支持多变量，提供 before/after |
| $$ | !! | 双向绑定语法替换 |

## 文件说明

- `before.ets` — V1 设置页，使用 @Link 双向同步、@Provide/@Consume 跨层级、@Watch 监听、$$ 绑定
- `after.ets` — V2 等价实现，@Param+@Event 回调模式、@Provider/@Consumer、@Monitor

## 迁移注意

- @Link → @Param + @Event 需要手动定义回调函数，父组件在回调中更新本地状态
- @Provider 禁止外部初始化；如需接收外部值再广播，用 @Param @Once 接收再赋值
- @Consumer 支持本地默认值（找不到 @Provider 时使用）
- @Monitor 是异步触发的，与 @Watch 的同步行为不同
