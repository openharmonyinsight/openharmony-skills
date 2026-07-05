// Badge: 叶子组件 —— 仅 @State/@Prop，无 @Provide/@Consume/@StorageLink 耦合（独立迁移判定用）。
@Component
export struct Badge {
  @State count: number = 0;
  @Prop label: string;

  build() {
    Text(`${this.label}: ${this.count}`)
  }
}
