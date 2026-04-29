/**
 * 案例对照：图片设置固定大小，分屏场景下页面图片显示截断 vs 通过断点的变化来调整图片尺寸，在分屏下正常显示
 *
 * 场景：分屏模式下应用界面出现图片截断等问题
 * 根因：页面未根据断点动态调整布局和设置小窗口布局。
 *
 * 下面分别是正确案例（goodcase）和错误案例（badcase）
 */

// ==================== 正确案例（goodcase）====================
// 关键点：根据断点动态调整图片大小，避免小窗口显示不全而截断
// 效果：小窗下图片缩小，页面正常展示图片

// src/main/ets/entryability/EntryAbility.ets
import { AbilityConstant, ConfigurationConstant, UIAbility, Want } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { window } from '@kit.ArkUI';

const DOMAIN = 0x0000;

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    try {
      this.context.getApplicationContext().setColorMode(ConfigurationConstant.ColorMode.COLOR_MODE_NOT_SET);
    } catch (err) {
      hilog.error(DOMAIN, 'testTag', 'Failed to set colorMode. Cause: %{public}s', JSON.stringify(err));
    }
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onCreate');
  }

  onDestroy(): void {
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onDestroy');
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    // Main window is created, set main page for this ability
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onWindowStageCreate');

    windowStage.loadContent('pages/Index', (err) => {
      try {
        let mainWindow = windowStage.getMainWindowSync();
        mainWindow.on('windowSizeChange', (windowSize: window.Size) => {
          AppStorage.setOrCreate('WidthBreakpoint' ,mainWindow.getUIContext().getWindowWidthBreakpoint());
          AppStorage.setOrCreate('HeightBreakpoint' ,mainWindow.getUIContext().getWindowHeightBreakpoint());
        })
      } catch (error) {
        // TODO: Implement error handling.
      }
      if (err.code) {
        hilog.error(DOMAIN, 'testTag', 'Failed to load the content. Cause: %{public}s', JSON.stringify(err));
        return;
      }
      hilog.info(DOMAIN, 'testTag', 'Succeeded in loading the content.');
    });
  }

  onWindowStageDestroy(): void {
    // Main window is destroyed, release UI related resources
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onWindowStageDestroy');
  }

  onForeground(): void {
    // Ability has brought to foreground
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onForeground');
  }

  onBackground(): void {
    // Ability has back to background
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onBackground');
  }
}

// src/main/ets/pages/Index.ets
@Entry
@Component
struct Index {
  @StorageLink('WidthBreakpoint') currentWidthBreakpoint: WidthBreakpoint = WidthBreakpoint.WIDTH_SM;
  @StorageLink('HeightBreakpoint') currentHeightBreakpoint: HeightBreakpoint = HeightBreakpoint.HEIGHT_SM;

  build() {
    Column() {
      ForEach([1, 2, 3], (index: number) => {
        Image($r('app.media.background'))
          .height(this.currentWidthBreakpoint === WidthBreakpoint.WIDTH_SM  &&
            (this.currentHeightBreakpoint === HeightBreakpoint.HEIGHT_SM  ||
              this.currentHeightBreakpoint === HeightBreakpoint.HEIGHT_MD) ? 50 : 200)
          .aspectRatio(1)
      })
    }
    .height('100%')
    .width('100%')
    .justifyContent(FlexAlign.SpaceBetween)
  }
}

// ==================== 错误案例（badcase）====================
// 问题：图片设置了固定大小
// 效果：小窗下图片维持原大小，导致显示不全被截断

@Entry
@Component
struct Index {

  build() {
    Column() {
      ForEach([1, 2, 3], (index: number) => {
        Image($r('app.media.background'))
          .height(200)
          .aspectRatio(1)
      })
    }
    .height('100%')
    .width('100%')
    .justifyContent(FlexAlign.SpaceBetween)
  }
}