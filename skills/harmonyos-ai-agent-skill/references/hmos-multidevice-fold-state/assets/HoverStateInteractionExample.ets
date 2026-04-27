/**
 * HoverStateInteractionExample.ets
 *
 * 官方方法模板（官方 API 模板资产）：
 * - 折叠状态：display.getFoldStatus() + foldStatusChange
 * - 悬停布局：FolderStack / FoldSplitContainer
 * - 方向策略：window.setPreferredOrientation(...) + 退出恢复 AUTO_ROTATION
 *
 * 说明：本文件仅提供工程接入模板，不引入机型假设与经验比例硬编码。
 */
import display from '@ohos.display';
import { window } from '@kit.ArkUI';

@Entry
@Component
struct HoverStateInteractionExample {
  @State private isHover: boolean = false;
  @State private useSplitContainer: boolean = false;
  private foldStatusCallback?: (status: display.FoldStatus) => void;

  aboutToAppear() {
    this.refreshFoldStatus();
    this.foldStatusCallback = (status: display.FoldStatus) => {
      this.isHover = (status === display.FoldStatus.FOLD_STATUS_HALF_FOLDED);
    };
    display.on('foldStatusChange', this.foldStatusCallback);
  }

  aboutToDisappear() {
    if (this.foldStatusCallback) {
      display.off('foldStatusChange', this.foldStatusCallback);
    }
    // 页面退出时恢复自动旋转（官方推荐做法）
    window.getLastWindow(getContext(this)).setPreferredOrientation(window.Orientation.AUTO_ROTATION);
  }

  private refreshFoldStatus() {
    const status = display.getFoldStatus();
    this.isHover = (status === display.FoldStatus.FOLD_STATUS_HALF_FOLDED);
  }

  @Builder
  private upperArea() {
    Column() {
      Text('Upper / Primary Content')
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  private lowerArea() {
    Column() {
      Text('Lower / Actions')
    }
    .width('100%')
    .height('100%')
  }

  build() {
    Column() {
      if (this.isHover) {
        if (this.useSplitContainer) {
          FoldSplitContainer({
            primary: () => this.upperArea(),
            secondary: () => this.lowerArea()
          })
        } else {
          FolderStack({ upperItems: ['upper'] }) {
            Column() { this.upperArea() }.id('upper')
            this.lowerArea()
          }
        }
      } else {
        // 非悬停态按常规单屏/断点布局处理
        Column() {
          Text('Normal Layout')
        }
        .width('100%')
        .height('100%')
      }
    }
    .width('100%')
    .height('100%')
  }
}
