# 视频类应用横竖屏切换与短视频自适应旋转


## 目录

1. [视频类应用横竖屏切换](#视频类应用横竖屏切换)
2. [短视频自适应旋转](#短视频自适应旋转)
3. [屏幕锁定功能](#屏幕锁定功能)
4. [横竖屏切换性能优化](#横竖屏切换性能优化)

---

## 视频类应用横竖屏切换

### 核心需求

视频播放应用的典型场景：首页竖屏展示，视频播放页横屏全屏播放。需要满足：

1. 应用跟随传感器旋转
2. 受控制中心旋转锁定按钮控制
3. 支持用户在应用页面中手动切换（如点击全屏按钮）

### 推荐旋转策略

| 场景 | 推荐策略 | 枚举值 |
|------|---------|--------|
| 进入视频全屏 | `USER_ROTATION_LANDSCAPE` | 14 |
| 退出视频全屏 | `USER_ROTATION_PORTRAIT` | 13 |
| 锁定到横屏 | `AUTO_ROTATION_LANDSCAPE` | 7 |
| 恢复三向旋转 | `AUTO_ROTATION_UNSPECIFIED` | 12 |

`USER_ROTATION_*` 系列策略的特点：调用时临时旋转到指定方向，之后跟随传感器自动旋转，且受控制中心旋转开关控制。

### 完整实现

#### 1. module.json5 配置

```json
{
  "module": {
    "abilities": [
      {
        "name": "EntryAbility",
        "orientation": "follow_desktop"
      }
    ]
  }
}
```

#### 2. 视频播放组件

```arkts
import { window, display } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';
import { BusinessError } from '@kit.BasicServicesKit';

@Component
export struct VideoPlayView {
  context = this.getUIContext()?.getHostContext() as common.UIAbilityContext;
  private windowClass = this.context.windowStage.getMainWindowSync();
  @State isLandscape: boolean = false;
  @State xComponentWidth: number = 0;
  @State xComponentHeight: number = 0;
  private aspect: number = 16 / 9;
  private sizeCallback: Callback<window.Size> | null = null;

  aboutToAppear(): void {
    const displayInfo = display.getDefaultDisplaySync();
    const uiContext = this.getUIContext();
    this.xComponentWidth = uiContext.px2vp(displayInfo.width);
    this.xComponentHeight = uiContext.px2vp(displayInfo.width * this.aspect);

    // 保存回调引用，确保 aboutToDisappear 时能正确取消
    this.sizeCallback = (size: window.Size) => {
      const viewWidth = uiContext.px2vp(size.width);
      const viewHeight = uiContext.px2vp(size.height);

      if (viewWidth > viewHeight) {
        // 横屏：全屏播放
        this.isLandscape = true;
        this.xComponentWidth = viewHeight / this.aspect;
        this.xComponentHeight = viewHeight;
        this.windowClass.setSpecificSystemBarEnabled('navigationIndicator', false);
      } else {
        // 竖屏：非全屏
        this.isLandscape = false;
        this.xComponentHeight = viewWidth * this.aspect;
        this.xComponentWidth = viewWidth;
        this.windowClass.setSpecificSystemBarEnabled('navigationIndicator', true);
      }
    };
    this.windowClass.on('windowSizeChange', this.sizeCallback);
  }

  aboutToDisappear(): void {
    if (this.sizeCallback) {
      this.windowClass.off('windowSizeChange', this.sizeCallback);
      this.sizeCallback = null;
    }
  }

  setOrientation(orientation: number) {
    this.windowClass.setPreferredOrientation(orientation).catch((err: BusinessError) => {
      console.error('setOrientation failed:', JSON.stringify(err));
    });
  }

  // 判断是否为折叠屏展开态/悬停态
  isExpandedOrHalfFolded(): boolean {
    return display.getFoldStatus() === display.FoldStatus.FOLD_STATUS_EXPANDED ||
      display.getFoldStatus() === display.FoldStatus.FOLD_STATUS_HALF_FOLDED;
  }

  build() {
    Stack() {
      XComponent({ id: 'video_player_id', type: XComponentType.SURFACE })
        .width(this.xComponentWidth)
        .height(this.xComponentHeight)

      // 全屏按钮
      Image($r('app.media.icon_zoom_in'))
        .onClick(() => {
          if (this.isExpandedOrHalfFolded()) {
            // 折叠屏展开态：不旋转，直接调整播窗大小
            this.isLandscape = true;
          } else {
            this.setOrientation(window.Orientation.USER_ROTATION_LANDSCAPE);
          }
        })

      // 返回按钮
      Image($r('app.media.icon_back'))
        .onClick(() => {
          this.setOrientation(window.Orientation.USER_ROTATION_PORTRAIT);
        })
    }
  }
}
```

---

## 短视频自适应旋转

### 方式一：使用 adaptive_video 三方库（推荐）

`adaptive_video` 三方库提供了完整的短视频自适应沉浸 + 自适应旋转方案，自动处理多设备差异。

#### 安装

```bash
ohpm install @hadss/adaptive_video
```

#### 核心能力

| 能力 | 说明 |
|------|------|
| 自适应沉浸 | 根据设备屏幕尺寸、视频宽高比自动计算沉浸式布局 |
| 自适应旋转 | 根据设备类型、屏幕区间、视频类型自动设置旋转策略 |
| 高阶组件 | `AdaptiveVideoComponent` 封装播放器+沉浸+旋转 |

#### 自适应旋转规则

| 屏幕区间 | 视频类型 | 全屏 | 旋转策略 |
|---------|---------|------|---------|
| Small_Portrait / Medium_Landscape | 横向视频 | 全屏 | `USER_ROTATION_LANDSCAPE` / `USER_ROTATION_LANDSCAPE_INVERTED` |
| Small_Portrait / Medium_Landscape | 竖向视频 | 全屏 | `PORTRAIT` |
| Medium_Portrait 及以上 | 任意 | 任意 | `AUTO_ROTATION_UNSPECIFIED` |

#### 使用示例

```arkts
import { AdaptiveRotation, AdaptiveImmersion, ScreenModeNotifier, ScreenMode } from '@hadss/adaptive_video';

const adaptiveRotation = AdaptiveRotation.getInstance();
const adaptiveImmersion = AdaptiveImmersion.getInstance();
const screenModeNotifier = ScreenModeNotifier.getInstance();

@Component
export struct AdaptiveAVPlayer {
  aboutToAppear(): void {
    adaptiveRotation.init(this.context);
    adaptiveImmersion.init(this.context);
    screenModeNotifier.init(this.context);
    screenModeNotifier.onScreenModeChange(this.onScreenModeChange);
  }

  aboutToDisappear(): void {
    screenModeNotifier.offScreenModeChange(this.onScreenModeChange);
  }

  // 非全屏播放
  private async changePortraitVideo() {
    adaptiveRotation.setOrientationNotFullScreen({
      width: this.videoWidth, height: this.videoHeight
    });
  }

  // 全屏播放
  private async setOrientationFullScreen() {
    adaptiveRotation.setOrientationFullScreen({
      width: this.videoWidth, height: this.videoHeight
    });
  }

  private onScreenModeChange = (data: string) => {
    if (data === ScreenMode.FULL_SCREEN) {
      this.setOrientationFullScreen();
    } else {
      this.changePortraitVideo();
    }
  };
}
```


### 方式二：手动实现短视频旋转

不使用三方库时，可手动根据断点和视频方向设置旋转策略：

```arkts
import { window, display } from '@kit.ArkUI';
import { deviceInfo } from '@kit.BasicServicesKit';

function setShortVideoOrientation(
  uiContext: UIContext,
  windowClass: window.Window,
  isFullScreen: boolean,
  videoWidth: number,
  videoHeight: number
): void {
  // 使用系统断点 API 判断设备类型
  const widthBp = uiContext.getWindowWidthBreakpoint();
  const heightBp = uiContext.getWindowHeightBreakpoint();

  const isLandscapeVideo = videoWidth > videoHeight;

  // PC/2in1/TV/车机不支持旋转
  if (deviceInfo.deviceType === '2in1' || deviceInfo.deviceType === 'tv') {
    return;
  }

  // 直板机竖屏：横向 sm + 纵向 lg
  const isBarPhone = widthBp === WidthBreakpoint.WIDTH_SM && heightBp === HeightBreakpoint.HEIGHT_LG;

  if (isBarPhone) {
    // 直板机：竖向视频固定竖屏，横向视频全屏时旋转横屏
    if (isLandscapeVideo && isFullScreen) {
      windowClass.setPreferredOrientation(window.Orientation.USER_ROTATION_LANDSCAPE);
    } else {
      windowClass.setPreferredOrientation(window.Orientation.PORTRAIT);
    }
  } else {
    // 大屏设备（折叠屏展开态、平板）：自动旋转
    windowClass.setPreferredOrientation(window.Orientation.AUTO_ROTATION_UNSPECIFIED);
  }
}

> 注意：此处使用 `deviceInfo.deviceType` 判断 PC/TV 等不支持旋转的设备是合理的（非布局判断）。判断屏幕大小的部分使用系统断点 API 替代了手动像素计算。
```

---

## 屏幕锁定功能

视频全屏播放时，支持锁定屏幕方向，避免误触：

- **锁定时**: 设置 `AUTO_ROTATION_LANDSCAPE`，支持横屏/反向横屏旋转，不可旋转为竖屏
- **解锁时**: 设置 `AUTO_ROTATION_UNSPECIFIED`，恢复三向旋转（横屏、竖屏、反向横屏），受控制中心控制

```arkts
import { window } from '@kit.ArkUI';

// 锁定/解锁
if (this.isVideoLock) {
  this.setOrientation(window.Orientation.AUTO_ROTATION_LANDSCAPE);
} else {
  this.setOrientation(window.Orientation.AUTO_ROTATION_UNSPECIFIED);
}
```

### 监听控制中心旋转锁定状态

```arkts
import { settings } from '@kit.BasicServicesKit';

// 监听控制中心旋转开关变化
settings.registerKeyObserver(this.context, settings.general.ACCELEROMETER_ROTATION_STATUS,
  settings.domainName.DEVICE_SHARED, () => {
    this.orientationLockState = settings.getValueSync(
      this.context,
      settings.general.ACCELEROMETER_ROTATION_STATUS,
      settings.domainName.DEVICE_SHARED
    );
  });
```

---

## 横竖屏切换性能优化


### 1. 使用自定义组件冻结

旋转时仅需要更新播放区域，其他组件可冻结避免不必要的 UI 更新：

```arkts
@Component({ freezeWhenInactive: true })
struct VideoDetailView {
  build() {
    Scroll() {
      // 视频下方的详情内容，旋转时不需更新
    }
  }
}
```

### 2. 对图片使用 autoResize

将图片裁剪到合适大小，减少内存占用：

```arkts
Image(imageSrc)
  .width('100%')
  .height('100%')
  .autoResize(true) // 原图 1920×1080，显示区域 200×100 时自动降采样
  .objectFit(ImageFit.Fill)
```

### 3. 避免耗时操作

排查页面是否存在冗余的 `OnAreaChange` 事件、`blur` 模糊或 `linearGradient` 属性，这些在旋转时会增加布局耗时。
