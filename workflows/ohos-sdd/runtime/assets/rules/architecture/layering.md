# Rule: 分层架构

## Rule ID

OH-ARCH-LAYERING

## Applies To

- Feature Design
- Feature Spec
- Task Spec
- AI implementation
- Design / GB 基线审查

适用于所有涉及应用层、框架层、系统服务层、内核层调用关系的变更。

## Must

- 必须识别本次变更涉及的 OpenHarmony 层级。
- 必须遵循应用层 → 框架层 → 系统服务层 → 内核层的单向依赖。
- 必须通过框架层公开 API 或 Kit 访问系统能力。
- 必须在 `design.md` 中说明调用方向、调用边界和依赖理由。
- 必须在 `spec.md` 或 Task Spec 中记录受影响模块、接口和验证方式。

## Must Not

- 禁止下层反向依赖上层。
- 禁止应用层直接调用系统服务层或内核层内部接口。
- 禁止跳过框架层直接访问系统服务能力。
- 禁止新增循环依赖。
- 禁止为了绕过编译依赖而引入不属于当前层级的内部头文件或实现类。

## Evidence

- `design.md` 中的适用架构规则和架构图。
- `spec.md` 中的架构约束表。
- BUILD.gn、bundle.json、include/import 变更说明。
- Design / GB 架构评审记录。
- 如存在跨层调用，需提供接口路径和验证结果。

## Check

- 检查调用链是否符合单向依赖。
- 检查新增 deps、include/import 是否引入反向依赖或跨层直接依赖。
- 检查应用层是否只通过公开 API、System API 或 Kit 使用系统能力。
- 检查设计文档是否说明例外情况、降级方案或迁移路径。
