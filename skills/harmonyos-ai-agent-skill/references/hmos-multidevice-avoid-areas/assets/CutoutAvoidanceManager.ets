import window from '@ohos.window';
import display from '@ohos.display';
import common from '@ohos.app.ability.common';
import { BusinessError } from '@ohos.base';
import { UIContext } from '@ohos.arkui.UIContext'

export interface CutoutPadding {
  top?: number;
  bottom?: number;
  left?: number;
  right?: number;
}

export class CutoutAvoidanceManager {
  private static instance: CutoutAvoidanceManager;
  private mainWindow: window.Window | null = null;
  private uiContext: common.UIAbilityContext | null = null;
  private currentPadding: CutoutPadding = {};
  private listeners: ((padding: CutoutPadding) => void)[] = [];
  private screenWidth: number = 0;
  private screenHeight: number = 0;

  static getInstance(): CutoutAvoidanceManager {
    if (!CutoutAvoidanceManager.instance) {
      CutoutAvoidanceManager.instance = new CutoutAvoidanceManager();
    }
    return CutoutAvoidanceManager.instance;
  }

  private constructor() {
  }

  async init(context: common.UIAbilityContext): Promise<void> {
    try {
      this.uiContext = context;
      this.mainWindow = await window.getLastWindow(context);

      if (!this.mainWindow) {
        console.error('CutoutAvoidanceManager: Failed to get main window');
        return;
      }

      const displayInfo = display.getDefaultDisplaySync();
      this.screenWidth = displayInfo.width;
      this.screenHeight = displayInfo.height;

      this.mainWindow.on('avoidAreaChange', (data: window.AvoidAreaOptions) => {
        this.onAvoidAreaChange(data);
      });

      const cutoutArea = this.mainWindow.getWindowAvoidArea(window.AvoidAreaType.TYPE_CUTOUT);
      this.updateAvoidPadding(cutoutArea);

      console.info('CutoutAvoidanceManager initialized successfully');
    } catch (error) {
      const err = error as BusinessError;
      console.error(`CutoutAvoidanceManager init failed. Code: ${err.code}, message: ${err.message}`);
    }
  }

  private onAvoidAreaChange(avoidOptions: window.AvoidAreaOptions): void {
    if (avoidOptions.type === window.AvoidAreaType.TYPE_CUTOUT) {
      console.info('Cutout area changed');
      this.updateAvoidPadding(avoidOptions.area);
    } else if (avoidOptions.type === window.AvoidAreaType.TYPE_SYSTEM) {
      console.info('System area changed');
    } else if (avoidOptions.type === window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR) {
      console.info('Navigation indicator area changed');
    } else if (avoidOptions.type === window.AvoidAreaType.TYPE_KEYBOARD) {
      console.info('Keyboard area changed');
    }
  }

  private updateAvoidPadding(area: window.AvoidArea): void {
    const avoidAreaPadding: CutoutPadding = {};

    try {
      const displayInfo = display.getDefaultDisplaySync();
      this.screenWidth = displayInfo.width;
      this.screenHeight = displayInfo.height;

      if (area.topRect.height > 0) {
        avoidAreaPadding.top = this.px2vp(area.topRect.height + area.topRect.top);
        console.info(`Top cutout detected: padding=${avoidAreaPadding.top}vp`);
      }

      if (area.leftRect.width > 0) {
        avoidAreaPadding.left = this.px2vp(area.leftRect.left + area.leftRect.width);
        console.info(`Left cutout detected: padding=${avoidAreaPadding.left}vp`);
      }

      if (area.rightRect.width > 0) {
        avoidAreaPadding.right = this.px2vp(this.screenWidth - area.rightRect.left);
        console.info(`Right cutout detected: padding=${avoidAreaPadding.right}vp`);
      }

      if (area.bottomRect.height > 0) {
        avoidAreaPadding.bottom = this.px2vp(this.screenHeight - area.bottomRect.top);
        console.info(`Bottom cutout detected: padding=${avoidAreaPadding.bottom}vp`);
      }

      this.currentPadding = avoidAreaPadding;
      this.notifyListeners();

      console.info(`Avoid padding updated: ${JSON.stringify(avoidAreaPadding)}`);
    } catch (error) {
      const err = error as BusinessError;
      console.error(`Failed to set avoid padding. Code: ${err.code}, message: ${err.message}`);
    }
  }

  private px2vp(px: number): number {
    try {
      if(!this.mainWindow){
        return px;
      }
      let vpCount = this.mainWindow.getUIContext().px2vp(px);
      return vpCount;
    } catch (error) {
      console.warn('px2vp conversion failed, using raw value');
      return px;
    }
  }

  private notifyListeners(): void {
    this.listeners.forEach(callback => {
      try {
        callback(this.currentPadding);
      } catch (error) {
        console.error('Cutout listener error:', error);
      }
    });
  }

  getCurrentPadding(): CutoutPadding {
    return this.currentPadding;
  }

  onPaddingChange(callback: (padding: CutoutPadding) => void): void {
    if (!this.listeners.includes(callback)) {
      this.listeners.push(callback);
      if (Object.keys(this.currentPadding).length > 0) {
        callback(this.currentPadding);
      }
    }
  }

  offPaddingChange(callback: (padding: CutoutPadding) => void): void {
    const index = this.listeners.indexOf(callback);
    if (index > -1) {
      this.listeners.splice(index, 1);
    }
  }

  async setFullScreenImmersive(): Promise<void> {
    if (!this.mainWindow) {
      console.error('Main window is null');
      return;
    }

    try {
      await this.mainWindow.setWindowLayoutFullScreen(true);
      console.info('Set window layout full screen success');
    } catch (error) {
      const err = error as BusinessError;
      console.error(`Set window layout full screen failed. Code: ${err.code}, message: ${err.message}`);
    }
  }

  async hideSystemBars(): Promise<void> {
    if (!this.mainWindow) {
      console.error('Main window is null');
      return;
    }

    try {
      await this.mainWindow.setWindowSystemBarEnable([]);
      console.info('Hide system bars success');
    } catch (error) {
      const err = error as BusinessError;
      console.error(`Hide system bars failed. Code: ${err.code}, message: ${err.message}`);
    }
  }

  async showSystemBars(): Promise<void> {
    if (!this.mainWindow) {
      console.error('Main window is null');
      return;
    }

    try {
      await this.mainWindow.setWindowSystemBarEnable(['status', 'navigation']);
      console.info('Show system bars success');
    } catch (error) {
      const err = error as BusinessError;
      console.error(`Show system bars failed. Code: ${err.code}, message: ${err.message}`);
    }
  }

  destroy(): void {
    if (this.mainWindow) {
      this.mainWindow.off('avoidAreaChange');
      this.mainWindow = null;
    }
    this.listeners = [];
    this.currentPadding = {};
    this.uiContext = null;
  }
}
