# 需求规格：应用分身功能

## 1. 概述

为 HarmonyOS NEXT 提供应用分身能力，允许用户为同一应用创建多个独立分身实例，各分身数据隔离。

## 2. 用户故事

### US-1：设置应用分身模式
作为设备管理员，我想要设置应用的分身模式，以便控制应用是否可以创建分身实例。

**验收标准：**
| AC编号 | WHEN（触发条件） | THEN（预期输出） |
|--------|-----------------|-----------------|
| AC-1 | 调用 setAppClonePreference(bundleName, {mode: ALWAYS_ASK}) | 返回 0，应用分身模式设为始终询问 |
| AC-2 | 调用 setAppClonePreference(bundleName, {mode: MAIN_APP}) | 返回 0，应用分身模式设为主应用 |
| AC-3 | 调用 setAppClonePreference(bundleName, {mode: CLONE_APP, index: 1}) | 返回 0，创建第1个分身 |
| AC-4 | 调用 setAppClonePreference(bundleName, {mode: CLONE_APP, index: 6}) | 返回 -1，超过分身数量上限(5) |

### US-2：查询应用分身状态
作为应用开发者，我想要查询应用的分身配置状态，以便获取当前分身模式。

**验收标准：**
| AC编号 | WHEN（触发条件） | THEN（预期输出） |
|--------|-----------------|-----------------|
| AC-5 | 调用 getAppClonePreference(bundleName)，应用已配置 | 返回 mode 及 index（如已设置） |
| AC-6 | 调用 getAppClonePreference(bundleName)，应用未配置 | 返回 mode: NOT_CONFIGURED |

### US-3：查询分身开关状态（文档验证类）
作为测试人员，我想要验证 @ohos.bundle.inner API 的 d.ts 签名完整性。

> 此 US 为文档验证类 US，验证目标为 d.ts 签名完整性，非功能性行为。

## 3. API 信息

| 接口名称 | 开放范围 | 入参 | 错误码 | 关联US |
|----------|---------|------|--------|--------|
| setAppClonePreference | public | bundleName: string, preference: {mode: CloneMode, index?: number} | 0, -1, 201 | US-1 |
| getAppClonePreference | public | bundleName: string | 0, -1, 201 | US-2 |
| getAppCloneInfo | @internal | bundleName: string | - | US-3 |

> CloneMode 枚举：NOT_CONFIGURED=0, ALWAYS_ASK=1, MAIN_APP=2, CLONE_APP=3

## 4. 业务规则

| 规则编号 | 类型 | 描述 | 关联AC |
|----------|------|------|--------|
| BR-1 | 权限控制 | 仅设备管理员（administrator 角色权限）可调用 setAppClonePreference | AC-1~AC-4 |
| BR-2 | 数量限制 | 分身数量上限为5，index 取值范围1-5 | AC-3, AC-4 |
| BR-3 | 默认行为 | 应用未配置分身时，getAppClonePreference 返回 NOT_CONFIGURED | AC-6 |

## 5. 异常规则

| 规则编号 | 触发条件 | 输出 | 关联AC |
|----------|---------|------|--------|
| EX-1 | bundleName 为空字符串 | 返回 -1，错误码 201（参数校验失败） | AC-1~AC-6 |
| EX-2 | bundleName 长度超过256字符 | 返回 -1，错误码 201 | AC-1~AC-6 |
| EX-3 | mode 值不在枚举范围内 | 返回 -1，错误码 201 | AC-1~AC-4 |
| EX-4 | index 超过5但mode为CLONE_APP | 返回 -1，错误码 201 | AC-4 |

## 6. 可测试性手段

| 手段 | 类型 | 用途 |
|------|------|------|
| 辅助API调用 | SDK API | 通过 setAppClonePreference/getAppClonePreference 触发被测对象 |

## 7. 非功能需求

| 需求ID | 类别 | 描述 | 关联主单元 |
|--------|------|------|-----------|
| NF-1 | 安全 | 仅授权管理员可修改分身配置 | US-1 |
| NF-2 | 性能 | getAppClonePreference 响应时间 ≤100ms | US-2 |
