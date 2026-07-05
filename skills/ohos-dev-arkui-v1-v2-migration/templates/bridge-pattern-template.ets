// ============================================================
// V1/V2 桥接模式模板 — 渐进迁移中共存方案参考
// ============================================================
// 使用场景:
//   - V1 父组件需要传递 @Observed class 给 V2 子组件
//   - 迁移过程中 V1/V2 组件共存
//
// 方案选择:
//   API >= 19 → enableV2Compatibility (推荐，简单)
//   API < 19  → 桥接组件模式 (必须)
// ============================================================

import { UIUtils } from '@kit.ArkUI'

// ══════════════════════════════════════════════════
// 方案一: API >= 19 — enableV2Compatibility
// ══════════════════════════════════════════════════

// V1 数据对象 (暂不迁移)
@Observed
class SharedData {
  @Track public value: number = 0
  @Track public label: string = ''
}

// --- V1 父组件传递复杂类型给 V2 子组件 ---

@Component
struct V1Parent {
  @State data: SharedData = new SharedData()

  build() {
    Column() {
      Text(`V1 Parent: ${this.data.value}`)

      // API >= 19: 用 enableV2Compatibility 包装后传递
      V2Child({ param: UIUtils.enableV2Compatibility(this.data) })
    }
  }
}

@ComponentV2
struct V2Child {
  @Param param: SharedData = new SharedData()

  build() {
    Text(`V2 Child: ${this.param.value}`)
  }
}

// --- V2 组件传递给 V1 组件 ---
// 关键约束 (官方 API >= 19 混用指导，见 references/mixing-rules.md):
//   1. V1 装饰器不能和 @ObservedV2 一起使用；V1 也不支持用装饰器接收 @ObservedV2 装饰的 class。
//      因此 V2→V1 共享的类必须是【普通 class 或 @Observed+@Track 装饰的 class】，不能是 @ObservedV2。
//   2. V2 侧: makeV1Observed 把普通 class 包装成 V1 状态变量，enableV2Compatibility 使其在 V2 中可观察。
//      (若类已是 @Observed 装饰，则无需 makeV1Observed，直接 enableV2Compatibility 即可。)
//   3. V1 侧用 @ObjectLink 接收 (makeV1Observed 的返回值 / @Observed 实例可初始化 @ObjectLink)，不能用 @State。

// 普通 class (注意: 不是 @ObservedV2)
class SharedModel {
  public count: number = 0
}

@ComponentV2
struct V2Parent {
  // makeV1Observed → V1 状态变量；enableV2Compatibility → 在 V2 中可观察第一层属性
  @Local model: SharedModel =
    UIUtils.enableV2Compatibility(UIUtils.makeV1Observed(new SharedModel()))

  build() {
    Column() {
      Text(`V2 Parent: ${this.model.count}`)
        .onClick(() => { this.model.count++ })
      // 传给 V1 子组件；V1 用 @ObjectLink 接收
      V1Receiver({ data: this.model })
    }
  }
}

@Component
struct V1Receiver {
  @ObjectLink data: SharedModel    // ← @ObjectLink (不是 @State)；类型为普通 class

  build() {
    Text(`V1 Receiver: ${this.data.count}`)
      .onClick(() => { this.data.count++ })
  }
}

// ══════════════════════════════════════════════════
// 方案二: API < 19 — 桥接组件模式
// ══════════════════════════════════════════════════

// V1 数据对象 (暂不迁移)
@Observed
class BridgeData {
  @Track public count: number = 0
  @Track public name: string = ''
}

// --- 桥接组件 (API < 19) ---
// 流程: V1Comp → V1Bridge(@Component) → V2Comp(@ComponentV2)
//
// 关键约束 (见 references/mixing-rules.md):
//   1. API < 19 下复杂类型(@Observed class / Array / Map / Set / Date)禁止跨 V1→V2 边界，
//      仅允许传递简单类型(boolean / number / string / null / undefined)，V2 用 @Param 接收。
//   2. V1 装饰器(@State / @Prop / ...)不能持有 @ObservedV2 装饰的 class。
//   因此桥接组件是【纯 V1 组件】: 把 @Observed class 拆成简单类型字段再传给 V2 子组件的 @Param，
//   不得在 V1 组件里持有 @ObservedV2 对象、也不得把整个 @Observed class 传过边界。
//   (多组件共享场景请用方案三的独立 @ObservedV2 单例。)

@Component
struct V1BridgeComponent {
  // 接收 V1 父组件传入的 @Observed class —— V1 装饰器持有 V1 @Observed 类，合法。
  //
  // ✅ 正确: @Watch 装饰【被监听的变量 v1Data】，字符串参数是【回调方法名 'onV1DataChange'】，
  //          与变量声明在同一行。
  // ❌ 错误(旧模板): 把 @Watch('v1Data') 单独写在方法 onDataChange() 上一行 ——
  //                  @Watch 不能装饰方法，参数也不应是变量名。
  @Prop @Watch('onV1DataChange') v1Data: BridgeData = new BridgeData()

  aboutToAppear() {
    this.onV1DataChange()
  }

  // @Watch 的回调是普通方法，不加任何装饰器。
  // 注意: @Watch 仅在 v1Data 被【重新赋值】时触发；父组件直接改 v1Data.count 等 @Track 属性时，
  // 靠 build() 读取该属性建立的观测自动刷新子组件，不需要在这里手动同步字段。
  onV1DataChange() {
    console.info(`bridge: v1Data reassigned, count=${this.v1Data.count}`)
  }

  build() {
    // 把复杂类型拆成简单类型字段，逐个传给 V2 子组件的 @Param。
    // ❌ 不得写 V2TargetComponent({ data: this.v1Data }) —— 会把 @Observed class
    //    跨 V1→V2 边界传递，违反 API < 19 混用规则。
    V2TargetComponent({
      count: this.v1Data.count,
      name: this.v1Data.name
    })
  }
}

// V2 目标组件 —— 仅用简单类型 @Param 接收
// (如需在 V2 侧维护自己的 @ObservedV2 模型，可在组件内部用这些原始值自行构造，不跨边界即可)
@ComponentV2
struct V2TargetComponent {
  @Param count: number = 0
  @Param name: string = ''

  build() {
    Column() {
      Text(`V2 Target: ${this.count}`)
      Text(`Name: ${this.name}`)
    }
  }
}

// --- V1 父组件 ---

@Component
struct V1SourceComponent {
  @State sourceData: BridgeData = new BridgeData()

  build() {
    Column() {
      Text(`V1 Source: ${this.sourceData.count}`)

      Button('increment')
        .onClick(() => { this.sourceData.count++ })

      // 通过桥接组件传递
      V1BridgeComponent({ v1Data: this.sourceData })
    }
  }
}

// ══════════════════════════════════════════════════
// 方案三: 单例桥接 — 多组件共享 V1/V2 数据
// ══════════════════════════════════════════════════

// V2 单例，同时持有 V1 和 V2 格式数据
@ObservedV2
class SharedBridgeSingleton {
  private static instance_: SharedBridgeSingleton

  static instance(): SharedBridgeSingleton {
    if (!SharedBridgeSingleton.instance_) {
      SharedBridgeSingleton.instance_ = new SharedBridgeSingleton()
    }
    return SharedBridgeSingleton.instance_
  }

  @Trace public count: number = 0
  @Trace public name: string = ''

  private constructor() {}
}

// V1 组件写入单例
@Component
struct V1Writer {
  @State localCount: number = 0

  updateShared() {
    const shared = SharedBridgeSingleton.instance()
    shared.count = this.localCount
  }

  build() {
    Column() {
      Button('V1 update')
        .onClick(() => {
          this.localCount++
          this.updateShared()
        })
    }
  }
}

// V2 组件读取单例
@ComponentV2
struct V2Reader {
  @Local shared: SharedBridgeSingleton = SharedBridgeSingleton.instance()

  @Monitor('shared.count')
  onCountChange(mon: IMonitor) {
    console.info(`V2 detected: count changed to ${this.shared.count}`)
  }

  build() {
    Text(`V2 reads: ${this.shared.count}`)
  }
}
