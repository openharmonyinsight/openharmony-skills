import window from '@ohos.window';
import { BusinessError } from '@kit.BasicServicesKit';

@Entry
@Component
struct FullScreenLayoutExample {
  @State statusBarHeight: number = 0;
  @State navBarHeight: number = 0;

  async aboutToAppear() {
    window.getLastWindow(this.getUIContext().getHostContext(), (err, win) => {
      if (err.code !== 0) {
        console.error('获取窗口失败:', err);
        return;
      }
      
      win.setWindowLayoutFullScreen(true).then(() => {
        const statusBarArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
        const navBarArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
        this.statusBarHeight = this.getUIContext().px2vp(statusBarArea.topRect.height);
        this.navBarHeight = this.getUIContext().px2vp(navBarArea.bottomRect.height);
      }).catch((err: BusinessError) => {
        console.error('设置全屏布局失败:', err);
      });
    });
  }

  build() {
    Column() {
      // 内容需要手动避让
      Column() {
        Text('全屏内容')
      }
      .width('100%')
      .height('100%')
      .padding({ 
        top: this.statusBarHeight, 
        bottom: this.navBarHeight 
      })
    }
  }
}
