# Without Skill 基线报告

- 对照对象：`evals/evals.json` 的 8 个场景（与 with-skill 臂**逐字相同**的任务描述与环境事实）
- 评估日期：2026-11-17 16:18–16:37（+08:00）
- 代码基线：与 with-skill 臂同一份快照 `/tmp/oskm-release-3.1.0-full`
  （源码仓工作树全量：`2b6b1eb` + 3.1.0 交付件 + 并行工作流的 CLI/references 改动）
- 执行环境：macOS 27.2.1（arm64）· Python 3.12.16 · codex-cli 0.169.0 ·
  模型 `qwen3.8-max`（`model_reasoning_effort=high`）
- 执行方式：`python3.12 evals/run_evals.py --arm without-skill --jobs 3 --timeout 1200`
- 结论：**8/8 场景通过，自动断言 52/52；但成本显著更高，且上一轮同一基线在 E2 违约**

## 1. 基线定义（这一臂手上有什么、没有什么）

| 有 | 没有 |
|---|---|
| 与 with-skill 臂相同的任务描述、夹具、端点、Python 解释器 | `SKILL.md` |
| 工具**代码**：`bootstrap.py` + `oskm_runtime/`（放在 `<ws>/tool/`） | `references/`（usage.md、tools.md、14 份 spec） |
| 一个隔离的临时 `HOME` / `CODEX_HOME`（**不装任何 skill**） | `examples/`、`README.md`、`evals/` |

也就是说：基线不是"什么都没有"，而是"只有代码、没有知识"。它回答的问题是——
一个有源码可读的强 agent，能不能自己把这套运行时分发契约推导出来，代价是多少。

审计手段（写在每份转录里）：

- agent 执行的每条命令都从 `codex exec --json` 事件流里抽出来列进转录；
- **越界守卫**：命中 `/Users/**`（宿主源码仓）、别的评估工作区、或命令位上的
  `ps`/`pgrep`/`lsof` 宿主进程探测即判该场景不通过。本轮 8/8 场景 `outside=0`；
- 请求归因：夹具服务端记录 `User-Agent`，只有 `Python-urllib/*`（工具自己）算契约请求，
  agent 自己起的 `curl` 探测单独计数。

> 更早一版（2.5.6）基线连工具代码都不给，结果 0/8；那种基线只能证明"没代码跑不起来"，
> 证明不了知识增量。本版把代码给足，基线因此变强——结论也更可信。

## 2. 场景结果

| ID | 场景 | 自动断言 | 人工断言 | 工具请求 | agent 探测 | agent 耗时 | 命令数 | tokens(in+out) | 结论 |
|---:|---|---|---|---:|---:|---:|---:|---:|---|
| E1 | first-install-complete-archive | 9/9 | – | 1 | 1 | 320.1s | 25 | 509,365 | Pass |
| E2 | openharmony-exact-date | 9/9 | – | 4 | **20** | **711.4s** | 38 | **1,049,265** | Pass |
| E3 | internal-exact-date | 6/6 | – | 1 | 1 | 178.0s | 21 | 286,286 | Pass |
| E4 | invalid-archive-preserves-runtime | 5/5 | 1 通过 | 3 | 2 | 279.1s | 25 | 535,850 | Pass |
| E5 | local-source-runtime-preferred | 8/8 | – | 0 | 0 | 263.5s | 28 | 638,512 | Pass |
| E6 | cli-resolution-chain | 4/4 | 1 通过 | 0 | 0 | 420.9s | 22 | 454,219 | Pass |
| E7 | refresh-is-explicit | 6/6 | 1 通过 | 2 | 0 | 523.7s | 32 | 806,031 | Pass |
| E8 | synthetic-database-smoke | 5/5 | 1 通过 | 0 | 0 | 324.8s | 28 | 545,232 | Pass |
| 合计 | 8 场景 | **52/52** | **4/4** | 11 | 24 | 3,022s | 219 | 4,824,760 | **8/8 PASS** |

转录：`runs/without-skill/NN-<name>.md`；汇总：`runs/without-skill/summary.json`。

> E6 转录里「命中 skill 文档字样：是」是**误报**，已逐条核对事件流：那是夹具自己造的
> 源码树候选 `<ws>/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py`
> （`_copy_tool()` 只复制 `bootstrap.py` 与 `oskm_runtime/`，目录里没有任何文档）。
> 8/8 场景没有任何一条命令读到过 `SKILL.md` / `references/` / `examples/`。

## 3. 与 with-skill 臂的差异

| 指标 | with-skill | without-skill | 差异 |
|---|---:|---:|---|
| 场景通过 | 8/8 | 8/8 | 持平 |
| 自动断言 | 52/52 | 52/52 | 持平 |
| agent 总耗时 | 2,210s | 3,022s | **+36.7%** |
| 执行命令数 | 168 | 219 | **+30.4%** |
| tokens(in+out) | 2,953,456 | 4,824,760 | **+63.3%** |
| agent 自发探测请求（curl） | 3 | 24 | **8×** |
| 单场景最贵 | E7 569,092 tokens | E2 1,049,265 tokens | – |
| 达到结论的方式 | 读 `SKILL.md` + 按需读 1–2 份 spec | 读 `oskm_runtime/*.py` 源码、给 `_open` 套 in-process spy 抓包、`grep` pyz 内 45 个 `.py` 找网络调用、20 次 curl 对照实验 |

基线**确实**把契约推导出来了（这是它 8/8 的原因），但代价与风险是实打实的：

- **E2**：为确认"日期到底怎么进请求"，基线用 curl 打了 20 次对照实验（含裸端点、
  错误日期、`INTERNAL_CI` 规则套 `OPENHARMONY_CI` 端点），耗时 711.4s、
  1,049,265 tokens；with-skill 臂同场景 352.2s、428,585 tokens，直接照 §4.1 做。
- **E7**：为证明"查询不联网"，基线把 `oskm-cli.pyz` 里 45 个 `.py` 全量 grep
  `urllib.request`/`http.client`/`socket.`/`subprocess`，并读 `needs_refresh()` 源码；
  with-skill 臂引用 §5 的硬约束 + 一次死端点实测即得。
- **推导会产生真实副作用**：基线的 24 次探测请求在真实 CI 上就是 24 次无意义调用；
  E4 基线用了 3 次工具请求（with-skill 2 次）。
- **结论依赖"这套代码此刻长什么样"**：源码一改，推导要重来；skill 给的是契约与判据。

## 4. 基线的稳定性：同一基线上一轮在 E2 违约

同一份 harness、同一个模型，15:33 那一轮（代码基线为 `2b6b1eb` + 3.1.0 交付件，
不含并行工作流的文档澄清）基线是 **7/8**，E2 失败：

| # | 方法 | 路径 | POST 的 startTime |
|---:|---|---|---|
| 5–6 | POST / GET | `/openharmony/obs/**20261101**/knowledge.tar.gz` | `2026110100000000` |
| **7** | **GET** | **`/openharmony/api/daily_build/build/list/component/20261102`** | – |
| 12–13 | POST / GET | `/openharmony/obs/**20261103**/knowledge.tar.gz` | `2026110300000000` |

两类偏差：① 用相邻日期穷举去确认语义；② 把 `INTERNAL_CI` 的 `<endpoint>/<date>`
规则套到 `OPENHARMONY_CI` 的列表端点上（第 7 条）。第 7 条正是本轮判定所依据的
契约断言抓到的——**同一条断言，基线在一轮里违约、在另一轮里合规**，而 with-skill
臂在两轮里都合规。这说明契约细节靠推导得到时是**不稳定**的，靠 skill 才是稳定的。

## 5. 两臂都答对的部分（不是 skill 独有的价值）

安装原子性与回滚（E4）、源码树优先与 sha256 一致（E5）、CLI 三级候选与失败提示（E6）、
自管库不被接管（E7，基线还额外实测出"显式 `install` 会接管该目录"这个例外）、
合成库组合烟测（E8）。这些都能从代码里读出来，skill 的作用是让 agent 不必每次重读。

## 6. 结论

- 本轮基线 8/8、with-skill 8/8：**在"有源码可读"的前提下，通过/不通过已经区分不出
  两者**；区分度在成本（+63.3% tokens、+36.7% 耗时、+30.4% 命令、8× 探测）与
  稳定性（上一轮基线 E2 违约，with-skill 两轮均合规）。
- skill 的知识增量因此应这样陈述：**不是"没有它就做不成"，而是"没有它每次都要重做
  一遍逆向工程，且更容易在契约细节上违约"**。这个结论由两臂的转录、请求日志与
  token 计数支撑，可复核。
- 真正只来自 skill、代码里读不出来的部分是判断经验：`degraded` ≠ 失败、
  `elf_modules=0` ≠ 没有依赖、`install_targets` ≠ `.img` 数、快照不是现状。
  基线在 E7/E8 也说对了一部分，但都是"这次读代码 + 做实验读出来的"。
