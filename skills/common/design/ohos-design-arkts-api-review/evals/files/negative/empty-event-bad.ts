// Eval file for rule: 禁止创建空的公共事件
// 反例1：声明了系统不会发送的公共事件
/**
 * 订阅自定义公共事件
 * @param event 公共事件名称，支持：
 *   - 'MY_CUSTOM_EVENT': 自定义事件
 *   - 'APP_STARTED': 应用启动事件（系统不会发送）
 * @param callback 回调函数
 * @since 8
 */
function subscribe(event: string, callback: Callback<CommonEventData>): void;

// 反例2：创建空的公共事件定义
/**
 * 公共事件数据
 * @since 7
 */
interface CommonEventData {
  /**
   * 事件名称
   */
  event: string;

  /**
   * 事件数据
   */
  data: string;
}

/**
 * 订阅公共事件
 * @param event 事件名称，可以是任意字符串
 * @param callback 回调函数
 * @since 7
 */
function subscribe(event: string, callback: Callback<CommonEventData>): void;

// 反例3：声明了没有实际发送机制的公共事件
/**
 * 公共事件支持列表
 * @since 8
 */
export class CommonEventSupport {
  /**
   * 应用安装完成事件
   * 注意：此事件系统不会发送
   */
  static readonly APP_INSTALLED = 'usual.event.APP_INSTALLED';

  /**
   * 应用卸载完成事件
   * 注意：此事件系统不会发送
   */
  static readonly APP_UNINSTALLED = 'usual.event.APP_UNINSTALLED';

  /**
   * 网络状态变化事件
   * 系统会在网络连接状态变化时发送
   */
  static readonly NETWORK_CHANGED = 'usual.event.NETWORK_CHANGED';
}

// 反例4：在文档中提前定义CES事件但系统不会发送
/**
 * 订阅系统事件
 *
 * 支持以下CommonEventSupport事件：
 * - DEVICE_SHUTDOWN: 设备关机（系统不会发送）
 * - DEVICE_REBOOT: 设备重启（系统不会发送）
 * - TIME_CHANGED: 时间变化
 *
 * @param event 事件名称
 * @param callback 回调函数
 * @since 9
 */
function subscribeCommonEvent(event: string, callback: Callback<void>): void;

// 反例5：声明公共事件但未说明系统是否支持
/**
 * 公共事件管理器
 * @syscap SystemCapability.Notification.CommonEvent
 * @since 7
 */
class CommonEventManager {
  /**
   * 订阅公共事件
   * @param events 事件名称数组，可订阅任意公共事件
   * @param callback 事件回调
   */
  subscribe(events: string[], callback: Callback<CommonEventData>): void;

  /**
   * 取消订阅公共事件
   * @param events 事件名称数组
   */
  unsubscribe(events: string[]): void;
}

// 反例6：文档中声明了事件但实际不支持
/**
 * 用户状态公共事件
 * @syscap SystemCapability.Notification.CommonEvent
 * @since 10
 */
export class UserCommonEvent {
  /**
   * 用户登录事件
   * 当用户成功登录时发送
   */
  static readonly USER_LOGIN = 'user.event.LOGIN';

  /**
   * 用户登出事件
   * 当用户登出时发送
   */
  static readonly USER_LOGOUT = 'user.event.LOGOUT';

  /**
   * 用户切换事件
   * 当用户切换账号时发送（系统不会发送此事件）
   */
  static readonly USER_SWITCH = 'user.event.SWITCH';
}

// 反例7：在API注释中声明了空事件
/**
 * 监听状态变化
 * @param event 状态事件名称
 * @param listener 事件监听器
 *
 * 支持的事件：
 * - 'change': 状态变化事件（空事件，不携带数据）
 */
function on(event: string, listener: () => void): void;
