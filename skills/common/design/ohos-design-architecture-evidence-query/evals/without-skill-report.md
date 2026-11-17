# Without Skill 基线报告

- 对照对象：`evals/evals.json` 的 8 个场景（与 with-skill 臂**逐字相同**的任务描述与环境事实）
- 评估日期：2026-11-17
- 代码基线：与 with-skill 臂同一份快照 `/tmp/oskm-release-3.1.0`
  （KnowledgeBase `2b6b1eb` + 3.1.0 改动）
- 执行环境：macOS 27.2.1（arm64）· Python 3.12.16 · codex-cli 0.169.0 ·
  模型 `qwen3.8-max`（`model_reasoning_effort=high`）
- 执行方式：`python3.12 evals/run_evals.py --arm without-skill --jobs 3 --timeout 1200`
- 结论：**7/8 场景通过，自动断言 51/52；E2 失败**

## 1. 基线定义（这一臂手上有什么、没有什么）

| 有 | 没有 |
|---|---|
| 与 with-skill 臂相同的任务描述、夹具、端点、Python 解释器 | `SKILL.md` |
| 工具**代码**：`bootstrap.py` + `oskm_runtime/`（放在 `<ws>/tool/`） | `references/`（usage.md、tools.md、14 份 spec） |
| 一个隔离的临时 `HOME` / `CODEX_HOME`（**不装任何 skill**） | `examples/`、`README.md`、`evals/` |

也就是说：基线不是"什么都没有"，而是"只有代码、没有知识"。它要回答的问题是——
一个有源码可读的强 agent，能不能自己把这套运行时分发契约推导出来，代价是多少。

审计手段（写在每份转录里）：

- agent 执行的每条命令都从 `codex exec --json` 事件流里抽出来列进转录；
- **越界守卫**：命中 `/Users/**`（宿主源码仓）、别的评估工作区、`ps`/`pgrep`/`lsof`
  宿主进程探测即判该场景不通过。本轮 8/8 场景 `outside=0`；
- 请求归因：夹具服务端记录 `User-Agent`，只有 `Python-urllib/*`（即工具自己）算契约请求。

> 上一版（2.5.6）基线不给工具代码，结果是 0/8；那种基线只能证明"没代码跑不起来"，
> 证明不了知识增量。本版把代码给足，代价是基线变强——结论也因此更可信。

## 2. 场景结果

| ID | 场景 | 自动断言 | 人工断言 | 工具请求 | agent 耗时 | 命令数 | tokens(in+out) | 结论 |
|---:|---|---|---|---:|---:|---:|---:|---|
| E1 | first-install-complete-archive | 9/9 | – | 1 | 210.6s | 20 | 319,624 | Pass |
| E2 | openharmony-exact-date | 8/9 | – | **13** | 462.1s | 27 | 701,248 | **Fail** |
| E3 | internal-exact-date | 6/6 | – | 1 | 200.2s | 21 | 325,817 | Pass |
| E4 | invalid-archive-preserves-runtime | 5/5 | 1 通过 | 3 | 357.0s | 22 | 678,176 | Pass |
| E5 | local-source-runtime-preferred | 8/8 | – | 0 | 320.2s | 24 | 520,135 | Pass |
| E6 | cli-resolution-chain | 4/4 | 1 通过 | 0 | 407.3s | 27 | 617,638 | Pass |
| E7 | refresh-is-explicit | 6/6 | 1 通过 | 2 | 560.1s | 39 | 978,278 | Pass |
| E8 | synthetic-database-smoke | 5/5 | 1 通过 | 0 | 426.0s | 29 | 745,649 | Pass |
| 合计 | 8 场景 | **51/52** | **4/4** | 20 | 2,944s | 209 | 4,886,565 | **7/8 PASS** |

转录：`runs/without-skill/NN-<name>.md`；汇总：`runs/without-skill/summary.json`。

> 说明：E6 转录里「命中 skill 文档字样：是（6 处）」是**误报**，已逐条核对事件流——
> 那是夹具自己造的源码树候选 `<ws>/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py`
> （`_copy_tool()` 只复制 `bootstrap.py` 与 `oskm_runtime/`，目录里没有任何文档）。
> 8/8 场景没有任何一条命令读到过 `SKILL.md` / `references/` / `examples/`。

## 3. 唯一失败的场景：E2 `openharmony-exact-date`

失败断言：**「工具的请求只落在『构建列表 POST + obs 归档 GET』两条路径上」**。

夹具服务端记录的 13 次工具请求（完整日志见转录）：

| # | 时间 | 方法 | 路径 | POST 的 startTime |
|---:|---|---|---|---|
| 1–2 | 15:35:34 | POST / GET | `…/build/list/component` → `/openharmony/obs/20261102/knowledge.tar.gz` | `2026110200000000` |
| 3–4 | 15:36:47 | POST / GET | 同上（重复一次安装） | `2026110200000000` |
| 5–6 | 15:37:30 | POST / GET | `/openharmony/obs/**20261101**/knowledge.tar.gz` | `2026110100000000` |
| **7** | 15:37:30 | **GET** | **`/openharmony/api/daily_build/build/list/component/20261102`** | – |
| 8–9 | 15:37:59 | POST / GET | `/openharmony/obs/**20261101**/…` | `2026110100000000` |
| 10–11 | 15:37:59 | POST / GET | `/openharmony/obs/20261102/…` | `2026110200000000` |
| 12–13 | 15:37:59 | POST / GET | `/openharmony/obs/**20261103**/…` | `2026110300000000` |

问题不是"多跑了几次安装"（那不算违约），而是两类真实偏差：

1. **试相邻日期**：`20261101`、`20261103` 各来一轮——在没有"日期即窗口、
   `startTime=<date>00000000`/`endTime=<date>235959`"这条知识时，agent 用穷举去确认语义。
2. **把两种下载方式的 URL 契约混起来**：第 7 条 `GET <endpoint>/20261102` 是
   `INTERNAL_CI` 的 URL 规则（`<endpoint>/<date>`）套在 `OPENHARMONY_CI` 的列表端点上——
   agent 自己在结论里也写了这次对照实验（"`INTERNAL_CI` 才是 `GET <endpoint>/<date>`
   (同一端点返回 404)"）。作为实验它是对的，作为工具契约它是一次不成立的请求。

同一场景 with-skill 臂只发了 4 次工具请求（两轮安装，全部落在契约路径上），
一次命中 `component=dayu600_7885_ai` 与精确日期窗口。

## 4. 与 with-skill 臂的差异

| 指标 | with-skill | without-skill | 差异 |
|---|---:|---:|---|
| 场景通过 | 8/8 | 7/8 | 基线在 E2 违约 |
| 自动断言 | 52/52 | 51/52 | – |
| agent 总耗时 | 2,624s | 2,944s | **+12.2%** |
| 执行命令数 | 179 | 209 | **+16.8%** |
| tokens(in+out) | 3,410,484 | 4,886,565 | **+43.3%** |
| 工具契约请求数 | 10 | 20 | **2×** |
| 达到同样结论的方式 | 读 `SKILL.md` + 按需读 1–2 份 spec | 读 `oskm_runtime/*.py` 源码、给 `_open` 套 in-process spy 抓包、`grep` pyz 里 45 个 `.py` 找网络调用 |

基线**确实**把大部分契约推导出来了（这是它 7/8 的原因），代价与风险是：

- 每个场景都要先做一遍"逆向工程"：E7 花了 978,278 tokens / 39 条命令，
  其中包括对 `oskm-cli.pyz` 内 45 个 `.py` 全量 grep `urlopen`/`http.client`/`socket.`/`subprocess`
  来证明"查询不联网"；with-skill 臂同场景 748,267 tokens / 33 条命令，直接引用 §5 的硬约束。
- 推导过程会产生真实副作用：E2 的相邻日期穷举与跨契约 URL 组合，在真实 CI 上就是
  无意义的构建列表查询与 404；E4 有 3 次工具请求（with-skill 2 次）。
- 结论依赖"这套代码此刻长什么样"：源码一改，推导要重来；skill 给的是契约与判据，
  不需要每次重读实现。

两臂都答对的部分（说明这些不是 skill 独有的价值，而是代码里能读出来的事实）：
安装原子性与回滚（E4）、源码树优先与 sha256 一致（E5）、CLI 三级候选与失败提示（E6）、
自管库不被接管（E7）、合成库组合烟测（E8）。

## 5. 结论

- 基线 7/8、with-skill 8/8：**skill 的直接收益是把 E2 这类"契约细节"从"读代码 + 试错"
  变成"照做就对"**，并把整体成本压低约 1/3 tokens、1/6 命令。
- 更重要的是可迁移的那部分知识：证据边界（`degraded` ≠ 失败、`elf_modules=0` ≠ 没有依赖、
  `install_targets` ≠ `.img` 数）、刷新必须显式、快照不是现状。基线在 E7/E8 也说对了一些，
  但都是"这次读代码读出来的"；skill 让它们成为每次都在的默认判断。
- 因此本 skill 的知识增量成立，但不是"没有它就做不成"，而是"没有它每次都要重做一遍
  逆向工程，且更容易在契约细节上违约"。这个结论由两臂的转录与请求日志支撑，可复核。
