# With Skill 评估报告

- 评估对象：`ohos-design-architecture-evidence-query` **3.1.0**（发布包内容：`SKILL.md` +
  `references/` + `examples/` + `bootstrap.py` + `oskm_runtime/`）
- 评估日期：2026-11-17 16:18–16:43（+08:00）
- 被评估代码基线：**源码仓工作树全量**（`2b6b1eb` + 本次 3.1.0 交付件 + 并行工作流的
  CLI/references 改动），冻结在快照 `/tmp/oskm-release-3.1.0-full`；三个臂与三套单元
  测试都跑在这一份快照上，`summary.json` 里记录了它的绝对路径
- 执行环境：macOS 27.2.1（arm64）· Python 3.12.16 · codex-cli 0.169.0 ·
  模型 `qwen3.8-max`（`model_reasoning_effort=high`）
- 夹具：合成 `knowledge.db`（`product=synthetic`，sha256 `f561e39f648cfd6b…`）+
  真构建的 `oskm-cli.pyz`（84,742 B，sha256 `3e78cf73a94bcf9d…`）+ 本地 HTTP 端点
- 执行方式：`python3.12 evals/run_evals.py --arm with-skill --jobs 3 --timeout 1200`
- 结论：**8/8 场景通过，自动断言 52/52 全过，人工断言 4/4 判定通过**

## 1. 这一臂到底怎么跑的

- skill 以**发布包内容**装进本次评估专用的临时 `$CODEX_HOME/skills/ohos-design-architecture-evidence-query/`，
  **不含 `evals/`**——期望答案不能喂给被测 agent。
- 每个场景一个隔离工作区 + 一个只监听 `127.0.0.1` 的夹具 HTTP 端点（扮演
  `OPENHARMONY_CI` 与 `INTERNAL_CI`），每次请求连 `User-Agent` 一起记进日志，
  所以"工具发了几次请求、请求体长什么样"是可判定的事实。
- 子进程的 `HOME` / `CODEX_HOME` 指向临时目录，`OSKM_*` 只由场景显式声明：
  全程不读写开发者自己的 `~/.oskm`，除 `--live-smoke` 外不访问真实网络。
- 每个场景起一个独立的 `codex exec` 进程（`--json` 事件流 + `-o agent-last-message.md`），
  任务描述取自 `evals.json` 的 `prompt`，与 without-skill 臂**逐字一致**。
- 越界守卫：agent 执行过的命令里若出现 `/Users/**`（宿主源码仓）、别的评估工作区，
  或命令位上的 `ps`/`pgrep`/`lsof` 宿主进程探测，该场景直接判不通过。
  本轮 8/8 场景 `outside=0`。

复现：

```bash
cd packages/oskm/skills/ohos-design-architecture-evidence-query
python3.12 evals/run_evals.py --arm with-skill --jobs 3 --timeout 1200
```

## 2. 场景结果

| ID | 场景 | 自动断言 | 人工断言 | 工具请求 | agent 耗时 | 命令数 | tokens(in+out) | 读了 skill 文档 | 结论 |
|---:|---|---|---|---:|---:|---:|---:|---|---|
| E1 | first-install-complete-archive | 9/9 | – | 1 | 165.7s | 16 | 264,808 | 是 | Pass |
| E2 | openharmony-exact-date | 9/9 | – | 7 | 352.2s | 22 | 428,585 | 是 | Pass |
| E3 | internal-exact-date | 6/6 | – | 1 | 187.5s | 18 | 227,937 | 是 | Pass |
| E4 | invalid-archive-preserves-runtime | 5/5 | 1 通过 | 2 | 291.9s | 26 | 497,368 | 是 | Pass |
| E5 | local-source-runtime-preferred | 8/8 | – | 0 | 249.2s | 19 | 301,576 | 是 | Pass |
| E6 | cli-resolution-chain | 4/4 | 1 通过 | 0 | 306.6s | 24 | 445,294 | 是 | Pass |
| E7 | refresh-is-explicit | 6/6 | 1 通过 | 1 | 415.5s | 26 | 569,092 | 是 | Pass |
| E8 | synthetic-database-smoke | 5/5 | 1 通过 | 0 | 241.2s | 17 | 218,796 | 是 | Pass |
| 合计 | 8 场景 | **52/52** | **4/4** | 12 | 2,210s | 168 | 2,953,456 | 8/8 | **8/8 PASS** |

逐场景转录（命令、stdout/stderr、退出码、请求归因、agent 命令审计、token 用量、断言表）：
`runs/with-skill/NN-<name>.md`；机器可读汇总：`runs/with-skill/summary.json`。

> E1 于 16:40 单独重跑一次（`summary.json` 的 `partial_reruns` 有记录）：首轮 E1 被
> 越界守卫误判——agent 把「没有用 ps/pgrep/lsof 反查宿主进程」写进 `answer.md` 的
> heredoc 正文，守卫把这段结论文字当成了命令。守卫改为先剥离 heredoc、且只在命令位
> 匹配探测词后重跑，9/9 通过。其余 7 个场景用的是 16:18–16:34 那一轮的结果，未重跑。

## 3. 人工断言判定（4 条）

| 场景 | 人工断言 | 判定 | 依据（转录原文） |
|---|---|---|---|
| E4 | 是否如实报告 refresh 失败（而不是宣称成功） | 通过 | 「`refresh --date 20261118` 失败…`错误: SQLite integrity_check 未通过: 文件头无效`」，并先自证夹具服务端确实返回 200/`application/gzip`/86,182 B，坏的是归档里的 DB；旧运行时逐文件 sha256 未变 |
| E6 | 解析顺序与失败提示是否与实现一致 | 通过 | 「`cli-path` 选 **第 1 级 `$OSKM_CLI`**…顺序固定为 `$OSKM_CLI`(env) → 源码树(source) → `<runtime-root>/oskm-cli.pyz`」，并用 `plain-tool` 与 `source-tree` 两个入口交叉实测 |
| E7 | 自管库（无状态文件）是否被正确说明为不刷新/不覆盖 | 通过 | 「夹具 `runtime/` 与 `unmanaged/` 一个字节都没动，`state date` 仍是 `20261116`」，并说明过期运行时上直接查询不下载、显式 `refresh` 才下载 |
| E8 | 是否明确说明该场景只验证组合链路、不代表真实产品数据 | 通过 | 「合成库 `counts.elf_modules=0`，按 skill 约束不据此回答依赖/影响面问题」；全程未 install、未联网、未创建 `~/.oskm` |

## 4. skill 起了什么作用（转录里的实证）

1. **触发率 8/8。** 每个场景的 agent 都主动读了 `$CODEX_HOME/skills/…/SKILL.md`
   （转录「读到 skill 文档：是」），并按 §7 路由表按需读 `references/usage.md`，
   不是一次性全量加载。
2. **一次走对下载契约。** E2 的 7 次工具请求全部落在「构建列表 POST（component 固定
   `dayu600_7885_ai`、`startTime=2026110200000000`/`endTime=20261102235959`）+ obs 归档 GET」
   两条路径上；E3 恒为 `GET <endpoint>/20261102`，没有退化成 `latest` 或系统当天。
3. **证据边界被当成硬约束执行。** E1/E7/E8 的 agent 都主动指出夹具库
   `elf_modules=0` 意味着「证据未采集」而不是「没有依赖」，并拒绝用它回答影响面问题
   ——这是 SKILL.md §4.5/§5 的判断经验。
4. **安装纪律。** E1 用绝对路径调用、安装前后 `pwd` 不变、`$HOME/.oskm` 未被创建；
   E4 损坏归档 refresh 失败后旧运行时逐字节未变、无残留临时目录；
   E5 源码树完整时工具零请求，装进来的 DB/CLI sha256 与源码树逐位相同；
   E7 过期运行时上直接查询零下载。
5. **成本。** 8 个场景合计 2,210s、168 条命令、2,953,456 tokens、3 次自发的 `curl` 探测；
   同一批任务在没有 skill 的基线臂是 3,022s、219 条命令、4,824,760 tokens、24 次探测。

## 5. 交叉验证（同一份快照、同一套夹具）

| 臂 | 结果 | 作用 |
|---|---|---|
| `scripted` | 8/8，自动断言 51/51，工具请求 5 次 | 按 `SKILL.md` 写死的命令逐条真跑，确定性复现锚点（`runs/scripted/`） |
| `with-skill`（本报告） | 8/8，自动断言 52/52 + 人工 4/4 | 上库要求的 with-skill 评估 |
| `without-skill` | 8/8，自动断言 52/52（成本显著更高，见基线报告） | 基线对照，`without-skill-report.md` |
| `--live-smoke` | 4/4（16:18） | 真连 `OPENHARMONY_CI` 装 `date=20261116`：339M 运行时、`product=wukong100`、`arch overview` 返回真实计数、`references/tools.md` 与 `ask --list --markdown` 逐行一致（`runs/live-smoke.md`） |

源码级回归（同一快照）：skill 测试 **215 passed**、CLI 测试 **199 passed（70 skipped）**、
oskm 测试 **301 passed（25 skipped）**。

## 6. 已知限制

- 人工断言由提交者对照转录判定，未做双人盲评；判定依据（agent 原话）已逐条贴在 §3。
- agent 臂绑定 `codex-cli 0.169.0` + `qwen3.8-max`；换宿主或换模型，agent 行为会变，
  但自动断言的判据是**文件状态、状态文件内容、sha256、夹具服务端请求日志、退出码**，
  与模型无关，因此结论可迁移。
- agent 行为有随机性：本轮 8/8；同一 skill 在上一轮（15:33，代码基线为
  `2b6b1eb` + 3.1.0 交付件）也是 8/8，但单场景耗时与请求次数会浮动
  （例如 E2 的工具请求数 4 → 7，都是契约内请求）。
- 夹具库是合成库（`product=synthetic`），业务数据不代表任何真实产品；真实端点与真实
  产品库的验证只在 `--live-smoke` 里做，且不冻结具体计数（`test_eval_does_not_freeze_product_data`
  门禁防止把业务数据写进 eval）。
- agent 为验证语义自行发起的 `curl` 探测（本臂 3 次）与工具自身请求分开统计，
  契约判定只算 `User-Agent: Python-urllib/*` 的那部分。
