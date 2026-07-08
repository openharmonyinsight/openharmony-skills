# 渲染控制与组件复用迁移

## ForEach -> Repeat（全量加载）

```typescript
// V1
List() {
  ForEach(this.data, (item: string) => {
    ListItem() { Text(item) }
  }, (item: string) => item)
}

// V2
List() {
  Repeat(this.data)
    .each((ri: RepeatItem<string>) => {
      ListItem() { Text(ri.item) }
    })
    .key((item: string) => item)
}
```

## LazyForEach -> Repeat + .virtualScroll()

### 数据源迁移
```typescript
// V1: 需要IDataSource
class MyDataSource extends BasicDataSource {
  private dataArray: string[] = [];
  public totalCount(): number { return this.dataArray.length; }
  public getData(index: number): string { return this.dataArray[index]; }
  public pushData(data: string): void {
    this.dataArray.push(data);
    this.notifyDataAdd(this.dataArray.length - 1);
  }
}

// V2: 直接用@Local数组
@Local data: Array<string> = [];
```

### 组件生成和键值函数
```typescript
// V1
LazyForEach(this.data, (item, index) => { ... }, (item, index) => item)

// V2
Repeat(this.data)
  .each((ri: RepeatItem<string>) => { ... })
  .key((item: string) => item)
  .virtualScroll()  // 使能懒加载
```

### 数据更新
V1需要手动调用 notifyDataAdd/notifyDataDelete/notifyDataChange 等。
V2直接修改数据源数组即可，状态管理V2自动监听变化。

### 模板渲染
Repeat内置模板渲染能力，用 .templateId() + .template() 替代手动if判断：
```typescript
Repeat(this.data)
  .template('A', (ri) => { ListItem() { ... } })
  .template('B', (ri) => { ListItem() { ... } })
  .templateId((item) => item.type === 0 ? 'A' : 'B')
  .virtualScroll()
```

### 拖拽排序
Repeat支持 .onMove() 属性，与LazyForEach一致。

### 子属性观测
V1用 @Observed + @ObjectLink，V2用 @ObservedV2 + @Trace：
```typescript
@ObservedV2
class StringData {
  @Trace message: string;
}
Repeat(this.data)
  .each((ri) => {
    ListItem() { Text(ri.item.message) }
    .onClick(() => { ri.item.message += '!'; })
  })
  .virtualScroll()
```

### 组件复用
Repeat自身默认具备复用能力。如需使用 @ReusableV2，需关闭Repeat自身复用：
```typescript
.virtualScroll({ reusable: false })
```

## @Reusable -> @ReusableV2

| V1 | V2 | 说明 |
|----|-----|------|
| @Reusable | @ReusableV2 | 装饰器替换 |
| aboutToRecycle() | aboutToRecycle() | 无需改动 |
| aboutToReuse(params) | aboutToReuse() | V2无参数，自动重置状态变量 |
| .reuseId('id') | .reuse({ reuseId: () => 'id' }) | API替换 |
| freezeWhenInactive | 自动冻结 | V2自动开启 |

### aboutToReuse变化
V2在复用前会自动重置各状态变量，无需手动赋值回初始值：
- @Local 重置回初始值
- @Param @Once 重置回外部传入值

### 数据源迁移
V1的 IDataSource + DataChangeListener → V2的 @Local 数组：
```typescript
// V1
private data: MyDataSource = new MyDataSource();
LazyForEach(this.data, ...)

// V2
@Local data: Array<string> = [];
Repeat(this.data).virtualScroll().each(...)
```
