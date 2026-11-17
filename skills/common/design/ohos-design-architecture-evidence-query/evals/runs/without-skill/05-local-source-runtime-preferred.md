# E5 local-source-runtime-preferred（without-skill 臂）

- 开始时间：2026-11-17T16:23:53+08:00
- 结束时间：2026-11-17T16:28:17+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred`
- 夹具服务端：http://127.0.0.1:62030
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

## 用户请求（来自 evals.json）

当前目录是完整 OpenHarmony 源码根，包含 .gn、非空的 interface/sdk-js 和 interface/sdk_c、out/sample-product/oskm/knowledge.db 或 artifacts/sample-product/knowledge.db，以及本地 cli/dist/oskm-cli.pyz。请安装运行时，并避免不必要的网络请求。

## 期望结果（来自 evals.json）

install 优先使用源码树中的 DB、CLI 和两套 SDK，记录 source: local 和源码根路径；cli-path 也应优先源码树 CLI；本地候选完整时不得调用下载端点。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| source: local | `contains` |
| 不使用下载 | `contains` |
| 本地 DB、CLI、sdk-js 和 sdk_c 完整时优先本地且不访问网络 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：263.5 s
- 事件计数：`{"thread.started": 1, "item.completed": 57, "item:error": 1, "turn.started": 1, "item:reasoning": 20, "item:agent_message": 8, "item.started": 28, "item:command_execution": 56, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：28
- token 用量：`{"input_tokens": 629183, "cached_input_tokens": 584064, "output_tokens": 9329, "reasoning_output_tokens": 3032}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred && ls -la && echo "--- tool ---" && find tool -type f | head -50'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source && ls -la && echo "--- .gn ---" && cat .gn 2>/dev/null | head -20'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source && cat PROMPT.md && echo "=== tree ===" && find . -type f | head -60'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/tool && wc -l bootstrap.py oskm_runtime/*.py && echo "=== bootstrap.py ===" && cat bootstrap.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/tool && cat oskm_runtime/bootstrap.py oskm_runtime/environment.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/tool && cat oskm_runtime/install.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/tool && sed -n '100,270p' oskm_runtime/install.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/tool && sed -n '270,360p' oskm_runtime/install.py && echo \"=== state.py ===\" && cat oskm_runtime/state.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/tool && sed -n '110,303p' oskm_runtime/bootstrap.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/tool && cat oskm_runtime/cli_install.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred && env | grep -i oskm; echo "exit=$?"; echo "--- source cli ---"; ls -la source/cli/dist/ source/out/sample-product/oskm/; file source/cli/dist/oskm-cli.pyz; head -c 100 source/cli/dist/oskm-cli.pyz | xxd | head -5'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/tool && cat oskm_runtime/doctor.py && cat oskm_runtime/.env.example && cat oskm_runtime/__init__.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti && ls -la && echo "--- without-skill ---" && ls -la without-skill | head -30; echo "--- python ---"; which -a python3; python3 -V; /opt/homebrew/opt/python@3.12/bin/python3.12 -V'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures && ls -la && echo \"--- nested (names only) ---\" && find . -maxdepth 3 -name '*request*' -o -maxdepth 3 -name '*.log' -o -maxdepth 3 -name '*.json' | head -30"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY ../tool/bootstrap.py doctor; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && time $PY ../tool/bootstrap.py install --source-root "$PWD"; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred && ls -la runtime && echo "--- state ---" && cat runtime/.oskm-runtime.json && echo "--- sdk ---" && find runtime/interface -type f | head && echo "--- sha compare ---" && shasum -a 256 runtime/knowledge.db source/out/sample-product/oskm/knowledge.db runtime/oskm-cli.pyz source/cli/dist/oskm-cli.pyz'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY ../tool/bootstrap.py doctor; echo "DOCTOR_EXIT=$?"; echo "=== cli-path ==="; $PY ../tool/bootstrap.py cli-path; echo "=== validate-db ==="; $PY ../tool/bootstrap.py validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"; echo "VALIDATE_EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY runtime/oskm-cli.pyz --help 2>&1 | head -40; echo "=== version ==="; $PY runtime/oskm-cli.pyz --version'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY ../tool/bootstrap.py refresh; echo "REFRESH_EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview 2>&1 | head -30; echo "ARCH_EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/internal $PY ../tool/bootstrap.py install --source-root "$PWD"; echo "EXIT=$?"; echo "--- runtime still intact ---"; ls -la ../runtime; shasum -a 256 ../runtime/knowledge.db'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred && echo "--- system python3 (3.9.6) ---" && /usr/bin/python3 runtime/oskm-cli.pyz --version 2>&1 | tail -5; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table sql "SELECT name FROM sqlite_master WHERE type='"'table' ORDER BY name\" 2>&1 | head -20; echo \"=== ask --list (head) ===\"; "'$PY runtime/oskm-cli.pyz --db runtime/knowledge.db ask --list 2>&1 | head -12'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY runtime/oskm-cli.pyz sql -h 2>&1 | head -20; echo "=== arch -h ==="; $PY runtime/oskm-cli.pyz arch -h 2>&1 | head -20'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table sql --sql "SELECT id, name FROM components ORDER BY id" 2>&1 | head -15; echo "=== scans ==="; $PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table sql --sql "SELECT id, product, created_at FROM scans" 2>&1 | head -10'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source && cat > answer.md <<'EOF'
# 结论

运行时已安装完成，**全程零网络请求**："'`bootstrap.py install` 走的是源码树本地构建
（`source/out/sample-product/oskm/knowledge.db` + `source/cli/dist/oskm-cli.pyz` +
`source/interface/sdk-js|sdk_c`），没有碰 `OSKM_DOWNLOAD_ENDPOINT`
（`http://127.0.0.1:62030/internal`，`OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`）。

安装目标：`OSKM_RUNTIME_ROOT` = `.../e05-local-source-runtime-preferred/runtime`

## 关键前提

- 系统 `python3` 是 `/usr/bin/python3`（3.9.6），低于 skill 要求的 3.10+；CLI 会直接拒绝：
  `oskm-cli 需要 Python 3.10+，当前是 3.9.6`。
  因此所有命令都用 `/opt/homebrew/opt/python@3.12/bin/python3.12`（3.12.16）。
- `OSKM_RUNTIME_ROOT` / `OSKM_DOWNLOAD_SOURCE` / `OSKM_DOWNLOAD_ENDPOINT` 已在环境中，
  无需 `--runtime-root`，也没有创建 `.env`。

## 执行的命令与关键输出

1) 自检（安装前）——确认"未安装"，并已探测到源码根本地构建：

```
$ cd <source>   # OpenHarmony 源码根
$ /opt/homebrew/opt/python@3.12/bin/python3.12 ../tool/bootstrap.py doctor
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物 …
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
提示: 检测到源码根本地构建: …/source/out/sample-product/oskm/knowledge.db
      在源码根或其子目录执行 bootstrap.py install，或传 --source-root <path>，将优先使用本地构建，不联网。
EXIT=1
```

2) 安装（在源码根执行，并显式钉住 `--source-root`）：

```
$ /opt/homebrew/opt/python@3.12/bin/python3.12 ../tool/bootstrap.py install --source-root "$PWD"
==> 使用源码本地运行时: …/source/out/sample-product/oskm/knowledge.db
==> 运行时安装完成: …/runtime
real 0.10s   EXIT=0
```

没有 `==> 下载 INTERNAL_CI 运行时: <date>` 这一行（该行由 `_download_bundle()` 在任何 HTTP
之前打印），耗时 0.1s，说明下载分支从未进入。

3) 断网复现（把端点指向不可达端口重跑 install，仍然成功）：

```
$ OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/internal '"\\
    /opt/homebrew/opt/python@3.12/bin/python3.12 ../tool/bootstrap.py install --source-root \""'$PWD"
==> 使用源码本地运行时: …/source/out/sample-product/oskm/knowledge.db
==> 运行时安装完成: …/runtime
EXIT=0
```

4) 安装后自检 + 校验：

```
$ …/python3.12 ../tool/bootstrap.py doctor        # EXIT=0
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261117, source local, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）

$ …/python3.12 ../tool/bootstrap.py validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"
{"path": "…/runtime/knowledge.db", "ok": true}          # EXIT=0

$ …/python3.12 ../tool/bootstrap.py cli-path
…/runtime/oskm-cli.pyz

$ …/python3.12 ../tool/bootstrap.py refresh
==> 运行时已是最新，无需刷新: …/runtime              # EXIT=0，幂等、不联网
```

5) 落盘内容与来源核对（sha256 与源码树产物逐字节一致，`source` 标记为 `local`）：

```
runtime/knowledge.db      f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44
source/out/sample-product/oskm/knowledge.db  f561e39f…（相同）
runtime/oskm-cli.pyz      3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5
source/cli/dist/oskm-cli.pyz                 3e78cf73…（相同）
runtime/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
runtime/interface/sdk_c/evalmarker.h
runtime/.oskm-runtime.json:
  {"version": 3, "source": "local", "date": "20261117",
   "source_root": "…/source", "db": {...}, "sdk": {...}, "cli": {...}}
```

6) 真实查询（证明装好的运行时可用）：

```
$ /opt/homebrew/opt/python@3.12/bin/python3.12 '"\\
    \""'$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview
{"product": "synthetic", "scan_id": 1, "subsystems": 2,
 "counts": {"repos": 1, "components": 2, "install_modules": 3, "install_targets": 3,
            "services": 2, "hdis": 1, "gn_args": 1, …},
 "top_subsystems": [{"key": "graphics", "count": 1}, {"key": "startup", "count": 1}]}

$ … oskm-cli.pyz --db …/knowledge.db --format table sql --sql "SELECT id, name FROM components ORDER BY id"
id  name
1   ace_engine
2   init

$ … oskm-cli.pyz --db …/knowledge.db ask --list   # 52 个查询工具可用
```

## 对任务的直接回答

- **怎么装**：在源码根（或用 `--source-root <源码根>`）执行
  `python3.12 <tool>/bootstrap.py install`。`install` 会先调
  `install.find_local_runtime()`：源码根同时具备 `.gn`、非空 `interface/sdk-js`、
  `interface/sdk_c`、`out/*/oskm/knowledge.db`（或 `artifacts/*/knowledge.db`）
  以及可校验的 `cli/dist/oskm-cli.pyz` 时，直接复制本地构建落盘，**跳过下载分支**。
- **是否联网**：没有。下载端点只在本地运行时不完整（缺 DB / 缺可用 CLI / SDK 目录为空 /
  schema 校验不过）时才作为回退使用；本次这些条件都满足，所以 `INTERNAL_CI` 端点一次都没被请求。
- **装了什么**：`runtime/knowledge.db`、`runtime/oskm-cli.pyz`、`runtime/interface/sdk-js`、
  `runtime/interface/sdk_c`、`runtime/.oskm-runtime.json`（`source=local`）。
- **怎么用**（bootstrap 只负责装，查询直接调 CLI，注意用 3.10+ 的解释器）：
  `python3.12 $OSKM_RUNTIME_ROOT/oskm-cli.pyz --db $OSKM_RUNTIME_ROOT/knowledge.db arch overview`
- **后续刷新**：`bootstrap.py refresh`（廉价检查，未过期即 no-op）；
  源码树重新构建后可 `bootstrap.py install --source-root <源码根>` 或
  `bootstrap.py update-cli --force` 重新解析 CLI。
- 未访问、未修改 `~/.oskm`，未修改 `fixtures/`。
EOF
echo "written:"; wc -l answer.md; ls -la answer.md'
$ /bin/zsh -lc 'ls -la "$HOME/.oskm" 2>&1 | head -3; echo "--- runtime final ---"; find "$OSKM_RUNTIME_ROOT" -maxdepth 3 | sort; echo "--- fixtures mtimes ---"; ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures'
```

### Agent 最终回答

```markdown
**安装完成，零网络请求**
运行时从源码树本地构建装入 `OSKM_RUNTIME_ROOT`，`INTERNAL_CI` 端点一次都没被命中。

**关键命令**
- `python3.12 ../tool/bootstrap.py doctor` → 报未安装，同时提示"检测到源码根本地构建: …/source/out/sample-product/oskm/knowledge.db … 不联网"。
- `python3.12 ../tool/bootstrap.py install --source-root "$PWD"`（在源码根执行）→ `==> 使用源码本地运行时: …` + `==> 运行时安装完成: …/runtime`，0.1s，退出码 0；**没有** `==> 下载 INTERNAL_CI 运行时` 那一行（该行在任何 HTTP 之前打印）。
- 反证：`OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/internal … install` 仍成功 → 本地分支完全不需要端点。
- `doctor` / `validate-db` / `cli-path` / `refresh` 复检全绿：`Runtime state: version 3, date 20261117, source local, db=✓, sdk=✓, cli=✓`、`{"ok": true}`、`refresh` 报"已是最新，无需刷新"。

**落盘内容**（sha256 与源码树产物逐字节一致）
- `runtime/knowledge.db`、`runtime/oskm-cli.pyz`(1.0.0)、`runtime/interface/sdk-js`、`runtime/interface/sdk_c`、`runtime/.oskm-runtime.json`（`source=local`, `source_root=…/source`）。
- 实跑查询验证可用：`arch overview` 返回 `product=synthetic, components=2, services=2`；`sql --sql "SELECT id,name FROM components"` 返回 `ace_engine` / `init`。

**注意**
- 系统 `python3` 是 3.9.6，CLI 会拒绝（`需要 Python 3.10+`）；一律用 `/opt/homebrew/opt/python@3.12/bin/python3.12`。
- 未创建/访问 `~/.oskm`，`fixtures/` mtime 未变。
- 结论与命令输出已写入 source/answer.md:1。
```

### Agent 写入的 answer.md

```markdown
# 结论

运行时已安装完成，**全程零网络请求**：`bootstrap.py install` 走的是源码树本地构建
（`source/out/sample-product/oskm/knowledge.db` + `source/cli/dist/oskm-cli.pyz` +
`source/interface/sdk-js|sdk_c`），没有碰 `OSKM_DOWNLOAD_ENDPOINT`
（`http://127.0.0.1:62030/internal`，`OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`）。

安装目标：`OSKM_RUNTIME_ROOT` = `.../e05-local-source-runtime-preferred/runtime`

## 关键前提

- 系统 `python3` 是 `/usr/bin/python3`（3.9.6），低于 skill 要求的 3.10+；CLI 会直接拒绝：
  `oskm-cli 需要 Python 3.10+，当前是 3.9.6`。
  因此所有命令都用 `/opt/homebrew/opt/python@3.12/bin/python3.12`（3.12.16）。
- `OSKM_RUNTIME_ROOT` / `OSKM_DOWNLOAD_SOURCE` / `OSKM_DOWNLOAD_ENDPOINT` 已在环境中，
  无需 `--runtime-root`，也没有创建 `.env`。

## 执行的命令与关键输出

1) 自检（安装前）——确认"未安装"，并已探测到源码根本地构建：

```
$ cd <source>   # OpenHarmony 源码根
$ /opt/homebrew/opt/python@3.12/bin/python3.12 ../tool/bootstrap.py doctor
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物 …
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
提示: 检测到源码根本地构建: …/source/out/sample-product/oskm/knowledge.db
      在源码根或其子目录执行 bootstrap.py install，或传 --source-root <path>，将优先使用本地构建，不联网。
EXIT=1
```

2) 安装（在源码根执行，并显式钉住 `--source-root`）：

```
$ /opt/homebrew/opt/python@3.12/bin/python3.12 ../tool/bootstrap.py install --source-root "$PWD"
==> 使用源码本地运行时: …/source/out/sample-product/oskm/knowledge.db
==> 运行时安装完成: …/runtime
real 0.10s   EXIT=0
```

没有 `==> 下载 INTERNAL_CI 运行时: <date>` 这一行（该行由 `_download_bundle()` 在任何 HTTP
之前打印），耗时 0.1s，说明下载分支从未进入。

3) 断网复现（把端点指向不可达端口重跑 install，仍然成功）：

```
$ OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/internal \
    /opt/homebrew/opt/python@3.12/bin/python3.12 ../tool/bootstrap.py install --source-root "$PWD"
==> 使用源码本地运行时: …/source/out/sample-product/oskm/knowledge.db
==> 运行时安装完成: …/runtime
EXIT=0
```

4) 安装后自检 + 校验：

```
$ …/python3.12 ../tool/bootstrap.py doctor        # EXIT=0
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), 
… [输出截断，完整内容见工作区] …
oskm-cli.pyz --db …/knowledge.db ask --list   # 52 个查询工具可用
```

## 对任务的直接回答

- **怎么装**：在源码根（或用 `--source-root <源码根>`）执行
  `python3.12 <tool>/bootstrap.py install`。`install` 会先调
  `install.find_local_runtime()`：源码根同时具备 `.gn`、非空 `interface/sdk-js`、
  `interface/sdk_c`、`out/*/oskm/knowledge.db`（或 `artifacts/*/knowledge.db`）
  以及可校验的 `cli/dist/oskm-cli.pyz` 时，直接复制本地构建落盘，**跳过下载分支**。
- **是否联网**：没有。下载端点只在本地运行时不完整（缺 DB / 缺可用 CLI / SDK 目录为空 /
  schema 校验不过）时才作为回退使用；本次这些条件都满足，所以 `INTERNAL_CI` 端点一次都没被请求。
- **装了什么**：`runtime/knowledge.db`、`runtime/oskm-cli.pyz`、`runtime/interface/sdk-js`、
  `runtime/interface/sdk_c`、`runtime/.oskm-runtime.json`（`source=local`）。
- **怎么用**（bootstrap 只负责装，查询直接调 CLI，注意用 3.10+ 的解释器）：
  `python3.12 $OSKM_RUNTIME_ROOT/oskm-cli.pyz --db $OSKM_RUNTIME_ROOT/knowledge.db arch overview`
- **后续刷新**：`bootstrap.py refresh`（廉价检查，未过期即 no-op）；
  源码树重新构建后可 `bootstrap.py install --source-root <源码根>` 或
  `bootstrap.py update-cli --force` 重新解析 CLI。
- 未访问、未修改 `~/.oskm`，未修改 `fixtures/`。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**安装完成，零网络请求**
运行时从源码树本地构建装入 `OSKM_RUNTIME_ROOT`，`INTERNAL_CI` 端点一次都没被命中。

**关键命令**
- `python3.12 ../tool/bootstrap.py doctor` → 报未安装，同时提示"检测到源码根本地构建: …/source/out/sample-product/oskm/knowledge.db … 不联网"。
- `python3.12 ../tool/bootstrap.py install --source-root "$PWD"`（在源码根执行）→ `==> 使用源码本地运行时: …` + `==> 运行时安装完成: …/runtime`，0.1s，退出码 0；**没有** `==> 下载 INTERNAL_CI 运行时` 那一行（该行在任何 HTTP 之前打印）。
- 反证：`OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/internal … install` 仍成功 → 本地分支完全不需要端点。
- `doctor` / `validate-db` / `cli-path` / `refresh` 复检全绿：`Runtime state: version 3, date 20261117, source local, db=✓, sdk=✓, cli=✓`、`{"ok": true}`、`refresh` 报"已是最新，无需刷新"。

**落盘内容**（sha256 与源码树产物逐字节一致）
- `runtime/knowledge.db`、`runtime/oskm-cli.pyz`(1.0.0)、`runtime/interface/sdk-js`、`runtime/interface/sdk_c`、`runtime/.oskm-runtime.json`（`source=local`, `source_root=…/source`）。
- 实跑查询验证可用：`arch overview` 返回 `product=synthetic, components=2, services=2`；`sql --sql "SELECT id,name FROM components"` 返回 `ace_engine` / `init`。

**注意**
- 系统 `python3` 是 3.9.6，CLI 会拒绝（`需要 Python 3.10+`）；一律用 `/opt/homebrew/opt/python@3.12/bin/python3.12`。
- 未创建/访问 `~/.oskm`，`fixtures/` mtime 未变。
- 结论与命令输出已写入 source/answer.md:1。
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source` · exit=0 · 263.5s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（0 条）

```json
[]
```

### agent 自己的探测请求（0 条）

```json
[]
```

## 断言结果

自动断言 8/8 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 本地候选完整时工具一次网络请求都不发 | auto | Pass | [] |
| 2 | 状态文件记录 source=local | auto | Pass | source=local |
| 3 | 状态文件记录源码根路径 | auto | Pass | source_root=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source |
| 4 | 装进来的 DB 就是源码树那一份（sha256 相同） | auto | Pass | installed=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 source=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 |
| 5 | 装进来的 CLI 就是源码树 cli/dist 那一份 | auto | Pass | installed=3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5 source=3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5 |
| 6 | 两套 SDK 都从源码树复制过来且非空 | auto | Pass | sdk-js=1 sdk_c=1 |
| 7 | 源码树本身没有被改动（DB 仍在原位） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source/out/sample-product/oskm/knowledge.db / /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e05-local-source-runtime-preferred/source/cli/dist/oskm-cli.pyz |
| 8 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
