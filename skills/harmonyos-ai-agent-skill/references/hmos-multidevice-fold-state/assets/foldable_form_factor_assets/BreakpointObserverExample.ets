import { window } from '@kit.ArkUI';
import { display } from '@kit.ArkUI';
import { hilog } from '@kit.PerformanceAnalysisKit';

const TAG = 'FoldableFormFactorBreakpointObserver';
const DOMAIN = 0xFF00;

interface BreakpointInfo {
  name: string;
  horizontal: string;
  vertical: string;
}

class BreakpointSystem {
  private currentBreakpoint: string = 'sm';
  private currentWindow: window.Window | null = null;
  private breakpointListeners: Array<(breakpoint: string) => void> = [];

  private breakpointMap: Record<string, BreakpointInfo> = {
    'sm': { name: 'sm', horizontal: '0-599vp', vertical: '0-599vp' },
    'md': { name: 'md', horizontal: '600-839vp', vertical: '600-839vp' },
    'lg': { name: 'lg', horizontal: '840-1439vp', vertical: '840-1439vp' },
    'xl': { name: 'xl', horizontal: '1440vp+', vertical: '1440vp+' }
  };

  async init() {
    try {
      this.currentWindow = window.getLastWindow(getContext(this));
      this.updateBreakpoint();

      this.currentWindow.on('windowSizeChange', (windowSize) => {
        const newBreakpoint = this.calculateBreakpoint(windowSize.width, windowSize.height);
        if (newBreakpoint !== this.currentBreakpoint) {
          this.currentBreakpoint = newBreakpoint;
          this.notifyListeners();
          hilog.info(DOMAIN, TAG, 'Window size changed, breakpoint: %{public}s', newBreakpoint);
        }
      });

      hilog.info(DOMAIN, TAG, 'BreakpointObserver initialized, current: %{public}s', this.currentBreakpoint);
    } catch (err) {
      hilog.error(DOMAIN, TAG, 'Failed to initialize BreakpointObserver: %{public}s', JSON.stringify(err));
    }
  }

  private calculateBreakpoint(width: number, height: number): string {
    const horizontalSize = Math.min(width, height);
    const verticalSize = Math.max(width, height);

    if (horizontalSize >= 1440) return 'xl';
    if (horizontalSize >= 840) return 'lg';
    if (horizontalSize >= 600) return 'md';
    return 'sm';
  }

  private updateBreakpoint() {
    if (this.currentWindow) {
      const rect = this.currentWindow.getWindowProperties().windowRect;
      this.currentBreakpoint = this.calculateBreakpoint(rect.width, rect.height);
    }
  }

  private notifyListeners() {
    this.breakpointListeners.forEach(listener => listener(this.currentBreakpoint));
  }

  getCurrentBreakpoint(): string {
    return this.currentBreakpoint;
  }

  onBreakpointChange(listener: (breakpoint: string) => void) {
    this.breakpointListeners.push(listener);
  }

  unregister() {
    if (this.currentWindow) {
      this.currentWindow.off('windowSizeChange');
      this.currentWindow = null;
    }
    this.breakpointListeners = [];
  }
}

@Entry
@Component
struct FoldableFormFactorBreakpointPage {
  @State currentBreakpoint: string = 'sm';
  @State windowWidth: number = 0;
  @State windowHeight: number = 0;
  @State isFolded: boolean = false;
  @State foldStatus: string = 'expanded';
  private breakpointSystem: BreakpointSystem = new BreakpointSystem();
  private foldStatusCallback: ((status: display.FoldStatus) => void) | null = null;

  async aboutToAppear() {
    await this.breakpointSystem.init();
    this.breakpointSystem.onBreakpointChange((breakpoint) => {
      this.currentBreakpoint = breakpoint;
      hilog.info(DOMAIN, TAG, 'Breakpoint changed to: %{public}s', breakpoint);
    });

    this.initFoldStatusListener();
  }

  private async initFoldStatusListener() {
    try {
      const defaultDisplay = display.getDefaultDisplaySync();
      if (defaultDisplay) {
        this.foldStatusCallback = (status: display.FoldStatus): void => {
          this.isFolded = (status === display.FoldStatus.FOLD_STATUS_FOLDED);
          switch (status) {
            case display.FoldStatus.FOLD_STATUS_FOLDED:
              this.foldStatus = 'folded';
              break;
            case display.FoldStatus.FOLD_STATUS_HALF_FOLDED:
              this.foldStatus = 'half_folded';
              break;
            case display.FoldStatus.FOLD_STATUS_EXPANDED:
              this.foldStatus = 'expanded';
              break;
            default:
              this.foldStatus = 'unknown';
          }
          hilog.info(DOMAIN, TAG, 'Fold status changed: %{public}s', this.foldStatus);
        };

        display.on('foldStatusChange', this.foldStatusCallback);
      }
    } catch (err) {
      hilog.error(DOMAIN, TAG, 'Failed to init fold status listener: %{public}s', JSON.stringify(err));
    }
  }

  aboutToDisappear() {
    this.breakpointSystem.unregister();
    if (this.foldStatusCallback) {
      try {
        display.off('foldStatusChange', this.foldStatusCallback);
      } catch (err) {
        hilog.error(DOMAIN, TAG, 'Failed to unregister fold status: %{public}s', JSON.stringify(err));
      }
    }
  }

  build() {
    Column() {
      Text('特殊比例折叠屏断点监听示例')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 20 })

      Column() {
        Text('当前断点')
          .fontSize(16)
          .fontColor('#666666')
        Text(this.currentBreakpoint.toUpperCase())
          .fontSize(32)
          .fontWeight(FontWeight.Bold)
          .fontColor('#007AFF')
          .margin({ top: 8 })
      }
      .width('100%')
      .padding(16)
      .backgroundColor('#F5F5F5')
      .borderRadius(12)
      .margin({ bottom: 16 })

      Row() {
        Column() {
          Text('折叠状态')
            .fontSize(14)
            .fontColor('#666666')
          Text(this.isFolded ? '已折叠' : '已展开')
            .fontSize(18)
            .fontWeight(FontWeight.Medium)
            .margin({ top: 4 })
        }
        .alignItems(HorizontalAlign.Center)

        Column() {
          Text('折叠状态值')
            .fontSize(14)
            .fontColor('#666666')
          Text(this.foldStatus)
            .fontSize(18)
            .fontWeight(FontWeight.Medium)
            .margin({ top: 4 })
        }
        .alignItems(HorizontalAlign.Center)
        .margin({ left: 40 })
      }
      .width('100%')
      .justifyContent(FlexAlign.Center)
      .margin({ bottom: 16 })

      Column() {
        Text('布局建议')
          .fontSize(16)
          .fontWeight(FontWeight.Medium)
          .margin({ bottom: 12 })

        if (this.currentBreakpoint === 'sm') {
          Text('单列布局 - 手机模式')
            .fontSize(14)
            .fontColor('#333333')
        } else if (this.currentBreakpoint === 'md') {
          Text('双列布局 - 小屏平板模式')
            .fontSize(14)
            .fontColor('#333333')
        } else if (this.currentBreakpoint === 'lg') {
          Text('三列布局 - 大屏平板模式')
            .fontSize(14)
            .fontColor('#333333')
        } else {
          Text('多列布局 - 超大屏模式')
            .fontSize(14)
            .fontColor('#333333')
        }
      }
      .width('100%')
      .padding(16)
      .backgroundColor('#E8F5E9')
      .borderRadius(12)
    }
    .width('100%')
    .height('100%')
    .padding(20)
    .backgroundColor('#FFFFFF')
  }
}
