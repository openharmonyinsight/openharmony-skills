/**
 * BreakpointType.ets
 * 断点类型工具类 - 简化断点条件渲染
 */

export class BreakpointType<T> {
  sm: T;
  md?: T;
  lg?: T;
  xl?: T;

  constructor(sm: T, md?: T, lg?: T, xl?: T) {
    this.sm = sm;
    this.md = md;
    this.lg = lg;
    this.xl = xl;
  }

  /**
   * 根据断点获取对应值
   */
  getValue(breakpoint: string): T {
    switch (breakpoint) {
      case 'xl':
        return this.xl ?? this.lg ?? this.md ?? this.sm;
      case 'lg':
        return this.lg ?? this.md ?? this.sm;
      case 'md':
        return this.md ?? this.sm;
      default:
        return this.sm;
    }
  }
}

/**
 * 创建断点类型
 */
export function breakpointType<T>(
  sm: T,
  md?: T,
  lg?: T,
  xl?: T
): BreakpointType<T> {
  return new BreakpointType(sm, md, lg, xl);
}

/**
 * 使用示例:
 *
 * // 1. 列数配置
 * const columns = new BreakpointType(4, 8, 12);
 * GridRow({ columns: columns.getValue(this.currentBreakpoint) }) { ... }
 *
 * // 2. 间距配置
 * const gutter = new BreakpointType(12, 16, 24);
 * GridRow({ gutter: { x: gutter.getValue(this.currentBreakpoint) } }) { ... }
 *
 * // 3. 组件可见性
 * const visibility = new BreakpointType(Visibility.None, Visibility.Visible);
 * Text('详情')
 *   .visibility(visibility.getValue(this.currentBreakpoint))
 *
 * // 4. 布局方向
 * const direction = new BreakpointType(Axis.Vertical, Axis.Horizontal);
 * List({ direction: direction.getValue(this.currentBreakpoint) }) { ... }
 */
