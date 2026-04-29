import window from '@ohos.window';

@Entry
@Component
struct AvoidAreaExample {
  @State statusBarHeight: number = 0;
  @State navBarHeight: number = 0;
  private windowClass: window.Window | null = null;

  aboutToAppear() {
    window.getLastWindow(this.getUIContext().getHostContext(), (err, win) => {
      if (err.code !== 0) {
        console.error('获取窗口失败:', err);
        return;
      }
      
      this.windowClass = win;
      
      this.updateAvoidAreas(win);
      
      win.on('avoidAreaChange', (data) => {
        if (data.type === window.AvoidAreaType.TYPE_SYSTEM) {
          this.statusBarHeight = this.getUIContext().px2vp(data.area.topRect.height);
        } else if (data.type === window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR) {
          this.navBarHeight = this.getUIContext().px2vp(data.area.bottomRect.height);
        }
      });
    });
  }

  aboutToDisappear() {
    if (this.windowClass) {
      this.windowClass.off('avoidAreaChange');
    }
  }

  private updateAvoidAreas(win: window.Window) {
    const statusBarArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
    const navBarArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
    
    this.statusBarHeight = this.getUIContext().px2vp(statusBarArea.topRect.height);
    this.navBarHeight = this.getUIContext().px2vp(navBarArea.bottomRect.height);
  }

  build() {
    Column() {
      Text(`状态栏高度: ${this.statusBarHeight}`)
      Text(`导航栏高度: ${this.navBarHeight}`)
    }
  }
}
