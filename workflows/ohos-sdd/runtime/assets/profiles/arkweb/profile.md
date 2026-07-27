---
name: arkweb
description: Use when working on ArkWeb / WebView / Chromium integration — input events, rendering behavior, compatibility
repos:
  - web_webview
applies_to:
  - "**/web_webview/**"
subprofiles: []
---

# ArkWeb Profile

## 基本信息

| 项 | 内容 |
|----|------|
| Profile ID | `arkweb` |
| 适用对象 | ArkWeb / web_webview / Chromium 相关特性、缺陷和设计任务 |
| 推荐复杂度 | 标准起步；跨仓、跨接口或高风险变更升级到 复杂/关键 |
| 触发条件 | 涉及 ArkWeb、WebView、Chromium 对接、输入事件、渲染行为、兼容性约束 |
| 不适用场景 | 与 ArkWeb 无关的一般系统服务或基础库任务 |

## 对 4 阶段的补充约束

| 阶段 | 补充要求 |
|------|----------|
| Phase 1 (Define) | 显式确认 OHOS 版本、设备范围、输入设备、兼容性和 DFX 是否涉及 |
| Phase 2 (Specify) | 明确行为规则、兼容性和异常路径；优先读取 `context-engine/analysis/arkweb/`、ArkWeb 相关源码、试点分析材料 |
| Phase 3 (Design) | 明确 ArkWeb 与上层应用/框架、下层 Chromium 或平台适配边界，沉淀模块关系和接口约束 |
| Phase 4 (Plan) | 重点检查实现范围、验证路径与兼容性闭环；增加 Committer / Owner 视角，重点关注线程、安全、性能、可测试性 |

## 专项检查清单

### 定义阶段 N/A 确认重点
- [ ] Chromium 侧依赖（CDP/Mojo/CEF API）是否涉及
- [ ] 跨仓调用链路（openharmony_master ↔ arkweb_144）是否涉及
- [ ] Public API 变更是否涉及（Web Kit 接口）
- [ ] 跨 SIG 协作是否涉及（ArkWeb SIG + ArkUI SIG 等）

### 上下文重点
- [ ] Chromium 侧接口能力（CEF Host / CDP Handler / Mojo IPC）
- [ ] NWeb 接口层与胶水层桥接机制
- [ ] 已有实现的实际路径（不要基于文档假设，需源码确认）

### 规范符合性重点
- [ ] 参数校验层级：应用层是否做了前置参数完整性检查，不依赖底层侧校验
- [ ] 多执行路径的回调格式统一性
- [ ] API 兼容性：入参出参变更是否有 @since 版本标注和迁移指引
- [ ] JS 注入约束：Spec 是否明确禁止/允许 JS 注入路径

### 代码质量重点
- [ ] 异步回调对象的生命周期管理（CefRefPtr / delete this 等模式安全性）
- [ ] 跨进程回调线程安全性
- [ ] 坐标/路径类参数的边界处理

### 验证重点
- [ ] HTML 测试页验证操控类功能触发正确的 DOM 事件
- [ ] 跨仓编译通过（openharmony_master + arkweb_144）
- [ ] 异常场景覆盖（非法输入、元素不存在、底层错误回传）

## 专家角色

| 角色 | 介入阶段 | 职责 | 对应 review.md 维度 |
|------|----------|------|---------------------|
| chromium-reviewer | Phase 3 设计 + Plan 后审查 | 审查 Chromium 侧调用链路安全性、CEF API 使用正确性 | 架构审查 → Chromium 专项 |
| api-reviewer | Phase 3 设计 | 审查 Public API 变更、d.ts 签名、SysCap 声明、@since 版本标注 | 接口审查 → API 兼容性 |

### 介入规则
- 涉及 Chromium 侧（CDP/CEF/Mojo）调用时 chromium-reviewer 必须介入
- 涉及 Public API 变更时 api-reviewer 必须介入
- 跨仓修改时两个角色都应介入

## 上下文来源

| 优先级 | 来源 | 仓库地址 | 用途 |
|--------|------|----------|------|
| P0 | arkweb_144 源码（NWebImpl / CEF Host / CDP Handler） | `gitcode.com/openharmony-tpc/chromium_arkweb`（Chromium 内核适配仓） | 实现路径验证、已有能力确认 |
| P0 | Chromium CDP Protocol（.pdl 文件） | Chromium 源码 `content/browser/devtools/protocol/` | CDP 命令参数和响应格式 |
| P1 | context-engine/analysis/arkweb/ | 本仓库 `openharmony/context-engine/analysis/arkweb/` | 架构分析、组件知识 |
| P1 | openharmony_master 源码（NAPI / NWeb 接口 / 胶水层） | `gitcode.com/AkashiKaiki/web_webview`（个人 fork，官方仓库见 openharmony-tpc/web_webview） | 接口层和桥接层验证 |

### 使用规则
- Phase 1 澄清阶段必须搜索源码确认“已有实现现状”，不要基于文档假设
- Phase 3 设计阶段应并行搜索两个仓的源码，交叉验证接口声明与实现
- 底层协议命令选择需引用具体协议定义文件

## 启用建议

- 对新需求先判断是"ArkWeb 新设计"还是"基于存量行为增量修改"
- 遇到 Chromium 侧依赖、跨模块调用或复杂输入链路时，不要跳过 Phase 3 设计
- 如历史分析材料不足，先补 `context-engine/analysis/arkweb/` 再推进复杂设计
