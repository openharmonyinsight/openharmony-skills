---
name: ohos-ci-git-upstream-contribution
description: 在用户要求将 OpenHarmony 改动提交到上游 GitCode、创建或更新贡献 PR，或向多个目标分支提交同一修复时使用。处理 Issue 关联、签名提交、fork 推送与 PR 模板。
metadata:
  author: openharmony
  source: SkillCreateBykingqaquuu/skills/openharmony-git-workflow
  source-revision: e4061b33471a45c181778e8272396ba9d028781a
  scope: common
  stage: cicd
  domain: git
  capability: upstream-contribution
  version: 0.1.0
  status: draft
  original-author: kingqaquu
  tags:
  - git
  - gitcode
  - pr
---

# OpenHarmony 上游贡献工作流

处理 Issue → commit → fork push → upstream PR。与普通 GitCode 工具的区别是维护目标分支、对应 Issue、签名提交及仓库门禁之间的一致性。遇到多目标分支、已有 PR 更新，或需要隔离未提交改动时，先读取 [分支、索引与更新规则](references/branch-workflow.md)；工作区干净的单分支新 PR 无须加载该引用。

## 确定目标和授权范围

读取 `git status`、当前分支、remotes、目标仓库贡献规范与用户指定范围。根据 remote URL 和用户输入识别 upstream/fork/目标分支；不假定 origin 就是 fork、目标就是 master，也不使用固定账号或邮箱。多个候选目标无法确定时仅询问缺失目标，其它准备继续进行。

用户仅要求整理材料时输出可审阅草稿；要求完整提交流程时完成授权范围内的 Issue、提交、推送和 PR，不重复索取已有授权。修改全局 Git 配置、改署名、丢弃改动、强制覆盖远端历史不属于普通贡献流程的隐含授权。先检查已有 staged diff：普通 git commit 会提交整个索引，仅限制 git add 的文件不足以隔离其它暂存内容。索引含无关改动时，不在原工作区运行普通 commit；按分支引用中的迁移流程在独立 worktree 提交，保留原索引和工作文件。

## 发现模板与关联 Issue

先查目标仓库 `.github/`、`.gitee/`、`.gitcode/` 的 Issue/PR 模板及贡献说明，使用 `rg --files --hidden`，兼容大小写、语言后缀、多模板目录、Markdown 与 YAML issue forms；不要使用会漏掉三级目录的 maxdepth 限制。多个模板按任务类型和语言选择，保留必填项。没有模板时使用 [中立 PR 模板](references/pr-template.md)，Issue 草稿给出问题/需求、预期、实际行为、复现或验收标准。

用户提供 Issue 时先核对仓库、分支适用性和内容，复用正确 Issue；先查已有 Issue/PR 避免重复创建。新建时按问题性质选择工具实际支持的缺陷/任务/需求等类型，不猜测枚举。发现当前可用 GitCode MCP 或已配置 CLI/API，核对真实参数；不可用时输出草稿和缺少的能力，不能用 `gh` 代替 GitCode 工具，也不修改用户凭据。

## 提交、验证与创建 PR

1. 确认功能分支基于实际目标分支；用 merge-base 与 diff 检查没有混入无关提交。若工作区已有其它修改，先读取分支引用中的“迁移选定未提交改动”，隔离 worktree；不要自动 stash、reset 或切换覆盖。同一文件混有未授权 hunk 时只迁移确认的部分。
2. 完成本次必要检查，记录命令与真实结果；无法运行写明原因。文本改动按仓库要求验证，不套用编译器专项测试。
3. 查看将提交的 diff。使用现有 Git 身份和 `--signoff`，提交消息按仓库规范；未规定时标题建议不超过 50 字符。提交正文 `Issue: <本分支 Issue URL>`，Signed-off-by 必须由真实身份生成，不能虚构。
4. 如仓库要求一 PR 一提交，遵守该门禁；其它仓库按自身策略，不强制改写已有多人历史。更新提交前必须读取分支引用的“更新已有 PR”，核对 PR 作者、待改写提交及授权。
5. 推送到确认的 fork 分支，创建 PR 到 upstream 的实际 base；head 使用真实 fork owner/branch。非快进更新前必须读取引用中的 lease 规则。写操作重试前先读取服务状态，避免请求超时后重复创建 Issue/PR 或重复推送。
6. PR 正文链接本分支 Issue、说明最终改动、已运行检查和未验证项。模板中的测试清单按证据勾选，不能预置“全部通过”或保留别人的邮箱。
7. 创建后回读 PR 的 head/base/Issue 关联和提交范围，返回 Issue/PR URL、提交 SHA、目标分支、检查结果及未完成事项。

典型提交（仅在隔离 worktree，或已核对索引不存在无关暂存内容时使用；替换占位符并确认 diff）：

```sh
git add -- <selected-files>
git commit --signoff -m '<title>' -m 'Issue: <issue-url>'
git push -u <fork-remote> <feature-branch>
```

认证失败、身份缺失、冲突或远端发生未预期变化时，保留已有工作并报告实际状态；不修改全局配置、伪造测试结果或循环重试。没有取得 PR 元信息时不声称已创建成功。
