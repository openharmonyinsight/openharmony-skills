# Context API 速查

> UIAbilityContext: UIAbility组件上下文 | ApplicationContext: 应用级上下文

## 导入
```typescript
import { common } from '@kit.AbilityKit';
```

---

## UIAbilityContext

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `abilityInfo` | AbilityInfo | 当前Ability信息 |
| `currentHapModuleInfo` | HapModuleInfo | 当前HAP模块信息 |
| `config` | Configuration | 配置信息（语言、颜色模式等） |
| `windowStage` | WindowStage | 窗口对象（API 12+） |

### 启动Ability

```typescript
// 基本启动
startAbility(want: Want, options?: StartOptions): Promise<void>

// 启动并获取返回结果
startAbilityForResult(want: Want, options?: StartOptions): Promise<AbilityResult>
```

**示例:**
```typescript
// 启动目标Ability
await this.context.startAbility({
  bundleName: 'com.example.app',
  abilityName: 'TargetAbility'
});

// 启动并等待结果
const result = await this.context.startAbilityForResult({
  bundleName: 'com.example.app',
  abilityName: 'PickerAbility'
});
if (result.resultCode === 0) {
  const data = result.want?.parameters;
}
```

### 销毁Ability

```typescript
// 销毁自身
terminateSelf(): Promise<void>

// 销毁并返回结果（配合 startAbilityForResult 使用）
terminateSelfWithResult(abilityResult: AbilityResult): Promise<void>
```

**示例:**
```typescript
// 简单退出
await this.context.terminateSelf();

// 带返回值退出
await this.context.terminateSelfWithResult({
  resultCode: 0,
  want: { parameters: { selectedId: 123 } }
});
```

### 连接ServiceExtension

```typescript
// 连接服务
connectServiceExtensionAbility(want: Want, options: ConnectOptions): number

// 断开连接
disconnectServiceExtensionAbility(connectionId: number): Promise<void>
```

**示例:**
```typescript
let connectionId = this.context.connectServiceExtensionAbility(
  { bundleName: 'com.example.app', abilityName: 'MyService' },
  {
    onConnect(elementName, remoteProxy) {
      console.log('Service connected');
    },
    onDisconnect(elementName) {
      console.log('Service disconnected');
    },
    onFailed(code) {
      console.error(`Connect failed: ${code}`);
    }
  }
);

// 断开
await this.context.disconnectServiceExtensionAbility(connectionId);
```

### Caller/Callee 后台通信

```typescript
// 获取Caller对象（用于跨Ability调用）
startAbilityByCall(want: Want): Promise<Caller>
```

**示例:**
```typescript
const caller = await this.context.startAbilityByCall({
  bundleName: 'com.example.app',
  abilityName: 'BackendAbility'
});

// 调用后台方法
const result = await caller.call('methodName', parcelable);

// 释放
caller.release();
```

### openLink 跳转（API 12+）

```typescript
// 打开链接（推荐替代显式跳转三方应用）
openLink(link: string, options?: OpenLinkOptions): Promise<AbilityResult>
```

**示例:**
```typescript
await this.context.openLink('https://example.com', {
  appLinkingOnly: false
});
```

### 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 16000001 | Ability不存在 | 检查want中bundleName/abilityName |
| 16000004 | 不可启动不可见组件 | 目标设置exported=true或申请权限 |
| 16000011 | Context不存在 | 检查Ability是否已销毁 |
| 16000050 | 内部错误 | 检查want数据大小，重试 |
| 16200001 | Caller已释放 | 重新获取Caller |

---

## ApplicationContext

> 通过 `this.context.getApplicationContext()` 获取

### 生命周期监听

```typescript
// 监听UIAbility生命周期
on(type: 'abilityLifecycle', callback: AbilityLifecycleCallback): number
off(type: 'abilityLifecycle', callbackId: number): Promise<void>
```

**AbilityLifecycleCallback 回调:**
- `onAbilityCreate(ability)` - 创建
- `onAbilityForeground(ability)` - 前台
- `onAbilityBackground(ability)` - 后台
- `onAbilityDestroy(ability)` - 销毁
- `onWindowStageCreate/Active/Inactive/Destroy` - 窗口相关

**示例:**
```typescript
const appContext = this.context.getApplicationContext();
const callbackId = appContext.on('abilityLifecycle', {
  onAbilityCreate(ability) {
    console.log(`Ability created: ${ability.name}`);
  },
  onAbilityDestroy(ability) {
    console.log(`Ability destroyed: ${ability.name}`);
  }
  // ... 其他回调
});

// 取消监听
appContext.off('abilityLifecycle', callbackId);
```

### 环境变化监听

```typescript
// 监听系统环境变化（语言、深浅色等）
on(type: 'environment', callback: EnvironmentCallback): number
off(type: 'environment', callbackId: number): Promise<void>
```

**EnvironmentCallback 回调:**
- `onConfigurationUpdated(config)` - 配置变化
- `onMemoryLevel(level)` - 内存警告

**示例:**
```typescript
const callbackId = appContext.on('environment', {
  onConfigurationUpdated(config) {
    console.log(`Config changed: ${JSON.stringify(config)}`);
  },
  onMemoryLevel(level) {
    console.log(`Memory level: ${level}`);
    // 0=适中, 1=低, 2=严重
  }
});
```

### 应用状态监听（API 10+）

```typescript
// 监听应用前后台切换
on(type: 'applicationStateChange', callback: ApplicationStateChangeCallback): void
off(type: 'applicationStateChange', callback?: ApplicationStateChangeCallback): void
```

**示例:**
```typescript
appContext.on('applicationStateChange', {
  onApplicationForeground() {
    console.log('App entered foreground');
  },
  onApplicationBackground() {
    console.log('App entered background');
  }
});
```

### 进程管理

```typescript
// 获取运行中进程信息
getRunningProcessInformation(): Promise<Array<ProcessInformation>>

// 终止所有进程（慎用，异常场景使用）
killAllProcesses(): Promise<void>
```

**示例:**
```typescript
const processes = await appContext.getRunningProcessInformation();
processes.forEach(p => {
  console.log(`Process: ${p.processName}, PID: ${p.pid}`);
});
```

### 应用设置（API 11+）

```typescript
// 设置颜色模式
setColorMode(colorMode: ConfigurationConstant.ColorMode): void

// 设置语言
setLanguage(language: string): void

// 设置字体
setFont(font: string): void
```

**示例:**
```typescript
import { ConfigurationConstant } from '@kit.AbilityKit';

// 切换深色模式
appContext.setColorMode(ConfigurationConstant.ColorMode.COLOR_MODE_DARK);

// 切换语言
appContext.setLanguage('zh-Hans');
```

### 分身索引（API 12+）

```typescript
// 获取当前应用分身索引
getCurrentAppCloneIndex(): number
```

---

## Context 继承层次

```
BaseContext
    └── Context
          ├── ApplicationContext (应用级)
          ├── AbilityStageContext (Module级)
          └── UIAbilityContext (Ability级)
```

## 获取方式

| Context类型 | 获取方式 |
|-------------|----------|
| UIAbilityContext | `this.context`（UIAbility中） |
| ApplicationContext | `this.context.getApplicationContext()` |
| AbilityStageContext | `this.context`（AbilityStage中） |
