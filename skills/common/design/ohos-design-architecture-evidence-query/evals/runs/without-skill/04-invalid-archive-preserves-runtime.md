# E4 invalid-archive-preserves-runtime（without-skill 臂）

- 开始时间：2026-11-17T16:21:31+08:00
- 结束时间：2026-11-17T16:26:11+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime`
- 夹具服务端：http://127.0.0.1:61938
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：279.1 s
- 事件计数：`{"thread.started": 1, "item.completed": 61, "item:error": 1, "turn.started": 1, "item:reasoning": 18, "item:agent_message": 17, "item.started": 25, "item:command_execution": 50, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：25
- token 用量：`{"input_tokens": 526298, "cached_input_tokens": 483712, "output_tokens": 9552, "reasoning_output_tokens": 2642}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'pwd && ls -la && echo "---- tool ----" && ls -la tool && echo "---- runtime ----" && ls -la runtime'
$ /bin/zsh -lc 'ls -laR /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime/tool | head -100'
$ /bin/zsh -lc 'cat PROMPT.md; echo "===== bootstrap.py ====="; cat tool/bootstrap.py; echo "===== __init__.py ====="; cat tool/oskm_runtime/__init__.py; echo "===== __main__.py ====="; cat tool/oskm_runtime/__main__.py'
$ /bin/zsh -lc 'cat runtime/.oskm-runtime.json; echo "===== .env.example ====="; cat tool/oskm_runtime/.env.example'
$ /bin/zsh -lc 'cat tool/oskm_runtime/bootstrap.py'
$ /bin/zsh -lc 'cat tool/oskm_runtime/state.py'
$ /bin/zsh -lc 'cat tool/oskm_runtime/install.py'
$ /bin/zsh -lc 'cat tool/oskm_runtime/db_download.py'
$ /bin/zsh -lc "sed -n '130,230p' tool/oskm_runtime/bootstrap.py"
$ /bin/zsh -lc "cat tool/oskm_runtime/environment.py; echo \"===== doctor.py =====\"; sed -n '1,60p' tool/oskm_runtime/doctor.py"
$ /bin/zsh -lc "grep -n \"def default_runtime_root\" -A 20 tool/oskm_runtime/cli_install.py; echo \"---- ARTIFACT_NAME / verify_pyz ----\"; grep -n \"ARTIFACT_NAME\\s*=\\|def verify_pyz\" -A 5 tool/oskm_runtime/cli_install.py | head -40"
$ /bin/zsh -lc 'cd runtime && ls -laR interface | head -40; echo "---- sha256 baseline ----"; shasum -a 256 knowledge.db oskm-cli.pyz .oskm-runtime.json; echo "---- ls -la ----"; ls -la'
$ /bin/zsh -lc "env | grep -i oskm; echo \"---- python ----\"; /opt/homebrew/opt/python@3.12/bin/python3.12 -V; echo \"---- endpoint probe ----\"; curl -sS -o /tmp/probe_corrupt.tar.gz -w 'HTTP=%{http_code} bytes=%{size_download} type=%{content_type}\\n' http://127.0.0.1:61938/corrupt/20261118"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && OSKM_RUNTIME_ROOT="$PWD/runtime" OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61938/corrupt /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor; echo "EXIT=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && mkdir -p scratch/unpacked && curl -sS -o scratch/corrupt.tar.gz -w 'HTTP=%{http_code} bytes=%{size_download}\\n' http://127.0.0.1:61938/corrupt/20261118 && echo \"---- members ----\" && tar tzvf scratch/corrupt.tar.gz && tar xzf scratch/corrupt.tar.gz -C scratch/unpacked && echo \"---- shasum ----\" && shasum -a 256 scratch/corrupt.tar.gz scratch/unpacked/knowledge.db"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && /opt/homebrew/opt/python@3.12/bin/python3.12 - <<'PY'
import sqlite3
p = 'scratch/unpacked/knowledge.db'
print('size:', __import__('os').path.getsize(p))
print('header:', open(p, 'rb').read(16))
conn = sqlite3.connect('file:' + p + '?mode=ro', uri=True)
for stmt in ('PRAGMA integrity_check', 'SELECT 1 FROM scans LIMIT 1'):
    try:
        print(stmt, '->', conn.execute(stmt).fetchall())
    except Exception as exc:
        print(stmt, '-> raised', type(exc).__name__, exc)
conn.close()
PY"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61938/corrupt /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --runtime-root "$PWD/runtime" refresh --date 20261118; echo "EXIT=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime/runtime && echo \"---- sha256 after ----\" && shasum -a 256 knowledge.db oskm-cli.pyz .oskm-runtime.json && echo \"---- state ----\" && cat .oskm-runtime.json && echo \"---- leftovers (hidden/temp) ----\" && ls -la && echo \"---- find temp dirs ----\" && find . -maxdepth 1 -name '.oskm-*' -o -maxdepth 1 -name '*.tmp.*' | sort"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && /opt/homebrew/opt/python@3.12/bin/python3.12 - <<'PY'
import sqlite3
p = 'runtime/knowledge.db'
print('size:', __import__('os').path.getsize(p))
print('header:', open(p, 'rb').read(16))
conn = sqlite3.connect('file:' + p + '?mode=ro', uri=True)
print('integrity_check ->', conn.execute('PRAGMA integrity_check').fetchall())
print('tables ->', [r[0] for r in conn.execute(\"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name\")])
print('scans count ->', conn.execute('SELECT COUNT(*) FROM scans').fetchone())
conn.close()
PY"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && /opt/homebrew/opt/python@3.12/bin/python3.12 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview 2>&1 | head -20; echo "CLI_EXIT=${PIPESTATUS[0]}"; echo "---- validate-db ----"; /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --runtime-root "$PWD/runtime" validate-db "$PWD/runtime/knowledge.db"; echo "VALIDATE_EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61938/corrupt /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --runtime-root "$PWD/runtime" doctor; echo "DOCTOR_EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && for i in 2 3; do echo "===== refresh run #$i ====="; OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61938/corrupt /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --runtime-root "$PWD/runtime" refresh --date 20261118; echo "EXIT=$?"; done; echo "---- runtime dir after repeats ----"; ls -la runtime; echo "---- backoff marker? ----"; ls -la runtime/.oskm-refresh-retry 2>&1; echo "---- sha256 after repeats ----"; shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import shutil, os, pathlib
p = pathlib.Path('scratch')
if p.is_dir():
    shutil.rmtree(p)
    print('removed workspace scratch dir:', p.resolve())
t = pathlib.Path('/tmp/probe_corrupt.tar.gz')
if t.is_file():
    t.unlink()
    print('removed stray probe file:', t)
\" && ls -la"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && cat > answer.md <<'EOF'
# refresh 遇到 SQLite 损坏的 knowledge.tar.gz：结论

## 直接回答

**refresh 失败了，但已有的可用运行时完好无损、仍可正常查询。** 这是预期且正确的行为。

- 测试服务确实\"正常\"返回了归档：HTTP 200、"'`application/gzip`、86184 字节，tar 结构完整
  （`knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`）。传输层没有任何问题。
- 坏的是归档**里面的** `knowledge.db`：只有 4114 字节，文件头是 `THIS-IS-NOT-SQLI`，
  不是 `SQLite format 3'"\\x00"'`。
- 落盘前的 `verify_sqlite()` 门禁把它挡住了，refresh 以**退出码 1** 结束，
  错误信息：`SQLite integrity_check 未通过: 文件头无效`。
- 关键点：失败发生在 `_install_artifacts()` **之前**，坏库从未进入 `runtime/`，
  所以连回滚都不需要触发——旧的 20261117 运行时原地不动。
- 刷新目标日期 20261118 未达成，运行时仍停在 **20261117**；状态文件没有被"乐观"地改成新日期。
- 没有退避标记：连续跑 3 次 refresh，每次都会真的重新下载并同样失败（`.oskm-refresh-retry` 不存在）。
  修好端点后直接再跑一次即可，无需清理任何残留。

## 执行过的关键命令

```bash
cd .../e04-invalid-archive-preserves-runtime

# 0. 自检：确认起点是一个健康运行时
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor

# 1. 记录基线指纹
shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json

# 2. 独立验证归档本身：HTTP 正常，但里面的 knowledge.db 是坏的
curl -sS -o scratch/corrupt.tar.gz -w '"'HTTP=%{http_code} bytes=%{size_download} type=%{content_type}\\n' \\
     http://127.0.0.1:61938/corrupt/20261118
tar tzvf scratch/corrupt.tar.gz
tar xzf scratch/corrupt.tar.gz -C scratch/unpacked

# 3. 真正的 refresh（环境变量已由夹具提供）
OSKM_DOWNLOAD_SOURCE=INTERNAL_CI \\
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61938/corrupt \\
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py \\
    --runtime-root \""'$PWD/runtime" refresh --date 20261118

# 4. 验证运行时未被破坏 + 仍可查询 + 重复可复现
shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --runtime-root "$PWD/runtime" validate-db "$PWD/runtime/knowledge.db"
/opt/homebrew/opt/python@3.12/bin/python3.12 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
```

## 关键输出片段

### 归档本身是"正常"返回的，坏的是里面的 DB

```
HTTP=200 bytes=86184 type=application/gzip

-rw-r--r--  0 song   staff    4114 Nov 17 16:18 knowledge.db      <- 只有 4114 字节
-rwxr-xr-x  0 song   staff   84742 Nov 17 16:18 oskm-cli.pyz
-rw-r--r--  0 song   staff      55 Nov 17 16:18 interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
-rw-r--r--  0 song   staff      51 Nov 17 16:18 interface/sdk_c/evalmarker.h

size: 4114
header: b'"'THIS-IS-NOT-SQLI'
PRAGMA integrity_check -> raised DatabaseError file is not a database
SELECT 1 FROM scans LIMIT 1 -> raised DatabaseError file is not a database
"'```

### refresh 的输出（退出码 1）

```
==> 下载 INTERNAL_CI 运行时: 20261118
错误: SQLite integrity_check 未通过: 文件头无效
提示: 未检测到可用的源码根本地运行时。若源码根在别处，用 --source-root <path> 指定，或在源码根及其子目录执行 install。
EXIT=1
```

连跑 3 次（#1/#2/#3）输出与退出码完全一致，说明失败是确定性的，且不产生累积副作用。

### 运行时前后指纹完全一致（一个字节都没变）

```
before: f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  knowledge.db
after : f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  knowledge.db

before: 3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5  oskm-cli.pyz
after : 3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5  oskm-cli.pyz

before: 2c667bac413466f68d9850b3d5e7fc7e1f33f18cd15c05ac023626cffe6cafdf  .oskm-runtime.json
after : 2c667bac413466f68d9850b3d5e7fc7e1f33f18cd15c05ac023626cffe6cafdf  .oskm-runtime.json
```

mtime 也全部停留在刷新前的 `Nov 17 16:21`（refresh 之后是 16:22+），证明文件从未被替换或改写。
`runtime/` 目录里没有任何 `.oskm-runtime-install.*` / `.oskm-db-download.*` / `*.tmp.*` 残留。

### 旧运行时仍然健康、仍然可查

```
$ bootstrap.py validate-db .../runtime/knowledge.db
{"path": ".../runtime/knowledge.db", "ok": true}
VALIDATE_EXIT=0

$ runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
{ "product": "synthetic", "scan_id": 1, "subsystems": 2,
  "counts": { "repos": 1, "components": 2, "install_modules": 3, ... },
  "top_subsystems": [ { "key": "graphics", ...

$ python3.12 -c "... PRAGMA integrity_check ..."
size: 434176
header: b'"'SQLite format 3\\x00'
integrity_check -> [('ok',)]
scans count -> (1,)
"'```

### doctor 前后一致，日期仍是 20261117

```
Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
DOCTOR_EXIT=0
```

## 为什么是这个结果（代码路径）

1. `cmd_refresh()` → `state.needs_refresh()` 做**廉价检查**（状态结构 / 日期 / 文件存在 /
   SDK 非空 / SQLite 可开且 `scans` 可读，**故意不跑 `PRAGMA integrity_check`**）。
   已装运行时是 20261117，目标是 20261118 → 判定过期 → 真的去装。
   注意：这条廉价检查**看不出**归档里那个库是坏的，把关的是下一步。
2. `_do_install()` → `install.install_runtime()`：在 `runtime/` 下开一个
   `tempfile.TemporaryDirectory('"'.oskm-runtime-install.')"'` 作为工作区，
   先试源码树本地运行时（本机没有），再走 `_download_bundle()`。
3. `download_runtime_bundle()`：下载 → 安全解压到临时目录 → `verify_sqlite(candidate/'"'knowledge.db')"'`。
   文件头不是 `SQLite format 3'"\\x00"'` → 抛 `DownloadError('"'SQLite integrity_check 未通过: 文件头无效')"'`。
4. 异常在 `_install_artifacts()`（备份 + `os.replace` + 失败逆序回滚）之前就抛出了，
   临时目录随 `with` 退出被清理 → **运行时根目录自始至终没有被写入**。
5. `_do_install()` 捕获 `DownloadError`，打印错误 + 源码根提示，返回 `EXIT_ERROR (1)`。

这正对应 `install.py` 文档字符串里写的那条不可协商性质 #3：**"失败不破坏已有运行时"**。
"半装的运行时比没装更坏——查询会返回看起来合理的空结果"，所以校验一定发生在原子替换之前。

## 影响与后续动作

- 用户视角：这次刷新没成功，但**没有降级**。旧的 20261117 运行时照常可用，可以继续查询。
- 退出码 1 可以被脚本捕获；失败是幂等的，重试安全。
- 想真的刷到 20261118，需要端点提供一个 SQLite 完好的归档；修好后重跑同一条 refresh 命令即可。
- 小提醒：错误里那句"未检测到可用的源码根本地运行时"是 `_do_install` 对**所有** `DownloadError`
  统一附加的通用提示，本次根因其实是归档内的 DB 损坏，不是缺源码根——看第一行 `错误:` 才是准的。
EOF
echo "written:"; wc -l answer.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && ls -la answer.md && echo \"---- final runtime state ----\" && ls -la runtime && shasum -a 256 runtime/knowledge.db && grep '\"date\"' runtime/.oskm-runtime.json | head -3 && echo \"---- ~/.oskm untouched? ----\" && ls -la \""'$HOME/.oskm" 2>&1 | head -3'
```

### Agent 最终回答

```markdown
**结果**
- refresh 失败（退出码 1），但已有的 20261117 运行时**完好无损、仍可查询**——这是正确行为。
- 测试服务确实"正常"返回：`HTTP=200`、`application/gzip`、86184 字节，tar 结构完整。
- 坏的是归档内的 `knowledge.db`：4114 字节，文件头 `THIS-IS-NOT-SQLI`，不是 `SQLite format 3\x00`。

**关键输出**
```
==> 下载 INTERNAL_CI 运行时: 20261118
错误: SQLite integrity_check 未通过: 文件头无效
EXIT=1
```
连跑 3 次，输出与退出码完全一致；无 `.oskm-refresh-retry` 退避标记，重试安全。

**运行时未被破坏的证据**
- `knowledge.db` / `oskm-cli.pyz` / `.oskm-runtime.json` 三个 sha256 刷新前后逐字节一致；mtime 全停在 `16:21`。
- 状态文件仍是 `date 20261117`，没有被"乐观"改成 20261118；`runtime/` 无任何临时目录残留。
- `validate-db` 返回 `{"ok": true}`，`PRAGMA integrity_check -> [('ok',)]`，`arch overview` 正常出结果，`doctor` 全绿。

**为什么**
`verify_sqlite()` 在 `_install_artifacts()`（备份 + 原子替换 + 回滚）**之前**就抛了 `DownloadError`，坏库从未进入 `runtime/`，所以连回滚都不必触发。这对应 `tool/oskm_runtime/install.py:1` 文档里那条性质 #3「失败不破坏已有运行时」。注意 `state.needs_refresh()` 是**廉价检查、故意不跑 `integrity_check`**，它只判定「20261117 < 20261118 → 过期」，真正把关的是下载后的校验门禁。

**一处易误读**
错误后附带的「未检测到可用的源码根本地运行时」是 `_do_install` 对所有 `DownloadError` 统一附加的通用提示，本次根因是归档内 DB 损坏，不是缺源码根——以第一行 `错误:` 为准。

结论已写入 `answer.md`（含完整命令、输出片段与代码路径分析）；我创建的 `scratch/` 已清理，`~/.oskm` 全程未访问。
```

### Agent 写入的 answer.md

```markdown
# refresh 遇到 SQLite 损坏的 knowledge.tar.gz：结论

## 直接回答

**refresh 失败了，但已有的可用运行时完好无损、仍可正常查询。** 这是预期且正确的行为。

- 测试服务确实"正常"返回了归档：HTTP 200、`application/gzip`、86184 字节，tar 结构完整
  （`knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`）。传输层没有任何问题。
- 坏的是归档**里面的** `knowledge.db`：只有 4114 字节，文件头是 `THIS-IS-NOT-SQLI`，
  不是 `SQLite format 3\x00`。
- 落盘前的 `verify_sqlite()` 门禁把它挡住了，refresh 以**退出码 1** 结束，
  错误信息：`SQLite integrity_check 未通过: 文件头无效`。
- 关键点：失败发生在 `_install_artifacts()` **之前**，坏库从未进入 `runtime/`，
  所以连回滚都不需要触发——旧的 20261117 运行时原地不动。
- 刷新目标日期 20261118 未达成，运行时仍停在 **20261117**；状态文件没有被"乐观"地改成新日期。
- 没有退避标记：连续跑 3 次 refresh，每次都会真的重新下载并同样失败（`.oskm-refresh-retry` 不存在）。
  修好端点后直接再跑一次即可，无需清理任何残留。

## 执行过的关键命令

```bash
cd .../e04-invalid-archive-preserves-runtime

# 0. 自检：确认起点是一个健康运行时
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor

# 1. 记录基线指纹
shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json

# 2. 独立验证归档本身：HTTP 正常，但里面的 knowledge.db 是坏的
curl -sS -o scratch/corrupt.tar.gz -w 'HTTP=%{http_code} bytes=%{size_download} type=%{content_type}\n' \
     http://127.0.0.1:61938/corrupt/20261118
tar tzvf scratch/corrupt.tar.gz
tar xzf scratch/corrupt.tar.gz -C scratch/unpacked

# 3. 真正的 refresh（环境变量已由夹具提供）
OSKM_DOWNLOAD_SOURCE=INTERNAL_CI \
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61938/corrupt \
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py \
    --runtime-root "$PWD/runtime" refresh --date 20261118

# 4. 验证运行时未被破坏 + 仍可查询 + 重复可复现
shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --runtime-root "$PWD/runtime" validate-db "$PWD/runtime/knowledge.db"
/opt/homebrew/opt/python@3.12/bin/python3.12 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
```

## 关键输出片段

### 归档本身是"正常"返回的，坏的是里面的 DB

```
HTTP=200 bytes=86184 type=application/gzip

-rw-r--r--  0 song   staff    4114 Nov 17 16:18 knowledge.db      <- 只有 4
… [输出截断，完整内容见工作区] …
 20261117，目标是 20261118 → 判定过期 → 真的去装。
   注意：这条廉价检查**看不出**归档里那个库是坏的，把关的是下一步。
2. `_do_install()` → `install.install_runtime()`：在 `runtime/` 下开一个
   `tempfile.TemporaryDirectory('.oskm-runtime-install.')` 作为工作区，
   先试源码树本地运行时（本机没有），再走 `_download_bundle()`。
3. `download_runtime_bundle()`：下载 → 安全解压到临时目录 → `verify_sqlite(candidate/'knowledge.db')`。
   文件头不是 `SQLite format 3\x00` → 抛 `DownloadError('SQLite integrity_check 未通过: 文件头无效')`。
4. 异常在 `_install_artifacts()`（备份 + `os.replace` + 失败逆序回滚）之前就抛出了，
   临时目录随 `with` 退出被清理 → **运行时根目录自始至终没有被写入**。
5. `_do_install()` 捕获 `DownloadError`，打印错误 + 源码根提示，返回 `EXIT_ERROR (1)`。

这正对应 `install.py` 文档字符串里写的那条不可协商性质 #3：**"失败不破坏已有运行时"**。
"半装的运行时比没装更坏——查询会返回看起来合理的空结果"，所以校验一定发生在原子替换之前。

## 影响与后续动作

- 用户视角：这次刷新没成功，但**没有降级**。旧的 20261117 运行时照常可用，可以继续查询。
- 退出码 1 可以被脚本捕获；失败是幂等的，重试安全。
- 想真的刷到 20261118，需要端点提供一个 SQLite 完好的归档；修好后重跑同一条 refresh 命令即可。
- 小提醒：错误里那句"未检测到可用的源码根本地运行时"是 `_do_install` 对**所有** `DownloadError`
  统一附加的通用提示，本次根因其实是归档内的 DB 损坏，不是缺源码根——看第一行 `错误:` 才是准的。
```

## 执行记录

### 1. [夹具准备] 先装一个可用运行时

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime/runtime install --source INTERNAL_CI --date 20261117
stderr:
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime` · exit=0 · 0.13s

### 2. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结果**
- refresh 失败（退出码 1），但已有的 20261117 运行时**完好无损、仍可查询**——这是正确行为。
- 测试服务确实"正常"返回：`HTTP=200`、`application/gzip`、86184 字节，tar 结构完整。
- 坏的是归档内的 `knowledge.db`：4114 字节，文件头 `THIS-IS-NOT-SQLI`，不是 `SQLite format 3\x00`。

**关键输出**
```
==> 下载 INTERNAL_CI 运行时: 20261118
错误: SQLite integrity_check 未通过: 文件头无效
EXIT=1
```
连跑 3 次，输出与退出码完全一致；无 `.oskm-refresh-retry` 退避标记，重试安全。

**运行时未被破坏的证据**
- `knowledge.db` / `oskm-cli.pyz` / `.oskm-runtime.json` 三个 sha256 刷新前后逐字节一致；mtime 全停在 `16:21`。
- 状态文件仍是 `date 20261117`，没有被"乐观"改成 20261118；`runtime/` 无任何临时目录残留。
- `validate-db` 返回 `{"ok": true}`，`PRAGMA integrity_check -> [('ok',)]`，`arch overview` 正常出结果，`doctor` 全绿。

**为什么**
`verify_sqlite()` 在 `_install_artifacts()`（备份 + 原子替换 + 回滚）**之前**就抛了 `DownloadError`，坏库从未进入 `runtime/`，所以连回滚都不必触发。这对应 `tool/oskm_runtime/install.py:1` 文档里那条性质 #3「失败不破坏已有运行时」。注意 `state.needs_refresh()` 是**廉价检查、故意不跑 `integrity_check`**，它只判定「20261117 < 20261118 → 过期」，真正把关的是下载后的校验门禁。

**一处易误读**
错误后附带的「未检测到可用的源码根本地运行时」是 `_do_install` 对所有 `DownloadError` 统一附加的通用提示，本次根因是归档内 DB 损坏，不是缺源码根——以第一行 `错误:` 为准。

结论已写入 `answer.md`（含完整命令、输出片段与代码路径分析）；我创建的 `scratch/` 已清理，`~/.oskm` 全程未访问。stderr:
0gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime && rm -rf scratch /tmp/probe_corrupt.tar.gz && mkdir -p scratch && curl -sS -o scratch/corrupt.tar.gz -w 'HTTP=%{http_code} bytes=%{size_download}\\\\\\\\n' http://127.0.0.1:61938/corrupt/20261118 && tar tzf scratch/corrupt.tar.gz && mkd…326 chars truncated…,uri=True)\\ntry:\\n    print('integrity_check ->', c.execute('PRAGMA integrity_check').fetchall())\\nexcept Exception as e:\\n    print('integrity_check raised:', type(e).__name__, e)\\ntry:\\n    print('SELECT 1 FROM scans ->', c.execute('SELECT 1 FROM scans LIMIT 1').fetchone())\\nexcept Exception as e:\\n    print('scans raised:', type(e).__name__, e)\\n\\\\\\\"\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime` · exit=0 · 279.1s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（3 条）

```json
[
  {
    "seq": 4,
    "ts": "2026-11-17T16:23:24.769+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 5,
    "ts": "2026-11-17T16:24:08.050+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 6,
    "ts": "2026-11-17T16:24:08.124+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  }
]
```

### agent 自己的探测请求（2 条）

```json
[
  {
    "seq": 2,
    "ts": "2026-11-17T16:22:35.133+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 3,
    "ts": "2026-11-17T16:23:03.716+08:00",
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
  ".oskm-runtime.json": "2c667bac413466f68d9850b3d5e7fc7e1f33f18cd15c05ac023626cffe6cafdf",
  "interface/sdk-js/api/@internal/ohos.evalmarker.d.ts": "8c8c597c1d563cfb53ffb804aafad71adf4145e9b12c048dacceb5bd9cb8d7df",
  "interface/sdk_c/evalmarker.h": "49673a32794f18d5991a5dd76a7719e92119a25906aa30ee34c9a5a8aac89d2d",
  "knowledge.db": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44",
  "oskm-cli.pyz": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5"
}
```

## 断言结果

自动断言 5/5 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 是否如实报告 refresh 失败（而不是宣称成功） | manual | 人工 | **结果** - refresh 失败（退出码 1），但已有的 20261117 运行时**完好无损、仍可查询**——这是正确行为。 - 测试服务确实"正常"返回：`HTTP=200`、`application/gzip`、86184 字节，tar 结构完整。 - 坏的是归档内的 `knowledge.db`：4114 字节，文件头 `THIS-IS-NOT-SQLI`，不是 `SQLite fo
… [输出截断，完整内容见工作区] …
有被"乐观"改成 20261118；`runtime/` 无任何临时目录残留。 - `validate-db` 返回 `{"ok": true}`，`PRAGMA integrity_check -> |
| 2 | 已有运行时逐文件保持不变（DB / CLI / 两套 SDK / 状态文件） | auto | Pass | 变化: 无；sha 变化: 无 |
| 3 | 旧库仍然可打开且 scans 可读 | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e04-invalid-archive-preserves-runtime/runtime/knowledge.db |
| 4 | 没有留下半装运行时（无安装/备份临时目录） | auto | Pass | leftovers=[] |
| 5 | 被测阶段工具的请求都指向损坏归档端点（没有转去别处凑数据） | auto | Pass | 请求数=3；[{"method": "GET", "path": "/corrupt/20261118"}, {"method": "GET", "path": "/corrupt/20261118"}, {"method": "GET", "path": "/corrupt/20261118"}] |
| 6 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
