# ohos-design-architecture-evidence-query

OpenHarmony 架构证据**运行时分发与 CLI 使用 skill**。核心职责是下载并安装
`knowledge.db`、`interface/sdk-js`、`interface/sdk_c` 和 `oskm-cli.pyz`，并提供 CLI
的整体功能说明；具体查询由 CLI 只读执行。skill 不包含采集器，不扫描、不编译、
不修改数据库或 SDK。

**2026-11-12 起拆成两个独立产物**：本 skill 负责运行时安装与 CLI 用法；查询引擎是
独立构建的 `oskm-cli.pyz`，并随 `knowledge.tar.gz` 一起发布。归档里不再有 2.5.6
时代内联的查询层目录与 `oskm_schema` 副本。分工与理由见源码仓
`docs/architecture/cli-skill-split.md`。

- 源码仓：`https://gitcode.com/openharmony-aiad/KnowledgeBase`（`packages/oskm`），
  发布归档由 `scripts/build_skill.py` 构建。
- 上库副本：`openharmony-skills` 的
  `skills/common/design/ohos-design-architecture-evidence-query/`
  （`metadata.scope=common`、`stage=design`、`domain=architecture`、
  `capability=evidence-query`）。

## 环境要求

- Python 3.10+（本次发布验收使用 Python 3.12）
- 不要求 Git，不要求 Bash，也没有第三方 Python 运行依赖
- 下载方式由 `OSKM_DOWNLOAD_SOURCE`（`OPENHARMONY_CI` 或 `INTERNAL_CI`）选择，
  端点由 `OSKM_DOWNLOAD_ENDPOINT` 提供
- `OPENHARMONY_CI` 的 component 固定为 `dayu600_7885_ai`；`INTERNAL_CI` 请求
  `$OSKM_DOWNLOAD_ENDPOINT/<YYYYMMDD>`
- CLI 随 `knowledge.tar.gz` 一起发布（归档里四样东西：`knowledge.db`、
  `oskm-cli.pyz`、`interface/sdk-js`、`interface/sdk_c`），`install` 一次装齐；
  没有单独的 CLI 下载端点
- CLI 按三级候选解析：`$OSKM_CLI` → 源码树 `packages/oskm/cli` →
  `<runtime-root>/oskm-cli.pyz`。源码树存在时优先使用本地 CLI；三步都不需要网络
- `install` 下载一个 `knowledge.tar.gz`，把里面的 `knowledge.db`、`oskm-cli.pyz`、
  `interface/sdk-js/`、`interface/sdk_c/` 一起装到 `<runtime-root>/`
- 在 OpenHarmony 源码根或其任意子目录执行 `install` 时会向上探测源码根，
  优先使用 `out/` 或 `artifacts/` 下的 DB、`interface/` SDK 和源码树
  `cli/dist/oskm-cli.pyz`；不在源码树内时可用 `--source-root <path>` 显式指定。
  本地候选不完整或 schema 不兼容时回退下载；
  安装执行完整 schema 校验（转发给 CLI 的 `validate-db`）、不做列迁移，不匹配的
  旧库需要重新扫描；本地运行时不按日期自动刷新，显式 `install` 才会重新复制源码产物

Windows 下把文中的 `python3` 换成 `py -3`。

## 名称与安装位置

skill 机器名、发布归档、解压根目录和安装目录叶子名统一为
`ohos-design-architecture-evidence-query`。父目录由宿主工具决定：

- Claude Code 项目级：`.claude/skills/ohos-design-architecture-evidence-query/`
- Claude Code 用户级：`~/.claude/skills/ohos-design-architecture-evidence-query/`
- Codex 用户级：`${CODEX_HOME:-$HOME/.codex}/skills/ohos-design-architecture-evidence-query/`
- 其余工具：`<tool-skill-root>/ohos-design-architecture-evidence-query/`
- 运行时数据：`~/.oskm/`（与 skill 安装目录分离）

发布归档名为 `ohos-design-architecture-evidence-query-<version>.tar.gz`，解压后只有
一个同名根目录。不要重命名叶子目录，否则会与 `SKILL.md` frontmatter 的 `name` 不一致。

## 快速开始

```bash
tar -xzf ohos-design-architecture-evidence-query-3.1.0.tar.gz
AGENT_CWD="$PWD"; SKILL_DIR="$AGENT_CWD/ohos-design-architecture-evidence-query"

# 初次使用时按需配置下载端点（也可放到 <runtime-root>/.env）
cp "$SKILL_DIR/oskm_runtime/.env.example" "$SKILL_DIR/oskm_runtime/.env"
"${EDITOR:-vi}" "$SKILL_DIR/oskm_runtime/.env"

python3.12 "$SKILL_DIR/bootstrap.py" doctor

# 初次使用：下载安装 DB + interface/sdk-js + interface/sdk_c + CLI
# OpenHarmony CI（component 固定为 dayu600_7885_ai，无需命令行传入）
python3.12 "$SKILL_DIR/bootstrap.py" install --source OPENHARMONY_CI --runtime-root ~/.oskm
# Internal platform CI（GET <endpoint>/<YYYYMMDD>）
python3.12 "$SKILL_DIR/bootstrap.py" install --source INTERNAL_CI --runtime-root ~/.oskm
# 不在源码树内但已有本地构建：加 --source-root <OH源码根>，优先本地、不联网
cd "$AGENT_CWD"   # 安装完成后回到 Agent 启动目录

python3.12 "$SKILL_DIR/bootstrap.py" cli-path  # 看它最终用了哪个 CLI

# 查询**直接调 CLI**（bootstrap 只负责装）
CLI=~/.oskm/oskm-cli.pyz; DB=~/.oskm/knowledge.db
python3.12 "$CLI" --db "$DB" arch overview
python3.12 "$CLI" --db "$DB" ask get_scan_info
python3.12 "$CLI" ask --list
```

如果 `~/.oskm/knowledge.db` 不存在，先执行 `install`，成功后再查询。
`bootstrap.py refresh` 只对带 `.oskm-runtime.json` 的托管运行时检查是否过期，
不会因为任意缺失的 `--db` 路径联网。

`bootstrap.py` 自己补 `sys.path`，**不需要设 `PYTHONPATH`**，也不需要在特定目录下运行。
本地 DB 探测从 cwd 向上找最近的 OpenHarmony 源码根；cwd 不在源码树内时传
`--source-root <path>`：

```bash
python3.12 /path/to/ohos-design-architecture-evidence-query/bootstrap.py doctor
```

查询直接调 CLI（它不下载任何数据）：

```bash
python3.12 ~/.oskm/oskm-cli.pyz --db ~/.oskm/knowledge.db ask --list
~/.oskm/oskm-cli.pyz --db ~/.oskm/knowledge.db arch overview    # shebang 直接执行，取决于 PATH 里的 python3
python3.12 ~/.oskm/oskm-cli.pyz --version                       # 版本问产物自己
```

`oskm-cli.pyz` 的 shebang 是 `#!/usr/bin/env python3`。如果系统默认 `python3`
低于 3.10（例如 macOS 自带 3.9），直接执行会失败；此时显式使用
`python3.12 ~/.oskm/oskm-cli.pyz ...`。

CLI 与 `knowledge.db` 同类：**固定文件名、不记版本、不锁摘要**。`install` 把它装到
`<runtime-root>/oskm-cli.pyz`，与 `knowledge.db` 并排；完整性靠结构校验
（shebang + 有效 zip + 必需条目 + CRC），不靠比对某一次构建的摘要。

## 包内容

```text
ohos-design-architecture-evidence-query/
  SKILL.md                 Tier 1：运行时安装 + CLI 入口与误读边界（正文 ≤175 行）
  README.md                本文件
  LICENSE                  Apache-2.0（与上库仓库其它 skill 一致）
  bootstrap.py             唯一入口：只负责安装，不执行查询
  oskm_runtime/
    bootstrap.py           命令分派、--runtime-root 摘取（**不跑查询**）
    cli_install.py         CLI 三级定位（源码树优先）、结构校验与载入
    environment.py         端点与 .env（DB/SDK 归档 + CLI 产物）
    db_download.py         HTTP、安全解压、SQLite 校验、原子替换
    install.py             安装与回滚、源码树探测（OpenHarmony 源码根）、显式刷新
    state.py               .oskm-runtime.json、廉价刷新判定（供 refresh 用）
    doctor.py              环境自检
    .env.example           配置模板（真实 .env 不发布）
  references/
    usage.md               CLI 与运行时完整用法（人读）
    tools.md               工具索引，由 `ask --list --markdown` 生成
    spec/                  Tier 2：14 模块 52 工具的字段级规格
  examples/                CLI 查询示例（运行时安装见 usage.md）
  evals/
    evals.json            8 个场景：用户请求、期望结果与断言（评估规格）
    README.md             评估怎么跑、三臂分别是什么、产物在哪
    run_evals.py          执行器：夹具 + scripted / with-skill / without-skill 三臂
    runs/                 真跑出来的逐场景转录（命令、输出、请求归因、agent 审计）
    with-skill-report.md  with-skill 最终评估报告
    without-skill-report.md without-skill 基线报告与差异分析
    skill-judge-report.md skill-judge 设计质量评分
    release-checklist.md  上库前置检查清单（逐项给证据）
```

发布包**不包含**查询引擎（`oskm_cli/`）、表定义（`oskm_schema/`）、采集器
（`oskm/`）、测试、构建脚本、维护者设计/打包文档或缓存文件。需要生成新库时，
回到 `packages/oskm` 源码环境使用扫描器。

## 规范评审记录（2026-11-17）

依据《OpenHarmony Agent Skill 实践指导书》与 `openharmony-skills` 的
《命名空间与目录放置规范》§9.2 完成本次发布改造：

- frontmatter 顶层只有 `name` / `description` / `metadata`；治理字段全部在
  `metadata` 下（`author=openharmony`、`scope=common`、`stage=design`、
  `domain=architecture`、`capability=evidence-query`、`version=3.1.0`、
  `status=trial`）。`tests/test_skill.py` 的 `GOVERNANCE` 表逐项门禁，
  改版本必须同时改测试里的 `VERSION`。
- 正文预算改成只数**正文**（≤175 行，当前 173 行）：治理元数据不是给 Agent 读的
  指令，把它算进正文预算只会逼人删判断依据。
- 实测 `skill-creator` 的 `scripts/quick_validate.py`：`Skill is valid!`；
  PyYAML 解析 frontmatter 与网站元数据 YAML 均通过。

评估改为**三臂真跑**（见 `evals/README.md`）：

| 臂 | 执行者 | 用途 |
|---|---|---|
| `scripted` | 本仓执行器按 `SKILL.md` 的命令逐条跑 | 确定性复现，判据是文件状态/sha256/请求日志/退出码 |
| `with-skill` | 隔离的 `codex exec`（临时 `HOME`/`CODEX_HOME`，装好本 skill，不含 `evals/`） | 上库要求的 with-skill 评估 |
| `without-skill` | 同上，但只给 `bootstrap.py` + `oskm_runtime/` 代码 | 基线，衡量知识增量 |

外加 `--live-smoke`：真连 `OPENHARMONY_CI` 端点装一次运行时并查询，同时校对
`references/tools.md` 与 `ask --list --markdown` 是否逐行一致。
执行器带**越界守卫**：agent 命令里出现 `/Users/**`、别的评估工作区，或
`ps`/`pgrep`/`lsof` 宿主进程探测，该场景直接判不通过（上一轮基线正是靠 `lsof`
反查到源码仓，守卫加上后已拦住并重跑）。

| 维度 | 结论 | 依据 |
|---|---|---|
| D1 知识增量 | 通过 | 运行时分发边界、CLI 三级解析、证据降级与误读判据；无通用教程与冻结业务数据 |
| D2 心智模型 | 通过 | §3 固定判断顺序，§4 按 `arch` / `ask` / `diff` / `sql` 分支选择 |
| D3 反模式质量 | 通过 | §5 七条硬约束，每条写明违反后的具体后果 |
| D4 规范符合度 | 通过 | frontmatter、七节骨架、触发式 description、条件引用、治理元数据均有门禁 |
| D5 渐进披露 | 通过 | 正文 173 行；规格、示例、评估与完整用法按问题路由，附 `Do NOT load` |
| D6 自由度校准 | 通过 | §4.5 明示为启发式，§5 明示为硬约束 |
| D7 模式合理性 | 通过 | 结构服务于"先装运行时、再定位 CLI、后选查询入口" |
| D8 实用可用性 | 通过 | 命令可直接运行；异常、退出码、安装/查询排错都有回退路径 |

准入检查无阻断项，`D1`、`D4`、`D8` 均达到发布门槛。详细评分见
`evals/skill-judge-report.md`。
