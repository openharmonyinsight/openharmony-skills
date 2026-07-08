// V2 示例：应用级状态 — @ObservedV2 单例 / AppStorageV2 / PersistenceV2
// 迁移要点：
//   1. LocalStorage → @ObservedV2/@Trace 单例模式（观察能力内嵌到数据，不与 View 耦合）
//   2. AppStorage → AppStorageV2.connect()（跨 Ability 共享）
//   3. PersistentStorage → PersistenceV2.globalConnect()（自动持久化 @Trace 属性）
//   4. @StorageProp 效果（本地修改不同步回源）→ @Local + @Monitor
//   5. $$ → !!

import { AppStorageV2, PersistenceV2, Type } from '@kit.ArkUI'

// ============================================================================
// storage.ets — 定义可观察的单例数据类（替代 LocalStorage + AppStorage）
// ============================================================================

@ObservedV2
export class AppSettings {
  private static instance_: AppSettings

  static instance(): AppSettings {
    if (!AppSettings.instance_) {
      AppSettings.instance_ = new AppSettings()
    }
    return AppSettings.instance_
  }

  @Trace public themeColor: string = '#4CAF50'
  @Trace public fontSize: number = 16
  @Trace public language: string = 'zh-CN'
  @Trace public notifications: boolean = true
  @Trace public launchCount: number = 0
}

// ============================================================================
// EntryAbility.ets — 不再需要手动初始化 PersistentStorage/AppStorage
// ============================================================================

import UIAbility from '@ohos.app.ability.UIAbility'

export default class EntryAbility extends UIAbility {
  onWindowStageCreate(windowStage: window.WindowStage): void {
    // V2 不需要 PersistentStorage.persistProp / AppStorage.setOrCreate
    // 数据通过 @ObservedV2/@Trace 单例 + AppStorageV2/PersistenceV2 自动管理
    const settings = AppSettings.instance()
    settings.launchCount += 1

    windowStage.loadContent('pages/MainPage')
  }
}

// ============================================================================
// MainPage.ets — 主页面，直接引用单例
// ============================================================================

@Entry
@ComponentV2
struct MainPage {
  // 直接引用单例（替代 @LocalStorageProp / @StorageProp 的读取）
  settings: AppSettings = AppSettings.instance()

  // 跨 Ability 共享：AppStorageV2.connect（替代 AppStorage + @StorageLink）
  @Local sharedSettings: AppSettings = AppStorageV2.connect(
    AppSettings, 'appSettings', () => AppSettings.instance()
  )!

  // 持久化读取：PersistenceV2.globalConnect（替代 PersistentStorage + @StorageProp）
  @Local persistentSettings: AppSettings = PersistenceV2.globalConnect({
    type: AppSettings,
    key: 'appSettings',
    defaultCreator: () => AppSettings.instance()
  })!

  @Local username: string = 'Alice'

  // 替代 @StorageProp 效果：本地修改不同步回源
  @Local localThemeColor: string = '#4CAF50'
  @Monitor('settings.themeColor')
  onThemeColorChange(monitor: IMonitor) {
    this.localThemeColor = this.settings.themeColor
  }

  build() {
    Column({ space: 15 }) {
      Text(`Welcome, ${this.username}`)
        .fontSize(this.persistentSettings.fontSize)
        .fontColor(this.localThemeColor)
        .fontWeight(FontWeight.Bold)

      Text(`Launch #${this.sharedSettings.launchCount}`)
        .fontSize(14)
        .fontColor('#888')

      Text(`Language: ${this.persistentSettings.language}`)
        .fontSize(this.persistentSettings.fontSize)

      Text('Main Page')
        .fontSize(20)
        .fontColor(this.sharedSettings.themeColor)

      Button('Open Settings')
        .backgroundColor(this.localThemeColor)
        .onClick(() => {
          // router.pushUrl({ url: 'pages/SettingsPage' })
        })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .padding(20)
  }
}

// ============================================================================
// SettingsPage.ets — 设置页，直接修改单例属性
// ============================================================================

@Entry
@ComponentV2
struct SettingsPage {
  // 直接引用同一个单例实例，修改自动传播到所有引用处
  settings: AppSettings = AppSettings.instance()

  // 持久化连接：修改 @Trace 属性自动持久化到磁盘
  @Local persistentSettings: AppSettings = PersistenceV2.globalConnect({
    type: AppSettings,
    key: 'appSettings',
    defaultCreator: () => AppSettings.instance()
  })!

  build() {
    Scroll() {
      Column({ space: 20 }) {
        Text('Settings')
          .fontSize(24)
          .fontWeight(FontWeight.Bold)
          .fontColor(this.settings.themeColor)

        // --- 替代 LocalStorage：页面级主题色 ---
        // V2 中直接修改单例属性即可，无需 LocalStorage 中间层
        Text('Page Theme (replaces LocalStorage)')
          .fontSize(14)
          .fontColor('#666')
        Row({ space: 10 }) {
          Text('Color:')
            .fontSize(this.settings.fontSize)
          Button('Green')
            .backgroundColor('#4CAF50')
            .onClick(() => { this.settings.themeColor = '#4CAF50' })
          Button('Blue')
            .backgroundColor('#2196F3')
            .onClick(() => { this.settings.themeColor = '#2196F3' })
        }

        // --- 替代 AppStorage：全局主题色 ---
        // 同一个单例实例，所有页面共享，天然跨 Ability
        Text('Global Theme (replaces AppStorage)')
          .fontSize(14)
          .fontColor('#666')
        Row({ space: 10 }) {
          Text('Color:')
            .fontSize(this.settings.fontSize)
          Button('Green')
            .backgroundColor('#4CAF50')
            .onClick(() => { this.settings.themeColor = '#4CAF50' })
          Button('Blue')
            .backgroundColor('#2196F3')
            .onClick(() => { this.settings.themeColor = '#2196F3' })
        }

        // --- 替代 PersistentStorage：持久化设置 ---
        // PersistenceV2 自动持久化 @Trace 属性，无需手动 persistProp
        Text('Persistent Settings (replaces PersistentStorage)')
          .fontSize(14)
          .fontColor('#666')

        Row({ space: 10 }) {
          Text(`Font Size: ${this.settings.fontSize}`)
            .fontSize(this.settings.fontSize)
          Button('-')
            .onClick(() => {
              this.settings.fontSize = Math.max(12, this.settings.fontSize - 2)
            })
          Button('+')
            .onClick(() => {
              this.settings.fontSize = Math.min(32, this.settings.fontSize + 2)
            })
        }

        // !! 替代 $$
        TextInput({ text: this.settings.language!!, placeholder: 'Language' })
          .width('80%')

        Row() {
          Text('Notifications')
            .fontSize(this.settings.fontSize)
          Toggle({ type: ToggleType.Switch, isOn: this.settings.notifications })
            .onChange((isOn: boolean) => {
              this.settings.notifications = isOn
            })
        }
        .width('80%')
        .justifyContent(FlexAlign.SpaceBetween)
      }
      .padding(20)
    }
    .width('100%')
    .height('100%')
  }
}
