---
description: 按 requirement 模板向 GitCode 仓库 openharmony-ai-testdesign/oh-test-skills 提交对测试设计能力的需求建议。Claude 辅助起草并充实方案，提交前需用户确认。
argument-hint: [可选：需求描述]
allowed-tools: Bash, PowerShell, Read, Write
---

# /oh-test-issue-req — 按 requirement 模板提交需求建议

帮用户向 GitCode 仓库 **openharmony-ai-testdesign/oh-test-skills** 按 **requirement 模板**提交需求建议 issue。兼容 macOS（bash/zsh）与 Windows（PowerShell），平台差异由你在运行时探测适配，不要写死某一种 shell 语法。

## 目标仓库（固定）
- owner `openharmony-ai-testdesign` / repo `oh-test-skills`
- 创建 issue：`POST https://api.gitcode.com/api/v5/repos/openharmony-ai-testdesign/issues`
- 模板：`.gitcode/ISSUE_TEMPLATE/requirement.yml`（标题前缀 `[REQ] `，label `enhancement`）

## 步骤 1：探测环境并校验 token

判断 shell：macOS/Linux/Windows+Git Bash 用 Bash 工具（`$GITCODE_TOKEN`）；Windows+PowerShell 用 PowerShell 工具（`$env:GITCODE_TOKEN`）。

检查 token 是否为空（**不要打印其值**）：
- Bash：`if [ -z "$GITCODE_TOKEN" ]; then echo MISSING; else echo OK; fi`
- PowerShell：`if (-not $env:GITCODE_TOKEN) { "MISSISS" } else { "OK" }`

若 **MISSING**，停止并给出配置指引：macOS 在 `~/.zshrc` 加 `export GITCODE_TOKEN="..."`（从终端启动 CC，或额外 `launchctl setenv`）；Windows 执行 `setx GITCODE_TOKEN "..."` 后重开。令牌在 GitCode → 个人设置 → 私人令牌生成（勾选 issues 权限）。

## 步骤 2：收集需求描述

- 若 `$ARGUMENTS` 非空，作为需求描述线索；否则**主动问用户**希望新增/改进什么能力、解决什么痛点，拿到清晰描述再继续。

## 步骤 3：辅助完善字段

- 基于上下文帮用户充实「需求背景 / 需求描述 / 实现方案」；**方案部分标注「AI 建议」**，不确定的不编造、标明待评估。
- 「需求名称」给一句话概括；「需求优先级」你先按价值/紧迫建议一个（高/中/低），预览时让用户确认。

## 步骤 4：按 requirement 模板渲染正文

先尝试 Read 当前目录及上级的 `.gitcode/ISSUE_TEMPLATE/requirement.yml` 取最新字段结构；读不到就用下面内置结构（二者一致）。渲染 Markdown 正文：

```
## 感谢您提出需求！
请清晰描述需求背景与期望方案，以便团队评估价值和可行性。
----

### 需求名称

<一句话概括>

### 需求背景

<为什么要做、解决什么业务问题或痛点>

### 需求描述

<期望的功能、交互方式、业务规则>

### 需求优先级

<高/中/低 之一；你先建议，预览时让用户确认>

### 实现方案（大致）

<你基于上下文给的方案建议；标注「AI 建议」>

### 备选方案

<可选；没有可写"暂无">

### 验收标准

<可选；可给验收要点清单>

### 确认事项

- [x] 我已搜索现有 Issue，确认该需求未被重复提出。
```

- **title**：`[REQ] ` + 需求名称
- **labels**：`enhancement`
- **assignee（默认分配人）**：`zhangrao`——预览时告知用户；用户若指定其他 username 则用那个覆盖。
- 本命令**不做根因分析**（需求场景不适用）。

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
     -F "labels=enhancement" \
     -F "assignee=zhangrao" \
     "https://api.gitcode.com/api/v5/repos/openharmony-ai-testdesign/issues?access_token=$GITCODE_TOKEN"
   ```

   **PowerShell 版（用 curl.exe，勿用 curl 别名）：**
   ```text
   curl.exe -sS -o "$env:TEMP\issue_resp.json" -w "%{http_code}" -X POST `
     -F "repo=oh-test-skills" `
     -F "title=<$env:TEMP\issue_title.md" `
     -F "body=<$env:TEMP\issue_body.md" `
     -F "labels=enhancement" `
     -F "assignee=zhangrao" `
     "https://api.gitcode.com/api/v5/repos/openharmony-ai-testdesign/issues?access_token=$env:GITCODE_TOKEN"
   ```

3. 读响应，提取 `html_url` 和 `number` 反馈给用户。
4. 错误处理：401→token 过期；403/404→权限或 owner/repo 不对；422→按 `message` 修正（labels 名要求长度 2-20、非特殊字符；或 assignee 不是本仓成员/username 不存在）。

## 约束（务必遵守）

- **绝不**打印/echo/写日志 `$GITCODE_TOKEN` 的值，也不写进 issue 正文/临时文件。
- 必须**用户确认后才 POST**。
- **必须按 requirement 模板生成**：标题前缀 `[REQ] `、labels `enhancement`、正文字段结构与步骤 4 一致。
- 方案/优先级等 AI 给出的内容标注「AI 建议」，不编造。
- 正文用 Markdown；提交成功后把 `html_url` 给用户。
