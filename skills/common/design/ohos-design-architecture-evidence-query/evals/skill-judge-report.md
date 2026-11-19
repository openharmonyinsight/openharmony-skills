# Skill Evaluation Report: ohos-design-architecture-evidence-query

## Summary

- **Total Score**: 110/120 (91.7%)
- **Grade**: A
- **Pattern**: Navigation + Process（短路由入口 + 分阶段工作流）
- **Knowledge Ratio**: E:A:R = 78:20:2
- **Verdict**: 一个把"运行时分发"和"证据判读"两件事都写清楚的 skill：契约具体、
  反模式带后果、参考文件按问题路由；主要成本在参考资料体量（`usage.md` 646 行、
  `session.md` 352 行）与随包发布的评估证据（`evals/` 占包体 75%）。

- **评估日期**: 2026-11-17
- **评估对象**: 发布归档 `ohos-design-architecture-evidence-query-3.1.0.tar.gz`
  （由 `scripts/build_skill.py` 从冻结快照 `/tmp/oskm-release-3.1.0-full` 构建；
  快照 = 源码仓工作树全量，即 `2b6b1eb` + 本次 3.1.0 交付件 + 并行工作流的
  CLI/references 改动，与三个评估臂、三套单元测试用的是同一份代码）
- **归档 SHA-256**: `217105efaa115da8c7ffd86ced0c1a558890d91de2bef1b0ff11caed2bc5e66c`
  （232,612 bytes，79 个 tar 条目 / 70 个文件 / 961,921 bytes 解压后）
- **包内容摘要 digest**（排序后的路径+逐文件 sha256）:
  `ab9aee3939397f0e0f80785f5bd9f8e32652ffa21b67dca750066d7da9154429`
- **构建确定性**: 连续两次构建 SHA-256 相同（`dd4f8a94…`）
- **评估方法**: 按 `skill-judge` 的五步协议执行（知识增量扫描 → 结构分析 →
  逐维度打分 → 汇总定级 → 出报告）。这是**基于准则的评估**，不是独立的自动打分器；
  所有量化数字都来自下面「Validation Evidence」里可复跑的命令。
- **发布说明**: 本报告与 `release-checklist.md` 在评估之后写入 `evals/`，因此最终
  重建的归档摘要与上面这个"被评估摘要"不同；最终摘要记录在 `dist/SHA256SUMS`。
- **包范围**: 发布包不含查询引擎与 `knowledge.tar.gz`；它安装并说明那份独立分发的
  运行时与 CLI（`oskm-cli.pyz`）。

## Step 1 — 知识增量扫描（E/A/R）

| 章节 | 分类 | 依据 |
|---|---|---|
| §1 任务与边界 | **E** | 四件产物的运行时契约、"只装不查"的职责切分、快照语义（提交号是扫描当时的） |
| §2 触发信号 | **E/A** | 触发词含 `degraded`/`elf_modules=0`/`truncated`/`out_of_scope` 这类证据边界术语；同时承担激活作用 |
| §3 首要判断 | **E** | 固定判断顺序：`doctor` → `--db` 定位 → `get_scan_info` 看采集完整度 → 选入口；并明确"degraded 不等于失败，但对应计数为 0 时该查询不可用" |
| §4.1 安装与 CLI 入口 | **E** | CLI 固定名/不记版本/不锁摘要、源码树优先与 `--source-root`、`AGENT_CWD` 纪律、`knowledge.tar.gz` 是唯一发布单元 |
| §4.2 六类架构问题 | **E** | 问题类型 → `arch` 子命令映射；`cpu_arch` 决定 `system/lib/` 还是 `system/lib64/` |
| §4.3 `ask` | **E/A** | 宽搜索先行并报 `total`/`truncated`、数组参数空格分隔、`component_*` 收 id 不收名字、下划线规范名与连字符 alias、多数 `search_*` 的 `total` 只是当前页数量；命令语法本身属激活 |
| §4.4 `diff` / `sql` | **E** | 两个 `--db` 是跨库、一个 `--db` 加 `--scan-a/b` 是同库两快照、参数写在 `diff` 之后；只读校验、1000 行默认与 5 秒超时 |
| §4.5 判断经验六处 | **E** | 全是误读判据（空值多义、引用条数≠对端数量、Kit 两条来路、闭包从 1 跳起、`out_of_scope` 不是缺陷、快照不是现状） |
| §5 禁止做法 | **E** | 7 条硬约束，每条写明违反后的具体后果 |
| §6 异常与回退 | **E** | 退出码 0/2/3/5 语义 + 七种止损情形路由到 `references/usage.md` |
| §7 参考文件 | **A** | 路由表本身是激活；但"按问题只读所需那一份 + Do NOT load"是设计约束 |

比例估算 **E:A:R ≈ 78:20:2**。冗余部分主要是 bash 片段里模型本来就会的调用语法，
以及 §7 的表头文字；没有"什么是 SQLite / 什么是 ELF"这类科普段落。

## Step 2 — 结构分析

```text
frontmatter 顶层键      : name, description, metadata（无其它顶层键）
metadata                : author=openharmony, scope=common, stage=design,
                          domain=architecture, capability=evidence-query,
                          version=3.1.0, status=trial
name 与目录名一致        : True
description 长度         : 151 字符（含 WHAT / WHEN / 关键词 / 只读边界）
SKILL.md 行数            : 185（frontmatter 11 + 正文 172）
参考文件                 : references/ 17 份 2,987 行（usage.md 669、spec/session.md 352、
                          spec/component.md 318、spec/install.md 173、spec/service.md 161、
                          tools.md 55 自动生成）
示例                     : examples/ 3 份 130 行
运行时代码               : bootstrap.py 29 行 + oskm_runtime/ 10 文件 2,181 行
评估材料                 : evals/ 36 文件 12,508 行（含 24 份真跑转录 + 3 份 summary.json）
加载触发                 : §7 路由表按"当前问题 → 读这个"逐条给条件，并写明
                          "写复杂 SQL 前必须读完 query.md 与 schema.md"、
                          末尾一条 **Do NOT load** 未命中的规格
孤儿参考文件             : 0（脚本核对：所有 .md 都在 SKILL.md 里登记）
包体分布                 : evals/ 718,300B（74.7%）、references/ 118,427B（12.3%）、
                          oskm_runtime/ 84,948B（8.8%）、SKILL.md 12,219B（1.3%）
```

## Dimension Scores

| Dimension | Score | Max | Notes |
|-----------|-------:|-----:|-------|
| D1: Knowledge Delta | 18 | 20 | 专家内容占主体：四件产物契约、CLI 三级解析、证据降级与误读判据、快照边界。扣分点是 §4.2–§4.4 里仍夹着命令语法这类激活内容。 |
| D2: Mindset + Procedures | 14 | 15 | §3 给出"前一步不成立就别往后"的固定顺序，§4 按 `arch`/`ask`/`diff`/`sql` 分支；这些顺序都不是通用常识。扣分点：分支之间的取舍理由写得比顺序本身简略。 |
| D3: Anti-Pattern Quality | 14 | 15 | §5 七条硬约束每条都带后果（静默下载、`elf_modules=0`、`install_targets`≠`.img`、cfg≠运行态、裸名字猜路径、改库凑证据、加载维护者文档）；§4.5 六条误读判据。扣分点：少数反模式（如"不要改库"）后果描述偏原则化。 |
| D4: Specification Compliance | 15 | 15 | frontmatter 合法且顶层只有 `name`/`description`/`metadata`；治理字段齐备并与目录位置一致（`common/design`）；description 同时给出 WHAT、WHEN、触发关键词与只读排除项；`quick_validate.py` 输出 `Skill is valid!`。 |
| D5: Progressive Disclosure | 13 | 15 | 正文 172 行、路由表按问题分发、显式 Do NOT load；扣分点：`usage.md` 669 行、`session.md` 352 行、`component.md` 318 行，单份参考仍偏重；`evals/` 占包体 74.7%（Agent 不加载，但随包分发）。 |
| D6: Freedom Calibration | 14 | 15 | §4.5 明示"这是启发式"，§5 明示"这些是硬约束"，两类指令强度分得清；安装与证据判读用精确规则，查询构造留判断空间。扣分点：§4.3 的一段长句把多条约束挤在一起，强度层级不如 §5 清晰。 |
| D7: Pattern Recognition | 8 | 10 | Navigation + Process 混合：短路由入口 + 分阶段流程。扣分点：安装与查询两块都有一定体量，不是单一范式。 |
| D8: Practical Usability | 14 | 15 | 命令都实测可跑（`scripted` 臂 8/8、`with-skill` 臂 8/8）；退出码、七种止损情形、安装与查询排错都有回退路径；示例不冻结业务数据；本版还修掉了 `usage.md` 里"自动注入 scan_id 与 LIMIT"的旧描述（实际是复制当前 scan 的白名单表到私有内存快照后执行）。扣分点：`--format` 是全局参数这类易错点只在 §4.3 一句带过（评估中 agent 实测踩过）。 |

**Total = 18+14+14+15+13+14+8+14 = 110/120 = 91.7% → Grade A**

发布门槛核对（《实践指导书》§5.3）：`D1 ≥ 良好` ✓、`D4 ≥ 良好` ✓、`D8 ≥ 良好` ✓；
无任何维度存在需要单独说明的明显缺陷。上库要求为 B 级或以上 → **满足**。

## Critical Issues

无阻断项。

## Top 3 Improvements

1. **拆分 `references/usage.md`（669 行）。** 它同时承载安装、下载排错、CLI 用法、
   查询故障与构建说明。拆成"运行时安装"与"CLI 查询"两份可以进一步降低按需加载成本。
2. **压缩 `references/spec/session.md`（352 行）。** 其中大量工具在 CLI 里退化成
   `--db` / `--scan-id` / `diff` 参数，一张 CLI 等价表可以取代大部分生命周期描述。
3. **把 `llm_judge` 断言继续自动化。** `evals.json` 仍有 8 条 `llm_judge`；
   本轮已把可机检部分做成 `evals/run_evals.py` 的自动断言（52 条/臂）并加了越界守卫，
   剩下的是语义判定，可用带 rubric 的评审器进一步减少人工。

## Validation Evidence（都是本机真跑）

| 检查 | 命令 | 结果 |
|---|---|---|
| frontmatter 规则 | `skill-creator/scripts/quick_validate.py <pkg>` | `Skill is valid!` |
| frontmatter 解析 | PyYAML 解析 `SKILL.md` | 顶层键 `{name, description, metadata}`；`metadata` 七字段齐备 |
| 目录名一致 | `name == 目录名` | True |
| 归档内容 | `tar -tzf …-3.1.0.tar.gz` | 79 条目 / 70 文件；无 `.pyz`/`.db`/`.tar.gz`/`__pycache__`/`.env`/`tests`/`scripts`/`dist` |
| 构建确定性 | 连续两次 `build_skill.py` | SHA-256 相同 |
| 入口可用 | `python3.12 <pkg>/bootstrap.py --help` | rc=0，19 行输出，并明确"查询直接调 CLI" |
| 孤儿参考文件 | 脚本核对全部 `.md` 是否在 `SKILL.md` 登记 | 0 个孤儿 |
| evals 规格 | PyYAML/JSON 解析 `evals/evals.json` | 8 场景、29 条断言（21 contains + 8 llm_judge）、3 个执行臂 |
| scripted 臂 | `run_evals.py --arm scripted` | 8/8 场景、51/51 自动断言、工具请求 5 次 |
| with-skill 臂 | `run_evals.py --arm with-skill --jobs 3` | 8/8 场景、52/52 自动断言、4/4 人工断言、8/8 触发 skill；2,210s / 168 命令 / 2,953,456 tokens |
| without-skill 臂 | `run_evals.py --arm without-skill --jobs 3` | 8/8 场景、52/52 自动断言，但 3,022s / 219 命令 / 4,824,760 tokens（+63.3%）、24 次自发探测；上一轮同基线在 E2 契约违约（7/8） |
| live smoke | `run_evals.py --live-smoke --live-date 20261116` | 4/4：真连 `OPENHARMONY_CI` 装出 339M 运行时、`product=wukong100`、`arch overview` 返回真实计数、`references/tools.md` 与 `ask --list --markdown` 逐行一致 |
| skill 测试 | `python3.12 -m unittest discover -s skills/…/tests` | 215 passed |
| CLI 测试 | `python3.12 -m unittest discover -s cli/tests` | 199 passed（70 skipped） |
| oskm 测试 | `python3.12 -m unittest discover -s oskm/tests` | 301 passed（25 skipped） |
| 环境 | – | macOS 27.2.1 (arm64)、Python 3.12.16、codex-cli 0.169.0、模型 `qwen3.8-max`(reasoning=high) |

> 三份测试与四个评估臂都在同一份冻结快照上跑，避免与仓库内并行进行的其它改动互相污染。
