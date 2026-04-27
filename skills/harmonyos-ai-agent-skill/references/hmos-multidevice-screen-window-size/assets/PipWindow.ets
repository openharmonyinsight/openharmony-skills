/**
 * ================================================================
 * HarmonyOS 画中画(Picture-in-Picture) 完整示例文档
 * ================================================================
 *
 * 本文档展示了如何在 HarmonyOS 应用中实现画中画功能
 * 基于 @kit.ArkUI 的 PiPWindow API
 *
 * 适用版本：API 20+
 * 支持设备：Phone, Tablet, PC/2in1
 *
 * ================================================================
 */

/*
 * --------------------------------------------------------------------------
 * 第一部分：画中画管理器 (PipManager.ets)
 * --------------------------------------------------------------------------
 *
 * 功能说明：
 * - 封装 PiPWindow API 的核心逻辑
 * - 提供单例模式管理画中画控制器
 * - 实现画中画的初始化、启动、停止、更新尺寸等功能
 * - 处理画中画控制面板的播放/暂停事件
 */

import { PiPWindow, typeNode } from '@kit.ArkUI';
import { BusinessError } from '@kit.BasicServicesKit';
import { CustomNodeController } from './CustomNodeController';

const TAG = 'PipManager';

// 自定义 XComponent 控制器
export class CustomXComponentController extends XComponentController {
  onSurfaceCreated(surfaceId: string): void {
    console.info(`${TAG} onSurfaceCreated: ${surfaceId}`);
    // 在此初始化视频播放器或其它渲染逻辑
    // 示例：VideoPlayerManager.getInstance().initVideoPlayer(surfaceId)
  }

  onSurfaceDestroyed(surfaceId: string): void {
    console.info(`${TAG} onSurfaceDestroyed: ${surfaceId}`);
    // 画中画切换时 surface 会销毁并重建，不要在此释放播放器
    // 新的 surface 会通过 onSurfaceCreated 重新传入
  }
}

/**
 * 画中画管理器（单例模式）
 */
export class PipManager {
  private static instance: PipManager = new PipManager();
  private pipController?: PiPWindow.PiPController = undefined;
  private customNodeController: CustomNodeController;
  private mXComponentController: XComponentController;
  private lifeCycleCallback: Set<Function> = new Set();

  private constructor() {
    this.customNodeController = new CustomNodeController();
    this.mXComponentController = new CustomXComponentController();
  }

  public static getInstance(): PipManager {
    return PipManager.instance;
  }

  /**
   * 注册生命周期回调
   */
  public registerLifecycleCallback(callBack: Function): void {
    this.lifeCycleCallback.add(callBack);
  }

  public unRegisterLifecycleCallback(callBack: Function): void {
    this.lifeCycleCallback.delete(callBack);
  }

  getNode(): typeNode.XComponent | null {
    return this.customNodeController.getNode();
  }

  getNodeController(): CustomNodeController {
    return this.customNodeController;
  }

  /**
   * 画中画状态变化回调处理
   *
   * 状态说明：
   * - ABOUT_TO_START: 即将启动画中画
   * - STARTED: 画中画已启动
   * - ABOUT_TO_STOP: 即将停止画中画
   * - STOPPED: 画中画已停止
   * - ABOUT_TO_RESTORE: 即将恢复全屏
   * - ERROR: 发生错误
   */
  onStateChange(state: PiPWindow.PiPState, reason: string): void {
    let curState: string = '';

    // 根据状态控制节点添加/移除
    this.customNodeController.setCanAddNode(
      state === PiPWindow.PiPState.ABOUT_TO_STOP ||
      state === PiPWindow.PiPState.STOPPED
    );

    // 通知所有监听器
    this.lifeCycleCallback.forEach((fun: Function) => {
      fun(state);
    });

    switch (state) {
      case PiPWindow.PiPState.ABOUT_TO_START:
        curState = 'ABOUT_TO_START';
        // 从布局中移除 typeNode 节点
        this.customNodeController.removeNode();
        break;

      case PiPWindow.PiPState.STARTED:
        curState = 'STARTED';
        break;

      case PiPWindow.PiPState.ABOUT_TO_STOP:
        curState = 'ABOUT_TO_STOP';
        // 将节点重新添加回主布局（不要 dispose，否则节点被销毁无法再次启动画中画）
        this.customNodeController.addNode();
        break;

      case PiPWindow.PiPState.STOPPED:
        curState = 'STOPPED';
        break;

      case PiPWindow.PiPState.ABOUT_TO_RESTORE:
        curState = 'ABOUT_TO_RESTORE';
        break;

      case PiPWindow.PiPState.ERROR:
        curState = 'ERROR';
        break;
    }

    console.info(`[${TAG}] onStateChange: ${curState}, reason: ${reason}`);
  }

  /**
   * 注销画中画状态监听器
   */
  unregisterPipStateChangeListener(): void {
    this.pipController?.off('stateChange');
    this.pipController?.off('controlEvent');
    this.pipController = undefined;
  }

  getXComponentController(): CustomXComponentController {
    return this.mXComponentController;
  }

  /**
   * 步骤 1：创建画中画控制器
   *
   * 必须在页面显示时调用（onPageShow）
   *
   * @param ctx 上下文对象，通过 this.getUIContext().getHostContext() 获取
   */
  initPipController(ctx: Context): void {
    // 避免重复创建
    if (this.pipController) {
      return;
    }

    // 检查设备是否支持画中画
    if (!PiPWindow.isPiPEnabled()) {
      console.error(TAG, '画中画功能在当前系统不可用');
      return;
    }

    // 配置画中画参数
    let config: PiPWindow.PiPConfiguration = {
      context: ctx,
      componentController: this.getXComponentController(),
      templateType: PiPWindow.PiPTemplateType.VIDEO_PLAY,
      // 使用 typeNode 时必须设置大于 0 的宽高
      contentWidth: 1920,
      contentHeight: 1080,
    };

    // 创建画中画控制器
    PiPWindow.create(config, this.getNode())
      .then((controller: PiPWindow.PiPController) => {
        this.pipController = controller;

        // 设置自动启动（返回桌面时自动进入画中画）
        this.pipController.setAutoStartEnabled(true);

        // 注册生命周期事件回调
        this.pipController.on('stateChange',
          (state: PiPWindow.PiPState, reason: string) => {
            this.onStateChange(state, reason);
          }
        );

        // 注册控制事件回调（播放/暂停等）
        this.pipController.on('controlEvent',
          (control: PiPWindow.ControlEventParam) => {
            console.info('控制事件:', control.controlType, control.status);
            // 将画中画控制面板的操作转发给播放器
            // 示例：根据 control.controlType 和 control.status 调用播放器的 play()/pause()
            if (control.controlType === PiPWindow.PiPControlType.VIDEO_PLAY_PAUSE) {
              if (control.status === PiPWindow.PiPControlStatus.PLAY) {
                // player.play();
              } else if (control.status === PiPWindow.PiPControlStatus.PAUSE) {
                // player.pause();
              }
            }
          }
        );

        console.info(TAG, '画中画控制器创建成功');
      })
      .catch((err: BusinessError) => {
        console.error(TAG, `创建失败: ${err.code}, ${err.message}`);
      });
  }

  /**
   * 步骤 2：启动画中画
   *
   * 调用此方法后，内容将以小窗口形式显示在屏幕角落
   */
  startPip(): void {
    this.pipController?.startPiP()
      .then(() => {
        console.info(TAG, '画中画启动成功');
      })
      .catch((err: BusinessError) => {
        console.error(TAG, `启动失败: ${err.code}, ${err.message}`);
      });
  }

  /**
   * 步骤 3：更新媒体源尺寸信息
   *
   * 当视频内容尺寸变化时调用，以调整画中画窗口比例
   *
   * @param width 媒体内容宽度
   * @param height 媒体内容高度
   */
  updateContentSize(width: number, height: number): void {
    if (this.pipController) {
      this.pipController.updateContentSize(width, height);
      console.info(TAG, `更新尺寸: ${width}x${height}`);
    }
  }

  /**
   * 步骤 4：关闭画中画
   *
   * 调用此方法后，将恢复全屏显示
   */
  stopPip(): void {
    if (this.pipController) {
      this.pipController.stopPiP()
        .then(() => {
          console.info(TAG, '画中画已停止');
        })
        .catch((err: BusinessError) => {
          console.error(TAG, `停止失败: ${err.code}, ${err.message}`);
        });
    }
  }

  /**
   * 设置自动启动画中画
   *
   * @param autoStart 是否在应用返回桌面时自动启动画中画
   */
  setAutoStart(autoStart: boolean): void {
    this.pipController?.setAutoStartEnabled(autoStart);
  }

  /**
   * 移除节点
   */
  removeNode(): void {
    this.customNodeController.removeNode();
  }

  /**
   * 添加节点
   */
  addNode(): void {
    this.customNodeController.addNode();
  }
}

/*
 * --------------------------------------------------------------------------
 * 第二部分：自定义节点控制器 (CustomNodeController.ets)
 * --------------------------------------------------------------------------
 *
 * 功能说明：
 * - 继承 NodeController，实现自定义节点控制
 * - 管理 XComponent typeNode 的创建、添加和移除
 * - 处理节点的生命周期和内存管理
 */

import { FrameNode, NodeController, typeNode } from '@kit.ArkUI';
import { PipManager } from './PipManager';

const TAG = 'CustomNodeController';

/**
 * 自定义节点控制器
 * 用于管理画中画内容的 typeNode 节点
 */
export class CustomNodeController extends NodeController {
  public xComponent: typeNode.XComponent | null = null;
  private node: FrameNode | null = null;
  private canAddNode: boolean = true;

  /**
   * 设置是否可以添加节点
   * 在画中画停止时设置为 true
   */
  setCanAddNode(canAddNode: boolean): void {
    this.canAddNode = canAddNode;
  }

  /**
   * 实现 makeNode 方法
   * 当 NodeController 被添加到布局时，该方法会被自动调用
   *
   * @param context UI上下文
   * @returns FrameNode 或 null
   */
  makeNode(context: UIContext): FrameNode | null {
    this.node = new FrameNode(context);

    // 首次创建 XComponent
    if (this.xComponent === null) {
      // 创建 XComponent 类型的 typeNode
      this.xComponent = typeNode.createNode(context, 'XComponent', {
        // 设置类型为 SURFACE（用于视频播放）
        type: XComponentType.SURFACE,
        // 设置 XComponent 控制器
        controller: PipManager.getInstance().getXComponentController(),
      });
    }

    // 根据状态决定是否添加节点
    if (this.canAddNode) {
      try {
        // 先移除父节点（避免重复添加）
        this.xComponent.getParent()?.removeChild(this.xComponent);
      } catch (error) {
        console.error(`${TAG} 移除节点失败: ${error}`);
      }

      try {
        // 将 XComponent 添加到 FrameNode
        this.node.appendChild(this.xComponent);
      } catch (error) {
        console.error(`${TAG} 添加节点失败: ${error}`);
      }
    }

    return this.node;
  }

  /**
   * 重新添加 typeNode 节点到布局
   * 在画中画恢复时调用
   */
  addNode(): void {
    if (this.node && this.xComponent) {
      console.info(TAG, '添加节点');
      try {
        this.node.appendChild(this.xComponent);
      } catch (error) {
        console.error(`${TAG} 添加节点失败: ${error}`);
      }
    }
  }

  /**
   * 从布局中移除 typeNode 节点
   * 在画中画启动前调用
   */
  removeNode(): void {
    if (this.node && this.xComponent) {
      console.info(TAG, '移除节点');
      try {
        this.node.removeChild(this.xComponent);
      } catch (error) {
        console.error(`${TAG} 移除节点失败: ${error}`);
      }
    }
  }

  /**
   * 获取 XComponent 节点
   */
  getNode(): typeNode.XComponent | null {
    return this.xComponent;
  }

  /**
   * 销毁节点，释放资源
   * 在页面销毁时调用，避免内存泄漏
   */
  dispose(): void {
    console.info(TAG, '销毁节点');
    if (this.node) {
      this.node.dispose();
    }
  }
}

/*
 * --------------------------------------------------------------------------
 * 第三部分：画中画页面 (Index.ets) - 唯一页面
 * --------------------------------------------------------------------------
 *
 * 功能说明：
 * - 这是应用的主页面，也是画中画功能的演示页面
 * - 使用 NodeContainer 显示画中画内容
 * - 提供启动/停止画中画的控制按钮
 * - 实现页面生命周期管理
 * - 监听画中画状态变化并更新 UI
 */

import { PipManager } from '../manager/PipManager';
import { PiPWindow } from '@kit.ArkUI';

const TAG = 'Index';

@Entry
@Component
struct Index {
  @State pipStatus: string = '未启动';
  @State currentTime: string = new Date().toLocaleTimeString();
  @State statusColor: string = '#757575'; // 状态文本颜色
  private timer?: number;

  build() {
    Scroll() {
      Column() {
        // 页面标题
        Text('HarmonyOS 画中画示例')
          .fontSize(28)
          .fontWeight(FontWeight.Bold)
          .fontColor(Color.Black)
          .margin({ top: 40, bottom: 10 })

      // 状态显示
      Row() {
        Circle()
          .width(8)
          .height(8)
          .fill(this.getStatusColor())
          .margin({ right: 8 })

        Text(`画中画状态: ${this.pipStatus}`)
          .fontSize(16)
          .fontColor(this.getStatusColor())
          .fontWeight(FontWeight.Medium)
      }
      .margin({ bottom: 20 })

      /*
       * 核心：NodeContainer 显示画中画内容
       *
       * NodeContainer 用于承载自定义节点（typeNode）
       * 这里显示的是 XComponent，可用于播放视频或自定义内容
       */
      NodeContainer(PipManager.getInstance().getNodeController())
        .size({ width: '90%', height: 400 })
        .backgroundColor(Color.Black)
        .borderRadius(16)
        .margin({ bottom: 20 })
        .shadow({
          radius: 20,
          color: '#1F000000',
          offsetX: 0,
          offsetY: 4
        })

      // 当前时间显示
      Column() {
        Text('当前时间')
          .fontSize(14)
          .fontColor(Color.Gray)
          .margin({ bottom: 5 })

        Text(this.currentTime)
          .fontSize(32)
          .fontWeight(FontWeight.Bold)
          .fontColor(0x667eea)
      }
      .width('90%')
      .padding(20)
      .backgroundColor(0xF5F5F5)
      .borderRadius(12)
      .margin({ bottom: 20 })

      // 控制按钮区域
      Column({ space: 12 }) {
        // 第一行按钮：启动/停止画中画
        Row({ space: 16 }) {
          // 步骤 2：启动画中画
          Button('启动画中画')
            .fontSize(16)
            .fontColor(Color.White)
            .backgroundColor(0x4CAF50)
            .borderRadius(24)
            .width('48%')
            .height(50)
            .onClick(() => {
              PipManager.getInstance().startPip();
            })

          // 步骤 4：停止画中画
          Button('停止画中画')
            .fontSize(16)
            .fontColor(Color.White)
            .backgroundColor(0xF44336)
            .borderRadius(24)
            .width('48%')
            .height(50)
            .onClick(() => {
              PipManager.getInstance().stopPip();
            })
        }
        .width('90%')
        .justifyContent(FlexAlign.SpaceBetween)

        // 第二行按钮：更新尺寸
        Row({ space: 16 }) {
          // 步骤 3：更新内容尺寸
          Button('更新尺寸')
            .fontSize(16)
            .fontColor(Color.White)
            .backgroundColor(0x2196F3)
            .borderRadius(24)
            .width('48%')
            .height(50)
            .onClick(() => {
              PipManager.getInstance().updateContentSize(900, 1600);
            })

          // 显示说明
          Button('使用说明')
            .fontSize(16)
            .fontColor(Color.White)
            .backgroundColor(0xFF9800)
            .borderRadius(24)
            .width('48%')
            .height(50)
            .onClick(() => {
              this.showUsageDialog();
            })
        }
        .width('90%')
        .justifyContent(FlexAlign.SpaceBetween)
      }
      .margin({ bottom: 20 })

      // 使用提示卡片
      Column() {
        Text('💡 提示')
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .margin({ bottom: 10 })

        Text('• 点击"启动画中画"进入画中画模式')
          .fontSize(14)
          .fontColor(Color.Gray)
          .margin({ bottom: 6 })

        Text('• 点击"停止画中画"退出画中画模式')
          .fontSize(14)
          .fontColor(Color.Gray)
          .margin({ bottom: 6 })

        Text('• 点击"更新尺寸"调整画中画窗口比例')
          .fontSize(14)
          .fontColor(Color.Gray)
          .margin({ bottom: 6 })

        Text('• 返回桌面时自动进入画中画（如果已启动）')
          .fontSize(14)
          .fontColor(Color.Gray)
      }
      .width('90%')
      .padding(16)
      .backgroundColor(0xE3F2FD)
      .borderRadius(12)
      .alignItems(HorizontalAlign.Start)

        // 底部留白，确保内容不被遮挡
        Blank()
          .height(20)
      }
      .width('100%')
      .backgroundColor(Color.White)
    }
    .width('100%')
    .height('100%')
    .scrollable(ScrollDirection.Vertical) // 启用垂直滚动
    .scrollBar(BarState.Auto) // 自动显示滚动条
    .edgeEffect(EdgeEffect.Spring) // 滚动边缘弹性效果
  }

  /**
   * 根据状态获取颜色
   */
  private getStatusColor(): ResourceColor {
    switch (this.pipStatus) {
      case '运行中':
        return 0x4CAF50;
      case '已停止':
        return 0xF44336;
      case '即将启动':
        return 0xFF9800;
      case '即将停止':
        return 0xFF9800;
      default:
        return 0x757575;
    }
  }

  /**
   * 显示使用说明对话框
   */
  private showUsageDialog(): void {
    AlertDialog.show({
      title: '使用说明',
      message: '画中画功能使用步骤：\n\n' +
        '1️⃣ 点击"启动画中画"按钮\n' +
        '   内容将显示在屏幕角落的小窗口\n\n' +
        '2️⃣ 应用返回桌面时自动进入画中画\n' +
        '   无需手动操作\n\n' +
        '3️⃣ 点击"停止画中画"退出\n' +
        '   恢复全屏显示\n\n' +
        '4️⃣ 点击"更新尺寸"调整比例\n' +
        '   适应不同视频尺寸',
      confirm: {
        value: '我知道了',
        action: () => {
          console.info(TAG, '对话框关闭');
        }
      }
    });
  }

  /**
   * 画中画生命周期监听回调
   */
  private callback: Function = (state: PiPWindow.PiPState) => {
    console.info(`${TAG} 画中画状态变化: ${state}`);

    switch (state) {
      case PiPWindow.PiPState.STARTED:
        this.pipStatus = '运行中';
        break;
      case PiPWindow.PiPState.STOPPED:
        this.pipStatus = '已停止';
        break;
      case PiPWindow.PiPState.ABOUT_TO_START:
        this.pipStatus = '即将启动';
        break;
      case PiPWindow.PiPState.ABOUT_TO_STOP:
        this.pipStatus = '即将停止';
        // 重新添加节点到布局
        PipManager.getInstance().addNode();
        break;
      case PiPWindow.PiPState.ABOUT_TO_RESTORE:
        this.pipStatus = '即将恢复';
        break;
    }
  };

  /**
   * 页面显示时的生命周期
   *
   * 关键：必须在此处初始化画中画控制器
   */
  onPageShow(): void {
    console.info(TAG, 'onPageShow');

    // 注册画中画状态监听
    PipManager.getInstance().registerLifecycleCallback(this.callback);

    // 步骤 1：创建画中画控制器
    PipManager.getInstance().initPipController(
      this.getUIContext().getHostContext() as Context
    );

    // 设置自动启动（返回桌面时自动进入画中画）
    PipManager.getInstance().setAutoStart(true);
  }

  /**
   * 页面隐藏时的生命周期
   */
  onPageHide(): void {
    console.info(TAG, 'onPageHide');

    // 禁用自动启动
    // PipManager.getInstance().setAutoStart(false);

    // 移除节点
    PipManager.getInstance().removeNode();
  }

  aboutToAppear(): void {
    // 更新时间
    this.timer = setInterval((): void => {
      this.currentTime = new Date().toLocaleTimeString();
    }, 1000);
  }

  aboutToDisappear(): void {
    // 清理定时器
    if (this.timer) {
      clearInterval(this.timer);
    }

    // 注销监听
    PipManager.getInstance().unregisterPipStateChangeListener();
    PipManager.getInstance().unRegisterLifecycleCallback(this.callback);
  }
}

/*
 * --------------------------------------------------------------------------
 * 第四部分：配置文件说明 (module.json5)
 * --------------------------------------------------------------------------
 *
 * 在 entry/src/main/module.json5 中添加以下配置：
 *
 * {
 *   "module": {
 *     "abilities": [
 *       {
 *         "name": "EntryAbility",
 *         "continuable": true,  // 启用画中画支持
 *         // ... 其他配置
 *       }
 *     ]
 *   }
 * }
 */
