---
description: 按 bug 模板向 GitCode 仓库 openharmony-ai-testdesign/oh-test-skills 提交测试设计过程中的缺陷。Claude 辅助起草 + 根因分析，提交前需用户确认。
argument-hint: [可选：问题描述]
allowed-tools: Bash, PowerShell, Read, Write
---

# /oh-test-issue-bug — 按 bug 模板提交缺陷

帮用户向 GitCode 仓库 **openharmony-ai-testdesign/oh-test-skills** 按 **bug 模板**提交缺陷 issue。兼容 macOS（bash/zsh）与 Windows（PowerShell），平台差异由你在运行时探测适配，不要写死某一种 shell 语法。

## 目标仓库（固定）
- owner `openharmony-ai-testdesign` / repo `oh-test-skills`
- 创建 issue：`POST https://api.gitcode.com/api/v5/repos/openharmony-ai-testdesign/issues`
- 模板：`.gitcode/ISSUE_TEMPLATE/bug.yml`（标题前缀 `[BUG] `，label `bug`）

## 步骤 1：探测环境并校验 token

判断 shell：macOS/Linux/Windows+Git Bash 用 Bash 工具（`$GITCODE_TOKEN`）；Windows+PowerShell 用 PowerShell 工具（`$env:GITCODE_TOKEN`）。

检查 token 是否为空（**不要打印其值**）：
- Bash：`if [ -z "$GITCODE_TOKEN" ]; then echo MISSING; else echo OK; fi`
- PowerShell：`if (-not $env:GITCODE_TOKEN) { "MISSISS" } else { "OK" }`

若 **MISSING**，停止并给出配置指引：macOS 在 `~/.zshrc` 加 `export GITCODE_TOKEN="..."`（从终端启动 CC，或额外 `launchctl setenv`）；Windows 执行 `setx GITCODE_TOKEN "..."` 后重开。令牌在 GitCode → 个人设置 → 私人令牌生成（勾选 issues 权限）。

## 步骤 2：收集问题描述

- 若 `$ARGUMENTS` 非空，作为问题描述线索；否则**主动问用户**遇到了什么问题（现象、在哪个阶段、报错），拿到清晰描述再继续。

## 步骤 3：根因分析（AI 辅助）

基于上下文（对话、报错、相关 skill 文件、测试设计各阶段产物）分析**为什么会发生**：
- 定位最可能环节：需求解析(phase1)/测试点(phase2)/用例(phase4)/导出(phase5)/Demo/门控/计时，或 skill 外原因（环境、输入文档格式、依赖、网络）。
- 给 1～3 条根因假设 + 触发条件；**推测标「推测」、有把握标「已核实」**。
- 信息不足时**如实说明**并指出还需哪些信息，不要编造。
把分析先简短复述给用户（便于纠正），随后写入正文（见步骤 4）。

## 步骤 4：按 bug 模板渲染正文

先尝试 Read 当前目录及上级的 `.gitcode/ISSUE_TEMPLATE/bug.yml` 取最新字段结构；读不到就用下面内置结构（二者一致）。渲染 Markdown 正文：

```
## 感谢您反馈 Bug！
----

### 问题级别

<P0/P1/P2/P3 之一；你先按影响建议一个，预览时让用户确认/修改>

### 问题现象

<用户描述的现象、报错、堆栈；保留关键原文>

### 上传附件

（GitCode API 暂不支持 issue 附件上传，本次未附带；如需附件请在网页端补传）

----

## 问题原因分析（AI 辅助）

<步骤 3 的根因分析；标注 推测/已核实>
```

- **title**：`[BUG] ` + 一句话标题（≤50 字）
- **labels**：`bug`
- **assignee（默认分配人）**：`LINERT`——预览时告知用户；用户若指定其他 username 则用那个覆盖。

## 步骤 5：预览并确认

把 **title 和完整正文**打印给用户预览，明确询问"确认提交吗？（确认后我才创建 issue）"。要改就改完再次预览。**未确认前不要调用 API。**

## 步骤 6：提交（跨平台，multipart 表单）

GitCode 创建 issue 用 multipart 表单（非 JSON），token 走 URL 查询参数。确认后：

1. 用 Write 工具把 title、body 写入临时文件（macOS 用 `/tmp/`，Windows 用 `$env:TEMP`）。
2. curl 发 multipart，`title`/`body` 用 `<文件路径` 读文件内容为字段值（避免转义）：

   **Bash 版（macOS / Windows+Git Bash）：**
   ```text
   curl -sS -o /tmp/issue_resp.json -w "%{http_code}" -X POST \
     -F "repo=oh-test-skills" \
     -F "title=</tmp/issue_title.md" \
     -F "body=</tmp/issue_body.md" \
     -F "labels=bug" \
     -F "assignee=LINERT" \
     "https://api.gitcode.com/api/v5/repos/openharmony-ai-testdesign/issues?access_token=$GITCODE_TOKEN"
   ```

   **PowerShell 版（用 curl.exe，勿用 curl 别名）：**
   ```text
   curl.exe -sS -o "$env:TEMP\issue_resp.json" -w "%{http_code}" -X POST `
     -F "repo=oh-test-skills" `
     -F "title=<$env:TEMP\issue_title.md" `
     -F "body=<$env:TEMP\issue_body.md" `
     -F "labels=bug" `
     -F "assignee=LINERT" `
     "https://api.gitcode.com/api/v5/repos/openharmony-ai-testdesign/issues?access_token=$env:GITCODE_TOKEN"
   ```

3. 读响应，提取 `html_url` 和 `number` 反馈给用户。
4. 错误处理：401→token 过期；403/404→权限或 owner/repo 不对；422→按 `message` 修正（labels 名要求长度 2-20、非特殊字符；或 assignee 不是本仓成员/username 不存在）。

## 约束（务必遵守）

- **绝不**打印/echo/写日志 `$GITCODE_TOKEN` 的值，也不写进 issue 正文/临时文件。
- 必须**用户确认后才 POST**。
- **必须按 bug 模板生成**：标题前缀 `[BUG] `、labels `bug`、正文字段结构与步骤 4 一致。
- 根因分析段必须标注「AI 辅助」，区分推测/已核实。
- 正文用 Markdown；提交成功后把 `html_url` 给用户。
