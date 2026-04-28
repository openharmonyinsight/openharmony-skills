/**
 * BreakpointObserver.ets
 * 断点观察者 - 统一监听窗口尺寸变化并更新断点状态
 */

import window from '@ohos.window';
import {
  BreakpointConstants,
  getBreakpointByWidth,
  getVerticalBreakpoint
} from './BreakpointConstants';

export type BreakpointChangeListener = (breakpoint: string, verticalBreakpoint: string) => void;

export class BreakpointObserver {
  private static instance: BreakpointObserver;
  private windowClass?: window.Window;
  private currentBreakpoint: string = BreakpointConstants.BREAKPOINT_SM;
  private currentVerticalBreakpoint: string = BreakpointConstants.VERTICAL_LG;
  private listeners: BreakpointChangeListener[] = [];
  private isInitialized: boolean = false;
  private windowSizeChangeCallback?: (size: window.Size) => void;

  private constructor() {}

  static getInstance(): BreakpointObserver {
    if (!BreakpointObserver.instance) {
      BreakpointObserver.instance = new BreakpointObserver();
    }
    return BreakpointObserver.instance;
  }

  /**
   * 初始化断点观察者
   * @param context 应用上下文
   */
  async init(context: Context): Promise<void> {
    if (this.isInitialized) {
      return;
    }

    try {
      this.windowClass = await window.getLastWindow(context);

      // 获取初始窗口尺寸
      const properties = this.windowClass.getWindowProperties();
      const width = px2vp(properties.windowRect.width);
      const height = px2vp(properties.windowRect.height);

      // 初始化断点
      this.updateBreakpoint(width, height);

      this.windowSizeChangeCallback = (size: window.Size) => {
        const newWidth = px2vp(size.width);
        const newHeight = px2vp(size.height);
        this.updateBreakpoint(newWidth, newHeight);
      };

      // 监听窗口尺寸变化
      this.windowClass.on('windowSizeChange', this.windowSizeChangeCallback);

      this.isInitialized = true;
    } catch (error) {
      console.error('BreakpointObserver init failed:', error);
    }
  }

  /**
   * 更新断点状态
   */
  private updateBreakpoint(width: number, height: number): void {
    const newBreakpoint = getBreakpointByWidth(width);
    const newVerticalBreakpoint = getVerticalBreakpoint(width, height);

    const breakpointChanged = this.currentBreakpoint !== newBreakpoint;
    const verticalChanged = this.currentVerticalBreakpoint !== newVerticalBreakpoint;

    if (breakpointChanged || verticalChanged) {
      this.currentBreakpoint = newBreakpoint;
      this.currentVerticalBreakpoint = newVerticalBreakpoint;

      // 更新 AppStorage
      AppStorage.setOrCreate(BreakpointConstants.CURRENT_BREAKPOINT, newBreakpoint);
      AppStorage.setOrCreate(BreakpointConstants.CURRENT_VERTICAL_BREAKPOINT, newVerticalBreakpoint);
      AppStorage.setOrCreate(BreakpointConstants.WINDOW_WIDTH, width);
      AppStorage.setOrCreate(BreakpointConstants.WINDOW_HEIGHT, height);

      // 通知监听器
      this.notifyListeners(newBreakpoint, newVerticalBreakpoint);
    }
  }

  /**
   * 添加断点变化监听器
   */
  addListener(listener: BreakpointChangeListener): void {
    this.listeners.push(listener);
  }

  /**
   * 移除断点变化监听器
   */
  removeListener(listener: BreakpointChangeListener): void {
    const index = this.listeners.indexOf(listener);
    if (index > -1) {
      this.listeners.splice(index, 1);
    }
  }

  /**
   * 通知所有监听器
   */
  private notifyListeners(breakpoint: string, verticalBreakpoint: string): void {
    this.listeners.forEach(listener => {
      try {
        listener(breakpoint, verticalBreakpoint);
      } catch (error) {
        console.error('BreakpointObserver listener error:', error);
      }
    });
  }

  /**
   * 获取当前断点
   */
  getCurrentBreakpoint(): string {
    return this.currentBreakpoint;
  }

  /**
   * 获取当前纵向断点
   */
  getCurrentVerticalBreakpoint(): string {
    return this.currentVerticalBreakpoint;
  }

  /**
   * 是否为小屏设备
   */
  isSmallScreen(): boolean {
    return this.currentBreakpoint === BreakpointConstants.BREAKPOINT_SM ||
           this.currentBreakpoint === BreakpointConstants.BREAKPOINT_XS;
  }

  /**
   * 是否为中等屏幕
   */
  isMediumScreen(): boolean {
    return this.currentBreakpoint === BreakpointConstants.BREAKPOINT_MD;
  }

  /**
   * 是否为大屏设备
   */
  isLargeScreen(): boolean {
    return this.currentBreakpoint === BreakpointConstants.BREAKPOINT_LG ||
           this.currentBreakpoint === BreakpointConstants.BREAKPOINT_XL;
  }

  /**
   * 是否为横向窗口
   */
  isLandscapeWindow(): boolean {
    return this.currentVerticalBreakpoint === BreakpointConstants.VERTICAL_SM;
  }

  /**
   * 销毁观察者
   */
  destroy(): void {
    if (this.windowClass && this.windowSizeChangeCallback) {
      this.windowClass.off('windowSizeChange', this.windowSizeChangeCallback);
    }
    this.listeners = [];
    this.isInitialized = false;
  }
}
