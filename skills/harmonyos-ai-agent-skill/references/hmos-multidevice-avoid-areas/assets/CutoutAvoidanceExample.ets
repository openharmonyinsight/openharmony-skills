import display from '@ohos.display';

async function getCutoutInfo() {
   try {
    const displayClass = display.getDefaultDisplaySync();
    const res = await displayClass.getCutoutInfo();
    return res.boundingRects;  // 返回挖孔区域的矩形数组
  }catch (e) {
    return [];
  }
}

// 使用示例
@Entry
@Component
struct CutoutAvoidanceExample {
  @State cutoutRects: display.Rect[] = [];
  @State topMargin: number = 0;

  async aboutToAppear() {
    this.cutoutRects = await getCutoutInfo();
    // 计算顶部避让距离
    if (this.cutoutRects.length > 0) {
      const topCutout = this.cutoutRects.find(rect => rect.top === 0);
      if (topCutout) {
        this.topMargin = this.getUIContext().px2vp(topCutout.height);
      }
    }
  }

  build() {
    Column() {
      // 顶部内容，避让挖孔区域
      Text('重要内容')
        .margin({ top: this.topMargin })
    }
    .width('100%')
    .height('100%')
  }
}
