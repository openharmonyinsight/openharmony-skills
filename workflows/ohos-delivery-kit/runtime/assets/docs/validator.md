# Validator

## 目标

validator 是 `ohos-delivery-kit` 的唯一强耦合点。

无论团队使用什么插件、什么流程、什么写作风格，最终都必须通过同一个 validator，交付件才算正式可归档。

## 设计原则

### 1. 统一验证口

验证口只能有一个。

这意味着：

- 插件可以自由组合
- prompt 可以各不相同
- 业务团队可以有自己的执行习惯
- 但正式交付判断不能分散到不同插件内部

### 2. 渐进严格度

validator 不应一开始就要求所有内容满配。

应按阶段逐步收紧：

- 初始化阶段：只检查结构
- 草拟阶段：允许部分占位
- 归档前：严格检查章节和一致性

### 3. 先结构，后语义

当前先解决：

- 有没有
- 是否放对地方
- 关键章节是否存在
- 文档之间是否能互相对应

复杂语义质量判断按高收益路径逐步收紧；当前已覆盖关键表格和追溯链，不做自然语言质量评分。

## 命令模型

建议首批命令：

```text
ohdk init <id>
ohdk validate <path>
ohdk status <path>
```

其中：

- `init`
  - 创建 `.codespec/changes/<id>/` 骨架
- `validate`
  - 校验结构、章节、关键表格和一致性
- `status`
  - 展示当前完成度和阻塞项

如果后续需要兼容多平台，也应保持这组命令语义稳定，不要让平台包各自发散。

## 当前脚本入口

在正式 `ohdk validate` CLI 落地前，仓库内使用以下脚本分层验证：

| 脚本 | 用途 | 严格度 |
|------|------|--------|
| `scripts/validate-artifacts-structural.sh <change-dir>` | 宽松结构检查：目录、文件、关键章节抽样 | Level A/B |
| `scripts/validate-artifacts-contract.py <change-dir>` | 草稿/审查 contract 检查：必需文件、必需章节、条件章节提示、关键表格语义、AC→Task→代码范围映射追溯、可选 evidence 目录存在性 | Level A-C + optional evidence |
| `scripts/validate-artifacts-contract.py --archive <change-dir>` | 归档前严格检查：在 contract 检查基础上要求无关键占位、代码范围映射已回填、Task `Actual Result` 已回填、evidence 结论不与未完成产物矛盾 | Level D |
| `scripts/check-examples.sh` | 样例与模板同步检查，并调用 artifact contract 校验 | 示例回归 |
| `scripts/validate-contracts.sh` | `core/contracts/artifacts.yaml` 与核心模板一致性 | 维护期 |
| `scripts/validate-distribution.sh` | 分发产物、contract、adapter、文档漂移和确定性检查 | 维护期 |

## 验证维度

### 1. 结构完整性

检查：

- `.codespec/changes/` 目录是否存在
- 变更目录名是否符合 `issue-<issue-number>-<slug>` 格式
- 必需归档文件是否存在（proposal.md, spec.md, design.md, execution-plan.md）

### 2. 章节完整性

检查：

- `proposal.md`、`spec.md`、`design.md`、`execution-plan.md` 是否包含必需章节
- 可选 `evidence/reviews/` 如存在，是否覆盖符合性、质量、风险和验证证据

### 3. 交叉一致性

检查：

- `spec.md` 验证映射表覆盖所有 AC，且每个 AC 有非空验证方式
- `execution-plan.md` 的 AC-Task 追溯表覆盖所有 AC，且每个 AC 有 Task 和验证方式
- `execution-plan.md` 的 Task 列表覆盖所有被追溯的 Task，且包含 AC 映射、完成判据和验证命令
- `execution-plan.md` 的 Task 详情包含 Files 表和 Verification 表，且有文件范围和期望验证结果
- `execution-plan.md` 代码范围映射的每个被追溯 Task 都有非空文件（archive 严格模式额外校验）
- 可选 `evidence/reviews/spec-compliance.md` 如存在，是否覆盖了所有 AC

## 分阶段严格度

### Level A: Init

目的：

- 建骨架

要求：

- 目录存在
- 必需文件存在

允许：

- 文档为空
- 模板占位符存在

### Level B: Draft

目的：

- 形成可审查草稿

要求：

- 主要文档章节齐全

允许：

- 部分内容较简略
- 少量非关键占位仍存在

### Level C: Review

目的：

- 进入正式审查

要求：

- 必需章节有实质内容
- 关键交叉引用可解析

### Level D: Archive

目的：

- 正式归档

要求：

- 无关键占位符
- 章节和引用全部一致
- `execution-plan.md`「AC 到 Task 追溯」验证状态、「代码范围映射」实际文件已回填
- `execution-plan.md` Task 详情中的 `Actual Result` 已回填
- 如存在可选过程证据，验证证据齐全且可追溯

## 已落地校验范围

默认 contract 校验已覆盖：

- 目录存在性
- 必需文件存在性
- 目录名格式正确（`issue-<issue-number>-<slug>`）
- 文档必需章节标题
- 条件章节缺失提示
- spec 验证映射表完整性
- AC 到 Task 追溯表完整性
- Task 列表和 Task 详情表格完整性
- 可选 evidence 目录存在性和非空检查

`--archive` 归档模式额外覆盖：

- 必需归档件必需章节中的关键占位符（`TBD`、`TODO`、`待定`、`待补充` 等）
- `execution-plan.md`「AC 到 Task 追溯」验证状态、「代码范围映射」实际文件
- `execution-plan.md` Verification 表的 `Actual Result`
- required artifacts 未完成时，evidence 不应声明 `PASS` / `Ready` / `通过` / `可归档`

这些检查仍然避免依赖外部包和自然语言评分，重点防止空表、漏 AC、漏 Task、漏验证方式这类高频交付质量问题。

## 后续增强

第二阶段可增加：

- `target_release` 引用一致性
- 关联项解析
- review 证据与 AC/Task 的显式映射

第三阶段再考虑：

- 章节内容充分性
- 条件章节触发条件的自动判定

## 与 adapter 的边界

adapter 负责把插件输出落回标准目录。

validator 负责判断这些标准目录下的内容是否合规。

因此：

- adapter 可以多种多样
- validator 必须保持单一

如果某个插件只能在自己的私有目录中通过检查，而无法通过标准 validator，它就不适合作为正式归档链路的一部分。
