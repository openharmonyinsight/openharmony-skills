@Component
struct PageA {
  build() {
    Column() {
      Button('A').key('sharedKey')
      Text('A').id('sharedId')
    }
  }
}
