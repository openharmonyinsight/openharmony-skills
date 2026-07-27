# ArkUI Asset Model

## 三类资产

ArkUI 需求会同时涉及三类资产：

| 资产 | 路径 | 作用 |
|---|---|---|
| 流程实例 | `.codespec/changes/<id>/` | 单次需求的 proposal/spec/design/plan/review 和 gate 证据 |
| 长期规格 | `specs/<func-domain>/` | FuncID / FeatID 的长期行为事实和功能域设计 |
| SpecTest / Host Preview 用例 | `examples/SpecTest/...` | 可通过 Inspector 或 Host Preview 断言的 UI 行为验证 |

## 最低映射关系

ArkUI 任务至少要把下面几项映射清楚：

- `manifest.func_id`
- `manifest.feat_id`
- `manifest.profile`
- `manifest.subprofiles`
- `manifest.long_term_spec_path`
- `manifest.long_term_design_path`
- `manifest.spectest_feature_path`（如适用）

## 何时需要这份文档

- Define 阶段要判断是新增能力还是存量补规格
- Specify 阶段要确认当前变更对应哪个长期 Feat
- Plan 阶段要安排短期产物向长期 `specs/` 的回灌

## 不负责的内容

这里不定义 gate 结果，也不替代 `profile.md` 里的 Owner 必问项。它只解释资产之间的映射关系。
