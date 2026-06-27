// Eval file for rule: 在描述中列出API的使用限制、特殊写法和单位
// 正例1：API有使用限制，在NOTE中列出
/**
 * 获取设备信息
 * NOTE:
 * - 此API仅可在主线程调用
 * - 需要ohos.permission.GET_DEVICE_INFO权限
 * - 系统版本要求：API 9及以上
 * @returns 设备信息对象
 */
function getDeviceInfo(): DeviceInfo {
  return deviceInfo;
}

// 正例2：API有调用频率限制，在NOTE中列出
/**
 * 上报用户行为数据
 * NOTE:
 * - 调用频率限制：每分钟最多调用60次
 * - 数据大小限制：单次上报数据不超过1MB
 * @param data 行为数据
 */
function reportUserData(data: UserData): void {
  // implementation
}

// 正例3：API有特殊写法说明，在NOTE中列出
/**
 * 解析时间字符串
 * NOTE:
 * - 时间格式必须为"YYYY-MM-DD HH:mm:ss"
 * - 月份范围：01-12，日期范围：01-31
 * - 小时范围：00-23，分钟范围：00-59，秒范围：00-59
 * @param timeStr 时间字符串
 * @returns 时间戳（ms）
 */
function parseTime(timeStr: string): number {
  return Date.parse(timeStr);
}

// 正例4：常量定义包含单位说明
使用符号代替汉字
/**
 * 默认超时时间，单位：ms
 */
const DEFAULT_TIMEOUT = 5000;

/**
 * 屏幕宽度，单位：vp
 */
const SCREEN_WIDTH = 1080;

/**
 * 音量最大值，单位：db
 */
const MAX_VOLUME = 100;

// 正例5：属性定义包含单位说明
class AnimationConfig {
  /**
   * 动画持续时间，单位：ms
   */
  duration: number = 300;

  /**
   * 延迟执行时间，单位：ms
   */
  delay: number = 0;

  /**
   * 旋转角度，单位：deg
   */
  rotation: number = 0;
}


// 正例6：函数参数包含单位说明
/**
 * 设置定时器
 * @param interval 间隔时间，单位：ms
 * @param callback 回调函数
 */
function setInterval(interval: number, callback: () => void): void {
  // implementation
}

/**
 * 设置音量
 * @param volume 音量值，单位：db，范围：0-100
 */
function setVolume(volume: number): void {
  // implementation
}

/**
 * 移动视图
 * @param x X轴偏移量，单位：vp
 * @param y Y轴偏移量，单位：vp
 */
function moveView(x: number, y: number): void {
  // implementation
}

// 正例7：多个使用限制，在NOTE中以列表形式给出
/**
 * 下载文件
 * NOTE:
 * - 仅支持HTTP/HTTPS协议
 * - 文件大小限制：不超过100MB
 * - 并发下载数限制：最多同时下载3个文件
 * - 需要ohos.permission.INTERNET权限
 * @param url 下载URL
 * @param savePath 保存路径
 */
function downloadFile(url: string, savePath: string): void {
  // implementation
}

// 正例8：特殊写法说明包含多种格式要求
/**
 * 设置颜色值
 * NOTE:
 * - 支持格式：#RRGGBB、#AARRGGBB、rgb(r,g,b)、rgba(r,g,b,a)
 * - RGB值范围：0-255
 * - Alpha值范围：0.0-1.0
 * @param color 颜色值字符串
 */
function setColor(color: string): void {
  // implementation
}
