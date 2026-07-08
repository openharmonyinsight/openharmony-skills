// V1 示例：部分迁移 / 混用场景 — ForEach / LazyForEach
// 场景：API 14 项目，V1 列表页，使用 ForEach + LazyForEach + IDataSource
//       部分子组件已迁移到 V2，需要通过桥接模式传递数据

// ============ 数据模型 ============

@Observed
class TodoItem {
  @Track public id: string = ''
  @Track public title: string = ''
  @Track public done: boolean = false
  @Track public priority: number = 0

  constructor(id: string, title: string, done: boolean, priority: number) {
    this.id = id
    this.title = title
    this.done = done
    this.priority = priority
  }
}

// ============ IDataSource（LazyForEach 所需） ============

class TodoDataSource extends BasicDataSource {
  private dataArray: TodoItem[] = []

  public totalCount(): number {
    return this.dataArray.length
  }

  public getData(index: number): TodoItem {
    return this.dataArray[index]
  }

  public pushData(item: TodoItem): void {
    this.dataArray.push(item)
    this.notifyDataAdd(this.dataArray.length - 1)
  }

  public removeData(index: number): void {
    this.dataArray.splice(index, 1)
    this.notifyDataDelete(index)
  }

  public updateData(index: number, item: TodoItem): void {
    this.dataArray[index] = item
    this.notifyDataChange(index)
  }
}

// ============ V1 列表页 ============

@Entry
@Component
struct TodoListPage {
  @State searchQuery: string = ''
  @State todos: TodoItem[] = [
    new TodoItem('1', 'Buy groceries', false, 1),
    new TodoItem('2', 'Read book', false, 2),
    new TodoItem('3', 'Write report', true, 3),
    new TodoItem('4', 'Call mom', false, 1),
    new TodoItem('5', 'Exercise', false, 2),
  ]
  private lazyDataSource: TodoDataSource = new TodoDataSource()
  @State selectedTodo: TodoItem | null = null

  aboutToAppear() {
    this.lazyDataSource.pushData(new TodoItem('6', 'Lazy item 1', false, 1))
    this.lazyDataSource.pushData(new TodoItem('7', 'Lazy item 2', false, 2))
    this.lazyDataSource.pushData(new TodoItem('8', 'Lazy item 3', true, 3))
  }

  build() {
    Column({ space: 10 }) {
      Text('Todo List')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)

      TextInput({ text: $$this.searchQuery, placeholder: 'Search...' })
        .width('90%')

      // ForEach 全量渲染
      Text('Pinned (ForEach)')
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
      List() {
        ForEach(
          this.todos.filter(t => t.priority >= 3),
          (item: TodoItem) => {
            ListItem() {
              TodoRow({ todo: item })
            }
          },
          (item: TodoItem) => item.id
        )
      }
      .height(120)

      // LazyForEach 懒加载
      Text('All Tasks (LazyForEach)')
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
      List() {
        LazyForEach(
          this.lazyDataSource,
          (item: TodoItem) => {
            ListItem() {
              TodoRow({ todo: item })
            }
          },
          (item: TodoItem) => item.id
        )
      }
      .height(200)

      // 详情（如果 TodoDetail 已迁移为 V2，需要桥接）
      if (this.selectedTodo !== null) {
        TodoDetailV2({ todoId: this.selectedTodo.id, todoTitle: this.selectedTodo.title })
      }
    }
    .width('100%')
    .height('100%')
    .padding(15)
  }
}

// ============ V1 子组件 ============

@Component
struct TodoRow {
  @Prop todo: TodoItem = new TodoItem('', '', false, 0)

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

// ============ 已迁移的 V2 组件（混用场景） ============
// 注意：API < 19 下，V1 不能直接传 @Observed class 给 V2 组件
// 需要通过桥接模式传递简单类型参数

@ComponentV2
struct TodoDetailV2 {
  // API < 19：只能接收简单类型
  @Param todoId: string = ''
  @Param todoTitle: string = ''

  build() {
    Column({ space: 8 }) {
      Text('Detail (V2)')
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
      Text(`ID: ${this.todoId}`)
        .fontSize(14)
      Text(`Title: ${this.todoTitle}`)
        .fontSize(16)
    }
    .padding(15)
    .borderRadius(10)
    .backgroundColor('#e8f5e9')
    .width('90%')
  }
}
