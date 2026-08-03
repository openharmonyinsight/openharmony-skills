---
name: arkgraphic
description: Use when working on graphic subsystem — 2D graphics, surface, composition, display
repos:
  - graphic_2d
  - graphic_surface
applies_to:
  - "**/graphic_2d/**"
  - "**/graphic_surface/**"
subprofiles: []
---

# ArkGraphic Profile

## 基本信息

| 项 | 内容 |
|----|------|
| Profile ID | `arkgraphic` |
| 适用对象 | ArkGraphic / 图形渲染 / 图像、合成、显示管线相关特性、缺陷和设计任务 |
| 推荐复杂度 | 标准起步；跨图形管线、跨硬件适配层、跨仓或高性能风险变更升级到 复杂/关键 |
| 触发条件 | 涉及渲染结果、图形管线、GPU/硬件差异、显示合成、图像处理、性能或稳定性约束 |
| 不适用场景 | 与图形渲染、显示、图像处理无关的一般业务逻辑或纯数据层任务 |

## 对 4 阶段的补充约束

| 阶段 | 补充要求 |
|------|----------|
| Phase 1 (Define) | 显式确认设备/GPU 差异、分辨率、帧率、功耗、稳定性和兼容性是否涉及 |
| Phase 2 (Specify) | 明确渲染行为、异常路径、性能约束和兼容性要求；优先读取 `analysis/arkgraphic/`、ArkGraphic 相关源码、图形链路设计材料 |
| Phase 3 (Design) | 明确图形管线边界、模块职责、资源生命周期以及硬件/驱动相关影响 |
| Phase 4 (Plan) | 重点检查渲染行为、资源状态、异常路径和兼容性描述是否前后一致；增加 Owner / Committer 视角，重点关注性能、内存、并发、资源管理和稳定性 |

## 启用建议

- 对图形需求先确认是渲染结果调整、管线行为修改、图像处理增强，还是硬件适配问题修复。
- 涉及资源生命周期、GPU 差异、合成链路或高性能风险时，不要跳过 Phase 3 设计。
- 如现有分析资产不足，先补 `analysis/arkgraphic/` 再推进复杂设计。
