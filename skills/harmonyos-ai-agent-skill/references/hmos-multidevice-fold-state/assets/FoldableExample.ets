import { window } from '@kit.ArkUI';
import { hilog } from '@kit.PerformanceAnalysisKit';

@Entry
@Component
struct FoldableExample {
  @State isFolded: boolean = false;
  private windowSizeChangeCallback: ((size: window.Size) => void) | null = null;
  private readonly FOLD_THRESHOLD: number = 600;

  aboutToAppear() {
    try {
      const windowStage = AppStorage.get('windowStage') as window.WindowStage;
      if (windowStage) {
        const win = windowStage.getMainWindowSync();
        
        if (win) {
          const properties = win.getWindowProperties();
          if (properties && properties.windowRect) {
            this.isFolded = properties.windowRect.width < this.FOLD_THRESHOLD;
            hilog.info(0xFF00, 'FoldableExample', 'Initial state: isFolded=%{public}s, width=%{public}f', 
              this.isFolded.toString(), properties.windowRect.width);
          }
          
          this.windowSizeChangeCallback = (size: window.Size) => {
            try {
              if (size && size.width !== undefined) {
                this.isFolded = size.width < this.FOLD_THRESHOLD;
                hilog.info(0xFF00, 'FoldableExample', 'Size changed: isFolded=%{public}s, width=%{public}f', 
                  this.isFolded.toString(), size.width);
              } else {
                hilog.warn(0xFF00, 'FoldableExample', 'Invalid size data received');
              }
            } catch (err) {
              hilog.error(0xFF00, 'FoldableExample', 'Error in size change callback: %{public}s', JSON.stringify(err));
            }
          };
          
          win.on('windowSizeChange', this.windowSizeChangeCallback);
        }
      }
    } catch (err) {
      hilog.error(0xFF00, 'FoldableExample', 'Failed to get window: %{public}s', JSON.stringify(err));
    }
  }

  aboutToDisappear() {
    try {
      const windowStage = AppStorage.get('windowStage') as window.WindowStage;
      if (windowStage && this.windowSizeChangeCallback) {
        const win = windowStage.getMainWindowSync();
        if (win) {
          win.off('windowSizeChange', this.windowSizeChangeCallback);
          hilog.info(0xFF00, 'FoldableExample', 'Window size change listener removed');
        }
      }
      this.windowSizeChangeCallback = null;
    } catch (err) {
      hilog.error(0xFF00, 'FoldableExample', 'Failed to cleanup: %{public}s', JSON.stringify(err));
    }
  }

  build() {
    Column() {
      Text('折叠屏适配示例')
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 16 })
      
      Text('当前状态: ' + (this.isFolded ? '折叠态' : '展开态'))
        .fontSize(16)
        .fontColor('#666666')
        .margin({ bottom: 16 })
      
      if (this.isFolded) {
        Column() {
          Text('折叠态布局（单列）')
            .fontSize(16)
            .fontColor('#333333')
            .margin({ bottom: 8 })
          
          Column() {
            Text('内容区域 1')
              .fontSize(14)
              .padding(16)
              .backgroundColor('#F5F5F5')
              .borderRadius(8)
              .margin({ bottom: 8 })
            
            Text('内容区域 2')
              .fontSize(14)
              .padding(16)
              .backgroundColor('#F5F5F5')
              .borderRadius(8)
          }
          .width('100%')
          .padding(16)
        }
      } else {
        Row() {
          Column() {
            Text('左侧区域')
              .fontSize(16)
              .fontColor('#333333')
              .margin({ bottom: 8 })
            
            Text('内容 1')
              .fontSize(14)
              .padding(16)
              .backgroundColor('#F5F5F5')
              .borderRadius(8)
              .margin({ bottom: 8 })
            
            Text('内容 2')
              .fontSize(14)
              .padding(16)
              .backgroundColor('#F5F5F5')
              .borderRadius(8)
          }
          .width(320)
          .padding(16)
          .backgroundColor('#FFFFFF')
          
          Column() {
            Text('右侧区域')
              .fontSize(16)
              .fontColor('#333333')
              .margin({ bottom: 8 })
            
            Text('详细内容')
              .fontSize(14)
              .padding(16)
              .backgroundColor('#F5F5F5')
              .borderRadius(8)
          }
          .layoutWeight(1)
          .padding(16)
          .backgroundColor('#FFFFFF')
        }
        .width('100%')
      }
    }
    .width('100%')
    .height('100%')
    .padding(16)
    .backgroundColor('#FFFFFF')
  }
}
