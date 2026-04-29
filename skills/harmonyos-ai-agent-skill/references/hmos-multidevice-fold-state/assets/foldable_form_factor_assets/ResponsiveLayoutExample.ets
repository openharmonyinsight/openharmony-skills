import { window } from '@kit.ArkUI';
import { display } from '@kit.ArkUI';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { common } from '@kit.AbilityKit';

const TAG = 'FoldableFormFactorResponsiveLayout';
const DOMAIN = 0xFF02;

interface LayoutConfig {
  columns: number;
  sidebarWidth: number;
  gridColumns: number;
  showSidebar: boolean;
}

@Entry
@Component
struct FoldableFormFactorResponsiveLayoutPage {
  @State currentBreakpoint: string = 'sm';
  @State isFolded: boolean = false;
  @State layoutConfig: LayoutConfig = {
    columns: 1,
    sidebarWidth: 0,
    gridColumns: 2,
    showSidebar: false
  };
  private windowClass: window.Window | null = null;
  private foldStatusCallback: ((status: display.FoldStatus) => void) | null = null;

  private layoutConfigs: Record<string, LayoutConfig> = {
    'sm': { columns: 1, sidebarWidth: 0, gridColumns: 2, showSidebar: false },
    'md': { columns: 2, sidebarWidth: 200, gridColumns: 3, showSidebar: false },
    'lg': { columns: 3, sidebarWidth: 240, gridColumns: 4, showSidebar: true },
    'xl': { columns: 4, sidebarWidth: 280, gridColumns: 6, showSidebar: true }
  };

  async aboutToAppear() {
    await this.initWindowListener();
    this.initFoldStatusListener();
  }

  private async initWindowListener() {
    try {
      this.windowClass = await window.getLastWindow(this.getUIContext().getHostContext() as common.UIAbilityContext);
      this.updateLayout();

      this.windowClass.on('windowSizeChange', () => {
        this.updateLayout();
      });
    } catch (err) {
      hilog.error(DOMAIN, TAG, 'Failed to init window listener: %{public}s', JSON.stringify(err));
    }
  }

  private initFoldStatusListener() {
    try {
      const defaultDisplay = display.getDefaultDisplaySync();
      if (defaultDisplay !== null) {
        this.foldStatusCallback = (status: display.FoldStatus): void => {
          this.isFolded = (status === display.FoldStatus.FOLD_STATUS_FOLDED);
          this.updateLayout();
          hilog.info(DOMAIN, TAG, 'Fold status: %{public}d, isFolded: %{public}s', status, this.isFolded.toString());
        };
        display.on('foldStatusChange', this.foldStatusCallback);
      }
    } catch (err) {
      hilog.error(DOMAIN, TAG, 'Failed to init fold status: %{public}s', JSON.stringify(err));
    }
  }

  private updateLayout() {
    if (this.windowClass) {
      const rect = this.windowClass.getWindowProperties().windowRect;
      const minSize = Math.min(rect.width, rect.height);

      if (minSize >= 1440) {
        this.currentBreakpoint = 'xl';
      } else if (minSize >= 840) {
        this.currentBreakpoint = 'lg';
      } else if (minSize >= 600) {
        this.currentBreakpoint = 'md';
      } else {
        this.currentBreakpoint = 'sm';
      }

      this.layoutConfig = this.layoutConfigs[this.currentBreakpoint];
      hilog.info(DOMAIN, TAG, 'Layout updated, breakpoint: %{public}s', this.currentBreakpoint);
    }
  }

  aboutToDisappear() {
    if (this.windowClass) {
      this.windowClass.off('windowSizeChange');
      this.windowClass = null;
    }
    if (this.foldStatusCallback) {
      try {
        display.off('foldStatusChange', this.foldStatusCallback);
      } catch (err) {
        hilog.error(DOMAIN, TAG, 'Failed to unregister: %{public}s', JSON.stringify(err));
      }
    }
  }

  build() {
    Row() {
      if (this.layoutConfig.showSidebar) {
        Column() {
          Text('侧边栏')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .margin({ bottom: 16 })

          Column() {
            Text('导航1')
              .fontSize(16)
              .padding(12)
              .width('100%')
          }
          .backgroundColor('#F5F5F5')
          .borderRadius(8)
          .margin({ bottom: 8 })

          Column() {
            Text('导航2')
              .fontSize(16)
              .padding(12)
              .width('100%')
          }
          .backgroundColor('#F5F5F5')
          .borderRadius(8)
          .margin({ bottom: 8 })

          Column() {
            Text('导航3')
              .fontSize(16)
              .padding(12)
              .width('100%')
          }
          .backgroundColor('#F5F5F5')
          .borderRadius(8)
        }
        .width(this.layoutConfig.sidebarWidth)
        .height('100%')
        .padding(16)
        .backgroundColor('#FAFAFA')
        .border({ width: { right: 1 }, color: '#E0E0E0' })
      }

      Column() {
        Row() {
          Text('特殊比例折叠屏响应式布局示例')
            .fontSize(24)
            .fontWeight(FontWeight.Bold)

          Blank()

          Column() {
            Text(`断点: ${this.currentBreakpoint.toUpperCase()}`)
              .fontSize(14)
              .fontColor('#007AFF')
          }
          .padding(8)
          .backgroundColor('#E3F2FD')
          .borderRadius(8)
        }
        .margin({ bottom: 20 })

        Row() {
          Column() {
            Text('内容区域')
              .fontSize(16)
              .fontColor('#666666')
            Text(`列数: ${this.layoutConfig.columns}`)
              .fontSize(14)
              .margin({ top: 8 })
          }
          .alignItems(HorizontalAlign.Center)
          .layoutWeight(1)

          Column() {
            Text('网格')
              .fontSize(16)
              .fontColor('#666666')
            Text(`列数: ${this.layoutConfig.gridColumns}`)
              .fontSize(14)
              .margin({ top: 8 })
          }
          .alignItems(HorizontalAlign.Center)
          .layoutWeight(1)
        }
        .margin({ bottom: 20 })

        Text('网格布局演示')
          .fontSize(18)
          .fontWeight(FontWeight.Medium)
          .width('100%')
          .margin({ bottom: 12 })

        Grid() {
          ForEach([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], (item: number) => {
            GridItem() {
              Column() {
                Text(`Item ${item}`)
                  .fontSize(14)
                  .fontWeight(FontWeight.Medium)
              }
              .width('100%')
              .height(60)
              .justifyContent(FlexAlign.Center)
              .backgroundColor(this.getItemColor(item))
              .borderRadius(8)
            }
          })
        }
        .columnsTemplate(this.getColumnsTemplate())
        .columnsGap(8)
        .rowsGap(8)
        .width('100%')
        .layoutWeight(1)

        Text(`折叠状态: ${this.isFolded ? '已折叠' : '已展开'}`)
          .fontSize(14)
          .fontColor('#666666')
          .margin({ top: 16 })
      }
      .layoutWeight(1)
      .height('100%')
      .padding(20)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFFFFF')
  }

  private getItemColor(index: number): string {
    const colors = ['#E3F2FD', '#F3E5F5', '#E8F5E9', '#FFF3E0', '#FCE4EC', '#E0F7FA'];
    return colors[index % colors.length];
  }

  private getColumnsTemplate(): string {
    const cols = this.layoutConfig.gridColumns;
    let template = '';
    for (let i = 0; i < cols; i++) {
      template += '1fr ';
    }
    return template.trim();
  }
}
