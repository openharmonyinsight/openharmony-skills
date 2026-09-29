# 0.12.0：Proposal ID 统一命名迁移

ODK 的归档身份现在统一称为 proposal ID，而不是外部需求编号。它仍由开发者提供，
正式编号只包含数字、不限制长度；保留前导零。已有数字目录不改名，也不重编编号。

## 字段和命令

| 旧名称 | 新名称 |
| --- | --- |
| 路径占位符 `<req-id>` | `<proposal-id>` |
| proposal.md frontmatter `req` | `proposal_id` |
| metadata_tracking.yaml `req_id` | `proposal_id` |
| 模板变量 `REQ_ID` | `PROPOSAL_ID` |
| `odk-link-req` / `link-req` | `odk-link-proposal` / `link-proposal` |

这是字段与命令的破坏性重命名，不保留双写字段或旧命令别名。升级后重新生成并安装
ODK 分发包，避免混用旧 skill 与新校验器。历史迁移文档中的路径示例应结合本文使用。

## 已有归档

1. 在业务仓中修改每个 proposal.md 的 YAML frontmatter：将唯一 `req` 键改为
   `proposal_id`，不修改正文、编号值、target_release 或其他字段。
2. metadata_tracking.yaml 若已存在，将唯一 `req_id` 键改为 `proposal_id`；
   保留仓库、PR、issue、SHA 等全部记录。文件不存在时不必为了迁移新建。
3. 正式归档的目录叶子、proposal.md 和 metadata 的 `proposal_id` 必须一致。
   草稿的 `proposal_id` 仍为空，取得编号后使用 `odk-link-proposal` 绑定。
4. 若旧、新字段同时存在或值冲突，先人工确认真实编号，再只保留一个新字段；
   不以“最后一个值”覆盖冲突。更新命令调用、脚本引用及模板变量。
5. 在业务仓执行 `validate-artifacts-contract.py <change-dir> --archive`；提交设计文档
   时再执行 `--design-docs-submit`。旧字段会被拒绝，不会静默当成未编号草稿。

仅字段重命名无需路径迁移 TSV。若还存在历史扁平目录，则另按归档迁移指南运行
`validate-archive-migration.py plan` / `check-staged`，目标文件必须使用新字段。
升级后已有文档仓副本也须显式同步，迁移本身不授权自动跨仓推送。
