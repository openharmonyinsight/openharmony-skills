// Eval file for rule: 禁止创建空的公共事件
// 正例1：正确声明系统会发送的公共事件
/**
 * 订阅屏幕解锁事件
 * @param event 屏幕解锁事件，值为 'unlock'
 * @param callback 回调函数，接收解锁事件数据
 * @throws {BusinessError} 参数错误时抛出异常
 * @syscap SystemCapability.WindowManager.WindowManager
 * @since 7
 */
function on(event: 'unlock', callback: Callback<void>): void;

// 正例2：正确声明多个系统支持的公共事件
/**
 * 订阅系统公共事件
 * @param event 公共事件名称，支持以下事件：
 *   - 'BOOT_COMPLETED': 系统启动完成事件
 *   - 'BATTERY_CHANGED': 电池状态变化事件
 *   - 'SCREEN_ON': 屏幕点亮事件
 * @param callback 回调函数
 * @syscap SystemCapability.Notification.CommonEvent
 * @since 8
 */
function subscribe(event: string, callback: Callback<CommonEventData>): void;

// 正例3：明确标注系统支持的事件类型
/**
 * 公共事件数据
 * @syscap SystemCapability.Notification.CommonEvent
 * @since 7
 */
interface CommonEventData {
  /**
   * 事件名称，系统支持的事件包括：
   * - COMMON_EVENT_BOOT_COMPLETED: 系统启动完成
   * - COMMON_EVENT_BATTERY_CHANGED: 电池状态变化
   * - COMMON_EVENT_SCREEN_ON: 屏幕点亮
   * - COMMON_EVENT_SCREEN_OFF: 屏幕熄灭
   */
  event: string;

  /**
   * 事件数据
   */
  data: string;

  /**
   * 事件代码
   */
  code: number;
}

// 正例4：声明实际可用的公共事件常量
/**
 * 公共事件常量定义
 * @syscap SystemCapability.Notification.CommonEvent
 * @since 8
 */
export class CommonEventSupport {
  /**
   * 系统启动完成事件
   * 系统启动完成后会发送此事件
   */
  static readonly BOOT_COMPLETED = 'usual.event.BOOT_COMPLETED';

  /**
   * 电池状态变化事件
   * 电池电量或充电状态变化时发送
   */
  static readonly BATTERY_CHANGED = 'usual.event.BATTERY_CHANGED';

  /**
   * 屏幕点亮事件
   * 屏幕从熄灭状态变为点亮时发送
   */
  static readonly SCREEN_ON = 'usual.event.SCREEN_ON';
}

// 正例5：文档中清晰说明事件的发送条件
/**
 * 订阅用户解锁设备事件
 *
 * 此事件在用户成功解锁设备后发送。
 * 注意：设备启动后首次解锁不会触发此事件，
 * 需要使用BOOT_COMPLETED事件代替。
 *
 * @param callback 解锁事件回调
 * @syscap SystemCapability.WindowManager.WindowManager
 * @since 9
 */
function onUserUnlocked(callback: Callback<void>): void;
