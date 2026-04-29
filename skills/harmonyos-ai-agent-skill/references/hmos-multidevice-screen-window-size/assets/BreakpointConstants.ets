/**
 * BreakpointConstants.ets
 * 断点常量定义 - 统一管理所有断点值
 */

export class BreakpointConstants {
  // 断点值 (vp)
  static readonly BREAKPOINT_XS_VALUE: number = 320;
  static readonly BREAKPOINT_SM_VALUE: number = 600;
  static readonly BREAKPOINT_MD_VALUE: number = 840;
  static readonly BREAKPOINT_LG_VALUE: number = 1440;

  // 断点名称
  static readonly BREAKPOINT_XS: string = 'xs';
  static readonly BREAKPOINT_SM: string = 'sm';
  static readonly BREAKPOINT_MD: string = 'md';
  static readonly BREAKPOINT_LG: string = 'lg';
  static readonly BREAKPOINT_XL: string = 'xl';

  // 纵向断点 (高宽比)
  static readonly VERTICAL_BREAKPOINT_SM: number = 0.8;
  static readonly VERTICAL_BREAKPOINT_MD: number = 1.2;

  // 纵向断点名称
  static readonly VERTICAL_SM: string = 'vertical_sm'; // 横向窗口
  static readonly VERTICAL_MD: string = 'vertical_md'; // 类方形窗口
  static readonly VERTICAL_LG: string = 'vertical_lg'; // 纵向窗口

  // AppStorage Key
  static readonly CURRENT_BREAKPOINT: string = 'currentBreakpoint';
  static readonly CURRENT_VERTICAL_BREAKPOINT: string = 'currentVerticalBreakpoint';
  static readonly WINDOW_WIDTH: string = 'windowWidth';
  static readonly WINDOW_HEIGHT: string = 'windowHeight';
}

/**
 * 根据窗口宽度获取断点
 */
export function getBreakpointByWidth(width: number): string {
  if (width < BreakpointConstants.BREAKPOINT_XS_VALUE) {
    return BreakpointConstants.BREAKPOINT_XS;
  } else if (width < BreakpointConstants.BREAKPOINT_SM_VALUE) {
    return BreakpointConstants.BREAKPOINT_SM;
  } else if (width < BreakpointConstants.BREAKPOINT_MD_VALUE) {
    return BreakpointConstants.BREAKPOINT_MD;
  } else if (width < BreakpointConstants.BREAKPOINT_LG_VALUE) {
    return BreakpointConstants.BREAKPOINT_LG;
  } else {
    return BreakpointConstants.BREAKPOINT_XL;
  }
}

/**
 * 根据高宽比获取纵向断点
 */
export function getVerticalBreakpoint(width: number, height: number): string {
  const ratio = height / width;
  if (ratio < BreakpointConstants.VERTICAL_BREAKPOINT_SM) {
    return BreakpointConstants.VERTICAL_SM;
  } else if (ratio < BreakpointConstants.VERTICAL_BREAKPOINT_MD) {
    return BreakpointConstants.VERTICAL_MD;
  } else {
    return BreakpointConstants.VERTICAL_LG;
  }
}

/**
 * 使用示例 - OrangeShopping 主页响应式商品列表
 *
 * // 1. 在页面中监听窗口尺寸变化
 * @Entry
 * @Component
 * struct MainPage {
 *   @State currentBreakpoint: string = BreakpointConstants.BREAKPOINT_SM;
 *
 *   // 商品列表列数配置
 *   private readonly productColumns: BreakpointType<number> = new BreakpointType(2, 3, 4, 6);
 *
 *   // 更新断点
 *   private updateBreakpoint(width: number): void {
 *     const newBreakpoint = getBreakpointByWidth(width);
 *     if (this.currentBreakpoint !== newBreakpoint) {
 *       this.currentBreakpoint = newBreakpoint;
 *     }
 *   }
 *
 *   build() {
 *     Column() {
 *       // ... 其他组件
 *
 *       // 响应式商品列表
 *       GridRow({
 *         columns: this.productColumns.getValue(this.currentBreakpoint),
 *         gutter: { x: 8, y: 8 }
 *       }) {
 *         ForEach(this.products, (product: ProductItem, index: number) => {
 *           GridCol({ span: 1 }) {
 *             ProductCard({ product: product, index: index })
 *           }
 *         })
 *       }
 *     }
 *     .onAreaChange((oldValue: Area, newValue: Area) => {
 *       const newWidth = Number(newValue.width);
 *       if (newWidth > 0) {
 *         this.updateBreakpoint(newWidth);
 *       }
 *     })
 *   }
 * }
 *
 * // 2. 断点与列数对应关系
 * // | 断点 | 窗口宽度(vp) | 商品列表列数 | 典型设备 |
 * // |------|-------------|-------------|----------|
 * // | sm   | [320, 600)  | 2列         | 手机竖屏 |
 * // | md   | [600, 840)  | 3列         | 手机横屏/折叠屏展开 |
 * // | lg   | [840, 1440) | 4列         | 平板 |
 * // | xl   | [1440, +∞)  | 6列         | PC/大平板 |
 */
