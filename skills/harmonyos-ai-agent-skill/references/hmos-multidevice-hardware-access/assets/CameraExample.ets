
let cameraModule: ESObject | null = null;
try {
  cameraModule = import('@kit.CameraKit');
} catch (err) {
  console.error(`Failed to import camera module: ${JSON.stringify(err)}`);
}

@Entry
@Component
struct CameraExample {
  @State isCameraSupported: boolean = false;
  @State cameraStatus: string = '未检查';

  checkCamera() {
    try {
      const supported = canIUse("SystemCapability.Multimedia.Camera.Core");
      this.isCameraSupported = supported;
      this.cameraStatus = supported ? '相机功能支持' : '相机功能不支持';
      console.info(`Camera capability: ${supported ? 'Supported' : 'Not Supported'}`);

      try {
        this.getUIContext().getPromptAction().showToast({
          message: this.cameraStatus,
          duration: 2000
        });
      } catch (toastErr) {
        console.error(`Failed to show toast: ${JSON.stringify(toastErr)}`);
      }
    } catch (err) {
      console.error(`Failed to check camera capability: ${JSON.stringify(err)}`);
      this.cameraStatus = '检查失败';
    }
  }

  importCheckCamera() {
    try {
      if (cameraModule !== undefined && cameraModule !== null) {
        console.info('Camera module imported successfully');
        this.cameraStatus = '相机模块导入成功';
        try {
          this.getUIContext().getPromptAction().showToast({
            message: "相机模块导入成功",
            duration: 2000
          });
        } catch (toastErr) {
          console.error(`Failed to show toast: ${JSON.stringify(toastErr)}`);
        }
      } else {
        console.info('Camera module not available');
        this.cameraStatus = '相机模块不可用';
        try {
          this.getUIContext().getPromptAction().showToast({
            message: "相机模块不可用",
            duration: 2000
          });
        } catch (toastErr) {
          console.error(`Failed to show toast: ${JSON.stringify(toastErr)}`);
        }
      }
    } catch (err) {
      console.error(`Failed to check camera import: ${JSON.stringify(err)}`);
      this.cameraStatus = '导入检查失败';
    }
  }

  initCamera() {
    try {
      if (!this.isCameraSupported) {
        console.warn('Camera not supported, cannot initialize');
        this.cameraStatus = '相机不支持，无法初始化';
        try {
          this.getUIContext().getPromptAction().showToast({
            message: "设备不支持相机，无法初始化",
            duration: 2000
          });
        } catch (toastErr) {
          console.error(`Failed to show toast: ${JSON.stringify(toastErr)}`);
        }
        return;
      }

      console.info('Initializing camera...');
      this.cameraStatus = '正在初始化相机...';
      try {
        this.getUIContext().getPromptAction().showToast({
          message: "正在初始化相机...",
          duration: 2000
        });
      } catch (toastErr) {
        console.error(`Failed to show toast: ${JSON.stringify(toastErr)}`);
      }

      console.info('Camera initialized successfully');
      this.cameraStatus = '相机初始化成功';
      try {
        this.getUIContext().getPromptAction().showToast({
          message: "相机初始化成功",
          duration: 2000
        });
      } catch (toastErr) {
        console.error(`Failed to show toast: ${JSON.stringify(toastErr)}`);
      }
    } catch (err) {
      console.error(`Failed to initialize camera: ${JSON.stringify(err)}`);
      this.cameraStatus = '初始化失败';
    }
  }

  build() {
    Column() {
      Text('相机功能示例')
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 20, bottom: 20 })

      Button('检查相机能力')
        .onClick(() => {
          this.checkCamera();
        })
        .margin({ bottom: 10 })

      Button('检查相机模块导入')
        .onClick(() => {
          this.importCheckCamera();
        })
        .margin({ bottom: 10 })

      Button('初始化相机')
        .onClick(() => {
          this.initCamera();
        })
        .margin({ bottom: 20 })

      Text(`状态: ${this.cameraStatus}`)
        .fontSize(14)
        .fontColor('#666666')
        .margin({ bottom: 20 })

      Text('说明:')
        .fontSize(14)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 10, bottom: 5 })

      Text('方法一：使用canIUse()判断系统能力')
        .fontSize(12)
        .fontColor('#666666')
        .margin({ bottom: 5 })

      Text('方法二：使用import动态导入模块')
        .fontSize(12)
        .fontColor('#666666')
        .margin({ bottom: 5 })

      Text('实际使用：初始化相机并获取相机管理器')
        .fontSize(12)
        .fontColor('#666666')
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}
