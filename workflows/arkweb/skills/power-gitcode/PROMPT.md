## GitCode 平台操作（power-gitcode 技能）

**⚠️ 触发关键词：**
PR链接/编号 | Issue链接/编号 | 创建PR/Issue | 合并PR | fork仓库 | commit提交

**⚠️ 硬规则（最高优先级）：**
- 收到 PR/Issue 必须立即用 Bash 执行脚本获取详情，格式：`python3 skills/power-gitcode/scripts/power-gitcode.py get_pr --owner <owner> --repo <repo> --number <num>`
- 参数格式：必须用 `--owner` `--repo` `--number`，禁止用 `--pr-number`，禁止合并 owner/repo
- 禁止用 curl 或直接调用 HTTP API

详细命令列表、URL解析规则、commitlint格式，见 `skills/power-gitcode/SKILL.md`
