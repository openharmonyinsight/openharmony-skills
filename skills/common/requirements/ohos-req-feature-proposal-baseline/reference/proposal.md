---
target_release: ""
feature_id: ""        # 关联 platform_issues 的 FEAT-NNNNN
rr_id: ""             # RR单号：从 04-feature.md 继承
issue: ""
author: ""
date: ""
status: Draft        # Draft → GA-Approved
gate_a: ""           # GA 审视记录链接
---
# Proposal

> 模板定位：SDD 入口 proposal，归档到对应代码仓，过 GATE A(GA: Proposal Gate)。
> 以 ODK `core/templates/ai/proposal.md` 为基，融合 OpenSpec(Why) + MatrixSpec(User Stories/DFX)。
> requirements 阶段先落盘为 `proposals/05-proposal-<slug>.md`；进入 ODK 交付阶段时转换为 `.codespec/changes/<change-id>/proposal.md`，并满足 ODK `artifacts.yaml`。

## 1. 背景与问题（Why）
<!-- 动机、问题陈述、当前痛点（OpenSpec Why 风格） -->

| 字段 | 内容 |
|------|------|
| 需求ID | {feature_id} |
| RR单号 | {从 04-feature.md 继承} |

## 2. 初始分级判断
> L0/简单变更：非目标等章节可简化为一句话；L1+ 建议完整填写。

| 判断项 | 结果 | 依据 |
|--------|------|------|
| 复杂度 | 简单/标准/复杂/关键 | |
| 涉及仓数量 | | |
| 是否涉及 Public/System API | | |
| 是否涉及安全/性能关键路径 | | |
| 是否跨 SIG | | |

## 3. 目标 / 非目标
### 目标
### 非目标

## 4. Agent Scope Guard
> 约束 AI/Agent 的探索和修改边界。若需要突破边界，先更新本 proposal 并获得确认。

| 维度 | 范围/限制 | 需人工确认的触发条件 |
|------|-----------|----------------------|
| 允许仓库 | | |
| 允许模块/目录 | | |
| 禁止修改项 | | |
| 外部依赖/网络访问 | | |

## 5. 用户故事与能力（Capabilities）
| US# | As a... I want... so that... | 验收标准(AC) |
|-----|------------------------------|-------------|

## 6. 成功标准
> 每条标准必须可观察、可量化。

| 标准 | 可观察指标 | 验证方式 |
|------|-----------|---------|

## 7. 影响范围
| 子系统 | 仓库 | 模块/路径 | 影响类型 |
|--------|------|-----------|---------|

## 8. 假设与开放问题
### 假设
### 开放问题

## 9. 不涉及项确认（8 维）
| 维度 | 是否涉及 | 依据 |
|------|---------|------|
| 性能 | | |
| 安全/权限 | | |
| 兼容性 | | |
| API/SDK | | |
| IPC/跨进程 | | |
| 构建/组件 | | |
| 国际化/无障碍 | | |
| 数据迁移 | | |
