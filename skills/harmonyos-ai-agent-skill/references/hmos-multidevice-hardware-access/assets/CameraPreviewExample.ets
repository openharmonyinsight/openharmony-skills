import { camera } from '@kit.CameraKit';
import display from '@ohos.display';
import { common } from '@kit.AbilityKit';

@Entry
@Component
struct CameraPreview {
  private cameraDevice: camera.CameraDevice | null = null;
  private cameraManager: camera.CameraManager = camera.getCameraManager(this.getUIContext().getHostContext() as common.UIAbilityContext);
  private cameraInput: camera.CameraInput | null = null;
  private previewOutput: camera.PreviewOutput | null = null;
  private captureSession: camera.Session | null = null;
  private surfaceId: string = '';

  async createPreviewStream(cameraDevice: camera.CameraDevice) {
    try {
      const profiles = this.cameraManager.getSupportedOutputCapability(cameraDevice, camera.SceneMode.NORMAL_VIDEO).previewProfiles;
      
      const previewProfile = this.selectPreviewProfile(profiles);
      
      const rotation = await this.calculatePreviewRotation(cameraDevice);
      
      this.cameraInput = this.cameraManager.createCameraInput(cameraDevice);
      await this.cameraInput.open();
      
      this.previewOutput = this.cameraManager.createPreviewOutput(previewProfile, this.surfaceId);
      
      this.captureSession = this.cameraManager.createSession(camera.SceneMode.NORMAL_VIDEO);
      this.captureSession.beginConfig();
      this.captureSession.addInput(this.cameraInput);
      this.captureSession.addOutput(this.previewOutput);
      await this.captureSession.commitConfig();
      
      await this.captureSession.start();
      
      console.log('预览流已配置，rotation:', rotation);
    } catch (error) {
      console.error('创建预览流失败:', error);
    }
  }

  private selectPreviewProfile(profiles: camera.Profile[]): camera.Profile {
    let windowAspectRatio = 1.0;
    
    let bestProfile = profiles[0];
    let minDiff = Infinity;
    
    for (const profile of profiles) {
      const profileAspectRatio = profile.size.width / profile.size.height;
      const diff = Math.abs(profileAspectRatio - windowAspectRatio);
      
      if (diff < minDiff) {
        minDiff = diff;
        bestProfile = profile;
      }
    }
    
    return bestProfile;
  }

  private async calculatePreviewRotation(cameraDevice: camera.CameraDevice): Promise<number> {
    const defaultDisplay = display.getDefaultDisplaySync();
    const rotation = defaultDisplay.rotation;
    
    const lensOrientation = this.getLensOrientation(cameraDevice);
    
    const previewRotation = (lensOrientation + rotation * 90) % 360;
    
    return previewRotation;
  }

  private getLensOrientation(cameraDevice: camera.CameraDevice): number {
    if (cameraDevice.cameraPosition === camera.CameraPosition.CAMERA_POSITION_BACK) {
      return 90;
    } else {
      return 270;
    }
  }

  async release() {
    if (this.captureSession) {
      await this.captureSession.stop();
      this.captureSession.release();
    }
    if (this.previewOutput) {
      this.previewOutput.release();
    }
    if (this.cameraInput) {
      this.cameraInput.close();
    }
  }

  build() {
    Column() {
      XComponent({
        id: 'cameraPreview',
        type: XComponentType.SURFACE
      })
        .onLoad((event) => {
          this.surfaceId = (event as Record<string, Object>).surfaceId as string;
          console.log('Surface ID:', this.surfaceId);
        })
        .width('100%')
        .height('100%')
    }
  }
}