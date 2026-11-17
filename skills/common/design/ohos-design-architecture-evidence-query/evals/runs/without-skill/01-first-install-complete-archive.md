# E1 first-install-complete-archive（without-skill 臂）

- 开始时间：2026-11-17T15:33:43+08:00
- 结束时间：2026-11-17T15:37:14+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive`
- 夹具服务端：http://127.0.0.1:61142
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

运行根目录为空，测试夹具已提供一个本地 knowledge.tar.gz，内含 knowledge.db、oskm-cli.pyz、interface/sdk-js 和 interface/sdk_c。请从任意 Agent 启动目录安装该 skill 的托管运行时，并报告安装后的布局、状态与当前工作目录。

## 期望结果（来自 evals.json）

使用绝对路径调用 bootstrap.py install，把 knowledge.db、oskm-cli.pyz、interface/sdk-js 和 interface/sdk_c 一次装到同一个 runtime root；状态文件包含 db、sdk、cli 三段，不需要单独的 CLI 下载端点；安装完成后回到 Agent 启动目录。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| knowledge.db | `contains` |
| oskm-cli.pyz | `contains` |
| interface/sdk-js | `contains` |
| interface/sdk_c | `contains` |
| 四个产物位于同一 runtime root，未使用单独的 CLI 下载端点，且安装后当前目录等于 Agent 启动目录 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：210.6 s
- 事件计数：`{"thread.started": 1, "item.completed": 47, "item:error": 1, "turn.started": 1, "item:reasoning": 14, "item:agent_message": 12, "item.started": 20, "item:command_execution": 40, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：20
- token 用量：`{"input_tokens": 312790, "cached_input_tokens": 282240, "output_tokens": 6834, "reasoning_output_tokens": 1456}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'pwd; ls -la; echo "---"; ls -la ..; echo "--- tool ---"; find tool -maxdepth 3 | head -50'
$ /bin/zsh -lc 'env | grep -i oskm; echo "---"; ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/runtime 2>&1'
$ /bin/zsh -lc "cd ..; cat agent-start/PROMPT.md; echo \"=== tool tree ===\"; find tool -maxdepth 4 -not -path '*/.git/*' | sort"
$ /bin/zsh -lc 'cd ../tool; wc -l bootstrap.py; echo "---"; sed -n 1,200p bootstrap.py'
$ /bin/zsh -lc 'cd ../tool/oskm_runtime; wc -l *.py .env.example; echo "=== bootstrap.py ==="; cat bootstrap.py; echo "=== .env.example ==="; cat .env.example'
$ /bin/zsh -lc 'cd ../tool/oskm_runtime; echo "=== environment.py ==="; cat environment.py; echo "=== state.py ==="; cat state.py'
$ /bin/zsh -lc 'cd ../tool/oskm_runtime; sed -n 1,120p install.py'
$ /bin/zsh -lc 'cd ../tool/oskm_runtime; sed -n 1,80p doctor.py; echo "=== cli_install head ==="; sed -n 1,60p cli_install.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY ../tool/bootstrap.py --help; echo "== exit $? =="; echo "=== doctor (before install) ==="; $PY ../tool/bootstrap.py doctor; echo "== exit $? =="'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && time $PY ../tool/bootstrap.py install; echo "== exit $? =="'
$ /bin/zsh -lc 'cd ..; R=runtime; echo "=== tree (depth 2) ==="; find $R -maxdepth 2 -not -path '"'*/.git*' | sort; echo; echo \"=== sizes ===\"; du -sh "'$R/* 2>/dev/null; echo; echo "=== state file ==="; ls -a $R; echo "---"; cat $R/.oskm-state.json 2>/dev/null || cat $R/*.json 2>/dev/null'
$ /bin/zsh -lc "cd ..; grep -n \"STATE_NAME\\|SDK_PATHS\\|MINIMUM_PYTHON\\|DB_NAME\" tool/oskm_runtime/state.py | head -20"
$ /bin/zsh -lc "cd ..; cat runtime/.oskm-runtime.json; echo; echo \"=== SDK contents ===\"; ls -la runtime/interface/sdk-js runtime/interface/sdk_c; echo; echo \"=== db tables ===\"; /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"import sqlite3;c=sqlite3.connect('runtime/knowledge.db');print([r[0] for r in c.execute(\\\"select name from sqlite_master where type='table' order by name\\\")])\""
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "cwd=$(pwd)"; echo "=== doctor (after) ==="; $PY ../tool/bootstrap.py doctor; echo "== exit $? =="; echo "=== cli-path ==="; $PY ../tool/bootstrap.py cli-path; echo "=== refresh ==="; $PY ../tool/bootstrap.py refresh; echo "== exit $? =="'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && R=$OSKM_RUNTIME_ROOT && echo "=== validate-db ==="; $PY ../tool/bootstrap.py validate-db "$R/knowledge.db"; echo "== exit $? =="; echo "=== CLI --version ==="; $PY "$R/oskm-cli.pyz" --version; echo "=== arch overview ==="; $PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" arch overview 2>&1 | head -25'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/tool && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "cwd=$(pwd)"; $PY bootstrap.py refresh; echo "== exit $? =="; $PY bootstrap.py doctor | tail -6; echo "=== fixtures untouched ==="; cd ..; ls -la; find . -maxdepth 2 -name '"'*fixture*' -o -maxdepth 2 -name 'knowledge.tar.gz' | sort"
$ /bin/zsh -lc "cd ..; find runtime | sort | sed 's|"'^|  |'"'; echo \"=== sdk-js api ===\"; find runtime/interface -type f | sort; echo; ls -l runtime/knowledge.db runtime/oskm-cli.pyz"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start && cat > answer.md <<'EOF'
# 安装托管运行时：结果报告

## 直接回答

- **安装方式**："'`bootstrap.py` 是这个 skill 的唯一入口，只负责"装"不负责"查"。它把自己所在目录插到 `sys.path[0]`，因此**可以从任意 Agent 启动目录调用**，不需要 `cd`，也不需要设 `PYTHONPATH`。本次全程在 `agent-start/` 里执行，没有改动 fixtures。
- **落盘位置**：`OSKM_RUNTIME_ROOT` 已被解析为运行时根目录（优先级 `--runtime-root` > `validate-db PATH` 的父目录 > `$OSKM_RUNTIME_ROOT` > `~/.oskm`）。本次未传 `--runtime-root`，环境变量即生效，**没有触碰 `~/.oskm`**。
- **安装来源**：`OSKM_DOWNLOAD_SOURCE=INTERNAL_CI` + `OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61142/internal`，按当天日期 `20261117` 取完整 `knowledge.tar.gz`。归档里同时带 `knowledge.db`、`oskm-cli.pyz` 与两套 SDK，`install` 一次装齐；CLI 不单独下载（三级候选：`$OSKM_CLI` → 源码树 → `<runtime-root>/oskm-cli.pyz`，本次命中第三级）。
- **当前工作目录**：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start`（安装与所有后续命令都在这里跑；另在 `tool/` 里复跑了一次 `refresh`/`doctor` 验证 cwd 无关）。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
cd .../e01-first-install-complete-archive/agent-start

$PY ../tool/bootstrap.py doctor      # 安装前：CLI FAIL、模块缺失、runtime 未安装
$PY ../tool/bootstrap.py install     # 从 INTERNAL_CI 端点装 DB + CLI + 两套 SDK
$PY ../tool/bootstrap.py doctor      # 安装后：全绿
$PY ../tool/bootstrap.py cli-path
$PY ../tool/bootstrap.py refresh     # 幂等：已是最新，不重装
$PY ../tool/bootstrap.py validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --version
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview
```

## 关键输出片段

安装前 `doctor`（exit 1）：

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。…已尝试：1. $OSKM_CLI 未设置 2. 源码树… 3. <runtime>/oskm-cli.pyz —— 不存在
Modules: oskm_runtime (OK), oskm_cli (FAIL), oskm_schema (FAIL)
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。
```

`install`（exit 0，约 0.11s）：

```
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /…/e01-first-install-complete-archive/runtime
```

安装后 `doctor`（exit 0）：

```
CLI: /…/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: /…/e01-first-install-complete-archive/runtime
Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
```

`refresh`（幂等，exit 0）：

```
==> 运行时已是最新，无需刷新: /…/e01-first-install-complete-archive/runtime
```

功能冒烟：

```
validate-db → {"path": "/…/runtime/knowledge.db", "ok": true}
oskm-cli.pyz --version → oskm-cli 1.0.0
arch overview → {"product":"synthetic","scan_id":1,"subsystems":2,"counts":{"repos":1,"components":2,…}}
```

## 安装后的布局

运行时根目录 `/…/e01-first-install-complete-archive/runtime`（即 `$OSKM_RUNTIME_ROOT`）：

```
runtime/
├── .oskm-runtime.json                                  # 状态文件（STATE_NAME）
├── knowledge.db                                        # 434176 B，SQLite，25 张表
├── oskm-cli.pyz                                        # 83741 B，可执行，oskm-cli 1.0.0
└── interface/
    ├── sdk-js/api/@internal/ohos.evalmarker.d.ts
    └── sdk_c/evalmarker.h
```

- 归档根目录的四类内容原样平铺到 `<runtime-root>/`：`knowledge.db`、`oskm-cli.pyz`、`interface/sdk-js/`、`interface/sdk_c/`，外加入门写一个状态文件。
- CLI 与 DB 都是**固定文件名、不带版本号**，所以文档里可以直接写完整调用而不必钉版本。
- DB 表：`arkts_kit_relations, arkts_kits, arkts_links_run, arkts_modules, arkts_sources, collector_runs, collector_tables, component_links_run, components, elf_module_dependencies, elf_modules, features, gn_args, hdis, innerapis, install_module_tags, install_modules, install_targets, issues, native_headers, repos, sas, scans, services, syscaps`。

## 状态（`runtime/.oskm-runtime.json`）

```json
{
  "version": 3,
  "source": "INTERNAL_CI",
  "date": "20261117",
  "updated_at": "2026-11-17T15:34:36+08:00",
  "db":  { "date": "20261117", "path": "knowledge.db",
           "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44" },
  "sdk": { "date": "20261117",
           "sdk-js": { "path": "interface/sdk-js" },
           "sdk_c":  { "path": "interface/sdk_c" } },
  "cli": { "path": "oskm-cli.pyz",
           "sha256": "ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e" }
}
```

- `version: 3`，`source: INTERNAL_CI`，`date/updated_at` 为当天（20261117）。
- `sha256` 只是**出处记录**，不是 pin；完整性判定是结构性的（DB 走文件头 + `PRAGMA integrity_check`，pyz 走 shebang/zip/入口文件/CRC）。
- `needs_refresh()` 只看 `db` + `sdk` 的日期与文件在不在（`source=local` 时不看日期）；`cli` 段**不参与**刷新判定，缺 CLI 由 `ensure_cli()` 单独补齐，不会触发整包重下。因此当前状态在同一天内 `refresh` 一律 no-op。

## 安装后怎么用（查询不经 bootstrap）

```bash
python3 "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview
python3 "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask --list
python3 "$OSKM_RUNTIME_ROOT/bootstrap 不管查询"   # ← 查询一律直接调 CLI
```

`bootstrap.py` 传非托管子命令（如 `ask`/`arch`/`sql`）会以 exit 2 拒绝并提示直接调 CLI，这是 2026-11-12 之后的刻意设计。
EOF
echo "written: $(wc -l < answer.md) lines"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start && /opt/homebrew/opt/python@3.12/bin/python3.12 ../tool/bootstrap.py arch overview; echo "== exit $? =="'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start && python3 - <<'EOF'
from pathlib import Path
p = Path('answer.md')
text = p.read_text(encoding='utf-8')
old = 'python3 \""'$OSKM_RUNTIME_ROOT/bootstrap 不管查询"   # ← 查询一律直接调 CLI'"\\n'
assert old in text
text = text.replace(old, 'python3 \""'$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --help'"\\n')
old2 = '"'`bootstrap.py` 传非托管子命令（如 `ask`/`arch`/`sql`）会以 exit 2 拒绝并提示直接调 CLI，这是 2026-11-12 之后的刻意设计。'"'
new2 = ('实测 "'`$PY ../tool/bootstrap.py arch overview` → exit 2，输出：'"\\n\\n'
        '"'```'"\\n'
        '错误: 未知命令 arch。bootstrap.py 只负责安装，查询请直接调 CLI：\\n'
        '  python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db <ask|arch|diff|sql> …\\n'
        '可用命令: doctor, install, refresh, update-cli, download-db, validate-db, cli-path\\n'
        '"'```'"\\n\\n'
        '这是 2026-11-12 之后的刻意设计：查询透传已删除，避免 bootstrap 手抄一份 CLI 的解析器知识。')
assert old2 in text
text = text.replace(old2, new2)
p.write_text(text, encoding='utf-8')
print('patched')
EOF
tail -22 answer.md; echo \"=== final workspace state ===\"; ls -la; ls -la ../runtime"
```

### Agent 最终回答

```markdown
装好并跑通了。`answer.md` 已写入启动目录。

**安装**
- 入口是 `../tool/bootstrap.py`，它自把所在目录插到 `sys.path[0]`，所以从 `agent-start/` 直接调用即可，无需 `cd` 或 `PYTHONPATH`。
- 关键命令：`$PY ../tool/bootstrap.py install`（`$PY` = `/opt/homebrew/opt/python@3.12/bin/python3.12`），输出 `==> 下载 INTERNAL_CI 运行时: 20261117` / `==> 运行时安装完成: …/runtime`，exit 0，约 0.11s。
- 未传 `--runtime-root`，`$OSKM_RUNTIME_ROOT` 生效；全程没有触碰 `~/.oskm`，也没改 fixtures。

**布局**（`$OSKM_RUNTIME_ROOT` = `…/e01-first-install-complete-archive/runtime`）
- `knowledge.db`（434176 B，25 张表）、`oskm-cli.pyz`（83741 B，可执行，`oskm-cli 1.0.0`）、`interface/sdk-js/api/@internal/ohos.evalmarker.d.ts`、`interface/sdk_c/evalmarker.h`、`.oskm-runtime.json`（0600）。
- 归档根目录四类内容原样平铺；CLI 与 DB 均为固定无版本名，CLI 走三级候选并命中 `<runtime-root>/oskm-cli.pyz`。

**状态**（`.oskm-runtime.json`）
- `version 3`，`source INTERNAL_CI`，`date 20261117`，`updated_at 2026-11-17T15:34:36+08:00`；`db.sha256=f561e39f…`，`cli.sha256=ad760c16…`（仅出处记录，非 pin）。
- `doctor` exit 0：`db=✓, sdk=✓, cli=✓`，`Modules: oskm_runtime/oskm_cli/oskm_schema 全 OK`；安装前同一命令 exit 1 且 CLI FAIL。

**验证**
- `refresh` → `运行时已是最新，无需刷新`（同日幂等，`cli` 段不参与刷新判定）。
- `validate-db` → `{"path": "…/knowledge.db", "ok": true}`；`arch overview` 返回 `product synthetic / scan_id 1 / subsystems 2`。
- `bootstrap.py arch overview` → exit 2 并提示直接调 CLI（查询不经 bootstrap）；在 `tool/` 目录复跑 `refresh`/`doctor` 结果一致，确认与 cwd 无关。

**产物**
- `answer.md:1` — 含关键命令、输出片段与布局/状态/cwd 的直接回答。
```

### Agent 写入的 answer.md

```markdown
# 安装托管运行时：结果报告

## 直接回答

- **安装方式**：`bootstrap.py` 是这个 skill 的唯一入口，只负责"装"不负责"查"。它把自己所在目录插到 `sys.path[0]`，因此**可以从任意 Agent 启动目录调用**，不需要 `cd`，也不需要设 `PYTHONPATH`。本次全程在 `agent-start/` 里执行，没有改动 fixtures。
- **落盘位置**：`OSKM_RUNTIME_ROOT` 已被解析为运行时根目录（优先级 `--runtime-root` > `validate-db PATH` 的父目录 > `$OSKM_RUNTIME_ROOT` > `~/.oskm`）。本次未传 `--runtime-root`，环境变量即生效，**没有触碰 `~/.oskm`**。
- **安装来源**：`OSKM_DOWNLOAD_SOURCE=INTERNAL_CI` + `OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61142/internal`，按当天日期 `20261117` 取完整 `knowledge.tar.gz`。归档里同时带 `knowledge.db`、`oskm-cli.pyz` 与两套 SDK，`install` 一次装齐；CLI 不单独下载（三级候选：`$OSKM_CLI` → 源码树 → `<runtime-root>/oskm-cli.pyz`，本次命中第三级）。
- **当前工作目录**：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start`（安装与所有后续命令都在这里跑；另在 `tool/` 里复跑了一次 `refresh`/`doctor` 验证 cwd 无关）。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
cd .../e01-first-install-complete-archive/agent-start

$PY ../tool/bootstrap.py doctor      # 安装前：CLI FAIL、模块缺失、runtime 未安装
$PY ../tool/bootstrap.py install     # 从 INTERNAL_CI 端点装 DB + CLI + 两套 SDK
$PY ../tool/bootstrap.py doctor      # 安装后：全绿
$PY ../tool/bootstrap.py cli-path
$PY ../tool/bootstrap.py refresh     # 幂等：已是最新，不重装
$PY ../tool/bootstrap.py validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --version
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview
```

## 关键输出片段

安装前 `doctor`（exit 1）：

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。…已尝试：1. $OSKM_CLI 未设置 2. 源码树… 3. <runtime>/oskm-cli.pyz —— 不存在
Modules: oskm_runtime (OK), oskm_cli (FAIL), oskm_schema (FAIL)
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。
```

`install`（exit 0，约 0.11s）：

```
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /…/e01-first-install-complete-ar
… [输出截断，完整内容见工作区] …
e47ea5e63568ab0f1469afc1efead5cd5eb49e" }
}
```

- `version: 3`，`source: INTERNAL_CI`，`date/updated_at` 为当天（20261117）。
- `sha256` 只是**出处记录**，不是 pin；完整性判定是结构性的（DB 走文件头 + `PRAGMA integrity_check`，pyz 走 shebang/zip/入口文件/CRC）。
- `needs_refresh()` 只看 `db` + `sdk` 的日期与文件在不在（`source=local` 时不看日期）；`cli` 段**不参与**刷新判定，缺 CLI 由 `ensure_cli()` 单独补齐，不会触发整包重下。因此当前状态在同一天内 `refresh` 一律 no-op。

## 安装后怎么用（查询不经 bootstrap）

```bash
python3 "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview
python3 "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask --list
python3 "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --help
```

实测 `$PY ../tool/bootstrap.py arch overview` → exit 2，输出：

```
错误: 未知命令 arch。bootstrap.py 只负责安装，查询请直接调 CLI：
  python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db <ask|arch|diff|sql> …
可用命令: doctor, install, refresh, update-cli, download-db, validate-db, cli-path
```

这是 2026-11-12 之后的刻意设计：查询透传已删除，避免 bootstrap 手抄一份 CLI 的解析器知识。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
装好并跑通了。`answer.md` 已写入启动目录。

**安装**
- 入口是 `../tool/bootstrap.py`，它自把所在目录插到 `sys.path[0]`，所以从 `agent-start/` 直接调用即可，无需 `cd` 或 `PYTHONPATH`。
- 关键命令：`$PY ../tool/bootstrap.py install`（`$PY` = `/opt/homebrew/opt/python@3.12/bin/python3.12`），输出 `==> 下载 INTERNAL_CI 运行时: 20261117` / `==> 运行时安装完成: …/runtime`，exit 0，约 0.11s。
- 未传 `--runtime-root`，`$OSKM_RUNTIME_ROOT` 生效；全程没有触碰 `~/.oskm`，也没改 fixtures。

**布局**（`$OSKM_RUNTIME_ROOT` = `…/e01-first-install-complete-archive/runtime`）
- `knowledge.db`（434176 B，25 张表）、`oskm-cli.pyz`（83741 B，可执行，`oskm-cli 1.0.0`）、`interface/sdk-js/api/@internal/ohos.evalmarker.d.ts`、`interface/sdk_c/evalmarker.h`、`.oskm-runtime.json`（0600）。
- 归档根目录四类内容原样平铺；CLI 与 DB 均为固定无版本名，CLI 走三级候选并命中 `<runtime-root>/oskm-cli.pyz`。

**状态**（`.oskm-runtime.json`）
- `version 3`，`source INTERNAL_CI`，`date 20261117`，`updated_at 2026-11-17T15:34:36+08:00`；`db.sha256=f561e39f…`，`cli.sha256=ad760c16…`（仅出处记录，非 pin）。
- `doctor` exit 0：`db=✓, sdk=✓, cli=✓`，`Modules: oskm_runtime/oskm_cli/oskm_schema 全 OK`；安装前同一命令 exit 1 且 CLI FAIL。

**验证**
- `refresh` → `运行时已是最新，无需刷新`（同日幂等，`cli` 段不参与刷新判定）。
- `validate-db` → `{"path": "…/knowledge.db", "ok": true}`；`arch overview` 返回 `product synthetic / scan_id 1 / subsystems 2`。
- `bootstrap.py arch overview` → exit 2 并提示直接调 CLI（查询不经 bootstrap）；在 `tool/` 目录复跑 `refresh`/`doctor` 结果一致，确认与 cwd 无关。

**产物**
- `answer.md:1` — 含关键命令、输出片段与布局/状态/cwd 的直接回答。stderr:
2026-11-17T07:33:43.348823Z ERROR codex_skills_extension::host_service: failed to install system skills: io error while remove existing system skills dir: Directory not empty (os error 66)
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/agent-start` · exit=0 · 210.6s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T15:34:36.226+08:00",
    "method": "GET",
    "path": "/internal/20261117",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  }
]
```

### agent 自己的探测请求（0 条）

```json
[]
```

## 断言结果

自动断言 9/9 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | knowledge.db 装到了运行时根目录 | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/runtime/knowledge.db |
| 2 | oskm-cli.pyz 与 DB 并排（同一次安装装齐） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e01-first-install-complete-archive/runtime/oskm-cli.pyz |
| 3 | interface/sdk-js 非空 | auto | Pass | 1 个文件 |
| 4 | interface/sdk_c 非空 | auto | Pass | 1 个文件 |
| 5 | 状态文件同时记录 db / sdk / cli 三段 | auto | Pass | ["cli", "date", "db", "sdk", "source", "updated_at", "version"] |
| 6 | 工具每次安装只发一条"按日期取归档"的请求（没有盲探端点，也没有单独的 CLI 下载端点） | auto | Pass | 请求数=1，其中按日期归档请求=1；oskm-cli.pyz 已随归档装好=True；[{"method": "GET", "path": "/internal/20261117"}] |
| 7 | Agent 启动目录没有被安装产物污染 | auto | Pass | 启动目录内容: ['PROMPT.md', 'agent-last-message.md', 'answer.md', 'codex-events.jsonl', 'codex-stderr.log'] |
| 8 | 运行时根目录没有残留安装临时目录 | auto | Pass | leftovers=[] |
| 9 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
