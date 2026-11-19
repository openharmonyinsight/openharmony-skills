# evals —— 这套评估怎么跑、跑出来的是什么

本目录里的每一份报告都对应一次**真实执行**：命令是真的跑了，输出是真的贴了，
断言是真的判了。这里说明怎么复现，以及每种产物到底是什么。

## 目录内容

| 路径 | 是什么 |
|---|---|
| `evals.json` | 8 个场景的用户请求、期望结果与断言（评估的**规格**） |
| `run_evals.py` | 评估执行器：搭夹具、跑命令/跑 agent、判自动断言、写转录 |
| `runs/scripted/` | 脚本臂转录：按 `SKILL.md` 写死的命令逐条真跑 |
| `runs/with-skill/` | with-skill 臂转录：真起一个 agent，`CODEX_HOME` 里装好本 skill |
| `runs/without-skill/` | without-skill 臂转录：真起一个 agent，只给工具代码、不给任何文档 |
| `runs/live-smoke.md` | 真连 CI 端点装一次运行时并查询（含 `references/tools.md` 与 CLI 的一致性校对） |
| `with-skill-report.md` | with-skill 最终评估报告 |
| `without-skill-report.md` | without-skill 基线报告与差异分析 |
| `skill-judge-report.md` | 按 `skill-judge` 协议做的设计质量评分 |
| `release-checklist.md` | 上库前置检查清单（逐项给证据） |

## 三个执行臂

同一个场景、同一套夹具，唯一区别是**执行者手上有什么**：

- **scripted**：执行器按 `SKILL.md` 规定的命令逐条执行。它证明"文档里写的命令
  真的能跑通"，是确定性复现的锚点。
- **with-skill**：起一个独立的 `codex exec` 进程，临时 `CODEX_HOME` 里装着本 skill
  （`SKILL.md` + `references/` + `examples/` + 运行时代码），**不给** `evals/`，
  避免把期望答案喂给被测 agent。
- **without-skill**：同样起一个独立 agent，但工作区里只有 `bootstrap.py` 与
  `oskm_runtime/` 代码，没有任何 skill 文档。它衡量的是"没有这份知识增量时，
  agent 靠读代码能走到哪一步"。

两个 agent 臂用**同一段任务描述**（`evals.json` 的 `prompt`）和同一份环境事实，
差别只有文档有无；转录里会记录 agent 执行的每条命令、是否读过 skill 文档、
token 用量，便于事后审计（包括"with-skill 臂是否真的触发了 skill"）。

## 怎么跑

依赖：

- Python 3.10+（验收用 3.12）
- oskm 源码树（夹具要用 `oskm_testing.fixture` 造合成库、用
  `cli/scripts/build_cli.py` 构建真 `oskm-cli.pyz`）。默认从本文件向上探测
  `packages/oskm`，也可用 `OSKM_SOURCE_ROOT=<packages/oskm>` 指定。
- agent 臂还需要 `codex` CLI，以及一份可用的 codex 配置（默认读
  `~/.codex/config.toml`，只取 model / provider 段生成一份**隔离**配置；
  也可用 `--codex-config` 指定）。

```bash
cd packages/oskm/skills/ohos-design-architecture-evidence-query

python3.12 evals/run_evals.py --arm scripted                      # 约 5 秒
python3.12 evals/run_evals.py --arm with-skill    --jobs 4         # 约 10–20 分钟
python3.12 evals/run_evals.py --arm without-skill --jobs 4         # 约 10–20 分钟
python3.12 evals/run_evals.py --arm with-skill --only 4            # 只跑一个场景
python3.12 evals/run_evals.py --live-smoke --live-date 20261116     # 真连端点
```

退出码：全部场景通过为 `0`，否则 `1`。转录写在 `evals/runs/<arm>/`，
汇总写在 `evals/runs/<arm>/summary.json`。

## 夹具做了什么

- 起一个只监听 `127.0.0.1` 的本地 HTTP 服务，扮演两种 CI 端点：
  `OPENHARMONY_CI`（POST 构建列表 → GET `obsPath` 归档）与
  `INTERNAL_CI`（GET `<endpoint>/<date>`）；每次请求都记进
  `server-requests.jsonl`，所以"发了几次请求、请求体长什么样"是可判定的事实。
- 用 `oskm_testing.fixture.create_fixture_db` 造 `product=synthetic` 的合成
  `knowledge.db`，用 `cli/scripts/build_cli.py` 构建真 `oskm-cli.pyz`，
  两者打进 `knowledge.tar.gz`（含 `interface/sdk-js`、`interface/sdk_c`）。
- 另备一个损坏归档（`knowledge.db` 不是 SQLite）和一个"完整 OpenHarmony 源码根"
  （`.gn` + 两套非空 SDK + `out/<product>/oskm/knowledge.db` + `cli/dist/oskm-cli.pyz`）。

隔离措施：每个场景独立工作区与独立服务端；子进程的 `HOME` / `CODEX_HOME`
指向临时目录，`OSKM_*` 环境变量只由场景显式声明——**不会**读写开发者自己的
`~/.oskm`，也不会访问真实网络（`--live-smoke` 除外）。

## 判定规则

- **auto 断言**：执行器直接判定，判据是文件系统状态、状态文件内容、sha256、
  服务端请求日志、退出码与命令输出。场景 PASS 当且仅当其全部 auto 断言通过。
- **人工断言**（转录里标 `人工`）：需要读语义的项（例如"是否如实报告失败"），
  由评审人对照转录判定，结论写进 `with-skill-report.md` /
  `without-skill-report.md`。

`evals.json` 里的断言是规格；执行器里的 auto 断言是它的可机检子集，
两者一起构成"这个场景算过"的完整定义。
