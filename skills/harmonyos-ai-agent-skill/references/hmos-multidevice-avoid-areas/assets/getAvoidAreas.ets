import window from '@ohos.window';

@Entry
@Component
struct GetAvoidAreasExample {
  aboutToAppear() {
    this.getAvoidAreas();
  }

  getAvoidAreas() {
    window.getLastWindow(this.getUIContext().getHostContext(), (err, win) => {
      if (err.code !== 0) {
        console.error('获取窗口失败:', err);
        return;
      }
      
      // 获取状态栏避让区域
      const statusBarArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
      console.log('状态栏高度(vp):', this.getUIContext().px2vp(statusBarArea.topRect.height));
      
      // 获取导航栏避让区域
      const navBarArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
      console.log('导航栏高度(vp):', this.getUIContext().px2vp(navBarArea.bottomRect.height));
      
      // 获取刘海屏避让区域
      const cutoutArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_CUTOUT);
      console.log('刘海屏高度(vp):', this.getUIContext().px2vp(cutoutArea.topRect.height));
    });
  }

  build() {
    Column() {
      Text('获取避让区域示例')
    }
  }
}
