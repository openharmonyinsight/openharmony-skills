# oh-test-skills

HarmonyOS 测试设计相关的 Claude Code skill 集合。

---

# /oh-test-issue-bug & /oh-test-issue-req —— 按 issue 模板一键提交

两个 Claude Code 自定义命令，分别按仓库的 issue 模板向 `openharmony-ai-testdesign/oh-test-skills` 提交 issue：

| 命令 | 模板 | 用途 | 特性 |
| --- | --- | --- | --- |
| `/oh-test-issue-bug` | `bug.yml` | 报告测试设计过程中的缺陷/异常 | 含 AI **根因分析**；标题 `[BUG]`，label `bug` |
| `/oh-test-issue-req` | `requirement.yml` | 提出对测试设计能力的需求/改进建议 | Claude 辅助充实**实现方案**；标题 `[REQ]`，label `enhancement` |

**共同特性**：提交前打印标题+正文让你确认；兼容 macOS 与 Windows；自动套用模板的标题前缀、labels 和正文字段结构。

> 以**用户全局命令**方式分发：装到每人的 `~/.claude/commands/`，在任何项目里都能用。

## 1. 生成 GitCode 私人令牌

1. 登录 GitCode → 右上角头像 → **设置** → **私人令牌**（Personal Access Tokens）。
2. 新建令牌，**勾选 issues 相关权限**，生成并复制令牌（只显示一次）。

> 每人用自己的令牌——issue 会归属到你名下，权限最小、可单独撤销。**不要把令牌提交进仓库、不要发给同事。**

## 2. 配置令牌（按你的系统选一栏）

### macOS（zsh）
```sh
echo 'export GITCODE_TOKEN="你的令牌"' >> ~/.zshrc
source ~/.zshrc
```
> ⚠️ 若从 **Dock / Spotlight** 启动 Claude Code（而不是从终端启动），`.zshrc` 不会被加载。两种办法二选一：从「终端」启动 Claude Code（最简单）；或额外执行一次 `launchctl setenv GITCODE_TOKEN "你的令牌"`。

### Windows（PowerShell）
```powershell
setx GITCODE_TOKEN "你的令牌"
```
然后**重开终端和 Claude Code**（`setx` 对终端和 GUI 启动都生效，但当前窗口不立即生效）。

## 3. 安装命令到全局

在**本仓库根目录**下执行：

### macOS（软链，git pull 后自动更新）
```sh
mkdir -p ~/.claude/commands
ln -sf "$PWD/.claude/commands/oh-test-issue-bug.md" ~/.claude/commands/oh-test-issue-bug.md
ln -sf "$PWD/.claude/commands/oh-test-issue-req.md" ~/.claude/commands/oh-test-issue-req.md
```

### Windows（复制；更新仓库后需重新执行一次）
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\commands" | Out-Null
Copy-Item ".claude\commands\oh-test-issue-bug.md" "$env:USERPROFILE\.claude\commands\" -Force
Copy-Item ".claude\commands\oh-test-issue-req.md" "$env:USERPROFILE\.claude\commands\" -Force
```

## 4. 使用

```
/oh-test-issue-bug <可选：简单描述遇到的问题>
/oh-test-issue-req <可选：简单描述需求>
```
Claude 会收集信息 →（bug 命令做根因分析 / req 命令辅助方案）→ 按模板起草标题+正文 → 打印预览 → 你确认 → 提交，返回 issue 链接。

## 5. 排错

| 现象 | 原因 / 处理 |
| --- | --- |
| 提示 `未检测到 GITCODE_TOKEN` | 令牌没配好，或 Claude Code 没重启。macOS 从 Dock 启动见第 2 步的 `launchctl` 提示。 |
| HTTP 401 | 令牌无效/过期，重新生成。 |
| HTTP 403 / 404 | 无仓库权限或 owner/repo 不对，联系仓库管理员。 |
| HTTP 422 | 多为 labels 名不合规（长度需 2-20、非特殊字符）；按返回 message 修正。 |
| Windows 下 `curl` 报参数错 | 命令已自动用 `curl.exe`；如仍异常，确认 Windows 10+（自带 curl.exe）或装 Git for Windows。 |

## 6. 安全须知

- 令牌只存在你本机的环境变量里，**绝不**进仓库、不发聊天、不贴 issue 正文。
- `.claude/settings.local.json` 和 `*.token` 已在 `.gitignore` 中屏蔽。
- 命令提交前必经你确认，不会静默创建 issue。

## 7. 后续可扩展（当前未做）

- **交付件打包上传**：把需求输入文档 + 测试设计输出目录（`requirement_analysis.md`、`test_point_design.md`、`demo_design.md`、`test_cases.xlsx` 等）打包随 issue 上传。当前 GitCode 公开 API 无 issue 附件专用接口，待接口就绪再做。
