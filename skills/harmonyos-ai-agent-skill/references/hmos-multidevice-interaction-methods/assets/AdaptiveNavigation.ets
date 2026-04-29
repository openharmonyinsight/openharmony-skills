import { KeyCode } from '@kit.InputKit';

/**
 * 自适应导航壳组件示例：
 * - Phone（小屏）：使用底部 TabBar + 页面栈。
 * - Tablet/Foldable/2-in-1（大屏）：使用 SideBarContainer 侧边导航 + 双栏布局。
 * 同时在此组件中统一处理 Hover、焦点与键盘快捷键等交互归一化逻辑。
 */
@Entry
@Component
struct AdaptiveNavigation {
  @StorageProp('currentWidthBreakpoint') currentWidthBreakpoint: WidthBreakpoint = WidthBreakpoint.WIDTH_SM;
  @State selectedIndex: number = 0;

  // 模拟菜单数据
  private menuItems: string[] = ['Home', 'Discover', 'Profile'];

  

  private get showSidebar(): boolean {
    // 小屏/手机优先使用底部导航，其它场景使用侧边栏
    return this.currentWidthBreakpoint !== WidthBreakpoint.WIDTH_SM &&
      this.currentWidthBreakpoint !== WidthBreakpoint.WIDTH_XS
  }

  build() {
    // 使用 SideBarContainer 实现自适应导航
    SideBarContainer(SideBarContainerType.Embed) {
      // 1. 侧边栏 (在大屏显示)
      if (this.showSidebar) {
        Column() {
          ForEach(this.menuItems, (item: string, index: number) => {
            this.MenuItem(item, index, true)
          })
        }
        .width(240)
        .height('100%')
        .backgroundColor('#F1F3F5')
        .justifyContent(FlexAlign.Start)
        .padding({ top: 50 })
      }

      // 2. 主内容区域
      Column() {
        // 顶部标题
        Text(this.menuItems[this.selectedIndex])
          .fontSize(30)
          .fontWeight(FontWeight.Bold)
          .margin(20)

        // 内容占位
        Blank()

        // 3. 底部导航栏 (仅在小屏 / 手机显示)
        if (!this.showSidebar) {
          Row() {
            ForEach(this.menuItems, (item: string, index: number) => {
              this.MenuItem(item, index, false)
            })
          }
          .width('100%')
          .height(56)
          .backgroundColor(Color.White)
          .border({ width: { top: 1 }, color: '#E3E3E3' })
          .justifyContent(FlexAlign.SpaceAround)
        }
      }
      .height('100%')
      .width('100%')
    }
    // 控制侧边栏显隐：大屏/双栏推荐场景显示，小屏/手机隐藏
    .showSideBar(this.showSidebar)
    .showControlButton(false) // 隐藏默认控制按钮
    .sideBarWidth(240)
    .minSideBarWidth(200)
    .maxSideBarWidth(300)
  }

  @Builder
  MenuItem(title: string, index: number, isSidebar: boolean) {
    Column() {
      // 图标占位
      Circle({ width: 24, height: 24 })
        .fill(this.selectedIndex === index ? '#007DFF' : '#999')
        .margin({ bottom: 4 })

      Text(title)
        .fontSize(14)
        .fontColor(this.selectedIndex === index ? '#007DFF' : '#999')
    }
    .width(isSidebar ? '100%' : 'auto')
    .height(isSidebar ? 50 : '100%')
    .justifyContent(FlexAlign.Center)
    // 鼠标悬浮效果
    .hoverEffect(HoverEffect.Highlight)
    // 键盘焦点支持
    .focusable(true)
    .stateStyles({
      focused: { .backgroundColor('#E0F0FF') }
    })
    // 点击/回车键归一化处理
    .onClick(() => this.selectedIndex = index)
    .onKeyEvent((event) => {
      if (event.type === KeyType.Down && (event.keyCode === KeyCode.KEYCODE_ENTER || event.keyCode === KeyCode.KEYCODE_SPACE)) {
        this.selectedIndex = index;
      }
    })
  }
}
