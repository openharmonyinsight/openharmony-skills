# Plugin Update Notice and Explicit Refresh

> Status: Planned — Phase 1 not yet implemented; only dist manifest staleness infrastructure (`odk_dist.sh`) is in place
> Scope: Claude / Codex / OpenCode 安装与后续升级体验

## Goal

在不降低安装稳定性、不引入 hook 副作用的前提下，为 ODK 增加：

- 新版本提示
- 已安装版本可见性
- 显式命令触发的升级刷新路径

目标不是“自动升级插件”，而是“让用户知道有更新，并能用稳定命令完成升级”。

## Problem

当前安装链路已经具备：

- `core -> dist/*` 生成分发
- Codex / OpenCode 缺失或 stale 时自动刷新 `dist/*`
- Claude / Codex 有 `session-start` hook，可注入轻量上下文

但仍缺 3 个能力：

1. 用户不知道自己安装的 ODK 是哪个版本 / commit
2. 用户激活插件时，不知道源码仓库是否已有更新
3. 用户没有统一的“检查并刷新安装”的显式入口

这会导致：

- 本地仓库已经升级，但业务项目仍在跑旧安装副本
- review 时难以判断问题来自模板变更还是安装未刷新
- 需要依赖口头约定让用户手工重装

## Design Constraints

1. **hook 只做提示，不做自动升级**
2. **不依赖联网**
3. **不破坏 OpenCode 的非插件安装模型**
4. **不把安装态元数据写成新的规范真相源**
5. **不增加用户激活插件时的明显卡顿**

## Recommended Approach

采用“安装元数据 + 本地比对 + 显式更新命令”的三段式方案。

### 1. 安装时写入 metadata

每次安装 / 刷新时写一份 ODK metadata，至少包含：

```yaml
plugin_name: ohos-delivery-kit
installed_at: 2026-06-07T14:10:00+08:00
installed_from_repo: /abs/path/to/ohos-delivery-kit
installed_commit: 4d74b3e
installed_version: dev-4d74b3e
dist_manifest: dist/.odk-dist-manifest
platform: codex
```

建议位置：

- Claude: 插件安装目录下的 metadata 文件
- Codex: 目标项目 `.codex/odk-install.yaml`
- OpenCode: 目标项目 `.opencode/odk-install.yaml`

这份 metadata 只描述“安装态”，不进入 `.codespec/`，也不参与 artifact validator。

### 2. SessionStart / command 读取 metadata

Claude / Codex:

- `session-start` hook 读取 metadata
- 如果 `installed_from_repo` 仍存在，读取该 repo 当前 `HEAD`
- 当 `HEAD != installed_commit` 时，在注入上下文中追加一条 update notice

OpenCode:

- 没有对称 hook
- 通过项目本地命令或 `opencode.md` 中的显式说明提供“检查更新”入口

### 3. 升级动作保持显式命令

不在 hook 中直接升级。

建议提供统一命令：

- `bash scripts/update-codex.sh <target-project>`
- `bash scripts/update-opencode.sh <target-project>`
- Claude 可提供 `bash packaging/claude/install-local.sh` 的刷新包装，或新增统一 `scripts/update-claude.sh`

最小可行版本也可以先不新增脚本，只在提示中给出现有安装命令：

- Claude: `bash scripts/distribute-skills.sh && claude plugin install dist/claude`
- Codex: `bash scripts/install-codex.sh /path/to/project`
- OpenCode: `bash scripts/install-opencode.sh /path/to/project`

## Why Not Auto-Upgrade in Hook

不推荐 hook 中自动升级，原因有 4 个：

1. hook 是会话入口，执行升级会增加启动延迟
2. 失败场景复杂：权限、CLI 不存在、repo 不在本地、目标目录被移动
3. 自动修改用户项目 / 插件缓存会让副作用边界变差
4. OpenCode 无法复用同样机制，平台体验会明显分叉

因此建议：

- hook 只提示
- 升级由用户确认后显式触发

## Platform Evaluation

### Claude

现状：

- 已有 `packaging/claude/hooks/session-start`
- 安装入口偏向 `claude plugin install dist/claude`

建议：

- 在分发阶段写入 `dist/claude` 版本信息
- 安装时把 `installed_commit` 和 `installed_from_repo` 一并落到插件 metadata
- `session-start` 比较本地 repo `HEAD`
- 如有更新，在 `additionalContext` 中加入一行轻量提示

风险：

- Claude 的插件缓存/版本目录可能导致 metadata 位置需要固定约定

### Codex

现状：

- 已有 `packaging/codex/hooks/session-start`
- `scripts/install-codex.sh` 支持 marketplace add 和 manual copy fallback

建议：

- 在 manual install 时写 `.codex/odk-install.yaml`
- 如 CLI install 走 marketplace/cache，也补一份项目侧 metadata，避免只存在于插件缓存
- `session-start` 优先读取项目侧 metadata，兼容性更高

风险：

- 如果用户只装插件、不在项目内落 metadata，hook 的版本比较信息不足

### OpenCode

现状：

- 不支持插件安装
- 使用 `opencode.md` + `.opencode/commands/*.md`

建议：

- 安装脚本写 `.opencode/odk-install.yaml`
- 不尝试 session hook
- 在 `opencode.md` 或新增 `project:odk-check-update` 命令里提供检查提示

风险：

- 用户不执行相关命令时，不会自动看到更新提示

## Alternative Options

### 方案 A：hook 自动升级

优点：

- 用户几乎无感

缺点：

- 副作用太大
- 启动变慢
- 故障处理和回滚复杂
- OpenCode 无法对齐

结论：不推荐。

### 方案 B：每次启动联网检查远端版本

优点：

- 能发现本地 repo 也未更新的情况

缺点：

- 依赖网络
- 增加启动不确定性
- 与当前本地 repo 驱动的安装模型不一致

结论：不推荐作为第一阶段。

### 方案 C：只提供手工更新命令，不做提示

优点：

- 实现最简单

缺点：

- 仍然依赖用户记忆，不解决“已过期但无感知”的问题

结论：不够。

## Proposed File Changes

第一阶段最小落地建议：

- 新增 `scripts/lib/odk_install_metadata.sh`
  - 读写安装 metadata
  - 计算 `installed_version`
  - 检测 source repo 是否比 installed commit 更新
- 修改 `scripts/install-codex.sh`
  - 安装完成后写 `.codex/odk-install.yaml`
- 修改 `scripts/install-opencode.sh`
  - 安装完成后写 `.opencode/odk-install.yaml`
- 修改 `packaging/codex/hooks/session-start`
  - 输出 update notice
- 修改 `packaging/claude/hooks/session-start`
  - 输出 update notice
- 视 Claude 安装方式补充：
  - `scripts/update-claude.sh`，或
  - `packaging/claude/README.md` 中统一刷新命令
- 文档：
  - `docs/quick-start.md`
  - `HANDOFF.md`

## User Experience

### Claude / Codex

当已安装版本落后于 ODK repo 当前版本时，hook 注入：

```text
ODK update available: installed dev-4d74b3e, source repo now at dev-ab50fb7.
Refresh with: bash scripts/install-codex.sh /path/to/project
```

如果 repo 不存在、metadata 不完整或无法比对：

- 不报错
- 只保留原有 ODK router 提示

### OpenCode

显式执行检查命令后提示：

```text
ODK update available for this project.
Installed: dev-4d74b3e
Source repo: dev-ab50fb7
Refresh with: bash scripts/install-opencode.sh /path/to/project
```

## Rollout Plan

### Phase 1

- 写 metadata helper
- Codex / OpenCode 安装脚本落 metadata
- Claude / Codex hook 增加 update notice
- 文档补刷新命令

### Phase 2

- 统一 `update-*` 显式刷新脚本
- 增加 `odk-check-update` / `odk-self-update` 之类的辅助命令

### Phase 3

- 若实际使用证明稳定，再评估是否需要远端版本感知

## Non-Goals

- 不把“已安装版本”纳入 `.codespec/` 归档件
- 不在 hook 中直接执行升级
- 不在第一阶段做联网检查
- 不追求三平台完全一致的自动升级体验

## Open Questions

1. Claude 插件安装目录中最稳妥的 metadata 落点放哪里
2. Codex CLI marketplace 安装路径与项目侧 metadata 的关系是否需要双写
3. OpenCode 是否需要新增单独的 `project:odk-check-update` 命令

## Success Criteria

- 用户能在 Claude / Codex 会话启动时感知“ODK 已过期”
- 用户能看到明确刷新命令
- 更新检测不依赖网络
- hook 失败时不影响正常激活 ODK
- 不改变当前 `.codespec/` 产物质量和 validator 结果
