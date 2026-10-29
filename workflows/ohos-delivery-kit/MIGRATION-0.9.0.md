# ODK 0.9.0 仓库分层归档迁移指南

ODK 0.9.0 将正式归档从
`codespec/changes/<proposal-id>-<english-slug>/` 切换为
`codespec/changes/<repo-name>/<proposal-id>/`。这是不向后兼容的变更。

`repo-name` 优先取 Git `origin` URL 的仓名（去掉 `.git`）；没有 `origin` 时取工作树根目录名。正式目录叶子只保留 `proposal-id`，英文简述仅保留在尚未取得编号的草稿目录：

```text
codespec/changes/<repo-name>/draft-<yyyymmdd>-<english-slug>/
```

取得编号后运行 `odk-link-proposal`，将草稿重命名为：

```text
codespec/changes/<repo-name>/<proposal-id>/
```

## 迁移存量正式目录与在途草稿

先在独立分支确认仓名和每个旧目录的 `proposal_id:`，并将 TSV 映射文件放在工作树外：

```text
.codespec/changes/issue-9988-legacy-focus	9988
codespec/changes/REQ-12345-arkui-focus	12345
codespec/changes/REQ-PLAT-88-render-cache	88
codespec/changes/draft-20260831-new-focus	-
```

第二列为开发者确认的纯数字 `proposal-id`；旧目录名可以继续包含历史字母前缀，迁移结果只使用第二列。尚未取得编号的合法 `draft-*` 使用单个 `-`，工具会保留
完整 draft 目录名，只增加 `<repo-name>` 层。不得为草稿虚构proposal ID。映射必须覆盖工具
发现的全部隐藏 `issue-*`、0.8 扁平正式目录和 0.8 扁平 draft，且不能重复源或目标。

迁移前检查和打印移动计划：

```bash
python3 runtime/executables/validate-archive-migration.py plan --map ../odk-0.9-archive-map.tsv --repo .
```

按 `PLAN` 输出执行 `git mv`。正式目录须将 proposal frontmatter 的 `proposal_id:` 更新为映射第二列的纯数字编号；
draft 的 `proposal_id:` 保持为空或不存在。更新仓内所有旧路径引用并暂存完整迁移后，使用同一份
映射执行：

```bash
python3 runtime/executables/validate-archive-migration.py check-staged --map ../odk-0.9-archive-map.tsv --repo .
python3 runtime/executables/validate-artifacts-contract.py codespec/changes/<repo-name>/<proposal-id> --archive
```

`check-staged` 会复核映射守恒：HEAD 中每个旧源必须从暂存索引删除，旧源目录在工作区中
也必须完全消失（包括 ignored 文件），每个计划目标必须唯一存在，且 staged proposal 集合
必须与映射完全一致。正式目录随后运行 Archive 校验；draft
只运行默认 Draft 校验。全部通过后再提交。若目标已存在、多个旧目录映射到同一目标，或
仓名与当前仓不一致，迁移工具会在移动前阻断。
