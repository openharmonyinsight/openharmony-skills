/**
 * 案例对照：Row 容器内标签截断 vs displayPriority 按需展示
 *
 * 场景：一组横向排列的标签，宽度不足时预期按优先级隐藏而非截断
 * 根因：缺少 .displayPriority() 导致子组件被截断，容器缺少 .width('100%') 导致约束不生效
 *
 * 下面分别是正确案例（goodcase）和错误案例（badcase）
 */

// ==================== 正确案例（goodcase）====================
// 关键点：.displayPriority(10 - index) + Row 设置 .width('100%')
// 效果：宽度不足时，靠后的低优先级标签自动隐藏，靠前的完整展示

@Entry
@Component
struct GoodCase {
  @State selectedIndex: number = 0
  private tags: string[] = ['推荐', '科技', '财经', '娱乐', '体育', '教育', '健康', '旅游', '美食', '音乐']

  build() {
    Column() {
      Row({ space: 12 }) {
        ForEach(this.tags, (tag: string, index: number) => {
          Text(tag)
            .displayPriority(10 - index) // 关键：设置显示优先级，值越大越优先显示
            .fontSize(14)
            .fontColor(this.selectedIndex === index ? '#FFFFFF' : '#333333')
            .backgroundColor(this.selectedIndex === index ? '#007DFF' : '#F1F3F5')
            .borderRadius(16)
            .padding({ left: 16, right: 16, top: 8, bottom: 8 })
            .onClick(() => {
              this.selectedIndex = index
            })
        }, (tag: string, index: number) => `${index}_${tag}`)
      }
      .width('100%') // 关键：容器宽度占满，displayPriority 才能正确触发
      .padding({ left: 16, right: 16 })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Start)
    .padding({ top: 20 })
  }
}

// ==================== 错误案例（badcase）====================
// 问题：displayPriority 被注释掉，Row 的 .width('100%') 也被注释掉
// 效果：宽度不足时标签被截断，右侧内容消失在屏幕外

@Entry
@Component
struct BadCase {
  @State selectedIndex: number = 0
  private tags: string[] = ['推荐', '科技', '财经', '娱乐', '体育']

  build() {
    Column() {
      Row({ space: 12 }) {
        ForEach(this.tags, (tag: string, index: number) => {
          Text(tag)
            // .displayPriority(10 - index) // 问题：缺少 displayPriority
            .fontSize(14)
            .fontColor(this.selectedIndex === index ? '#FFFFFF' : '#333333')
            .backgroundColor(this.selectedIndex === index ? '#007DFF' : '#F1F3F5')
            .borderRadius(16)
            .padding({ left: 16, right: 16, top: 8, bottom: 8 })
            .onClick(() => {
              this.selectedIndex = index
            })
        }, (tag: string, index: number) => `${index}_${tag}`)
      }
      // .width('100%') // 问题：缺少容器宽度约束
      .padding({ left: 16, right: 16 })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Start)
    .padding({ top: 20 })
  }
}
