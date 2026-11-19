# Validation Checklist

手动校验清单，按 validator Level 组织。在 `ohdk validate` 脚本就绪前使用本清单逐项检查。

---

## Level A: Init (初始化后)

- [ ] `codespec/changes/` 目录存在
- [ ] 路径为 `codespec/changes/<repo-name>/<proposal-id-or-draft>/`，仓名与 Git `origin`（无 origin 时为工作树根目录名）一致
- [ ] 正式目录叶子为纯数字 `<proposal-id>`（不限制长度）；`proposal.md` frontmatter 的 `proposal_id:` 必须与目录名完全一致
- [ ] 草稿目录名格式正确（`draft-<yyyymmdd>-<english-slug>`），且位于 `<repo-name>` 层下
- [ ] `english-slug` 仅含小写字母、数字和分隔非空片段的连字符，长度不超过 40；目录名在 `codespec/` 下唯一
- [ ] 必需归档文件列表存在 (proposal.md + spec.md + design.md + execution-plan.md)
- [ ] 文件可为空或含模板占位符

## Level B: Draft (草稿阶段)

- [ ] 各文档必需章节标题存在 (见 contracts.md 各类型章节契约)
- [ ] 允许部分内容简略或非关键占位

## Level C: Review (审查阶段)

- [ ] 所有必需章节有实质内容 (非仅标题)
- [ ] `execution-plan.md` AC-Task 追溯表无空行
- [ ] 可选过程证据如存在，应位于 `evidence/` 下，不作为最小归档 contract

## Level D: Archive (归档前)

- [ ] 无关键占位符 (`TBD`、`TODO` 等)
- [ ] `execution-plan.md`「AC 到 Task 追溯」无空行 +「代码范围映射」每个 Task 有文件
- [ ] `execution-plan.md` 每个 Task 有完成判据和代码范围
- [ ] 如存在可选 review/verification 证据，应包含 spec-compliance + code-quality + verification
- [ ] 如存在可选 verification 证据，应有明确的「代码与规格一致性结论」
- [ ] 追溯链完整 (proposal → spec AC → execution-plan Task → code → commit → review)；commit 与 PR 的实际关联由 `metadata_tracking.yaml` 的 `pull_requests.commit` 校验负责，Python 校验器不按本行自动生成检查
- [ ] 实现的 commit message 包含关联的 `proposal-id`
- [ ] 准备向 GitCode 提交代码时，已提醒用户将 `codespec/` 文档单独提交到 `codespec/profile.yaml` 的 `design_docs_repository`；地址缺失时明确标记“待开发者填写”，不得猜测或自动跨仓推送
- [ ] 实际提交 design-docs 前已生成或刷新 `metadata_tracking.yaml`，并用 `--design-docs-submit` 验证 `proposal.md`、`spec.md`、`design.md`、`execution-plan.md` 与该文件组成的五件套；业务代码 PR 未创建时 `pull_requests: []` 合法
- [ ] **API 设计校验**：
  - `API/SDK=否` 时：`spec.md` 的 `## API 规格定义` 填写 `不涉及：<具体理由>`，且不得存在 `arkts-api-spec.yaml`、`c-api-spec.yaml`。
  - `API/SDK=是` 时：适用 metadata 文件必须存在并通过结构校验；`spec.md` 仅保留 API 概览和确认指引，不得重新展开逐 API 规格。
  - 适用 metadata 文件必须包含 API kind、ID、父级、声明、参数、返回值、错误码、权限、`@syscap`、`@since`、平台支持、FA/Stage 模型、设备支持与差异，以及双语三要素/五要素。
  - API 文档三要素/五要素必须由 `odk-spec` 内的隔离 subagent 生成；subagent 不可用属于 spec 阶段失败，不允许主会话内联降级。
  - `API/SDK=是` 时必须归档适用 metadata 文件和按语言拆分的声明 diff：ArkTS 为 `task1-arkts-api-declaration-en/zh.diff`，C 为 `task1-c-api-declaration-en/zh.diff`；声明 diff 须与对应 metadata 的 API 声明一致，且不得混合不同 API 声明仓库。每个 API 的完整声明注释块与声明必须位于同一个连续 hunk；同签名 API 必须提供 API ID / qualifiedName 或唯一源位置，防止复用声明证据。
  - 声明注释须逐项体现 metadata 的 API 级 8 个描述字段、参数描述、返回值描述和错误码描述；仅显式 `N/A` / `不适用` 字段必须省略，且声明注释中不得输出 `N/A` / `不适用` 占位文本；非 `N/A` 内容不得合并、截断或丢失。描述字段值直接成行，不得输出 `Scenario:` / `Notes:` 等要素类型标签，也不得复述 `@since`、`@syscap`、权限、平台、错误码等结构化属性。声明注释排版须与声明对齐，`*/` 与声明之间不得有空行；API 级描述与参数/返回值描述不得重复同一行为子句。
