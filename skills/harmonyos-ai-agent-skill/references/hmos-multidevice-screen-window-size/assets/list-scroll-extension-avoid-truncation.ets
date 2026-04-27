/**
 * 案例对照：使用 List 延伸组件避免小屏幕内容截断
 *
 * 场景：应用列表横向排列，在悬浮窗等小屏幕场景下，宽度不足以容纳所有内容
 * 预期：内容可以横向滚动查看，而不是被截断
 * 根因：Row 容器不具备滚动能力，超出宽度的内容会被截断；List 容器具备滚动延伸能力
 *
 * 下面分别是正确案例（goodcase）和错误案例（badcase）
 */

// ==================== 正确案例（goodcase）====================
// 关键点：使用 List + ListItem 替代 Row + ForEach，启用滚动能力
// 效果：小屏幕下可以左右滑动查看所有应用，不会被截断

@Entry
@Component
struct GoodCase {
  private appList: number [] = [0, 1, 2, 3];

  build() {
    Row() {
      // 关键：使用 List 容器，具备滚动和延伸能力
      List({ space: 10 }) {
        ForEach(this.appList, () => {
          ListItem() {  // 关键：子组件必须用 ListItem 包裹
            Column() {
              Image($r('app.media.startIcon'))
                .width(48)
                .height(48)
                .margin({ top: 8 });
              Text('appName')
                .width(64)
                .height(30)
                .lineHeight(15)
                .fontSize(12)
                .textAlign(TextAlign.Center)
                .margin({ top: 8 })
                .padding({ bottom: 15 });
            }
            .width(80)
            .height(102);
          }
          .width(80)
          .height(102);
        }, (item: number, index: number) => JSON.stringify(item) + index);
      }
      .padding({ top: 16, left: 10 })
      .listDirection(Axis.Horizontal)  // 关键：设置为横向滚动
      .width('100%')
      .height(118)
      .borderRadius(16)
      .backgroundColor(Color.White);
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(VerticalAlign.Center);
  }
}

// ==================== 错误案例（badcase）====================
// 问题：使用 Row 容器 + ForEach，不具备滚动能力
// 效果：小屏幕下超出宽度的内容被截断，无法查看

@Entry
@Component
struct BadCase {
  private appList: number [] = [0, 1, 2, 3];

  build() {
    Row() {
      // 问题：Row 容器不具备滚动能力
      Row({ space: 10 }) {
        ForEach(this.appList, () => {
          // 问题：直接使用 Column，没有被可滚动容器包裹
          Column() {
            Image($r('app.media.startIcon'))
              .width(48)
              .height(48)
              .margin({ top: 8 });
            Text('appName')
              .width(64)
              .height(30)
              .lineHeight(15)
              .fontSize(12)
              .textAlign(TextAlign.Center)
              .margin({ top: 8 })
              .padding({ bottom: 15 });
          }
          .width(80)
          .height(102);
        }, (item: number, index: number) => JSON.stringify(item) + index);
      }
      .width('60%');  // 问题：固定宽度，超出内容被截断
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(VerticalAlign.Center);
  }
}

// ==================== 关键差异总结 ====================
// 1. 容器类型：List（可滚动）vs Row（不可滚动）
// 2. 子组件包裹：ListItem vs 直接使用 Column
// 3. 滚动配置：.listDirection(Axis.Horizontal) 明确指定横向滚动
// 4. 延伸能力：List 会延伸内容到可视区域外，用户可滑动查看；Row 会截断超出部分
