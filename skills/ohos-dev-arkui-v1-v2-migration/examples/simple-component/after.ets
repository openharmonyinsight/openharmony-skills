// V2 示例：简单组件 — @Local / @Param
// 迁移要点：
//   1. @Component → @ComponentV2
//   2. @State → @Local（内部状态）
//   3. @Prop → @Param（父组件传入，只读）

@Entry
@ComponentV2
struct CounterPage {
  @Local count: number = 0
  @Local message: string = 'Hello V2'
  @Local step: number = 1

  build() {
    Column({ space: 10 }) {
      Text(this.message)
        .fontSize(24)
        .fontWeight(FontWeight.Bold)

      Text(`Count: ${this.count}`)
        .fontSize(20)

      // @Param 替代 @Prop，引用传递、只读
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

@ComponentV2
struct CountDisplay {
  @Param currentCount: number = 0
  @Param step: number = 1

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
