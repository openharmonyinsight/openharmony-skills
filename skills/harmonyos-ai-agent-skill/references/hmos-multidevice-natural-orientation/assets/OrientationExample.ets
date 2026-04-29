/**
 * OrientationExample.ets
 *
 * 窗口方向设置和运行时动态切换示例。
 * 演示如何结合系统断点 API 和媒体查询实现横竖屏布局切换，
 * 适用于折叠屏等需要在运行时动态响应方向变化的场景。
 *
 * 关键点：
 *   - 使用 windowSizeChange 监听窗口尺寸变化
 *   - 使用 getWindowWidthBreakpoint/getWindowHeightBreakpoint 获取系统断点
 *   - 使用 mediaquery 监听横竖屏状态变化
 *   - 回调必须保存引用以确保 aboutToDisappear 时能正确取消
 */

import { window, mediaquery } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';

@Component
struct LandscapeContent {
  build() {
    Column() {
      Text('横屏内容')
        .fontSize(24)
    }
    .width('100%')
    .height('100%')
  }
}

@Component
struct PortraitContent {
  build() {
    Column() {
      Text('竖屏内容')
        .fontSize(24)
    }
    .width('100%')
    .height('100%')
  }
}

@Entry
@Component
struct FoldableOrientationExample {
  @State widthBreakpoint: WidthBreakpoint = WidthBreakpoint.WIDTH_SM;
  @State heightBreakpoint: HeightBreakpoint = HeightBreakpoint.HEIGHT_LG;
  @State isLandscape: boolean = false;
  private windowClass: window.Window | null = null;
  private mediaListener: mediaquery.MediaQueryListener | null = null;
  private windowSizeCallback: Callback<window.Size> | null = null;

  async aboutToAppear() {
    try {
      let context = this.getUIContext().getHostContext() as common.UIAbilityContext;
      this.windowClass = context.windowStage.getMainWindowSync();

      // 使用保存的引用注册窗口尺寸变化监听
      this.windowSizeCallback = (newSize: window.Size) => {
        this.updateBreakpoints();
      };
      this.windowClass.on('windowSizeChange', this.windowSizeCallback);

      this.mediaListener = this.getUIContext().getMediaQuery().matchMediaSync('(orientation: landscape)');
      this.mediaListener.on('change', (result: mediaquery.MediaQueryResult) => {
        this.isLandscape = result.matches;
      });

      this.updateBreakpoints();
    } catch (err) {
      console.error('Failed to get window:', err);
    }
  }

  aboutToDisappear() {
    if (this.mediaListener) {
      this.mediaListener.off('change');
    }
    if (this.windowSizeCallback && this.windowClass) {
      this.windowClass.off('windowSizeChange', this.windowSizeCallback);
      this.windowSizeCallback = null;
    }
  }

  // 使用系统断点 API，而非手动阈值判断
  private updateBreakpoints() {
    const uiContext = this.getUIContext();
    this.widthBreakpoint = uiContext.getWindowWidthBreakpoint();
    this.heightBreakpoint = uiContext.getWindowHeightBreakpoint();
  }

  build() {
    Column() {
      if (this.isLandscape) {
        LandscapeContent()
      } else {
        PortraitContent()
      }
    }
  }
}
