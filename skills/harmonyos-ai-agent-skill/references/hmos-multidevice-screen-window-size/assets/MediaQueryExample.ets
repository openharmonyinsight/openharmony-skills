/**
 * 媒体查询完整示例
 * 
 * 功能:
 * 1. 监听窗口宽度变化
 * 2. 监听屏幕方向变化
 * 3. 监听深色模式变化
 * 4. 监听设备类型
 * 5. 复杂条件组合
 */

import mediaquery from '@ohos.mediaquery';
import { UIContext } from '@kit.ArkUI';

@Entry
@Component
struct MediaQueryExample {
  private uiContext: UIContext = this.getUIContext();

  // 窗口宽度监听器
  private widthSmListener: mediaquery.MediaQueryListener = 
    this.uiContext.getMediaQuery().matchMediaSync('(min-width: 320vp) and (max-width: 599vp)');
  private widthMdListener: mediaquery.MediaQueryListener = 
    this.uiContext.getMediaQuery().matchMediaSync('(min-width: 600vp) and (max-width: 839vp)');
  private widthLgListener: mediaquery.MediaQueryListener = 
    this.uiContext.getMediaQuery().matchMediaSync('(min-width: 840vp)');
  
  // 屏幕方向监听器
  private orientationListener: mediaquery.MediaQueryListener = 
    this.uiContext.getMediaQuery().matchMediaSync('(orientation: portrait)');
  
  // 深色模式监听器
  private darkModeListener: mediaquery.MediaQueryListener = 
    this.uiContext.getMediaQuery().matchMediaSync('(dark-mode: true)');
  
  // 设备类型监听器
  private phoneListener: mediaquery.MediaQueryListener = 
    this.uiContext.getMediaQuery().matchMediaSync('(device-type: phone)');
  private tabletListener: mediaquery.MediaQueryListener = 
    this.uiContext.getMediaQuery().matchMediaSync('(device-type: tablet)');

  // 状态变量
  @State currentBreakpoint: string = 'sm';
  @State isPortrait: boolean = true;
  @State isDarkMode: boolean = false;
  @State deviceType: string = 'unknown';
  @State changeLog: string[] = [];

  /**
   * 组件即将出现
   */
  aboutToAppear() {
    // 初始化状态
    this.updateBreakpoint();
    this.isPortrait = this.orientationListener.matches;
    this.isDarkMode = this.darkModeListener.matches;
    this.updateDeviceType();

    // 注册窗口宽度监听
    this.widthSmListener.on('change', () => {
      this.updateBreakpoint();
      this.addLog('窗口宽度变化');
    });
    this.widthMdListener.on('change', () => {
      this.updateBreakpoint();
      this.addLog('窗口宽度变化');
    });
    this.widthLgListener.on('change', () => {
      this.updateBreakpoint();
      this.addLog('窗口宽度变化');
    });

    // 注册屏幕方向监听
    this.orientationListener.on('change', (result) => {
      this.isPortrait = result.matches;
      this.addLog(`屏幕方向: ${this.isPortrait ? '竖屏' : '横屏'}`);
    });

    // 注册深色模式监听
    this.darkModeListener.on('change', (result) => {
      this.isDarkMode = result.matches;
      this.addLog(`主题: ${this.isDarkMode ? '深色' : '浅色'}`);
    });

    // 注册设备类型监听
    this.phoneListener.on('change', () => {
      this.updateDeviceType();
      this.addLog('设备类型变化');
    });
    this.tabletListener.on('change', () => {
      this.updateDeviceType();
      this.addLog('设备类型变化');
    });

    this.addLog('媒体查询初始化完成');
  }

  /**
   * 组件即将消失
   */
  aboutToDisappear() {
    // 注销所有监听器
    this.widthSmListener.off('change');
    this.widthMdListener.off('change');
    this.widthLgListener.off('change');
    this.orientationListener.off('change');
    this.darkModeListener.off('change');
    this.phoneListener.off('change');
    this.tabletListener.off('change');
  }

  /**
   * 更新断点
   */
  private updateBreakpoint() {
    if (this.widthLgListener.matches) {
      this.currentBreakpoint = 'lg';
    } else if (this.widthMdListener.matches) {
      this.currentBreakpoint = 'md';
    } else {
      this.currentBreakpoint = 'sm';
    }
  }

  /**
   * 更新设备类型
   */
  private updateDeviceType() {
    if (this.phoneListener.matches) {
      this.deviceType = 'phone';
    } else if (this.tabletListener.matches) {
      this.deviceType = 'tablet';
    } else {
      this.deviceType = 'other';
    }
  }

  /**
   * 添加日志
   */
  private addLog(message: string) {
    const timestamp = new Date().toLocaleTimeString();
    this.changeLog.unshift(`[${timestamp}] ${message}`);
    
    // 只保留最近20条日志
    if (this.changeLog.length > 20) {
      this.changeLog = this.changeLog.slice(0, 20);
    }
  }

  /**
   * 获取主题背景色
   */
  private getBackgroundColor(): string {
    return this.isDarkMode ? '#1E1E1E' : '#F5F5F5';
  }

  /**
   * 获取主题文字颜色
   */
  private getTextColor(): string {
    return this.isDarkMode ? '#FFFFFF' : '#000000';
  }

  /**
   * 获取次要文字颜色
   */
  private getSecondaryTextColor(): string {
    return this.isDarkMode ? '#CCCCCC' : '#666666';
  }

  /**
   * 获取卡片背景色
   */
  private getCardBackgroundColor(): string {
    return this.isDarkMode ? '#2D2D2D' : '#FFFFFF';
  }

  /**
   * 状态信息卡片
   */
  @Builder
  StatusCard() {
    Column() {
      Text('当前状态')
        .fontSize('18fp')
        .fontWeight(FontWeight.Bold)
        .fontColor(this.getTextColor())
        .margin({ bottom: 12 })

      // 断点信息
      Row() {
        Text('断点:')
          .fontSize('14fp')
          .fontColor(this.getSecondaryTextColor())
          .width(80)
        Text(this.currentBreakpoint)
          .fontSize('14fp')
          .fontWeight(FontWeight.Medium)
          .fontColor(this.getTextColor())
      }
      .width('100%')
      .margin({ bottom: 8 })

      // 屏幕方向
      Row() {
        Text('屏幕方向:')
          .fontSize('14fp')
          .fontColor(this.getSecondaryTextColor())
          .width(80)
        Text(this.isPortrait ? '竖屏' : '横屏')
          .fontSize('14fp')
          .fontWeight(FontWeight.Medium)
          .fontColor(this.getTextColor())
      }
      .width('100%')
      .margin({ bottom: 8 })

      // 主题
      Row() {
        Text('主题:')
          .fontSize('14fp')
          .fontColor(this.getSecondaryTextColor())
          .width(80)
        Text(this.isDarkMode ? '深色模式' : '浅色模式')
          .fontSize('14fp')
          .fontWeight(FontWeight.Medium)
          .fontColor(this.getTextColor())
      }
      .width('100%')
      .margin({ bottom: 8 })

      // 设备类型
      Row() {
        Text('设备类型:')
          .fontSize('14fp')
          .fontColor(this.getSecondaryTextColor())
          .width(80)
        Text(this.deviceType)
          .fontSize('14fp')
          .fontWeight(FontWeight.Medium)
          .fontColor(this.getTextColor())
      }
      .width('100%')
    }
    .width('100%')
    .padding(16)
    .backgroundColor(this.getCardBackgroundColor())
    .borderRadius(8)
  }

  /**
   * 监听器信息卡片
   */
  @Builder
  ListenerCard() {
    Column() {
      Text('监听器状态')
        .fontSize('18fp')
        .fontWeight(FontWeight.Bold)
        .fontColor(this.getTextColor())
        .margin({ bottom: 12 })

      // 窗口宽度监听器
      this.ListenerItem('widthSmListener', this.widthSmListener.matches, '(min-width: 320vp) and (max-width: 599vp)');
      this.ListenerItem('widthMdListener', this.widthMdListener.matches, '(min-width: 600vp) and (max-width: 839vp)');
      this.ListenerItem('widthLgListener', this.widthLgListener.matches, '(min-width: 840vp)');

      Divider().margin({ top: 8, bottom: 8 })

      // 其他监听器
      this.ListenerItem('orientationListener', this.orientationListener.matches, '(orientation: portrait)');
      this.ListenerItem('darkModeListener', this.darkModeListener.matches, '(dark-mode: true)');
      this.ListenerItem('phoneListener', this.phoneListener.matches, '(device-type: phone)');
      this.ListenerItem('tabletListener', this.tabletListener.matches, '(device-type: tablet)');
    }
    .width('100%')
    .padding(16)
    .backgroundColor(this.getCardBackgroundColor())
    .borderRadius(8)
  }

  /**
   * 监听器项
   */
  @Builder
  ListenerItem(name: string, matches: boolean, condition: string) {
    Column() {
      Row() {
        Text(name)
          .fontSize('14fp')
          .fontWeight(FontWeight.Medium)
          .fontColor(this.getTextColor())
          .layoutWeight(1)
        
        Text(matches ? '✅ 匹配' : '❌ 不匹配')
          .fontSize('12fp')
          .fontColor(matches ? '#52C41A' : '#FF4D4F')
          .padding({ left: 8, right: 8, top: 2, bottom: 2 })
          .backgroundColor(matches ? '#F6FFED' : '#FFF1F0')
          .borderRadius(4)
      }
      .width('100%')

      Text(condition)
        .fontSize('12fp')
        .fontColor(this.getSecondaryTextColor())
        .margin({ top: 4 })
    }
    .width('100%')
    .margin({ bottom: 8 })
  }

  /**
   * 变化日志卡片
   */
  @Builder
  ChangeLogCard() {
    Column() {
      Row() {
        Text('变化日志')
          .fontSize('18fp')
          .fontWeight(FontWeight.Bold)
          .fontColor(this.getTextColor())
          .layoutWeight(1)
        
        Button('清空')
          .fontSize('12fp')
          .height(28)
          .onClick(() => {
            this.changeLog = [];
          })
      }
      .width('100%')
      .margin({ bottom: 12 })

      if (this.changeLog.length === 0) {
        Text('暂无日志')
          .fontSize('14fp')
          .fontColor(this.getSecondaryTextColor())
          .textAlign(TextAlign.Center)
          .width('100%')
          .padding({ top: 20, bottom: 20 })
      } else {
        List({ space: 4 }) {
          ForEach(this.changeLog, (log: string, index: number) => {
            ListItem() {
              Text(log)
                .fontSize('12fp')
                .fontColor(this.getSecondaryTextColor())
                .width('100%')
                .padding(8)
                .backgroundColor(this.isDarkMode ? '#3A3A3A' : '#F0F0F0')
                .borderRadius(4)
            }
          })
        }
        .width('100%')
        .height(200)
      }
    }
    .width('100%')
    .padding(16)
    .backgroundColor(this.getCardBackgroundColor())
    .borderRadius(8)
  }

  /**
   * 响应式布局示例
   */
  @Builder
  ResponsiveLayoutExample() {
    Column() {
      Text('响应式布局示例')
        .fontSize('18fp')
        .fontWeight(FontWeight.Bold)
        .fontColor(this.getTextColor())
        .margin({ bottom: 12 })

      if (this.isPortrait) {
        // 竖屏布局: 上下排列
        Column({ space: 12 }) {
          ForEach([1, 2, 3, 4], (item: number) => {
            Text(`Item ${item}`)
              .width('100%')
              .height(80)
              .backgroundColor('#007DFF')
              .textAlign(TextAlign.Center)
              .borderRadius(8)
              .fontColor('#FFFFFF')
          })
        }
        .width('100%')
      } else {
        // 横屏布局: 左右排列
        Row({ space: 12 }) {
          ForEach([1, 2, 3, 4], (item: number) => {
            Text(`Item ${item}`)
              .layoutWeight(1)
              .height(80)
              .backgroundColor('#007DFF')
              .textAlign(TextAlign.Center)
              .borderRadius(8)
              .fontColor('#FFFFFF')
          })
        }
        .width('100%')
      }
    }
    .width('100%')
    .padding(16)
    .backgroundColor(this.getCardBackgroundColor())
    .borderRadius(8)
  }

  build() {
    Scroll() {
      Column({ space: 16 }) {
        // 标题
        Text('媒体查询示例')
          .fontSize('24fp')
          .fontWeight(FontWeight.Bold)
          .fontColor(this.getTextColor())
          .margin({ top: 16 })

        // 状态信息卡片
        this.StatusCard()

        // 监听器信息卡片
        this.ListenerCard()

        // 变化日志卡片
        this.ChangeLogCard()

        // 响应式布局示例
        this.ResponsiveLayoutExample()
      }
      .width('100%')
      .padding({ left: 16, right: 16, bottom: 16 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor(this.getBackgroundColor())
  }
}





