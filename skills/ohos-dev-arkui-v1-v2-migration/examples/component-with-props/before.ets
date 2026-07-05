// V1 示例：复杂父子交互 — @Link / @Provide/@Consume / @Watch / $$
// 场景：设置页面，父组件通过 @Provide 共享主题色，
//       子组件通过 @Link 双向同步数据、@Watch 监听变化、$$ 绑定输入框

@Entry
@Component
struct SettingsPage {
  @State username: string = 'Alice'
  @State fontSize: number = 16
  @Provide('themeColor') themeColor: string = '#4CAF50'
  @State showAdvanced: boolean = false

  build() {
    Column({ space: 15 }) {
      Text('Settings')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor(this.themeColor)

      // $$ 双向绑定输入框
      TextInput({ placeholder: 'Username', text: $$this.username })
        .width('80%')
        .fontSize(this.fontSize)

      Text(`Hello, ${this.username}`)
        .fontSize(this.fontSize)

      // @Link 双向同步 fontSize
      FontSizeAdjuster({ size: $fontSize })

      // @Consume 跨层级获取主题色
      ThemeToggle()

      Button(this.showAdvanced ? 'Hide Advanced' : 'Show Advanced')
        .onClick(() => {
          this.showAdvanced = !this.showAdvanced
        })

      if (this.showAdvanced) {
        AdvancedSettings({ username: $username })
      }
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}

@Component
struct FontSizeAdjuster {
  @Link size: number
  @Watch('onSizeChange') private prevSize: number = 0

  onSizeChange() {
    console.info(`FontSize changed to ${this.size}`)
  }

  build() {
    Row({ space: 10 }) {
      Button('-')
        .onClick(() => { this.size = Math.max(12, this.size - 2) })
      Text(`${this.size}`)
        .fontSize(16)
        .width(40)
        .textAlign(TextAlign.Center)
      Button('+')
        .onClick(() => { this.size = Math.min(32, this.size + 2) })
    }
  }
}

@Component
struct ThemeToggle {
  @Consume('themeColor') themeColor: string

  build() {
    Row({ space: 10 }) {
      Text('Theme:')
        .fontSize(16)
      Button('Green')
        .backgroundColor('#4CAF50')
        .onClick(() => { this.themeColor = '#4CAF50' })
      Button('Blue')
        .backgroundColor('#2196F3')
        .onClick(() => { this.themeColor = '#2196F3' })
    }
  }
}

@Component
struct AdvancedSettings {
  @Link username: string

  build() {
    Column({ space: 10 }) {
      Text('Advanced')
        .fontSize(18)
        .fontWeight(FontWeight.Medium)
      TextInput({ placeholder: 'Edit username', text: $$this.username })
        .width('80%')
    }
    .padding(15)
    .borderRadius(10)
    .backgroundColor('#f5f5f5')
  }
}
