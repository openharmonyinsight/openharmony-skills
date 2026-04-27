
import { mediaquery } from '@kit.ArkUI';

/**
 * 媒体查询管理器
 * 注意：需要在组件内部使用，因为需要使用getUIContext()
 */
export class MediaQueryManager {
  private uiContext: UIContext | null = null;
  private listeners: Map<string, mediaquery.MediaQueryListener> = new Map();
  private callbacks: Map<string, (matches: boolean) => void> = new Map();

  /**
   * 设置UIContext（必须在组件中调用）
   */
  setUIContext(uiContext: UIContext) {
    this.uiContext = uiContext;
  }

  /**
   * 注册媒体查询
   * @param key 唯一标识
   * @param condition 查询条件
   * @param callback 回调函数
   */
  register(key: string, condition: string, callback: (matches: boolean) => void) {
    if (!this.uiContext) {
      console.error('MediaQueryManager: UIContext未设置，请先调用setUIContext()');
      return;
    }
    // ✅ 推荐：使用UIContext.getMediaQuery()新API
    const listener = this.uiContext.getMediaQuery().matchMediaSync(condition);
    
    // 保存监听器和回调
    this.listeners.set(key, listener);
    this.callbacks.set(key, callback);

    // 立即执行一次回调(初始化状态)
    callback(listener.matches);

    // 注册变化回调
    listener.on('change', (result) => {
      callback(result.matches);
    });
  }

  /**
   * 注销媒体查询
   * @param key 唯一标识
   */
  unregister(key: string) {
    const listener = this.listeners.get(key);
    if (listener) {
      listener.off('change');
      this.listeners.delete(key);
      this.callbacks.delete(key);
    }
  }

  /**
   * 注销所有媒体查询
   */
  unregisterAll() {
    this.listeners.forEach((listener) => {
      listener.off('change');
    });
    this.listeners.clear();
    this.callbacks.clear();
  }

  /**
   * 获取当前匹配状态
   * @param key 唯一标识
   */
  getMatches(key: string): boolean {
    const listener = this.listeners.get(key);
    return listener ? listener.matches : false;
  }
}

// 使用示例
@Entry
@Component
struct MediaQueryManagerExample {
  private mqManager: MediaQueryManager = new MediaQueryManager();
  @State isWideScreen: boolean = false;
  @State isPortrait: boolean = true;

  aboutToAppear() {
    // ✅ 必须先设置UIContext
    this.mqManager.setUIContext(this.getUIContext());
    
    // 注册宽屏监听
    this.mqManager.register('wideScreen', '(min-width: 600vp)', (matches) => {
      this.isWideScreen = matches;
    });

    // 注册竖屏监听
    this.mqManager.register('portrait', '(orientation: portrait)', (matches) => {
      this.isPortrait = matches;
    });
  }

  aboutToDisappear() {
    // 注销所有监听
    this.mqManager.unregisterAll();
  }

  build() {
    Column() {
      Text(`宽屏: ${this.isWideScreen}`)
      Text(`竖屏: ${this.isPortrait}`)
    }
  }
}
