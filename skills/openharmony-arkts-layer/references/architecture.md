# 架构设计原则和分层规则

## 分层架构详解

### 三层架构模型

ark-layer 采用严格的三层分离架构：

```
┌─────────────────────────────────┐
│       pages/ (视图层)            │  仅 ArkUI 组件
├─────────────────────────────────┤
│     domain/ (业务领域层)         │  业务逻辑和服务编排
├─────────────────────────────────┤
│     infra/ (基础设施层)          │  框架核心 + 通用工具和能力封装
└─────────────────────────────────┘
```

### 关于 core/ 目录

**core/ 目录的定位**：
- `core/` 包含框架核心的参考实现（Service、ServiceManager、DefaultPhases 等）
- 这些文件应视为**三方件/库**，类似于 lodash、axios
- 目前尚未打包发布到鸿蒙三方中心仓，需要手动拷贝使用

**使用方式**：
1. 将 `core/` 目录下的文件拷贝到你项目的 `infra/` 目录下
2. 建议的组织方式：
   ```
   infra/
   ├── service-core/        # 从 core/ 拷贝过来的框架核心
   │   ├── Service.ets
   │   ├── ServiceManager.ets
   │   ├── DefaultPhases.ets
   │   ├── Phase.ets
   │   └── ...
   ├── storage/             # 通用工具
   ├── network/
   └── ...
   ```
3. 也可以直接放在 `infra/` 根目录下（不推荐子目录嵌套过深）

**注意**：本仓库中的 `core/` 目录仅作为参考展示，实际项目使用时应将其整合到 `infra/` 目录中。

### 各层职责

#### 1. infra/ - 基础设施层

**职责**：提供框架核心能力，封装无状态、通用的技术能力和工具类

**包含内容**：
- **框架核心**（从 `core/` 拷贝）：
  - `Service.ets` - Service 抽象基类
  - `ServiceManager.ets` - 服务管理器（单例）
  - `DefaultPhases.ets` - 预定义的加载阶段
  - `Phase.ets` - 阶段定义接口
- **通用工具**：
  - `storage/` - 本地存储封装
  - `network/` - 网络请求封装
  - `audio/` - 音频播放封装
  - `database/` - 数据库操作封装

**规则**：
- **无状态**：不包含业务状态
- **通用性**：可被多个业务模块复用
- **严禁向上依赖**：不能依赖 domain 和 pages 层

**示例目录结构**：
```
infra/
├── service-core/              # 框架核心（从 core/ 拷贝）
│   ├── Service.ets
│   ├── ServiceManager.ets
│   ├── DefaultPhases.ets
│   └── Phase.ets
├── storage/
│   └── StorageService.ets
├── network/
│   └── NetworkService.ets
├── audio/
│   └── AudioService.ets
└── database/
    └── DatabaseService.ets
```

#### 2. domain/ - 业务领域层

**职责**：实现具体的业务逻辑和领域服务

**包含内容**：
- `user/` - 用户相关业务
- `auth/` - 认证相关业务
- `focus/` - 专注相关业务
- `achievement/` - 成就相关业务

**规则**：
- 按业务领域划分模块
- **向下依赖**：可依赖 infra 层（包括框架核心）
- **严禁向上依赖**：不能依赖 pages 层
- Service 之间通过构造函数声明依赖

**示例目录结构**：
```
domain/
├── user/
│   └── UserService.ets
├── auth/
│   └── AuthService.ets
├── focus/
│   └── FocusService.ets
└── achievement/
    └── AchievementService.ets
```

#### 3. pages/ - 视图层

**职责**：UI 展示和用户交互

**包含内容**：
- ArkUI 组件
- 页面路由
- UI 状态管理

**规则**：
- **仅包含 UI 逻辑**：不包含业务逻辑
- **通过 ServiceManager 获取服务**：不直接 import Service 实例
- **向下依赖**：可依赖所有下层
- **组件化**：使用 @Component 装饰器

**示例目录结构**：
```
pages/
├── Index.ets
├── Profile.ets
├── Settings.ets
└── components/
    ├── UserCard.ets
    └── FocusTimer.ets
```

## 依赖规则

### 允许的依赖方向

```
infra ← domain ← pages
  ↑        ↑       ↑
  └────────┴───────┘
```

**原则**：
- 上层可以依赖下层
- 下层不能依赖上层
- 同层之间谨慎依赖（domain 层除外，可相互依赖）

**注意**：框架核心（Service、ServiceManager 等）拷贝到 infra/ 后，所有依赖它的代码都应通过 `infra/` 路径引用。

### 禁止的跨层引用

#### ❌ 错误示例 1：Infra 依赖 Domain

```typescript
// infra/network/NetworkService.ets
import { UserService } from '../../domain/user/UserService'  // ❌ 错误

export class NetworkService extends Service {
  constructor(services: Service[] = []) {
    super(services)
  }

  async request(url: string): Promise<any> {
    // ❌ Infra 不应该依赖 Domain
    const user = this.userService.getUserInfo()
    // ...
  }
}
```

**正确做法**：将用户信息作为参数传入

```typescript
// ✅ 正确
async request(url: string, userId: string): Promise<any> {
  const headers = { 'X-User-Id': userId }
  // ...
}
```

#### ❌ 错误示例 2：Domain 依赖 Pages

```typescript
// domain/user/UserService.ets
import { UserProfile } from '../../pages/components/UserProfile'  // ❌ 错误

export class UserService extends Service {
  // ❌ Domain 不应该知道 UI 组件
  showUserProfile(user: UserInfo): void {
    // ...
  }
}
```

**正确做法**：通过事件或回调机制

```typescript
// ✅ 正确
// UserService 只提供数据
getUserInfo(userId: string): UserInfo | undefined {
  return this.users.get(userId)
}

// 在 Page 中处理 UI
// pages/Index.ets
const user = this.userService.getUserInfo(userId)
if (user) {
  UserProfile.show(user)
}
```

#### ❌ 错误示例 3：Pages 直接创建 Service 实例

```typescript
// pages/Index.ets
import { UserService } from '../domain/user/UserService'

@Entry
@Component
struct Index {
  // ❌ 错误：不应该直接创建 Service 实例
  private userService: UserService = new UserService([])

  aboutToAppear(): void {
    // 这会导致多个实例，违反单例原则
  }
}
```

**正确做法**：通过 ServiceManager 获取

```typescript
// ✅ 正确
import { serviceManager } from '../core/ServiceManager'
import { UserService } from '../domain/user/UserService'

@Entry
@Component
struct Index {
  private userService: UserService = serviceManager.get<UserService>('UserService')!
}
```

## 分层验证清单

在开发过程中，使用以下清单验证代码是否符合分层规范：

### infra/ 层检查清单（包含框架核心）

- [ ] 框架核心文件已从 `core/` 拷贝到 `infra/` 目录
- [ ] 框架核心不包含任何业务逻辑
- [ ] 通用工具类是无状态的
- [ ] 不依赖 domain、pages 层
- [ ] 可被多个业务模块复用

### domain/ 层检查清单

- [ ] 按业务领域划分模块
- [ ] 不依赖 pages 层
- [ ] Service 依赖通过构造函数声明
- [ ] 业务逻辑完整且内聚

### pages/ 层检查清单

- [ ] 仅包含 UI 组件和交互逻辑
- [ ] 通过 ServiceManager 获取服务
- [ ] 不直接创建 Service 实例
- [ ] 使用 @Component 或 @Entry 装饰器

## 常见违规场景

### 场景 1：在 Service 中直接操作 UI

```typescript
// ❌ 错误
async showErrorMessage(message: string): Promise<void> {
  AlertDialog.show({ message: message })  // Service 不应该操作 UI
}
```

**正确做法**：Service 返回状态，Page 处理 UI

```typescript
// ✅ 正确
async validateInput(input: string): Promise<boolean> {
  return input.length > 0
}

// 在 Page 中
if (!await this.userService.validateInput(input)) {
  AlertDialog.show({ message: '输入无效' })
}
```

### 场景 2：在 Page 中实现业务逻辑

```typescript
// ❌ 错误
@Component
struct UserList {
  async loadUsers(): Promise<void> {
    // ❌ Page 不应该包含复杂的业务逻辑
    const response = await fetch('https://api.example.com/users')
    const data = await response.json()
    this.users = data.map(u => ({
      id: u.id,
      name: u.name,
      email: u.email
    }))
  }
}
```

**正确做法**：将业务逻辑移至 Service

```typescript
// ✅ 正确 - UserService.ets
async loadUsers(): Promise<boolean> {
  const response = await this.networkService.get('/users')
  this.users = response.data
  return true
}

// ✅ 正确 - Page
@Component
struct UserList {
  private userService: UserService = serviceManager.get<UserService>('UserService')!

  async loadUsers(): Promise<void> {
    await this.userService.loadUsers()
    this.users = this.userService.getUsers()
  }
}
```

## 分层架构的优势

### 1. 关注点分离

- **infra** 关注框架机制和技术能力
- **domain** 关注业务逻辑
- **pages** 关注用户体验

### 2. 可维护性

- 修改 UI 不影响业务逻辑
- 修改业务逻辑不影响技术能力
- 各层可独立测试

### 3. 可复用性

- infra 层的能力可被多个 domain 模块复用
- domain 层的服务可被多个 pages 复用

### 4. 可测试性

- 各层可独立进行单元测试
- 通过 Mock 依赖可以隔离测试

## 返回主文档

[返回 SKILL.md](../SKILL.md)
