import { window } from '@kit.ArkUI';
import { hilog } from '@kit.PerformanceAnalysisKit';

const TAG = 'FoldableFormFactorWindowSize';
const DOMAIN = 0xFF01;

interface WindowSize {
  width: number;
  height: number;
}

@Entry
@Component
struct FoldableFormFactorWindowSizePage {
  @State currentWindowSize: WindowSize = { width: 0, height: 0 };
  @State previousWindowSize: WindowSize = { width: 0, height: 0 };
  @State windowMode: string = 'full';
  @State isChanging: boolean = false;
  private windowClass: window.Window | null = null;
  private changeTimer: number | null = null;

  async aboutToAppear() {
    try {
      this.windowClass = window.getLastWindow(getContext(this));
      const properties = this.windowClass.getWindowProperties();
      this.currentWindowSize = {
        width: Math.round(properties.windowRect.width),
        height: Math.round(properties.windowRect.height)
      };
      this.previousWindowSize = { ...this.currentWindowSize };

      this.windowClass.on('windowSizeChange', (windowSize: window.Size) => {
        this.isChanging = true;
        if (this.changeTimer) {
          clearTimeout(this.changeTimer);
        }

        this.previousWindowSize = { ...this.currentWindowSize };
        this.currentWindowSize = {
          width: Math.round(windowSize.width),
          height: Math.round(windowSize.height)
        };

        hilog.info(DOMAIN, TAG, 'Window size changed: %{public}d x %{public}d',
          this.currentWindowSize.width, this.currentWindowSize.height);

        this.changeTimer = setTimeout(() => {
          this.isChanging = false;
          this.updateWindowMode();
        }, 300);
      });

      this.updateWindowMode();
      hilog.info(DOMAIN, TAG, 'Window size listener registered');
    } catch (err) {
      hilog.error(DOMAIN, TAG, 'Failed to get window: %{public}s', JSON.stringify(err));
    }
  }

  private updateWindowMode() {
    const minSize = Math.min(this.currentWindowSize.width, this.currentWindowSize.height);
    if (minSize < 400) {
      this.windowMode = '悬浮窗';
    } else if (this.currentWindowSize.width < 600 || this.currentWindowSize.height < 600) {
      this.windowMode = '分屏';
    } else {
      this.windowMode = '全屏';
    }
  }

  aboutToDisappear() {
    if (this.windowClass) {
      this.windowClass.off('windowSizeChange');
      this.windowClass = null;
    }
    if (this.changeTimer) {
      clearTimeout(this.changeTimer);
    }
  }

  build() {
    Column() {
      Text('特殊比例折叠屏窗口尺寸变化监听示例')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 20 })

      Column() {
        Text('当前窗口尺寸')
          .fontSize(16)
          .fontColor('#666666')
        Text(`${this.currentWindowSize.width} x ${this.currentWindowSize.height} vp`)
          .fontSize(28)
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
          Text('窗口模式')
            .fontSize(14)
            .fontColor('#666666')
          Text(this.windowMode)
            .fontSize(18)
            .fontWeight(FontWeight.Medium)
            .margin({ top: 4 })
        }
        .alignItems(HorizontalAlign.Center)

        Column() {
          Text('变化状态')
            .fontSize(14)
            .fontColor('#666666')
          Text(this.isChanging ? '变化中...' : '稳定')
            .fontSize(18)
            .fontWeight(FontWeight.Medium)
            .fontColor(this.isChanging ? '#FF9500' : '#34C759')
            .margin({ top: 4 })
        }
        .alignItems(HorizontalAlign.Center)
        .margin({ left: 40 })
      }
      .width('100%')
      .justifyContent(FlexAlign.Center)
      .margin({ bottom: 16 })

      if (this.previousWindowSize.width > 0) {
        Column() {
          Text('尺寸变化')
            .fontSize(14)
            .fontColor('#666666')
            .margin({ bottom: 8 })
          
          Row() {
            Text('宽度变化: ')
              .fontSize(14)
              .fontColor('#666666')
            Text(this.currentWindowSize.width >= this.previousWindowSize.width ? '+' : '')
              .fontSize(14)
              .fontColor(this.currentWindowSize.width >= this.previousWindowSize.width ? '#34C759' : '#FF3B30')
            Text((this.currentWindowSize.width - this.previousWindowSize.width).toString())
              .fontSize(14)
              .fontWeight(FontWeight.Bold)
              .fontColor(this.currentWindowSize.width >= this.previousWindowSize.width ? '#34C759' : '#FF3B30')
            Text(' vp')
              .fontSize(14)
              .fontColor('#666666')
          }
          .margin({ bottom: 4 })

          Row() {
            Text('高度变化: ')
              .fontSize(14)
              .fontColor('#666666')
            Text(this.currentWindowSize.height >= this.previousWindowSize.height ? '+' : '')
              .fontSize(14)
              .fontColor(this.currentWindowSize.height >= this.previousWindowSize.height ? '#34C759' : '#FF3B30')
            Text((this.currentWindowSize.height - this.previousWindowSize.height).toString())
              .fontSize(14)
              .fontWeight(FontWeight.Bold)
              .fontColor(this.currentWindowSize.height >= this.previousWindowSize.height ? '#34C759' : '#FF3B30')
            Text(' vp')
              .fontSize(14)
              .fontColor('#666666')
          }
        }
        .width('100%')
        .padding(16)
        .backgroundColor('#E8F5E9')
        .borderRadius(12)
      }

      Column() {
        Text('使用说明')
          .fontSize(16)
          .fontWeight(FontWeight.Medium)
          .margin({ bottom: 12 })
        
        Text('window.on("windowSizeChange") 用于监听窗口尺寸变化')
          .fontSize(14)
          .fontColor('#333333')
          .margin({ bottom: 8 })
        Text('回调参数为 window.Size 对象，包含 width 和 height 属性')
          .fontSize(14)
          .fontColor('#333333')
          .margin({ bottom: 8 })
        Text('建议结合断点系统实现响应式布局')
          .fontSize(14)
          .fontColor('#333333')
      }
      .width('100%')
      .padding(16)
      .backgroundColor('#FFF3E0')
      .borderRadius(12)
      .margin({ top: 16 })
    }
    .width('100%')
    .height('100%')
    .padding(20)
    .backgroundColor('#FFFFFF')
  }
}
