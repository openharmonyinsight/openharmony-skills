# 问题排查指南

## 编译错误

### 1. "Property 'state' is used before being assigned"

**原因**：ArkTS 严格模式不允许在赋值前读取属性

**解决方案**：
```typescript
// 错误
constructor() {
  super();
  const baseState = this.state;  // 错误！
  this.state = { ... };
}

// 正确
constructor() {
  super();
  this.state = {  // 直接赋值
    title: '',
    isLoading: false,
    // ...
  };
}
```

### 2. "Cannot find name 'XXX'"

**原因**：缺少导入或类型未定义

**解决方案**：
- 检查导入语句
- 确认类型是否已导出
- 检查命名空间是否正确

### 3. "super.property is not allowed"

**原因**：不应该使用 `super` 访问父类属性

**解决方案**：
```typescript
// 错误
const value = super.state;

// 正确
const value = this.state;  // 继承的属性直接通过 this 访问
```

## 运行时错误

### 1. 白屏问题

**可能原因**：
- 权限检查失败
- 状态未正确初始化
- 页面路径配置错误

**排查步骤**：
1. 检查 `main_pages.json` 配置
2. 检查 `EntryAbility.ets` 中的 `loadContent` 路径
3. 检查权限检查方法返回值
4. 检查状态变量是否正确初始化

### 2. TypeError: Cannot read property XXX of undefined

**可能原因**：
- 对象未正确初始化
- 异步操作未完成就访问数据
- 可选链未正确使用

**解决方案**：
```typescript
// 使用可选链
const value = object?.property?.subProperty

// 或添加空值检查
if (object && object.property) {
  const value = object.property
}
```

### 3. 应用崩溃

**排查方法**：
1. 查看 `runlog.txt` 日志文件
2. 定位崩溃的代码位置
3. 检查是否有未捕获的异常
4. 确认所有异步操作都有错误处理

## 性能问题

### 1. 页面卡顿

**可能原因**：
- 过度渲染
- 状态更新频率过高
- 大量同步计算

**解决方案**：
```typescript
// 使用防抖
private debounce(func: Function, wait: number): Function {
  let timeout: number | null = null
  return (...args: any[]) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func.apply(this, args), wait)
  }
}

// 使用 computed 缓存计算结果
```

### 2. 内存泄漏

**排查方法**：
1. 检查是否正确清理定时器
2. 检查事件监听器是否正确移除
3. 检查是否有循环引用
4. 检查大对象是否正确释放

## API 相关问题

### 1. API 版本不兼容

**检查方法**：
```bash
# 查看 API 文档
# 确保使用的 API <= 22
```

**常见高版本 API**：
- `router.pushUrl` (已弃用) → 使用 `router.push`
- `router.getState` (已弃用) → 使用新的路由 API

### 2. 权限被拒绝

**解决方案**：
1. 检查 `module.json5` 中的权限声明
2. 检查权限请求代码
3. 检查用户是否手动拒绝了权限

### 3. 数据库操作失败

**常见原因**：
- RdbStore 未初始化
- SQL 语法错误
- 数据库版本不匹配

**排查步骤**：
```typescript
try {
  // 添加详细日志
  console.log('[Database] Executing query:', sql)
  await this.rdbStore.executeSql(sql)
  console.log('[Database] Query executed successfully')
} catch (error) {
  console.error('[Database] Query failed:', error)
  console.error('[Database] SQL:', sql)
  console.error('[Database] Error code:', error.code)
  console.error('[Database] Error message:', error.message)
}
```

## 调试技巧

### 1. 使用 hilog

```typescript
import { hilog } from '@kit.PerformanceAnalysisKit'

const DOMAIN = 0x0001

hilog.debug(DOMAIN, 'TAG', 'Debug message: %{public}s', 'value')
hilog.info(DOMAIN, 'TAG', 'Info message')
hilog.warn(DOMAIN, 'TAG', 'Warning message')
hilog.error(DOMAIN, 'TAG', 'Error message: %{public}s', JSON.stringify(error))
```

### 2. 使用 DevEco Studio 调试器

1. 在代码行号左侧点击设置断点
2. 点击 Debug 按钮启动调试
3. 使用 Step Over/Step Into 逐行执行
4. 查看变量值和调用栈

### 3. 使用日志定位问题

```typescript
// 添加函数入口/出口日志
async function myFunction() {
  console.log('[MyFunction] Enter')
  try {
    // 业务逻辑
    console.log('[MyFunction] Step 1 completed')
    // ...
    console.log('[MyFunction] Exit successfully')
  } catch (error) {
    console.error('[MyFunction] Error:', error)
    throw error
  }
}
```

## 常见陷阱

### 1. this 指向问题

```typescript
// 错误
class MyClass {
  private value: string = 'test'

  problematicMethod() {
    setTimeout(function() {
      console.log(this.value)  // this 指向错误
    }, 100)
  }
}

// 正确
class MyClass {
  private value: string = 'test'

  correctMethod() {
    setTimeout(() => {
      console.log(this.value)  // 箭头函数保持 this 指向
    }, 100)
  }
}
```

### 2. 异步操作处理

```typescript
// 错误 - 没有等待异步完成
async loadData() {
  this.data = this.fetchData()  // 返回 Promise，不是数据
}

// 正确
async loadData() {
  this.data = await this.fetchData()  // 等待异步完成
}
```

### 3. 状态更新不触发 UI 刷新

```typescript
// 错误 - 直接修改数组元素
this.items[0].name = 'new name'

// 正确 - 创建新数组
const newItems = [...this.items]
newItems[0] = { ...newItems[0], name: 'new name' }
this.items = newItems
```
