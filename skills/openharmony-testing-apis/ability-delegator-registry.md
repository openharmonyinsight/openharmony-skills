# @ohos.app.ability.abilityDelegatorRegistry

**模块**: AbilityDelegatorRegistry
**API 版本**: 9+
**导入方式**: `import { abilityDelegatorRegistry } from '@kit.TestKit';`

## 概述

用于获取 **AbilityDelegator** 和 **AbilityDelegatorArgs** 对象以执行测试框架操作。提供以下能力：
- 启动和管理 Ability
- 使用 AbilityMonitor 监控 Ability 生命周期状态
- 执行 Shell 命令
- 访问测试参数

## 类型定义

### AbilityLifecycleState

枚举 Ability 生命周期状态，由 `getAbilityState()` 返回。

| 值 | 名称 | 描述 |
|-------|------|-------------|
| 0 | UNINITIALIZED | 无效状态 |
| 1 | CREATE | Ability 已创建 |
| 2 | FOREGROUND | 在前台运行 |
| 3 | BACKGROUND | 在后台运行 |
| 4 | DESTROY | Ability 已销毁 |

## API 方法

### getAbilityDelegator()

```typescript
getAbilityDelegator(): AbilityDelegator
```

获取 **AbilityDelegator** 对象用于测试框架操作。

**返回值**: `AbilityDelegator` 对象

**示例**:
```typescript
import { abilityDelegatorRegistry } from '@kit.TestKit';
import { Want } from '@kit.AbilityKit';

let abilityDelegator = abilityDelegatorRegistry.getAbilityDelegator();
let want: Want = {
  bundleName: 'com.example.myapplication',
  abilityName: 'EntryAbility'
};

abilityDelegator.startAbility(want, (err) => {
  if (err) {
    console.error(`启动 Ability 失败，错误: ${JSON.stringify(err)}`);
  } else {
    console.info('启动 Ability 成功');
  }
});
```

### getArguments()

```typescript
getArguments(): AbilityDelegatorArgs
```

获取 **AbilityDelegatorArgs** 对象以访问测试参数。

**返回值**: `AbilityDelegatorArgs` 对象，包含：
- `bundleName: string` - 应用的包名
- `parameters: { [key: string]: string }` - 测试参数
- `testCaseNames: string[]` - 测试用例名称
- `testRunnerClassName: string` - 测试运行器类名

**示例**:
```typescript
import { abilityDelegatorRegistry } from '@kit.TestKit';

let args = abilityDelegatorRegistry.getArguments();
console.info(`bundleName: ${args.bundleName}`);
console.info(`参数: ${JSON.stringify(args.parameters)}`);
console.info(`测试用例名: ${args.testCaseNames}`);
console.info(`测试运行器类名: ${args.testRunnerClassName}`);
```

## 相关类型

### AbilityDelegator

提供以下 API：
- 添加/移除 **AbilityMonitor** 对象
- 启动 Ability
- 等待 Ability 到达特定状态
- 执行 Shell 命令
- 获取 Ability 生命周期状态

### AbilityDelegatorArgs

提供对传递给测试运行器的测试参数的访问。

### AbilityMonitor

监控 Ability 生命周期状态变化。与 AbilityDelegator 的 `addAbilityMonitor()` 方法配合使用。

### AbilityStageMonitor (API 14+)

监控 AbilityStage 生命周期状态变化。

### ShellCmdResult

表示 Shell 命令执行的结果。
