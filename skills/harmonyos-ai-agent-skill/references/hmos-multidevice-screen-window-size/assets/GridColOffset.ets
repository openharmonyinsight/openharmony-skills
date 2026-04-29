
@Entry
@Component
struct GridColOffset {
  build() {
    Column() {
      GridRow({ columns: 12 }) {
        // 第一个元素: 占4列,无偏移
        GridCol({ span: 4, offset: 0 }) {
          Text('元素1').backgroundColor(Color.Pink).width('100%')
        }

        // 第二个元素: 占4列,偏移2列
        GridCol({ span: 4, offset: 2 }) {
          Text('元素2').backgroundColor('#87CEEB').width('100%')
        }

        // 第三个元素: 占4列,无偏移
        GridCol({ span: 4, offset: 0 }) {
          Text('元素3').backgroundColor(Color.Orange).width('100%')
        }
      }
      .width('100%')
      .height(100)

      // 响应式offset
      GridRow({ columns: 12 }) {
        GridCol({
          span: { sm: 6, md: 4, lg: 3 },
          offset: { sm: 0, md: 2, lg: 1 }  // 不同断点下的偏移
        }) {
          Text('响应式偏移').backgroundColor(Color.Green).width('100%')
        }
      }
      .width('100%')
      .height(50)
    }
  }
}
