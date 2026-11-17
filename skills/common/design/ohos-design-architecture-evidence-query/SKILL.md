---
name: ohos-design-architecture-evidence-query
description: "当用户需要安装或更新 OpenHarmony 架构证据运行时，或询问产品顶层架构证据时使用：安装 DB、两套 SDK 与 oskm-cli，再用 CLI 查询子系统、部件、代码仓、镜像文件归属、影响面、SysCap/InnerAPI/SDK 接口和 GN 编译开关。只读已有库；不扫描、不编译、不改库。"
metadata:
  author: "openharmony"
  scope: "common"
  stage: "design"
  domain: "architecture"
  capability: "evidence-query"
  version: "3.1.0"
  status: "trial"
---

# OpenHarmony 架构证据运行时与 CLI 使用

## 1. 任务与边界（Task and Boundaries）

本 skill 的核心职责是把 `knowledge.db`、`interface/sdk-js`、`interface/sdk_c`、
`oskm-cli.pyz` 下载并安装到运行时根目录，同时提供 CLI 的整体功能说明；具体查询由
CLI 执行，skill 不内置查询引擎。

**只做**：安装/刷新运行时；定位并校验 CLI；说明 CLI 入口；按 DB 里的路径读 SDK
源码核对声明、头文件与实现 `.so`。
**不做**：不扫描、不建库、不编译、不改 DB 或 SDK 源码、不查实时设备状态——库是
一次扫描的**快照**，`git` 提交号是扫描当时的。

## 2. 触发信号（Trigger Signals）

命中任一即适用：「安装/更新 oskm 运行时」「找不到 CLI」「doctor / install /
refresh / cli-path」，以及「这个产品由哪些子系统/部件构成」「这个 `.so` / `.img` /
配置文件属于谁」「改 X 会影响谁」「某部件对外提供什么」「SysCap / InnerAPI 由谁
实现」「这个 GN 参数控制什么」「某 SDK 模块的实现在哪、声明在哪」「这个原生库
有哪些 Native SDK 头文件」「两个库或两个快照差了什么」，以及 `degraded`、
`elf_modules=0`、`truncated`、`out_of_scope` 这类证据边界问题。**不适用**：
要新扫一个产品（用源码仓的采集器）、要看设备运行态、要改代码。

## 3. 首要判断（Initial Checks）

按顺序走，前一步不成立就别往后：

1. **运行时是否就绪。** 先跑 `bootstrap.py doctor`；库或 CLI 缺失时执行
   `bootstrap.py install`，再用 `cli-path` 确认实际 CLI 位置。
2. **库在哪、能不能开。** 查询必须给 `--db`（或 `--product X`，按
   `artifacts/X/knowledge.db` 推导）；不猜默认产品，**不要**换一个不相干的库凑答案。
3. **这份证据全不全。** 先 `ask get_scan_info` 看 `status` 与各采集器的
   `status`/`record_count`。`degraded` 不等于失败——**degraded 数量和原因随库、
   产品与采集器版本变化**；但**对应证据计数为 0 时该查询不可用**，不要编数。
4. **该用哪个入口。** 六类架构问题用 `arch`（它只编排 `ask`，省掉手写多跳）；
   单点字段用 `ask`；对比用 `diff`；聚合与长 SQL 用 `sql --file`。

## 4. 执行策略（Execution Strategy）

### 4.1 安装运行时与 CLI 入口

`bootstrap.py` 只负责**装**（`doctor` · `install` · `refresh` · `update-cli` ·
`download-db` · `validate-db` · `cli-path`）；查询**直接调 CLI**。CLI 是独立产物，
但随发布归档交付：固定名 `oskm-cli.pyz`、不记版本、不锁摘要（版本问 `--version`）。
数据过期时显式 `refresh`，**查询不会自动触发下载**。
当前目录是 OpenHarmony 源码根或其子目录时，**源码树优先**：向上探测本地 `out/**/oskm/knowledge.db`（或 `artifacts/*/knowledge.db`）、源码树 `oskm-cli.pyz`、`interface/sdk-js`、`interface/sdk_c` 可用则不下载；不在源码树内时用 `--source-root <OH源码根>`。
```bash
AGENT_CWD="$PWD"; SKILL_DIR=/path/to/ohos-design-architecture-evidence-query
python3 "$SKILL_DIR/bootstrap.py" install --runtime-root ~/.oskm; cd "$AGENT_CWD"  # 安装完成后回到 Agent 启动目录
python3 "$SKILL_DIR/bootstrap.py" install --runtime-root ~/.oskm --source-root <OH源码根>  # cwd 不在源码树内
CLI=~/.oskm/oskm-cli.pyz; DB=~/.oskm/knowledge.db   # 实际位置问 cli-path
python3 $CLI --db $DB arch overview
```

`knowledge.tar.gz` 是唯一发布单元：`knowledge.db` + `oskm-cli.pyz` +
`interface/sdk-js` + `interface/sdk_c`，`install` 一次装齐，没有单独下载物。下载方式
和端点由 `OSKM_DOWNLOAD_SOURCE` / `OSKM_DOWNLOAD_ENDPOINT` 选择；`OPENHARMONY_CI`
的 component 固定为 `dayu600_7885_ai`。底层只用 Python 标准库（3.10+），不要求 Git；
装后先跑 `python3 bootstrap.py doctor`；`python3` 需 ≥3.10（macOS 默认 3.9 时用 `python3.12`），排错见 `references/usage.md`。

### 4.2 六类架构问题：`arch`

```bash
python3 $CLI --db $DB arch overview                       # 1 这个产品由什么构成
python3 $CLI --db $DB arch trace system/lib64/module/multimedia/libimage.z.so
python3 $CLI --db $DB arch impact init                    # 3 改它影响谁（带 / 是库级）
python3 $CLI --db $DB arch provides image_framework       # 4 某部件对外提供什么
python3 $CLI --db $DB arch switch ace_engine_feature_asbng_path
python3 $CLI --db $DB arch runtime foundation             # 6 服务名模糊搜索，可能返回多个
```

回答 GN 开关问题时必须报告 `feature_count` 和关联 `features` 名称——只给当前值
和声明文件说明不了影响面。示例路径随库走（`scans.cpu_arch` 决定 `system/lib/`
还是 `system/lib64/`）；`sas.libpath` 只是 profile 声明值，真实 `dest` 用 `ask search_elf_modules --query <文件名>` 或 `install_targets` 查。

### 4.3 更细的查询：`ask`

```bash
python3 $CLI ask --list                        # 52 个工具，按模块分组
python3 $CLI ask get_component --help          # 参数与枚举从 schema 生成
python3 $CLI --db $DB ask get_component --name ace_engine
python3 $CLI --db $DB --format table ask search_elf_modules --query libimage
python3 $CLI --db $DB ask search_native_headers --query image    # 原生库 → SDK 头文件
```

ELF / Native SDK 证据问题先各做一次**宽搜索**，报告 ELF 与 Native SDK 宽搜索的 `total` 与
`truncated`；精确命中数不是宽搜索总数，`truncated=true` 时先提高 `limit` 或说明
截断。数组参数用空格分隔（逗号在 GN label 和路径里都出现），对象参数收 JSON，
`component_*` 收 `component_id` 不是名字（先用 `get_component` 换 id）；工具参数规范名是下划线、也接受等价连字符 alias；除 ELF / Native 外，多数 `search_*` 的 `total` 只是当前页数量，总量统计用 `sql` / `list_entities`。

### 4.4 对比与复杂 SQL

```bash
python3 $CLI --db a.db --db b.db diff --entity components
python3 $CLI --db $DB diff --entity gn_args --scan-a 1 --scan-b 2
python3 $CLI --db $DB sql --file query.sql     # - 表示 stdin
python3 $CLI --db $DB sql --sql "SELECT COUNT(*) AS n FROM components"
```

`--db` 给两次是跨库；给一次加 `--scan-a/--scan-b` 是同库两快照，这两个参数写在
`diff` 后面。多行 SQL 走 `--file`（可带注释）。只读校验要求第一个关键字为
SELECT/WITH，表名走白名单；执行用当前快照私有内存副本，默认 1000 行、`truncated` 与 5 秒超时，详见 `references/spec/query.md`。

### 4.5 判断经验：容易误读的六处

**这是启发式，不是硬规则**——它说的是"看到这个现象先怀疑什么"；硬约束在 §5。

1. **空值有好几种含义。** 无实现 `.so` 时看 `implementation_kind`：`type_only`
   不需要、`arkts_builtin` 由运行时提供、`unknown` 才是真不知道。
2. **引用条数 ≠ 对端数量。** 同一模块可能在多个条件分支被 import；看去重后的
   模块列表，不把 evidence 行数当成员数。
3. **Kit 成员有两条来路且会不一致。** `@kit` 标签 vs 入口 import；分别报告
   `declared_only`、`referenced_only` 与 `both`，不要只给合计。
4. **依赖闭包从 1 跳起。** 先看 `total` 与 `truncated`；需要更深闭包时显式提高
   `max_distance`，不要把截断条数当闭包规模。
5. **`out_of_scope` 不是缺陷。** 未解析的引用可能本来就指向外部包。
6. **快照不是现状。** `content_match` 恒为 `unverified`，提交号是扫描当时的。

（`cpu_arch` 决定路径根见 §4.2；`install_targets` 与 `.img` 的区别见 §5。）

## 5. 禁止做法（Prohibited Practices）

这些是**硬约束**（必须/不得），不是建议；每条都写上违反后的具体后果。

- **不要对任意缺失的 `--db` 路径自动下载。** 只有显式 `bootstrap.py install` /
  `refresh` 才联网——查询路径静默联网会把一次秒回问答变成几十秒下载，离线时直接失败。
- **不得用 `elf_modules=0` 的库回答依赖问题，也不得编造数量。** 计数为 0 是
  "该证据未采集"，不是"没有依赖"；把两者混起来会给出一个看起来精确、
  实际无依据的影响面。
- **`install_targets` 不是实际 `.img` 数。** 它是安装落点（一个组件文件一条），
  一个 `.img` 里可能有几百条；用户问镜像数量时必须另行实测 `.img` 数量，并说明两者区别。
- **不得把配置记录当成运行态。** 服务/SA/HDI 的 `cfg` 是扫描时的**声明**，
  进程可能根本没起来；直接当成"当前在跑什么"会给出无法证伪的结论。
- **不得用裸名字猜实现路径。** `arm` 走 `system/lib/`、`arm64` 走
  `system/lib64/`，同名的库可能两份都在；以 DB 里的真实 `dest` 为准，
  否则 `owner_of` / `elf_dependencies` 会打空或打错。
- **不得修改 `knowledge.db` 或 SDK 源码去"凑"一个证据。** 库是审计对象，
  改它等于伪造证据；要新数据就重扫并重装。
- **不得加载 maintainer 设计/打包文档来回答产品架构问题。** 那些文档讲的是
  代码怎么组织，不含产品事实，加载它们只会引入与问题无关的噪声。

## 6. 异常与回退（Exceptions and Fallbacks）

退出码：`0` 正常 · `2` 参数错 · `3` 库打不开 · `5` 工具返回 error（JSON 到 stderr）；
默认 JSON（可 `| jq`），`--format table` 给人读。**遇到失败先停手，不要换个库或
编个数交差**：库打不开、快照不完整、工具报错、`elf_modules=0`、`truncated=true`、
SDK 源码缺失、跨快照对不上这七种情形的判据，以及下载/`.env`/解压排错，见
`references/usage.md` 的「查询故障与回退」。

## 7. 参考文件（References）

按问题只读**所需那一份**；参数枚举优先跑对应命令的 `--help`。不确定读哪份时先看
`references/spec/README.md`（14 份规格的索引与逐模块工具数）。

| 当前问题 | 读这个 |
|---|---|
| 部件归属、依赖、影响面、SysCap、InnerAPI | `references/spec/component.md` |
| SDK 模块、Kit、ArkTS 声明或实现 | `references/spec/arkts.md` |
| ELF 依赖、反向依赖或库影响面 | `references/spec/elf.md` |
| Native SDK 库和头文件映射 | `references/spec/native.md` |
| 服务 / SA / HDI | `references/spec/service.md`、`sa.md`、`hdi.md` |
| GN 参数和特性 | `references/spec/gn_args.md` |
| 代码仓 / 镜像安装落点 | `references/spec/repos.md`、`install.md` |
| 扫描质量问题（`list_issues`） | `references/spec/issues.md` |
| 通用列表、聚合、复杂 SQL | `references/spec/query.md`、`schema.md`（**写复杂 SQL 前必须读完两份**） |
| 会话与快照语义（`--scan-id`、`diff --scan-a/b`） | `references/spec/session.md` |
| 安装、整体功能与 CLI 用法（人读） | `references/usage.md` |
| 45 个查询工具的一行索引（自动生成，勿手改；会话类 7 个由 `--db`/`--scan-id`/`diff` 代替） | `references/tools.md` |
| 照着 CLI 查询流程走一遍 | `examples/architecture-trace.md`、`complex-sql.md`、`query-parts-by-subsystem.sql` |
| 下载/安装评估、上库清单与最终报告 | `evals/evals.json`、`release-checklist.md`、`with-skill-report.md`、`without-skill-report.md`、`skill-judge-report.md` |

**Do NOT load** 未命中上表的规格。
