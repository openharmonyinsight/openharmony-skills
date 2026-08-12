@Component
struct DemoUI {
  build() {
    Column() {
      Text('hello')
        .width(100)
        .height('50px')
      Button('click')
        .width('80vp')
    }
  }
}
