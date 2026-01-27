# 特殊场景处理

本文档提供 ark-layer 框架中常见特殊场景的处理方案和最佳实践。

## 目录

- [Service 需要在登录前加载数据](#场景1service-需要在登录前加载数据)
- [Service 依赖关系复杂](#场景2service-依赖关系复杂)
- [需要在登出时持久化数据](#场景3需要在登出时持久化数据)
- [Service 需要监听系统事件](#场景4service-需要监听系统事件)
- [并行加载的服务有依赖](#场景5并行加载的服务有依赖)
- [Service 需要定时刷新数据](#场景6service-需要定时刷新数据)
- [Service 需要处理大量数据](#场景7service-需要处理大量数据)
- [需要在多个页面共享状态](#场景8需要在多个页面共享状态)
- [Service 加载失败需要重试](#场景9service-加载失败需要重试)
- [需要延迟加载某些功能](#场景10需要延迟加载某些功能)

## 场景 1：Service 需要在登录前加载数据

### 问题描述

某些配置或数据需要在用户登录前就准备好，例如应用配置、主题设置等。

### 解决方案

使用 `init()` 方法而不是 `load()` 方法，因为 `init()` 在 Service 注册时立即执行。

### 代码示例

```typescript
// entry/src/main/ets/domain/config/ConfigService.ets
import { Service } from '../../core/Service'

export class ConfigService extends Service {
  private static readonly TAG = 'ConfigService'
  private config: AppConfig = {
    theme: 'light',
    language: 'zh-CN',
    apiBaseUrl: 'https://api.example.com'
  }

  constructor(services: Service[] = []) {
    super(services)
  }

  init(): void {
    console.log(`[${ConfigService.TAG}] Initializing...`)

    // ✅ 在 init() 中读取本地配置文件
    const configData = this.readConfigFromFile()

    if (configData) {
      this.config = configData
    }

    console.log(`[${ConfigService.TAG}] Config loaded:`, this.config)
  }

  async load(): Promise<boolean> {
    // load() 可以为空或仅做验证
    console.log(`[${ConfigService.TAG}] Loading...`)
    return true
  }

  async unload(): Promise<boolean> {
    console.log(`[${ConfigService.TAG}] Unloading...`)

    // 保存配置到文件
    this.saveConfigToFile(this.config)

    return true
  }

  private readConfigFromFile(): AppConfig | null {
    try {
      // 从文件读取配置
      const configPath = `${this.context.filesDir}/config.json`
      // 实现文件读取逻辑
      return null  // 简化示例
    } catch (error) {
      console.error('Read config failed:', error)
      return null
    }
  }

  private saveConfigToFile(config: AppConfig): void {
    try {
      // 保存配置到文件
      const configPath = `${this.context.filesDir}/config.json`
      // 实现文件写入逻辑
    } catch (error) {
      console.error('Save config failed:', error)
    }
  }

  getConfig(): AppConfig {
    return this.config
  }

  updateConfig(config: Partial<AppConfig>): void {
    this.config = Object.assign({}, this.config, config)
  }
}

interface AppConfig {
  theme: string
  language: string
  apiBaseUrl: string
}
```

## 场景 2：Service 依赖关系复杂

### 问题描述

Service 之间存在复杂的依赖链，需要确保正确的加载顺序。

### 解决方案

创建依赖关系图，确保依赖链清晰，并在 XXXApp.ets 中按正确顺序注册。

### 依赖关系示例

```
FocusService
  ↓
UserService → AuthService
  ↓              ↓
StorageService  NetworkService
  ↓
DatabaseService
```

### 代码示例

```typescript
// entry/src/main/ets/MyApp.ets
export class MyApp {
  static async init(context: Context): Promise<void> {
    serviceManager.register(context)

    // 1. 加载最底层的服务
    serviceManager.load({
      phase: GLOBAL_PHASE,
      sceneList: [
        new DatabaseService([]),
        new StorageService([])
      ]
    })

    // 2. 加载基础设施服务
    serviceManager.load({
      phase: GLOBAL_PHASE,
      sceneList: [
        new NetworkService([
          serviceManager.get<DatabaseService>('DatabaseService')
        ])
      ]
    })

    // 3. 加载认证服务
    serviceManager.load({
      phase: BUSINESS_PHASE,
      sceneList: [
        new AuthService([
          serviceManager.get<StorageService>('StorageService'),
          serviceManager.get<NetworkService>('NetworkService')
        ])
      ]
    })

    // 4. 加载用户服务（依赖 AuthService）
    serviceManager.load({
      phase: BUSINESS_PHASE,
      sceneList: [
        new UserService([
          serviceManager.get<AuthService>('AuthService'),
          serviceManager.get<StorageService>('StorageService')
        ])
      ]
    })

    // 5. 加载专注服务（依赖 UserService）
    serviceManager.load({
      phase: BUSINESS_PHASE,
      sceneList: [
        new FocusService([
          serviceManager.get<UserService>('UserService')
        ])
      ]
    })

    await serviceManager.loginCallback()
  }
}
```

## 场景 3：需要在登出时持久化数据

### 问题描述

用户登出时需要保存当前状态，以便下次登录时恢复。

### 解决方案

在 `unload()` 方法中持久化数据到本地存储。

### 代码示例

```typescript
// entry/src/main/ets/domain/user/UserService.ets
export class UserService extends Service {
  private users: Map<string, UserInfo> = new Map()
  private currentUser: UserInfo | null = null
  private userSettings: UserSettings = {
    theme: 'light',
    language: 'zh-CN',
    notifications: true
  }

  async unload(): Promise<boolean> {
    try {
      console.log('[UserService] Unloading...')

      // 1. 持久化用户数据
      const userData = JSON.stringify(Array.from(this.users.values()))
      await this.storageService.save('users', userData)

      // 2. 持久化当前用户信息
      if (this.currentUser) {
        await this.storageService.save('current_user', JSON.stringify(this.currentUser))
      }

      // 3. 持久化用户设置
      await this.storageService.save('user_settings', JSON.stringify(this.userSettings))

      // 4. 清理内存
      this.users.clear()
      this.currentUser = null

      console.log('[UserService] Unloaded successfully')
      return true
    } catch (error) {
      console.error('[UserService] Unload failed:', error)
      return false
    }
  }

  async load(): Promise<boolean> {
    try {
      console.log('[UserService] Loading...')

      // 1. 恢复用户数据
      const userData = await this.storageService.get('users')
      if (userData) {
        const userArray: UserInfo[] = JSON.parse(userData)
        userArray.forEach(user => {
          this.users.set(user.id, user)
        })
      }

      // 2. 恢复当前用户
      const currentUserData = await this.storageService.get('current_user')
      if (currentUserData) {
        this.currentUser = JSON.parse(currentUserData)
      }

      // 3. 恢复用户设置
      const settingsData = await this.storageService.get('user_settings')
      if (settingsData) {
        this.userSettings = JSON.parse(settingsData)
      }

      console.log('[UserService] Loaded successfully')
      return true
    } catch (error) {
      console.error('[UserService] Load failed:', error)
      return false
    }
  }
}
```

## 场景 4：Service 需要监听系统事件

### 问题描述

Service 需要监听系统事件（如网络变化、屏幕旋转等）。

### 解决方案

在 `init()` 中注册监听器，在 `unload()` 中取消注册。

### 代码示例

```typescript
// entry/src/main/ets/domain/network/NetworkMonitorService.ets
export class NetworkMonitorService extends Service {
  private static readonly TAG = 'NetworkMonitorService'
  private networkState: NetworkState = {
    isConnected: true,
    type: 'wifi'
  }
  private listeners: Array<(state: NetworkState) => void> = []

  init(): void {
    console.log(`[${NetworkMonitorService.TAG}] Initializing...`)

    // 注册网络状态监听器
    this.registerNetworkListener()

    console.log(`[${NetworkMonitorService.TAG}] Initialized`)
  }

  async unload(): Promise<boolean> {
    console.log(`[${NetworkMonitorService.TAG}] Unloading...`)

    // 取消网络状态监听器
    this.unregisterNetworkListener()

    // 清理监听器
    this.listeners = []

    console.log(`[${NetworkMonitorService.TAG}] Unloaded successfully`)
    return true
  }

  private registerNetworkListener(): void {
    // 使用 HarmonyOS 网络管理 API
    // 注意：这里使用伪代码，实际 API 需要根据 HarmonyOS 文档调整
    /*
    connection.on('networkChange', (data) => {
      this.networkState = {
        isConnected: data.isConnected,
        type: data.type
      }

      // 通知所有监听器
      this.notifyListeners(this.networkState)

      console.log('[NetworkMonitorService] Network state changed:', this.networkState)
    })
    */
  }

  private unregisterNetworkListener(): void {
    // 取消网络状态监听
    /*
    connection.off('networkChange')
    */
  }

  private notifyListeners(state: NetworkState): void {
    this.listeners.forEach(listener => {
      try {
        listener(state)
      } catch (error) {
        console.error('[NetworkMonitorService] Listener error:', error)
      }
    })
  }

  getNetworkState(): NetworkState {
    return this.networkState
  }

  addListener(listener: (state: NetworkState) => void): void {
    this.listeners.push(listener)
  }

  removeListener(listener: (state: NetworkState) => void): void {
    const index = this.listeners.indexOf(listener)
    if (index !== -1) {
      this.listeners.splice(index, 1)
    }
  }
}

interface NetworkState {
  isConnected: boolean
  type: string
}
```

## 场景 5：并行加载的服务有依赖

### 问题描述

即使多个 Service 在同一个 Phase（并行触发），它们之间仍有依赖关系。

### 解决方案

通过构造函数声明依赖，框架会自动确保依赖服务先完成。

### 代码示例

```typescript
// 即使都在 FEATURE_PHASE (waitForComplete: false)
// AnalyticsService 仍会等待 UserService 完成

// entry/src/main/ets/MyApp.ets
serviceManager.load({
  phase: FEATURE_PHASE,
  sceneList: [
    new AnalyticsService([
      serviceManager.get<UserService>('UserService')  // 声明依赖
    ]),
    new LogService([])  // 不依赖其他服务
  ]
})

// 执行顺序：
// 1. 两者同时触发 init()
// 2. UserService.load() 和 LogService.load() 同时触发
// 3. AnalyticsService.load() 等待 UserService.load() 完成
// 4. LogService.load() 不等待任何服务
```

## 场景 6：Service 需要定时刷新数据

### 问题描述

Service 需要定期从服务器获取最新数据，但不影响用户操作。

### 解决方案

在 `init()` 中启动定时器，在 `unload()` 中取消。

### 代码示例

```typescript
// entry/src/main/ets/domain/sync/SyncService.ets
export class SyncService extends Service {
  private static readonly TAG = 'SyncService'
  private syncInterval: number = 60000  // 60秒
  private timer: number = -1
  private isSyncing: boolean = false

  constructor(services: Service[] = []) {
    super(services)
  }

  init(): void {
    console.log(`[${SyncService.TAG}] Initializing...`)

    // 启动定时同步
    this.startSyncTimer()

    console.log(`[${SyncService.TAG}] Initialized`)
  }

  async unload(): Promise<boolean> {
    console.log(`[${SyncService.TAG}] Unloading...`)

    // 停止定时同步
    this.stopSyncTimer()

    console.log(`[${SyncService.TAG}] Unloaded successfully`)
    return true
  }

  private startSyncTimer(): void {
    if (this.timer !== -1) {
      return  // 已经在运行
    }

    console.log(`[${SyncService.TAG}] Starting sync timer...`)

    this.timer = setInterval(() => {
      this.syncData()
    }, this.syncInterval)
  }

  private stopSyncTimer(): void {
    if (this.timer !== -1) {
      clearInterval(this.timer)
      this.timer = -1
      console.log(`[${SyncService.TAG}] Sync timer stopped`)
    }
  }

  private async syncData(): Promise<void> {
    if (this.isSyncing) {
      console.log(`[${SyncService.TAG}] Sync already in progress, skipping...`)
      return
    }

    this.isSyncing = true
    console.log(`[${SyncService.TAG}] Starting data sync...`)

    try {
      // 同步用户数据
      await this.syncUserData()

      // 同步配置数据
      await this.syncConfigData()

      console.log(`[${SyncService.TAG}] Data sync completed`)
    } catch (error) {
      console.error(`[${SyncService.TAG}] Sync failed:`, error)
    } finally {
      this.isSyncing = false
    }
  }

  private async syncUserData(): Promise<void> {
    // 实现用户数据同步逻辑
  }

  private async syncConfigData(): Promise<void> {
    // 实现配置数据同步逻辑
  }

  // 手动触发同步
  async manualSync(): Promise<boolean> {
    await this.syncData()
    return true
  }
}
```

## 场景 7：Service 需要处理大量数据

### 问题描述

Service 需要加载或处理大量数据，可能导致性能问题。

### 解决方案

使用分页加载、懒加载或异步处理。

### 代码示例

```typescript
// entry/src/main/ets/domain/data/DataService.ets
export class DataService extends Service {
  private static readonly TAG = 'DataService'
  private pageSize: number = 50
  private cache: Map<string, any[]> = new Map()

  async loadData(category: string, page: number = 1): Promise<any[]> {
    try {
      console.log(`[${DataService.TAG}] Loading ${category}, page ${page}...`)

      // 检查缓存
      const cacheKey = `${category}_${page}`
      if (this.cache.has(cacheKey)) {
        console.log(`[${DataService.TAG}] Cache hit for ${cacheKey}`)
        return this.cache.get(cacheKey)!
      }

      // 从网络加载数据
      const response = await this.networkService.get(`/data/${category}`, {
        page: page,
        pageSize: this.pageSize
      })

      if (response.success && response.data) {
        // 缓存数据
        this.cache.set(cacheKey, response.data)

        // 限制缓存大小
        if (this.cache.size > 100) {
          const firstKey = this.cache.keys().next().value
          this.cache.delete(firstKey)
        }

        return response.data
      }

      return []
    } catch (error) {
      console.error(`[${DataService.TAG}] Load failed:`, error)
      return []
    }
  }

  async loadAllData(category: string): Promise<any[]> {
    console.log(`[${DataService.TAG}] Loading all data for ${category}...`)

    const allData: any[] = []
    let page = 1
    let hasMore = true

    while (hasMore) {
      const data = await this.loadData(category, page)

      if (data.length > 0) {
        allData.push(...data)
        page++

        // 如果返回的数据少于页大小，说明没有更多数据了
        if (data.length < this.pageSize) {
          hasMore = false
        }
      } else {
        hasMore = false
      }
    }

    console.log(`[${DataService.TAG}] Loaded ${allData.length} items for ${category}`)
    return allData
  }

  clearCache(): void {
    this.cache.clear()
    console.log(`[${DataService.TAG}] Cache cleared`)
  }
}
```

## 场景 8：需要在多个页面共享状态

### 问题描述

多个页面需要访问和修改同一份数据，需要保持状态同步。

### 解决方案

使用 Service 作为状态管理中心，页面通过 ServiceManager 获取 Service。

### 代码示例

```typescript
// entry/src/main/ets/domain/state/StateService.ets
export class StateService extends Service {
  private static readonly TAG = 'StateService'
  private state: Map<string, any> = new Map()
  private listeners: Map<string, Array<(value: any) => void>> = new Map()

  get(key: string): any | undefined {
    return this.state.get(key)
  }

  set(key: string, value: any): void {
    const oldValue = this.state.get(key)
    this.state.set(key, value)

    // 通知监听器
    this.notifyListeners(key, value, oldValue)
  }

  subscribe(key: string, listener: (value: any) => void): () => void {
    if (!this.listeners.has(key)) {
      this.listeners.set(key, [])
    }

    this.listeners.get(key)!.push(listener)

    // 返回取消订阅函数
    return () => {
      this.unsubscribe(key, listener)
    }
  }

  private unsubscribe(key: string, listener: (value: any) => void): void {
    const listeners = this.listeners.get(key)
    if (listeners) {
      const index = listeners.indexOf(listener)
      if (index !== -1) {
        listeners.splice(index, 1)
      }
    }
  }

  private notifyListeners(key: string, newValue: any, oldValue: any): void {
    const listeners = this.listeners.get(key)
    if (listeners) {
      listeners.forEach(listener => {
        try {
          listener(newValue)
        } catch (error) {
          console.error(`[${StateService.TAG}] Listener error:`, error)
        }
      })
    }
  }
}

// 在页面中使用
// entry/src/main/ets/pages/PageA.ets
@Entry
@Component
struct PageA {
  @State counter: number = 0
  private stateService: StateService = serviceManager.get<StateService>('StateService')!
  private unsubscribe?: () => void

  aboutToAppear(): void {
    // 获取初始值
    this.counter = this.stateService.get('counter') || 0

    // 订阅变化
    this.unsubscribe = this.stateService.subscribe('counter', (value) => {
      this.counter = value
    })
  }

  aboutToDisappear(): void {
    // 取消订阅
    if (this.unsubscribe) {
      this.unsubscribe()
    }
  }

  build() {
    Column() {
      Text(`Counter: ${this.counter}`)
        .fontSize(24)

      Button('Increment')
        .onClick(() => {
          const newValue = this.counter + 1
          this.stateService.set('counter', newValue)
        })
    }
  }
}
```

## 场景 9：Service 加载失败需要重试

### 问题描述

Service 加载可能因为网络问题失败，需要自动重试。

### 解决方案

在 `load()` 方法中实现重试逻辑。

### 代码示例

```typescript
// entry/src/main/ets/domain/user/UserService.ets
export class UserService extends Service {
  private static readonly TAG = 'UserService'
  private maxRetries: number = 3
  private retryDelay: number = 2000  // 2秒

  async load(): Promise<boolean> {
    console.log(`[${UserService.TAG}] Loading...`)

    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        console.log(`[${UserService.TAG}] Load attempt ${attempt}/${this.maxRetries}`)

        const response = await this.networkService.get('/user/profile')

        if (response.success && response.data) {
          this.userProfile = response.data
          console.log(`[${UserService.TAG}] Loaded successfully`)
          return true
        }

        console.error(`[${UserService.TAG}] Invalid response`)
      } catch (error) {
        console.error(`[${UserService.TAG}] Load attempt ${attempt} failed:`, error)

        // 如果还有重试次数，等待后重试
        if (attempt < this.maxRetries) {
          console.log(`[${UserService.TAG}] Retrying in ${this.retryDelay}ms...`)
          await this.delay(this.retryDelay)
        }
      }
    }

    // 所有重试都失败
    console.error(`[${UserService.TAG}] All load attempts failed`)
    return false
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}
```

## 场景 10：需要延迟加载某些功能

### 问题描述

某些功能不常用或比较重量级，希望延迟到用户真正需要时才加载。

### 解决方案

将 Service 放在 LAZY_PHASE，或按需加载。

### 代码示例

```typescript
// entry/src/main/ets/MyApp.ets
export class MyApp {
  static async init(context: Context): Promise<void> {
    serviceManager.register(context)

    // 加载核心服务
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

    // 延迟加载重量级服务
    serviceManager.load({
      phase: LAZY_PHASE,
      sceneList: [
        new ReportService([]),
        new BackupService([])
      ]
    })

    await serviceManager.loginCallback()
  }
}

// 或者在需要时才加载
// entry/src/main/ets/pages/ReportPage.ets
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

  build() {
    // 页面内容
  }
}
```

## 返回主文档

[返回 SKILL.md](../SKILL.md)
