# 常见问题 FAQ

本文档收集了 ark-layer 框架使用过程中的常见问题及解答。

## 目录

- [Service 相关](#service-相关)
- [生命周期相关](#生命周期相关)
- [依赖管理相关](#依赖管理相关)
- [Phase 和场景相关](#phase-和场景相关)
- [页面使用相关](#页面使用相关)
- [ArkTS 语法相关](#arkts-语法相关)
- [架构设计相关](#架构设计相关)
- [错误处理相关](#错误处理相关)

## Service 相关

### Q: Service 之间如何通信？

**A:** 通过构造函数声明依赖，然后直接调用依赖服务的方法。

```typescript
export class UserService extends Service {
  private authService: AuthService

  constructor(services: Service[] = []) {
    super(services)

    this.authService = this.depServices.find(
      s => s.constructor.name === 'AuthService'
    ) as AuthService
  }

  async getCurrentUser(): Promise<UserInfo | null> {
    // 直接调用依赖服务的方法
    const token = this.authService.getToken()
    if (!token) {
      return null
    }

    return await this.fetchUserInfo(token)
  }
}
```

### Q: 如何在 UI 中获取 Service？

**A:** 使用 `serviceManager.get<ServiceName>('ServiceName')`。

```typescript
import { serviceManager } from '../core/ServiceManager'
import { UserService } from '../domain/user/UserService'

@Entry
@Component
struct Index {
  private userService: UserService = serviceManager.get<UserService>('UserService')!

  aboutToAppear(): void {
    const user = this.userService.getUserInfo('user123')
  }

  build() {
    Text('Hello World')
  }
}
```

### Q: Service 可以是单例吗？

**A:** 是的，通过 ServiceManager 管理的 Service 默认就是单例。不要在代码中手动 `new Service()`，始终通过 ServiceManager 获取。

```typescript
// ❌ 错误：手动创建实例
const userService = new UserService([])

// ✅ 正确：从 ServiceManager 获取
const userService = serviceManager.get<UserService>('UserService')
```

### Q: 如何在 Service 中使用上下文？

**A:** 在 `init()` 方法及之后可以安全使用 `this.context`。

```typescript
init(): void {
  // ✅ 可以安全使用上下文
  const filesDir = this.context.filesDir
  const cacheDir = this.context.cacheDir

  console.log('Files dir:', filesDir)
  console.log('Cache dir:', cacheDir)
}
```

### Q: Service 可以在构造函数中使用上下文吗？

**A:** 不可以。构造函数执行时上下文尚未初始化，必须在 `init()` 方法中使用。

```typescript
constructor(services: Service[] = []) {
  super(services)

  // ❌ 错误：此时 this.context 未初始化
  // const filesDir = this.context.filesDir
}

init(): void {
  // ✅ 正确：此时可以安全使用上下文
  const filesDir = this.context.filesDir
}
```

## 生命周期相关

### Q: init() 和 load() 的区别？

**A:**

| 特性 | init() | load() |
|------|--------|--------|
| 执行时机 | 注册后立即 | 登录时触发 |
| 同步/异步 | 同步 | 异步 |
| 可用上下文 | ✅ | ✅ |
| 网络IO | ❌ 严禁 | ✅ 可以 |
| 数据库操作 | ❌ 严禁 | ✅ 可以 |
| 用途 | 初始化成员属性 | 加载数据 |

```typescript
init(): void {
  // ✅ 初始化成员属性
  this.cache = new Map()

  // ❌ 不能有网络IO
  // await this.networkService.get('/data')
}

async load(): Promise<boolean> {
  // ✅ 可以进行网络IO
  const response = await this.networkService.get('/data')
  return true
}
```

### Q: 如何切换企业/账号重新加载？

**A:** 调用 `serviceManager.loginCallback()` 重新触发所有 `load()`。

```typescript
// 切换账号
async switchAccount(newAccountId: string): Promise<void> {
  // 1. 清理当前账号数据
  await serviceManager.logoutCallback()

  // 2. 更新账号信息
  this.currentAccountId = newAccountId

  // 3. 重新加载所有服务
  await serviceManager.loginCallback()
}
```

### Q: unload() 什么时候被调用？

**A:** 当调用 `serviceManager.logoutCallback()` 时会触发所有 Service 的 `unload()` 方法。

```typescript
// 在 EntryAbility 中
onDestroy(): void {
  // 清理所有服务
  serviceManager.logoutCallback()
}
```

### Q: Service 加载失败会怎样？

**A:** 取决于失败的服务。如果被其他服务依赖，依赖它的服务的 `load()` 也会失败。

```typescript
// AuthService 加载失败
// UserService 依赖 AuthService，UserService.load() 也会受影响

async load(): Promise<boolean> {
  const authResult = await this.authService.load()
  if (!authResult) {
    console.error('Auth service failed, user service cannot load')
    return false  // 返回 false
  }

  // 继续加载
  return true
}
```

## 依赖管理相关

### Q: 检测到循环依赖怎么办？

**A:** 重构服务职责，引入中间服务，或使用事件机制解耦。

```typescript
// ❌ 循环依赖
// A → B → C → A

// ✅ 解决方案 1：重构服务职责
// A → B
// A → C
// B 和 C 不再相互依赖

// ✅ 解决方案 2：引入中间服务
// A → B → M → C
// A → C

// ✅ 解决方案 3：使用事件机制
// A 发布事件，C 订阅事件
// 不再直接依赖
```

### Q: 如何检查是否有循环依赖？

**A:** ServiceManager 会自动检测并抛出异常。

```typescript
// 如果存在循环依赖，会在注册时报错
// Error: Circular dependency detected: A -> B -> C -> A

// 检查依赖关系的工具方法
function checkCircularDependency(): void {
  const services = serviceManager.getAllServices()
  const visited = new Set<string>()
  const recursionStack = new Set<string>()

  function dfs(serviceName: string): boolean {
    if (recursionStack.has(serviceName)) {
      console.error(`Circular dependency detected: ${serviceName}`)
      return true
    }

    if (visited.has(serviceName)) {
      return false
    }

    visited.add(serviceName)
    recursionStack.add(serviceName)

    const service = serviceManager.get(serviceName)
    if (service) {
      const dependencies = service.depServices
      for (const dep of dependencies) {
        if (dfs(dep.constructor.name)) {
          return true
        }
      }
    }

    recursionStack.delete(serviceName)
    return false
  }

  services.forEach(service => {
    if (dfs(service.constructor.name)) {
      return
    }
  })
}
```

### Q: 依赖的服务未初始化怎么办？

**A:** 确保在 XXXApp.ets 中按正确的顺序注册服务，或在 Phase 中正确声明依赖。

```typescript
// ❌ 错误：UserService 注册在 StorageService 之前
serviceManager.load({
  phase: BUSINESS_PHASE,
  sceneList: [
    new UserService([storageService])  // StorageService 还未注册
  ]
})

serviceManager.load({
  phase: GLOBAL_PHASE,
  sceneList: [
    new StorageService([])
  ]
})

// ✅ 正确：先注册 StorageService
serviceManager.load({
  phase: GLOBAL_PHASE,
  sceneList: [
    new StorageService([])
  ]
})

serviceManager.load({
  phase: BUSINESS_PHASE,
  sceneList: [
    new UserService([
      serviceManager.get<StorageService>('StorageService')
    ])
  ]
})
```

## Phase 和场景相关

### Q: 如何选择合适的 Phase？

**A:** 使用以下决策树：

```
是否是应用启动必须的服务？
├─ 是 → GLOBAL_PHASE
└─ 否 → 是否是核心业务逻辑？
    ├─ 是 → BUSINESS_PHASE
    └─ 否 → 是否是重量级或非关键服务？
        ├─ 是 → LAZY_PHASE
        └─ 否 → FEATURE_PHASE
```

**典型示例**：
- ConfigService → GLOBAL_PHASE
- UserService → BUSINESS_PHASE
- AnalyticsService → FEATURE_PHASE
- ReportService → LAZY_PHASE

### Q: 如何创建自定义 Phase？

**A:** 使用 `createPhase` 函数。

```typescript
import { createPhase } from '../core/DefaultPhases'

const CUSTOM_PHASE = createPhase({
  name: 'CUSTOM',
  priority: 25,           // 在 BUSINESS(20) 和 FEATURE(30) 之间
  waitForComplete: false, // 并行触发，不等待完成
  description: '自定义阶段'
})

export { CUSTOM_PHASE }
```

### Q: 并行 Phase 中的服务有依赖怎么办？

**A:** 通过构造函数声明依赖，框架会自动确保依赖服务先完成。

```typescript
// 即使都在 FEATURE_PHASE (并行)
// AnalyticsService 仍会等待 UserService 完成

serviceManager.load({
  phase: FEATURE_PHASE,
  sceneList: [
    new AnalyticsService([
      serviceManager.get<UserService>('UserService')  // 声明依赖
    ])
  ]
})
```

### Q: 如何延迟加载某些功能？

**A:** 将 Service 放在 LAZY_PHASE，或按需加载。

```typescript
// 方式 1：使用 LAZY_PHASE
serviceManager.load({
  phase: LAZY_PHASE,
  sceneList: [
    new ReportService([])
  ]
})

// 方式 2：按需加载
@Entry
@Component
struct ReportPage {
  private reportService?: ReportService

  aboutToAppear(): void {
    // 首次使用时才加载
    if (!this.reportService) {
      this.reportService = serviceManager.get<ReportService>('ReportService')
    }
  }
}
```

## 页面使用相关

### Q: 页面中可以创建 Service 实例吗？

**A:** 不可以。始终通过 ServiceManager 获取 Service。

```typescript
// ❌ 错误
private userService = new UserService([])

// ✅ 正确
private userService: UserService = serviceManager.get<UserService>('UserService')!
```

### Q: 如何在多个页面共享状态？

**A:** 使用 Service 作为状态管理中心。

```typescript
// StateService.ets
export class StateService extends Service {
  private state: Map<string, any> = new Map()

  get(key: string): any {
    return this.state.get(key)
  }

  set(key: string, value: any): void {
    this.state.set(key, value)
  }
}

// PageA.ets
@Component
struct PageA {
  private stateService = serviceManager.get<StateService>('StateService')!

  build() {
    Button('Set Value')
      .onClick(() => {
        this.stateService.set('key', 'value')
      })
  }
}

// PageB.ets
@Component
struct PageB {
  private stateService = serviceManager.get<StateService>('StateService')!

  aboutToAppear(): void {
    const value = this.stateService.get('key')
    console.log('Value:', value)
  }

  build() {
    Text('Page B')
  }
}
```

### Q: 页面卸载时需要清理 Service 吗？

**A:** 不需要。Service 由 ServiceManager 统一管理，页面只需要清理自己的资源。

```typescript
@Entry
@Component
struct Index {
  private timer: number = -1

  aboutToAppear(): void {
    // 启动定时器
    this.timer = setInterval(() => {
      // 定时任务
    }, 1000)
  }

  aboutToDisappear(): void {
    // 清理页面资源
    if (this.timer !== -1) {
      clearInterval(this.timer)
    }

    // 不需要清理 Service，ServiceManager 会管理
  }

  build() {
    Text('Hello World')
  }
}
```

## ArkTS 语法相关

### Q: 为什么不能用对象展开运算符？

**A:** ArkTS 是 TypeScript 的严格子集，为了优化性能和内存管理，禁用了一些语法。使用 `Object.assign` 或手动复制代替。

```typescript
// ❌ 错误
const newObj = { ...oldObj, prop: 'value' }

// ✅ 正确
const newObj = Object.assign({}, oldObj, { prop: 'value' })
```

### Q: 为什么不能用解构赋值？

**A:** 同上，使用点语法代替。

```typescript
// ❌ 错误
const { name, age } = user

// ✅ 正确
const name = user.name
const age = user.age
```

### Q: 如何在 ArkTS 中合并对象？

**A:** 使用 `Object.assign` 或手动复制。

```typescript
// 方式 1：Object.assign
const merged = Object.assign({}, obj1, obj2, { prop: 'value' })

// 方式 2：手动复制
const merged: Record<string, any> = {}
Object.keys(obj1).forEach(key => {
  merged[key] = obj1[key]
})
Object.keys(obj2).forEach(key => {
  merged[key] = obj2[key]
})
merged['prop'] = 'value'
```

## 架构设计相关

### Q: Domain 层可以依赖 Infra 层吗？

**A:** 可以，这是允许的依赖方向。

```
core ← infra ← domain ← pages
```

```typescript
// ✅ 正确：Domain 依赖 Infra
export class UserService extends Service {
  private storageService: StorageService  // Infra 层
  private networkService: NetworkService  // Infra 层

  constructor(services: Service[] = []) {
    super(services)

    this.storageService = this.depServices.find(
      s => s.constructor.name === 'StorageService'
    ) as StorageService

    this.networkService = this.depServices.find(
      s => s.constructor.name === 'NetworkService'
    ) as NetworkService
  }
}
```

### Q: Infra 层可以依赖 Domain 层吗？

**A:** 不可以，这违反了分层原则。

```typescript
// ❌ 错误：Infra 依赖 Domain
export class NetworkService extends Service {
  private userService: UserService  // Domain 层

  async request(url: string): Promise<any> {
    const user = this.userService.getCurrentUser()  // ❌ 错误
    // ...
  }
}

// ✅ 正确：将用户信息作为参数传入
export class NetworkService extends Service {
  async request(url: string, userId: string): Promise<any> {
    const headers = { 'X-User-Id': userId }
    // ...
  }
}
```

### Q: Service 应该放在哪个目录？

**A:** 根据服务职责决定：

- **core/**: 框架核心（Service、ServiceManager）
- **infra/**: 基础设施（Storage、Network、Database）
- **domain/**: 业务逻辑（User、Auth、Focus）
- **pages/**: 仅 UI 组件，不包含 Service

### Q: 如何验证代码是否符合分层规范？

**A:** 使用以下检查清单：

**core/ 层**：
- [ ] 不包含业务逻辑
- [ ] 不依赖 infra、domain、pages 层

**infra/ 层**：
- [ ] 无状态的工具类
- [ ] 不依赖 domain、pages 层

**domain/ 层**：
- [ ] 按业务领域划分
- [ ] 不依赖 pages 层

**pages/ 层**：
- [ ] 仅包含 UI 组件
- [ ] 通过 ServiceManager 获取服务

## 错误处理相关

### Q: Service 的 load() 失败了怎么办？

**A:** 在 `load()` 中使用 try-catch，返回 `false` 表示失败。

```typescript
async load(): Promise<boolean> {
  try {
    const response = await this.networkService.get('/data')
    if (response.success) {
      return true
    }
    return false
  } catch (error) {
    console.error('Load failed:', error)
    return false  // 返回 false
  }
}
```

### Q: 如何处理 Service 加载失败？

**A:** 在依赖该 Service 的其他 Service 中处理。

```typescript
async load(): Promise<boolean> {
  try {
    // 检查依赖服务是否加载成功
    const authLoaded = await this.authService.load()
    if (!authLoaded) {
      console.error('Auth service failed, cannot load user service')
      return false
    }

    // 继续加载
    const response = await this.networkService.get('/user/profile')
    return response.success
  } catch (error) {
    console.error('Load failed:', error)
    return false
  }
}
```

### Q: 为什么不能用 throw 语句？

**A:** ArkTS 不支持 throw 语句，使用返回值表示错误。

```typescript
// ❌ 错误
function validate(input: string): void {
  if (!input) {
    throw new Error('Input is required')
  }
}

// ✅ 正确
function validate(input: string): boolean {
  if (!input) {
    console.error('Input is required')
    return false
  }
  return true
}
```

### Q: 如何实现错误重试机制？

**A:** 在 `load()` 中实现重试逻辑。

```typescript
async load(): Promise<boolean> {
  const maxRetries = 3
  const retryDelay = 2000

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await this.networkService.get('/data')
      if (response.success) {
        return true
      }
    } catch (error) {
      console.error(`Attempt ${attempt} failed:`, error)

      if (attempt < maxRetries) {
        await this.delay(retryDelay)
      }
    }
  }

  return false
}

private delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}
```

## 其他问题

### Q: 如何调试 Service 的加载过程？

**A:** 在生命周期方法中添加日志。

```typescript
init(): void {
  console.log(`[${this.constructor.name}] init() called`)
}

async load(): Promise<boolean> {
  console.log(`[${this.constructor.name}] load() started`)
  // ...
  console.log(`[${this.constructor.name}] load() completed`)
  return true
}

async unload(): Promise<boolean> {
  console.log(`[${this.constructor.name}] unload() called`)
  // ...
  return true
}
```

### Q: 如何查看所有已注册的 Service？

**A:** 使用 ServiceManager 提供的方法。

```typescript
// 获取所有 Service
const allServices = serviceManager.getAllServices()
allServices.forEach(service => {
  console.log('Registered service:', service.constructor.name)
})

// 检查特定 Service 是否存在
const userService = serviceManager.get<UserService>('UserService')
if (userService) {
  console.log('UserService is registered')
} else {
  console.log('UserService is not registered')
}
```

### Q: 如何实现 Service 的热重载？

**A:** ark-layer 不支持热重载，需要重启应用。但在开发时可以使用快速刷新。

```typescript
// 在开发模式下
if (isDevelopmentMode) {
  // 重新加载 Service
  await serviceManager.logoutCallback()
  await serviceManager.loginCallback()
}
```

### Q: 如何性能优化 Service 的加载？

**A:**

1. **合理划分 Phase**：将非关键服务放在 FEATURE_PHASE 或 LAZY_PHASE
2. **并行加载**：利用 FEATURE_PHASE 和 LAZY_PHASE 的并行特性
3. **延迟加载**：不常用的功能放在 LAZY_PHASE
4. **缓存数据**：在 `unload()` 中缓存数据，加速下次 `load()`

```typescript
// 性能优化示例
serviceManager.load({
  phase: GLOBAL_PHASE,      // 关键服务，串行
  sceneList: [new ConfigService([])]
})

serviceManager.load({
  phase: BUSINESS_PHASE,    // 核心业务，串行
  sceneList: [new UserService([])]
})

serviceManager.load({
  phase: FEATURE_PHASE,     // 辅助功能，并行
  sceneList: [
    new AnalyticsService([]),
    new LogService([])
  ]
})

serviceManager.load({
  phase: LAZY_PHASE,        // 延迟加载，并行
  sceneList: [new ReportService([])]
})
```

## 返回主文档

[返回 SKILL.md](../SKILL.md)
