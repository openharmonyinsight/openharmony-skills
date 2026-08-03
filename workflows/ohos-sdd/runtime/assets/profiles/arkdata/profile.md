---
name: arkdata
description: Use when working on ArkData — relational/kv/object storage, persistence, data management
repos:
  - distributeddata
applies_to:
  - "**/distributeddata/**"
subprofiles: []
---

# ArkData Profile

## 基本信息

| 项 | 内容 |
|----|------|
| Profile ID | `arkdata` |
| 适用对象 | ArkData / 数据管理 / 存储、同步、查询、模型演进相关特性、缺陷和设计任务 |
| 推荐复杂度 | 标准起步；跨存储层、跨同步链路、跨仓或高兼容性风险变更升级到 复杂/关键 |
| 触发条件 | 涉及数据模型、存储结构、查询接口、同步机制、迁移策略、一致性或兼容性约束 |
| 不适用场景 | 纯 UI 表现层或与数据存储、同步无关的轻量逻辑任务 |

## 对 4 阶段的补充约束

| 阶段 | 补充要求 |
|------|----------|
| Phase 1 (Define) | 显式确认数据模型、迁移、兼容性、一致性、权限和性能是否涉及 |
| Phase 2 (Specify) | 明确行为规则、数据契约、错误路径和兼容性要求；优先读取 `analysis/arkdata/`、ArkData 相关源码、现有模型和接口材料 |
| Phase 3 (Design) | 明确模型边界、存储层职责、同步链路、索引/查询影响和迁移策略 |
| Phase 4 (Plan) | 重点检查数据字段、默认值、迁移行为、错误路径和兼容性描述是否一致；增加 Owner / Committer 视角，重点关注模型演进、可维护性、性能、一致性和恢复能力 |

## 启用建议

- 对需求先确认是新增数据能力、修改既有模型，还是迁移/兼容性修复。
- 涉及 schema 变更、数据迁移、同步链路或恢复策略时，不要跳过 Phase 3 设计。
- 如现有分析资产不足，先补 `analysis/arkdata/` 再推进复杂设计。
