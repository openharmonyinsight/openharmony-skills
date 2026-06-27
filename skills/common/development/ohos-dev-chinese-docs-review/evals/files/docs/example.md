# ExampleAPI

## 概述

ExampleAPI 提供示例功能，用于测试文档质量检查。

## 权限

无

## ExampleAPI.performOperation

performOperation(input: string): void

执行示例操作。

**系统能力**: SystemCapability.Example.Feature

**需要权限**: ohos.permission.EXAMPLE

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| input | string | 是 | 输入参数 |

**错误码**:

以下错误码的详细描述请参见[错误码](../error-codes.md)。

| 错误码ID | 错误信息 |
| ------- | ------- |
| 401 | Parameter validation failed. |
| 403 | Permission denied. |

## ExampleAPI.getState

getState(): number

获取当前状态。

**系统能力**: SystemCapability.Example.State

**返回值**:

| 类型 | 说明 |
| ---- | ---- |
| number | 当前状态值 |

## 错误码

以下错误码的详细描述请参见[错误码](../error-codes.md)。

| 错误码ID | 错误信息 |
| ------- | ------- |
| 401 | Parameter validation failed. |
| 403 | Permission denied. |
| 404 | Resource not found. |
| 500 | Internal service error. |
