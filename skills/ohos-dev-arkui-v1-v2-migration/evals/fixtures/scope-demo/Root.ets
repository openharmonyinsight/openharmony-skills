// Fixture for scope/storage workflow evals. Minimal, intentionally synthetic.
// Root: 提供者 —— @Provide pageStack、user，并 @StorageLink 消费 'theme' key。
class User {
  name: string = '';
}

@Component
export struct Root {
  @Provide('pageStack') pageStack: NavPathStack = new NavPathStack();
  @Provide('user') user: User = new User();
  @StorageLink('theme') theme: string = 'light';

  build() {
    Column() {
      Text('root')
    }
  }
}
