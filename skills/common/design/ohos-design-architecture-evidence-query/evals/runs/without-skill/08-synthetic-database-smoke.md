# E8 synthetic-database-smoke（without-skill 臂）

- 开始时间：2026-11-17T16:30:53+08:00
- 结束时间：2026-11-17T16:36:18+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke`
- 夹具服务端：http://127.0.0.1:62273
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：324.8 s
- 事件计数：`{"thread.started": 1, "item.completed": 63, "item:error": 1, "turn.started": 1, "item:reasoning": 20, "item:agent_message": 14, "item.started": 28, "item:command_execution": 56, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：28
- token 用量：`{"input_tokens": 533630, "cached_input_tokens": 492800, "output_tokens": 11602, "reasoning_output_tokens": 4336}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'pwd && ls -la && echo "---TOOL---" && ls -R tool | head -50'
$ /bin/zsh -lc 'ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures/ 2>/dev/null | head -30'
$ /bin/zsh -lc 'cat PROMPT.md && echo "=====BOOTSTRAP=====" && cat tool/bootstrap.py'
$ /bin/zsh -lc 'ls -la plain-tool && find artifacts runtime -maxdepth 3 && echo "---" && wc -l tool/oskm_runtime/*.py'
$ /bin/zsh -lc 'cat tool/oskm_runtime/bootstrap.py'
$ /bin/zsh -lc 'cat tool/oskm_runtime/cli_install.py'
$ /bin/zsh -lc 'cat tool/oskm_runtime/environment.py && echo "=====STATE=====" && cat tool/oskm_runtime/state.py'
$ /bin/zsh -lc "sed -n '120,235p' tool/oskm_runtime/cli_install.py"
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures && ls -R cli-tree | head -20 && echo "---SOURCE---" && ls source && echo "---sha---" && shasum -a 256 oskm-cli.pyz && ls -l oskm-cli.pyz'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY -V && head -c 60 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz | head -1 && echo && $PY /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz --version && $PY /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz --help'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --help'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && cp /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz runtime/oskm-cli.pyz && ls -l runtime/ && shasum -a 256 runtime/oskm-cli.pyz'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "### cli-path (installed) ###" && $PY tool/bootstrap.py --runtime-root runtime cli-path; echo "exit=$?" && echo "### cli-path (OSKM_CLI override -> fixture) ###" && OSKM_CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz $PY tool/bootstrap.py --runtime-root runtime cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --runtime-root runtime doctor; echo "doctor exit=$?"'
$ /bin/zsh -lc "env | grep -i -E 'oskm|codex_home' ; echo \"---dotfiles---\"; ls -la tool/oskm_runtime/ plain-tool/oskm_runtime/ | grep -i env; find . -name '.env*' -maxdepth 4 2>/dev/null"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "### cli-path without OSKM_CLI (falls to installed candidate) ###" && env -u OSKM_CLI $PY tool/bootstrap.py --runtime-root runtime cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && CLI=$(python3 tool/bootstrap.py cli-path 2>/dev/null || /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py cli-path) && echo "CLI=$CLI" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" ask --list 2>&1 | grep -i -n scan | head -40'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && $PY "$CLI" ask --help && echo "=== SQL HELP ===" && $PY "$CLI" sql --help'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && DB=$PWD/artifacts/synthetic/knowledge.db && echo "### list_scans (table) ###" && $PY "$CLI" --db "$DB" ask list_scans; echo "exit=$?"; echo "### list_scans (json) ###" && $PY "$CLI" --db "$DB" --format json ask list_scans; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && DB=$PWD/artifacts/synthetic/knowledge.db && echo "### get_scan_info (default = latest) ###" && $PY "$CLI" --db "$DB" ask get_scan_info; echo "exit=$?"; echo "### get_scan_info --scan-id 1 ###" && $PY "$CLI" --db "$DB" --scan-id 1 ask get_scan_info; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && echo "### --product synthetic (derives artifacts/synthetic/knowledge.db) ###" && $PY "$CLI" --product synthetic ask list_scans; echo "exit=$?"; echo "### sql on scans ###" && $PY "$CLI" --db "$PWD/artifacts/synthetic/knowledge.db" sql --sql "SELECT scan_id, product, cpu_arch, status, workspace_root, started_at, finished_at FROM scans"; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && echo "### CLI validate-db ###" && $PY "$CLI" --db "$PWD/artifacts/synthetic/knowledge.db" validate-db 2>&1 | tail -20; echo "exit=${PIPESTATUS[0]}"; echo "### bootstrap validate-db (forwarded) ###" && $PY tool/bootstrap.py --runtime-root runtime validate-db "$PWD/artifacts/synthetic/knowledge.db" 2>&1 | tail -8; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && DB=$PWD/artifacts/synthetic/knowledge.db && $PY "$CLI" --db "$DB" ask get_tables 2>&1 | tr '"',' '\\n' | grep -i -E 'scan|collector|meta' "
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import sqlite3
c=sqlite3.connect('artifacts/synthetic/knowledge.db')
print([r[0] for r in c.execute(\\\"select name from sqlite_master where type='table' order by name\\\") if 'scan' in r[0] or 'collect' in r[0]])
print(list(c.execute('select * from scans')))
\""
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && DB=$PWD/artifacts/synthetic/knowledge.db && echo "### get_tables (head) ###" && $PY "$CLI" --db "$DB" ask get_tables 2>&1 | head -c 600; echo; echo "### sql SELECT * FROM scans ###" && $PY "$CLI" --db "$DB" sql --sql "SELECT * FROM scans"; echo "exit=$?"; echo "### sql with limit ###" && $PY "$CLI" --db "$DB" sql --sql "SELECT scan_id, product, cpu_arch FROM scans" --limit 5; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI=$($PY tool/bootstrap.py cli-path) && DB=$PWD/artifacts/synthetic/knowledge.db && echo "### sql on an allowed table ###" && $PY "$CLI" --db "$DB" sql --sql "SELECT COUNT(*) AS n FROM components"; echo "exit=$?"; echo "### get_schema scans? ###" && $PY "$CLI" --db "$DB" ask get_schema --table scans 2>&1 | head -c 300; echo; echo "### arch overview ###" && $PY "$CLI" --db "$DB" arch overview 2>&1 | head -c 900'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && cat > answer.md <<'EOF'
# 合成库 smoke：skill(bootstrap.py) + oskm-cli.pyz 组合验证

## 直接回答

**能组合运行。** 用 "'`tool/bootstrap.py cli-path` 定位到单独构建的 CLI 产物，直接调用它查询
`product=synthetic` 的合成库，`list_scans` / `get_scan_info` 全部 exit=0，
`bootstrap.py validate-db` 转发给 CLI 的 schema 契约校验也返回 `ok: true`。

合成库里只有 **1 个 scan**：

| 字段 | 值 |
| --- | --- |
| scan_id | 1 |
| product | synthetic |
| cpu_arch | arm64 |
| workspace_root | /src |
| status | complete |
| started_at / finished_at | 2026-11-02T00:00:00Z / 2026-11-02T00:00:01Z |
| collectors | 11 个，全部 `status=complete`、`schema_version=4.0.0`、`record_count=1` |
| attached_aliases | `[]`（没有挂载对比库） |

11 个 collector：`args, arkts, components, elf_modules, hdi, install_modules, links,
native, repos, sas, services`。

## 关键命令与输出

### 0. 环境事实核对

```console
$ env | grep -i oskm
OSKM_CLI=/private/var/.../oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz
OSKM_RUNTIME_ROOT=/var/folders/.../without-skill/e08-synthetic-database-smoke/runtime

$ shasum -a 256 <fixtures>/oskm-cli.pyz && ls -l <fixtures>/oskm-cli.pyz
3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5
-rwxr-xr-x  1 song  staff  84742 Nov 17 16:18 oskm-cli.pyz
```

sha256 前缀 `3e78cf73a94bcf9d…` 与 84742 bytes 都和任务里给的一致。
`OSKM_CLI` / `OSKM_RUNTIME_ROOT` 已由环境预先导出，所以不必手写 `--runtime-root`。

### 1. bootstrap.py cli-path 定位 CLI

```console
$ python3.12 tool/bootstrap.py cli-path
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz

$ python3.12 tool/bootstrap.py --runtime-root runtime doctor | grep -E '"'Python|CLI|Modules'
Python: 3.12.16 (OK, requires Python 3.10+)
CLI: /private/var/.../fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
"'```

命中的是三级候选里的第 1 级 `$OSKM_CLI`（doctor 标为 `env`）。把 `OSKM_CLI` 摘掉后
落到第 3 级 `<runtime-root>/oskm-cli.pyz`（我按 fixture 复制了一份到 runtime/）：

```console
$ env -u OSKM_CLI python3.12 tool/bootstrap.py --runtime-root runtime cli-path
/var/folders/.../without-skill/e08-synthetic-database-smoke/runtime/oskm-cli.pyz
```

第 2 级"源码树"在本工作区不存在（`tool/` 向上找不到 `cli/oskm_cli/__init__.py`），符合预期。

### 2. 直接调 CLI 查 scan 信息

```console
$ CLI=$(python3.12 tool/bootstrap.py cli-path)
$ DB=$PWD/artifacts/synthetic/knowledge.db
$ python3.12 "$CLI" --version
oskm-cli 1.0.0

$ python3.12 "$CLI" --db "$DB" ask list_scans          # exit=0
{
  "scans": [
    {
      "scan_id": 1,
      "product": "synthetic",
      "cpu_arch": "arm64",
      "started_at": "2026-11-02T00:00:00Z",
      "finished_at": "2026-11-02T00:00:01Z",
      "status": "complete"
    }
  ]
}

$ python3.12 "$CLI" --db "$DB" ask get_scan_info       # exit=0，缺省取最新 scan
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
    { "collector": "args", "status": "complete", "schema_version": "4.0.0", "record_count": 1 },
    ...（共 11 条，全部 complete / 4.0.0 / record_count=1）
  ],
  "attached_aliases": []
}

$ python3.12 "$CLI" --db "$DB" --scan-id 1 ask get_scan_info   # 显式指定，输出同上，exit=0
```

`--product` 推导路径也通（`artifacts/<product>/knowledge.db`，相对 cwd）：

```console
$ python3.12 "$CLI" --product synthetic ask list_scans   # exit=0，输出与 --db 版一致
```

### 3. 交叉验证

```console
$ python3.12 "$CLI" --db "$DB" arch overview
{ "product": "synthetic", "scan_id": 1, "subsystems": 2,
  "counts": { "repos": 1, "components": 2, "install_modules": 3, "install_targets": 3,
              "elf_modules": 0, "services": 2, "sas": 0, "hdis": 1, "gn_args": 1,
              "arkts_modules": 0, "arkts_kits": 0 },
  "top_subsystems": [ {"key":"graphics","count":1}, {"key":"startup","count":1} ] }

$ python3.12 tool/bootstrap.py --runtime-root runtime validate-db "$DB"   # exit=0
{"path": "/var/folders/.../artifacts/synthetic/knowledge.db", "ok": true}

$ python3.12 -c "import sqlite3;print(list(sqlite3.connect('"'artifacts/synthetic/knowledge.db').execute('select * from scans')))\"
[(1, 'synthetic', 'arm64', '/src', '2026-11-02T00:00:00Z', '2026-11-02T00:00:01Z')]
"'```

裸 sqlite3 读到的行与 `list_scans` / `get_scan_info` 完全一致。

## 过程中的两个非阻塞发现

1. **`sql` 子命令查不到 `scans`。** `sql --sql "SELECT * FROM scans"` 返回
   `{"error": {"code": "TABLE_NOT_ALLOWED", "message": "no such table: scans"}}`（exit=5），
   `ask get_schema --table scans` 返回 `INVALID_TABLE`。原因是 `sql` 沙箱只放开
   `ask get_tables` 里那 21 张业务表（`components`、`repos`、`services`…），
   `scans` / `collector_runs` / `collector_tables` 属于会话层，只能走
   `ask list_scans` / `get_scan_info` / `diff_scans`。沙箱本身是好的：
   `sql --sql "SELECT COUNT(*) AS n FROM components"` → `{"rows":[{"n":2}],"row_count":1,"truncated":false}`。

2. **`doctor` 整体 exit=1，但与本次 smoke 无关。** 两条 FAIL/提示分别是：
   `OSKM_DOWNLOAD_ENDPOINT 未配置`（本场景不下载，用现成夹具）与
   `运行时状态: 未安装（没有 knowledge.db）`（runtime/ 下只有 CLI，没有 DB；
   合成库按任务要求留在 `artifacts/synthetic/`）。Python 版本、CLI、
   三个内部模块 `oskm_runtime` / `oskm_cli` / `oskm_schema` 均 OK。

3. **CLI 的 `validate-db` 用位置参数，不是 `--db`。**
   `python3.12 oskm-cli.pyz --db X validate-db` 会报
   `error: the following arguments are required: path`；正确形式是
   `validate-db <path>`，或直接走 `bootstrap.py validate-db <path>`（它会转发）。

## 本次对工作区的改动

- 只新增了 `runtime/oskm-cli.pyz`（从夹具复制，sha256 一致）和本文件 `answer.md`。
- 未修改 `fixtures/`，未触碰 `~/.oskm`，未使用 `ps`/`pgrep`/`lsof`。
EOF
echo "written:" && wc -l answer.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke && ls -la . runtime artifacts/synthetic && echo "--- fixtures untouched? ---" && ls -l /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz && echo "--- answer.md head ---" && head -20 answer.md'
```

### Agent 最终回答

```markdown
**Result**
Skill + CLI compose and run. `bootstrap.py cli-path` locates the standalone build, and direct CLI calls return scan info from the `product=synthetic` DB (all exit 0).

**Commands Run**
- `python3.12 tool/bootstrap.py cli-path` → `/…/fixtures/oskm-cli.pyz` (candidate 1, `$OSKM_CLI` already exported by the env; `doctor` tags it `env, oskm-cli 1.0.0`).
- `env -u OSKM_CLI python3.12 tool/bootstrap.py --runtime-root runtime cli-path` → `runtime/oskm-cli.pyz` (candidate 3 works after copying the fixture in; candidate 2 source tree absent, as expected).
- `python3.12 "$CLI" --db "$DB" ask list_scans` and `ask get_scan_info` (plus `--scan-id 1`, plus `--product synthetic`) → `scan_id=1`, `product=synthetic`, `cpu_arch=arm64`, `workspace_root=/src`, `status=complete`, `2026-11-02T00:00:00Z`→`00:00:01Z`, 11 collectors all `complete` / `schema_version 4.0.0` / `record_count 1`, `attached_aliases: []`.
- `python3.12 tool/bootstrap.py --runtime-root runtime validate-db <db>` → `{"ok": true}`; `arch overview` confirms `product=synthetic, scan_id=1`.

**Gotchas Found**
- `sql --sql "SELECT * FROM scans"` → `TABLE_NOT_ALLOWED` (exit 5): the SQL sandbox only exposes the 21 registered business tables from `ask get_tables`; scan metadata must come from `list_scans` / `get_scan_info` / `diff_scans`. Sandbox itself is fine (`SELECT COUNT(*) FROM components` → `2`).
- CLI `validate-db` takes a positional path, not `--db`; `--db X validate-db` errors with `required: path`.
- `doctor` exits 1 for unrelated reasons only: `OSKM_DOWNLOAD_ENDPOINT` unset and no `knowledge.db` in `runtime/` (DB intentionally stays in `artifacts/synthetic/`). Python 3.12.16, CLI, and `oskm_runtime`/`oskm_cli`/`oskm_schema` all OK.

**Changes**
- Added `runtime/oskm-cli.pyz` (copy of fixture, sha256 `3e78cf73…` matches) and `answer.md` with full command/output log. `fixtures/` untouched, `~/.oskm` never accessed.

Want me to also drop a `.env` in `runtime/` so `doctor` goes fully green, or copy the synthetic DB to `runtime/knowledge.db` for the canonical `<runtime-root>/knowledge.db` invocation?
```

### Agent 写入的 answer.md

```markdown
# 合成库 smoke：skill(bootstrap.py) + oskm-cli.pyz 组合验证

## 直接回答

**能组合运行。** 用 `tool/bootstrap.py cli-path` 定位到单独构建的 CLI 产物，直接调用它查询
`product=synthetic` 的合成库，`list_scans` / `get_scan_info` 全部 exit=0，
`bootstrap.py validate-db` 转发给 CLI 的 schema 契约校验也返回 `ok: true`。

合成库里只有 **1 个 scan**：

| 字段 | 值 |
| --- | --- |
| scan_id | 1 |
| product | synthetic |
| cpu_arch | arm64 |
| workspace_root | /src |
| status | complete |
| started_at / finished_at | 2026-11-02T00:00:00Z / 2026-11-02T00:00:01Z |
| collectors | 11 个，全部 `status=complete`、`schema_version=4.0.0`、`record_count=1` |
| attached_aliases | `[]`（没有挂载对比库） |

11 个 collector：`args, arkts, components, elf_modules, hdi, install_modules, links,
native, repos, sas, services`。

## 关键命令与输出

### 0. 环境事实核对

```console
$ env | grep -i oskm
OSKM_CLI=/private/var/.../oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz
OSKM_RUNTIME_ROOT=/var/folders/.../without-skill/e08-synthetic-database-smoke/runtime

$ shasum -a 256 <fixtures>/oskm-cli.pyz && ls -l <fixtures>/oskm-cli.pyz
3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5
-rwxr-xr-x  1 song  staff  84742 Nov 17 16:18 oskm-cli.pyz
```

sha256 前缀 `3e78cf73a94bcf9d…` 与 84742 bytes 都和任务里给的一致。
`OSKM_CLI` / `OSKM_RUNTIME_ROOT` 已由环境预先导出，所以不必手写 `--runtime-root`。

### 1. bootstrap.py cli-path 定位 CLI

```console
$ python3.12 tool/bootstrap.py cli-path
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz

$ python3.12 tool/bootstrap.py --runtime-root runtime doctor | grep -E 'Python|CLI|Modules'
Python: 3.12.16 (OK, requires Python 3.10+)
CLI: /private/var/.../fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
```

命中的是三级候选里的第 1 级 `$OSKM_CLI`（doctor 标为 `env`）。把 `OSKM_CLI` 摘掉后
落到第 3 级 `<runtime-root>/oskm-cli.pyz`（我按 fixture 复制了一份到 runtime/）：

```console
$ env -u OSKM_CLI python3.12 tool/bootstrap.py --runtime-root runtime cli-path
/var/folders/.../without-skill/e0
… [输出截断，完整内容见工作区] …
sk get_schema --table scans` 返回 `INVALID_TABLE`。原因是 `sql` 沙箱只放开
   `ask get_tables` 里那 21 张业务表（`components`、`repos`、`services`…），
   `scans` / `collector_runs` / `collector_tables` 属于会话层，只能走
   `ask list_scans` / `get_scan_info` / `diff_scans`。沙箱本身是好的：
   `sql --sql "SELECT COUNT(*) AS n FROM components"` → `{"rows":[{"n":2}],"row_count":1,"truncated":false}`。

2. **`doctor` 整体 exit=1，但与本次 smoke 无关。** 两条 FAIL/提示分别是：
   `OSKM_DOWNLOAD_ENDPOINT 未配置`（本场景不下载，用现成夹具）与
   `运行时状态: 未安装（没有 knowledge.db）`（runtime/ 下只有 CLI，没有 DB；
   合成库按任务要求留在 `artifacts/synthetic/`）。Python 版本、CLI、
   三个内部模块 `oskm_runtime` / `oskm_cli` / `oskm_schema` 均 OK。

3. **CLI 的 `validate-db` 用位置参数，不是 `--db`。**
   `python3.12 oskm-cli.pyz --db X validate-db` 会报
   `error: the following arguments are required: path`；正确形式是
   `validate-db <path>`，或直接走 `bootstrap.py validate-db <path>`（它会转发）。

## 本次对工作区的改动

- 只新增了 `runtime/oskm-cli.pyz`（从夹具复制，sha256 一致）和本文件 `answer.md`。
- 未修改 `fixtures/`，未触碰 `~/.oskm`，未使用 `ps`/`pgrep`/`lsof`。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**Result**
Skill + CLI compose and run. `bootstrap.py cli-path` locates the standalone build, and direct CLI calls return scan info from the `product=synthetic` DB (all exit 0).

**Commands Run**
- `python3.12 tool/bootstrap.py cli-path` → `/…/fixtures/oskm-cli.pyz` (candidate 1, `$OSKM_CLI` already exported by the env; `doctor` tags it `env, oskm-cli 1.0.0`).
- `env -u OSKM_CLI python3.12 tool/bootstrap.py --runtime-root runtime cli-path` → `runtime/oskm-cli.pyz` (candidate 3 works after copying the fixture in; candidate 2 source tree absent, as expected).
- `python3.12 "$CLI" --db "$DB" ask list_scans` and `ask get_scan_info` (plus `--scan-id 1`, plus `--product synthetic`) → `scan_id=1`, `product=synthetic`, `cpu_arch=arm64`, `workspace_root=/src`, `status=complete`, `2026-11-02T00:00:00Z`→`00:00:01Z`, 11 collectors all `complete` / `schema_version 4.0.0` / `record_count 1`, `attached_aliases: []`.
- `python3.12 tool/bootstrap.py --runtime-root runtime validate-db <db>` → `{"ok": true}`; `arch overview` confirms `product=synthetic, scan_id=1`.

**Gotchas Found**
- `sql --sql "SELECT * FROM scans"` → `TABLE_NOT_ALLOWED` (exit 5): the SQL sandbox only exposes the 21 registered business tables from `ask get_tables`; scan metadata must come from `list_scans` / `get_scan_info` / `diff_scans`. Sandbox itself is fine (`SELECT COUNT(*) FROM components` → `2`).
- CLI `validate-db` takes a positional path, not `--db`; `--db X validate-db` errors with `required: path`.
- `doctor` exits 1 for unrelated reasons only: `OSKM_DOWNLOAD_ENDPOINT` unset and no `knowledge.db` in `runtime/` (DB intentionally stays in `artifacts/synthetic/`). Python 3.12.16, CLI, and `oskm_runtime`/`oskm_cli`/`oskm_schema` all OK.

**Changes**
- Added `runtime/oskm-cli.pyz` (copy of fixture, sha256 `3e78cf73…` matches) and `answer.md` with full command/output log. `fixtures/` untouched, `~/.oskm` never accessed.

Want me to also drop a `.env` in `runtime/` so `doctor` goes fully green, or copy the synthetic DB to `runtime/knowledge.db` for the canonical `<runtime-root>/knowledge.db` invocation?
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e08-synthetic-database-smoke` · exit=0 · 324.8s

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
| 3 | 是否明确说明该场景只验证组合链路、不代表真实产品数据 | manual | 人工 | **Result** Skill + CLI compose and run. `bootstrap.py cli-path` locates the standalone build, and direct CLI calls return scan info from the `product=synthetic` DB (all exit 0).  **Commands Run** - `p
… [输出截断，完整内容见工作区] …
g the fixture in; candidate 2 source tree absent, as expected). - `python3.12 "$CLI" --db "$DB" ask  |
| 4 | 查询是只读的：合成库 sha256 未变 | auto | Pass | sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 |
| 5 | 工具没有联网 | auto | Pass | [] |
| 6 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
