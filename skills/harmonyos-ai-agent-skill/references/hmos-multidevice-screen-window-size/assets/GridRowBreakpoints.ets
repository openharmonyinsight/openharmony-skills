
@Entry
@Component
struct GridRowBreakpoints {
  build() {
    // 示例1: 页面整体布局(推荐使用WindowSize)
    GridRow({
      columns: { sm: 4, md: 8, lg: 12 },
      breakpoints: {
        reference: BreakpointsReference.WindowSize  // 以窗口宽度为参照
      }
    }) {
      GridCol({ span: { sm: 4, md: 4, lg: 3 } }) {
        Text('卡片1').width('100%').height(100).backgroundColor(Color.Pink)
      }
      GridCol({ span: { sm: 4, md: 4, lg: 3 } }) {
        Text('卡片2').width('100%').height(100).backgroundColor('#ADD8E6')
      }
      // ...
    }
    .width('100%')
  }
}
