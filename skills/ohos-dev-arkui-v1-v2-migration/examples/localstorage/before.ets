// V1 示例：应用级状态 — LocalStorage / AppStorage / PersistentStorage
// 场景：多页面共享应用配置（主题色、字体大小），持久化用户设置
// 文件按真实项目结构拆分展示

// ============================================================================
// EntryAbility.ets — 应用入口，初始化 PersistentStorage + AppStorage
// ============================================================================

import UIAbility from '@ohos.app.ability.UIAbility'

let storage: LocalStorage = LocalStorage.GetShared()

export default class EntryAbility extends UIAbility {
  onWindowStageCreate(windowStage: window.WindowStage): void {
    // PersistentStorage：持久化到磁盘，应用重启后自动恢复
    PersistentStorage.persistProp('fontSize', 16)
    PersistentStorage.persistProp('language', 'zh-CN')
    PersistentStorage.persistProp('notifications', true)

    // AppStorage：全局状态，跨页面、跨 Ability 共享
    AppStorage.setOrCreate('appThemeColor', '#4CAF50')
    AppStorage.setOrCreate('launchCount', 0)

    // LocalStorage：页面级共享，通过 @Entry(localStorage) 注入
    storage.setOrCreate('themeColor', '#4CAF50')

    windowStage.loadContent('pages/MainPage', storage)
  }
}

// ============================================================================
// MainPage.ets — 主页面，演示三种状态源的读取
// ============================================================================

let localStorage = LocalStorage.GetShared()

@Entry(localStorage)
@Component
struct MainPage {
  // LocalStorage — 页面级共享
  @LocalStorageProp('themeColor') localThemeColor: string = '#4CAF50'
  // AppStorage — 全局共享（单向，本地修改不同步回源）
  @StorageProp('appThemeColor') globalThemeColor: string = '#4CAF50'
  @StorageProp('launchCount') launchCount: number = 0
  // PersistentStorage — 持久化的 AppStorage 子集（单向读取）
  @StorageProp('fontSize') fontSize: number = 16
  @StorageProp('language') language: string = 'zh-CN'
  @State username: string = 'Alice'

  aboutToAppear() {
    // 模拟启动计数
    let count = AppStorage.get<number>('launchCount') ?? 0
    AppStorage.setOrCreate('launchCount', count + 1)
  }

  build() {
    Column({ space: 15 }) {
      Text(`Welcome, ${this.username}`)
        .fontSize(this.fontSize)
        .fontColor(this.localThemeColor)
        .fontWeight(FontWeight.Bold)

      Text(`Launch #${this.launchCount}`)
        .fontSize(14)
        .fontColor('#888')

      Text(`Language: ${this.language}`)
        .fontSize(this.fontSize)

      Text('Main Page')
        .fontSize(20)
        .fontColor(this.globalThemeColor)

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
// SettingsPage.ets — 设置页，演示 LocalStorage 双向同步 + AppStorage 双向同步
// ============================================================================

let settingsStorage = LocalStorage.GetShared()

@Entry(settingsStorage)
@Component
struct SettingsPage {
  // LocalStorage 双向同步
  @LocalStorageLink('themeColor') localThemeColor: string = '#4CAF50'
  // AppStorage 双向同步
  @StorageLink('appThemeColor') globalThemeColor: string = '#4CAF50'
  // PersistentStorage 通过 AppStorage 双向同步（修改会自动持久化）
  @StorageLink('fontSize') fontSize: number = 16
  @StorageLink('language') language: string = 'zh-CN'
  @StorageLink('notifications') notifications: boolean = true

  build() {
    Scroll() {
      Column({ space: 20 }) {
        Text('Settings')
          .fontSize(24)
          .fontWeight(FontWeight.Bold)
          .fontColor(this.globalThemeColor)

        // --- LocalStorage：页面级主题色 ---
        Text('Page Theme (LocalStorage)')
          .fontSize(14)
          .fontColor('#666')
        Row({ space: 10 }) {
          Text('Color:')
            .fontSize(this.fontSize)
          Button('Green')
            .backgroundColor('#4CAF50')
            .onClick(() => { this.localThemeColor = '#4CAF50' })
          Button('Blue')
            .backgroundColor('#2196F3')
            .onClick(() => { this.localThemeColor = '#2196F3' })
        }

        // --- AppStorage：全局主题色（跨 Ability） ---
        Text('Global Theme (AppStorage)')
          .fontSize(14)
          .fontColor('#666')
        Row({ space: 10 }) {
          Text('Color:')
            .fontSize(this.fontSize)
          Button('Green')
            .backgroundColor('#4CAF50')
            .onClick(() => { this.globalThemeColor = '#4CAF50' })
          Button('Blue')
            .backgroundColor('#2196F3')
            .onClick(() => { this.globalThemeColor = '#2196F3' })
        }

        // --- PersistentStorage：持久化设置 ---
        Text('Persistent Settings')
          .fontSize(14)
          .fontColor('#666')

        Row({ space: 10 }) {
          Text(`Font Size: ${this.fontSize}`)
            .fontSize(this.fontSize)
          Button('-')
            .onClick(() => { this.fontSize = Math.max(12, this.fontSize - 2) })
          Button('+')
            .onClick(() => { this.fontSize = Math.min(32, this.fontSize + 2) })
        }

        TextInput({ text: $$this.language, placeholder: 'Language' })
          .width('80%')

        Row() {
          Text('Notifications')
            .fontSize(this.fontSize)
          Toggle({ type: ToggleType.Switch, isOn: this.notifications })
            .onChange((isOn: boolean) => {
              this.notifications = isOn
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
