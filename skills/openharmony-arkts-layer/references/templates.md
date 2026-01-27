# 代码模板

本文档提供 ark-layer 框架中常用的代码模板，帮助快速生成符合规范的代码。

## 目录

- [标准 Service 模板](#标准-service-模板)
- [应用层编排模板](#应用层编排模板)
- [自定义 Phase 模板](#自定义-phase-模板)
- [页面组件模板](#页面组件模板)

## 标准 Service 模板

### 基础版本（无依赖）

```typescript
// entry/src/main/ets/domain/example/ExampleService.ets
import { Service } from '../../core/Service'

export class ExampleService extends Service {
  private static readonly TAG = 'ExampleService'
  private data: Map<string, any> = new Map()

  constructor(services: Service[] = []) {
    super(services)
  }

  /**
   * 初始化阶段（同步）
   * 可安全获取上下文，初始化成员属性
   * 注意：严禁网络IO
   */
  init(): void {
    console.log(`[${ExampleService.TAG}] Initializing...`)

    // 初始化成员属性
    this.data = new Map()

    console.log(`[${ExampleService.TAG}] Initialized`)
  }

  /**
   * 加载阶段（异步）
   * 登录时自动触发，可进行网络IO
   * 依赖的服务会自动先完成
   */
  async load(): Promise<boolean> {
    try {
      console.log(`[${ExampleService.TAG}] Loading...`)

      // 从数据库或网络加载数据
      // const response = await this.networkService.get('/data')
      // this.data = new Map(Object.entries(response.data))

      console.log(`[${ExampleService.TAG}] Loaded successfully`)
      return true
    } catch (error) {
      console.error(`[${ExampleService.TAG}] Load failed: ${error}`)
      return false
    }
  }

  /**
   * 卸载阶段（异步）
   * 登出时自动触发，清理资源
   */
  async unload(): Promise<boolean> {
    try {
      console.log(`[${ExampleService.TAG}] Unloading...`)

      // 清理资源
      this.data.clear()

      console.log(`[${ExampleService.TAG}] Unloaded successfully`)
      return true
    } catch (error) {
      console.error(`[${ExampleService.TAG}] Unload failed: ${error}`)
      return false
    }
  }

  /**
   * 业务方法示例
   */
  getData(key: string): any | undefined {
    return this.data.get(key)
  }

  async setData(key: string, value: any): Promise<boolean> {
    try {
      this.data.set(key, value)
      return true
    } catch (error) {
      console.error(`[${ExampleService.TAG}] Set data failed: ${error}`)
      return false
    }
  }
}
```

### 带依赖的版本

```typescript
// entry/src/main/ets/domain/user/UserService.ets
import { Service } from '../../core/Service'
import { StorageService } from '../../infra/storage/StorageService'
import { NetworkService } from '../../infra/network/NetworkService'

export class UserService extends Service {
  private static readonly TAG = 'UserService'
  private users: Map<string, UserInfo> = new Map()
  private storageService: StorageService
  private networkService: NetworkService

  constructor(services: Service[] = []) {
    super(services)

    // 获取依赖的服务
    this.storageService = this.depServices.find(
      s => s.constructor.name === 'StorageService'
    ) as StorageService

    this.networkService = this.depServices.find(
      s => s.constructor.name === 'NetworkService'
    ) as NetworkService
  }

  init(): void {
    console.log(`[${UserService.TAG}] Initializing...`)

    // 初始化用户缓存
    this.users = new Map()

    console.log(`[${UserService.TAG}] Initialized`)
  }

  async load(): Promise<boolean> {
    try {
      console.log(`[${UserService.TAG}] Loading...`)

      // 从本地存储加载缓存的用户数据
      const cachedUsers = await this.storageService.get('users')
      if (cachedUsers) {
        const userArray: UserInfo[] = JSON.parse(cachedUsers)
        userArray.forEach(user => {
          this.users.set(user.id, user)
        })
      }

      // 从网络加载最新用户数据
      const response = await this.networkService.get('/users')
      if (response.success && response.data) {
        response.data.forEach((user: UserInfo) => {
          this.users.set(user.id, user)
        })

        // 缓存到本地存储
        await this.storageService.save('users', JSON.stringify(response.data))
      }

      console.log(`[${UserService.TAG}] Loaded successfully, count: ${this.users.size}`)
      return true
    } catch (error) {
      console.error(`[${UserService.TAG}] Load failed: ${error}`)
      return false
    }
  }

  async unload(): Promise<boolean> {
    try {
      console.log(`[${UserService.TAG}] Unloading...`)

      // 持久化用户数据
      const userArray = Array.from(this.users.values())
      await this.storageService.save('users', JSON.stringify(userArray))

      // 清理内存
      this.users.clear()

      console.log(`[${UserService.TAG}] Unloaded successfully`)
      return true
    } catch (error) {
      console.error(`[${UserService.TAG}] Unload failed: ${error}`)
      return false
    }
  }

  /**
   * 获取用户信息
   */
  getUserInfo(userId: string): UserInfo | undefined {
    return this.users.get(userId)
  }

  /**
   * 获取所有用户
   */
  getAllUsers(): UserInfo[] {
    return Array.from(this.users.values())
  }

  /**
   * 更新用户信息
   */
  async updateUserInfo(userId: string, info: UserInfo): Promise<boolean> {
    try {
      // 更新内存
      this.users.set(userId, info)

      // 同步到服务器
      const response = await this.networkService.put(`/users/${userId}`, info)
      if (response.success) {
        // 更新本地缓存
        await this.storageService.save('users', JSON.stringify(Array.from(this.users.values())))
        return true
      }

      return false
    } catch (error) {
      console.error(`[${UserService.TAG}] Update user failed: ${error}`)
      return false
    }
  }
}

// 类型定义
interface UserInfo {
  id: string
  name: string
  email: string
  avatar?: string
}
```

### Infra 层服务模板

```typescript
// entry/src/main/ets/infra/storage/StorageService.ets
import { Service } from '../../core/Service'

export class StorageService extends Service {
  private static readonly TAG = 'StorageService'
  private preferences: preferences.Preferences | null = null

  constructor(services: Service[] = []) {
    super(services)
  }

  init(): void {
    console.log(`[${StorageService.TAG}] Initializing...`)

    // 获取 Preferences 实例
    const options: preferences.Options = { name: 'MyAppStore' }
    preferences.getPreferences(this.context, options)
      .then(pref => {
        this.preferences = pref
        console.log(`[${StorageService.TAG}] Preferences initialized`)
      })
      .catch((error: Error) => {
        console.error(`[${StorageService.TAG}] Init failed: ${error}`)
      })
  }

  async load(): Promise<boolean> {
    console.log(`[${StorageService.TAG}] Loading...`)
    console.log(`[${StorageService.TAG}] Loaded successfully`)
    return true
  }

  async unload(): Promise<boolean> {
    console.log(`[${StorageService.TAG}] Unloading...`)

    // 关闭 Preferences
    if (this.preferences) {
      try {
        await preferences.deletePreferences(this.context, 'MyAppStore')
        this.preferences = null
      } catch (error) {
        console.error(`[${StorageService.TAG}] Close failed: ${error}`)
      }
    }

    console.log(`[${StorageService.TAG}] Unloaded successfully`)
    return true
  }

  /**
   * 保存数据
   */
  async save(key: string, value: string): Promise<boolean> {
    if (!this.preferences) {
      console.error(`[${StorageService.TAG}] Preferences not initialized`)
      return false
    }

    try {
      await this.preferences.put(key, value)
      await this.preferences.flush()
      return true
    } catch (error) {
      console.error(`[${StorageService.TAG}] Save failed: ${error}`)
      return false
    }
  }

  /**
   * 获取数据
   */
  async get(key: string): Promise<string | undefined> {
    if (!this.preferences) {
      console.error(`[${StorageService.TAG}] Preferences not initialized`)
      return undefined
    }

    try {
      return await this.preferences.get(key, '') as string
    } catch (error) {
      console.error(`[${StorageService.TAG}] Get failed: ${error}`)
      return undefined
    }
  }

  /**
   * 删除数据
   */
  async remove(key: string): Promise<boolean> {
    if (!this.preferences) {
      console.error(`[${StorageService.TAG}] Preferences not initialized`)
      return false
    }

    try {
      await this.preferences.delete(key)
      await this.preferences.flush()
      return true
    } catch (error) {
      console.error(`[${StorageService.TAG}] Remove failed: ${error}`)
      return false
    }
  }
}
```

## 应用层编排模板

### 最小化版本

```typescript
// entry/src/main/ets/MyApp.ets
import { serviceManager } from './core/ServiceManager'
import { GLOBAL_PHASE, BUSINESS_PHASE } from './core/DefaultPhases'
import { StorageService } from './infra/storage/StorageService'
import { UserService } from './domain/user/UserService'

export class MyApp {
  static async init(context: Context): Promise<void> {
    console.log('[MyApp] Initializing application...')

    // 1. 注册应用上下文
    serviceManager.register(context)

    // 2. 加载全局核心服务
    serviceManager.load({
      phase: GLOBAL_PHASE,
      sceneList: [
        new StorageService([])
      ]
    })

    // 3. 加载业务服务
    serviceManager.load({
      phase: BUSINESS_PHASE,
      sceneList: [
        new UserService([
          serviceManager.get<StorageService>('StorageService')
        ])
      ]
    })

    // 4. 触发登录流程
    await serviceManager.loginCallback()

    console.log('[MyApp] Application initialized')
  }
}
```

### 完整版本

```typescript
// entry/src/main/ets/MyApp.ets
import { serviceManager } from './core/ServiceManager'
import { GLOBAL_PHASE, BUSINESS_PHASE, FEATURE_PHASE, LAZY_PHASE } from './core/DefaultPhases'
import { ConfigService } from './infra/config/ConfigService'
import { DatabaseService } from './infra/database/DatabaseService'
import { StorageService } from './infra/storage/StorageService'
import { NetworkService } from './infra/network/NetworkService'
import { AuthService } from './domain/auth/AuthService'
import { UserService } from './domain/user/UserService'
import { FocusService } from './domain/focus/FocusService'
import { AnalyticsService } from './domain/analytics/AnalyticsService'
import { LogService } from './domain/log/LogService'
import { ReportService } from './domain/report/ReportService'

export class MyApp {
  private static readonly TAG = 'MyApp'

  /**
   * 初始化应用
   * 在 EntryAbility.onCreate() 中调用
   */
  static async init(context: Context): Promise<void> {
    console.log(`[${MyApp.TAG}] Initializing application...`)

    // 1. 注册应用上下文
    serviceManager.register(context)

    // 2. 加载全局核心服务（串行等待完成）
    serviceManager.load({
      phase: GLOBAL_PHASE,
      sceneList: [
        new ConfigService([]),
        new DatabaseService([]),
        new StorageService([])
      ]
    })

    // 3. 加载基础设施服务（串行等待完成）
    serviceManager.load({
      phase: GLOBAL_PHASE,
      sceneList: [
        new NetworkService([
          serviceManager.get<ConfigService>('ConfigService')
        ])
      ]
    })

    // 4. 加载业务核心服务（串行等待完成）
    serviceManager.load({
      phase: BUSINESS_PHASE,
      sceneList: [
        new AuthService([
          serviceManager.get<StorageService>('StorageService'),
          serviceManager.get<NetworkService>('NetworkService')
        ]),
        new UserService([
          serviceManager.get<AuthService>('AuthService'),
          serviceManager.get<StorageService>('StorageService')
        ]),
        new FocusService([
          serviceManager.get<UserService>('UserService')
        ])
      ]
    })

    // 5. 加载功能服务（并行触发）
    serviceManager.load({
      phase: FEATURE_PHASE,
      sceneList: [
        new AnalyticsService([
          serviceManager.get<UserService>('UserService')
        ]),
        new LogService([])
      ]
    })

    // 6. 加载延迟服务（并行触发）
    serviceManager.load({
      phase: LAZY_PHASE,
      sceneList: [
        new ReportService([
          serviceManager.get<FocusService>('FocusService')
        ])
      ]
    })

    // 7. 触发登录流程（多阶段自动加载）
    await serviceManager.loginCallback()

    console.log(`[${MyApp.TAG}] Application initialized`)
  }
}
```

### 在 EntryAbility 中调用

```typescript
// entry/src/main/ets/EntryAbility.ets
import { MyApp } from '../MyApp'

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    console.log('[EntryAbility] onCreate')
    MyApp.init(this.context)
  }

  onDestroy(): void {
    console.log('[EntryAbility] onDestroy')
    serviceManager.logoutCallback()
  }

  onForeground(): void {
    console.log('[EntryAbility] onForeground')
  }

  onBackground(): void {
    console.log('[EntryAbility] onBackground')
  }
}
```

## 自定义 Phase 模板

### 创建自定义 Phase

```typescript
// entry/src/main/ets/domain/cache/CachePhase.ets
import { createPhase } from '../../core/DefaultPhases'

// 创建自定义缓存服务阶段
export const CACHE_PHASE = createPhase({
  name: 'CACHE',
  priority: 25,           // 在 BUSINESS(20) 和 FEATURE(30) 之间
  waitForComplete: false, // 并行触发，不等待完成
  description: '缓存服务阶段，并行加载'
})
```

### 使用自定义 Phase

```typescript
// entry/src/main/ets/MyApp.ets
import { CACHE_PHASE } from './domain/cache/CachePhase'
import { CacheService } from './domain/cache/CacheService'
import { ImageCacheService } from './domain/cache/ImageCacheService'

export class MyApp {
  static async init(context: Context): Promise<void> {
    serviceManager.register(context)

    // ... 加载其他阶段 ...

    // 使用自定义阶段
    serviceManager.load({
      phase: CACHE_PHASE,
      sceneList: [
        new CacheService([]),
        new ImageCacheService([])
      ]
    })

    await serviceManager.loginCallback()
  }
}
```

## 页面组件模板

### 基础页面

```typescript
// entry/src/main/ets/pages/Index.ets
import { serviceManager } from '../core/ServiceManager'
import { UserService } from '../domain/user/UserService'

@Entry
@Component
struct Index {
  @State message: string = 'Hello World'
  private userService: UserService = serviceManager.get<UserService>('UserService')!

  aboutToAppear(): void {
    console.log('[Index] aboutToAppear')

    // 使用 Service
    const userInfo = this.userService.getUserInfo('user123')
    if (userInfo) {
      this.message = `Welcome, ${userInfo.name}!`
    }
  }

  build() {
    Row() {
      Column() {
        Text(this.message)
          .fontSize(24)
          .fontWeight(FontWeight.Bold)
          .margin({ top: 20, bottom: 20 })
      }
      .width('100%')
    }
    .height('100%')
  }
}
```

### 带列表的页面

```typescript
// entry/src/main/ets/pages/UserList.ets
import { serviceManager } from '../core/ServiceManager'
import { UserService } from '../domain/user/UserService'

@Entry
@Component
struct UserList {
  @State users: UserInfo[] = []
  private userService: UserService = serviceManager.get<UserService>('UserService')!

  aboutToAppear(): void {
    console.log('[UserList] aboutToAppear')

    // 加载用户列表
    this.users = this.userService.getAllUsers()
  }

  build() {
    Column() {
      Text('User List')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 20, bottom: 20 })

      List({ space: 10 }) {
        ForEach(this.users, (user: UserInfo) => {
          ListItem() {
            this.UserItem(user)
          }
        })
      }
      .width('100%')
      .layoutWeight(1)
      .padding({ left: 16, right: 16 })
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  UserItem(user: UserInfo) {
    Row() {
      Text(user.name)
        .fontSize(18)
        .layoutWeight(1)

      Text(user.email)
        .fontSize(14)
        .fontColor('#999999')
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#FFFFFF')
    .borderRadius(8)
  }
}

interface UserInfo {
  id: string
  name: string
  email: string
}
```

### 带状态管理的页面

```typescript
// entry/src/main/ets/pages/FocusTimer.ets
import { serviceManager } from '../core/ServiceManager'
import { FocusService } from '../domain/focus/FocusService'

@Entry
@Component
struct FocusTimer {
  @State focusTime: number = 0  // 专注时间（秒）
  @State isRunning: boolean = false
  private focusService: FocusService = serviceManager.get<FocusService>('FocusService')!
  private timer: number = -1

  aboutToAppear(): void {
    console.log('[FocusTimer] aboutToAppear')

    // 加载当前专注时间
    this.focusTime = this.focusService.getCurrentTime()
  }

  aboutToDisappear(): void {
    console.log('[FocusTimer] aboutToDisappear')

    // 清理定时器
    if (this.timer !== -1) {
      clearInterval(this.timer)
      this.timer = -1
    }
  }

  build() {
    Column() {
      Text('Focus Timer')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 40, bottom: 40 })

      Text(`${this.formatTime(this.focusTime)}`)
        .fontSize(48)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 40 })

      Row({ space: 20 }) {
        Button('Start')
          .enabled(!this.isRunning)
          .onClick(() => {
            this.startTimer()
          })

        Button('Stop')
          .enabled(this.isRunning)
          .onClick(() => {
            this.stopTimer()
          })

        Button('Reset')
          .onClick(() => {
            this.resetTimer()
          })
      }
    }
    .width('100%')
    .height('100%')
  }

  private startTimer(): void {
    this.isRunning = true
    this.timer = setInterval(() => {
      this.focusTime++
    }, 1000)
  }

  private stopTimer(): void {
    this.isRunning = false
    if (this.timer !== -1) {
      clearInterval(this.timer)
      this.timer = -1
    }
  }

  private resetTimer(): void {
    this.stopTimer()
    this.focusTime = 0
  }

  private formatTime(seconds: number): string {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60

    if (hours > 0) {
      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    } else {
      return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    }
  }
}
```

## 使用说明

### 1. Service 生成步骤

1. 根据需求选择合适的模板
2. 替换 `ExampleService` 为实际的 Service 名称
3. 根据业务需求实现方法
4. 确定依赖关系并在构造函数中声明
5. 在 `MyApp.ets` 中注册到合适的 Phase

### 2. 页面使用步骤

1. 在页面顶部导入 `serviceManager`
2. 通过 `serviceManager.get<ServiceName>('ServiceName')` 获取服务
3. 在 `aboutToAppear()` 中初始化数据
4. 在 `build()` 方法中使用数据
5. 在 `aboutToDisappear()` 中清理资源（如有需要）

### 3. 代码生成命令示例

```
创建一个 UserProfileService
生成一个订单管理 OrderService
创建一个依赖 StorageService 的 CacheService
```

## 返回主文档

[返回 SKILL.md](../SKILL.md)
