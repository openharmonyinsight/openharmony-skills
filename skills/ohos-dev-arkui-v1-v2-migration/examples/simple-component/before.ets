// V1 示例：简单组件 — @State / @Prop / @Watch
// 场景：计数器父组件 + 显示子组件，演示基础状态管理和父子传值

@Entry
@Component
struct CounterPage {
  @State count: number = 0
  @State message: string = 'Hello V1'
  @State step: number = 1

  build() {
    Column({ space: 10 }) {
      Text(this.message)
        .fontSize(24)
        .fontWeight(FontWeight.Bold)

      Text(`Count: ${this.count}`)
        .fontSize(20)

      // 简单类型 @Prop 传递
      CountDisplay({ currentCount: this.count, step: this.step })

      Row({ space: 10 }) {
        Button('Reset')
          .onClick(() => {
            this.count = 0
          })

        Button(`+${this.step}`)
          .onClick(() => {
            this.count += this.step
          })
      }
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }
}

@Component
struct CountDisplay {
  @Prop currentCount: number = 0
  @Prop step: number = 1

  build() {
    Column({ space: 5 }) {
      Text(`Current: ${this.currentCount}`)
        .fontSize(18)
      Text(`Step: ${this.step}`)
        .fontSize(14)
        .fontColor('#888')
    }
    .padding(10)
    .borderRadius(8)
    .backgroundColor('#f0f0f0')
  }
}
