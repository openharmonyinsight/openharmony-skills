# OpenHarmony 架构证据运行时与 CLI 使用指南

本 skill 的整体功能是：下载并安装 `knowledge.db`、两套 SDK 源码和 `oskm-cli.pyz`，
然后指导调用 CLI。它不实现查询引擎；CLI 负责只读查询、diff 和受限 SQL。

> **两个命令各管一半。** skill 目录里的 `python3 bootstrap.py` 只负责**装**
> （`doctor / install / refresh / update-cli / download-db / validate-db /
> cli-path`）；查询一律**直接调 CLI**：
> `python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db …`。
> 本发布包**不含查询引擎**，也不含表结构定义；schema 契约只有 CLI 那一份。
> 拆分理由见源码仓 `docs/architecture/cli-skill-split.md`。

## 1. 运行时与前置条件

架构证据查询 skill 的运行时来自一个统一归档 `knowledge.tar.gz`，解压后必须得到：

```text
knowledge.tar.gz
├── knowledge.db
├── oskm-cli.pyz      # 查询 CLI（固定文件名，不带版本）
└── interface/
    ├── sdk-js/       # ArkTS API / Kit 声明
    └── sdk_c/        # Native SDK 头文件
```

**归档里的四样东西是同一个发布单元**：`install` 一次装齐，`download-db` 从
同一个归档里只捞出 `knowledge.db`。没有单独的 CLI 下载物，也没有单独的
DB 下载物。

安装后的托管目录为：

```text
<runtime-root>/            # 默认 ~/.oskm，可用 --runtime-root 或 OSKM_RUNTIME_ROOT 改
  knowledge.db
  .oskm-runtime.json       # version 3：日期、下载方式、db/sdk/cli 三段产物
  oskm-cli.pyz             # 独立产物，与 knowledge.db 并排；install/update-cli 装到这里
  .env                     # 可选；优先级低于真实环境变量
  interface/
    sdk-js/
    sdk_c/
```

CLI 与 `knowledge.db` **同类**：固定文件名、不记版本、不锁摘要，装在运行时根目录下
并排。`.oskm-refresh-retry`（15 分钟失败退避标记）已于 2026-11-12 删除——
那是"每条查询都可能触发下载"时代的产物，刷新改为显式命令后不需要退避。

`install` 下载并安全解压这个归档；`download-db` 从同一个归档中只提取
`knowledge.db`。下载端点只负责取归档，**不再从 Git 仓库拉取 SDK**，不要求
GitCode/CodeHub 凭据，也没有 SDK 分支参数。DB 中的 `source_path` /
`header_path` 相对 `<runtime-root>` 解析，因此目录必须是
`interface/sdk-js/` 与 `interface/sdk_c/`，不能多套一层 `interface/interface/...`。

运行时下载、安装、状态和显式刷新只有一个功能入口：

```bash
python3 bootstrap.py doctor|install|refresh|update-cli|download-db|validate-db|cli-path ...

# 查询不归 bootstrap 管，直接调 CLI（固定文件名，不带版本）：
python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db arch|ask|diff|sql ...
```

它使用 **Python 3.10+ 标准库**：HTTP 走 `urllib.request`，tar 走 `tarfile`，
历史 zip DB 走 `zipfile`，SQLite 校验走 `sqlite3`。Windows 不需要 Bash、curl、
unzip 或 tar，查询和运行时命令统一把 `python3` 换成 `py -3`。

**没有 `.sh` 包装器**（2026-11-12 随拆分删除）：它们要求 Bash，而 skill 的承诺是
Windows 上 `py -3 bootstrap.py …` 同样能用。一个只在两个平台上成立的入口，
等于在第三个平台上没有入口。

`--runtime-root` 是 bootstrap 级的选项，写在命令前后都行；摘掉之后子命令解析器
始终看不到它。`validate-db PATH` 会用 `PATH` 的父目录当运行时根——CLI 就装在
那个库旁边。

### CLI 产物从哪来

CLI 是**独立构建产物**，随 `knowledge.tar.gz` 一起发布（不是 skill 源码的一部分，
也不是单独下载物）。它与 `knowledge.db` 同类：**固定文件名 `oskm-cli.pyz`，不记版本、
不锁摘要**。安装在 `<runtime-root>/` 下与 `knowledge.db` 并排，所以文档与调用方
始终不用钉版本号；版本问产物自己（`oskm-cli.pyz --version`）。

`bootstrap.py` 按**三级**候选定位，第一个命中的就用（三步都不联网）。源码树
存在时优先使用本地 CLI，发布包没有 CLI 源码时自然回退到已安装产物：

| # | 候选 | 校验 |
|---|---|---|
| 1 | `$OSKM_CLI`（`.pyz` 或源码目录） | 结构校验 |
| 2 | 源码树 `packages/oskm/cli` 或 `cli/oskm_cli` | 无（开发路径） |
| 3 | `<runtime-root>/oskm-cli.pyz`（`install` 从 `knowledge.tar.gz` 解出来的那份） | 结构校验 |

**结构校验**（`cli_install.verify_pyz`）= shebang + 是有效 zip + 含
`__main__.py` 与 `oskm_cli/cli.py` + CRC 完好。它与 DB 那侧的 `verify_sqlite`
（文件头 + `PRAGMA integrity_check`）是同一思路：校"它是不是一个能用的产物"，
而不是"它是不是某一次构建的那一份"。最常见的失败形态是端点返回 200 + 一个
HTML 错误页——不挡住的话，症状会变成后面某处一句看不懂的 ImportError。

```bash
python3 bootstrap.py cli-path               # bootstrap 最终选了哪一个
python3 bootstrap.py update-cli --force     # 删掉已装产物后重新解析
python3 <runtime-root>/oskm-cli.pyz --version
```

状态文件里的 `cli` 段记 `{path, sha256}`，与 `db.sha256` 同性质：**出处记录**，
不是期望值，不参与任何校验。

> 这里曾经有两套现已删除的机制。`cli_pin.json`（version + sha256 锁）与
> "源码树版本必须等于 pin，否则硬失败"：它们防的是开发时源码树与已装产物漂移，
> 代价是每次改 `oskm_cli/**` 都要重跑 `--update-pin`，而失败信息指向一个与改动
> 毫无关系的摘要（实测踩到过，改的是一句注释）。npm 分发通道
> （`node_modules/oskm-cli/vendor/`）：pyz 自己就能直接执行，多一条通道就多一处
> 会漂的版本和一份要维护的启动器。

### 检查并安装依赖

只需要 **Python 3.10+**；查询已有 DB、下载、安装和显式刷新都不要求 Git。
Python 侧没有 pip 第三方包，但内部模块必须可导入。解压独立发布包后，在
`ohos-design-architecture-evidence-query/` 根目录运行全量检查：

```bash
cd ohos-design-architecture-evidence-query
python3 bootstrap.py doctor
```

`doctor` 按 **Python → 下载配置 → CLI → 运行时状态** 的顺序检查，第一个 FAIL
通常就是根因；它会报告解析到的 CLI 位置、`oskm_runtime`/`oskm_cli`/`oskm_schema`
是否可导入、以及状态文件里的 `db`/`sdk`/`cli` 三段是否齐全。`OSKM_DOWNLOAD_SOURCE` 只能是 `OPENHARMONY_CI` 或 `INTERNAL_CI`，
默认 `OPENHARMONY_CI`；`OSKM_DOWNLOAD_ENDPOINT` 必须是 HTTP(S) URL。
诊断输出只显示下载方式和端点配置状态，不会打印 URL。

macOS（Homebrew）：

```bash
brew install python@3.12
python3.12 bootstrap.py doctor
```

Ubuntu/Debian：

```bash
sudo apt update
sudo apt install python3.12
python3.12 bootstrap.py doctor
```

如果发行版仓库没有 `python3.12`，安装其提供的最新 Python（必须 ≥3.10），
并替换命令中的解释器名。

Windows PowerShell：

```powershell
winget install Python.Python.3.12
cd <ohos-design-architecture-evidence-query 解压目录>
py -3.12 bootstrap.py doctor
```

如果 `py -3` 指向 Python 3.9 或更早，请显式使用 `py -3.12`；查询和安装命令同理。

### 下载方式与 `.env`

下载端点只从环境变量读取，下载方式只由 `OSKM_DOWNLOAD_SOURCE`
（或命令行 `--source`）决定。仓库只提交本地模板 `oskm_runtime/.env.example`；
真实 `.env` 已被 `.gitignore` 忽略，不提交。**只有 `bootstrap.py` 读它，
oskm-cli 不读任何 `.env`**——查询 CLI 不联网，也就不该有端点概念。

`.env` 查找顺序：真实环境变量 > `<runtime-root>/.env` > `oskm_runtime/.env`。
已安装目录可能是只读的，所以运行时根目录那份优先。

两个下载环境变量（必填的是 ENDPOINT），两个可选变量：

```dotenv
OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI
OSKM_DOWNLOAD_ENDPOINT=https://<CI API 或归档前缀>
# 可选：
# OSKM_CLI=/abs/path/oskm-cli.pyz      第 1 级候选（显式覆盖）
# OSKM_RUNTIME_ROOT=~/.oskm            等价于每条命令都写 --runtime-root
```

**没有 `OSKM_CLI_ENDPOINT`。** CLI 在 `knowledge.tar.gz` 里，不需要第二个端点。

写入 `.env` 的键必须在 `ENV_KEYS` 白名单里，写错会**报错**而不是被静默忽略。

初次使用时：

```bash
cp oskm_runtime/.env.example oskm_runtime/.env
"${EDITOR:-vi}" oskm_runtime/.env
python3.12 bootstrap.py doctor
```

`OPENHARMONY_CI` 向 `$OSKM_DOWNLOAD_ENDPOINT` POST；
`startTime` / `endTime` 是同一个日期范围的两端，不是两个独立时间输入：

```json
{
  "component": "dayu600_7885_ai",
  "startTime": "${date}00000000",
  "endTime": "${date}235959",
  "buildStatus": "success"
}
```

component 固定为 dayu600_7885_ai，由代码常量提供，不通过环境变量或命令行传入。
成功构建响应从 `.data.list.dataList[0].obsPath` 读取 OBS 地址；OBS 地址必须
可直接下载（例如预签名 URL）。

INTERNAL_CI URL 为 `$OSKM_DOWNLOAD_ENDPOINT/$date`，响应文件名应为
`knowledge.tar.gz`，不使用旧 latest 端点。缺失或格式错误时，下载器会在联网前报错；

Windows PowerShell：

```powershell
Copy-Item oskm_runtime\.env.example oskm_runtime\.env
notepad oskm_runtime\.env
py -3.12 bootstrap.py doctor
```

也可以只在当前 shell 设置：

```bash
export OSKM_DOWNLOAD_SOURCE='OPENHARMONY_CI'
export OSKM_DOWNLOAD_ENDPOINT='https://<CI API 或归档前缀>'
```

```powershell
$env:OSKM_DOWNLOAD_SOURCE = "OPENHARMONY_CI"
$env:OSKM_DOWNLOAD_ENDPOINT = "https://<CI API 或归档前缀>"
```

### 安装托管运行时

推荐固定使用 `~/.oskm` 作为 Agent 的运行时根目录。初次查询前先检查
`~/.oskm/knowledge.db`；如果不存在，先执行下面的 `install`，成功后再查询该库。
查询 CLI 不会自动刷新任何运行时；任意 `--db` 路径缺失时也不会触发联网下载。
需要更新时显式执行 `bootstrap.py refresh` 或 `bootstrap.py install`。

#### 源码根优先使用本地构建

`install` 先探测源码根本地构建，命中就用本地 DB + SDK + CLI，不联网。不传
`--source-root` 时从 cwd 向上找最近的 OpenHarmony 源码根，因此在源码根或其任意
子目录执行都能命中。不在源码树内时传 `--source-root <path>`；显式路径必须是
OpenHarmony 源码根，否则直接报错，不会静默改用 cwd 或下载。

源码根必须同时存在 `.gn`、`interface/sdk-js/`、`interface/sdk_c/`、`out/`；
`install` 会检查两套 SDK、源码构建里的 DB 和源码树 CLI：

```text
<source-root>/interface/sdk-js/                       # 必须存在且非空
<source-root>/interface/sdk_c/                        # 必须存在且非空
<source-root>/out/<product>/oskm/knowledge.db          # 一层布局
<source-root>/out/<abi>/<device>/oskm/knowledge.db     # 两层布局
<source-root>/artifacts/<product>/knowledge.db         # 扫描产物布局
<source-root>/cli/dist/oskm-cli.pyz                    # 可选；存在则一起装入
```

布局按 `product` 路径自动判断，只匹配上述一至两层 `out` 布局，不递归扫描整个 `out/`；有多个候选时按数据库文件
修改时间选择最新者。DB 必须通过当前查询层 schema 校验。命中的 DB、CLI 与两套 SDK
会先复制到安装事务的临时目录，再装入 `<runtime-root>/`，因此源码树中的文件只读，
不会被移动或修改。任一文件缺失、SDK 目录为空、DB 损坏或 schema 不兼容时，自动
回退到按 `OSKM_DOWNLOAD_SOURCE` 选择的下载流程；成功状态会记录 `"source": "local"`
与源码根路径。

给 Agent 或日常查询使用托管运行时，一次安装 DB、CLI 和两套 SDK：

```bash
RUNTIME_ROOT="$HOME/.oskm"
date=20261102

# OpenHarmony CI（component 固定为 dayu600_7885_ai）
python3 bootstrap.py install --source OPENHARMONY_CI --runtime-root "$RUNTIME_ROOT" --date "$date"
python3 bootstrap.py install --source OPENHARMONY_CI --runtime-root "$RUNTIME_ROOT" \
    --source-root <OH源码根> --date "$date"

# Internal platform CI（GET <endpoint>/<YYYYMMDD>）
python3 bootstrap.py install --source INTERNAL_CI --runtime-root "$RUNTIME_ROOT" --date "$date"
```

Windows PowerShell 直接调用同一模块，不需要 Bash：

```powershell
$RuntimeRoot = "$env:USERPROFILE\oskm-runtime"
$date = "20261102"
py -3 bootstrap.py install --source OPENHARMONY_CI `
    --runtime-root $RuntimeRoot --date $date
py -3 bootstrap.py install --source INTERNAL_CI `
    --runtime-root $RuntimeRoot --date $date
```

- 省略 `--date` 时，安装器取本地时区的系统当天；历史快照显式传 `YYYYMMDD`。
- `--skip-db` 只准备 SDK，`--skip-sdk` 只准备 DB；两者不能同时使用。
- 安装器先探测并校验源码根本地运行时；未命中或不可用时再下载并校验归档。随后按
  `--skip-*` 选择要替换的产物；DB 与两套 SDK 在同一事务中逐项替换，中途失败会回滚。
- 安全解压接受归档根目录的 `knowledge.db`、`oskm-cli.pyz` 与
  `interface/sdk-js/`、`interface/sdk_c/`；根目录的其余普通文件（如构建日志和清单）
  会被忽略且不落盘。
  未知目录、完整路径、`..`、硬链接、设备文件和逃逸 SDK 目录树的符号链接仍会被拒绝。
- SDK 路径缺失、为空时明确报告 **`SDK 源码缺失`**，不会静默跳过源码证据。
- `--skip-db` / `--skip-sdk` 会保留尚未刷新的那一侧的旧状态；之后显式执行
  `refresh` / `install` 时，托管运行时会补齐缺失的一侧，源码本地运行时则需重新
  `install` 才会更新。

成功安装后，安装器会原子写入 `<runtime-root>/.oskm-runtime.json`（version 3，
比 2 多一个 `cli` 段；旧的 version 2 仍能读，缺 `cli` 只表示"这个根目录还没装 CLI"，
由 `update-cli` 或下一次 `install` 补齐，**不会因此触发 DB/SDK 重新下载**）。
`bootstrap.py refresh` 读取这个文件做一次**廉价检查**：状态结构合法、
日期是否当天、DB 文件在不在、两套 SDK 目录非空、SQLite 能否打开且 `scans` 可读。
过期才重装；不过期就什么都不做（也不会去碰 CLI）。

> **2026-11-12 的行为变更**：刷新**不再挂在查询前面**。查询透传删掉之后
> （`bootstrap.py` 只负责装），没有任何隐式触发点了——数据过期时请显式跑
> `bootstrap.py refresh`。随之删掉的还有 15 分钟失败退避标记
> `.oskm-refresh-retry`：那是"每条查询都可能触发下载"时代的产物，
> 显式命令不需要退避。

下载安装的托管运行时只要 DB 或任一 SDK 的日期不是当天，`refresh` / `install`
就会刷新到当天；
源码树本地运行时（`"source": "local"`）不因日期变化刷新，显式执行 `install` 才会
重新选择并复制源码树中的最新 DB/CLI/SDK。托管运行时**只覆盖最新一份**，不建立按日期
命名的历史目录。状态文件是托管标记：没有该文件的 `artifacts/*/knowledge.db`
视为用户自管，始终不会自动联网。

> **2026-11-12 的行为变更**：廉价检查**不再跑 `PRAGMA integrity_check`**，
> 也不再逐表逐列比对 schema。旧实现在每次查询前都做全量校验，19 MB 的库要
> ~128 ms；而库是 `install` 校验通过后才原子落盘的，之后没有任何代码路径会改它，
> 等于把安装期已经付过的成本按查询次数重付。完整的表/列契约校验现在只在两处执行：
> `install` 落盘前，以及显式 `validate-db`——两处都由 **CLI 的
> `oskm_cli.database`** 提供，skill 里没有第二份清单。降级后仍能捕获真正会发生的
> 故障（文件被删、被截断、被写坏到打不开）。

如果当天构建尚未就绪、网络失败或新归档校验失败，`refresh` / `install` 会以退出码 1
报错，而**已有运行时原样保留**——`_install_artifacts` 先把旧产物 `os.replace` 到
同目录的备份目录，任一步失败就逆序还原。半装的运行时比没装更坏：查询会返回
看起来合理的空结果。修好网络或配置后再跑一次即可。任何情况下都不会为缺失的
`--db` 路径自动下载——那种情况由 CLI 用退出码 3 报错。

### 只下载指定日期的 DB

只需要保存某天的历史 DB、不需要 SDK 时，使用独立下载：

```bash
DB_OUT=/path/to/knowledge_20261102.db
date=20261102

# OpenHarmony CI（component 固定为 dayu600_7885_ai）
python3 bootstrap.py download-db --source OPENHARMONY_CI --date "$date" --output "$DB_OUT"

# Internal platform CI
python3 bootstrap.py download-db --source INTERNAL_CI --date "$date" --output "$DB_OUT"
```

Windows：

```powershell
$DBOut = "$env:USERPROFILE\knowledge_20261102.db"
$date = "20261102"
py -3 bootstrap.py download-db --source OPENHARMONY_CI `
    --date $date --output $DBOut
py -3 bootstrap.py download-db --source INTERNAL_CI `
    --date $date --output $DBOut
```

`download-db` 对统一归档只读取其中的 `knowledge.db`，不会安装 SDK。为兼容历史
下载物，仍按文件名后缀支持：

| 文件后缀 | 处理 |
|---|---|
| `.db` | 直接作为候选 |
| `.zip` | `zipfile` 读取 |
| `.tar`、`.tar.gz`、`.tgz`、`.tar.xz`、`.txz`、`.tar.bz2`、`.tbz2` | `tarfile` 读取 |
| 其余 | 明确失败 |

归档中必须恰有一个普通文件 `knowledge.db`。独立下载只校验 SQLite 完整性和结构：
文件头、能够只读打开，并通过 `PRAGMA integrity_check`。它**不要求历史 DB 满足当前
查询层 schema**，因此可用来保存旧日期快照。托管运行时安装则校验当前 oskm 查询层
schema，包括 `scans.product`、`scans.cpu_arch`、`collector_tables` 等；
schema 不匹配的旧库直接拒绝安装，不做列迁移，需要重新扫描。校验失败不会修改
已有 DB、SDK 或状态。

独立下载和运行时安装都会先写输出目录内的临时文件，再原子替换目标。网络、HTTP、
归档、完整性或 schema 校验失败都不会破坏已有输出或运行时。

### 下载故障诊断

HTTP 默认使用系统和 `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY` 环境配置。失败信息会
区分 HTTP 状态、超时、TLS/证书、DNS/代理和下载不完整；检查构建日期、当前下载端点与
`knowledge.tar.gz` 是否存在后重试。Python 路径不依赖 `curl -vI`，Windows 可直接用
`Invoke-WebRequest` 或 `Test-NetConnection` 做网络排障。

归档解压失败时先检查根目录结构：

```bash
tar -tzf knowledge.tar.gz | head -50
```

正常情况下应看到 `knowledge.db`、`interface/sdk-js/...` 和
`interface/sdk_c/...`；多套一层顶层目录不会被安装器猜测或自动剥离。

校验当前查询层 schema 可单独运行（**转发给 CLI**，退出码 `0` 通过 / `2` 不兼容）：

```bash
python3 bootstrap.py validate-db "$RUNTIME_ROOT/knowledge.db"
python3 "$RUNTIME_ROOT/oskm-cli.pyz" validate-db "$RUNTIME_ROOT/knowledge.db"   # 等价
```

这是唯一会跑 `PRAGMA integrity_check` 加全表全列比对的命令；日常查询不走它。

归档中的 SDK 快照应与 DB 的扫描 revision 配套；没有 Git HEAD 时，仍按 DB 中的
revision 比较证据，`content_match` 应视为 `unverified`。目标若为
`~/.oskm/knowledge.db` 且文件不存在，应先执行 `bootstrap.py install`；查询发布包本身
不扫描、不重建库。只有确实需要自行生成数据时，才回到 `packages/oskm` 源码仓使用
采集器；采集入口与查询入口不是同一个命令。

回到发布包根目录即可检查运行时：

```bash
cd ohos-design-architecture-evidence-query
python3 bootstrap.py doctor
```

下文用 `DB="$RUNTIME_ROOT/knowledge.db"`。示例中的路径和实体名是占位符；实际查询
先做宽搜索，再按返回的真实 `dest`、部件名或服务名调整，不要从扫描元数据推断
架构目录。

## 2. 四个子命令

下文统一用这两个变量（`RUNTIME_ROOT` 默认 `~/.oskm`）：

```bash
RUNTIME_ROOT="${RUNTIME_ROOT:-$HOME/.oskm}"
CLI="$RUNTIME_ROOT/oskm-cli.pyz"      # 固定文件名，不带版本
DB="$RUNTIME_ROOT/knowledge.db"
python3 bootstrap.py cli-path         # 不确定 CLI 在哪时问它
```

| 命令 | 干什么 |
|---|---|
| `oskm-cli arch <问题> [目标]` | 六类顶层架构问题，一条命令串完多步 |
| `oskm-cli ask <工具> [--参数]` | 直接调任意一个查询工具（52 个） |
| `oskm-cli diff --entity <实体>` | 跨库或跨快照对比 |
| `oskm-cli sql --file <文件>` | 受限只读 SQL |

全局参数：`--db PATH`（可给两次，见 §5）、`--product NAME`、`--scan-id N`、
`--format json|table`。

**不猜默认产品**：不给 `--db` 时用 `<runtime-root>/knowledge.db`；要查别处的库就
显式给 `--db`。`--product NAME` 只在 `artifacts/<NAME>/knowledge.db` 真的存在时才有
意义——`artifacts/` 的目录布局很容易被误认成"N 个产品"，而按域导出的 JSON 目录里
并没有 knowledge.db。**宁可报错也不蒙一个。**

## 3. `arch`：六类架构问题

```bash
python3 "$CLI" --db "$DB" arch overview
python3 "$CLI" --db "$DB" arch trace system/lib64/module/multimedia/libimage.z.so
# 库级影响面：仅当 ask get_scan_info 显示 ELF 采集器完整时使用真实 dest
python3 "$CLI" --db "$DB" arch impact <elf-dest>
python3 "$CLI" --db "$DB" arch impact init          # 不带 / 的按部件反查
python3 "$CLI" --db "$DB" arch provides image_framework
python3 "$CLI" --db "$DB" arch switch ace_engine_feature_asbng_path
python3 "$CLI" --db "$DB" arch runtime foundation
```

`arch trace` 一条命令走完五跳——镜像文件 → 安装模块 → 部件 → 子系统 → 代码仓，
外带它实现的 SDK 接口与直接依赖数：

```json
{
  "file": "system/lib/module/multimedia/libimage.z.so",
  "install_module": "//foundation/multimedia/image_framework/interfaces/kits/js/common:image_napi",
  "component": "image_framework",
  "subsystem": "multimedia",
  "repo": "multimedia_image_framework",
  "repo_url": "https://vpcep-f2878022-9474-4e70-80e2-86fdcbb5ca6d.cn-north-4.huaweicloud.com/openharmony/multimedia_image_framework",
  "sdk_modules": ["api/@ohos.multimedia.image"],
  "direct_dependencies": 5  // 无 ELF 证据时为 null；数值随库走
}
```

**`arch` 只有六条，而且只编排 `ask` 已有的工具、不自带 SQL。**
它不会给出 `ask` 给不了的事实，只是省掉手工串多步。有测试盯着这条约束
（`test_cli.py::test_arch_writes_no_sql`）。

## 4. `ask`：直接调工具

```bash
python3 "$CLI" ask --list                        # 全部工具，按模块分组
python3 "$CLI" ask get_component --help          # 参数与枚举，从 schema 生成
python3 "$CLI" --db "$DB" ask get_component --name ace_engine
python3 "$CLI" --db "$DB" ask list_arkts_modules --limit 5
python3 "$CLI" --db "$DB" --format table ask search_elf_modules --query libimage
```

子命令、参数、类型、枚举、帮助文本**全部由工具的 JSON Schema 生成**，
不是手写的——加一个工具，CLI 和 `--help` 自动就有，不会过期。
枚举错值在 argparse 这一层就被拒：

```
$ python3 "$CLI" --db "$DB" ask list_arkts_modules --implementation_kind bogus
error: argument --implementation_kind: invalid choice: 'bogus'
       (choose from 'napi','arkui','arkts_builtin','arkts_language','type_only','unknown')
```

数组参数用空格分隔（不用逗号——逗号在 GN label 和路径里都出现）：

```bash
python3 "$CLI" --db "$DB" ask aggregate --table components --group_by subsystem
```

对象参数收 JSON：

```bash
python3 "$CLI" --db "$DB" ask list_entities --table components --page '{"limit": 3}'
```

### 典型问答

| 问题 | 命令 |
|---|---|
| 某文件属于哪个部件 | `ask owner_of --dest system/lib/libcamera.z.so` |
| 某部件有哪些 feature | `ask get_component --name X` 取 id，再按工具 `--help` 查询对应 component 的 features |
| foundation 跑哪些 SA | `arch runtime foundation` |
| SA 1401 是什么 | `ask get_sa --sa_id 1401` |
| libfoo 依赖哪些库 | `ask search_elf_modules --query libfoo` → `ask elf_dependencies --dest <路径> --max_distance 1` |
| 某编译参数当前值 | `ask get_gn_arg --name ace_engine_feature_enable_web` |
| 哪些部件依赖 ace_engine | `arch impact ace_engine` |
| 扫描有哪些质量问题 | `ask list_issues` |
| 按子系统统计部件数 | `ask aggregate --table components --group_by subsystem` |

> `component_*` 这批工具收的是 `component_id` 而不是名字，先用 `get_component`
> 换 id。`arch provides` / `arch impact` 已经替用户做了这一跳。

## 5. `diff`：两个库对比

```bash
python3 "$CLI" --db a.db --db b.db diff --entity components
python3 "$CLI" --db a.db --db b.db diff --entity gn_args --fields current_value
python3 "$CLI" --db "$DB" diff --entity components --scan-a 1 --scan-b 2
```

`--db` 给两次就是跨库（CLI 在一次调用内 open + ATTACH，alias 不对外暴露）；
给一次加 `--scan-a/--scan-b` 就是同库两快照——**这两个是 `diff` 的参数，写在 `diff` 之后**。
`--entity` 取 components / gn_args / features / services / install_modules / innerapis。

输出是结构化三段：

```json
{"entity": "components", "added": [], "removed": ["ace_engine", "image_framework"],
 "changed": [{"key": "init", "changes": [
   {"field": "subsystem", "before": "startup", "after": "changed"}]}]}
```

需要跨库 JOIN 这种 `diff` 表达不了的对比时，当前没有开放 `sql` 的跨库
`--attach` 形态；不要假设第二个库可以用 `b.` 前缀访问。

## 6. `sql`：复杂查询走文件

```bash
python3 "$CLI" --db "$DB" sql --file query.sql
cat query.sql | python3 "$CLI" --db "$DB" sql --file -
python3 "$CLI" --db "$DB" sql --sql "SELECT COUNT(*) AS n FROM components"
python3 "$CLI" --db "$DB" sql --file q.sql --param ace_engine --param system
```

**多行 SQL 不要塞进命令行**——单引号、`%`、换行在 shell 里全是坑，这正是
支持 `--file` 的原因。文件里可以带注释：

```sql
-- 各子系统部件数，排除三方
SELECT c.subsystem, COUNT(*) AS parts
  FROM components c
 WHERE c.subsystem != 'thirdparty'
 GROUP BY c.subsystem HAVING parts > 8 ORDER BY parts DESC
```

只读校验照常生效：第一个关键字必须是 SELECT/WITH（**跳过开头注释后再判**），
表名走白名单，自动注入 `scan_id` 与 `LIMIT`。
`-- SELECT\nDROP TABLE x` 这种伪装会被拒。

## 6.5 查询故障与回退

SKILL.md 只留判据，完整说明在这里。**遇到失败先停手，不要换个库或编个数交差。**

| 现象 | 判据与做法 |
|---|---|
| 退出码 3 / `database not found` | 缺的是库不是知识。跑 `bootstrap.py install`，或核对 `--db` 指向；**不要**换一个不相干的库 |
| `NO_COMPLETED_SCAN` / `SCAN_INCOMPLETE` | 该库没有已完成的快照：换 `--scan-id`，或重扫后重装 |
| 退出码 5 | stderr 的 JSON 有 `code` / `message`；先分是参数错还是证据缺失 |
| `elf_modules=0` | ELF 证据未采集：`arch impact <dest>` 会以 5 退出，改答"该证据不可用"，不要给出依赖数量 |
| `truncated=true` | 提高 `limit`，或按 `total` 报告，不要当全量 |
| SDK 源码缺失 | 需要源码证据的结论无法核对：明确说"SDK 源码缺失"，不要静默降级成"没有关系" |
| 跨快照对不上 | 先核 `scan_id` / `cpu_arch` 一致；比两个快照用 `diff` |

下载失败、`.env` 不生效、解压被拒等安装侧排错，见上文「下载故障诊断」。

## 7. 退出码

| 码 | 含义 |
|---:|---|
| 0 | 正常 |
| 2 | 参数错（含 argparse 的枚举/必填校验）；`validate-db` 不兼容也用 2 |
| 3 | 库打不开 |
| 5 | 工具返回 error，详情 JSON 打到 stderr |

与源码仓采集侧 `python3 -m oskm.cli scan` 的退出码口径一致，没有另造一套。
这四个码属于 **oskm-cli**（查询直接调它，不经 bootstrap）。
`bootstrap.py validate-db` 转发给 CLI，所以沿用同一套；其余托管命令另有一个码：

| 码 | 含义 |
|---:|---|
| 1 | 托管命令失败（下载失败、找不到 CLI、状态文件损坏、`.env` 有不支持的键） |

`doctor` 用 `0` / `1` 表示"就绪 / 未就绪"。

## 8. 工具速查

共 52 个工具、14 个模块。生成式索引见
[tools.md](./tools.md)（由 `python3 "$CLI" ask --list --markdown` 生成），
字段级规格见 [spec/](./spec/)。

会话类的那 7 个（`open_session` / `attach_secondary` / `diff_scans` …）
在 CLI 里**退化成参数**——`--db` / `--scan-id` 和 `diff`。
它们仍在注册表里、`ask` 也能直通，但不作为日常用法介绍。

## 9. 测试与构建

```bash
cd packages/oskm
# 仅 CLI 的真实库样本测试需要；skill 测试全部使用合成库，可不设置。
export OSKM_TEST_DB="$HOME/.oskm/knowledge.db"

# 两个产物各有一套测试；共用合成库辅助在 packages/oskm/oskm_testing/
python3.12 -m unittest discover -s cli/tests -p "test_*.py"
python3.12 -m unittest discover -s skills/ohos-design-architecture-evidence-query/tests -p "test_*.py"

# 两个产物互不依赖，构建先后顺序无所谓；各写各的 dist/
python3.12 cli/scripts/build_cli.py                                    # → cli/dist/oskm-cli.pyz
python3.12 skills/ohos-design-architecture-evidence-query/scripts/build_skill.py

# 发布包解压后先验证运行时入口；尚未安装时执行 bootstrap.py install
python3.12 bootstrap.py doctor
python3.12 bootstrap.py cli-path
python3.12 ~/.oskm/oskm-cli.pyz ask --list        # 查询直接调 CLI
```

> 本机 `python3` 可能是 3.9（macOS Command Line Tools 就是），跑不了本仓
> ——`oskm_schema/base.py` 用了 `str | None`。**一律用 `python3.12`。**
> pyz 的 `__main__.py` 里有版本守卫，撞上 3.9 会给出可执行的提示而不是
> 一句 `TypeError: unsupported operand type(s) for |`。
