# Service 生命周期详解

## Service 基类

所有 Service 必须继承 `Service` 抽象类，位于 `core/Service.ets`：

```typescript
// core/Service.ets
export abstract class Service {
  protected depServices: Service[]
  protected context: Context

  constructor(services: Service[] = []) {
    this.depServices = services
  }

  abstract init(): void
  abstract load(): Promise<boolean>
  abstract unload(): Promise<boolean>
}
```

## 生命周期阶段

Service 的生命周期分为四个阶段：

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  NONE    │ -> │INITIALIZED│ -> │ WORKING  │ -> │INITIALIZED│
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                   (init)         (load)         (unload)
```

### 1. 构造阶段

**触发时机**：创建 Service 实例时

**职责**：
- 声明依赖关系
- 调用父类构造函数

**示例**：

```typescript
export class UserService extends Service {
  private storageService: StorageService
  private networkService: NetworkService

  constructor(services: Service[] = []) {
    super(services)  // 必须调用父类构造函数

    // 获取依赖的服务
    this.storageService = this.depServices.find(
      s => s.constructor.name === 'StorageService'
    ) as StorageService

    this.networkService = this.depServices.find(
      s => s.constructor.name === 'NetworkService'
    ) as NetworkService

    // ❌ 错误：此时不能使用上下文
    // this.context 还未初始化
  }
}
```

**注意事项**：
- ✅ 必须调用 `super(services)`
- ✅ 从 `depServices` 中获取依赖
- ❌ 不能使用 `this.context`（尚未初始化）
- ❌ 不能进行任何初始化操作

### 2. 初始化阶段 (init)

**触发时机**：Service 注册到 ServiceManager 后立即执行

**职责**：
- 初始化成员属性
- 获取并存储上下文
- 注册监听器
- **严禁网络IO**

**示例**：

```typescript
init(): void {
  // ✅ 可以安全使用上下文
  const filesDir = this.context.filesDir

  // ✅ 初始化成员属性
  this.configPath = `${filesDir}/config.json`
  this.cache = new Map<string, any>()

  // ✅ 注册监听器
  this.registerEventListener()

  console.log(`[${this.constructor.name}] Initialized`)
}
```

**注意事项**：
- ✅ 同步执行
- ✅ 可以使用 `this.context`
- ✅ 可以初始化成员属性
- ✅ 可以注册监听器
- ❌ **严禁网络IO**
- ❌ 不能使用 `async/await`

### 3. 加载阶段 (load)

**触发时机**：调用 `serviceManager.loginCallback()` 时

**职责**：
- 从网络或数据库加载数据
- 初始化业务状态
- 进行耗时操作

**示例**：

```typescript
async load(): Promise<boolean> {
  try {
    console.log(`[${this.constructor.name}] Loading...`)

    // ✅ 可以进行网络IO
    const response = await this.networkService.get('/user/profile')
    if (response.success) {
      this.userProfile = response.data
    }

    // ✅ 可以读取本地数据
    const cachedData = await this.storageService.get('cache')
    if (cachedData) {
      this.cache = new Map(JSON.parse(cachedData))
    }

    // ✅ 可以进行复杂的计算
    this.processData()

    console.log(`[${this.constructor.name}] Loaded successfully`)
    return true  // ✅ 成功返回 true
  } catch (error) {
    console.error(`[${this.constructor.name}] Load failed: ${error}`)
    return false  // ❌ 失败返回 false
  }
}
```

**注意事项**：
- ✅ 异步执行
- ✅ 可以进行网络IO
- ✅ 可以进行数据库操作
- ✅ 可以进行耗时计算
- ✅ 依赖的服务会自动先完成
- ❌ 不能抛出异常（使用 try-catch）
- ✅ 必须返回 `Promise<boolean>`

### 4. 卸载阶段 (unload)

**触发时机**：调用 `serviceManager.logoutCallback()` 时

**职责**：
- 清理资源
- 持久化数据
- 取消监听器
- 重置状态

**示例**：

```typescript
async unload(): Promise<boolean> {
  try {
    console.log(`[${this.constructor.name}] Unloading...`)

    // ✅ 持久化数据
    const cacheData = JSON.stringify(Array.from(this.cache.entries()))
    await this.storageService.save('cache', cacheData)

    // ✅ 清理内存
    this.userProfile = undefined
    this.cache.clear()

    // ✅ 取消监听器
    this.unregisterEventListener()

    console.log(`[${this.constructor.name}] Unloaded successfully`)
    return true  // ✅ 成功返回 true
  } catch (error) {
    console.error(`[${this.constructor.name}] Unload failed: ${error}`)
    return false  // ❌ 失败返回 false
  }
}
```

**注意事项**：
- ✅ 异步执行
- ✅ 应该清理所有资源
- ✅ 应该持久化重要数据
- ✅ 应该取消监听器
- ❌ 不能抛出异常（使用 try-catch）
- ✅ 必须返回 `Promise<boolean>`

## 生命周期方法对比

| 特性 | init() | load() | unload() |
|------|--------|--------|----------|
| 执行时机 | 注册后立即 | 登录时 | 登出时 |
| 同步/异步 | 同步 | 异步 | 异步 |
| 可用上下文 | ✅ | ✅ | ✅ |
| 网络IO | ❌ | ✅ | ✅ |
| 数据库操作 | ❌ | ✅ | ✅ |
| 返回值 | void | Promise<boolean> | Promise<boolean> |
| 异常处理 | 不抛异常 | 不抛异常 | 不抛异常 |

## 依赖关系处理

### 依赖声明

通过构造函数参数声明依赖：

```typescript
export class UserService extends Service {
  private authService: AuthService
  private storageService: StorageService

  constructor(services: Service[] = []) {
    super(services)

    // 方式 1：通过构造函数名称查找
    this.authService = this.depServices.find(
      s => s.constructor.name === 'AuthService'
    ) as AuthService

    // 方式 2：通过类型判断（如果 Service 有类型标识）
    this.storageService = this.depServices.find(
      s => s instanceof StorageService
    ) as StorageService
  }
}
```

### 依赖加载顺序

依赖的服务会自动先完成 `load()`：

```typescript
// UserService 依赖 AuthService
// 在 XXXApp.ets 中：
new UserService([
  serviceManager.get<AuthService>('AuthService')
])

// 执行顺序：
// 1. AuthService.init()
// 2. UserService.init()
// 3. AuthService.load()
// 4. UserService.load()  // AuthService.load() 完成后才执行
```

### 循环依赖检测

框架会自动检测循环依赖：

```typescript
// ❌ 错误：循环依赖
// A → B → C → A

new ServiceA([serviceB])
new ServiceB([serviceC])
new ServiceC([serviceA])

// 框架会抛出异常：Circular dependency detected
```

## 常见场景

### 场景 1：需要在登录前加载数据

**问题**：某些数据需要在用户登录前就准备好

**解决方案**：使用 `init()` 而不是 `load()`

```typescript
export class ConfigService extends Service {
  private config: AppConfig

  init(): void {
    // ✅ 在 init() 中读取本地配置
    const configData = this.context.resourceManager.getRawFileContent('config.json')
    this.config = JSON.parse(configData)
  }

  async load(): Promise<boolean> {
    // load() 可以为空或仅做验证
    return true
  }
}
```

### 场景 2：需要在多个阶段加载数据

**问题**：某些数据需要分阶段加载

**解决方案**：在 `load()` 中使用 Promise.all 或顺序加载

```typescript
async load(): Promise<boolean> {
  try {
    // 阶段 1：加载基础数据
    const basicData = await this.networkService.get('/user/basic')
    this.basicInfo = basicData.data

    // 阶段 2：加载详细数据
    const detailData = await this.networkService.get('/user/detail')
    this.detailInfo = detailData.data

    // 阶段 3：加载扩展数据（并行）
    const [extensions, preferences] = await Promise.all([
      this.networkService.get('/user/extensions'),
      this.networkService.get('/user/preferences')
    ])

    this.extensions = extensions.data
    this.preferences = preferences.data

    return true
  } catch (error) {
    console.error('Load failed:', error)
    return false
  }
}
```

### 场景 3：需要在卸载时保存状态

**问题**：用户登出时需要保存当前状态

**解决方案**：在 `unload()` 中持久化数据

```typescript
async unload(): Promise<boolean> {
  try {
    // 保存用户当前状态
    const state = {
      lastView: this.currentView,
      scrollPosition: this.scrollPosition,
      selectedItems: Array.from(this.selectedItems)
    }

    await this.storageService.save('user_state', JSON.stringify(state))

    // 清理内存
    this.currentView = null
    this.scrollPosition = 0
    this.selectedItems.clear()

    return true
  } catch (error) {
    console.error('Unload failed:', error)
    return false
  }
}
```

### 场景 4：需要在后台定期刷新数据

**问题**：需要定期更新数据，但不影响用户操作

**解决方案**：在 `init()` 中启动定时器，在 `unload()` 中取消

```typescript
export class DataService extends Service {
  private timer: number | null = null

  init(): void {
    // 启动定时器
    this.timer = setInterval(() => {
      this.refreshData()
    }, 60000)  // 每分钟刷新
  }

  async refreshData(): Promise<void> {
    try {
      const data = await this.networkService.get('/data/latest')
      this.updateData(data)
    } catch (error) {
      console.error('Refresh failed:', error)
    }
  }

  async unload(): Promise<boolean> {
    // 取消定时器
    if (this.timer !== null) {
      clearInterval(this.timer)
      this.timer = null
    }
    return true
  }
}
```

## 最佳实践

### 1. init() 最佳实践

```typescript
init(): void {
  // ✅ 初始化成员属性
  this.cache = new Map()
  this.config = this.loadConfig()

  // ✅ 注册监听器
  this.context.eventHub.on('event', this.handleEvent)

  // ❌ 不要在 init() 中进行网络IO
  // await this.networkService.get('/config')

  // ❌ 不要在 init() 中抛出异常
  // if (!this.config) throw new Error('Config not found')
}
```

### 2. load() 最佳实践

```typescript
async load(): Promise<boolean> {
  try {
    // ✅ 使用 try-catch 捕获异常
    const data = await this.networkService.get('/data')

    // ✅ 验证数据
    if (!data || !data.success) {
      console.error('Invalid data')
      return false
    }

    // ✅ 处理数据
    this.processData(data.data)

    // ✅ 返回成功
    return true
  } catch (error) {
    // ✅ 记录错误
    console.error('Load failed:', error)

    // ✅ 返回失败（不要抛出异常）
    return false
  }
}
```

### 3. unload() 最佳实践

```typescript
async unload(): Promise<boolean> {
  try {
    // ✅ 持久化重要数据
    await this.saveState()

    // ✅ 清理资源
    this.cache.clear()
    this.context.eventHub.off('event', this.handleEvent)

    // ✅ 取消定时器
    if (this.timer) {
      clearInterval(this.timer)
    }

    // ✅ 返回成功
    return true
  } catch (error) {
    console.error('Unload failed:', error)
    return false
  }
}
```

## 返回主文档

[返回 SKILL.md](../SKILL.md)
