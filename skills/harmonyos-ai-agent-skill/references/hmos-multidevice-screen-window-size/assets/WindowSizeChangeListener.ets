/**
 * WindowSizeChangeListener.ets
 * 直接监听窗口精确尺寸变化的工具类
 *
 * 适用场景：需要获取窗口具体宽高值（而非离散断点），如动态计算列数、
 * 按比例调整布局尺寸、根据宽高比切换横竖屏布局等。
 *
 * 与 BreakpointObserver / SystemBreakpointManager 的区别：
 * - 本工具提供精确的 vp 宽高值，不做断点归类
 * - BreakpointObserver / SystemBreakpointManager 提供离散的断点状态
 */

import window from '@ohos.window';

/**
 * 窗口尺寸信息
 */
export interface WindowSizeInfo {
  width: number;  // vp
  height: number; // vp
}

/**
 * 窗口尺寸变化回调类型
 */
export type WindowSizeChangeCallback = (size: WindowSizeInfo) => void;

/**
 * 窗口尺寸监听管理器
 *
 * 使用方式：
 * 1. 在 EntryAbility.onWindowStageCreate 的 loadContent 回调中，
 *    用 windowStage.getMainWindowSync() 获取窗口，调用 init(mainWindow, uiContext)
 * 2. 通过 addListener() 注册尺寸变化回调（init 完成后会立即回调一次初始尺寸）
 * 3. 在页面组件中通过 @StorageProp('windowWidth') / @StorageProp('windowHeight') 响应变化
 * 4. 在 onDestroy 中调用 destroy()
 */
export class WindowSizeManager {
  private windowClass?: window.Window;
  private uiContext?: UIContext;
  private listeners: WindowSizeChangeCallback[] = [];
  private currentSize: WindowSizeInfo = { width: 0, height: 0 };
  private debounceTimer: number = -1;
  private debounceMs: number = 100;
  private isInitialized: boolean = false;

  /**
   * 初始化：直接传入窗口实例，同步完成
   *
   * 必须在 loadContent 回调中调用，此时窗口已完成布局，可正确读取尺寸。
   * 不要在 loadContent 之前调用，否则窗口 rect 可能为 0*0。
   *
   * @param windowClass - 窗口实例，通过 windowStage.getMainWindowSync() 获取
   * @param uiContext - UIContext 实例，用于 px2vp 转换
   * @param debounceMs - 防抖间隔（毫秒），默认 100ms，传 0 禁用防抖
   */
  init(windowClass: window.Window, uiContext: UIContext, debounceMs: number = 100): void {
    if (this.isInitialized) {
      return;
    }

    this.windowClass = windowClass;
    this.uiContext = uiContext;
    this.debounceMs = debounceMs;

    // 读取初始尺寸
    const props = windowClass.getWindowProperties();
    this.currentSize = {
      width: uiContext.px2vp(props.windowRect.width),
      height: uiContext.px2vp(props.windowRect.height),
    };

    // 监听窗口尺寸变化
    windowClass.on('windowSizeChange', (size: window.Size) => {
      this.handleSizeChange(
        uiContext.px2vp(size.width),
        uiContext.px2vp(size.height)
      );
    });

    this.isInitialized = true;

    // 立即通知已注册的 listener 初始尺寸
    this.notifyListeners(this.currentSize.width, this.currentSize.height);
  }

  /**
   * 防抖处理尺寸变化
   */
  private handleSizeChange(width: number, height: number): void {
    if (this.debounceMs <= 0) {
      this.notifyListeners(width, height);
      return;
    }

    if (this.debounceTimer !== -1) {
      clearTimeout(this.debounceTimer);
    }
    this.debounceTimer = setTimeout(() => {
      this.notifyListeners(width, height);
      this.debounceTimer = -1;
    }, this.debounceMs);
  }

  /**
   * 通知监听器并同步 AppStorage
   */
  private notifyListeners(width: number, height: number): void {
    this.currentSize = { width, height };
    AppStorage.setOrCreate('windowWidth', width);
    AppStorage.setOrCreate('windowHeight', height);

    this.listeners.forEach(listener => {
      try {
        listener(this.currentSize);
      } catch (error) {
        console.error('WindowSizeManager listener error:', JSON.stringify(error));
      }
    });
  }

  /**
   * 添加尺寸变化监听器
   */
  addListener(listener: WindowSizeChangeCallback): void {
    this.listeners.push(listener);
  }

  /**
   * 移除监听器
   */
  removeListener(listener: WindowSizeChangeCallback): void {
    const index = this.listeners.indexOf(listener);
    if (index > -1) {
      this.listeners.splice(index, 1);
    }
  }

  /**
   * 获取当前窗口尺寸
   */
  getSize(): WindowSizeInfo {
    return this.currentSize;
  }

  /**
   * 销毁：取消监听并清理资源
   */
  destroy(): void {
    if (this.windowClass) {
      this.windowClass.off('windowSizeChange');
    }
    if (this.debounceTimer !== -1) {
      clearTimeout(this.debounceTimer);
    }
    this.listeners = [];
    this.isInitialized = false;
  }
}

// ──────────────────────────────────────────────────────
// 使用示例（页面组件通过 AppStorage 响应尺寸变化）
// ──────────────────────────────────────────────────────

interface ProductItem {
  id: number;
  name: string;
  price: number;
}

@Entry
@Component
struct WindowSizeExamplePage {
  @StorageProp('windowWidth') windowWidth: number = 0;
  @StorageProp('windowHeight') windowHeight: number = 0;

  private products: ProductItem[] = [
    { id: 1, name: '商品A', price: 99 },
    { id: 2, name: '商品B', price: 199 },
    { id: 3, name: '商品C', price: 299 },
    { id: 4, name: '商品D', price: 399 },
    { id: 5, name: '商品E', price: 499 },
    { id: 6, name: '商品F', price: 599 },
  ];

  private calcColumnCount(width: number): number {
    if (width >= 840) return 4;
    if (width >= 600) return 3;
    return 2;
  }

  build() {
    Column() {
      Text(`窗口尺寸: ${this.windowWidth.toFixed(0)} x ${this.windowHeight.toFixed(0)} vp`)
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 16 })

      Text(`当前列数: ${this.calcColumnCount(this.windowWidth)}`)
        .fontSize(14)
        .fontColor('#666666')
        .margin({ bottom: 16 })

      Flex({ wrap: FlexWrap.Wrap, justifyContent: FlexAlign.Start }) {
        ForEach(this.products, (item: ProductItem) => {
          Column() {
            Text(item.name)
              .fontSize(16)
              .fontWeight(FontWeight.Medium)
            Text(`¥${item.price}`)
              .fontSize(14)
              .fontColor('#FF6600')
              .margin({ top: 4 })
          }
          .width(`${100 / this.calcColumnCount(this.windowWidth) - 2}%`)
          .height(100)
          .margin(4)
          .backgroundColor('#F0F0F0')
          .borderRadius(8)
          .justifyContent(FlexAlign.Center)
          .padding(12)
        })
      }
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .padding(16)
  }
}

// ──────────────────────────────────────────────────────
// EntryAbility 初始化示例（必须在此处初始化）
// ──────────────────────────────────────────────────────
//
// import { WindowSizeManager } from '../common/WindowSizeChangeListener';
//
// let sizeManager: WindowSizeManager = new WindowSizeManager();
//
// export default class EntryAbility extends UIAbility {
//   onWindowStageCreate(windowStage: window.WindowStage): void {
//     windowStage.loadContent('pages/Index', (err) => {
//       if (err) { return; }
//       const mainWindow = windowStage.getMainWindowSync();
//       const uiContext = mainWindow.getUIContext();
//       sizeManager.init(mainWindow, uiContext);
//     });
//   }
//
//   onDestroy(): void {
//     sizeManager.destroy();
//   }
// }
