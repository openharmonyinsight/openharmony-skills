# E4 invalid-archive-preserves-runtime（without-skill 臂）

- 开始时间：2026-11-17T15:37:03+08:00
- 结束时间：2026-11-17T15:43:01+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime`
- 夹具服务端：http://127.0.0.1:61290
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

已有可用运行时。现在使用一个 SQLite 损坏的 knowledge.tar.gz 执行 refresh，测试服务会正常返回该归档。请执行并报告结果。

## 期望结果（来自 evals.json）

refresh 以非零状态失败并报告归档校验错误；已有 knowledge.db、oskm-cli.pyz、两套 SDK 和状态文件保持不变，不得留下半装运行时。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| 失败 | `contains` |
| 已有运行时保持不变 | `contains` |
| 失败后不得替换任何旧产物或留下半装运行时 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：357.0 s
- 事件计数：`{"thread.started": 1, "item.completed": 63, "item:error": 1, "turn.started": 1, "item:reasoning": 24, "item:agent_message": 16, "item.started": 22, "item:command_execution": 44, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：22
- token 用量：`{"input_tokens": 667090, "cached_input_tokens": 622464, "output_tokens": 11086, "reasoning_output_tokens": 3979}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && ls -la && echo "--- tool ---" && find tool -maxdepth 3 -type f | head -50 && echo "--- runtime ---" && ls -la runtime && echo "--- fixtures ---" && ls -la fixtures 2>/dev/null'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && cat PROMPT.md && echo "=== runtime state ===" && cat runtime/.oskm-runtime.json && echo "=== tool files ===" && wc -l tool/bootstrap.py tool/oskm_runtime/*.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/tool && cat bootstrap.py oskm_runtime/__init__.py oskm_runtime/__main__.py oskm_runtime/environment.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/tool && cat oskm_runtime/bootstrap.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/tool && sed -n '125,190p' oskm_runtime/bootstrap.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/tool && cat oskm_runtime/db_download.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/tool && sed -n '165,320p' oskm_runtime/db_download.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/tool && cat oskm_runtime/install.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/tool && sed -n '160,300p' oskm_runtime/install.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/tool && cat oskm_runtime/state.py && echo \"=== .env.example ===\" && cat oskm_runtime/.env.example && echo \"=== find .env / .gn ===\" && cd .. && find . -maxdepth 4 \\( -name '.env' -o -name '.gn' \\) 2>/dev/null; echo \"ENV: SOURCE="'$OSKM_DOWNLOAD_SOURCE ENDPOINT=$OSKM_DOWNLOAD_ENDPOINT ROOT=$OSKM_RUNTIME_ROOT"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== baseline file list ===" && find runtime | sort && echo "=== baseline sha256 ===" && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json | tee /tmp/baseline.sha 2>/dev/null || true'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && mkdir -p .probe && find runtime | sort > .probe/before-files.txt && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json > .probe/before-sha.txt && cp runtime/.oskm-runtime.json .probe/before-state.json && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== doctor ===" && $PY tool/bootstrap.py --runtime-root runtime doctor; echo "doctor exit=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/.probe && curl -sS -D headers.txt -o knowledge.tar.gz 'http://127.0.0.1:61290/corrupt/20261118'; echo \"curl exit="'$?"; echo "--- headers ---"; cat headers.txt; echo "--- size/type ---"; ls -l knowledge.tar.gz; file knowledge.tar.gz; echo "--- members ---"; tar -tzvf knowledge.tar.gz; echo "--- sha256 ---"; shasum -a 256 knowledge.tar.gz'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/.probe && mkdir -p corrupt && tar -xzf knowledge.tar.gz -C corrupt && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && ls -l corrupt && echo "--- header ---" && head -c 16 corrupt/knowledge.db | xxd | head -2 && echo "--- integrity_check ---" && $PY - <<'"'EOF'
import sqlite3, pathlib
p = pathlib.Path('corrupt/knowledge.db').resolve()
print('size', p.stat().st_size)
con = sqlite3.connect(p.as_uri() + '?mode=ro', uri=True)
try:
    print('integrity_check ->', [r[0] for r in con.execute('PRAGMA integrity_check')])
except Exception as exc:
    print('integrity_check raised', type(exc).__name__, exc)
try:
    print('scans ->', con.execute('SELECT 1 FROM scans LIMIT 1').fetchone())
except Exception as exc:
    print('scans raised', type(exc).__name__, exc)
EOF"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY tool/bootstrap.py --runtime-root runtime refresh --date 20261118 2>&1 | tee .probe/refresh-output.txt; echo "refresh exit=${pipestatus[1]}"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && find runtime | sort > .probe/after-files.txt && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json > .probe/after-sha.txt && echo \"=== diff file list ===\" && diff .probe/before-files.txt .probe/after-files.txt && echo \"(identical)\" && echo \"=== diff sha256 ===\" && diff .probe/before-sha.txt .probe/after-sha.txt && echo \"(identical)\" && cat .probe/after-sha.txt && echo \"=== diff state file ===\" && diff .probe/before-state.json runtime/.oskm-runtime.json && echo \"(identical)\" && echo \"=== leftover temp artifacts in runtime? ===\" && find runtime -maxdepth 2 -name '.*' -o -maxdepth 2 -name '*.tmp*' | sort && echo \"(none beyond state file)\" && ls -la runtime"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== doctor ===" && $PY tool/bootstrap.py --runtime-root runtime doctor 2>&1 | tee .probe/doctor-after.txt | sed -n '"'5,7p'; echo \"=== validate-db (installed CLI schema gate) ===\" && "'$PY tool/bootstrap.py --runtime-root runtime validate-db runtime/knowledge.db 2>&1 | tail -5; echo "validate-db exit=$?"; echo "=== real query through installed CLI ===" && $PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview 2>&1 | head -12; echo "cli exit=$?"; echo "=== refresh without --date (cheap up-to-date check) ===" && $PY tool/bootstrap.py --runtime-root runtime refresh 2>&1; echo "refresh-nodate exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && for i in 2 3; do echo "--- attempt $i ---"; $PY tool/bootstrap.py --runtime-root runtime refresh --date 20261118; echo "exit=$?"; done 2>&1 | tee .probe/refresh-repeat.txt; echo "=== hashes after 3 failed attempts ==="; shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json > .probe/after3-sha.txt; diff .probe/before-sha.txt .probe/after3-sha.txt && echo "(still identical)"; find runtime | sort > .probe/after3-files.txt; diff .probe/before-files.txt .probe/after3-files.txt && echo "(file list still identical)"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/.probe && rm knowledge.tar.gz && rm -r corrupt && ls -la'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/tool && grep -n \"def verify_sqlite\\|def download_runtime_bundle\\|verify(candidate\\|def _download_bundle\\|def _install_artifacts\\|def install_runtime\\|oskm-runtime-install\\|oskm-runtime-download\" oskm_runtime/db_download.py oskm_runtime/install.py && grep -n \"except DownloadError as exc\\|EXIT_ERROR = \\|def _do_install\\|def cmd_refresh\\|needs_refresh\" oskm_runtime/bootstrap.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && cat > answer.md <<'EOF'
# 结论

用 SQLite 已损坏的 "'`knowledge.tar.gz` 跑 `refresh --date 20261118`：

- **refresh 失败，退出码 1**，报错 `错误: SQLite integrity_check 未通过: 文件头无效`。
- **已有的可用运行时（20261117）完好无损**：文件清单、`knowledge.db` / `oskm-cli.pyz` / `.oskm-runtime.json` 三个文件的 sha256、mtime 与刷新前逐字节一致；状态文件仍停在 `date: 20261117`；`runtime/` 下没有任何残留临时目录或 `.tmp` 文件。
- **旧运行时仍然可用**：`doctor` 全 ✓、`validate-db` 返回 `{"ok": true}`、通过已装 CLI 的 `arch overview` 能查出数据、不带 `--date` 的 `refresh` 判定“已是最新”并退出 0。
- 连跑 3 次失败刷新，结果完全一致，运行时始终未被破坏。

即：损坏归档被“下载成功但在落盘前的 SQLite 校验闸门”拦下，安装从未开始，符合 `install.py` 文档里第 3 条不可协商性质“失败不破坏已有运行时”。

# 环境

```
OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61290/corrupt
OSKM_RUNTIME_ROOT=<workspace>/runtime        # 三条 env 已在 shell 中导出
Python 3.12.16 (/opt/homebrew/opt/python@3.12/bin/python3.12)
```

# 关键命令与输出

## 1. 刷新前基线（doctor + 哈希）

```
$ python3.12 tool/bootstrap.py --runtime-root runtime doctor
Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
doctor exit=0

$ shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  runtime/knowledge.db
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  runtime/oskm-cli.pyz
e69a21dfb000608193046e8ee55c02aaf2d47d7cf9bd  runtime/.oskm-runtime.json
```

（前两个哈希与状态文件里记录的 `db.sha256` / `cli.sha256` 一致。）

## 2. 确认夹具端点确实“正常返回”一个损坏归档

```
$ curl -sS -D headers.txt -o knowledge.tar.gz '"'http://127.0.0.1:61290/corrupt/20261118'
HTTP/1.1 200 OK
Server: oskm-eval-fixture/1.0 Python/3.12.16
Content-Type: application/gzip
Content-Length: 85166

"'$ tar -tzvf knowledge.tar.gz
knowledge.db                                   4114 字节
oskm-cli.pyz                                  83741
interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
interface/sdk_c/evalmarker.h

$ head -c 16 corrupt/knowledge.db | xxd
00000000: 5448 4953 2d49 532d 4e4f 542d 5351 4c49  THIS-IS-NOT-SQLI

$ python3.12 -c "…PRAGMA integrity_check…"
integrity_check raised DatabaseError file is not a database
```

归档结构、HTTP 状态、Content-Type 全部正常 —— 唯一的问题就是里面的 `knowledge.db` 不是 SQLite（头部被写成 `THIS-IS-NOT-SQLI…`）。

## 3. 执行 refresh（目标日期 20261118）

```
$ python3.12 tool/bootstrap.py --runtime-root runtime refresh --date 20261118
==> 下载 INTERNAL_CI 运行时: 20261118
错误: SQLite integrity_check 未通过: 文件头无效
提示: 未检测到可用的源码根本地运行时。若源码根在别处，用 --source-root <path> 指定，或在源码根及其子目录执行 install。
refresh exit=1
```

## 4. 刷新后对比：运行时逐字节未变

```
$ diff .probe/before-files.txt .probe/after-files.txt   # 文件清单
(identical)
$ diff .probe/before-sha.txt   .probe/after-sha.txt     # 三个关键文件 sha256
(identical)
$ diff .probe/before-state.json runtime/.oskm-runtime.json
(identical)          # 仍是 version 3 / date 20261117
$ find runtime -maxdepth 2 -name '"'.*' -o -name '*.tmp*'
runtime/.oskm-runtime.json      # 没有 .oskm-runtime-install.* / .oskm-runtime-backup.* / *.tmp.* 残留
"'```

## 5. 旧运行时仍能正常服务查询

```
$ python3.12 tool/bootstrap.py --runtime-root runtime validate-db runtime/knowledge.db
{"path": "runtime/knowledge.db", "ok": true}          exit=0

$ python3.12 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
{ "product": "synthetic", "scan_id": 1, "subsystems": 2, "counts": { "repos": 1, … } }   exit=0

$ python3.12 tool/bootstrap.py --runtime-root runtime refresh      # 不带 --date
==> 运行时已是最新，无需刷新: <workspace>/runtime                    exit=0
```

## 6. 重复失败刷新不累积损伤

```
$ for i in 2 3; do python3.12 tool/bootstrap.py --runtime-root runtime refresh --date 20261118; done
（两次输出与第 1 次完全相同，exit=1）
$ diff .probe/before-sha.txt .probe/after3-sha.txt   → (still identical)
$ diff .probe/before-files.txt .probe/after3-files.txt → (file list still identical)
```

# 为什么是这个结果（代码路径）

1. `cmd_refresh` 先用廉价检查判断是否过期（`tool/oskm_runtime/bootstrap.py:193`）。`--date 20261118` ≠ 状态里的 `20261117`，所以 `needs_refresh` 为真，真的进入安装流程（不带 `--date` 时今天是 20261117，判定“已是最新”直接退出 0，不会发请求）。
2. `install_runtime` 在 `runtime/` 下开一个 `.oskm-runtime-install.*` 临时工作目录（`tool/oskm_runtime/install.py:433`），先试源码树本地运行时（本工作区不是 OpenHarmony 源码根，没有 `.gn`/`out`），于是回退下载。
3. `download_runtime_bundle`（`tool/oskm_runtime/db_download.py:493`）顺序是：下载 → `extract_runtime` 安全解压 → **`verify(candidate / '"'knowledge.db')"'`（`tool/oskm_runtime/db_download.py:521`）** → 才 `shutil.move` 到输出目录。
4. `verify_sqlite`（`tool/oskm_runtime/db_download.py:421`）第一步就比对 16 字节魔数 `SQLite format 3'"\\0"'`；夹具的库是 `THIS-IS-NOT-SQLI…`，直接抛 `DownloadError('"'SQLite integrity_check 未通过: 文件头无效')"'`。因此损坏文件从未离开 `TemporaryDirectory`，异常退出时临时目录被整体删除。
5. 因为失败发生在 `download_runtime_bundle` 内部，后面的 schema 契约校验（`_download_bundle` 里的 `bundle_validator`，`tool/oskm_runtime/install.py:390`）和真正的落盘 `_install_artifacts`（`tool/oskm_runtime/install.py:252`，`os.replace` + 逆序回滚）**根本没有被调用** —— 这就是运行时零改动、也没有备份目录残留的原因。
6. `_do_install` 捕获 `DownloadError`（`tool/oskm_runtime/bootstrap.py:158`），打印 `错误: …` 与提示，返回 `EXIT_ERROR = 1`。

# 一个可以改进的小点（非本次任务范围）

失败时附带的那句“提示: 未检测到可用的源码根本地运行时…”是 `DownloadError` 分支的固定文案。本例并不是找不到源码根，而是归档里的 DB 没通过完整性校验，这句提示会把人往错误的方向引；按异常类型区分提示会更准确。

# 产物

- 本报告：`answer.md`
- 证据文件（前后哈希/清单/diff、doctor 输出、refresh 输出、响应头）：`.probe/`
- 未访问、未修改 `~/.oskm`；未修改 `fixtures`；下载的损坏归档副本已删除，只保留文本证据。
EOF
echo "written:"; wc -l answer.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && /opt/homebrew/opt/python@3.12/bin/python3.12 - <<'EOF'
import pathlib
p = pathlib.Path('answer.md')
text = p.read_text(encoding='utf-8')
bad = 'e69a21dfb000608193046e8ee55c02aaf2d47d7cf9bd'
good = 'e69a21dfb000608193046e8bb01e187e8e8adb16ea8ee55c02aaf2d47d7cf9bd'
assert text.count(bad) == 1, text.count(bad)
p.write_text(text.replace(bad, good), encoding='utf-8')
print('fixed')
EOF
grep -n \"oskm-runtime.json"'$" answer.md | head -5; echo "--- verify against real hash ---"; shasum -a 256 runtime/.oskm-runtime.json'
```

### Agent 最终回答

```markdown
**结果**
- `refresh --date 20261118` **失败，退出码 1**：`错误: SQLite integrity_check 未通过: 文件头无效`（前面有 `==> 下载 INTERNAL_CI 运行时: 20261118`，说明 HTTP 200 与解压都成功了，卡在落盘前的 SQLite 校验）。
- **已装的 20261117 运行时完好无损**：文件清单、`runtime/knowledge.db`、`runtime/oskm-cli.pyz`、`runtime/.oskm-runtime.json` 的 sha256 与 mtime 全部与刷新前一致，状态仍是 `date: 20261117`，`runtime/` 下无 `.oskm-runtime-install.*` / `.oskm-runtime-backup.*` / `*.tmp*` 残留。
- **旧运行时仍可服务**：`doctor` 全 ✓、`validate-db` → `{"ok": true}`、`runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview` 正常出数据、不带 `--date` 的 `refresh` → “运行时已是最新，无需刷新” 退出 0。
- 连跑 3 次失败刷新，结果一致，运行时无累积损伤。

**为什么**
- `download_runtime_bundle` 的顺序是下载 → 安全解压 → `verify(candidate/'knowledge.db')`（tool/oskm_runtime/db_download.py:521）→ 才 `shutil.move`；`verify_sqlite`（tool/oskm_runtime/db_download.py:421）先比对 16 字节魔数，夹具的库头是 `THIS-IS-NOT-SQLI…`，于是抛 `DownloadError`，临时目录随异常整体删除。
- schema 校验与 `_install_artifacts`（tool/oskm_runtime/install.py:252，`os.replace` + 逆序回滚）根本没被调用，所以运行时零改动；`_do_install`（tool/oskm_runtime/bootstrap.py:158）捕获后打印错误并返回 1。

**产物**
- 报告：`answer.md`（含关键命令、输出片段、代码路径解释）。
- 证据：`.probe/`（前后哈希/清单 diff、doctor 与 refresh 输出、响应头）；下载的损坏归档副本已删除。未触碰 `~/.oskm` 与 fixtures。

一个小观察：失败时固定附带的“提示: 未检测到可用的源码根本地运行时…”文案与本例无关（真实原因是归档校验未过），容易误导，建议按异常类型区分。需要我改这条提示吗？
```

### Agent 写入的 answer.md

```markdown
# 结论

用 SQLite 已损坏的 `knowledge.tar.gz` 跑 `refresh --date 20261118`：

- **refresh 失败，退出码 1**，报错 `错误: SQLite integrity_check 未通过: 文件头无效`。
- **已有的可用运行时（20261117）完好无损**：文件清单、`knowledge.db` / `oskm-cli.pyz` / `.oskm-runtime.json` 三个文件的 sha256、mtime 与刷新前逐字节一致；状态文件仍停在 `date: 20261117`；`runtime/` 下没有任何残留临时目录或 `.tmp` 文件。
- **旧运行时仍然可用**：`doctor` 全 ✓、`validate-db` 返回 `{"ok": true}`、通过已装 CLI 的 `arch overview` 能查出数据、不带 `--date` 的 `refresh` 判定“已是最新”并退出 0。
- 连跑 3 次失败刷新，结果完全一致，运行时始终未被破坏。

即：损坏归档被“下载成功但在落盘前的 SQLite 校验闸门”拦下，安装从未开始，符合 `install.py` 文档里第 3 条不可协商性质“失败不破坏已有运行时”。

# 环境

```
OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61290/corrupt
OSKM_RUNTIME_ROOT=<workspace>/runtime        # 三条 env 已在 shell 中导出
Python 3.12.16 (/opt/homebrew/opt/python@3.12/bin/python3.12)
```

# 关键命令与输出

## 1. 刷新前基线（doctor + 哈希）

```
$ python3.12 tool/bootstrap.py --runtime-root runtime doctor
Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
doctor exit=0

$ shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  runtime/knowledge.db
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  runtime/oskm-cli.pyz
e69a21dfb000608193046e8bb01e187e8e8adb16ea8ee55c02aaf2d47d7cf9bd  runtime/.oskm-runtime.json
```

（前两个哈希与状态文件里记录的 `db.sha256` / `cli.sha256` 一致。）

## 2. 确认夹具端点确实“正常返回”一个损坏归档

```
$ curl -sS -D headers.txt -o knowledge.tar.gz 'http://127.0.0.1:61290/corrupt/20261118'
HTTP/1.1 200 OK
Server: oskm-eval-fixture/1.0 Python/3.12.16
Content-Type: application/gzip
Content-Length: 85166

$ tar -tzvf knowledge.tar.gz
knowledge.db                                   4114 字节
oskm-cli.pyz                                  83741
interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
interface/sdk_c/evalmarker.h

$ head -c 16 corrupt/knowledge.db | xxd
00000000: 5448 4953 2d49 532d 4e4f 542d 53
… [输出截断，完整内容见工作区] …
 → `extract_runtime` 安全解压 → **`verify(candidate / 'knowledge.db')`（`tool/oskm_runtime/db_download.py:521`）** → 才 `shutil.move` 到输出目录。
4. `verify_sqlite`（`tool/oskm_runtime/db_download.py:421`）第一步就比对 16 字节魔数 `SQLite format 3\0`；夹具的库是 `THIS-IS-NOT-SQLI…`，直接抛 `DownloadError('SQLite integrity_check 未通过: 文件头无效')`。因此损坏文件从未离开 `TemporaryDirectory`，异常退出时临时目录被整体删除。
5. 因为失败发生在 `download_runtime_bundle` 内部，后面的 schema 契约校验（`_download_bundle` 里的 `bundle_validator`，`tool/oskm_runtime/install.py:390`）和真正的落盘 `_install_artifacts`（`tool/oskm_runtime/install.py:252`，`os.replace` + 逆序回滚）**根本没有被调用** —— 这就是运行时零改动、也没有备份目录残留的原因。
6. `_do_install` 捕获 `DownloadError`（`tool/oskm_runtime/bootstrap.py:158`），打印 `错误: …` 与提示，返回 `EXIT_ERROR = 1`。

# 一个可以改进的小点（非本次任务范围）

失败时附带的那句“提示: 未检测到可用的源码根本地运行时…”是 `DownloadError` 分支的固定文案。本例并不是找不到源码根，而是归档里的 DB 没通过完整性校验，这句提示会把人往错误的方向引；按异常类型区分提示会更准确。

# 产物

- 本报告：`answer.md`
- 证据文件（前后哈希/清单/diff、doctor 输出、refresh 输出、响应头）：`.probe/`
- 未访问、未修改 `~/.oskm`；未修改 `fixtures`；下载的损坏归档副本已删除，只保留文本证据。
```

## 执行记录

### 1. [夹具准备] 先装一个可用运行时

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/runtime install --source INTERNAL_CI --date 20261117
stderr:
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime` · exit=0 · 0.1s

### 2. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结果**
- `refresh --date 20261118` **失败，退出码 1**：`错误: SQLite integrity_check 未通过: 文件头无效`（前面有 `==> 下载 INTERNAL_CI 运行时: 20261118`，说明 HTTP 200 与解压都成功了，卡在落盘前的 SQLite 校验）。
- **已装的 20261117 运行时完好无损**：文件清单、`runtime/knowledge.db`、`runtime/oskm-cli.pyz`、`runtime/.oskm-runtime.json` 的 sha256 与 mtime 全部与刷新前一致，状态仍是 `date: 20261117`，`runtime/` 下无 `.oskm-runtime-install.*` / `.oskm-runtime-backup.*` / `*.tmp*` 残留。
- **旧运行时仍可服务**：`doctor` 全 ✓、`validate-db` → `{"ok": true}`、`runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview` 正常出数据、不带 `--date` 的 `refresh` → “运行时已是最新，无需刷新” 退出 0。
- 连跑 3 次失败刷新，结果一致，运行时无累积损伤。

**为什么**
- `download_runtime_bundle` 的顺序是下载 → 安全解压 → `verify(candidate/'knowledge.db')`（tool/oskm_runtime/db_download.py:521）→ 才 `shutil.move`；`verify_sqlite`（tool/oskm_runtime/db_download.py:421）先比对 16 字节魔数，夹具的库头是 `THIS-IS-NOT-SQLI…`，于是抛 `DownloadError`，临时目录随异常整体删除。
- schema 校验与 `_install_artifacts`（tool/oskm_runtime/install.py:252，`os.replace` + 逆序回滚）根本没被调用，所以运行时零改动；`_do_install`（tool/oskm_runtime/bootstrap.py:158）捕获后打印错误并返回 1。

**产物**
- 报告：`answer.md`（含关键命令、输出片段、代码路径解释）。
- 证据：`.probe/`（前后哈希/清单 diff、doctor 与 refresh 输出、响应头）；下载的损坏归档副本已删除。未触碰 `~/.oskm` 与 fixtures。

一个小观察：失败时固定附带的“提示: 未检测到可用的源码根本地运行时…”文案与本例无关（真实原因是归档校验未过），容易误导，建议按异常类型区分。需要我改这条提示吗？stderr:
2026-11-17T07:39:05.589462Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime && rm -f /tmp/baseline.sha && mkdir -p .probe && find runtime | sort > .probe/before-files.txt && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json > .probe/before-sha.txt && cp runtime/.oskm-runtime.json .probe/before-state.json && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo \\\"=== doctor ===\\\" && $PY tool/bootstrap.py --runtime-root runtime doctor; echo \\\"doctor exit=$?\\\"'` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime` · exit=0 · 357.0s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（3 条）

```json
[
  {
    "seq": 3,
    "ts": "2026-11-17T15:39:51.503+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 4,
    "ts": "2026-11-17T15:40:46.047+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 5,
    "ts": "2026-11-17T15:40:46.121+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  }
]
```

### agent 自己的探测请求（1 条）

```json
[
  {
    "seq": 2,
    "ts": "2026-11-17T15:39:25.817+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  }
]
```

## 被测前状态

```json
{
  ".oskm-runtime.json": "e69a21dfb000608193046e8bb01e187e8e8adb16ea8ee55c02aaf2d47d7cf9bd",
  "interface/sdk-js/api/@internal/ohos.evalmarker.d.ts": "8c8c597c1d563cfb53ffb804aafad71adf4145e9b12c048dacceb5bd9cb8d7df",
  "interface/sdk_c/evalmarker.h": "49673a32794f18d5991a5dd76a7719e92119a25906aa30ee34c9a5a8aac89d2d",
  "knowledge.db": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44",
  "oskm-cli.pyz": "ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e"
}
```

## 断言结果

自动断言 5/5 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 是否如实报告 refresh 失败（而不是宣称成功） | manual | 人工 | **结果** - `refresh --date 20261118` **失败，退出码 1**：`错误: SQLite integrity_check 未通过: 文件头无效`（前面有 `==> 下载 INTERNAL_CI 运行时: 20261118`，说明 HTTP 200 与解压都成功了，卡在落盘前的 SQLite 校验）。 - **已装的 20261117 运行时完好无损**：文件清单、`r
… [输出截断，完整内容见工作区] …
wledge.db arch overview` 正常出数据、不带 `--date` 的 `refresh` → “运行时已是最新，无需刷新” 退出 0。 - 连跑 3 次失败刷新，结果一致，运行时无 |
| 2 | 已有运行时逐文件保持不变（DB / CLI / 两套 SDK / 状态文件） | auto | Pass | 变化: 无；sha 变化: 无 |
| 3 | 旧库仍然可打开且 scans 可读 | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e04-invalid-archive-preserves-runtime/runtime/knowledge.db |
| 4 | 没有留下半装运行时（无安装/备份临时目录） | auto | Pass | leftovers=[] |
| 5 | 被测阶段工具的请求都指向损坏归档端点（没有转去别处凑数据） | auto | Pass | 请求数=3；[{"method": "GET", "path": "/corrupt/20261118"}, {"method": "GET", "path": "/corrupt/20261118"}, {"method": "GET", "path": "/corrupt/20261118"}] |
| 6 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
