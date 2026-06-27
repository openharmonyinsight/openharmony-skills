# Feature API

## 概述

Feature API 提供特性管理功能，支持特性的启用、禁用和状态查询。

## FeatureAPI.enableFeature

enableFeature(featureId: string, options?: FeatureOptions): Promise\<boolean\>

启用指定特性。

**系统能力**: SystemCapability.FeatureManagement

**需要权限**: ohos.permission.MANAGE_FEATURES

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| featureId | string | 是 | 特性 ID |
| options | FeatureOptions | 否 | 特性选项 |

**返回值**：

| 类型 | 说明 |
| ---- | ---- |
| Promise\<boolean\> | 成功返回 true，失败返回 false |

**错误码**：

| 错误码ID | 错误信息 |
| ------- | ------- |
| 401 | Feature not found. |
| 403 | Permission denied. |
| 409 | Feature already enabled. |

## FeatureAPI.disableFeature

disableFeature(featureId: string): Promise\<boolean\>

禁用指定特性。

**系统能力**: SystemCapability.FeatureManagement

**需要权限**: ohos.permission.MANAGE_FEATURES

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| featureId | string | 是 | 特性 ID |

**返回值**：

| 类型 | 说明 |
| ---- | ---- |
| Promise\<boolean\> | 成功返回 true，失败返回 false |

**错误码**：

| 错误码ID | 错误信息 |
| ------- | ------- |
| 401 | Feature not found. |
| 403 | Permission denied. |

## FeatureAPI.getFeatureStatus

getFeatureStatus(featureId: string): FeatureStatus

查询特性状态。

**系统能力**: SystemCapability.FeatureManagement

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| featureId | string | 是 | 特性 ID |

**返回值**：

| 类型 | 说明 |
| ---- | ---- |
| FeatureStatus | 特性状态对象 |

## FeatureStatus

特性状态对象。

### 属性

| 名称 | 类型 | 说明 |
| ---- | ---- | ---- |
| enabled | boolean | 特性是否已启用 |
| version | string | 特性版本号 |

## FeatureOptions

特性选项配置。

### 属性

| 名称 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| autoStart | boolean | 否 | 是否自动启动，默认 false |
| priority | number | 否 | 优先级，默认 0 |
