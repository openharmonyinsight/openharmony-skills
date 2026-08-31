# Validation Checklist

手动校验清单，按 validator Level 组织。在 `ohdk validate` 脚本就绪前使用本清单逐项检查。

---

## Level A: Init (初始化后)

- [ ] `codespec/changes/` 目录存在
- [ ] 正式变更目录名格式正确（`<req-id>-<english-slug>`）；`proposal.md` frontmatter 的 `req:` 必须有效、不是保留旧格式 `issue-<digits>`，且与目录精确前缀一致
- [ ] 草稿目录名格式正确（`draft-<yyyymmdd>-<english-slug>`）
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
- [ ] 追溯链完整 (AC → Task → code → commit → review)
- [ ] 实现的 commit message 包含关联的 `req-id`
- [ ] **API 设计校验**：
  - 校验 `proposal.md` 的 `## API 设计属性` 与 `spec.md` 的 `## API 规格定义` 已填写（`API/SDK` = 否时均标注"不涉及"）。API 仓库路径/commit、既有声明格式参考为过程信息，不要求体现在 spec.md 中。
  - 如 `API/SDK` = 是，校验声明文件修改 diff 已归档到 `codespec/changes/<req-id>-<english-slug>/`（声明文件 PR 由开发者自行管理）。
