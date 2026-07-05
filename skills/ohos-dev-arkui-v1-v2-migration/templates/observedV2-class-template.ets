// ============================================================
// @ObservedV2 / @Trace 数据对象模板 — V2 数据层所有模式参考
// ============================================================
// 迁移对照:
//   @Observed  → @ObservedV2  (类级装饰器)
//   @Track     → @Trace       (属性级装饰器)
//   @ObjectLink → 不再需要，V2 深度观测直接访问嵌套属性
// ============================================================

import { AppStorageV2, PersistenceV2, Type } from '@kit.ArkUI';

// ──────────────────────────────────────────────
// 1. 基本数据对象: @Observed + @Track → @ObservedV2 + @Trace
// ──────────────────────────────────────────────

// V1:
// @Observed
// class User {
//   @Track public name: string = '';
//   @Track public age: number = 0;
// }

// V2:
@ObservedV2
class User {
  @Trace public name: string = ''
  @Trace public age: number = 0

  constructor(name: string = '', age: number = 0) {
    this.name = name
    this.age = age
  }
}

// 在 @ComponentV2 中使用:
// @Local user: User = new User('Alice', 30)
// 直接修改即可触发更新: this.user.name = 'Bob'

// ──────────────────────────────────────────────
// 2. 嵌套对象: V2 深度观测，无需子组件分解
// ──────────────────────────────────────────────

// V1 需要为嵌套对象创建子组件 + @ObjectLink 才能观察:
// @Observed class Address { public city: string = ''; }
// @Observed class User { public address: Address = new Address(); }
// → 需要 AddressView(@ObjectLink address: Address) 子组件

// V2 直接深度观测:
@ObservedV2
class Address {
  @Trace public city: string = ''
  @Trace public zipCode: string = ''

  constructor(city: string = '', zipCode: string = '') {
    this.city = city
    this.zipCode = zipCode
  }
}

@ObservedV2
class UserProfile {
  @Trace public name: string = ''
  @Trace public address: Address = new Address()

  constructor(name: string = '', address?: Address) {
    this.name = name
    if (address) this.address = address
  }
}

// 在组件中直接观察嵌套属性:
// @Local profile: UserProfile = new UserProfile('Alice', new Address('NY'))
// this.profile.address.city = 'LA'  ← 直接触发 UI 更新，无需子组件

// ──────────────────────────────────────────────
// 3. 集合类型: Array / Map / Set
// ──────────────────────────────────────────────

@ObservedV2
class CollectionModel {
  @Trace public items: string[] = []
  @Trace public userMap: Map<string, string> = new Map()
  @Trace public tags: Set<string> = new Set()

  addItem(item: string) {
    // V1 需要重新赋值 this.items = [...this.items, item]
    // V2 直接修改即可触发更新
    this.items.push(item)
  }

  removeItem(index: number) {
    this.items.splice(index, 1)
  }
}

// ──────────────────────────────────────────────
// 4. 单例模式: 替代 LocalStorage
// ──────────────────────────────────────────────

// V1:
// const storage = LocalStorage.GetShared()
// storage.setOrCreate('count', 42)

// V2: @ObservedV2 单例类
@ObservedV2
class AppStorage {
  private static instance_: AppStorage

  static instance(): AppStorage {
    if (!AppStorage.instance_) {
      AppStorage.instance_ = new AppStorage()
    }
    return AppStorage.instance_
  }

  @Trace public count: number = 0
  @Trace public theme: string = 'light'

  private constructor() {}
}

// 组件中使用:
// @Local storage: AppStorage = AppStorage.instance()
// this.storage.count++  ← 自动同步到所有引用同一单例的组件

// ──────────────────────────────────────────────
// 5. AppStorageV2: 替代 V1 AppStorage + @StorageLink/@StorageProp
// ──────────────────────────────────────────────

@ObservedV2
class CountStorage {
  @Trace public count: number = 0
}

// 替代 @StorageLink('count') — 双向同步
@Entry
@ComponentV2
struct StorageLinkPage {
  @Local storage: CountStorage = AppStorageV2.connect(
    CountStorage, 'count', () => new CountStorage()
  )!

  build() {
    Column() {
      Text(`${this.storage.count}`)
      Button('+1').onClick(() => this.storage.count++)
    }
  }
}

// 替代 @StorageProp('count') — 单向（本地副本 + @Monitor）
@ComponentV2
struct StoragePropPage {
  @Local localCount: number = 0
  storage: CountStorage = AppStorageV2.connect(
    CountStorage, 'count', () => new CountStorage()
  )!

  @Monitor('storage.count')
  onCountChange(mon: IMonitor) {
    this.localCount = this.storage.count
  }

  build() {
    Text(`${this.localCount}`)
  }
}

// ──────────────────────────────────────────────
// 6. PersistenceV2: 替代 PersistentStorage
// ──────────────────────────────────────────────

@ObservedV2
class AppSettings {
  @Trace public fontSize: number = 16
  @Trace public language: string = 'zh-CN'
  @Trace public notifications: boolean = true
}

@Entry
@ComponentV2
struct SettingsPage {
  @Local settings: AppSettings = PersistenceV2.globalConnect({
    type: AppSettings,
    key: 'appSettings',
    defaultCreator: () => new AppSettings()
  })!

  build() {
    Column() {
      Text(`Font: ${this.settings.fontSize}`)
      Text(`Lang: ${this.settings.language}`)
      Toggle({ type: ToggleType.Switch, isOn: this.settings.notifications!! })
        .onChange((on: boolean) => { this.settings.notifications = on })
    }
  }
}

// ──────────────────────────────────────────────
// 6.1 @Type: 持久化嵌套对象的类型还原
// ──────────────────────────────────────────────
// @Type 仅在 PersistenceV2 / AppStorageV2 反序列化时用于还原"自定义嵌套对象"。
// 框架从磁盘读到的是普通 JSON，无法推断它应属于哪个类，
// 因此需要 @Type(构造器) 显式标注，否则该字段会丢失原型，@Trace/方法失效。
//
// 规则:
//   - 原始类型 (number / string / boolean): 序列化类型天然可推断，禁用 @Type
//   - 内置集合 (Array / Map / Set): 同上，无需 @Type
//   - 自定义嵌套对象 (如 Theme / Address): 必须 @Type(类名) 标注

@ObservedV2
class Theme {
  @Trace public mode: string = 'light'
  @Trace public accentColor: string = '#007DFF'
}

@ObservedV2
class UserPrefs {
  @Trace public userId: string = ''                  // 原始类型 → 不加 @Type
  @Type(Theme) @Trace public theme: Theme = new Theme()  // 嵌套对象 → 必须加 @Type(Theme)
}

@Entry
@ComponentV2
struct UserPrefsPage {
  @Local prefs: UserPrefs = PersistenceV2.globalConnect({
    type: UserPrefs,
    key: 'userPrefs',
    defaultCreator: () => new UserPrefs()
  })!

  build() {
    Column() {
      Text(`User: ${this.prefs.userId}`)
      Text(`Mode: ${this.prefs.theme.mode}`)        // 嵌套属性深度观测，@Type 保证反序列化后仍可触发更新
      Toggle({ type: ToggleType.Switch, isOn: this.prefs.theme.mode === 'dark' })
        .onChange((on: boolean) => {
          this.prefs.theme.mode = on ? 'dark' : 'light'
        })
    }
  }
}
