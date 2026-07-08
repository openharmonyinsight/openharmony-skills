# 应用级状态迁移：LocalStorage / AppStorage / PersistentStorage

## 涵盖的迁移点

| V1 | V2 | 说明 |
|----|-----|------|
| LocalStorage + @LocalStorageLink | @ObservedV2/@Trace 单例 | 观察能力内嵌到数据，不与 View 耦合 |
| LocalStorage + @LocalStorageProp | @Local + @Monitor | 本地修改不同步回源 |
| AppStorage + @StorageLink / @StorageProp | AppStorageV2.connect() | 跨 Ability 共享 |
| PersistentStorage.persistProp() | PersistenceV2.globalConnect() | 自动持久化 @Trace 属性 |
| EntryAbility 中手动初始化 | @Trace 属性自动管理 | 不再需要 persistProp / setOrCreate |
| $$ | !! | 绑定语法替换 |

## 文件说明

- `before.ets` — V1 完整示例：
  - EntryAbility 中初始化 PersistentStorage + AppStorage
  - MainPage 使用 @LocalStorageProp + @StorageProp 读取（单向）
  - SettingsPage 使用 @LocalStorageLink + @StorageLink 双向同步（含持久化）
- `after.ets` — V2 等价实现：
  - @ObservedV2/@Trace 单例替代 LocalStorage 中间层
  - AppStorageV2.connect() 替代 AppStorage
  - PersistenceV2.globalConnect() 替代 PersistentStorage
  - EntryAbility 无需手动初始化

## 迁移注意

- V2 的数据观察能力内嵌到数据类本身，不再需要 View 层的中间容器
- @LocalStorageProp 效果（本地修改不同步回源）用 @Local + @Monitor 实现
- AppStorageV2.connect() 返回值可能为 null，需用 `!` 断言
- PersistenceV2 自动持久化 @Trace 属性，从 PersistentStorage 迁移时需编写一次性数据迁移函数
- V1 中 PersistentStorage 本质上是 AppStorage 的持久化子集，V2 中 PersistenceV2 独立运作，不再与 AppStorageV2 耦合
