/**
 * HoverEffectExample.ets
 * 鼠标悬浮效果示例
 */

/**
 * 悬浮效果类型
 */
export enum HoverEffectType {
  NONE = 'none',
  HIGHLIGHT = 'highlight',
  SCALE = 'scale',
  CUSTOM = 'custom'
}

/**
 * 悬浮效果配置
 */
export interface HoverEffectConfig {
  type: HoverEffectType;
  normalColor?: string;
  hoverColor?: string;
  scaleRatio?: number;
  transitionDuration?: number;
}

/**
 * 悬浮效果管理器
 */
export class HoverEffectManager {
  private static instance: HoverEffectManager;
  private effects: Map<string, HoverEffectConfig> = new Map();

  private constructor() {
    this.initDefaultEffects();
  }

  static getInstance(): HoverEffectManager {
    if (!HoverEffectManager.instance) {
      HoverEffectManager.instance = new HoverEffectManager();
    }
    return HoverEffectManager.instance;
  }

  /**
   * 初始化默认效果
   */
  private initDefaultEffects(): void {
    this.effects.set('button', {
      type: HoverEffectType.HIGHLIGHT,
      normalColor: '#F5F5F5',
      hoverColor: '#E8E8E8',
      transitionDuration: 200
    });

    this.effects.set('card', {
      type: HoverEffectType.SCALE,
      scaleRatio: 1.02,
      transitionDuration: 150
    });

    this.effects.set('listItem', {
      type: HoverEffectType.HIGHLIGHT,
      normalColor: '#FFFFFF',
      hoverColor: '#F0F0F0',
      transitionDuration: 100
    });
  }

  /**
   * 获取效果配置
   */
  getEffect(name: string): HoverEffectConfig | undefined {
    return this.effects.get(name);
  }

  /**
   * 注册自定义效果
   */
  registerEffect(name: string, config: HoverEffectConfig): void {
    this.effects.set(name, config);
  }

  /**
   * 判断是否应该显示悬浮效果
   * 基于当前输入设备类型
   */
  shouldShowHoverEffect(): boolean {
    // 检测是否有鼠标/触控板连接
    // 这里简化处理，实际应检测输入设备
    return true; // 平板和PC默认显示
  }
}

/**
 * 悬浮效果组件示例
 */
@Component
export struct HoverCard {
  @Prop title: string = '标题';
  @Prop description: string = '描述内容';
  @State isHovered: boolean = false;

  private config: HoverEffectConfig = {
    type: HoverEffectType.HIGHLIGHT,
    normalColor: '#FFFFFF',
    hoverColor: '#F5F5F5',
    transitionDuration: 200
  };

  build() {
    Column() {
      Text(this.title)
        .fontSize(18)
        .fontWeight(FontWeight.Medium)

      Text(this.description)
        .fontSize(14)
        .fontColor('#666666')
        .margin({ top: 8 })
    }
    .width('100%')
    .padding(16)
    .backgroundColor(this.isHovered ? this.config.hoverColor : this.config.normalColor)
    .borderRadius(12)
    .animation({
      duration: this.config.transitionDuration,
      curve: Curve.EaseInOut
    })
    .onHover((isHover: boolean) => {
      if (HoverEffectManager.getInstance().shouldShowHoverEffect()) {
        this.isHovered = isHover;
      }
    })
  }
}

/**
 * 悬浮效果按钮示例
 */
@Component
export struct HoverButton {
  @State text: string = '按钮';
  @State isHovered: boolean = false;
  private clickFunc: () => void  = ()=>{};

  constructor(onClick: () => void) {
    super();
    this.clickFunc = onClick;
  }

  build() {
    Button(this.text)
      .backgroundColor(this.isHovered ? '#0066CC' : '#007AFF')
      .borderRadius(8)
      .animation({
        duration: 150,
        curve: Curve.EaseInOut
      })
      .onHover((isHover: boolean) => {
        this.isHovered = isHover;
      })
      .onClick(() => {
        this.clickFunc();
      })
  }
}

/**
 * 带阴影的悬浮卡片
 */
@Component
export struct HoverCardWithShadow {
  @Prop title: string = '标题';
  @State isHovered: boolean = false;
  @State elevation: number = 2;

  build() {
    Column() {
      Text(this.title)
        .fontSize(18)
    }
    .width('100%')
    .height(100)
    .padding(16)
    .backgroundColor(Color.White)
    .borderRadius(12)
    .shadow({
      radius: this.isHovered ? 16 : 8,
      color: '#1A000000',
      offsetX: 0,
      offsetY: this.isHovered ? 4 : 2
    })
    .scale({
      x: this.isHovered ? 1.02 : 1,
      y: this.isHovered ? 1.02 : 1
    })
    .animation({
      duration: 200,
      curve: Curve.EaseOut
    })
    .onHover((isHover: boolean) => {
      this.isHovered = isHover;
    })
  }
}

/**
 * 使用示例:
 *
 * @Entry
 * @Component
* struct HoverEffectPage {
 *   build() {
 *     Column() {
 *       // 基础悬浮卡片
 *       HoverCard({
 *         title: '卡片标题',
 *         description: '这是卡片描述内容'
 *       })
 *
 *       // 带阴影的悬浮卡片
 *       HoverCardWithShadow({
 *         title: '带阴影的卡片'
 *       })
 *
 *       // 悬浮按钮
 *       HoverButton(() => {
 *         console.log('按钮被点击');
 *       })
 *     }
 *     .padding(16)
 *   }
 * }
 */
