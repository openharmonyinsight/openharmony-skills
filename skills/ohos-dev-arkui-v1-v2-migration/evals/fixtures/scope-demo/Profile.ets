// Profile: @Consume pageStack、user —— 与 Root 通过 @Provide/@Consume 耦合（联合迁移判定用）。
@Component
export struct Profile {
  @Consume('pageStack') pageStack: NavPathStack;
  @Consume('user') user: User;

  build() {
    Text(`name: ${this.user.name}`)
  }
}
