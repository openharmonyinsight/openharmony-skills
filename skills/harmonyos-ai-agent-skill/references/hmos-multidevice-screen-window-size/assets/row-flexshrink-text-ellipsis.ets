/**
 * 案例对照：Row 内文本 + 固定宽度子组件的溢出截断 vs flexShrink 按需压缩
 *
 * 场景：Row 内有一个可变长度昵称文本和一组固定宽度的图标/标签，宽度不足时
 *       预期文本省略、图标完整保留，而非整体被截断到可视区外
 * 根因：缺少 .flexShrink() 显式分配导致 Row 默认的 flex 收缩行为不符合预期，
 *       同时外层 Row 缺少 .width('100%') 导致无宽度约束边界
 *
 * 下面分别是正确案例（goodcase）和错误案例（badcase）
 */

// ==================== 正确案例（goodcase）====================
// 关键点：
//   1. Text 设置 .flexShrink(1) —— 允许文本被压缩
//   2. 内部 Row 设置 .flexShrink(0) —— 阻止图标行被压缩
//   3. 外部 Row 设置 .width('100%') —— 提供宽度约束，触发 flex 收缩计算
// 效果：宽度不足时，nick_name 文本省略号截断，图标和标签完整显示

@Entry
@Component
struct GoodCase {
  @State nick_name: string = "我我我我我说不出口";

  build() {
    RelativeContainer() {
      Row() {
        Text(this.nick_name)
          .fontSize(14)
          .fontFamily('PingFang SC')
          .fontWeight(500)
          .lineHeight(18)
          .fontColor(Color.Black)
          .margin({ left: 8, right: 4 })
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          .flexShrink(1) // 关键：允许此组件被压缩，配合 maxLines + textOverflow 实现省略号
        Row() {
          Image($r('app.media.live_family_medal_icon_night'))
            .width(21)
            .height(18).margin({ right: 4 })
          Image($r("app.media.alpha_ic_new_goods_fans_level_1"))
            .width(23)
            .height(18)
            .margin({ left: 4, right: 20 })
          Text("盒瑞士卷")
            .fontSize(14)
            .fontFamily('PingFang SC')
            .fontWeight(500)
            .lineHeight(18)
        }
        .flexShrink(0) // 关键：阻止此 Row 被压缩，保证图标和标签始终完整
      }
      .width('100%') // 关键：提供宽度约束，flexShrink 才有计算依据
    }
    .clip(true)
    .height('100%')
    .width('50%')
  }
}

// ==================== 错误案例（badcase）====================
// 问题：
//   1. Text 缺少 .flexShrink(1)
//   2. 内部 Row 缺少 .flexShrink(0)
//   3. 外部 Row 缺少 .width('100%')
// 效果：宽度不足时子组件超出父容器可视范围，被截断不可见

@Entry
@Component
struct BadCase {
  @State nick_name: string = "我我我我我说不出口";

  build() {
    RelativeContainer() {
      Row() {
        Text(this.nick_name)
          .fontSize(14)
          .fontFamily('PingFang SC')
          .fontWeight(500)
          .lineHeight(18)
          .fontColor(Color.Black)
          .margin({ left: 8, right: 4 })
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          // 问题：缺少 .flexShrink(1)，文本不会主动让出空间
        Row() {
          Image($r('app.media.live_family_medal_icon_night'))
            .width(21)
            .height(18).margin({ right: 4 })
          Image($r("app.media.alpha_ic_new_goods_fans_level_1"))
            .width(23)
            .height(18)
            .margin({ left: 4, right: 20 })
          Text("盒瑞士卷")
            .fontSize(14)
            .fontFamily('PingFang SC')
            .fontWeight(500)
            .lineHeight(18)
        }
        // 问题：缺少 .flexShrink(0)，图标行可能被意外压缩
      }
      // 问题：缺少 .width('100%')，Row 无宽度约束，flexShrink 无法触发
    }
    .clip(true)
    .height('100%')
    .width('50%')
  }
}
