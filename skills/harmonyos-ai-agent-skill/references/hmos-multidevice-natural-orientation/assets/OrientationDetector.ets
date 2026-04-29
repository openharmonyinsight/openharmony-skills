/**
 * OrientationDetector.ets
 *
 * 统一方向检测封装（单例），基于 display.on('change') + windowSizeChange 监听
 * 实现方向变化感知、自然方向判定和方向控制。
 *
 * 核心能力：
 *   - 自动检测设备自然方向（通过折叠状态+宽高比判断）
 *   - 监听屏幕/窗口变化，实时更新方向信息
 *   - 提供横竖屏锁定/解锁接口
 *
 * 设计决策：优先使用 display/window 监听而非传感器，符合官方最佳实践。
 * 仅当需要连续角度做动画等场景时，才需额外接入传感器（参考 rotation_detection.md）。
 */

import { display, window } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';

export type DeviceOrientation = 'portrait' | 'landscape' | 'portrait_inverted' | 'landscape_inverted';
export type NaturalOrientation = 'portrait' | 'landscape';

export interface OrientationInfo {
  orientation: DeviceOrientation;
  rotation: number; // 0, 90, 180, 270
  isLandscape: boolean;
  naturalOrientation: NaturalOrientation;
}

export class OrientationDetector {
  private static instance: OrientationDetector;
  private windowClass?: window.Window;
  private currentInfo: OrientationInfo = {
    orientation: 'portrait',
    rotation: 0,
    isLandscape: false,
    naturalOrientation: 'portrait'
  };
  private listeners: ((info: OrientationInfo) => void)[] = [];
  private initialized: boolean = false;
  // 保存回调引用，确保 off 时只移除自身的监听
  private displayChangeCallback: Callback<number> | null = null;
  private windowSizeChangeCallback: Callback<window.Size> | null = null;

  private constructor() {}

  static getInstance(): OrientationDetector {
    if (!OrientationDetector.instance) {
      OrientationDetector.instance = new OrientationDetector();
    }
    return OrientationDetector.instance;
  }

  /**
   * 初始化方向检测器
   * @param context UIAbilityContext，用于获取窗口实例
   */
  async init(context: Context): Promise<void> {
    if (this.initialized) {
      return;
    }
    this.windowClass = (context as common.UIAbilityContext).windowStage.getMainWindowSync();
    this.updateOrientationInfo();

    // 使用保存的引用注册监听，确保 destroy 时只移除自身的监听
    this.displayChangeCallback = () => {
      this.updateOrientationInfo();
    };
    display.on('change', this.displayChangeCallback);

    this.windowSizeChangeCallback = () => {
      this.updateOrientationInfo();
    };
    this.windowClass.on('windowSizeChange', this.windowSizeChangeCallback);

    this.initialized = true;
  }

  /**
   * 更新方向信息
   */
  private updateOrientationInfo(): void {
    const displayInfo = display.getDefaultDisplaySync();
    // 通过窗口实例获取 UIContext 进行 px2vp 转换
    const uiContext = this.windowClass?.getUIContext();
    if (!uiContext) return;
    const width = uiContext.px2vp(displayInfo.width);
    const height = uiContext.px2vp(displayInfo.height);

    // 判断自然方向（基于设备类型或窗口比例）
    const naturalOrientation = this.detectNaturalOrientation(width, height);

    // 计算当前方向
    const orientation = this.calculateOrientation(
      displayInfo.rotation,
      naturalOrientation
    );

    const newInfo: OrientationInfo = {
      orientation,
      rotation: displayInfo.rotation * 90,
      isLandscape: width > height,
      naturalOrientation
    };

    // 检查是否有变化（逐字段比较，避免 JSON.stringify 性能开销）
    if (this.currentInfo.orientation !== newInfo.orientation ||
      this.currentInfo.rotation !== newInfo.rotation ||
      this.currentInfo.isLandscape !== newInfo.isLandscape ||
      this.currentInfo.naturalOrientation !== newInfo.naturalOrientation) {
      this.currentInfo = newInfo;
      this.notifyListeners(newInfo);
    }
  }

  /**
   * 检测设备自然方向
   * 优先通过折叠状态判断三折叠 G 态，再通过宽高比辅助判断
   */
  private detectNaturalOrientation(width: number, height: number): NaturalOrientation {
    // 通过折叠状态判断三折叠 G 态（展开双轴 → 自然横屏）
    if (display.isFoldable()) {
      const foldStatus = display.getFoldStatus();
      if (foldStatus === display.FoldStatus.FOLD_STATUS_EXPANDED_WITH_SECOND_EXPANDED) {
        return 'landscape';
      }
    }

    // 通过宽高比判断：宽明显大于高时为自然横屏设备
    if (width > height * 1.2) {
      return 'landscape';
    }

    // 其他设备默认自然方向是竖屏
    return 'portrait';
  }

  /**
   * 根据旋转角度和自然方向计算当前方向
   */
  private calculateOrientation(
    rotation: number,
    naturalOrientation: NaturalOrientation
  ): DeviceOrientation {
    if (naturalOrientation === 'portrait') {
      // 自然竖屏设备
      switch (rotation) {
        case 0: return 'portrait';
        case 1: return 'landscape';
        case 2: return 'portrait_inverted';
        case 3: return 'landscape_inverted';
        default: return 'portrait';
      }
    } else {
      // 自然横屏设备（如三折叠G态）
      // 三折叠G态的 rotation=0 对应 LANDSCAPE_INVERTED
      switch (rotation) {
        case 0: return 'landscape_inverted';
        case 1: return 'landscape';
        case 2: return 'portrait';
        case 3: return 'portrait_inverted';
        default: return 'landscape';
      }
    }
  }

  /**
   * 获取当前方向信息
   */
  getCurrentInfo(): OrientationInfo {
    return { ...this.currentInfo };
  }

  /**
   * 是否为横屏
   */
  isLandscape(): boolean {
    return this.currentInfo.isLandscape;
  }

  /**
   * 是否为自然横屏设备
   */
  isNaturalLandscapeDevice(): boolean {
    return this.currentInfo.naturalOrientation === 'landscape';
  }

  /**
   * 添加方向变化监听器
   */
  addListener(listener: (info: OrientationInfo) => void): void {
    this.listeners.push(listener);
  }

  /**
   * 移除方向变化监听器
   */
  removeListener(listener: (info: OrientationInfo) => void): void {
    const index = this.listeners.indexOf(listener);
    if (index > -1) {
      this.listeners.splice(index, 1);
    }
  }

  /**
   * 通知监听器
   */
  private notifyListeners(info: OrientationInfo): void {
    this.listeners.forEach(listener => {
      try {
        listener(info);
      } catch (error) {
        console.error('OrientationDetector listener error:', error);
      }
    });
  }

  /**
   * 设置窗口方向
   */
  async setOrientation(orientation: window.Orientation): Promise<void> {
    if (this.windowClass) {
      await this.windowClass.setPreferredOrientation(orientation);
    }
  }

  /**
   * 锁定竖屏
   */
  async lockPortrait(): Promise<void> {
    await this.setOrientation(window.Orientation.PORTRAIT);
  }

  /**
   * 锁定横屏
   */
  async lockLandscape(): Promise<void> {
    await this.setOrientation(window.Orientation.LANDSCAPE);
  }

  /**
   * 允许自动旋转
   */
  async unlockOrientation(): Promise<void> {
    await this.setOrientation(window.Orientation.AUTO_ROTATION);
  }

  /**
   * 销毁，只移除自身注册的监听
   */
  destroy(): void {
    if (this.displayChangeCallback) {
      display.off('change', this.displayChangeCallback);
      this.displayChangeCallback = null;
    }
    if (this.windowSizeChangeCallback && this.windowClass) {
      this.windowClass.off('windowSizeChange', this.windowSizeChangeCallback);
      this.windowSizeChangeCallback = null;
    }
    this.listeners = [];
    this.initialized = false;
  }
}
