/**
 * 相机硬件适配工具类
 * 
 * 功能：
 * 1. 相机设备选择（根据窗口尺寸和折叠状态）
 * 2. 预览流旋转角度计算
 * 3. 拍照旋转角度计算
 * 4. 相机位置判断（前置/后置）
 * 
 * 使用场景：
 * - 多设备相机适配
 * - 折叠屏相机适配
 * - 三折叠相机适配
 * - Pura X阔折叠相机适配
 */

import { camera } from '@kit.CameraKit';
import display from '@ohos.display';
import window from '@ohos.window';
import { common } from '@kit.AbilityKit';

interface WindowSize {
  width: number;
  height: number;
}

/**
 * 相机适配器类
 */
export class CameraAdapter {
  private context: common.UIAbilityContext | null = null;
  private windowClass: window.Window | null = null;

  constructor(context: common.UIAbilityContext) {
    this.context = context;
    this.windowClass = context.windowStage?.getMainWindowSync() || null;
  }

  /**
   * 获取当前窗口尺寸
   */
  private getWindowSize(): WindowSize {
    if (!this.windowClass) {
      return { width: 0, height: 0 };
    }
    const windowProperties = this.windowClass.getWindowProperties();
    return {
      width: windowProperties.windowRect.width,
      height: windowProperties.windowRect.height
    };
  }

  /**
   * 获取屏幕旋转角度
   */
  private getScreenRotation(): number {
    try {
      const displayClass = display.getDefaultDisplaySync();
      return displayClass.rotation;
    } catch (e) {
      console.error('获取屏幕旋转角度失败:', e);
      return 0;
    }
  }

  /**
   * 判断是否为折叠屏设备
   */
  private isFoldableDevice(): boolean {
    try {
      return display.isFoldable();
    } catch (e) {
      return false;
    }
  }

  /**
   * 获取折叠状态
   */
  private getFoldStatus(): display.FoldStatus {
    try {
      return display.getFoldStatus();
    } catch (e) {
      return display.FoldStatus.FOLD_STATUS_UNKNOWN;
    }
  }

  /**
   * 根据窗口尺寸和折叠状态选择相机
   * 
   * @param preferredPosition 首选相机位置（前置或后置）
   * @returns 可用的相机设备信息，如果不可用则返回null
   */
  async selectCamera(preferredPosition: camera.CameraPosition = camera.CameraPosition.CAMERA_POSITION_BACK): Promise<camera.CameraDevice | null> {
    try {
      const cameraManager = camera.getCameraManager(this.context!);
      const cameras = await cameraManager.getSupportedCameras();
      
      if (cameras.length === 0) {
        console.warn('没有可用的相机设备');
        return null;
      }

      if (this.isFoldableDevice()) {
        return this.selectCameraForFoldable(cameras, preferredPosition);
      }

      const preferredCamera = cameras.find((cam: camera.CameraDevice) => cam.cameraPosition === preferredPosition);
      if (preferredCamera) {
        return preferredCamera;
      }

      return cameras[0];
    } catch (e) {
      console.error('选择相机失败:', e);
      return null;
    }
  }

  /**
   * 为折叠屏设备选择相机
   */
  private async selectCameraForFoldable(
    cameras: camera.CameraDevice[],
    preferredPosition: camera.CameraPosition
  ): Promise<camera.CameraDevice | null> {
    const foldStatus = this.getFoldStatus();
    const windowSize = this.getWindowSize();

    if (windowSize.width <= 350 && windowSize.height <= 350) {
      const frontCamera = cameras.find((cam: camera.CameraDevice) => cam.cameraPosition === camera.CameraPosition.CAMERA_POSITION_FRONT);
      if (frontCamera) {
        return frontCamera;
      }
    }

    if (foldStatus === display.FoldStatus.FOLD_STATUS_FOLDED) {
      const frontCamera = cameras.find((cam: camera.CameraDevice) => cam.cameraPosition === camera.CameraPosition.CAMERA_POSITION_FRONT);
      if (frontCamera) {
        return frontCamera;
      }
    } else if (foldStatus === display.FoldStatus.FOLD_STATUS_EXPANDED) {
      const backCamera = cameras.find((cam: camera.CameraDevice) => cam.cameraPosition === camera.CameraPosition.CAMERA_POSITION_BACK);
      if (backCamera) {
        return backCamera;
      }
    }

    const preferredCamera = cameras.find((cam: camera.CameraDevice) => cam.cameraPosition === preferredPosition);
    if (preferredCamera) {
      return preferredCamera;
    }

    return cameras[0];
  }

  /**
   * 计算预览流旋转角度
   * 
   * @param cameraDevice 相机设备
   * @returns 预览流旋转角度（0, 90, 180, 270）
   */
  calculatePreviewRotation(cameraDevice: camera.CameraDevice): number {
    const rotation = this.getScreenRotation();
    const lensFacing = cameraDevice.cameraPosition;
    
    let lensOrientation = 90;
    if (lensFacing === camera.CameraPosition.CAMERA_POSITION_FRONT) {
      lensOrientation = 270;
    }

    const previewRotation = (lensOrientation + rotation * 90) % 360;
    
    return previewRotation;
  }

  /**
   * 计算拍照旋转角度
   * 
   * @param cameraDevice 相机设备
   * @returns 拍照旋转角度（0, 90, 180, 270）
   */
  calculateCaptureRotation(cameraDevice: camera.CameraDevice): number {
    return this.calculatePreviewRotation(cameraDevice);
  }

  /**
   * 获取相机镜头角度
   * 
   * @param cameraDevice 相机设备
   * @returns 镜头安装角度（0, 90, 180, 270）
   */
  getLensOrientation(cameraDevice: camera.CameraDevice): number {
    if (cameraDevice.cameraPosition === camera.CameraPosition.CAMERA_POSITION_BACK) {
      return 90;
    } else {
      return 270;
    }
  }

  /**
   * 判断相机是否可用
   * 
   * @param cameraDevice 相机设备
   * @returns 是否可用
   */
  async isCameraAvailable(cameraDevice: camera.CameraDevice): Promise<boolean> {
    try {
      const cameraManager = camera.getCameraManager(this.context!);
      const cameras = await cameraManager.getSupportedCameras();
      return cameras.some((cam: camera.CameraDevice) => cam.cameraId === cameraDevice.cameraId);
    } catch (e) {
      console.error('检查相机可用性失败:', e);
      return false;
    }
  }

  /**
   * 监听窗口尺寸变化，重新选择相机
   * 
   * @param callback 相机变化回调
   */
  onWindowSizeChange(callback: (cameraDevice: camera.CameraDevice | null) => void): void {
    if (!this.windowClass) {
      return;
    }

    this.windowClass.on('windowSizeChange', async () => {
      const cameraDevice = await this.selectCamera();
      callback(cameraDevice);
    });
  }

  /**
   * 清理资源
   */
  release(): void {
    if (this.windowClass) {
      this.windowClass.off('windowSizeChange');
    }
  }
}

/**
 * 相机设备选择器（简化版）
 * 用于快速选择相机设备
 */
export class CameraDeviceSelector {
  private adapter: CameraAdapter;

  constructor(context: common.UIAbilityContext) {
    this.adapter = new CameraAdapter(context);
  }

  /**
   * 选择后置相机
   */
  async selectBackCamera(): Promise<camera.CameraDevice | null> {
    return await this.adapter.selectCamera(camera.CameraPosition.CAMERA_POSITION_BACK);
  }

  /**
   * 选择前置相机
   */
  async selectFrontCamera(): Promise<camera.CameraDevice | null> {
    return await this.adapter.selectCamera(camera.CameraPosition.CAMERA_POSITION_FRONT);
  }

  /**
   * 自动选择相机（优先后置）
   */
  async selectAutoCamera(): Promise<camera.CameraDevice | null> {
    return await this.adapter.selectCamera();
  }

  /**
   * 获取预览旋转角度
   */
  getPreviewRotation(cameraDevice: camera.CameraDevice): number {
    return this.adapter.calculatePreviewRotation(cameraDevice);
  }

  /**
   * 获取拍照旋转角度
   */
  getCaptureRotation(cameraDevice: camera.CameraDevice): number {
    return this.adapter.calculateCaptureRotation(cameraDevice);
  }

  /**
   * 监听窗口变化
   */
  onWindowSizeChange(callback: (cameraDevice: camera.CameraDevice | null) => void): void {
    this.adapter.onWindowSizeChange(callback);
  }

  /**
   * 清理资源
   */
  release(): void {
    this.adapter.release();
  }
}





