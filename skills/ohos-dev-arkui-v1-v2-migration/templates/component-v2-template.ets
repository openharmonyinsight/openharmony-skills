// ============================================================
// V2 Component Template — @ComponentV2 所有装饰器模式参考
// ============================================================
// 迁移对照:
//   @Component       → @ComponentV2
//   @Reusable         → @ReusableV2
//   @State            → @Local (内部状态) 或 @Param @Once (外部初始化)
//   @Prop             → @Param
//   @Link             → @Param + @Event (回调模式)
//   @Provide/@Consume → @Provider/@Consumer
//   @Watch            → @Monitor
//   无                 → @Computed (V2新增)
//   $$                → !!
//   ForEach/LazyForEach → Repeat
// ============================================================

import { AppStorageV2 } from '@kit.ArkUI';

// ──────────────────────────────────────────────
// 1. 简单组件: @State → @Local
// ──────────────────────────────────────────────

@Entry
@ComponentV2
struct SimplePage {
  // V1: @State count: number = 0
  @Local count: number = 0

  build() {
    Column() {
      Text(`${this.count}`)
      Button('increment')
        .onClick(() => this.count++)
    }
  }
}

// ──────────────────────────────────────────────
// 2. 外部初始化: @State外部初始化 → @Param @Once
// ──────────────────────────────────────────────

@ComponentV2
struct ChildWithInit {
  // V1: @State value: number = 0  (父组件可 Child({ value: 30 }))
  // V2: @Local 禁止外部初始化，需用 @Param @Once
  @Param @Once value: number = 0

  build() {
    Text(`${this.value}`)
  }
}

// 父组件使用:
// ChildWithInit({ value: 30 })

// ──────────────────────────────────────────────
// 3. 父子单向传递: @Prop → @Param
// ──────────────────────────────────────────────

@ComponentV2
struct DisplayItem {
  // V1: @Prop title: string = ''
  // V2: @Param 是引用传递（非深拷贝），只读
  @Param title: string = ''

  // 子组件需本地修改: @Local 本地副本 + @Monitor 同步
  @Local localTitle: string = ''
  @Param editableTitle: string = ''
  @Monitor('editableTitle')
  onTitleChange(mon: IMonitor) {
    this.localTitle = this.editableTitle
  }

  build() {
    Text(this.localTitle)
  }
}

// ──────────────────────────────────────────────
// 4. 双向绑定: @Link → @Param + @Event
// ──────────────────────────────────────────────

// V1:
// @Component struct Child {
//   @Link count: number;
// }
// Parent: Child({ count: this.myCount })

// V2:
@ComponentV2
struct Child {
  @Param count: number = 0
  @Event setCount: (val: number) => void = () => {}

  // 子组件修改时通过 @Event 回调通知父组件
  increment() {
    this.setCount(this.count + 1)
  }

  build() {
    Column() {
      Text(`${this.count}`)
      Button('+1').onClick(() => this.increment())
    }
  }
}

// 父组件使用:
// Child({ count: this.myCount, setCount: (v: number) => this.myCount = v })

// ──────────────────────────────────────────────
// 5. 跨层级传递: @Provide/@Consume → @Provider/@Consumer
// ──────────────────────────────────────────────

@ComponentV2
struct Grandparent {
  // V1: @Provide('theme') theme: string = 'dark'
  // V2: 必须加 ()，alias 为唯一匹配键
  @Provider('theme') theme: string = 'dark'

  build() {
    Column() {
      // 子/孙组件通过 @Consumer('theme') 获取
      MiddleComponent()
    }
  }
}

@ComponentV2
struct DeepChild {
  // V1: @Consume('theme') theme: string
  // V2: 支持本地默认值（找不到 @Provider 时使用）
  @Consumer('theme') theme: string = 'light'

  build() {
    Text(`Theme: ${this.theme}`)
  }
}

// ──────────────────────────────────────────────
// 6. 变量监听: @Watch → @Monitor
// ──────────────────────────────────────────────

@ComponentV2
struct MonitorDemo {
  @Local apple: number = 0
  @Local orange: number = 0

  // V1: @State @Watch('onApple') apple: number = 0
  //     onApple(): void { ... }
  // V2: 支持多变量监听，提供 before/after 值
  @Monitor('apple', 'orange')
  onFruitChange(monitor: IMonitor) {
    monitor.dirty.forEach((name: string) => {
      const before = monitor.value(name)?.before
      const now = monitor.value(name)?.now
      console.info(`${name}: ${before} -> ${now}`)
    })
  }

  build() {
    Column() {
      Button('apple').onClick(() => this.apple++)
      Button('orange').onClick(() => this.orange++)
    }
  }
}

// ──────────────────────────────────────────────
// 7. 派生状态: @Computed (V2新增)
// ──────────────────────────────────────────────

@ComponentV2
struct ComputedDemo {
  @Local firstName: string = 'Li'
  @Local lastName: string = 'Hua'

  // 自动缓存，依赖的 @Local 变化时重新计算
  @Computed
  get fullName(): string {
    return `${this.firstName} ${this.lastName}`
  }

  build() {
    Text(this.fullName)
  }
}

// ──────────────────────────────────────────────
// 8. 渲染控制: ForEach/LazyForEach → Repeat
// ──────────────────────────────────────────────

@ComponentV2
struct ListDemo {
  @Local items: string[] = ['A', 'B', 'C']

  // ForEach → Repeat (全量)
  buildList() {
    List() {
      // V1: ForEach(this.items, (item) => { ListItem() { ... } }, (item) => item)
      Repeat(this.items)
        .each((ri: RepeatItem<string>) => {
          ListItem() {
            Text(ri.item)
          }
        })
        .key((item: string) => item)
    }
  }

  // LazyForEach → Repeat + .virtualScroll()
  buildLazyList() {
    List() {
      Repeat(this.items)
        .each((ri: RepeatItem<string>) => {
          ListItem() {
            Text(ri.item)
          }
        })
        .key((item: string) => item)
        .virtualScroll()
    }
  }

  // 模板渲染: .templateId() + .template()
  buildTemplateList() {
    Repeat(this.items)
      .template('A', (ri: RepeatItem<string>) => {
        ListItem() { Text(`TypeA: ${ri.item}`) }
      })
      .template('B', (ri: RepeatItem<string>) => {
        ListItem() { Text(`TypeB: ${ri.item}`) }
      })
      .templateId((item: string) => item.startsWith('A') ? 'A' : 'B')
      .virtualScroll()
  }

  build() {
    Column() {
      this.buildList()
    }
  }
}

// ──────────────────────────────────────────────
// 9. 双向语法: $$ → !!
// ──────────────────────────────────────────────

@ComponentV2
struct BindingDemo {
  @Local text: string = ''

  build() {
    // V1: TextInput({ text: $$this.text })
    // V2: TextInput({ text: this.text!! })
    TextInput({ text: this.text!! })
      .onChange((value: string) => { this.text = value })
  }
}

// ──────────────────────────────────────────────
// 10. 组件复用: @Reusable → @ReusableV2
// ──────────────────────────────────────────────

@ReusableV2
@ComponentV2
struct ReusableItem {
  @Local name: string = ''

  // V1: aboutToReuse(params: Record<string, Object>) { this.name = params.name as string }
  // V2: aboutToReuse() 无参数，@Local @Param @Once 自动重置
  aboutToReuse(): void {
    // 无需手动赋值，状态变量自动重置
  }

  aboutToRecycle(): void {
    // 与 V1 一致
  }

  build() {
    Text(this.name)
  }
}

// 使用:
// V1: ReusableItem().reuseId('item')
// V2: ReusableItem().reuse({ reuseId: () => 'item' })
