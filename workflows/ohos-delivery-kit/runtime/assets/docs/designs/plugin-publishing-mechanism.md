# 插件与 Skill 发布机制设计（claude / codex / opencode → ohos-marketplace）

> 状态：**as-built + 已验证**（Phase 1 ODK 仓 + Phase 2 marketplace 仓已实现；Phase 3 真实加载 / 三端 e2e / marketplace 闭环已实测通过，详见 §8）。Route A 定型；三端版本 `0.6.5`。
> 日期：2026-07-11
> 关联：`docs/designs/source-boundary-and-distribution.md`（core→dist 边界）、`docs/designs/plugin-update-notice-and-refresh.md`（更新通知）、`HANDOFF.md` P2（marketplace/release-repo 决策记录）
> 参考：superpowers 6.1.1（`obra/superpowers`，实证 `.opencode/plugins/superpowers.js`）、OpenSpec 官方（`Fission-AI/OpenSpec`）、`agent-tools-research` 调研

## 0. 关键决策与设计约束

OpenCode 端从 markdown-skill 模型迁移到原生 JS 插件过程中，以下决策非常规或易被误读，单列于此；实现细节见 §4。

| 决策 | 选择 | 理由 / 约束 |
|---|---|---|
| 加载方式 | **裸 `.js` 自动加载为主**（无需 `plugin[]`）；`--add-config` 包模式仅 fallback | `plugin[]` 虽可指目录包（superpowers `INSTALL.md` 实证 `plugin:["~/.config/opencode/node_modules/superpowers"]`），但"相对路径指目录包"未经验证；裸文件自动加载最稳。 |
| 导出形式 | 命名导出 `OhosDeliveryKitPlugin`（非 default） | 对齐 superpowers `superpowers.js`；OpenCode 加载命名导出。 |
| 路径解析 | skill 体 `{{PLUGIN_ROOT}}` → `__ODK_PLUGIN_ROOT__`（build 占位符），**install 期替换**为绝对资产根 | 确定性，不依赖 agent NLP 解析裸 token；对齐现有 `ODK_ROOT` 重写模式。 |
| commands 去留 | **保留**为薄包装（委托对应 skill），不退役 | 维持 ODK 历史的 `/odk-*` 命令入口；规则源收敛到 skills，commands 不承载逻辑。文件名直接用 skill 名（skill 已含 `odk-` 前缀，不双拼）。 |
| hook 降级 | 始终返回 `config` + `messages.transform` 两 hook；transform 内部全 guard | OpenCode 不支持 `experimental.*` 时忽略该 hook，skills 仍可用（非不可用）；`engines.opencode` 仅元数据，Bun 不强制。 |
| uninstall 安全 | manifest 驱动精确删 + opencode owned-prefixes 白名单 + relpath 校验 | 禁止 `../` 越权；`--add-config` 写的 `plugin` entry 结构化删除，不动用户其它配置，不删容器目录。 |
| `--add-config` 目标 | `plugin[]` 不得指向纯资产目录 | 纯资产目录（无 `package.json/main`）非合法 plugin entry。 |
| copy vs npm | **本质差异**：copy=install 期替换路径；npm=需 runtime 注入（install 脚本不跑） | npm 通道非零代码；启用前必补 runtime path-injection 验证（见 §7）。 |
| 版本单一来源 | `packaging/claude/.claude-plugin/plugin.json` | distribute 读取并传播三端；codex manifest 手工同步、opencode dist 注入，`validate-plugin-versions.sh` 拦截 drift。 |
| 实测要点 | auto-load **无需**邻近 `package.json`；transform 注入是模型**输入**侧，不出现在 `opencode run` stdout | 故加载验证用 hook 内文件 trace（执行序 `MODULE_LOADED → FACTORY_CALLED → HOOK_config → HOOK_transform_INJECTED`），而非 grep stdout。 |
| Claude 持久化安装 | `install-claude.sh` 注册本地 marketplace（`dist/claude-marketplace`）+ `plugin install`；会话级 `--plugin-dir` 保留 | Claude 无"从本地目录直接持久安装"命令，持久化必经 marketplace；本地 marketplace（名 `ohos-delivery-kit-local`）使开发仓三端自足。`--plugin-dir` 仍供活跃开发 live-reload（每次读 live dist，改源即生效，无需 `plugin update` 刷缓存）。 |

## 1. 背景与目标

**问题**
- `ohos-marketplace` 发布仓已完整支持 **Claude / Codex** 两端安装 ODK 插件（marketplace manifest + committed 产物 + `sync-plugins.sh`），但 **OpenCode 完全缺失**：无 `opencode-plugins/`、无 `sync-plugins.sh` 的 opencode 列、README 无 OpenCode 安装段。
- ODK 开发仓当前的 OpenCode 形态是**特例化的松散结构**：`opencode.md`（上下文注入）+ 平铺 `.opencode/commands/*.md`（无 frontmatter）。它没有 plugin manifest、没有 hook、没有自动 bootstrap、没有 owned-files 卸载，与 Claude/Codex 严重不对称。
- `HANDOFF.md` P2 锁定的"superpowers 式 release 仓 + 发版管线"对 OpenCode 一直未落地。
- 调研证实 OpenCode 1.17+ **有** hook 系统与按需 skill 加载——`packaging/opencode/opencode.md:117` 那条"OpenCode 无 hook / 无 on-demand skill loading"的声明已过时。

**目标**：三仓协同，使 `ohos-marketplace` 发布仓**完整支持 Claude / Codex / OpenCode 三类 codeagent 安装并运行 ODK 插件**，且 OpenCode 端与另两端 bootstrap 行为对称。

**决策（Route A）**：OpenCode 形态升级为**原生 JS 插件**（superpowers 式）——命名导出的 JS 入口，用 `config` hook 注册 skills 路径 + `experimental.chat.messages.transform` 注入 `using-odk` bootstrap。本地分发走 copy（裸 .js 自动加载 + 幂等 refresh 脚本），npm 作为未来无损增强（结构预留，按 YAGNI 现在不发）。

## 2. 范围

**本次包含（IN）**
- ODK 开发仓：OpenCode 形态重构为 JS 插件；`distribute-skills.sh` 升级；新增对称的 install / uninstall / 幂等 refresh。
- `ohos-marketplace`：`sync-plugins.sh` 加 OpenCode 列；提交 `opencode-plugins/ohos-delivery-kit/`；新增用户级 `install-opencode.sh`；README 加安装段 + 迁移说明。
- 三平台端到端验证（含真实 OpenCode 加载测试）。

**本次不包含（OUT）**
- `spec-for-ai` / `ohos-sdd` 重构（单独处理；marketplace 机制保持通用，后续可平滑接入）。
- `npm publish` 实际发布（作为 documented future enhancement，结构与发版脚本预留接口）。
- `agent-tools-research` 仓更新（已沉淀完成并推送，不在实现链路）。
- 其它 codeagent（Cursor / Kimi 等）。

## 3. 现状基线（关键代码事实）

> 注：本节为**实现前**的基线快照（opencode.md 模型、2 列 marketplace 注册表），用于说明本设计要解决的问题。as-built 状态见 §4（目标架构，已落地）。

**ODK 开发仓**（`core/` 源 → `scripts/distribute-skills.sh` → `dist/{claude,codex,opencode}/`，dist 被 gitignore）
- 版本单一来源：`packaging/claude/.claude-plugin/plugin.json` 的 `version`（`distribute-skills.sh:23`），三端共用。
- Claude/Codex：`write_platform_skill`（`:70-89`）发**带 frontmatter 的 SKILL.md**，`{{PLUGIN_ROOT}}`→`${CLAUDE_PLUGIN_ROOT}`/`${CODEX_PLUGIN_ROOT}`，`{{CMD_PREFIX}}`→`/odk-`/`odk-`。
- OpenCode：`write_opencode_command`（`:91-105`）发**无 frontmatter 的 command 文件**，`{{PLUGIN_ROOT}}`→"the ohos-delivery-kit repo's"，并把模板路径重写回 `core/templates/`（即产物**回指开发仓**，不自包含）；`using-odk*` 被 skip（`:176-180`）。
- 共享资源（templates/profiles/contracts/adapters）只拷进 claude/codex（`:187-191`），**不进 opencode**。
- `opencode.md`（`:197-213`）与 `core/skills/using-odk-bridge/SKILL.md` 之间用 `<!-- SYNC: -->` 标记做手工漂移检查。
- `scripts/install-opencode.sh`：拷 `opencode.md`→目标根（重写 `ODK_ROOT`→开发仓路径）、`commands/*`→`.opencode/commands/`；**无 package.json、无 manifest、无卸载、非幂等**。
- `opencode.md:117`：过时的"OpenCode 无 hook"声明。

**ohos-marketplace 发布仓**
- Claude（`.claude-plugin/marketplace.json` + `plugins/<name>/`）与 Codex（`.agents/plugins/marketplace.json` + `codex-plugins/<name>/`）**完整**。
- `sync-plugins.sh`：注册表为 2 列（`claude-dist-rel | codex-dist-rel`，`:34-37`），`sync_plugin` 只拷 `plugins/` 与 `codex-plugins/`（`:68-78`）；版本同步 python 块只更新 Claude manifest（`:93-114`）。无用户级安装脚本。

**superpowers 6.1.1（参考模型，已核实）**
- `.opencode/plugins/superpowers.js`：**命名导出** `SuperpowersPlugin = async ({ client, directory }) => {...}`（`:55`）。
- 资产解析用 `import.meta.url` 算 `__dirname`（`:13`），`path.resolve(__dirname, '../../skills')`（`:57`）定位 skills——**不靠 `directory` 入参**。
- `config` hook 把 skills 路径推入 `config.skills.paths`（`:107-113`）；`experimental.chat.messages.transform` 注入 `using-superpowers/SKILL.md` bootstrap（幂等守卫、模块级缓存，`:124-137`）。
- 分发：`plugin:["superpowers@git+https://..."]`（git-backed 包）；Windows 降级 `plugin:["~/.config/opencode/node_modules/superpowers"]`（plugin[] 指目录包）。

## 4. 目标架构

### 4.1 设计纪律（决定可无损扩展到 npm）

| 纪律 | 含义 | 落实点 |
|---|---|---|
| 自包含单插件包 | 产物自带全部运行时资源（skills / commands / templates / profiles / contracts / adapters），不回指开发仓 | `dist/opencode/.opencode/ohos-delivery-kit/` 含全部资产 |
| 运行时相对路径解析 | JS 用 `import.meta.url` 算 `__dirname` 定位兄弟资产（对齐 superpowers，不依赖 `directory` 入参） | `ohos-delivery-kit.js`：`path.resolve(__dirname, '../ohos-delivery-kit/skills')` |
| 路径确定性（copy 通道） | skill 体里 `{{PLUGIN_ROOT}}`→`__ODK_PLUGIN_ROOT__`（build 占位符），install 期替换为绝对资产根 | `distribute-skills.sh` 替换 + `install-opencode.sh` 二次替换 |
| 来源无关 hook | hook 逻辑不依赖"被 copy 还是 npm 装"，只用 `import.meta.url` | `ohos-delivery-kit.js` 不含安装位置判断 |
| hook 全 guard + 未知 hook 降级 | 插件始终返回 `config` 与 `experimental.chat.messages.transform` 两个 hook；transform 内部全程 guard（不假设 `output.messages`/`message.info`/`parts` 存在）；OpenCode 不支持 `experimental.*` 时忽略该 hook，skills 仍经 `config` hook 加载 | `ohos-delivery-kit.js` guard 模式（对齐 superpowers `:124-137`）；`engines.opencode` 仅元数据 |
| 零依赖 | 插件只做文件/路径/字符串操作，无 npm 依赖 | `ohos-delivery-kit.js` 仅用 `node:fs`/`node:path`/`node:url` |

> 守这 6 条，copy 通道可先闭环；npm 通道保留结构基础，但启用前仍需补 runtime path-injection 与验证（见 §7）。

### 4.2 核心收敛：opencode skills 对齐 claude/codex + 保留薄 commands

Route A 的关键收敛：opencode **skills 升级为带 frontmatter 的 SKILL.md**（与 claude/codex 同构），由 `config` hook 注册给原生 skill 工具；`using-odk*` 不再 skip（bootstrap 需读 `using-odk/SKILL.md`）。

与初稿的差异：**不退役 commands**，改为薄包装——每个 `.opencode/commands/odk-*.md` 只做"要求 agent 用 skill 工具加载对应 `odk-*` skill"。规则源收敛到 skills，commands 仅作显式 `/odk-*` 入口（带 frontmatter，不再无 frontmatter）。这样既保留 ODK 历史的命令驱动 UX，又不让 commands 承载规则逻辑。

### 4.3 ODK 开发仓改动

#### 4.3.1 新增 `packaging/opencode/` 源
```
packaging/opencode/
├── package.json          # 新增：name/version(type:module)/main/files/description/license/engines.opencode(仅元数据)
├── plugins/
│   └── ohos-delivery-kit.js            # 新增：命名导出 OhosDeliveryKitPlugin（源）
└── README.md             # 更新：OpenCode 安装/运行说明
```
- `opencode.md` **退役**（其内容由 JS bootstrap 读 `using-odk/SKILL.md` 注入取代），随之删除 `distribute-skills.sh:197-213` 的 SYNC 漂移检查，并消除 `opencode.md:117` 的过时声明。
- `package.json` 的 `version` 在生成时由 `distribute-skills.sh` 从 Claude manifest 注入（保持单一来源）；`main` 指向 `.opencode/plugins/ohos-delivery-kit.js`。

#### 4.3.2 `ohos-delivery-kit.js` 契约（命名导出 + import.meta.url + 能力降级）
```js
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ASSET_ROOT = path.resolve(__dirname, '../ohos-delivery-kit');   // 运行时相对解析
const SKILLS_DIR = path.resolve(ASSET_ROOT, 'skills');
let _bootstrapCache;                                                    // 模块级缓存

export const OhosDeliveryKitPlugin = async ({ directory } = {}) => {
  return {
    config: async (config) => {                                         // 注册 skills 给原生 skill 工具
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(SKILLS_DIR)) config.skills.paths.push(SKILLS_DIR);
    },
    'experimental.chat.messages.transform': async (_input, output) => { // 注入 using-odk bootstrap（幂等）
      const bootstrap = getBootstrap();                                 // 读 ASSET_ROOT/skills/using-odk/SKILL.md，strip frontmatter
      if (!bootstrap || !output.messages?.length) return;
      const firstUser = output.messages.find(m => m.info?.role === 'user');
      if (!firstUser?.parts?.length) return;
      if (firstUser.parts.some(p => p.type === 'text' && p.text.includes('EXTREMELY_IMPORTANT'))) return;
      firstUser.parts.unshift({ type: 'text', text: bootstrap });
    },
  };
};
```
- 资产解析一律用 `import.meta.url`（不依赖 `directory` 入参是否被正确传递）。
- **hook 降级（非运行时查询）**：插件始终同时返回 `config` 与 `experimental.chat.messages.transform`；transform 内部全程 guard（`if (!output.messages?.length) return`、`if (!firstUser?.parts?.length) return`，对齐 superpowers `:124-137`）。OpenCode 若不支持 `experimental.*`，忽略该 hook——skills 仍经 `config` hook 加载，仅无自动 bootstrap。`engines.opencode` 仅作文档元数据（Bun 不强制解释自定义 engines 字段）。插件日志只记 debug/info，不污染用户对话。
- 选择性：注入 `using-odk/SKILL.md` 全文（已含激活/去激活规则——仅 `.codespec/` 或显式提 ODK 时激活，不接管普通编码）。
- 零依赖：仅 `node:fs`/`node:path`/`node:url`。

#### 4.3.3 `dist/opencode/` 目标结构（copy 与 npm 目录布局同形，路径注入策略不同）

关键设计：dist 直接用 `.opencode/` 根布局，**本地 copy 即把 `.opencode/` 子树并入目标项目**，npm 则以 `package.json` 为入口——**目录布局同形，无需 install 期结构转换；但 npm 通道不是即刻可用，仍需按 §7 补 runtime path-injection**。
```
dist/opencode/
├── package.json                          # npm 入口：main → .opencode/plugins/ohos-delivery-kit.js
├── .opencode/
│   ├── plugins/
│   │   └── ohos-delivery-kit.js          # 裸 .js 自动加载（本地无需 plugin[]）
│   ├── ohos-delivery-kit/                # 资产根 = __ODK_PLUGIN_ROOT__
│   │   ├── skills/<skill>/SKILL.md       # 带 frontmatter；{{PLUGIN_ROOT}}→__ODK_PLUGIN_ROOT__
│   │   │   └── using-odk/SKILL.md        # bootstrap 源（JS 运行时读取）
│   │   ├── templates/ profiles/ contracts/ adapters/
│   └── commands/
│       └── odk-*.md                      # 薄包装，带 frontmatter
└── README.md
```
JS 的 `__dirname`=`.opencode/plugins/`，`ASSET_ROOT`=`.opencode/ohos-delivery-kit/`——本地 copy 与 npm（`node_modules/<pkg>/`）下相对路径一致。

#### 4.3.4 `distribute-skills.sh` 改动点
- `write_opencode_command` → 拆为两个：
  - `write_opencode_skill`：复用 `write_skill_frontmatter`，输出 `dist/opencode/.opencode/ohos-delivery-kit/skills/<skill>/SKILL.md`；`{{PLUGIN_ROOT}}`→`__ODK_PLUGIN_ROOT__`，`{{CMD_PREFIX}}`→`odk-`。对所有 skill 调用（含 `using-odk*`）。
  - `write_opencode_command`（薄包装版）：仅对 `odk-*` skill 生成（`using-odk*` 路由 skill 不生成 command——它们经 config hook 自动加载 + bootstrap 注入）；输出 `dist/opencode/.opencode/commands/<skill>.md`，文件名直接用 skill 名（skill 目录已含 `odk-` 前缀，**不得再拼 `odk-`**，避免 `odk-odk-init.md`）；带 frontmatter（`description`/`agent: build`），正文仅"用 skill 工具加载 `<skill>` 并遵循之"。
- 共享资源循环（`:187-191`）：加 `opencode`，拷 templates/profiles/contracts/adapters 进 `dist/opencode/.opencode/ohos-delivery-kit/`。
- `prepare_dist`（`:149-150`）：拷 `packaging/opencode/{package.json, plugins/ohos-delivery-kit.js, README.md}` 到对应位置（`package.json`→dist 根；`ohos-delivery-kit.js`→`.opencode/plugins/`，同名拷贝）；移除 `opencode.md` 拷贝。
- 移除 `:197-213` 的 opencode.md SYNC 漂移检查。
- 新增 opencode 产物结构校验：`package.json` 合法、`main` 文件存在、skills 有 frontmatter、commands 有 frontmatter、无 `{{PLUGIN_ROOT}}`/`{{CMD_PREFIX}}` 残留、`__ODK_PLUGIN_ROOT__` 占位符存在（待 install 期替换）。
- 纠正/移除 `opencode.md` 的"无 hook"过时声明（随文件退役自动消除）。
- 新增 `dist/claude-marketplace/`（本地 Claude marketplace，供 `install-claude.sh` 持久化安装）：拷 `dist/claude`→`plugins/ohos-delivery-kit/` + 写 `.claude-plugin/marketplace.json`（name `ohos-delivery-kit-local`、version = `PLUGIN_VERSION`、source `./plugins/ohos-delivery-kit`），布局同构 ohos-marketplace；`command -v claude` 块追加 `claude plugin validate dist/claude-marketplace`。

#### 4.3.5 install / uninstall / refresh（对齐 codex 成熟模型 + opencode 专属白名单）

**`scripts/install-opencode.sh` v2**（开发仓版，从 `dist/opencode` 安装到目标项目）：
- 目标形态：把 `dist/opencode/.opencode/` 子树并入 `<target>/.opencode/`：
  - `plugins/ohos-delivery-kit.js` → `<target>/.opencode/plugins/`
  - `ohos-delivery-kit/` → `<target>/.opencode/ohos-delivery-kit/`
  - `commands/odk-*.md` → `<target>/.opencode/commands/`
- **install 期路径替换**：把所有 `SKILL.md` 中的 `__ODK_PLUGIN_ROOT__` 替换为绝对资产根 `<target>/.opencode/ohos-delivery-kit`（确定性，对齐现有 `ODK_ROOT` 重写模式）。
- **裸 .js 自动加载**：不写 `plugin[]`，OpenCode 启动时自动加载 `.opencode/plugins/ohos-delivery-kit.js`。
- `--global`：安装到 `~/.config/opencode/` 同构布局。
- `--add-config`（可选 fallback，仅 package mode）：若裸文件自动加载在某 OpenCode 版本不工作，改走包模式——`plugin[]` 指向 dist package root、npm pack tarball 安装结果、或经验证可加载的 JS 文件；**不得指向纯资产目录**（`.opencode/ohos-delivery-kit/` 无 `package.json/main`，不是合法 plugin entry）。写入时把 entry 记录进 owned-files manifest，uninstall 只删该 entry，不覆盖用户其它 plugin 配置。
- **幂等 refresh**：重装前若存在旧 manifest，先调 `uninstall-opencode.sh --quiet` 清旧（对齐 codex `85023ca` 的"重装清旧 manifest"）。
- 写 owned-files manifest（枚举每个拷贝文件 + 结构化 config 变更）。
- 复用 `scripts/lib/odk_dist.sh` 的 freshness 检测（install 前自动 refresh stale dist）。
- **冲突处理**：(a) 目标已有 `.opencode/plugins/ohos-delivery-kit.js` 但无 ODK manifest → 拒绝覆盖，提示手动处理；(b) 目标 `opencode.json plugin[]` 已含 `ohos-delivery-kit` 的 npm/git/package entry → 默认 warning 并拒绝 local copy，除非 `--force-local`；(c) 旧版 `opencode.md` / `.opencode/commands/odk-*.md` 存在但无 manifest → 提示迁移，不静默删除。

**`scripts/uninstall-opencode.sh`（新增）**：
- manifest 驱动精确删 + **opencode owned-prefixes 白名单**（对齐 `uninstall-codex.sh:67-96` 的 relpath 安全）：
  ```
  .opencode/plugins/ohos-delivery-kit.js
  .opencode/ohos-delivery-kit/**
  .opencode/commands/odk-*.md
  ```
- `opencode.json`：只允许结构化删除自己写入的 `plugin` entry（按 manifest 记录），**不按文件删除**，**不删容器目录**（`.opencode/plugins/`、`.opencode/` 等）。
- 无 manifest 则拒绝并给出指引（不猜删）。

**`scripts/install-claude.sh` + `uninstall-claude.sh`（新增，Claude 持久化安装）**：
- 与 codex/opencode 不同：Claude 插件装在**用户级**（`~/.claude`）且**必经 marketplace**，故 `install-claude.sh` 依赖 `claude` CLI、不接 target 参数。
- `install-claude.sh`：`ensure` dist fresh → `claude plugin marketplace add dist/claude-marketplace` → `claude plugin install ohos-delivery-kit@ohos-delivery-kit-local`。幂等（add 已注册则刷新、install 已装则 no-op）。Claude **按版本缓存**——同版本内容变更 install 为 no-op,需 `--force`（uninstall+install）或 bump 版本后 `plugin update`。
- `uninstall-claude.sh`：`claude plugin uninstall` + `claude plugin marketplace remove ohos-delivery-kit-local`，未安装则优雅提示。
- 实测（e2e）：local **非 git 路径** marketplace add 可用；fresh 安装 / 重跑（幂等）/ 卸载三态全过。
- `--plugin-dir dist/claude`（会话级、live-reload）保留，供活跃开发——每次读 live dist，改源→重 distribute 即生效，无需 `plugin update`。

### 4.4 ohos-marketplace 改动
- `sync-plugins.sh`：注册表（`:34-37`）每行加 `opencode-dist-rel` 列；`sync_plugin` 加一段：校验 dist 存在 → `rm -rf opencode-plugins/<name>` → `cp -R dist/opencode opencode-plugins/<name>`。
- **新增用户级 `scripts/install-opencode.sh`**：从 `opencode-plugins/ohos-delivery-kit/` 安装到用户项目（逻辑同 §4.3.5，源改为发布仓的 committed 产物）。用户不必 clone 开发仓。
- 新增 committed 产物 `opencode-plugins/ohos-delivery-kit/`。
- README 新增 **"Install (OpenCode)"** 段（clone 发布仓 → `./scripts/install-opencode.sh`）+ **"从旧版 OpenCode 安装迁移"** 段（删项目根 `opencode.md`、删旧 `.opencode/commands/odk-*.md`、装新插件）。
- **版本 drift 检查提为必需**：`sync-plugins.sh` 的 python 块扩展，检查 `plugins/<name>/.claude-plugin/plugin.json`、`codex-plugins/<name>/.codex-plugin/plugin.json`、`opencode-plugins/<name>/package.json` 三端 version + Claude marketplace entry version 一致；不一致则报错阻断。

### 4.5 agent-tools-research（已完成）
调研沉淀已在独立提交完成并推送（`docs/platforms/opencode-superpowers-marketplace-research.md` §12 + `docs/case-studies/odk-three-repo-publishing.md`），不在本次实现链路。

## 5. 三仓协同

```
┌─────────────────────────── ODK 开发仓（源 + 生成器）──────────────────────────┐
│  core/ (skills/templates/profiles/contracts/adapters)  ← 唯一源                │
│  packaging/{claude,codex,opencode}/  ← 平台壳（含 opencode 的 package.json     │
│                                         + plugins/ohos-delivery-kit.js 源）                   │
│         │ scripts/distribute-skills.sh                                         │
│         ▼                                                                       │
│  dist/{claude,codex,opencode}/  ← 生成产物（gitignored）                       │
└──────────────────────────────────┬──────────────────────────────────────────────┘
                                   │ scripts/sync-plugins.sh [--rebuild]
                                   ▼
┌─────────────────────────── ohos-marketplace（发布仓 / release vehicle）────────┐
│  .claude-plugin/marketplace.json   .agents/plugins/marketplace.json            │
│  plugins/<name>/   codex-plugins/<name>/   opencode-plugins/<name>/  ←commit   │
│  scripts/install-opencode.sh  ← 用户级安装入口                                  │
└──────────────────────────────────┬──────────────────────────────────────────────┘
                                   │ 用户安装
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
   claude plugin install      codex plugin add        install-opencode.sh
   @ohos-marketplace          @ohos-marketplace       (裸 .js 自动加载，无 plugin[])
        │                          │                          │
        ▼                          ▼                          ▼
   SessionStart hook          SessionStart hook       JS: config +
   (hooks/session-start)      (hooks/session-start)   messages.transform
```

| 仓 | 职责 | 不做 |
|---|---|---|
| ODK 开发仓 | 源、生成器、平台壳、install/uninstall 脚本 | 不 commit dist；不发 npm |
| ohos-marketplace | committed 产物、registry manifest、sync 脚本、**用户级 install 脚本**、安装文档 | 不拥有/不修改源；不重新生成产物 |
| agent-tools-research | 调研沉淀、决策记录、case study（已完成） | 不含可执行产物 |

**`--rebuild` 措辞统一**：marketplace 不拥有源、不修改源；`--rebuild` 仅调用 sibling dev repo 的构建脚本并拷产物。正式 release 建议默认用已构建 dist，CI 可用 `--rebuild`。

**版本与发版节奏**：开发仓改源 → bump `packaging/claude/.claude-plugin/plugin.json` version → `distribute-skills.sh`（version 自动传播三端）→ marketplace `sync-plugins.sh --rebuild`（拷产物 + 必需的三端版本 drift 检查 + 同步 manifest version）→ review/commit/tag。

**三端安装路径对照**（用户可选；两条路径产物同构，区别在"产物从哪来 / 装到哪 / 怎么触发 bootstrap"）

| 平台 | marketplace 仓安装（测试/过渡分发，正式发布仓与路径待定） | 开发仓本地安装（开发 / 当前版本） | 作用域 / 持久性 |
|---|---|---|---|
| Claude | `claude plugin marketplace add <ohos-marketplace-url>` → `claude plugin install ohos-delivery-kit@ohos-marketplace` | `bash scripts/install-claude.sh`（本地 marketplace `dist/claude-marketplace`）；或会话级 `claude --plugin-dir dist/claude`（live-reload） | 用户级（`~/.claude`），持久；`--plugin-dir` 为会话级 |
| Codex | `codex plugin marketplace add <url>` → `codex plugin add ohos-delivery-kit@ohos-marketplace` | `bash scripts/install-codex.sh <target>`（manual copy） | 项目级（`.codex/`），持久 |
| OpenCode | clone `ohos-marketplace` → `./scripts/install-opencode.sh <target>` | `bash scripts/install-opencode.sh <target>`（从本地 `dist/opencode`） | 项目级（`.opencode/`，裸 `.js` 自动加载），持久 |

- **marketplace 仓**：产物已构建并 commit，无需 clone 开发仓、无需生成 `dist/`；版本固定在 sync 时（可能滞后开发仓）。适合正式/对外安装。
- **开发仓本地**：装**当前工作树**的 `dist/`（需 clone + `distribute-skills.sh`）；适合开发、拿最新，或 marketplace 未同步时。
- 结构上三端 bootstrap 对称（Claude/Codex SessionStart hook、OpenCode `config` + `messages.transform`，见 §6）；两条路径只是"同一份插件产物的两个来源"。

## 6. OpenCode 安装与运行时

**安装**（裸 .js 自动加载，无 plugin[]）
1. clone `ohos-marketplace`（或开发仓本地 `dist/opencode`）。
2. `./scripts/install-opencode.sh <target> [--global]`：把 `.opencode/` 子树并入目标——裸 `.js` 进 `.opencode/plugins/`、资产进 `.opencode/ohos-delivery-kit/`、薄 commands 进 `.opencode/commands/`；install 期把 `__ODK_PLUGIN_ROOT__` 替换为绝对资产根；写 manifest；幂等 refresh。
3. 无需改 `opencode.json`（裸 .js 自动加载）。`--add-config` 仅作 fallback。

**运行时**
- 启动：OpenCode 自动加载 `.opencode/plugins/ohos-delivery-kit.js` → `config` hook 把 `<asset-root>/skills` 推入 `config.skills.paths` → 原生 skill 工具可发现 `odk-*` skills。
- 首条消息：`experimental.chat.messages.transform` 注入 `using-odk/SKILL.md` bootstrap（含激活/去激活规则），等价于 Claude/Codex 的 SessionStart。能力降级：hook 不可用时 skills 仍可用，仅无自动 bootstrap。
- 调用：agent 经 skill 工具按 description 触发 `odk-*` skills；用户也可 `/odk-*`（薄 command 委托对应 skill）。skill 体用 install 期替换好的绝对路径引用 `templates/profiles/contracts/adapters`。

**三端 bootstrap 对称性**
| 端 | bootstrap 注入机制 | 触发时机 | 选择性来源 |
|---|---|---|---|
| Claude | `hooks/session-start`（SessionStart） | 会话开始 | `using-odk/SKILL.md` 体 |
| Codex | `hooks/session-start`（SessionStart） | 会话开始 | `using-odk/SKILL.md` 体 |
| OpenCode | `experimental.chat.messages.transform` | 首条用户消息前 | 同上（JS 读取同一文件） |

**更新**：开发仓改源 → 重跑 `install-opencode.sh`（幂等 refresh，清旧 + 拷新 + 重替换 `__ODK_PLUGIN_ROOT__`）。
**卸载**：`uninstall-opencode.sh`（manifest 驱动、opencode owned-prefixes 白名单、结构化删 plugin entry、不删容器目录）。

## 7. npm 未来增强（预留接口，YAGNI 现在不发）

当前实现只保证 copy 通道。npm 通道为未来增强，**非零代码**——结构已预留，但启用前必须补 runtime root 注入并验证：
- `package.json` 已就绪（name/type:module/main/files）；仅需选 scope 包名 + `publishConfig`。
- dist 的 `.opencode/` 根结构对 npm 同样有效：`main`→`.opencode/plugins/ohos-delivery-kit.js`，JS 用 `import.meta.url` 解析 `node_modules/<pkg>/` 下资产。
- release 脚本预留 `--publish-npm` 开关：`cd opencode-plugins/<name> && npm publish`（CI 凭据门控）。
- `engines.opencode` 仅元数据；版本门控靠 hook guard + OpenCode 忽略未知 hook（见 §4.1 / §9），非运行时查询。
- copy 通道与 npm 通道**并存**：内网/GitCode/离线走 copy，公网走 npm。
- **npm path-injection（启用前必做）**：npm install 不跑本安装脚本，故 npm 形态的 `__ODK_PLUGIN_ROOT__` 不会被 install 期替换——需 JS 在 bootstrap 注入绝对资产根（运行时由 `import.meta.url` 算出），由 agent 据注入值解析。这是 copy 通道（install 期替换）与 npm 通道（runtime 注入）的**本质差异**，"npm 纯增量"的前提是补齐此项验证，不是零代码发布。
- 关键利好：OpenCode *安装*装不了 git 子目录，但 `npm publish` 从子目录发布无限制——npm 是多插件聚合仓更干净的远程通道。

## 8. 验证（已执行）

> ✅ **已执行**。下列各项为已运行结果，非计划。要点：OpenCode 四场景（local/copy + package + 冲突 + 降级）经 hook 内文件 trace 实测四机制全触发；三端 e2e（Claude `validate` + live `LOADED`、Codex 结构验证 + install/uninstall 测试、OpenCode `debug skill` 列出 24 skills）；marketplace sync 幂等 + drift 拦截回归 + 用户级安装。
>
> **两项已知限定**（非阻塞）：① Codex `codex exec` runtime 受 OpenAI provider `failed to refresh available models: timeout` 限制，"模型实际触发 odk-init" 未跑完整回路——结构安装已确定性验证（24 skills / hooks 合法 / manifest），本次唯一 Codex 改动（uninstall mindepth）已被 test-codex-install 9 断言覆盖。② install test 已 dist 隔离（per-run repo-relative `ODK_DIST_DIR=.odk-test-dist-{platform}-$$`，gitignored），可并行/并发无 race、不污染规范 `dist/`。

**结构/单元（开发仓）**
- `distribute-skills.sh` 产物校验：`package.json` 合法、`main` 文件存在、`skills/*/SKILL.md` 均有 frontmatter、`commands/*.md` 均有 frontmatter、无 `{{PLUGIN_ROOT}}`/`{{CMD_PREFIX}}` 残留、`__ODK_PLUGIN_ROOT__` 占位符存在、shared resources 齐全。
- `ohos-delivery-kit.js`：`node --check` 语法、命名导出存在、零依赖确认。
- `install-opencode.sh` / `uninstall-opencode.sh`：幂等性（连跑两遍无 diff）、manifest 完整性、`__ODK_PLUGIN_ROOT__` 已替换为绝对路径、relpath/owned-prefixes 安全（篡改 manifest 不可逃逸白名单、不可删容器目录）。
- **实现期已落地的自动化校验**（接入 distribute 或 standalone release-gate）：`validate-opencode-plugin.sh`（结构/frontmatter/token）、`validate-plugin-versions.sh`（三端 version drift）、`validate-claude-package.sh`（standalone，parity `validate-codex-package.sh`）、`validate-distribution.sh` 的 hook-consistency grep 守卫（catch `using-ohdk` 类拼写）。

**真实 OpenCode 加载测试**
- **local/copy 模式**：临时项目放 `.opencode/plugins/ohos-delivery-kit.js` + 资产；`opencode run --print-logs "hello" 2>&1`；**优先验证 skill discovery 与 bootstrap 行为**（用 skill 工具列出 `odk-*` skills、首条消息含 `EXTREMELY_IMPORTANT` bootstrap 标记、`/odk-init` 可用），辅以 `grep -i ohos` 日志——`ohos-delivery-kit.js` 实现时须用 OpenCode 推荐日志方式输出稳定可 grep 的标识，避免仅靠日志 grep 判断成败。
- **package 模式**：`opencode.json` 的 `plugin[]` 指本地 package 路径或 `npm pack` tarball；确认 `package.json/main` 生效。
- **冲突模式**：同时存在 local 裸 .js 与 `plugin[]` npm entry；验证是否双加载，安装器给出冲突提示。
- **降级模式**：模拟 `experimental.*` hook 不可用（低版本 OpenCode 或 mock）；确认 skills 仍可加载、bootstrap 跳过、无报错。

**端到端（三平台）**
- **Claude**：`claude plugin validate dist/claude` + `claude --plugin-dir dist/claude` 实测 SessionStart bootstrap 与 `odk-init`。
- **Codex**：`install-codex.sh` + `codex exec --ephemeral` 实测。
- **OpenCode**：见上方"真实加载测试"。

**发布仓**
- `sync-plugins.sh` 幂等（无变化时零 diff）；三端版本 drift 检查生效（故意造不一致→报错阻断）；`opencode-plugins/ohos-delivery-kit/` 结构完整、可被用户级 `install-opencode.sh` 直接消费。

## 9. 风险与对策
- **本地加载机制 —— ✅ 已验证**：spike 实测 opencode 1.17.13 裸 `.js` ESM 自动加载 + `config` + `messages.transform` 三机制均触发（文件 trace 确认）；auto-load 无需邻近 `package.json`。Fallback（`--add-config` package mode，`plugin[]` 指向 dist package root / npm tarball / 可加载 JS 文件，**不得指向纯资产目录**）保留但非必需。
- **`experimental.*` hook 跨版本不稳定**：`ohos-delivery-kit.js` 始终返回两个 hook + transform 内部全 guard；OpenCode 不支持时忽略 `experimental.*`，skills 仍可用（非不可用）；`engines.opencode` 元数据标注最低版本。
- **bootstrap 误激活接管普通编码**：注入内容沿用 `using-odk/SKILL.md` 的去激活规则。
- **路径解析可靠性**：copy 通道用 install 期替换为绝对路径（确定性，不靠 agent NLP）；验证覆盖 agent 实际 `read`/`glob` 能读到 templates/contracts/adapters。

## 10. 非目标 / 未来
- `spec-for-ai` / `ohos-sdd` 对齐到同一 OpenCode JS 插件模型（单独重构）。
- `npm publish` 实际启用（见 §7，含 npm 形态的运行时路径注入）。
- 其它 codeagent 平台支持。

## 11. 实现期关键文件清单
**ODK 开发仓**
- 新增：`packaging/opencode/package.json`、`packaging/opencode/plugins/ohos-delivery-kit.js`
- 改：`scripts/distribute-skills.sh`（opencode 产 frontmatter SKILL.md + 薄 commands + shared resources + 拷 package/plugin；退役 opencode.md 与 SYNC 检查；生成 `dist/claude-marketplace` 本地 marketplace）
- 重写：`scripts/install-opencode.sh`（裸 .js 自动加载布局 + `__ODK_PLUGIN_ROOT__` install 期替换 + manifest + 幂等 refresh + `--add-config` fallback）
- 新增：`scripts/uninstall-opencode.sh`（opencode owned-prefixes 白名单 + 结构化删 plugin entry）、`scripts/validate-opencode-plugin.sh`、`scripts/validate-plugin-versions.sh`（三端 version drift，接入 distribute）、`scripts/validate-claude-package.sh`（standalone，与 `validate-codex-package.sh` 对齐）
- 新增：`scripts/install-claude.sh` + `scripts/uninstall-claude.sh`（本地 Claude marketplace 持久化安装/卸载）、`scripts/test-claude-install.sh`（marketplace 结构测试）
- 删/退役：`packaging/opencode/opencode.md`
- 改：`packaging/opencode/README.md`

**ohos-marketplace**
- 改：`scripts/sync-plugins.sh`（注册表加列 + opencode 拷贝 + 三端版本 drift 必需检查）、`README.md`（Install (OpenCode) 段 + 迁移段）
- 新增：`scripts/install-opencode.sh`（用户级，从 `opencode-plugins/<name>/` 安装）
- 新增（生成）：`opencode-plugins/ohos-delivery-kit/`
