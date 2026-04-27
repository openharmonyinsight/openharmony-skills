/**
 * DisplayApiExample.ets
 *
 * display 模块 API 完整使用示例，涵盖：
 *   1. 三折叠设备双折轴状态检测（TriFoldStateManager）
 *   2. 普通折叠设备状态检测（FoldStateManager）
 *   3. 折叠状态变化监听（FoldStateListener）
 *   4. 折痕区域获取（CreaseRegionManager）
 *   5. 屏幕尺寸与可用区域获取（ScreenSizeManager）
 *
 * 注意：这些示例展示的是独立类的用法，在实际 @Component 中使用时
 * 需在组件生命周期内手动调用 init/destroy 方法管理监听注册与取消。
 */

import { display, Callback } from '@kit.ArkUI';

/**
 * 三折叠设备状态管理
 * 通过 display.getFoldStatus() 的双折轴枚举值判断具体折叠形态。
 * 双折轴相关枚举（如 FOLD_STATUS_EXPANDED_WITH_SECOND_EXPANDED）需要 API 15+。
 */
class TriFoldStateManager {
  getTriFoldStatus(): string {
    let isFoldable = display.isFoldable();
    if (!isFoldable) {
      return 'not_foldable';
    }
    let foldStatus = display.getFoldStatus();
    switch (foldStatus) {
      case display.FoldStatus.FOLD_STATUS_FOLDED:
        return 'folded';
      case display.FoldStatus.FOLD_STATUS_HALF_FOLDED:
        return 'first_axis_half_folded';
      case display.FoldStatus.FOLD_STATUS_EXPANDED:
        return 'expanded';
      case display.FoldStatus.FOLD_STATUS_EXPANDED_WITH_SECOND_EXPANDED:
        return 'both_axes_expanded';
      case display.FoldStatus.FOLD_STATUS_EXPANDED_WITH_SECOND_HALF_FOLDED:
        return 'first_expanded_second_half_folded';
      case display.FoldStatus.FOLD_STATUS_FOLDED_WITH_SECOND_EXPANDED:
        return 'first_folded_second_expanded';
      case display.FoldStatus.FOLD_STATUS_FOLDED_WITH_SECOND_HALF_FOLDED:
        return 'both_axes_folded';
      case display.FoldStatus.FOLD_STATUS_HALF_FOLDED_WITH_SECOND_EXPANDED:
        return 'first_half_folded_second_expanded';
      default:
        return 'unknown';
    }
  }
}

/**
 * 普通折叠设备状态管理
 * 适用于双折叠（单轴）设备，仅使用 FOLDED/HALF_FOLDED/EXPANDED 三种状态。
 */
class FoldStateManager {
  getFoldStatus(): string {
    let isFoldable = display.isFoldable();
    if (!isFoldable) {
      return 'not_foldable';
    }
    let foldStatus = display.getFoldStatus();
    switch (foldStatus) {
      case display.FoldStatus.FOLD_STATUS_FOLDED:
        return 'folded';
      case display.FoldStatus.FOLD_STATUS_HALF_FOLDED:
        return 'half_folded';
      case display.FoldStatus.FOLD_STATUS_EXPANDED:
        return 'expanded';
      default:
        return 'unknown';
    }
  }
}

/**
 * 折叠状态监听器
 * 注意：callback 必须使用对象引用注册，不能用匿名函数，否则无法正确取消导致内存泄漏。
 */
class FoldStateListener {
  private callback: (status: string) => void;
  private foldCallback: Callback<display.FoldStatus> | null = null;

  constructor(callback: (status: string) => void) {
    this.callback = callback;
  }

  startListening(): void {
    this.foldCallback = (status: display.FoldStatus) => {
      let statusStr = '';
      switch (status) {
        case display.FoldStatus.FOLD_STATUS_FOLDED:
          statusStr = 'folded';
          break;
        case display.FoldStatus.FOLD_STATUS_HALF_FOLDED:
          statusStr = 'half_folded';
          break;
        case display.FoldStatus.FOLD_STATUS_EXPANDED:
          statusStr = 'expanded';
          break;
      }
      this.callback(statusStr);
    };
    display.on('foldStatusChange', this.foldCallback);
  }

  stopListening(): void {
    if (this.foldCallback) {
      display.off('foldStatusChange', this.foldCallback);
      this.foldCallback = null;
    }
  }
}

/**
 * 折痕区域管理
 * 通过 init()/destroy() 管理监听生命周期（在 @Component 中对应 aboutToAppear/aboutToDisappear 调用）。
 */
class CreaseRegionManager {
  creaseRegion: display.FoldCreaseRegion | null = null;
  isCreaseVisible: boolean = false;
  private foldCallback: Callback<display.FoldStatus> | null = null;

  init(): void {
    this.getCreaseRegion();
    this.foldCallback = () => {
      this.getCreaseRegion();
    };
    display.on('foldStatusChange', this.foldCallback);
  }

  destroy(): void {
    if (this.foldCallback) {
      display.off('foldStatusChange', this.foldCallback);
      this.foldCallback = null;
    }
  }

  getCreaseRegion(): void {
    let isFoldable = display.isFoldable();
    if (!isFoldable) {
      this.creaseRegion = null;
      return;
    }
    this.creaseRegion = display.getCurrentFoldCreaseRegion();
    this.isCreaseVisible = this.creaseRegion?.creaseRects?.length > 0;
  }
}

interface SizeResult {
  width: number;
  height: number;
}

/**
 * 屏幕尺寸管理
 * getScreenSize() 返回屏幕物理像素宽高。
 * getAvailableArea() 返回扣除系统栏后的可用区域，availableWidth/availableHeight 在 PC/2in1 上有差异。
 */
class ScreenSizeManager {
  getScreenSize(): SizeResult {
    try {
      let displayObj = display.getDefaultDisplaySync();
      return {
        width: displayObj.width,
        height: displayObj.height
      };
    } catch (err) {
      console.error('Failed to get screen size:', JSON.stringify(err));
      return { width: 0, height: 0 };
    }
  }

  /**
   * 获取可用区域（扣除系统工具栏等）
   * availableWidth/availableHeight 在不同设备上含义不同，
   * PC/2in1 上扣除底部工具栏高度，手机/平板上通常与物理宽高一致。
   */
  getAvailableArea(): SizeResult {
    try {
      let displayObj = display.getDefaultDisplaySync();
      return {
        width: displayObj.availableWidth,
        height: displayObj.availableHeight
      };
    } catch (err) {
      console.error('Failed to get available area:', JSON.stringify(err));
      return { width: 0, height: 0 };
    }
  }
}
