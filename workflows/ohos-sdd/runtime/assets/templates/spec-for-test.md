---
artifact: spec-for-test
status: Draft
source_spec: spec.md
source_spec_hash: {{SOURCE_SPEC_HASH}}
source_design: design.md
source_design_hash: {{SOURCE_DESIGN_HASH}}
source_consistency: current
profile: {{PROFILE}}
subprofiles:
  - {{SUBPROFILE}}
generated_at: {{GENERATED_AT}}
---

# {{PROFILE_TITLE}}

> Profile 定义的 Spec for Test 旁路产物，面向测试工程师和测试设计 Agent。
> 用户故事、AC、规则、API、兼容性和非功能性要求来自 Approved `spec.md`；验证点和专项分析由命中的 Profile 声明。
> `GENERATED:*` 区域只能由 CLI 生成或刷新，禁止摘要、删减或手工改写；人工只填写 `TEST-ANALYSIS` 区域。

## 元信息

| 字段 | 内容 |
|---|---|
| Profile | `{{PROFILE}}` |
| 输入 | Approved `spec.md` + `design.md` |
| 输出用途 | 测试设计输入，不包含测试执行结果 |

<!-- GENERATED:EXTERNAL-SPEC:BEGIN -->
{{EXTERNAL_SPEC}}
<!-- GENERATED:EXTERNAL-SPEC:END -->

## 六、测试可观察性与验证约束 `[源: design.md]`

<!-- GENERATED:DESIGN-CONSTRAINTS:BEGIN -->
{{DESIGN_CONSTRAINTS}}
<!-- GENERATED:DESIGN-CONSTRAINTS:END -->

<!-- TEST-ANALYSIS:BEGIN -->
## 七、AC 到验证点追溯

{{AC_VERIFICATION}}

{{PROFILE_ANALYSIS_SECTIONS}}

## {{PENDING_SECTION_HEADING}}

- 待确认：由生成 Agent 基于 Approved Spec/Design 完成验证点和 Profile 专项分析后删除本项。
<!-- TEST-ANALYSIS:END -->

## {{APPROVAL_SECTION_HEADING}}

| 项 | 内容 |
|---|---|
| Spec 来源 | `spec.md` / `{{SOURCE_SPEC_HASH}}` |
| Design 来源 | `design.md` / `{{SOURCE_DESIGN_HASH}}` |
| 开发/Spec Owner 结论 | 待审批 |
| 测试 Owner 结论 | 待审批 |
