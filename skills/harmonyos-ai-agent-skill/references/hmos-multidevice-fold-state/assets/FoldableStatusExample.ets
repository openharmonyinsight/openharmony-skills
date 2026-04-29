import { display } from '@kit.ArkUI';

/**
 * 注意：
 * - 本文件为官方 API 工程模板，配套折叠状态检测主路径使用。
 * - 方案基线请先参考：../references/fold_status_detection.md
 */

@Entry
@Component
struct FoldableStatusExample {
  @StorageProp('foldStatus') foldStatus: number = 0;
  @StorageProp('isFoldable') isFoldable: boolean = false;
  @State currentStatus: string = '未知';

  aboutToAppear() {
    this.updateStatusDisplay();
  }

  updateStatusDisplay() {
    try {
      if (!this.isFoldable) {
        this.currentStatus = '非折叠屏设备';
        return;
      }

      switch (this.foldStatus) {
        case display.FoldStatus.FOLD_STATUS_EXPANDED:
          this.currentStatus = '展开态 (Expanded)';
          break;
        case display.FoldStatus.FOLD_STATUS_FOLDED:
          this.currentStatus = '折叠态 (Folded)';
          break;
        case display.FoldStatus.FOLD_STATUS_HALF_FOLDED:
          this.currentStatus = '半折叠态 (Half-Folded/Hover)';
          break;
        default:
          this.currentStatus = '未知状态';
      }
    } catch (err) {
      console.error(`[FoldableStatus] Failed to update status: ${JSON.stringify(err)}`);
      this.currentStatus = '状态获取失败';
    }
  }

  checkFoldStatus() {
    try {
      const status = display.getFoldStatus();
      AppStorage.setOrCreate('foldStatus', status);
      console.info(`[FoldableStatus] Current fold status: ${status}`);
      this.updateStatusDisplay();
      try {
        this.getUIContext().getPromptAction().showToast({
          message: `折叠状态: ${this.currentStatus}`,
          duration: 2000
        });
      } catch (toastErr) {
        console.error(`Failed to show toast: ${JSON.stringify(toastErr)}`);
      }
    } catch (err) {
      console.error(`[FoldableStatus] Failed to check fold status: ${JSON.stringify(err)}`);
      try {
        this.getUIContext().getPromptAction().showToast({
          message: "获取折叠状态失败",
          duration: 2000
        });
      } catch (toastErr) {
        console.error(`Failed to show toast: ${JSON.stringify(toastErr)}`);
      }
    }
  }

  build() {
    Column() {
      Text('折叠屏状态示例')
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 20, bottom: 20 })

      Text(`当前状态: ${this.currentStatus}`)
        .fontSize(16)
        .fontColor('#333333')
        .margin({ bottom: 20 })

      Button('检查折叠状态')
        .onClick(() => {
          this.checkFoldStatus();
        })
        .margin({ bottom: 20 })

      Text('状态说明:')
        .fontSize(14)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 10, bottom: 5 })

      if (this.foldStatus === display.FoldStatus.FOLD_STATUS_EXPANDED) {
        Column() {
          Text('展开态 (Expanded)')
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .margin({ bottom: 5 })
          Text('设备完全展开，显示完整屏幕')
            .fontSize(12)
            .fontColor('#666666')
        }
        .width('100%')
        .padding(10)
        .backgroundColor('#E8F5E9')
        .borderRadius(8)
        .margin({ bottom: 10 })
      } else if (this.foldStatus === display.FoldStatus.FOLD_STATUS_FOLDED) {
        Column() {
          Text('折叠态 (Folded)')
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .margin({ bottom: 5 })
          Text('设备完全折叠，显示外屏')
            .fontSize(12)
            .fontColor('#666666')
        }
        .width('100%')
        .padding(10)
        .backgroundColor('#FFF3E0')
        .borderRadius(8)
        .margin({ bottom: 10 })
      } else if (this.foldStatus === display.FoldStatus.FOLD_STATUS_HALF_FOLDED) {
        Column() {
          Text('半折叠态 (Half-Folded/Hover)')
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .margin({ bottom: 5 })
          Text('设备处于半折叠状态')
            .fontSize(12)
            .fontColor('#666666')
            .margin({ bottom: 5 })
          Text('适用于上展示下交互的免手持场景')
            .fontSize(12)
            .fontColor('#666666')
        }
        .width('100%')
        .padding(10)
        .backgroundColor('#E3F2FD')
        .borderRadius(8)
        .margin({ bottom: 10 })
      } else {
        Text('未知状态或非折叠屏设备')
          .fontSize(12)
          .fontColor('#666666')
      }

      Text('使用场景:')
        .fontSize(14)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 10, bottom: 5 })

      Text('• 展开态：大屏浏览、文档编辑、多任务处理')
        .fontSize(12)
        .fontColor('#666666')
        .margin({ bottom: 5 })

      Text('• 折叠态：便携模式、单手操作')
        .fontSize(12)
        .fontColor('#666666')
        .margin({ bottom: 5 })

      Text('• 半折叠态：上下分区交互、免手持操作')
        .fontSize(12)
        .fontColor('#666666')
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}
