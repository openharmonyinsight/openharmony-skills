/**
 * HoverStateUtil.ets
 *
 * 悬停状态工具函数
 * - 检测折叠状态和屏幕方向
 * - 计算折痕位置和尺寸
 * - 统一维护 AppStorage 状态
 */
import display from '@ohos.display';
import { window } from '@kit.ArkUI';

/**
 * 更新折叠屏悬停状态到 AppStorage
 *
 * 调用时机：
 * 1. 页面 aboutToAppear 时
 * 2. display.on('foldStatusChange') 触发时
 * 3. window.on('windowSizeChange') 触发时（屏幕旋转）
 */
export function updateFoldStatusFromDisplay(): void {
  let status: number;
  try {
    status = display.getFoldStatus();
  } catch (e) {
    console.error('HoverStateUtil: getFoldStatus failed', e);
    AppStorage.setOrCreate('isHover', false);
    AppStorage.setOrCreate('isHoverLandscape', false);
    AppStorage.setOrCreate('hoverTopHeight', 0);
    AppStorage.setOrCreate('hoverCreaseHeight', 0);
    return;
  }

  let isHover = false;
  let topHeight = 0;
  let creaseHeight = 0;
  let isHoverLandscape = false;

  if (status === display.FoldStatus.FOLD_STATUS_HALF_FOLDED) {
    isHover = true;
    try {
      const disp = display.getDefaultDisplaySync();
      const density = disp.densityPixels;
      const regions = display.getCurrentFoldCreaseRegion();

      if (regions && regions.creaseRects && regions.creaseRects.length > 0) {
        const rect = regions.creaseRects[0];
        topHeight = rect.top / density;
        creaseHeight = rect.height / density;
      } else {
        // 无法获取折痕区域时使用默认值
        topHeight = (disp.height / density) / 2 - 10;
        creaseHeight = 20;
      }

      const orientation = disp.orientation;
      // 1: LANDSCAPE, 3: LANDSCAPE_INVERTED
      isHoverLandscape = (orientation === 1 || orientation === 3);
    } catch (e) {
      console.error('HoverStateUtil: get crease/orientation failed', e);
      topHeight = 300;
      creaseHeight = 24;
    }
  }

  AppStorage.setOrCreate('isHover', isHover);
  AppStorage.setOrCreate('hoverTopHeight', topHeight);
  AppStorage.setOrCreate('hoverCreaseHeight', creaseHeight);
  AppStorage.setOrCreate('isHoverLandscape', isHoverLandscape);
  // 可选通用标记：上层可按需监听此标记触发布局重算。
  AppStorage.setOrCreate('hoverLayoutDirty', true);
}

/**
 * 初始化悬停状态监听
 * 在 EntryAbility.onWindowStageCreate 中调用
 */
export function initHoverStateListener(windowStage: window.WindowStage): void {
  try {
    const mainWin = windowStage.getMainWindowSync();
    mainWin.on('windowSizeChange', () => {
      updateFoldStatusFromDisplay();
    });
  } catch (e) {
    console.error('HoverStateUtil: Failed to register windowSizeChange', e);
  }
}
