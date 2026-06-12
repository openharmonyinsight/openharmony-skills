# Utils

## 概述

Utils 模块提供数据处理相关的工具函数。

## Utils.formatDate

formatDate(timestamp: number, format?: 'short' | 'long' | 'iso'): string

格式化时间戳为日期字符串。

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| timestamp | number | 是 | Unix 时间戳（毫秒） |
| format | string | 否 | 输出格式：'short' \| 'long' \| 'iso'，默认为 'short' |

**返回值**：

| 类型 | 说明 |
| ---- | ---- |
| string | 格式化后的日期字符串 |

## Utils.validateEmail

validateEmail(email: string): boolean

验证邮箱地址格式。

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| email | string | 是 | 待验证的邮箱字符串 |

**返回值**：

| 类型 | 说明 |
| ---- | ---- |
| boolean | 有效返回 true，否则返回 false |

## Utils.safeParse

safeParse\<T\>(json: string, fallback: T): T

安全解析 JSON 字符串。

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| json | string | 是 | 待解析的 JSON 字符串 |
| fallback | T | 是 | 解析失败时的默认值 |

**返回值**：

| 类型 | 说明 |
| ---- | ---- |
| T | 解析成功返回对象，失败返回 fallback |
