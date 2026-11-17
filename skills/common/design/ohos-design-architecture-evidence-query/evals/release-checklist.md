# 上库清单（3.1.0）

- Skill：`ohos-design-architecture-evidence-query`
- 版本：3.1.0（`metadata.status=trial`）
- 目标仓/分支：`openharmonyinsight/openharmony-skills` → `release`
- 目标目录：`skills/common/design/ohos-design-architecture-evidence-query/`
- 检查日期：2026-11-17
- 被检查的代码基线：**源码仓工作树全量**（`2b6b1eb` + 本次 3.1.0 交付件 + 并行工作流的
  CLI/references 改动），冻结快照 `/tmp/oskm-release-3.1.0-full`；三个评估臂与三套单元
  测试都跑在这一份快照上
- 发布归档：`ohos-design-architecture-evidence-query-3.1.0.tar.gz`
  - 评估时摘要：`217105efaa115da8c7ffd86ced0c1a558890d91de2bef1b0ff11caed2bc5e66c`
    （232,612 B / 79 tar 条目 / 70 文件 / 解压后 961,921 B）
  - 写入本报告与 `skill-judge-report.md` 后重建的最终摘要：见 `dist/SHA256SUMS`
  - 连续两次构建摘要一致（确定性构建）

## A. `openharmony-skills` 主分支 README「入库检查清单」

| # | 检查项 | 结果 | 证据 |
|---:|---|---|---|
| 1 | Skill name 全局唯一 | Pass | 目标仓 `release`/`main` 两分支内 grep 无同名 skill；公开网络精确检索 `"ohos-design-architecture-evidence-query"` 无其它命中 |
| 2 | 符合 `ohos-<stage>-<domain>-<capability>` | Pass | `ohos` / `design` / `architecture` / `evidence-query` |
| 3 | capability 是动名词或名词短语 | Pass | `evidence-query`（证据查询），非 `query`/`style` 这类宽泛单词 |
| 4 | 目录名与 `SKILL.md` 的 `name` 一致 | Pass | 均为 `ohos-design-architecture-evidence-query`；PyYAML 解析核对 `name == 目录名` → True |
| 5 | 有效 YAML Front Matter | Pass | `skill-creator/scripts/quick_validate.py` → `Skill is valid!`；PyYAML 解析成功 |
| 6 | description 说明触发场景 | Pass | 151 字符，覆盖"安装/更新运行时"与"询问产品顶层架构证据"两类触发，并列出子系统/部件/代码仓/镜像归属/影响面/SysCap/InnerAPI/SDK 接口/GN 开关与只读边界 |
| 7 | 包含 eval 用例 | Pass | `evals/evals.json`：8 场景 / 29 条断言（21 contains + 8 llm_judge）；执行器 `evals/run_evals.py` |
| 8 | with skill 评估全部通过 | Pass | `with-skill-report.md`：8/8 场景、自动断言 52/52、人工断言 4/4、8/8 场景触发 skill |
| 9 | 上传 with/without 最终评估报告 | Pass | `with-skill-report.md`、`without-skill-report.md`（基线 7/8，E2 失败原因与请求日志逐条列出） |
| 10 | skill-judge 达到 B 级或以上 | Pass | `skill-judge-report.md`：110/120（91.7%），A 级；D1/D4/D8 均达发布门槛 |

## B. `release` 分支《命名空间与目录放置规范》检查清单

| # | 检查项 | 结果 | 证据 |
|---:|---|---|---|
| 1 | name 唯一且符合 `ohos-<stage>-<domain>-<capability>` | Pass | 同 A.1、A.2 |
| 2 | capability 是动名词/名词短语 | Pass | 同 A.3 |
| 3 | 目录名与 `SKILL.md` 的 name 一致 | Pass | 同 A.4 |
| 4 | 放入正确的 common/domain 目录 | Pass | `skills/common/design/`：跨子系统的产品架构证据查询，不绑定单一框架/子系统（规范 §4） |
| 5 | 有效 YAML Front Matter | Pass | 同 A.5 |
| 6 | description 说明触发场景 | Pass | 同 A.6 |
| 7 | 元数据字段与目录和 name 一致 | Pass | `metadata.scope=common`（=一级命名空间）、`stage=design`（=阶段目录）、`domain=architecture`、`capability=evidence-query`（=name 中的两段）、`author=openharmony`、`version=3.1.0`、`status=trial`；顶层只有 `name`/`description`/`metadata` |
| 8 | 网站展示元数据 | Pass | `metadata/website/skills/ohos-design-architecture-evidence-query.yaml`（`schemaVersion: 1`，`category`/`status` 与 `SKILL.md` 一致，PyYAML 解析通过） |
| 9 | 阶段目录名用完整名称 | Pass | 目录为 `design`（规范 §7：`design` 阶段目录名即 `design`） |

## C. 入库要求（主分支 README「入库要求」1–5）

| # | 要求 | 结果 | 证据 |
|---:|---|---|---|
| 1 | skill-judge ≥ B | Pass | A 级 110/120，见 `skill-judge-report.md` |
| 2 | eval 用例随 skill 提交（输入/预期/评估方式） | Pass | `evals/evals.json`（输入=8 段用户请求，预期=`expected_output`，评估方式=29 条断言 + `runner` 说明）；`evals/README.md` 说明三臂与判定规则 |
| 3 | with skill 全部通过 | Pass | 8/8 场景，自动断言 52/52，人工断言 4/4，8/8 场景触发 skill（E1 因守卫误判单独重跑一次，`summary.json` 的 `partial_reruns` 有记录） |
| 4 | 同时跑 with / without skill | Pass | 同一份快照、同一段任务描述、同一套夹具；两臂各 8 个隔离 `codex exec` 进程。with-skill 2,210s / 168 命令 / 2,953,456 tokens；基线 3,022s / 219 命令 / 4,824,760 tokens（+63.3%） |
| 5 | 上传两份最终报告（含用例结果、通过情况、关键差异） | Pass | `with-skill-report.md` §2/§4、`without-skill-report.md` §2/§3/§4（含 token、耗时、命令数、探测请求数对比，以及基线在上一轮 E2 违约的稳定性证据） |

## D. 交付件与包内容自检

| 检查 | 结果 | 证据 |
|---|---|---|
| 归档不含查询引擎/表定义/采集器 | Pass | `test_the_query_engine_is_not_bundled` 门禁 + `tar -tzf` 核对：无 `oskm_cli/`、`oskm_schema/`、`oskm/`、`.pyz`、`.db` |
| 归档不含测试、构建脚本、缓存、真实 `.env` | Pass | `tar -tzf` 无 `tests/`、`scripts/`、`dist/`、`__pycache__`、`.env` |
| 归档只含一个包根目录 | Pass | `test_archive_has_exactly_one_package_root`；`tar -tzf` 全部条目以 `ohos-design-architecture-evidence-query/` 开头 |
| 参考文件无孤儿 | Pass | 脚本核对：`references/`、`examples/`、`evals/` 下的 `.md` 全部在 `SKILL.md` §7 登记 |
| 评估证据是真跑出来的 | Pass | `evals/runs/{scripted,with-skill,without-skill}/` 共 24 份转录 + 3 份 `summary.json` + `live-smoke.md`；每份含命令、stdout/stderr、退出码、请求归因、agent 命令审计与 token 用量 |
| 评估不冻结业务数据 | Pass | `test_eval_does_not_freeze_product_data`；合成库 `product=synthetic`；真实产品数据只出现在 `runs/live-smoke.md` 的实测记录里 |
| 源码级回归 | Pass | skill 215 passed；CLI 199 passed（70 skipped）；oskm 301 passed（25 skipped） |

## E. 本次发布相对 3.0.1 的改动

1. frontmatter 补齐 `openharmony-skills` `release` 分支要求的治理元数据
   （`author=openharmony`、`scope`、`stage`、`domain`、`capability`、`status`），版本 3.0.1 → 3.1.0。
2. 正文行数预算改为只数正文（≤175 行，当前 172 行）：治理元数据不是给 Agent 读的指令。
3. `SKILL.md` §7 修正 `references/tools.md` 的描述：索引列 45 个查询工具，
   会话类 7 个由 `--db`/`--scan-id`/`diff` 代替（`ask --list` 合计 52 个）。
4. 新增 `evals/run_evals.py` 三臂评估执行器 + `evals/README.md`；
   `evals/runs/` 存真跑转录；两份报告与 judge 报告全部按本轮实测重写。
5. 新增 `LICENSE`（Apache-2.0，与目标仓其它 skill 一致）。
6. 本次发布同时带上并行工作流对 `references/` 的澄清（8 份文档，+187/−52 行）：
   工具参数的连字符 alias、`owner_of`/`get_install_module` 的 `AMBIGUOUS` 语义、
   `arch runtime` 是模糊搜索、多数 `search_*` 的 `total` 只是当前页数量、
   只读 SQL 是"复制当前 scan 的白名单表到私有内存快照后执行"（不是文本注入
   `scan_id`/`LIMIT`）、Python 3.10+ 与 `python3.12` 提示。运行时代码
   （`bootstrap.py` / `oskm_runtime/`）未变，因此运行时分发类 eval 的判据不受影响；
   三个臂与 live-smoke 都在带上这些改动后的快照上重跑过。
