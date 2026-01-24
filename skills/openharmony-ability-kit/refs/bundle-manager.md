# BundleManager 速查

> 应用包管理，获取 BundleInfo、AbilityInfo 等应用信息

## 导入
```typescript
import { bundleManager } from '@kit.AbilityKit';
```

---

## BundleFlags（包信息查询标志）

位运算组合使用，控制返回的信息内容：

| Flag | 值 | 说明 |
|------|-----|------|
| `GET_BUNDLE_INFO_DEFAULT` | 0x00 | 默认，仅基本信息 |
| `GET_BUNDLE_INFO_WITH_APPLICATION` | 0x01 | 包含ApplicationInfo |
| `GET_BUNDLE_INFO_WITH_HAP_MODULE` | 0x02 | 包含HapModuleInfo |
| `GET_BUNDLE_INFO_WITH_ABILITY` | 0x04 | 包含AbilityInfo |
| `GET_BUNDLE_INFO_WITH_EXTENSION_ABILITY` | 0x08 | 包含ExtensionAbilityInfo |
| `GET_BUNDLE_INFO_WITH_REQUESTED_PERMISSION` | 0x10 | 包含权限信息 |
| `GET_BUNDLE_INFO_WITH_METADATA` | 0x20 | 包含Metadata |
| `GET_BUNDLE_INFO_WITH_DISABLE` | 0x40 | 包含禁用的组件 |
| `GET_BUNDLE_INFO_WITH_SIGNATURE_INFO` | 0x80 | 包含签名信息 |

**组合使用:**
```typescript
const flags = bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_APPLICATION 
            | bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_ABILITY;
```

---

## 核心 API

### 获取自身包信息

```typescript
// 获取当前应用的BundleInfo（最常用）
getBundleInfoForSelf(bundleFlags: number): Promise<BundleInfo>
getBundleInfoForSelfSync(bundleFlags: number): BundleInfo  // 同步版本
```

**示例:**
```typescript
import { bundleManager } from '@kit.AbilityKit';

// 获取自身包信息（包含Ability和HAP模块信息）
const flags = bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_HAP_MODULE 
            | bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_ABILITY;

const bundleInfo = await bundleManager.getBundleInfoForSelf(flags);

console.log(`Bundle name: ${bundleInfo.name}`);
console.log(`Version: ${bundleInfo.versionName}`);
console.log(`Abilities: ${bundleInfo.hapModulesInfo[0]?.abilitiesInfo?.length}`);
```

### 获取元数据配置

```typescript
// 从Ability的metadata中获取profile配置
getProfileByAbility(moduleName: string, abilityName: string, metadataName?: string): Promise<Array<string>>
```

**示例:**
```typescript
// 读取 metadata 中的配置文件内容
const profiles = await bundleManager.getProfileByAbility('entry', 'MainAbility', 'custom_config');
const configContent = JSON.parse(profiles[0]);
```

### 获取ExtensionAbility的元数据

```typescript
getProfileByExtensionAbility(moduleName: string, extensionAbilityName: string, metadataName?: string): Promise<Array<string>>
```

---

## 常用信息类型

### BundleInfo（包信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 包名 |
| `versionCode` | number | 版本号 |
| `versionName` | string | 版本名称 |
| `minCompatibleVersionCode` | number | 最低兼容版本 |
| `hapModulesInfo` | HapModuleInfo[] | HAP模块信息 |
| `appInfo` | ApplicationInfo | 应用信息 |
| `reqPermissions` | string[] | 请求的权限 |
| `signatureInfo` | SignatureInfo | 签名信息 |

### ApplicationInfo（应用信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 应用名 |
| `bundleName` | string | 包名 |
| `description` | string | 描述 |
| `icon` | string | 图标资源ID |
| `label` | string | 标签资源ID |
| `labelId` | number | 标签资源ID（数值） |
| `iconId` | number | 图标资源ID（数值） |
| `process` | string | 进程名 |
| `permissions` | string[] | 权限列表 |

### HapModuleInfo（HAP模块信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 模块名 |
| `description` | string | 描述 |
| `mainAbility` | string | 主Ability名 |
| `abilitiesInfo` | AbilityInfo[] | Ability列表 |
| `extensionAbilitiesInfo` | ExtensionAbilityInfo[] | ExtensionAbility列表 |
| `metadata` | Metadata[] | 元数据 |
| `type` | ModuleType | 模块类型（entry/feature/shared） |

### AbilityInfo（Ability信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | Ability名 |
| `bundleName` | string | 所属包名 |
| `moduleName` | string | 所属模块名 |
| `label` | string | 标签 |
| `description` | string | 描述 |
| `launchType` | LaunchType | 启动模式 |
| `exported` | boolean | 是否导出 |
| `metadata` | Metadata[] | 元数据 |
| `windowSize` | WindowSize | 窗口大小配置 |

---

## 枚举值

### LaunchType（启动模式）

| 值 | 说明 |
|----|------|
| `SINGLETON` (0) | 单实例 |
| `MULTITON` (1) | 多实例（已废弃，使用 STANDARD） |
| `STANDARD` (1) | 多实例 |
| `SPECIFIED` (2) | 指定实例 |

### ModuleType（模块类型）

| 值 | 说明 |
|----|------|
| `ENTRY` (1) | 入口模块 |
| `FEATURE` (2) | 功能模块 |
| `SHARED` (3) | 共享模块（HSP） |

### ExtensionAbilityType（扩展类型）

| 值 | 说明 |
|----|------|
| `FORM` (0) | 卡片 |
| `WORK_SCHEDULER` (1) | 后台任务 |
| `INPUT_METHOD` (2) | 输入法 |
| `SERVICE` (3) | 服务 |
| `DATA_SHARE` (5) | 数据共享 |
| `BACKUP` (9) | 备份 |
| `UNSPECIFIED` (255) | 未指定 |

---

## 典型使用场景

### 1. 检查自身版本信息

```typescript
const bundleInfo = await bundleManager.getBundleInfoForSelf(
  bundleManager.BundleFlag.GET_BUNDLE_INFO_DEFAULT
);
console.log(`当前版本: ${bundleInfo.versionName} (${bundleInfo.versionCode})`);
```

### 2. 获取所有Ability列表

```typescript
const bundleInfo = await bundleManager.getBundleInfoForSelf(
  bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_HAP_MODULE |
  bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_ABILITY
);

bundleInfo.hapModulesInfo.forEach(hapModule => {
  hapModule.abilitiesInfo?.forEach(ability => {
    console.log(`Ability: ${ability.name}, LaunchType: ${ability.launchType}`);
  });
});
```

### 3. 读取Ability的metadata配置

```typescript
// module.json5 中配置:
// "abilities": [{
//   "name": "MainAbility",
//   "metadata": [{
//     "name": "custom_config",
//     "resource": "$profile:custom_config"
//   }]
// }]

const profiles = await bundleManager.getProfileByAbility('entry', 'MainAbility', 'custom_config');
const config = JSON.parse(profiles[0]);
```

### 4. 获取应用签名信息

```typescript
const bundleInfo = await bundleManager.getBundleInfoForSelf(
  bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_SIGNATURE_INFO
);
console.log(`App ID: ${bundleInfo.signatureInfo.appId}`);
console.log(`Fingerprint: ${bundleInfo.signatureInfo.fingerprint}`);
```

---

## 权限说明

| API | 权限要求 |
|-----|----------|
| `getBundleInfoForSelf` | 无需权限 |
| `getBundleInfo` | ohos.permission.GET_BUNDLE_INFO_PRIVILEGED（系统应用） |
| `getAllBundleInfo` | ohos.permission.GET_INSTALLED_BUNDLE_LIST |
| `queryAbilityInfo` | ohos.permission.GET_BUNDLE_INFO_PRIVILEGED（系统应用） |

> 大多数常用操作只需 `getBundleInfoForSelf`，无需额外权限
