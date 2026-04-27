import window from '@ohos.window';

@Entry
@Component
struct CutoutAvoidanceExample {
  @State avoidArea: window.AvoidArea = {
    topRect: { left: 0, top: 0, width: 0, height: 0 },
    bottomRect: { left: 0, top: 0, width: 0, height: 0 },
    leftRect: { left: 0, top: 0, width: 0, height: 0 },
    rightRect: { left: 0, top: 0, width: 0, height: 0 },
    visible: false
  };

  aboutToAppear() {
    window.getLastWindow(this.getUIContext().getHostContext(), (err, win) => {
      if (err.code !== 0) {
        console.error('获取窗口失败:', err);
        return;
      }
      
      // 获取刘海/挖孔避让区域
      this.avoidArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_CUTOUT);
    });
  }

  build() {
    Column() {
      // 根据避让区域设置padding
      Column() {
        Text('内容区域')
      }
      .padding({
        top: this.avoidArea.topRect.height > 0 ? this.avoidArea.topRect.height : 0,
        bottom: this.avoidArea.bottomRect.height > 0 ? this.avoidArea.bottomRect.height : 0,
        left: this.avoidArea.leftRect.width > 0 ? this.avoidArea.leftRect.width : 0,
        right: this.avoidArea.rightRect.width > 0 ? this.avoidArea.rightRect.width : 0
      })
    }
    .width('100%')
    .height('100%')
  }
}
