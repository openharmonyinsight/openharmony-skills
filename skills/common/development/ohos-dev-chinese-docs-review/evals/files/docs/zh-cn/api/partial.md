# PartialAPI

## 概述

PartialAPI 提供部分功能接口。本文档仅包含公共 API 文档，系统 API 和错误码文档尚未完成。

## PartialAPI.getData

getData(): Promise\<DataItem[]\>

获取数据列表。

**系统能力**: SystemCapability.PartialAPI.Data

**返回值**：

| 类型 | 说明 |
| ---- | ---- |
| Promise\<DataItem[]\> | 数据项列表 |

## PartialAPI.setData

setData(items: DataItem[]): Promise\<void\>

设置数据列表。

**系统能力**: SystemCapability.PartialAPI.Data

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| items | DataItem[] | 是 | 数据项列表 |

**错误码**：

| 错误码ID | 错误信息 |
| ------- | ------- |
| 201 | Parameter validation failed. |
| 202 | Data size exceeds limit. |

## DataItem

数据项类型定义。

### 属性

| 名称 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| id | string | 是 | 数据项唯一标识 |
| name | string | 是 | 数据项名称 |
| value | number | 否 | 数据项数值 |
