# AbilityStage 速查

> Module级组件管理器，与Module一一对应，在Module首个Ability加载前创建

## 导入
```typescript
import { AbilityStage } from '@kit.AbilityKit';
```

## 基本结构

```typescript
export default class MyAbilityStage extends AbilityStage {
  onCreate(): void {
    // Module初始化
  }
  
  onAcceptWant(want: Want): string {
    // specified启动模式
    return 'instanceKey';
  }
  
  onConfigurationUpdate(config: Configuration): void {
    // 系统配置变更
  }
  
  onMemoryLevel(level: AbilityConstant.MemoryLevel): void {
    // 内存警告
  }
  
  onDestroy(): void {
    // Module清理（API 12+）
  }
}
```

## 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `context` | AbilityStageContext | AbilityStage上下文 |

---

## 生命周期回调

### onCreate()

> Module首个Ability实例创建前调用，同步执行

**用途:** 模块初始化（资源预加载、线程创建等）

```typescript
onCreate(): void {
  console.log('AbilityStage onCreate');
  // 初始化全局资源
  GlobalResource.init();
}
```

### onDestroy()（API 12+）

> Module最后一个Ability销毁后调用

**注意:** 异常退出或进程被杀时不会调用

```typescript
onDestroy(): void {
  console.log('AbilityStage onDestroy');
  // 清理全局资源
  GlobalResource.cleanup();
}
```

---

## 事件回调

### onAcceptWant(want)

> 处理 specified 启动模式的UIAbility

**返回值:** UIAbility实例唯一标识（相同标识复用实例，不同标识创建新实例）

```typescript
onAcceptWant(want: Want): string {
  // 根据业务逻辑决定实例标识
  if (want.parameters?.docId) {
    return `doc_${want.parameters.docId}`;  // 每个文档一个实例
  }
  return 'default';  // 默认实例
}
```

**典型场景:** 文档编辑器、多窗口应用

### onAcceptWantAsync(want)（API 20+）

> 异步版本，实现后同步版本不再触发

```typescript
async onAcceptWantAsync(want: Want): Promise<string> {
  const config = await fetchConfig();
  return config.instanceKey;
}
```

### onNewProcessRequest(want)（API 11+）

> 控制独立进程UIAbility/UIExtension的进程分配

**前提:** module.json5 中 `isolationProcess: true`

**设备限制:** 仅 2in1 和 Tablet 设备

```typescript
onNewProcessRequest(want: Want): string {
  if (want.parameters?.heavyTask) {
    return 'heavy_process';  // 独立进程
  }
  return '';  // 默认进程
}
```

### onConfigurationUpdate(config)

> 系统配置变更时调用（语言、深浅色等）

```typescript
onConfigurationUpdate(config: Configuration): void {
  console.log(`Language: ${config.language}`);
  console.log(`ColorMode: ${config.colorMode}`);
  // 更新全局配置
  GlobalConfig.update(config);
}
```

### onMemoryLevel(level)

> 系统内存紧张时调用

**level 取值:**
- `0` (MEMORY_LEVEL_MODERATE) - 适中
- `1` (MEMORY_LEVEL_LOW) - 低
- `2` (MEMORY_LEVEL_CRITICAL) - 严重

```typescript
import { AbilityConstant } from '@kit.AbilityKit';

onMemoryLevel(level: AbilityConstant.MemoryLevel): void {
  if (level >= AbilityConstant.MemoryLevel.MEMORY_LEVEL_LOW) {
    // 释放非必要资源
    CacheManager.clearAll();
    ImageLoader.releaseCache();
  }
}
```

---

## 准备终止回调（API 15+）

> 用于应用关闭前询问用户（如保存提示）

**权限要求:** `ohos.permission.PREPARE_APP_TERMINATE`

**设备限制:** 2in1 和 Tablet 设备

### onPrepareTermination()

```typescript
onPrepareTermination(): AbilityConstant.PrepareTermination {
  if (hasUnsavedChanges()) {
    return AbilityConstant.PrepareTermination.CANCEL;  // 取消关闭
  }
  return AbilityConstant.PrepareTermination.TERMINATE;  // 允许关闭
}
```

### onPrepareTerminationAsync()（异步版本）

```typescript
async onPrepareTerminationAsync(): Promise<AbilityConstant.PrepareTermination> {
  const userChoice = await showSaveDialog();
  if (userChoice === 'save') {
    await saveDocument();
  }
  return userChoice === 'cancel' 
    ? AbilityConstant.PrepareTermination.CANCEL 
    : AbilityConstant.PrepareTermination.TERMINATE;
}
```

---

## 配置文件

在 `module.json5` 中配置：

```json
{
  "module": {
    "srcEntry": "./ets/myabilitystage/MyAbilityStage.ets"
  }
}
```

---

## 生命周期顺序

```
HAP/HSP首次加载
    ↓
AbilityStage.onCreate()
    ↓
[specified模式] AbilityStage.onAcceptWant()
    ↓
UIAbility.onCreate()
    ↓
... (UIAbility生命周期)
    ↓
最后一个Ability退出
    ↓
AbilityStage.onDestroy()
```

---

## 最佳实践

1. **onCreate** 中只做必要的同步初始化，耗时操作异步处理
2. **onMemoryLevel** 中及时释放缓存，避免被系统杀死
3. **specified模式** 通过 onAcceptWant 返回唯一标识实现多实例
4. **资源共享** 利用 AbilityStage 管理 Module 内共享资源
