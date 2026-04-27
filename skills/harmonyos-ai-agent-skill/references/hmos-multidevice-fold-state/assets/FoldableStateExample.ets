import { window } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';

class FoldableStateManager {
  currentBreakpoint: string = 'sm';
  isFolded: boolean = true;
  private windowClass: window.Window | null = null;

  async aboutToAppear(context: common.UIAbilityContext) {
    try {
      this.windowClass = await window.getLastWindow(context);
      if (this.windowClass !== null) {
        const properties = this.windowClass.getWindowProperties();
        this.updateState(properties.windowRect.width, properties.windowRect.height);

        this.windowClass.on('windowSizeChange', (newWindowSize: window.Size) => {
          this.updateState(newWindowSize.width, newWindowSize.height);
        });
      }
    } catch (err) {
      console.error('Failed to get window:', err);
    }
  }

  private updateState(width: number, height: number) {
    const area = width * height;

    if (area < 600 * 600) {
      this.currentBreakpoint = 'sm';
      this.isFolded = true;
    } else if (area < 840 * 600) {
      this.currentBreakpoint = 'md';
      this.isFolded = false;
    } else {
      this.currentBreakpoint = 'lg';
      this.isFolded = false;
    }
  }
}

@Entry
@Component
struct AdaptiveLayout {
  @State currentBreakpoint: string = 'sm';
  @State windowWidth: number = 0;
  @State windowHeight: number = 0;

  async aboutToAppear() {
    try {
      let context = this.getUIContext().getHostContext() as common.UIAbilityContext;
      let windowClass = await window.getLastWindow(context);
      let properties = windowClass.getWindowProperties();
      this.windowWidth = properties.windowRect.width;
      this.windowHeight = properties.windowRect.height;
      this.currentBreakpoint = this.calculateBreakpoint(this.windowWidth);

      windowClass.on('windowSizeChange', (newSize: window.Size) => {
        this.windowWidth = newSize.width;
        this.windowHeight = newSize.height;
        let newBreakpoint = this.calculateBreakpoint(newSize.width);
        if (this.currentBreakpoint !== newBreakpoint) {
          this.currentBreakpoint = newBreakpoint;
        }
      });
    } catch (err) {
      console.error('Failed to get window:', err);
    }
  }

  private calculateBreakpoint(width: number): string {
    if (width < 600) return 'sm';
    if (width < 840) return 'md';
    if (width < 1440) return 'lg';
    return 'xl';
  }

  build() {
    Column() {
      if (this.currentBreakpoint === 'sm') {
        PhoneLayout()
      } else if (this.currentBreakpoint === 'md') {
        FoldableLayout()
      } else {
        TabletLayout()
      }
    }
  }
}

@Component
struct PhoneLayout {
  build() {
    Column() {
      Text('手机布局')
        .fontSize(24)
    }
    .width('100%')
    .height('100%')
  }
}

@Component
struct FoldableLayout {
  build() {
    Column() {
      Text('折叠屏展开态布局')
        .fontSize(24)
    }
    .width('100%')
    .height('100%')
  }
}

@Component
struct TabletLayout {
  build() {
    Column() {
      Text('平板布局')
        .fontSize(24)
    }
    .width('100%')
    .height('100%')
  }
}
