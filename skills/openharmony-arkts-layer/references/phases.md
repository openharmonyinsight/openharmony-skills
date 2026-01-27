# 多阶段加载系统

## Phase 机制概述

ark-layer 使用 Phase（阶段）机制来控制 Service 的加载顺序和并发策略。通过将 Service 分配到不同的 Phase，可以：

1. **控制加载顺序**：确保关键服务先加载
2. **优化启动性能**：并行加载非关键服务
3. **灵活配置**：根据业务需求调整加载策略

## 预定义阶段

框架在 `core/DefaultPhases.ets` 中定义了四个预定义阶段：

```typescript
import { GLOBAL_PHASE, BUSINESS_PHASE, FEATURE_PHASE, LAZY_PHASE } from '../core/DefaultPhases'
```

### 1. GLOBAL_PHASE

**优先级**：10
**执行策略**：串行等待
**用途**：全局核心服务

**特性**：
- 最高优先级，最先加载
- 串行执行，等待所有服务完成
- 适用于应用启动必须的服务

**典型服务**：
- `ConfigService` - 配置服务
- `DatabaseService` - 数据库服务
- `StorageService` - 存储服务

**示例**：

```typescript
serviceManager.load({
  phase: GLOBAL_PHASE,
  sceneList: [
    new ConfigService([]),
    new DatabaseService([]),
    new StorageService([])
  ]
})

// 执行顺序（串行）：
// 1. ConfigService.init() → ConfigService.load()
// 2. DatabaseService.init() → DatabaseService.load()
// 3. StorageService.init() → StorageService.load()
// 等待所有完成后，才进入下一阶段
```

### 2. BUSINESS_PHASE

**优先级**：20
**执行策略**：串行等待
**用途**：业务核心服务

**特性**：
- 高优先级，在 GLOBAL_PHASE 之后加载
- 串行执行，等待所有服务完成
- 适用于核心业务逻辑服务

**典型服务**：
- `AuthService` - 认证服务
- `UserService` - 用户服务
- `FocusService` - 专注服务

**示例**：

```typescript
serviceManager.load({
  phase: BUSINESS_PHASE,
  sceneList: [
    new AuthService([
      serviceManager.get<StorageService>('StorageService')
    ]),
    new UserService([
      serviceManager.get<AuthService>('AuthService')
    ])
  ]
})

// 执行顺序（串行）：
// 1. AuthService.init() → AuthService.load()
// 2. UserService.init() → UserService.load()
// UserService 会等待 AuthService.load() 完成
```

### 3. FEATURE_PHASE

**优先级**：30
**执行策略**：并行触发
**用途**：功能服务

**特性**：
- 中等优先级，在 BUSINESS_PHASE 之后加载
- 并行触发，不等待完成（默认）
- 适用于辅助功能服务

**典型服务**：
- `AnalyticsService` - 统计分析服务
- `NotificationService` - 通知服务
- `LogService` - 日志服务

**示例**：

```typescript
serviceManager.load({
  phase: FEATURE_PHASE,
  sceneList: [
    new AnalyticsService([]),
    new NotificationService([]),
    new LogService([])
  ]
})

// 执行顺序（并行）：
// 所有服务的 init() 和 load() 同时触发
// 不等待任何服务完成
```

### 4. LAZY_PHASE

**优先级**：40
**执行策略**：并行触发
**用途**：延迟加载服务

**特性**：
- 最低优先级，最后加载
- 并行触发，不等待完成
- 适用于非关键或重量级服务

**典型服务**：
- `ReportService` - 报表服务
- `BackupService` - 备份服务
- `SyncService` - 同步服务

**示例**：

```typescript
serviceManager.load({
  phase: LAZY_PHASE,
  sceneList: [
    new ReportService([]),
    new BackupService([])
  ]
})

// 执行顺序（并行）：
// 在前面所有阶段完成后才触发
// 不等待完成
```

## 阶段对比表

| 阶段 | 优先级 | 执行策略 | 等待完成 | 典型用途 |
|------|--------|----------|----------|----------|
| GLOBAL_PHASE | 10 | 串行 | ✅ | 全局核心服务 |
| BUSINESS_PHASE | 20 | 串行 | ✅ | 业务核心服务 |
| FEATURE_PHASE | 30 | 并行 | ❌ | 辅助功能服务 |
| LAZY_PHASE | 40 | 并行 | ❌ | 延迟加载服务 |

## 自定义阶段

如果预定义阶段不满足需求，可以创建自定义阶段：

### 创建自定义阶段

```typescript
import { createPhase } from '../core/DefaultPhases'

// 创建在 BUSINESS_PHASE 和 FEATURE_PHASE 之间的阶段
const CACHE_PHASE = createPhase({
  name: 'CACHE',
  priority: 25,           // 在 BUSINESS(20) 和 FEATURE(30) 之间
  waitForComplete: false, // 并行触发，不等待完成
  description: '缓存服务阶段'
})

export { CACHE_PHASE }
```

### 使用自定义阶段

```typescript
import { CACHE_PHASE } from './domain/cache/CachePhase'

serviceManager.load({
  phase: CACHE_PHASE,
  sceneList: [
    new CacheService([]),
    new ImageCacheService([])
  ]
})
```

### 阶段优先级规则

1. **优先级越小越先执行**：priority 10 → 20 → 30 → 40
2. **相同优先级按注册顺序执行**
3. **自定义阶段可以插入到任何位置**

```typescript
// 示例：插入自定义阶段
GLOBAL_PHASE (priority: 10)
  ↓
BUSINESS_PHASE (priority: 20)
  ↓
CACHE_PHASE (priority: 25)  // 自定义阶段
  ↓
FEATURE_PHASE (priority: 30)
  ↓
LAZY_PHASE (priority: 40)
```

## 应用层编排

### 完整的应用初始化示例

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
  static async init(context: Context): Promise<void> {
    // 1. 注册应用上下文
    serviceManager.register(context)

    // 2. 加载全局核心服务（串行等待）
    serviceManager.load({
      phase: GLOBAL_PHASE,
      sceneList: [
        new ConfigService([]),
        new DatabaseService([]),
        new StorageService([])
      ]
    })

    // 3. 加载基础设施服务（串行等待）
    serviceManager.load({
      phase: GLOBAL_PHASE,
      sceneList: [
        new NetworkService([
          serviceManager.get<ConfigService>('ConfigService')
        ])
      ]
    })

    // 4. 加载业务核心服务（串行等待）
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

    // 7. 触发登录流程
    await serviceManager.loginCallback()
  }
}
```

### 在 EntryAbility 中调用

```typescript
// entry/src/main/ets/EntryAbility.ets
import { MyApp } from '../MyApp'

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    // 异步初始化应用
    MyApp.init(this.context)
  }

  onDestroy(): void {
    // 清理资源
    serviceManager.logoutCallback()
  }
}
```

## 执行流程图

```
serviceManager.register(context)
  ↓
┌─────────────────────────────────────┐
│ GLOBAL_PHASE (串行等待)              │
│ - ConfigService.init() → load()     │
│ - DatabaseService.init() → load()   │
│ - StorageService.init() → load()    │
│ - NetworkService.init() → load()    │
└─────────────────────────────────────┘
  ↓ (等待所有完成)
┌─────────────────────────────────────┐
│ BUSINESS_PHASE (串行等待)            │
│ - AuthService.init() → load()       │
│ - UserService.init() → load()       │
│   (等待 AuthService.load() 完成)    │
│ - FocusService.init() → load()      │
│   (等待 UserService.load() 完成)    │
└─────────────────────────────────────┘
  ↓ (等待所有完成)
┌─────────────────────────────────────┐
│ FEATURE_PHASE (并行触发)             │
│ - AnalyticsService.init() → load()  │
│ - LogService.init() → load()        │
│ (不等待完成，立即触发下一阶段)       │
└─────────────────────────────────────┘
  ↓ (立即触发，不等待)
┌─────────────────────────────────────┐
│ LAZY_PHASE (并行触发)                │
│ - ReportService.init() → load()     │
└─────────────────────────────────────┘
  ↓
serviceManager.loginCallback()
  (等待所有依赖的 load() 完成)
```

## 依赖关系与阶段

### 跨阶段依赖

```typescript
// UserService (BUSINESS_PHASE) 依赖 StorageService (GLOBAL_PHASE)
new UserService([
  serviceManager.get<StorageService>('StorageService')  // ✅ 正确
])

// 执行顺序：
// 1. StorageService.load() (GLOBAL_PHASE) 先完成
// 2. UserService.load() (BUSINESS_PHASE) 后执行
```

### 同阶段依赖

```typescript
// UserService 和 AuthService 都在 BUSINESS_PHASE
new AuthService([storageService])
new UserService([authService])

// 执行顺序：
// 1. AuthService.init()
// 2. UserService.init()
// 3. AuthService.load()
// 4. UserService.load() (等待 AuthService.load() 完成)
```

### 并行阶段的依赖

```typescript
// AnalyticsService 和 LogService 都在 FEATURE_PHASE (并行)
new AnalyticsService([userService])
new LogService([])

// 执行顺序：
// 1. 两者同时触发 init() 和 load()
// 2. AnalyticsService 会等待 userService.load() 完成
// 3. LogService 不等待任何服务
```

## 选择合适的阶段

### 决策树

```
是否是应用启动必须的服务？
├─ 是 → GLOBAL_PHASE
└─ 否 → 是否是核心业务逻辑？
    ├─ 是 → BUSINESS_PHASE
    └─ 否 → 是否是重量级或非关键服务？
        ├─ 是 → LAZY_PHASE
        └─ 否 → FEATURE_PHASE
```

### 典型场景

#### 场景 1：配置服务 → GLOBAL_PHASE

```typescript
// 应用启动必须，优先级最高
new ConfigService([])
```

#### 场景 2：用户服务 → BUSINESS_PHASE

```typescript
// 核心业务，必须在配置服务之后
new UserService([
  serviceManager.get<StorageService>('StorageService')
])
```

#### 场景 3：统计服务 → FEATURE_PHASE

```typescript
// 辅助功能，可以并行加载
new AnalyticsService([
  serviceManager.get<UserService>('UserService')
])
```

#### 场景 4：报表服务 → LAZY_PHASE

```typescript
// 重量级服务，延迟加载
new ReportService([
  serviceManager.get<FocusService>('FocusService')
])
```

## 性能优化建议

### 1. 合理划分阶段

- ✅ 将关键服务放在 GLOBAL_PHASE 和 BUSINESS_PHASE
- ✅ 将非关键服务放在 FEATURE_PHASE 和 LAZY_PHASE
- ❌ 避免所有服务都放在 GLOBAL_PHASE

### 2. 利用并行加载

- ✅ FEATURE_PHASE 和 LAZY_PHASE 的服务并行加载
- ✅ 减少串行等待的服务数量
- ❌ 避免不必要的串行依赖

### 3. 延迟加载非关键服务

- ✅ 将重量级服务放在 LAZY_PHASE
- ✅ 用户使用时才加载的功能放在 LAZY_PHASE
- ❌ 不要让非关键服务阻塞应用启动

## 返回主文档

[返回 SKILL.md](../SKILL.md)
