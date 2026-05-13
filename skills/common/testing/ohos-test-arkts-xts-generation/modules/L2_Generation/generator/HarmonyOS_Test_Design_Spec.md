# HarmonyOS API 测试设计规范 - 增量知识

> **模块信息**
> - 层级：L2_Generation/generator
> - 优先级：按需加载
> - 适用范围：HarmonyOS 特有测试设计知识（状态机、生命周期、兼容性、安全性等）
> - 父模块：`test_generator.md`
> - 来源：总结自《终端 鸿蒙API测试设计规范》，仅收录常规测试规范中不常见的增量知识

---

## 一、API 注解体系

### 1.1 @syscap - 系统能力标识

```typescript
// 格式: SystemCapability.{子系统}.{能力名}
@syscap SystemCapability.FileManagement.UserFileService

// 可多选: and / or
@syscap SystemCapability.ArkUI.ArkUI.Full | SystemCapability.ArkUI.ArkUI.Lite
```

### 1.2 @permission - 权限注解

```typescript
// 单个权限
@permission ohos.permission.ACCESS_NEARLINK

// 多个权限 (AND)
@permission ohos.permission.READ_MEDIA & ohos.permission.WRITE_MEDIA

// 多个权限 (OR)
@permission ohos.permission.CAMERA | ohos.permission.MICROPHONE
```

### 1.3 其他关键注解

| 注解 | 用途 | 示例 |
|------|------|------|
| `@kit` | 标识 Kit 名称 | `@kit AbilityKit` |
| `@atomicservice` | 元服务 API | `@atomicservice [since 11]` |
| `@crossplatform` | 跨平台 API | `@crossplatform [since 10]` |
| `@stagemodelonly` | 仅 Stage 模型 | `@stagemodelonly` |
| `@famodelonly` | 仅 FA 模型 | `@famodelonly` |
| `@systemapi` | 系统 API | `@systemapi` |
| `@form` | 元服务卡片 API | `@form` |
| `@deprecated` | 废弃 API | `@deprecated since 9` |
| `@useinstead` | 替代 API | `@useinstead Component#click` |
| `@release` | 发布版本 | `@release since 12` |

---

## 二、API 分级制度

```
L0: ROM能力 (device-define)
    └── canIUse() 返回 False，API 直接 crash

L1: SDK + ROM
    └── 801 错误码
    └── 设备差异需要考虑

L2: SDK可选能力
    └── 需要检查 SysCap
    └── canIUse() 返回 True/False
    └── XTS/HCTS 测试

L3: SDK + 应用配置
    └── 无 SysCap 限制
    └── 基础数据类型
```

### SysCap 体系

- **HAMS SysCap**: SDK 定义的系统能力
- **ROM SysCap**: 设备商定义的能力
- **device-define**: 设备特有能力 (N-1 兼容)

---

## 三、API 命名规范

### 3.1 返回值规范

- **必须明确返回值类型**：禁止使用 `"success"`、`undefined` 表示成功，应使用明确的返回类型
- **参数可为可选**：使用 `?` 标记可选参数，但 API 必须有明确返回值类型

```typescript
// 正确示例
function save(path: string): Promise<void>
function getConfig(): Record<string, string>

// 错误示例
function execute(): undefined  // 禁止
function process(): "success"  // 禁止，应返回具体类型
```

### 3.2 回调参数规范

- **禁止使用通用术语**：使用具体参数名，不使用 `"result"`、`"data"` 等
- **禁止省略参数**：回调必须包含实际业务参数

---

## 四、API 完整性规范

### 4.1 命名空间规范

- **禁止省略命名空间**：ArkTS API 必须有命名空间前缀
- 正确: `document.XXX`, `urpc.XXX`
- 错误: 直接使用 `XXX`

### 4.2 继承关系说明

- **必须说明继承关系**：API 文档必须包含 extends/implements 说明
- 示例: `TimeGuardExtensionAbility extends ExtensionAbility`

### 4.3 属性/字段说明

- **必须标注属性来源**：说明是新增还是继承
- **枚举值必须有含义说明**：每个枚举值必须解释含义

---

## 五、状态机测试

### 5.1 状态转换完整性

- **必须测试所有有效转换**
- **必须测试无效转换的拒绝行为**

### 5.2 Call 状态机示例

```
IDLE → DIALING → ALERTING → ACTIVE → DISCONNECTED → IDLE
IDLE → DISCONNECTED (拒绝无效转换)
```

---

## 六、时序/生命周期测试

### 6.1 注册/解注册配对

必须验证配对操作的正确性：

```typescript
on/off, subscribe/unregister, bind/unbind
open/close, lock/unlock, create/destroy
```

### 6.2 生命周期时序

- **必须按正确顺序调用**
- **示例**: VpnConnection.create → 使用 → destroy

---

## 七、兼容性测试

### 7.1 SDK 版本检测

```typescript
// 使用 deviceInfo.sdkApiVersion
if (deviceInfo.sdkApiVersion <= 13) {
    // API 13 及以下
} else if (deviceInfo.sdkApiVersion <= 18) {
    // API 14 ~ 18
} else {
    // API 19+
}
```

### 7.2 OTA 兼容性

- **cache 可能失效**: OTA 后 API 行为可能变化
- **需验证**: OTA 前后 API 行为一致性

### 7.3 targetSdkVersion 影响

- **影响权限申请**: 不同版本权限行为不同
- **影响 API 可用性**: 高版本可能废弃低版本 API

---

## 八、安全性测试

### 8.1 权限模型

- **system_grant**: 安装时授予
- **user_grant**: 运行时用户授权
- **availableLevel**: Normal / SystemBasic / SystemCore

### 8.2 权限测试点

```typescript
// 1. 无权限调用 → 201 错误
// 2. 权限不足 → 201 错误
// 3. 权限撤销后 → 201 错误
// 4. 多权限组合 (and/or)
```

---

## 九、UI/API 特殊场景

### 9.1 accessibilityLevel 影响

- `accessibilityLevel: "no"` 或 `"no-hide-descendants"` 时，On.text() 无法定位
- 需使用 On.originalText() 替代

### 9.2 设备形态差异

- **1+8设备**: phone, tablet, 2in1, PC, wearable, liteWearable, tv, car, etc.
- **不同形态 API 行为可能不同**

### 9.3 窗口/多屏相关

- WindowFilter.displayId: API 20+ 支持多屏定位
- On.belongingDisplay(displayId): API 20+ 多屏控件查找

---

## 十、ArkTS 特有类型

### 10.1 类型表示方式

```typescript
// 可空类型
string | null | undefined

// 联合类型
number | Record<number, number>

// 可选字段
interface Config {
    name?: string;  // 可选
    value: string;  // 必选
}
```

### 10.2 类型层级

```
Namespace → Class → Method → Field
         → Interface → Property
         → Struct
         → Enum
```

---

## 十一、测试策略增量点

### 11.1 N-wise 组合测试

当参数组合爆炸时，使用 N-wise (N=2) 减少用例数。核心参数两两组合，覆盖 90%+ 场景。

### 11.2 AI 辅助测试设计

- 枚举类参数: 100% 覆盖
- 组合类参数: AI 分析依赖关系，提取关键组合
