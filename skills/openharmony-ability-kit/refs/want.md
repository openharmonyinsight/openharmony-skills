# Want 对象速查

> 应用组件间信息传递载体，最大数据量 100KB（IPC限制）

## 导入
```typescript
import { Want } from '@kit.AbilityKit';
```

## 核心字段

| 字段 | 类型 | 用途 | 说明 |
|------|------|------|------|
| `bundleName` | string | 显式启动 | 目标应用包名 |
| `moduleName` | string | 显式启动 | 目标模块名（HAR时需填依赖它的HAP/HSP） |
| `abilityName` | string | 显式启动 | 目标Ability名 |
| `action` | string | 隐式启动 | 操作类型（查看、分享等） |
| `entities` | string[] | 隐式启动 | 目标类别（浏览器、播放器等） |
| `uri` | string | 隐式启动 | 资源标识符 |
| `type` | string | 隐式启动 | MIME类型（如 'text/xml'、'image/*'） |
| `flags` | number | 权限控制 | URI权限标志 |
| `parameters` | Record<string, Object> | 数据传递 | 自定义键值对 |
| `fds` | Record<string, number> | 文件传递 | 文件描述符（API 15+） |
| `deviceId` | string | 分布式 | 目标设备ID，空串表示本设备 |

## 显式启动（推荐）

```typescript
// 精确指定目标Ability
let want: Want = {
  bundleName: 'com.example.target',
  moduleName: 'entry',
  abilityName: 'MainAbility'
};
this.context.startAbility(want);
```

## 隐式启动

```typescript
// 通过action+uri匹配
let want: Want = {
  action: 'ohos.want.action.viewData',
  uri: 'https://example.com',
  type: 'text/html'
};
this.context.startAbility(want);
```

## parameters 传递数据

### 支持的数据类型
- **基本类型**: String, Number, Boolean
- **复合类型**: Object, Array
- **特殊类型**: FD（文件描述符）

```typescript
// 发送方
let want: Want = {
  bundleName: 'com.example.target',
  abilityName: 'TargetAbility',
  parameters: {
    userId: 12345,
    userName: 'test',
    isVip: true,
    tags: ['dev', 'test'],
    config: { theme: 'dark' }
  }
};

// 接收方（onCreate中）
onCreate(want: Want, launchParam: AbilityConstant.LaunchParam) {
  const userId = want.parameters?.userId;
  const userName = want.parameters?.userName;
}
```

### 传递文件描述符 (FD)

```typescript
import { fileIo } from '@kit.CoreFileKit';

const fd = fileIo.openSync('/path/to/file').fd;
let want: Want = {
  bundleName: 'com.example.target',
  abilityName: 'TargetAbility',
  parameters: {
    'fileKey': { 'type': 'FD', 'value': fd }  // 固定格式
  }
};
```

## 系统预置 parameters Key

| Key | 说明 | 来源 |
|-----|------|------|
| `ohos.aafwk.param.callerPid` | 调用方PID | 系统自动填充 |
| `ohos.aafwk.param.callerBundleName` | 调用方包名 | 系统自动填充 |
| `ohos.aafwk.param.callerAbilityName` | 调用方Ability名 | 系统自动填充 |
| `ohos.aafwk.param.callerUid` | 调用方UID | 系统自动填充 |
| `ohos.ability.params.abilityRecoveryRestart` | 是否故障恢复重启 | 系统自动填充 |

## flags 常用值

```typescript
import { wantConstant } from '@kit.AbilityKit';

// 授权读取URI权限
want.flags = wantConstant.Flags.FLAG_AUTH_READ_URI_PERMISSION;

// 授权写入URI权限
want.flags = wantConstant.Flags.FLAG_AUTH_WRITE_URI_PERMISSION;
```

## 获取调用方信息

```typescript
// 在被拉起的Ability中
onCreate(want: Want, launchParam: AbilityConstant.LaunchParam) {
  const callerBundle = want.parameters?.['ohos.aafwk.param.callerBundleName'];
  const callerAbility = want.parameters?.['ohos.aafwk.param.callerAbilityName'];
  console.log(`Called by: ${callerBundle}/${callerAbility}`);
}
```

## 注意事项

1. **数据大小限制**: parameters 总大小不超过 100KB
2. **大数据传输**: 超过限制使用 `WriteRawDataBuffer` 或 uri 方式
3. **不支持 function**: parameters 的 value 不支持函数类型
4. **HAR模块**: 启动HAR中的Ability时，moduleName 需填依赖该HAR的HAP/HSP名称
