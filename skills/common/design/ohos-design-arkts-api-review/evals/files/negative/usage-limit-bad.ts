// Eval file for rule: 在描述中列出API的使用限制、特殊写法和单位

// 反例1：API有特殊写法要求但未说明
/**
 * 解析时间字符串
 * @param timeStr 时间字符串
 * @returns 时间戳
 */
function parseTime(timeStr: string): number {
  return Date.parse(timeStr);
}

// 反例2：常量定义缺少单位说明
/**
 * 默认超时时间
 */
const DEFAULT_TIMEOUT = 5000;

/**
 * 屏幕宽度
 */
const SCREEN_WIDTH = 1080;

/**
 * 音量最大值
 */
const MAX_VOLUME = 100;

// 反例3：属性定义缺少单位说明
class AnimationConfig {
  /**
   * 动画持续时间
   */
  duration: number = 300;

  /**
   * 延迟执行时间
   */
  delay: number = 0;

  /**
   * 旋转角度
   */
  rotation: number = 0;
}

// 反例4：函数参数缺少单位说明
/**
 * 设置定时器
 * @param interval 间隔时间
 * @param callback 回调函数
 */
function setInterval(interval: number, callback: () => void): void {
  // implementation
}

/**
 * 设置音量
 * @param volume 音量值
 */
function setVolume(volume: number): void {
  // implementation
}

// 反例5：使用限制说明不完整
/**
 * 下载文件
 * NOTE:
 * - 仅支持HTTP/HTTPS协议
 * @param url 下载URL
 * @param savePath 保存路径
 */
function downloadFile(url: string, savePath: string): void {
  // implementation
}

// 反例6：单位说明使用汉字而非符号
/**
 * 默认超时时间，单位：毫秒
 */
const DEFAULT_TIMEOUT = 5000;

/**
 * 屏幕宽度，单位：像素
 */
const SCREEN_WIDTH = 1080;

// 反例7：有数据大小限制但未说明
/**
 * 上传文件
 * @param filePath 文件路径
 */
function uploadFile(filePath: string): void {
  // implementation
}
