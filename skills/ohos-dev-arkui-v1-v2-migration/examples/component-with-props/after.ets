// V2 示例：复杂父子交互 — @Param+@Event / @Provider/@Consumer / @Monitor / !!
// 迁移要点：
//   1. @Link → @Param + @Event（手动回调实现双向同步）
//   2. @Provide/@Consume → @Provider/@Consumer（V2需加括号，alias为匹配键）
//   3. @Watch → @Monitor（异步，支持多变量，提供 before/after）
//   4. $$ → !!（语法替换）
//   5. @Provider 禁止外部初始化

@Entry
@ComponentV2
struct SettingsPage {
  @Local username: string = 'Alice'
  @Local fontSize: number = 16
  @Provider('themeColor') themeColor: string = '#4CAF50'
  @Local showAdvanced: boolean = false

  build() {
    Column({ space: 15 }) {
      Text('Settings')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor(this.themeColor)

      // !! 替代 $$ 双向绑定
      TextInput({ placeholder: 'Username', text: this.username!! })
        .width('80%')
        .fontSize(this.fontSize)

      Text(`Hello, ${this.username}`)
        .fontSize(this.fontSize)

      // @Param + @Event 替代 @Link
      FontSizeAdjuster({
        size: this.fontSize,
        onSizeChange: (newSize: number) => { this.fontSize = newSize }
      })

      // @Consumer 跨层级获取主题色
      ThemeToggle()

      Button(this.showAdvanced ? 'Hide Advanced' : 'Show Advanced')
        .onClick(() => {
          this.showAdvanced = !this.showAdvanced
        })

      if (this.showAdvanced) {
        AdvancedSettings({
          username: this.username,
          onUsernameChange: (val: string) => { this.username = val }
        })
      }
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}

@ComponentV2
struct FontSizeAdjuster {
  @Param size: number = 16
  @Event onSizeChange: (newSize: number) => void = () => {}
  @Local prevSize: number = 0

  // @Monitor 替代 @Watch，支持 before/after
  @Monitor('size')
  onSizeChangeMonitor(monitor: IMonitor) {
    monitor.dirty.forEach((name: string) => {
      const before = monitor.value(name)?.before;
      const now = monitor.value(name)?.now;
      console.info(`FontSize changed: ${before} → ${now}`);
    });
  }

  build() {
    Row({ space: 10 }) {
      Button('-')
        .onClick(() => { this.onSizeChange(Math.max(12, this.size - 2)) })
      Text(`${this.size}`)
        .fontSize(16)
        .width(40)
        .textAlign(TextAlign.Center)
      Button('+')
        .onClick(() => { this.onSizeChange(Math.min(32, this.size + 2)) })
    }
  }
}

@ComponentV2
struct ThemeToggle {
  // @Consumer 替代 @Consume，支持本地默认值
  @Consumer('themeColor') themeColor: string = '#4CAF50'

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

@ComponentV2
struct AdvancedSettings {
  @Param username: string = ''
  @Event onUsernameChange: (val: string) => void = () => {}

  build() {
    Column({ space: 10 }) {
      Text('Advanced')
        .fontSize(18)
        .fontWeight(FontWeight.Medium)
      TextInput({ placeholder: 'Edit username', text: this.username!! })
        .width('80%')
        .onChange((value: string) => {
          this.onUsernameChange(value)
        })
    }
    .padding(15)
    .borderRadius(10)
    .backgroundColor('#f5f5f5')
  }
}
