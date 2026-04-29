/**
 * SystemBreakpointExample.ets
 * 使用系统 WidthBreakpoint / HeightBreakpoint 枚举的推荐断点方案
 *
 * 优势：无需自定义断点常量，直接使用系统枚举，阈值与系统保持一致。
 * 适用场景：系统断点区间（xs/sm/md/lg/xl）满足需求时的首选方案。
 */

import window from '@ohos.window';
import { BreakpointType } from './BreakpointType';

/**
 * 系统断点工具类 - 封装系统断点枚举的初始化与监听
 *
 * 使用方式：
 * 1. 在 EntryAbility.onWindowStageCreate 中调用 SystemBreakpointManager.getInstance().init(uiContext, windowStage)
 * 2. 在页面组件中通过 @StorageProp('currentWidthBreakpoint') 获取当前横向断点
 * 3. 在 aboutToDisappear 或 Ability.onDestroy 中调用 destroy() 取消监听
 */
export class SystemBreakpointManager {
  private static instance: SystemBreakpointManager;
  private uiContext?: UIContext;
  private windowClass?: window.Window;
  private isInitialized: boolean = false;

  private constructor() {}

  static getInstance(): SystemBreakpointManager {
    if (!SystemBreakpointManager.instance) {
      SystemBreakpointManager.instance = new SystemBreakpointManager();
    }
    return SystemBreakpointManager.instance;
  }

  /**
   * 初始化：获取窗口实例，设置初始断点，注册窗口尺寸监听
   * @param uiContext - UI 上下文，用于调用 getWindowWidthBreakpoint / getWindowHeightBreakpoint
   * @param windowStage - 窗口舞台，用于获取主窗口实例
   */
  init(uiContext: UIContext, windowStage: window.WindowStage): void {
    if (this.isInitialized) {
      return;
    }

    this.uiContext = uiContext;

    try {
      this.windowClass = windowStage.getMainWindowSync();

      // 设置初始断点
      this.updateBreakpointToStorage();

      // 监听窗口尺寸变化
      this.windowClass.on('windowSizeChange', () => {
        this.updateBreakpointToStorage();
      });

      this.isInitialized = true;
    } catch (error) {
      console.error('SystemBreakpointManager init failed:', JSON.stringify(error));
    }
  }

  /**
   * 将当前系统断点写入 AppStorage
   */
  private updateBreakpointToStorage(): void {
    if (!this.uiContext) {
      return;
    }
    const widthBp: WidthBreakpoint = this.uiContext.getWindowWidthBreakpoint();
    const heightBp: HeightBreakpoint = this.uiContext.getWindowHeightBreakpoint();
    AppStorage.setOrCreate('currentWidthBreakpoint', widthBp);
    AppStorage.setOrCreate('currentHeightBreakpoint', heightBp);
  }

  /**
   * 销毁：取消监听
   */
  destroy(): void {
    if (this.windowClass) {
      this.windowClass.off('windowSizeChange');
    }
    this.isInitialized = false;
  }
}

/**
 * WidthBreakpoint 枚举值转字符串，用于与 BreakpointType.getValue() 配合
 */
export function widthBreakpointToStr(bp: WidthBreakpoint): string {
  switch (bp) {
    case WidthBreakpoint.WIDTH_XL:
      return 'xl';
    case WidthBreakpoint.WIDTH_LG:
      return 'lg';
    case WidthBreakpoint.WIDTH_MD:
      return 'md';
    case WidthBreakpoint.WIDTH_SM:
      return 'sm';
    default:
      return 'xs';
  }
}

/**
 * HeightBreakpoint 枚举值转字符串
 */
export function heightBreakpointToStr(bp: HeightBreakpoint): string {
  switch (bp) {
    case HeightBreakpoint.HEIGHT_LG:
      return 'lg';
    case HeightBreakpoint.HEIGHT_MD:
      return 'md';
    default:
      return 'sm';
  }
}

// ──────────────────────────────────────────────────────
// 使用示例（以下为可独立运行的页面组件，可直接复制使用）
// ──────────────────────────────────────────────────────

interface ProductItem {
  id: number;
  name: string;
  price: number;
}

@Entry
@Component
struct SystemBreakpointProductPage {
  @StorageProp('currentWidthBreakpoint') widthBp: WidthBreakpoint = WidthBreakpoint.WIDTH_SM;

  private readonly columns: BreakpointType<number> = new BreakpointType(2, 3, 4, 6);

  private products: ProductItem[] = [
    { id: 1, name: '商品A', price: 99 },
    { id: 2, name: '商品B', price: 199 },
    { id: 3, name: '商品C', price: 299 },
    { id: 4, name: '商品D', price: 399 },
    { id: 5, name: '商品E', price: 499 },
    { id: 6, name: '商品F', price: 599 }
  ];

  build() {
    Column() {
      Text('商品列表')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 16 })

      GridRow({ columns: this.columns.getValue(widthBreakpointToStr(this.widthBp)) }) {
        ForEach(this.products, (item: ProductItem) => {
          GridCol({ span: 1 }) {
            Column() {
              Text(item.name)
                .fontSize(16)
                .fontWeight(FontWeight.Medium)
              Text(`¥${item.price}`)
                .fontSize(14)
                .fontColor('#FF6600')
                .margin({ top: 4 })
            }
            .width('100%')
            .height(120)
            .backgroundColor('#F0F0F0')
            .borderRadius(8)
            .justifyContent(FlexAlign.Center)
            .padding(12)
          }
        })
      }
      .width('100%')
      .padding({ left: 16, right: 16 })
    }
    .width('100%')
    .height('100%')
    .padding(16)
  }
}

// ──────────────────────────────────────────────────────
// EntryAbility 初始化示例（在 EntryAbility.ets 中调用）
// ──────────────────────────────────────────────────────
//
// import { SystemBreakpointManager } from '../common/SystemBreakpointExample';
//
// export default class EntryAbility extends UIAbility {
//   onWindowStageCreate(windowStage: window.WindowStage): void {
//     windowStage.loadContent('pages/Index', (err) => {
//       if (err) {
//         return;
//       }
//       const mainWindow = windowStage.getMainWindowSync();
//       const uiContext = mainWindow.getUIContext();
//       SystemBreakpointManager.getInstance().init(uiContext, windowStage);
//     });
//   }
//
//   onDestroy(): void {
//     SystemBreakpointManager.getInstance().destroy();
//   }
// }
//
// ──────────────────────────────────────────────────────
// 断点与列数对应关系
// ──────────────────────────────────────────────────────
// | 枚举值        | 断点 | 窗口宽度(vp) | 列数 | 典型设备       |
// |--------------|------|-------------|------|---------------|
// | WIDTH_SM (1) | sm   | [320, 600)  | 2    | 手机竖屏      |
// | WIDTH_MD (2) | md   | [600, 840)  | 3    | 折叠屏展开    |
// | WIDTH_LG (3) | lg   | [840, 1440) | 4    | 平板          |
// | WIDTH_XL (4) | xl   | [1440, +∞)  | 6    | PC/大平板     |
