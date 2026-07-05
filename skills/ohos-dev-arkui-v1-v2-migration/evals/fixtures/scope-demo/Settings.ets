// Settings: @Consume pageStack（与 Root 耦合）+ @StorageLink('theme')（与 Root 共享 storage key）。
@Component
export struct Settings {
  @Consume('pageStack') pageStack: NavPathStack;
  @StorageLink('theme') theme: string = 'light';

  build() {
    Text(`theme: ${this.theme}`)
  }
}
