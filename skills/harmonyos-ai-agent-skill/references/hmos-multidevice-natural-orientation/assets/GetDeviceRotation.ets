/**
 * GetDeviceRotation.ets
 *
 * 获取设备屏幕旋转角度的示例代码。
 * display.rotation 返回 0/1/2/3，分别对应 0°/90°/180°/270°。
 *
 * 注意：rotation 的含义与设备自然方向有关：
 *   - 自然竖屏设备（直板机/平板）：rotation=0 → PORTRAIT
 *   - 自然横屏设备（PC/2in1）：rotation=0 → LANDSCAPE
 *   - 三折叠 G 态：rotation=0 → LANDSCAPE_INVERTED
 */

import { display } from '@kit.ArkUI';

function getDeviceRotation(): number {
  try {
    const defaultDisplay = display.getDefaultDisplaySync();
    return defaultDisplay.rotation * 90;
  } catch (err) {
    console.error('Failed to get device rotation:', JSON.stringify(err));
    return 0;
  }
}
