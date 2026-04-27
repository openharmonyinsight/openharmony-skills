import { display } from '@kit.ArkUI';

/**
 * 注意：
 * - 本文件为官方 API 工程模板集合，用于状态读取、监听和折痕数据接线示例。
 * - 方案基线请先参考：
 *   1) ../references/fold_status_detection.md
 *   2) ../references/multi_fold_states.md
 */

class MultiFoldStateManager {
  async getMultiFoldStatus(): Promise<string> {
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

class FoldStateManager {
  async getFoldStatus(): Promise<string> {
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

class FoldStateListener {
  constructor(callback: (status: string) => void) {
    this.callback = callback;
  }

  private callback: (status: string) => void;

  startListening(): void {
    display.on('foldStatusChange', (status) => {
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
    });
  }
}

class CreaseRegionManager {
  creaseRegion: display.FoldCreaseRegion | null = null;
  isCreaseVisible: boolean = false;

  aboutToAppear() {
    this.getCreaseRegion();
    display.on('foldStatusChange', () => {
      this.getCreaseRegion();
    });
  }

  getCreaseRegion() {
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

interface AreaResult {
  width: number;
  height: number;
}

class ScreenSizeManager {
  getScreenSize(): SizeResult {
    let displayObj = display.getDefaultDisplaySync();
    return {
      width: displayObj.width,
      height: displayObj.height
    };
  }

  getAvailableArea(): AreaResult {
    let displayObj = display.getDefaultDisplaySync();
    return {
      width: displayObj.availableWidth,
      height: displayObj.availableHeight
    };
  }
}
