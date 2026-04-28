/**
 * HoverStateMinimalExample.ets
 *
 * 极简悬停态示例，演示核心逻辑：
 * - 根据折叠状态 + 显示模式判断是否处于悬停分屏
 * - 竖屏：保持单一全屏布局
 * - 横屏悬停：上半区 / 折痕分隔区 / 下半区 三段结构
 *
 * 关键：悬停判定需同时监听 foldStatusChange 和 foldDisplayModeChange，
 * 因为 HALF_FOLDED 仅表示物理折叠状态，MAIN/SUB/FULL/COORDINATION
 * 显示模式需靠 foldDisplayModeChange 区分。
 */
import display from '@ohos.display';
import { FoldDisplayMode } from '@ohos.display';

@Entry
@Component
struct HoverStateMinimalExample {
  @State isHover: boolean = false;
  @State isHoverLandscape: boolean = false;
  @State hoverTopHeight: number = 0;
  @State hoverCreaseHeight: number = 0;
  private foldStatusCallback: Callback<number> | null = null;
  private foldDisplayModeCallback: Callback<display.FoldDisplayMode> | null = null;

  aboutToAppear() {
    this.updateFoldInfo();
    try {
      this.foldStatusCallback = () => {
        this.updateFoldInfo();
      };
      display.on('foldStatusChange', this.foldStatusCallback);
    } catch (e) {
      console.error('HoverStateMinimalExample register foldStatusChange failed', e);
    }
    try {
      this.foldDisplayModeCallback = () => {
        this.updateFoldInfo();
      };
      display.on('foldDisplayModeChange', this.foldDisplayModeCallback);
    } catch (e) {
      console.error('HoverStateMinimalExample register foldDisplayModeChange failed', e);
    }
  }

  aboutToDisappear() {
    try {
      if (this.foldStatusCallback) {
        display.off('foldStatusChange', this.foldStatusCallback);
        this.foldStatusCallback = null;
      }
    } catch (e) {
      console.error('HoverStateMinimalExample unregister foldStatusChange failed', e);
    }
    try {
      if (this.foldDisplayModeCallback) {
        display.off('foldDisplayModeChange', this.foldDisplayModeCallback);
        this.foldDisplayModeCallback = null;
      }
    } catch (e) {
      console.error('HoverStateMinimalExample unregister foldDisplayModeChange failed', e);
    }
  }

  private updateFoldInfo() {
    let status: number;
    let displayMode: display.FoldDisplayMode;
    try {
      status = display.getFoldStatus();
      displayMode = display.getFoldDisplayMode();
    } catch (e) {
      console.error('HoverStateMinimalExample getFoldStatus/getFoldDisplayMode failed', e);
      this.isHover = false;
      return;
    }

    // 悬停分屏条件：半折叠 + 非 MAIN/SUB 单屏模式
    // HALF_FOLDED 仅表示物理半折叠，MAIN/SUB 单屏模式下不应进入悬停布局
    this.isHover = (status === display.FoldStatus.FOLD_STATUS_HALF_FOLDED) &&
      (displayMode !== display.FoldDisplayMode.FOLD_DISPLAY_MODE_MAIN &&
       displayMode !== display.FoldDisplayMode.FOLD_DISPLAY_MODE_SUB);

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
