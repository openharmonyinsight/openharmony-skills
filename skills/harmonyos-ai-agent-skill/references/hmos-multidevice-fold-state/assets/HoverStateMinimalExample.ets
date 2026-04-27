/**
 * HoverStateMinimalExample.ets
 *
 * 极简悬停态示例，演示核心逻辑：
 * - 根据折叠状态 + 方向判断是否处于横屏悬停
 * - 竖屏：保持单一全屏布局
 * - 横屏悬停：上半区 / 折痕分隔区 / 下半区 三段结构
 */
import display from '@ohos.display';

@Entry
@Component
struct HoverStateMinimalExample {
  @State isHover: boolean = false;
  @State isHoverLandscape: boolean = false;
  @State hoverTopHeight: number = 0;
  @State hoverCreaseHeight: number = 0;

  aboutToAppear() {
    this.updateFoldInfo();
    try {
      display.on('foldStatusChange', () => {
        this.updateFoldInfo();
      });
    } catch (e) {
      console.error('HoverStateMinimalExample register foldStatusChange failed', e);
    }
  }

  aboutToDisappear() {
    try {
      display.off('foldStatusChange');
    } catch (e) {
      console.error('HoverStateMinimalExample unregister foldStatusChange failed', e);
    }
  }

  private updateFoldInfo() {
    let status: number;
    try {
      status = display.getFoldStatus();
    } catch (e) {
      console.error('HoverStateMinimalExample getFoldStatus failed', e);
      this.isHover = false;
      return;
    }

    this.isHover = (status === display.FoldStatus.FOLD_STATUS_HALF_FOLDED);

    if (!this.isHover) {
      this.isHoverLandscape = false;
      this.hoverTopHeight = 0;
      this.hoverCreaseHeight = 0;
      return;
    }

    try {
      const disp = display.getDefaultDisplaySync();
      const density = disp.densityPixels;
      const regions = display.getCurrentFoldCreaseRegion();
      const orientation = disp.orientation;

      this.isHoverLandscape = (orientation === 1 || orientation === 3);

      if (regions && regions.creaseRects && regions.creaseRects.length > 0) {
        const rect = regions.creaseRects[0];
        this.hoverTopHeight = rect.top / density;
        this.hoverCreaseHeight = rect.height / density;
      } else {
        this.hoverTopHeight = (disp.height / density) / 2 - 10;
        this.hoverCreaseHeight = 20;
      }
    } catch (e) {
      console.error('HoverStateMinimalExample updateFoldInfo failed', e);
      this.isHoverLandscape = false;
      this.hoverTopHeight = 0;
      this.hoverCreaseHeight = 0;
    }
  }

  build() {
    Column() {
      if (!this.isHover || !this.isHoverLandscape) {
        // 非悬停或竖屏：保持单一全屏布局
        Column() {
          Text('Normal / portrait or non-hover layout')
            .fontSize(18)
            .textAlign(TextAlign.Center)
        }
        .width('100%')
        .height('100%')
        .backgroundColor('#F5F5F5')
      } else {
        // 横屏悬停：上半区 + 折痕分隔区 + 下半区
        Column() {
          // 上半区
          Column() {
            Text('Top area (content)')
              .fontSize(18)
              .textAlign(TextAlign.Center)
          }
          .width('100%')
          .height(Math.max(0, this.hoverTopHeight - 24))
          .backgroundColor('#FFFFFF')
          .clip(true)

          // 折痕分隔区
          Row() {
            Text('Crease avoidance area')
              .fontSize(14)
              .fontColor(Color.White)
          }
          .width('100%')
          .height(this.hoverCreaseHeight)
          .backgroundColor('rgba(100, 149, 237, 0.7)')
          .justifyContent(FlexAlign.Center)

          // 下半区
          Column() {
            Text('Bottom area (for controls / IME space)')
              .fontSize(16)
              .textAlign(TextAlign.Center)
          }
          .width('100%')
          .layoutWeight(1)
          .backgroundColor('#F1F3F5')
        }
        .width('100%')
        .height('100%')
      }
    }
    .width('100%')
    .height('100%')
  }
}
