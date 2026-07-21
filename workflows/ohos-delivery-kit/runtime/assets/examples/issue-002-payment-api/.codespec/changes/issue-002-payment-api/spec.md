# Spec

## 概述

| 属性 | 值 |
|------|-----|
| 特性名称 | 支付 SDK API |
| 特性编号 | PAY-001 |
| 优先级 | P0 |
| 复杂度 | 复杂 |
| 目标版本 | 1.0 |

## 用户故事或场景

### US-1: 发起支付请求

**作为** 应用开发者，**我想要** 调用支付 API 发起支付，**以便** 用户完成商品购买。

**验收标准：**
- **AC-1.1:** WHEN 应用调用 PaymentAPI.request() THEN 验证调用者身份并传递请求到支付服务
- **AC-1.2:** WHEN 支付凭证不完整或无效 THEN 返回错误码 ERR_INVALID_CREDENTIALS
- **AC-1.3:** WHEN 支付服务超时（>5秒）THEN 返回错误码 ERR_TIMEOUT

### US-2: 支付结果通知

**作为** 应用开发者，**我想要** 接收支付结果回调，**以便** 更新应用状态。

**验收标准：**
- **AC-2.1:** WHEN 支付成功 THEN 回调 onPaymentSuccess() 包含交易 ID
- **AC-2.2:** WHEN 支付失败 THEN 回调 onPaymentFailed() 包含错误码和错误描述

## 业务规则

| 规则 ID | 规则描述 | 约束条件 | 关联 AC |
|---------|----------|----------|---------|
| BR-001 | 支付凭证必须通过 KeyMint 保护 | 禁止明文传递凭证 | AC-1.1 |
| BR-002 | 跨进程通信必须验证调用者身份 | Binder 身份验证 | AC-1.1 |
| BR-003 | 支付凭证传输必须加密 | 使用 AES-256-GCM | AC-1.1 |

## 异常与边界规则

| 编号 | 场景 | 触发条件 | 系统行为 | 关联 AC |
|------|------|----------|----------|---------|
| ERR-001 | 凭证无效 | 签名验证失败 | 返回 ERR_INVALID_CREDENTIALS | AC-1.2 |
| ERR-002 | 服务超时 | 响应时间 > 5000ms | 返回 ERR_TIMEOUT | AC-1.3 |

## 错误码定义

| 错误码 ID | 错误码值 | 含义 | 关联 AC |
|-----------|----------|------|---------|
| ERR_INVALID_CREDENTIALS | 1001 | 支付凭证无效或签名错误 | AC-1.2 |
| ERR_TIMEOUT | 1002 | 支付服务响应超时 | AC-1.3 |
| ERR_INSUFFICIENT_BALANCE | 1003 | 账户余额不足 | AC-2.2 |

## 接口变更分析

### 新增接口

| 接口名称 | 开放级别 | 参数概要 | 返回值 | 错误码 | 关联 AC |
|----------|----------|----------|--------|--------|---------|
| PaymentAPI.request | Public | amount: uint64, credential: EncryptedData | TransactionResult | 1001, 1002 | AC-1.1, AC-1.2, AC-1.3 |
| PaymentCallback.onSuccess | Public | transactionId: string | void | - | AC-2.1 |
| PaymentCallback.onFailed | Public | errorCode: int, message: string | void | 1001, 1002, 1003 | AC-2.2 |

### 变更/废弃接口

无

## 兼容性声明

- **已有 API 行为变更:** 否
- **配置文件格式变更:** 否
- **数据存储格式变更:** 否

## 验证映射

| AC | 关联规则 | 验证方式 | 证据 |
|----|----------|----------|------|
| AC-1.1 | BR-001, BR-002, BR-003 | 安全测试、IPC 验证 | 安全测试报告 |
| AC-1.2 | - | 异常测试 | 测试报告 |
| AC-1.3 | - | 超时测试 | 测试报告 |
| AC-2.1 | - | 集成测试 | 测试报告 |
| AC-2.2 | - | 集成测试 | 测试报告 |

## 测试设计提示

> 面向 AI 生成测试和实现计划。每条 AC 至少给出一个测试入口；`Red 条件` 必须说明实现前为什么会失败，避免写出立即通过的无效测试。

| AC | 测试类型 | 测试文件 | 测试名称 | 输入/触发 | 期望输出/错误 | Red 条件 |
|----|----------|----------|----------|-----------|---------------|----------|
| AC-1.1 | 集成测试 | payment/sdk/payment_api_test.cpp | RequestForwardsToServiceWithAuth | 已授权应用调 request(amount, credential) | 支付服务收到鉴权后的请求 | Binder 鉴权+转发链路尚未实现 |
| AC-1.2 | 单元测试 | payment/sdk/payment_api_test.cpp | RequestRejectsInvalidCredential | 签名错误/不完整凭证 | ERR_INVALID_CREDENTIALS (1001) | 凭证校验未接入 |
| AC-1.3 | 集成测试 | payment/sdk/payment_api_test.cpp | RequestReturnsTimeoutOnSlowService | 支付服务 >5s 无响应 | ERR_TIMEOUT (1002) | 超时定时器未实现 |
| AC-2.1 | 集成测试 | payment/sdk/payment_callback_test.cpp | OnSuccessCarriesTransactionId | 支付成功回调 | onPaymentSuccess(transactionId) 含非空交易 ID | 回调未携带交易 ID |
| AC-2.2 | 集成测试 | payment/sdk/payment_callback_test.cpp | OnFailedCarriesCodeAndMessage | 支付失败回调 | onPaymentFailed(code, message) 含错误码与描述 | 失败回调字段未填充 |

> AC → 实现文件 + Task + 验证状态的映射见 `execution-plan.md`「AC 到 Task 追溯」+「代码范围映射」。
