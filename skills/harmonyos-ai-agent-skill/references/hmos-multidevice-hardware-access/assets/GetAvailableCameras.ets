import { camera } from '@kit.CameraKit';
import { common } from '@kit.AbilityKit';

async function getAvailableCameras(context: common.UIAbilityContext): Promise<camera.CameraDevice[]> {
  try {
    const cameraManager = camera.getCameraManager(context);
    const cameras = await cameraManager.getSupportedCameras();
    return cameras;
  } catch (error) {
    console.error('获取相机列表失败:', error);
    return [];
  }
}
