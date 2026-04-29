import window from '@ohos.window';

@Entry
@Component
struct KeyboardAvoidanceExample {
  @State keyboardHeight: number = 0;
  private windowClass: window.Window | null = null;

  aboutToAppear() {
    window.getLastWindow(this.getUIContext().getHostContext(), (err, win) => {
      if (err.code !== 0) {
        console.error('获取窗口失败:', err);
        return;
      }

      this.windowClass = win;
      this.updateKeyboardArea(win);

      win.on('avoidAreaChange', (data: window.AvoidAreaInfo) => {
        if (data.type === window.AvoidAreaType.TYPE_KEYBOARD) {
          this.keyboardHeight = px2vp(data.area.bottomRect.height);
        }
      });
    });
  }

  aboutToDisappear() {
    if (this.windowClass) {
      this.windowClass.off('avoidAreaChange');
    }
  }

  private updateKeyboardArea(win: window.Window) {
    const keyboardArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_KEYBOARD);
    this.keyboardHeight = px2vp(keyboardArea.bottomRect.height);
  }

  build() {
    Column() {
      Text('视频详情')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .width('100%')

      Text('上方内容区保持稳定，底部输入区随键盘高度上移。')
        .fontSize(14)
        .fontColor('#666666')
        .width('100%')
        .margin({ top: 8, bottom: 16 })

      Column() {
        Text('评论 1：悬停态下保持内容和输入区职责分离')
        Text('评论 2：键盘弹出时仅提升输入区，不让列表整体跳动')
          .margin({ top: 12 })
        Text('评论 3：焦点切换后保持底部操作区可见')
          .margin({ top: 12 })
      }
      .width('100%')
      .layoutWeight(1)
      .padding(16)
      .borderRadius(16)
      .backgroundColor('#F3F5F7')

      Row() {
        TextInput({ placeholder: '写评论' })
          .layoutWeight(1)
          .height(44)

        Button('发送')
          .height(44)
          .margin({ left: 12 })
      }
      .width('100%')
      .padding(12)
      .borderRadius(20)
      .backgroundColor('#FFFFFF')
      .margin({ top: 16 })

      Text(`键盘高度: ${this.keyboardHeight.toFixed(0)}vp`)
        .fontSize(12)
        .fontColor('#999999')
        .width('100%')
        .margin({ top: 8 })
    }
    .width('100%')
    .height('100%')
    .padding({
      top: 16,
      left: 16,
      right: 16,
      bottom: this.keyboardHeight > 0 ? this.keyboardHeight : 16
    })
  }
}
