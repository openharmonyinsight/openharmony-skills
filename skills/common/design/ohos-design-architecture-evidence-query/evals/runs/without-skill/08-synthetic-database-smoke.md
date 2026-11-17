# E8 synthetic-database-smoke（without-skill 臂）

- 开始时间：2026-11-17T15:43:01+08:00
- 结束时间：2026-11-17T15:50:07+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke`
- 夹具服务端：http://127.0.0.1:61499
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

已解压 skill 并单独构建 oskm-cli.pyz，测试夹具已生成 product=synthetic 的合成 knowledge.db。请用 bootstrap.py cli-path 定位 CLI，再直接调用 CLI 查询 scan 信息。

## 期望结果（来自 evals.json）

cli-path 找到测试提供的 pyz；直接调用 oskm-cli.pyz --db < synthetic db > ask get_scan_info 返回 product=synthetic。该步骤只验证两个产物能组合运行，不校验真实产品业务数据。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| get_scan_info | `contains` |
| synthetic | `contains` |
| 只验证 skill 与 CLI 的组合链路，不依赖真实数据库业务统计 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：426.0 s
- 事件计数：`{"thread.started": 1, "item.completed": 63, "item:error": 1, "turn.started": 1, "item:reasoning": 24, "item:agent_message": 9, "item.started": 29, "item:command_execution": 58, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：29
- token 用量：`{"input_tokens": 731213, "cached_input_tokens": 683904, "output_tokens": 14436, "reasoning_output_tokens": 4745}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc "ls -la; echo '---'; find . -maxdepth 3 -not -path '*/.git/*' | head -100"
$ /bin/zsh -lc 'ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/ 2>&1 | head -40'
$ /bin/zsh -lc "cat PROMPT.md; echo '=== bootstrap.py ==='; cat tool/bootstrap.py"
$ /bin/zsh -lc "wc -l tool/oskm_runtime/*.py; echo '---'; ls -la runtime artifacts/synthetic; echo '---'; ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/cli-tree /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/source"
$ /bin/zsh -lc 'cat tool/oskm_runtime/bootstrap.py'
$ /bin/zsh -lc 'cat tool/oskm_runtime/cli_install.py'
$ /bin/zsh -lc 'cat tool/oskm_runtime/environment.py'
$ /bin/zsh -lc "sed -n '120,240p' tool/oskm_runtime/cli_install.py"
$ /bin/zsh -lc "find /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/cli-tree /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/source -maxdepth 4 | head -60; echo '--- .gn ---'; cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/source/.gn"
$ /bin/zsh -lc "diff -r tool plain-tool && echo \"IDENTICAL\"; echo '---'; for d in /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T; do echo \""'$d: $(ls $d/cli/oskm_cli/__init__.py 2>/dev/null || echo none)"; done'
$ /bin/zsh -lc "sed -n '1,120p' tool/oskm_runtime/db_download.py"
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures; $PY $FIX/oskm-cli.pyz --version; echo "exit=$?"; echo '"'=== HELP ==='; "'$PY $FIX/oskm-cli.pyz --help; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --help'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && RT=$PWD/runtime && echo '"'--- 无配置 ---' && "'$PY tool/bootstrap.py --runtime-root "$RT" cli-path; echo "exit=$?"; echo '"'--- OSKM_CLI 指向夹具 ---'; OSKM_CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz "'$PY tool/bootstrap.py --runtime-root "$RT" cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures && $PY $FIX/oskm-cli.pyz --db artifacts/synthetic/knowledge.db ask --list 2>&1 | head -70'
$ /bin/zsh -lc "env | grep -i -E 'oskm|codex_home' ; echo \"---\"; ls -la \""'$HOME/.oskm" 2>&1 | head -5; echo "--- .env files ---"; ls -la tool/oskm_runtime/.env* runtime/ 2>&1'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo '=== cli-path ===' && "'$PY tool/bootstrap.py cli-path && echo '"'=== doctor ===' && "'$PY tool/bootstrap.py doctor; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && echo "CLI=$CLI" && $PY "$CLI" ask --help 2>&1 | head -30; echo '"'=== get_scan_info help ==='; "'$PY "$CLI" ask get_scan_info --help 2>&1 | head -30; echo '"'=== list_scans help ==='; "'$PY "$CLI" ask list_scans --help 2>&1 | head -30'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && DB=$PWD/artifacts/synthetic/knowledge.db && echo '"'=== get_scan_info (json) ===' && "'$PY "$CLI" --db "$DB" ask get_scan_info; echo "exit=$?"; echo '"'=== get_scan_info (table) ==='; "'$PY "$CLI" --db "$DB" --format table ask get_scan_info; echo "exit=$?"; echo '"'=== list_scans ==='; "'$PY "$CLI" --db "$DB" ask list_scans; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && echo '"'=== --product synthetic --scan-id 1 ===' && "'$PY "$CLI" --product synthetic --scan-id 1 ask get_scan_info --limit 1 2>&1 | head -12; echo "exit=$?"; echo '"'=== get_link_stats ==='; "'$PY "$CLI" --product synthetic ask get_link_stats; echo "exit=$?"; echo '"'=== bootstrap validate-db ==='; "'$PY tool/bootstrap.py validate-db "$PWD/artifacts/synthetic/knowledge.db"; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && echo '"'=== --product synthetic --scan-id 1 (no --db) ===' && "'$PY "$CLI" --product synthetic --scan-id 1 --format table ask list_scans; echo "exit=$?"; echo '"'=== arch overview ==='; "'$PY "$CLI" --product synthetic arch overview 2>&1 | head -25; echo '"'=== sql scans ==='; "'$PY "$CLI" --product synthetic sql "SELECT scan_id, product, cpu_arch, status, started_at, finished_at FROM scans"; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && $PY "$CLI" sql --help; mkdir -p tmp && printf '"'SELECT scan_id, product, cpu_arch, workspace_root, status, started_at, finished_at FROM scans;\\n' > tmp/scans.sql && echo '=== sql --file ===' && "'$PY "$CLI" --product synthetic sql --file tmp/scans.sql; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && $PY "$CLI" --product synthetic ask get_tables 2>&1 | head -20; echo '"'=== sql --sql ==='; "'$PY "$CLI" --product synthetic sql --sql "SELECT name FROM sqlite_master WHERE type='"'table' AND name LIKE '%scan%'\" 2>&1 | head -10"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && $PY "$CLI" --product synthetic ask get_tables | tr -d '"' \",' | tr '\\n' ' '; echo; "'$PY -c "import pathlib,shutil; p=pathlib.Path('"'tmp'); (p/'scans.sql').unlink(missing_ok=True); p.rmdir() if p.is_dir() else None; print('cleaned:', not p.exists())\""
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures && shasum -a 256 oskm-cli.pyz && stat -f '%z bytes' oskm-cli.pyz"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && cat > answer.md <<'EOF'
# e08 合成库 smoke：bootstrap.py cli-path + 直接调 CLI 查 scan

## 直接回答

1. **"'`bootstrap.py cli-path` 解析到的 CLI**：
   `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz`
   命中三级候选的**第 1 级 `$OSKM_CLI`**（`doctor` 里显示 `kind=env, oskm-cli 1.0.0`）。
   第 2 级源码树（向上找 `cli/oskm_cli/__init__.py`）与第 3 级
   `<runtime-root>/oskm-cli.pyz` 在本机都不成立：`tool/` 的各级父目录里没有 CLI 源码树，
   而运行时根目录 `runtime/` 是空的（未跑过 `install`）。
   产物指纹与任务描述一致：`sha256=ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e`，83741 bytes。

2. **合成库（product=synthetic）的 scan 信息**：只有 1 个扫描，`scan_id=1`，
   `product=synthetic`、`cpu_arch=arm64`、`workspace_root=/src`、`status=complete`、
   `started_at=2026-11-02T00:00:00Z`、`finished_at=2026-11-02T00:00:01Z`；
   11 个 collector（args / arkts / components / elf_modules / hdi / install_modules /
   links / native / repos / sas / services）全部 `complete`，`schema_version=4.0.0`，
   各 `record_count=1`；`attached_aliases` 为空（没挂对比库）。

3. **skill 与 CLI 两个产物能组合运行**：`bootstrap.py` 只管装/定位，查询直接调 CLI，
   两条链路都实测通过——`cli-path` 定位 + `python3 <pyz> --db … ask get_scan_info` 查询，
   以及 `bootstrap.py validate-db` 把 schema 契约校验**转发**给同一个 CLI（返回 `ok: true`）。

## 关键命令与输出

环境已由 harness 导出（`env | grep -i oskm`）：
`OSKM_CLI=<fixtures>/oskm-cli.pyz`、`OSKM_RUNTIME_ROOT=<workspace>/runtime`；
`~/.oskm` 不存在，本次全程未访问。

```console
$ PY=/opt/homebrew/opt/python@3.12/bin/python3.12
$ CLI=$($PY tool/bootstrap.py cli-path)          # 第 1 级候选 $OSKM_CLI 命中
$ echo "$CLI"
/private/var/folders/2g/…/fixtures/oskm-cli.pyz

$ $PY tool/bootstrap.py doctor
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
        FAIL: 下载配置无效。…
CLI: /private/var/folders/2g/…/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: /private/var/folders/2g/…/e08-synthetic-database-smoke/runtime
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。        # exit=1，仅因离线夹具没配下载端点，与查询无关
```

查询（`--db` 指合成库；`--product synthetic` 亦可，由 cwd 推导 `artifacts/<product>/knowledge.db`）：

```console
$ DB=$PWD/artifacts/synthetic/knowledge.db
$ $PY "$CLI" --db "$DB" ask get_scan_info
{
  "session_id": 1,
  "scan_id": 1,
  "product": "synthetic",
  "cpu_arch": "arm64",
  "workspace_root": "/src",
  "status": "complete",
  "started_at": "2026-11-02T00:00:00Z",
  "finished_at": "2026-11-02T00:00:01Z",
  "collectors": [
    {"collector": "args", "status": "complete", "schema_version": "4.0.0", "record_count": 1},
    … 共 11 条，全部 complete / 4.0.0 / record_count=1 …
  ],
  "attached_aliases": []
}                                        # exit=0

$ $PY "$CLI" --db "$DB" --format table ask get_scan_info
collector        status    schema_version  record_count
args             complete  4.0.0           1
…
services         complete  4.0.0           1

$ $PY "$CLI" --product synthetic --scan-id 1 --format table ask list_scans
scan_id  product    cpu_arch  started_at            finished_at           status
1        synthetic  arm64     2026-11-02T00:00:00Z  2026-11-02T00:00:01Z  complete

$ $PY tool/bootstrap.py validate-db "$DB"
{"path": "/var/folders/2g/…/artifacts/synthetic/knowledge.db", "ok": true}   # exit=0
```

旁证（同一 CLI 读同一库，说明 scan 上下文被正确应用）：

```console
$ $PY "$CLI" --product synthetic arch overview
{"product": "synthetic", "scan_id": 1, "subsystems": 2,
 "counts": {"repos": 1, "components": 2, "install_modules": 3, "install_targets": 3,
            "services": 2, "hdis": 1, "gn_args": 1, …}, "top_subsystems": [{"key": "graphics", …}]}

$ $PY "$CLI" --product synthetic ask get_link_stats
{"features": null, "innerapis": null}
```

## 踩到的边界

- scan 元数据**只能**走 `ask get_scan_info` / `list_scans` / `diff_scans`：
  `sql --sql/--file` 读 `scans` 会被受限只读层挡下
  （`{"error": {"code": "TABLE_NOT_ALLOWED", "message": "no such table: scans"}}`，exit=5），
  `ask get_tables` 的 21 张表里也确实没有 `scans`；查 `sqlite_master` 同样被禁
  （`SQL_ERROR: access to sqlite_master.name is prohibited`）。
- `bootstrap.py` 不接受查询子命令（`ask/arch/diff/sql` 会报未知命令并 exit=2），
  这正是 skill/CLI 分工的体现。
- `sql` 的 SQL 文本要走 `--file` 或 `--sql`，直接当位置参数会 `unrecognized arguments`（exit=2）。
- 全程只在 workspace、fixtures（只读）内操作；未修改 fixtures，未创建 `~/.oskm`，
  `runtime/` 保持为空（没有产物需要落地，因为 CLI 由 `$OSKM_CLI` 直接指过来）。
EOF
ls -la answer.md && head -5 answer.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY tool/bootstrap.py arch overview; echo "exit=$?"; echo '"'--- runtime ---'; ls -A runtime; echo \"--- ~/.oskm ---\"; ls -d \""'$HOME/.oskm" 2>&1; echo '"'--- git status of fixtures (untouched) ---'; shasum -a 256 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/knowledge.db"
$ /bin/zsh -lc "[\"apply_patch\",\"*** Begin Patch\\n*** Update File: /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke/answer.md\\n@@\\n-- "'`bootstrap.py` 不接受查询子命令（`ask/arch/diff/sql` 会报未知命令并 exit=2），'"\\n-  这正是 skill/CLI 分工的体现。\\n+- "'`bootstrap.py` 不接受查询子命令，这正是 skill/CLI 分工的体现（实测）：'"\\n+\\n+  "'```console'"\\n+  "'$ $PY tool/bootstrap.py arch overview'"\\n+  错误: 未知命令 arch。bootstrap.py 只负责安装，查询请直接调 CLI：\\n+    python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db <ask|arch|diff|sql> …\\n+  可用命令: doctor, install, refresh, update-cli, download-db, validate-db, cli-path\\n+  # exit=2\\n+  "'```'"\\n+\\n - "'`sql` 的 SQL 文本要走 `--file` 或 `--sql`，直接当位置参数会 `unrecognized arguments`（exit=2）。'"\\n - 全程只在 workspace、fixtures（只读）内操作；未修改 fixtures，未创建 "'`~/.oskm`，'"\\n   "'`runtime/` 保持为空（没有产物需要落地，因为 CLI 由 `$OSKM_CLI` 直接指过来）。'"\\n+  收尾复核："'`ls -A runtime` 为空、`~/.oskm` 不存在、夹具 `oskm-cli.pyz`'"\\n+  摘要仍是 "'`ad760c16…`（未被改动）。'"\\n*** End Patch\"]"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && cat > answer.md <<'EOF'
# e08 合成库 smoke：bootstrap.py cli-path + 直接调 CLI 查 scan

## 直接回答

1. **"'`bootstrap.py cli-path` 解析到的 CLI**：
   `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz`
   命中三级候选的**第 1 级 `$OSKM_CLI`**（`doctor` 里显示 `kind=env, oskm-cli 1.0.0`）。
   第 2 级源码树（向上找 `cli/oskm_cli/__init__.py`）与第 3 级
   `<runtime-root>/oskm-cli.pyz` 在本机都不成立：`tool/` 的各级父目录里没有 CLI 源码树，
   而运行时根目录 `runtime/` 是空的（未跑过 `install`）。
   产物指纹与任务描述一致：`sha256=ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e`，83741 bytes。

2. **合成库（product=synthetic）的 scan 信息**：只有 1 个扫描，`scan_id=1`，
   `product=synthetic`、`cpu_arch=arm64`、`workspace_root=/src`、`status=complete`、
   `started_at=2026-11-02T00:00:00Z`、`finished_at=2026-11-02T00:00:01Z`；
   11 个 collector（args / arkts / components / elf_modules / hdi / install_modules /
   links / native / repos / sas / services）全部 `complete`，`schema_version=4.0.0`，
   各 `record_count=1`；`attached_aliases` 为空（没挂对比库）。

3. **skill 与 CLI 两个产物能组合运行**：`bootstrap.py` 只管装/定位，查询直接调 CLI，
   两条链路都实测通过——`cli-path` 定位 + `python3 <pyz> --db … ask get_scan_info` 查询，
   以及 `bootstrap.py validate-db` 把 schema 契约校验**转发**给同一个 CLI（返回 `ok: true`）。

## 关键命令与输出

环境已由 harness 导出（`env | grep -i oskm`）：
`OSKM_CLI=<fixtures>/oskm-cli.pyz`、`OSKM_RUNTIME_ROOT=<workspace>/runtime`；
`~/.oskm` 不存在，本次全程未访问。

```console
$ PY=/opt/homebrew/opt/python@3.12/bin/python3.12
$ CLI=$($PY tool/bootstrap.py cli-path)          # 第 1 级候选 $OSKM_CLI 命中
$ echo "$CLI"
/private/var/folders/2g/…/fixtures/oskm-cli.pyz

$ $PY tool/bootstrap.py doctor
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
        FAIL: 下载配置无效。…
CLI: /private/var/folders/2g/…/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: /private/var/folders/2g/…/e08-synthetic-database-smoke/runtime
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。        # exit=1，仅因离线夹具没配下载端点，与查询无关
```

查询（`--db` 指合成库；`--product synthetic` 亦可，由 cwd 推导 `artifacts/<product>/knowledge.db`）：

```console
$ DB=$PWD/artifacts/synthetic/knowledge.db
$ $PY "$CLI" --db "$DB" ask get_scan_info
{
  "session_id": 1,
  "scan_id": 1,
  "product": "synthetic",
  "cpu_arch": "arm64",
  "workspace_root": "/src",
  "status": "complete",
  "started_at": "2026-11-02T00:00:00Z",
  "finished_at": "2026-11-02T00:00:01Z",
  "collectors": [
    {"collector": "args", "status": "complete", "schema_version": "4.0.0", "record_count": 1},
    … 共 11 条，全部 complete / 4.0.0 / record_count=1 …
  ],
  "attached_aliases": []
}                                        # exit=0

$ $PY "$CLI" --db "$DB" --format table ask get_scan_info
collector        status    schema_version  record_count
args             complete  4.0.0           1
…
services         complete  4.0.0           1

$ $PY "$CLI" --product synthetic --scan-id 1 --format table ask list_scans
scan_id  product    cpu_arch  started_at            finished_at           status
1        synthetic  arm64     2026-11-02T00:00:00Z  2026-11-02T00:00:01Z  complete

$ $PY tool/bootstrap.py validate-db "$DB"
{"path": "/var/folders/2g/…/artifacts/synthetic/knowledge.db", "ok": true}   # exit=0
```

旁证（同一 CLI 读同一库，说明 scan 上下文被正确应用）：

```console
$ $PY "$CLI" --product synthetic arch overview
{"product": "synthetic", "scan_id": 1, "subsystems": 2,
 "counts": {"repos": 1, "components": 2, "install_modules": 3, "install_targets": 3,
            "services": 2, "hdis": 1, "gn_args": 1, …}, "top_subsystems": [{"key": "graphics", …}]}

$ $PY "$CLI" --product synthetic ask get_link_stats
{"features": null, "innerapis": null}
```

## 踩到的边界

- scan 元数据**只能**走 `ask get_scan_info` / `list_scans` / `diff_scans`：
  `sql --sql/--file` 读 `scans` 会被受限只读层挡下
  （`{"error": {"code": "TABLE_NOT_ALLOWED", "message": "no such table: scans"}}`，exit=5），
  `ask get_tables` 的 21 张表里也确实没有 `scans`；查 `sqlite_master` 同样被禁
  （`SQL_ERROR: access to sqlite_master.name is prohibited`）。
- `bootstrap.py` 不接受查询子命令，这正是 skill/CLI 分工的体现（实测）：

  ```console
  $ $PY tool/bootstrap.py arch overview
  错误: 未知命令 arch。bootstrap.py 只负责安装，查询请直接调 CLI：
    python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db <ask|arch|diff|sql> …
  可用命令: doctor, install, refresh, update-cli, download-db, validate-db, cli-path
  # exit=2
  ```

- `sql` 的 SQL 文本要走 `--file` 或 `--sql`，直接当位置参数会 `unrecognized arguments`（exit=2）。
- 全程只在 workspace、fixtures（只读）内操作；未修改 fixtures，未创建 `~/.oskm`，
  `runtime/` 保持为空（没有产物需要落地，因为 CLI 由 `$OSKM_CLI` 直接指过来）。
  收尾复核：`ls -A runtime` 为空、`~/.oskm` 不存在、夹具 `oskm-cli.pyz`
  摘要仍是 `ad760c16…`（未被改动）。
EOF
wc -l answer.md; ls -A .'
```

### Agent 最终回答

```markdown
**结论**
- `bootstrap.py cli-path` → `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz`，命中三级候选的第 1 级 `$OSKM_CLI`（harness 已导出），`doctor` 报 `kind=env, oskm-cli 1.0.0`；源码树与 `<runtime-root>/oskm-cli.pyz` 两条候选在本机都不成立（`runtime/` 为空，未跑 `install`）。
- 直接调该 CLI 查 scan：`ask get_scan_info` 返回 `scan_id=1`、`product=synthetic`、`cpu_arch=arm64`、`workspace_root=/src`、`status=complete`、`2026-11-02T00:00:00Z → 00:00:01Z`，11 个 collector 全 `complete` / `schema_version=4.0.0` / `record_count=1`，`attached_aliases` 为空；`ask list_scans` 确认库里只有这 1 个扫描。
- 组合链路成立：`bootstrap.py validate-db artifacts/synthetic/knowledge.db` 转发给同一 CLI 返回 `{"ok": true}`；`--product synthetic` 也能由 cwd 推导出 `artifacts/synthetic/knowledge.db`。
- 注意点：scan 元数据只能走 `ask get_scan_info/list_scans/diff_scans`，`sql` 读 `scans` 被受限层挡下（`TABLE_NOT_ALLOWED`，exit=5，`get_tables` 的 21 张表里没有 `scans`）；`bootstrap.py arch …` 会以 exit=2 拒绝查询；`doctor` exit=1 只因离线夹具没配 `OSKM_DOWNLOAD_ENDPOINT`，与查询无关。

**产物与边界**
- 结论写在 answer.md:1，含逐条命令、输出片段与退出码。
- 夹具未被修改（`oskm-cli.pyz` 摘要仍为 `ad760c16b3a56a99…`，83741 bytes），`runtime/` 保持为空，未创建/访问 `~/.oskm`，实验用的临时 `tmp/scans.sql` 已清理。

要我再顺手跑一轮 `arch` 全 6 条问题、或把 CLI 产物按 `install` 的布局落到 `runtime/` 里验证第 3 级候选吗？
```

### Agent 写入的 answer.md

```markdown
# e08 合成库 smoke：bootstrap.py cli-path + 直接调 CLI 查 scan

## 直接回答

1. **`bootstrap.py cli-path` 解析到的 CLI**：
   `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz`
   命中三级候选的**第 1 级 `$OSKM_CLI`**（`doctor` 里显示 `kind=env, oskm-cli 1.0.0`）。
   第 2 级源码树（向上找 `cli/oskm_cli/__init__.py`）与第 3 级
   `<runtime-root>/oskm-cli.pyz` 在本机都不成立：`tool/` 的各级父目录里没有 CLI 源码树，
   而运行时根目录 `runtime/` 是空的（未跑过 `install`）。
   产物指纹与任务描述一致：`sha256=ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e`，83741 bytes。

2. **合成库（product=synthetic）的 scan 信息**：只有 1 个扫描，`scan_id=1`，
   `product=synthetic`、`cpu_arch=arm64`、`workspace_root=/src`、`status=complete`、
   `started_at=2026-11-02T00:00:00Z`、`finished_at=2026-11-02T00:00:01Z`；
   11 个 collector（args / arkts / components / elf_modules / hdi / install_modules /
   links / native / repos / sas / services）全部 `complete`，`schema_version=4.0.0`，
   各 `record_count=1`；`attached_aliases` 为空（没挂对比库）。

3. **skill 与 CLI 两个产物能组合运行**：`bootstrap.py` 只管装/定位，查询直接调 CLI，
   两条链路都实测通过——`cli-path` 定位 + `python3 <pyz> --db … ask get_scan_info` 查询，
   以及 `bootstrap.py validate-db` 把 schema 契约校验**转发**给同一个 CLI（返回 `ok: true`）。

## 关键命令与输出

环境已由 harness 导出（`env | grep -i oskm`）：
`OSKM_CLI=<fixtures>/oskm-cli.pyz`、`OSKM_RUNTIME_ROOT=<workspace>/runtime`；
`~/.oskm` 不存在，本次全程未访问。

```console
$ PY=/opt/homebrew/opt/python@3.12/bin/python3.12
$ CLI=$($PY tool/bootstrap.py cli-path)          # 第 1 级候选 $OSKM_CLI 命中
$ echo "$CLI"
/private/var/folders/2g/…/fixtures/oskm-cli.pyz

$ $PY tool/bootstrap.py doctor
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
        FAIL: 下载配置无效。…
CLI: /private/var/folders/2g/…/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: /private/var/folders/2g/…/e08-synthetic-database-smoke/runtime
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py 
… [输出截断，完整内容见工作区] …
ures": null, "innerapis": null}
```

## 踩到的边界

- scan 元数据**只能**走 `ask get_scan_info` / `list_scans` / `diff_scans`：
  `sql --sql/--file` 读 `scans` 会被受限只读层挡下
  （`{"error": {"code": "TABLE_NOT_ALLOWED", "message": "no such table: scans"}}`，exit=5），
  `ask get_tables` 的 21 张表里也确实没有 `scans`；查 `sqlite_master` 同样被禁
  （`SQL_ERROR: access to sqlite_master.name is prohibited`）。
- `bootstrap.py` 不接受查询子命令，这正是 skill/CLI 分工的体现（实测）：

  ```console
  $ $PY tool/bootstrap.py arch overview
  错误: 未知命令 arch。bootstrap.py 只负责安装，查询请直接调 CLI：
    python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db <ask|arch|diff|sql> …
  可用命令: doctor, install, refresh, update-cli, download-db, validate-db, cli-path
  # exit=2
  ```

- `sql` 的 SQL 文本要走 `--file` 或 `--sql`，直接当位置参数会 `unrecognized arguments`（exit=2）。
- 全程只在 workspace、fixtures（只读）内操作；未修改 fixtures，未创建 `~/.oskm`，
  `runtime/` 保持为空（没有产物需要落地，因为 CLI 由 `$OSKM_CLI` 直接指过来）。
  收尾复核：`ls -A runtime` 为空、`~/.oskm` 不存在、夹具 `oskm-cli.pyz`
  摘要仍是 `ad760c16…`（未被改动）。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结论**
- `bootstrap.py cli-path` → `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz`，命中三级候选的第 1 级 `$OSKM_CLI`（harness 已导出），`doctor` 报 `kind=env, oskm-cli 1.0.0`；源码树与 `<runtime-root>/oskm-cli.pyz` 两条候选在本机都不成立（`runtime/` 为空，未跑 `install`）。
- 直接调该 CLI 查 scan：`ask get_scan_info` 返回 `scan_id=1`、`product=synthetic`、`cpu_arch=arm64`、`workspace_root=/src`、`status=complete`、`2026-11-02T00:00:00Z → 00:00:01Z`，11 个 collector 全 `complete` / `schema_version=4.0.0` / `record_count=1`，`attached_aliases` 为空；`ask list_scans` 确认库里只有这 1 个扫描。
- 组合链路成立：`bootstrap.py validate-db artifacts/synthetic/knowledge.db` 转发给同一 CLI 返回 `{"ok": true}`；`--product synthetic` 也能由 cwd 推导出 `artifacts/synthetic/knowledge.db`。
- 注意点：scan 元数据只能走 `ask get_scan_info/list_scans/diff_scans`，`sql` 读 `scans` 被受限层挡下（`TABLE_NOT_ALLOWED`，exit=5，`get_tables` 的 21 张表里没有 `scans`）；`bootstrap.py arch …` 会以 exit=2 拒绝查询；`doctor` exit=1 只因离线夹具没配 `OSKM_DOWNLOAD_ENDPOINT`，与查询无关。

**产物与边界**
- 结论写在 answer.md:1，含逐条命令、输出片段与退出码。
- 夹具未被修改（`oskm-cli.pyz` 摘要仍为 `ad760c16b3a56a99…`，83741 bytes），`runtime/` 保持为空，未创建/访问 `~/.oskm`，实验用的临时 `tmp/scans.sql` 已清理。

要我再顺手跑一轮 `arch` 全 6 条问题、或把 CLI 产物按 `install` 的布局落到 `runtime/` 里验证第 3 级候选吗？stderr:
2026-11-17T07:46:42.827843Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && $PY \\\"$CLI\\\" --product synthetic ask get_tables | tr -d '\\\"' \\\\\\\",' | tr '\\\\\\\\n' ' '; echo; rm -rf tmp\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
2026-11-17T07:48:33.396557Z ERROR codex_core::tools::router: error=failed to parse function arguments: missing field `cmd` at line 1 column 1319
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e08-synthetic-database-smoke` · exit=0 · 426.0s

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

自动断言 5/5 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 回答里出现 get_scan_info | auto | Pass | answer/输出中出现 get_scan_info |
| 2 | 回答里出现 synthetic | auto | Pass | answer/输出中出现 synthetic |
| 3 | 是否明确说明该场景只验证组合链路、不代表真实产品数据 | manual | 人工 | **结论** - `bootstrap.py cli-path` → `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz`，命中三级候选的第 1 级 `$OSKM_CLI`（harness 已导出），`doctor` 报 `k
… [输出截断，完整内容见工作区] …
ema_version=4.0.0` / `record_count=1`，`attached_aliases` 为空；`ask list_scans` 确认库里只有这 1 个扫描。 - 组合链路成立 |
| 4 | 查询是只读的：合成库 sha256 未变 | auto | Pass | sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 |
| 5 | 工具没有联网 | auto | Pass | [] |
| 6 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
