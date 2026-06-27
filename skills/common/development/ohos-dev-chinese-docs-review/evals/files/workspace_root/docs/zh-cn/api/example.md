# ExampleComponent

## 概述

ExampleComponent 是一个示例组件，用于测试工作空间根路径发现功能。

## 权限

ohos.permission.EXAMPLE

## ExampleComponent.setProperty

setProperty(name: string, value: any): void

设置属性值。

**系统能力**: SystemCapability.Example.Property

**需要权限**: ohos.permission.EXAMPLE

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| name | string | 是 | 属性名称 |
| value | any | 是 | 属性值 |

## ExampleComponent.getProperty

getProperty(name: string): any

获取属性值。

**系统能力**: SystemCapability.Example.Property

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| name | string | 是 | 属性名称 |

**返回值**：

| 类型 | 说明 |
| ---- | ---- |
| any | 属性值，如果属性不存在返回 undefined |
