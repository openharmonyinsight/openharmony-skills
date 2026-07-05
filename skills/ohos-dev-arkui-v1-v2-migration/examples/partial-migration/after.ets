// V2 示例：部分迁移 / 混用场景 — Repeat 替代 ForEach/LazyForEach
// 迁移要点：
//   1. ForEach → Repeat（全量加载）
//   2. LazyForEach + IDataSource → Repeat + .virtualScroll()（懒加载）
//   3. IDataSource → @Local 数组（直接修改即自动更新）
//   4. API < 19 混用：V1→V2 只能传简单类型，复杂类型需桥接模式
//   5. API >= 19 混用：使用 enableV2Compatibility 放宽约束
//   6. $$ → !!

import { UIUtils } from '@kit.ArkUI'

// ============ 数据模型 ============

@ObservedV2
class TodoItem {
  @Trace public id: string = ''
  @Trace public title: string = ''
  @Trace public done: boolean = false
  @Trace public priority: number = 0

  constructor(id: string, title: string, done: boolean, priority: number) {
    this.id = id
    this.title = title
    this.done = done
    this.priority = priority
  }
}

// ============ V2 列表页 ============

@Entry
@ComponentV2
struct TodoListPage {
  @Local searchQuery: string = ''
  // IDataSource 不再需要，直接使用 @Local 数组
  @Local pinnedTodos: TodoItem[] = [
    new TodoItem('1', 'Buy groceries', false, 1),
    new TodoItem('2', 'Read book', false, 2),
    new TodoItem('3', 'Write report', true, 3),
    new TodoItem('4', 'Call mom', false, 1),
    new TodoItem('5', 'Exercise', false, 2),
  ]
  // 懒加载也用 @Local 数组
  @Local lazyTodos: TodoItem[] = [
    new TodoItem('6', 'Lazy item 1', false, 1),
    new TodoItem('7', 'Lazy item 2', false, 2),
    new TodoItem('8', 'Lazy item 3', true, 3),
  ]
  @Local selectedTodo: TodoItem | null = null

  build() {
    Column({ space: 10 }) {
      Text('Todo List')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)

      TextInput({ text: this.searchQuery!!, placeholder: 'Search...' })
        .width('90%')

      // Repeat 替代 ForEach（全量加载模式）
      Text('Pinned (Repeat)')
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
      List() {
        Repeat(this.pinnedTodos.filter(t => t.priority >= 3))
          .each((ri: RepeatItem<TodoItem>) => {
            ListItem() {
              TodoRow({ todo: ri.item })
            }
          })
          .key((item: TodoItem) => item.id)
      }
      .height(120)

      // Repeat + .virtualScroll() 替代 LazyForEach（懒加载模式）
      // 不再需要 IDataSource / BasicDataSource / notifyDataAdd 等
      Text('All Tasks (Repeat + virtualScroll)')
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
      List() {
        Repeat(this.lazyTodos)
          .each((ri: RepeatItem<TodoItem>) => {
            ListItem() {
              TodoRow({ todo: ri.item })
            }
          })
          .key((item: TodoItem) => item.id)
          .virtualScroll()
      }
      .height(200)

      // 详情 — 全 V2，不再需要桥接
      if (this.selectedTodo !== null) {
        TodoDetailV2({ todo: this.selectedTodo })
      }

      // 演示：直接修改数组即自动更新（无需 notifyDataAdd）
      Button('Add lazy item')
        .onClick(() => {
          this.lazyTodos.push(
            new TodoItem(`${this.lazyTodos.length + 6}`, 'New task', false, 1)
          )
        })
    }
    .width('100%')
    .height('100%')
    .padding(15)
  }
}

// ============ V2 子组件 ============

@ComponentV2
struct TodoRow {
  @Param todo: TodoItem = new TodoItem('', '', false, 0)

  build() {
    Row({ space: 10 }) {
      Checkbox()
        .select(this.todo.done)
        .onChange((checked: boolean) => {
          this.todo.done = checked
        })
      Text(this.todo.title)
        .fontSize(16)
        .decoration({ type: this.todo.done ? TextDecorationType.LineThrough : TextDecorationType.None })
      Text(`P${this.todo.priority}`)
        .fontSize(12)
        .fontColor('#888')
    }
    .width('90%')
    .padding(8)
    .borderRadius(6)
    .backgroundColor('#f8f8f8')
  }
}

// ============ V2 详情组件 ============
// 全 V2 后可传递复杂类型 @ObservedV2 class，无需桥接

@ComponentV2
struct TodoDetailV2 {
  @Param todo: TodoItem = new TodoItem('', '', false, 0)

  build() {
    Column({ space: 8 }) {
      Text('Detail (V2)')
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
      Text(`ID: ${this.todo.id}`)
        .fontSize(14)
      Text(`Title: ${this.todo.title}`)
        .fontSize(16)
    }
    .padding(15)
    .borderRadius(10)
    .backgroundColor('#e8f5e9')
    .width('90%')
  }
}

// ============ 附录：API < 19 桥接模式（如果必须保留部分 V1 组件） ============
// 场景：V1 父组件需要传 @Observed class 给 V2 子组件时

// 桥接 V1 组件：用 @Watch 监听变化，同步到 V2 可观察的单例
// @ObservedV2
// class TodoBridge {
//   private static inst: TodoBridge
//   static instance() { if (!TodoBridge.inst) TodoBridge.inst = new TodoBridge(); return TodoBridge.inst }
//   @Trace public title: string = ''
//   @Trace public done: boolean = false
// }
//
// @Component
// struct V1Bridge {
//   @Prop todo: TodoItem
//   private bridge = TodoBridge.instance()
//
//   aboutToAppear() {
//     this.syncToBridge()
//   }
//
//   @Watch('todo')
//   syncToBridge() {
//     this.bridge.title = this.todo.title
//     this.bridge.done = this.todo.done
//   }
//
//   build() {
//     // 传递 V2 可观察的桥接单例给 V2 子组件
//     TodoDetailV2({ todo: this.bridge })
//   }
// }

// ============ 附录：API >= 19 混用模式 ============
// 场景：V1 组件需传递复杂类型给 V2 子组件

// @ComponentV2
// struct V2Child {
//   // API >= 19：使用 enableV2Compatibility 使 V1 状态变量在 V2 中可观察
//   @Param todo: TodoItem = UIUtils.enableV2Compatibility(new TodoItem('', '', false, 0))
//   // ...
// }
//
// // V1 父组件传递：
// // V2Child({ todo: UIUtils.enableV2Compatibility(this.v1Todo) })
