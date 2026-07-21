# Payment API 集成与安全 验证规格

> 基于 spec.md 和 design.md 派生。spec.md 已描述的正常流程、异常规则、错误码不在此重复，
> 仅补充集成 / 系统验证视角的增量场景（重点：Binder 边界安全鉴权、重放 / 篡改、并发、超时崩溃隔离）。
> 场景关联 spec.md AC 编号 **和** threat-model.md 威胁 / 缓解编号，保持追溯链完整。

## 概述

| 属性     | 值              |
| -------- | --------------- |
| 关联 AC  | AC-1.1 ~ AC-2.2 |
| 验证层级 | L2/L3           |

标签: `security` `regression` `api` `smoke`

## 验证范围

**验证重点**: `PaymentAPI` 公开接口的端到端集成行为，以及 `threat-model.md` 识别的 Binder 边界安全控制（D-001 三段鉴权、D-003 AES-256-GCM 认证加密 + Nonce 防重放）在系统层是否真实生效。

**非验证重点**: 单元测试覆盖的凭证字段校验逻辑、回调字段装配（由单元测试覆盖）。

## 环境前置与公共配置

- 已初始化支付 SDK 并注册 `PaymentCallback` 的测试应用
- 设备支持 TEE / KeyMint（支付凭证密钥由 KeyMint 保护，BR-001）
- 支付服务（system ability）已启动并注册到 servicemanager
- 攻击模拟工具：可伪造 Binder 调用方 UID / 签名 / 权限令牌的测试进程；可抓取并重放 Binder 报文的工具

## 场景

> 所有场景锚定本次变更的修改点路径（PaymentAPI → Binder → 支付服务 → TEE/KeyMint），
> 不重复 spec.md AC 已覆盖的正常 / 异常单接口流程，只补充集成验证角度的增量场景。

### SC-1: 伪造身份调用支付 Binder 被三段鉴权拒绝（security）

标签: `security`

> 系统视角：支付服务 Binder 鉴权层（D-001）的内部拦截行为。上层触发 = 恶意 / 被攻破应用尝试发起支付。

* Given 攻击者应用未持有支付权限令牌，或签名 / UID 与已授权应用不符
* When 攻击者应用绕过 SDK、伪造身份直接经 Binder 调用 `PaymentAPI.request()`
* Then 支付服务三段鉴权（UID + 签名 + 权限令牌，D-001）校验失败，请求被拒绝，不进入支付流程
* And 不返回可推断鉴权细节的信息（不暴露「哪个因子失败」），凭证不离开 TEE
* 关联: spec.md AC-1.1 / AC-1.2 / threat-model.md TH-001（Binder Spoofing）→ D-001

---

### SC-2: 重放 / 篡改 Binder 凭证密文被认证加密拦截（security）

标签: `security`

> 系统视角：Binder 信道 D-003（AES-256-GCM 认证加密 + Nonce 防重放）。上层触发 = 中间人抓取并重放 / 篡改支付请求报文。

* Given 攻击者已抓取一次合法的支付 Binder 报文（含凭证密文）
* When 攻击者原样重放该报文，或篡改密文中的金额 / 凭证字段后重发
* Then AES-256-GCM tag 校验失败（篡改）或 Nonce 重复命中防重放（重放），支付服务拒绝该请求
* And 重放不产生重复交易；篡改不触发任何支付动作
* 关联: spec.md AC-1.1 / threat-model.md TH-003（Binder Tampering）、TH-005（重放）→ D-003

---

### SC-3: 并发支付请求互不串单（integration）

标签: `regression`

* Given 测试应用同时发起多笔支付请求（不同金额、不同凭证）
* When 多笔 `request()` 并发到达支付服务
* Then 每笔请求独立处理，各自回调携带唯一且正确的 `transactionId`（AC-2.1），不出现串单 / 错配
* And 任一笔失败不影响其他笔的回调与错误码（AC-2.2）
* 关联: spec.md AC-2.1 / AC-2.2

---

### SC-4: 支付服务超时 / 崩溃不泄露进行中凭证（系统视角）

标签: `regression`

> 系统视角：超时与崩溃隔离。上层触发 = 应用发起支付后，支付服务长时间无响应或中途崩溃。

* Given 应用已发起支付请求，凭证密文已发出
* When 支付服务 >5s 无响应，或处理中途崩溃
* Then SDK 在 5s 后回调 `onPaymentFailed(errorCode=1002 ERR_TIMEOUT, message)`（AC-1.3 / AC-2.2）
* And 进行中的凭证不在 REE / 日志 / 崩溃 dump 中残留（符合 BR-001 KeyMint 保护、缓解 TH-002 Info Disclosure）
* 关联: spec.md AC-1.3 / AC-2.2 / threat-model.md TH-002（REE Info Disclosure）/ TH-006（DoS）→ D-002
