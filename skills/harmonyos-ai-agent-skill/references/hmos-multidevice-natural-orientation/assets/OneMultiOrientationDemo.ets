/**
 * OneMultiOrientationDemo.ets
 *
 * 端到端一多方向适配示例
 * 演示三层策略的完整接入：
 *   1. module.json5 配置 follow_desktop（默认策略）
 *   2. EntryAbility 全局动态调整（基于断点）
 *   3. 特定页面级覆盖（视频全屏横屏，退出恢复）
 *
 * module.json5 配置:
 * {
 *   "module": {
 *     "abilities": [{
 *       "name": "EntryAbility",
 *       "orientation": "follow_desktop"
 *     }]
 *   }
 * }
 */

// ===================== 第一层：EntryAbility 全局动态调整 =====================

import { window, display } from '@kit.ArkUI';
import { UIAbility, AbilityConstant, common } from '@kit.AbilityKit';

export default class EntryAbility extends UIAbility {
  windowObj?: window.Window;
  uiContext?: UIContext;

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.getMainWindow().then((windowObj) => {
      this.windowObj = windowObj;
    });

    windowStage.loadContent('pages/Index', () => {
      this.uiContext = this.windowObj!.getUIContext();
      this.setDefaultOrientation();
      // 监听窗口尺寸变化，动态调整方向策略
      this.windowObj!.on('windowSizeChange', () => {
        this.setDefaultOrientation();
      });
    });
  }

  /**
   * 全局默认方向策略
   * 窗口最小边 > 348vp 时支持旋转，否则锁定竖屏
   */
  private setDefaultOrientation(): void {
    if (!this.windowObj || !this.uiContext) return;

    const windowRect = this.windowObj.getWindowProperties().windowRect;
    const widthVp = this.uiContext.px2vp(windowRect.width);
    const heightVp = this.uiContext.px2vp(windowRect.height);

    if (Math.min(widthVp, heightVp) > 348) {
      // 大屏/展开态：支持旋转（受控制中心开关控制）
      this.windowObj.setPreferredOrientation(window.Orientation.AUTO_ROTATION_RESTRICTED);
    } else {
      // 小屏/折叠态：锁定竖屏
      this.windowObj.setPreferredOrientation(window.Orientation.PORTRAIT);
    }
  }
}

// ===================== 第二层：首页（使用系统断点判断布局形态） =====================

@Entry
@Component
struct IndexPage {
  @State widthBp: WidthBreakpoint = WidthBreakpoint.WIDTH_SM;
  @State heightBp: HeightBreakpoint = HeightBreakpoint.HEIGHT_LG;
  @State isLandscape: boolean = false;
  private windowClass?: window.Window;
  private sizeCallback: Callback<window.Size> | null = null;

  aboutToAppear(): void {
    const ctx = this.getUIContext()?.getHostContext() as common.UIAbilityContext;
    this.windowClass = ctx.windowStage.getMainWindowSync();

    this.sizeCallback = (size: window.Size) => {
      const uiContext = this.getUIContext();
      const width = uiContext.px2vp(size.width);
      const height = uiContext.px2vp(size.height);
      this.isLandscape = width > height;
      this.widthBp = this.getUIContext().getWindowWidthBreakpoint();
      this.heightBp = this.getUIContext().getWindowHeightBreakpoint();
    };
    this.windowClass.on('windowSizeChange', this.sizeCallback);

    // 初始化断点
    const props = this.windowClass.getWindowProperties();
    this.sizeCallback({ width: props.windowRect.width, height: props.windowRect.height } as window.Size);
  }

  aboutToDisappear(): void {
    if (this.sizeCallback && this.windowClass) {
      this.windowClass.off('windowSizeChange', this.sizeCallback);
      this.sizeCallback = null;
    }
  }

  build() {
    // 根据断点展示不同布局
    if (this.widthBp === WidthBreakpoint.WIDTH_LG) {
      // 大屏横屏布局（平板横屏、三折叠 G/M 态）
      this.largeScreenLayout()
    } else if (this.widthBp === WidthBreakpoint.WIDTH_MD) {
      // 中屏布局（折叠屏展开态、平板竖屏）
      this.mediumScreenLayout()
    } else {
      // 小屏布局（直板机、折叠屏折叠态）
      this.smallScreenLayout()
    }
  }

  @Builder
  smallScreenLayout() {
    Column() {
      Text('小屏模式')
        .fontSize(20)
      // 竖屏列表布局...
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  mediumScreenLayout() {
    Row() {
      Column() {
        Text('导航栏')
          .fontSize(18)
      }
      .width('30%')

      Column() {
        Text('内容区')
          .fontSize(18)
      }
      .width('70%')
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  largeScreenLayout() {
    Row() {
      Column() {
        Text('侧边栏')
          .fontSize(18)
      }
      .width('20%')

      Column() {
        Text('列表')
          .fontSize(18)
      }
      .width('30%')

      Column() {
        Text('详情')
          .fontSize(18)
      }
      .width('50%')
    }
    .width('100%')
    .height('100%')
  }
}

// ===================== 第三层：视频全屏页面级覆盖 =====================

@Component
struct VideoFullScreenPage {
  private context = this.getUIContext()?.getHostContext() as common.UIAbilityContext;
  private windowClass = this.context.windowStage.getMainWindowSync();
  private lastOrientation: number = window.Orientation.PORTRAIT;
  @State isLandscape: boolean = false;
  @State videoWidth: number = 0;
  @State videoHeight: number = 0;
  private sizeCallback: Callback<window.Size> | null = null;

  aboutToAppear(): void {
    // 保存当前方向
    this.lastOrientation = this.windowClass.getPreferredOrientation();

    this.sizeCallback = (size: window.Size) => {
      const uiContext = this.getUIContext();
      const width = uiContext.px2vp(size.width);
      const height = uiContext.px2vp(size.height);
      this.isLandscape = width > height;

      if (this.isLandscape) {
        this.videoWidth = width;
        this.videoHeight = height;
        this.windowClass.setSpecificSystemBarEnabled('navigationIndicator', false);
      } else {
        this.videoWidth = width;
        this.videoHeight = width * 9 / 16; // 16:9 比例
        this.windowClass.setSpecificSystemBarEnabled('navigationIndicator', true);
      }
    };
    this.windowClass.on('windowSizeChange', this.sizeCallback);
  }

  aboutToDisappear(): void {
    // 先取消监听，再恢复方向，避免恢复过程中触发回调
    if (this.sizeCallback) {
      this.windowClass.off('windowSizeChange', this.sizeCallback);
      this.sizeCallback = null;
    }
    // 恢复之前保存的方向
    this.windowClass.setPreferredOrientation(this.lastOrientation);
  }

  build() {
    Stack() {
      // 视频播放区域
      Column() {
        Text('视频播放区')
          .fontSize(24)
          .fontColor(Color.White)
      }
      .width(this.videoWidth)
      .height(this.videoHeight)
      .backgroundColor(Color.Black)

      // 全屏/退出按钮
      Row() {
        if (!this.isLandscape) {
          Button('全屏播放')
            .onClick(() => {
              this.windowClass.setPreferredOrientation(window.Orientation.USER_ROTATION_LANDSCAPE);
            })
        } else {
          Button('退出全屏')
            .onClick(() => {
              this.windowClass.setPreferredOrientation(window.Orientation.USER_ROTATION_PORTRAIT);
            })
        }
      }
      .position({ x: 10, y: 10 })
    }
    .width('100%')
    .height('100%')
  }
}
