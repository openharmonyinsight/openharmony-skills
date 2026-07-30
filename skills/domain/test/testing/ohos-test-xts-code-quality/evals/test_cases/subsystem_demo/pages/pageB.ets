@Component
struct PageB {
  build() {
    Column() {
      Button('B').key('sharedKey')
      Text('B').id('sharedId')
    }
  }
}
