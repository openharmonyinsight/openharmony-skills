# E7 refresh-is-explicit（without-skill 臂）

- 开始时间：2026-11-17T15:42:34+08:00
- 结束时间：2026-11-17T15:51:55+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit`
- 夹具服务端：http://127.0.0.1:61481
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

一个托管运行时已经过期，但用户只是直接执行 oskm-cli 查询，没有运行 refresh。请说明是否会下载，以及用户应如何更新运行时；再说明没有 .oskm-runtime.json 的自管库会怎样。

## 期望结果（来自 evals.json）

直接查询不会触发下载，应显式执行 bootstrap.py refresh 或 install；没有 .oskm-runtime.json 的自管库不会被刷新或覆盖。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| 查询不会自动下载 | `contains` |
| bootstrap.py refresh | `contains` |
| 自管库不会被刷新或覆盖 | `contains` |
| 刷新必须是显式动作，查询没有下载副作用 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：560.1 s
- 事件计数：`{"thread.started": 1, "item.completed": 78, "item:error": 1, "turn.started": 1, "item:reasoning": 27, "item:agent_message": 11, "item.started": 39, "item:command_execution": 78, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：39
- token 用量：`{"input_tokens": 959187, "cached_input_tokens": 897280, "output_tokens": 19091, "reasoning_output_tokens": 7578}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc "pwd; ls -la; echo '--- runtime ---'; ls -la runtime 2>/dev/null; echo '--- unmanaged ---'; ls -la unmanaged 2>/dev/null; echo '--- tool ---'; ls -la tool 2>/dev/null"
$ /bin/zsh -lc "find . -maxdepth 3 -name '*.json' -o -maxdepth 3 -name 'AGENTS.md' | head -50"
$ /bin/zsh -lc "cat PROMPT.md; echo '=== state ==='; cat runtime/.oskm-runtime.json; echo; echo '=== bootstrap ==='; cat tool/bootstrap.py; echo '=== tool tree ==='; find tool -type f | sort"
$ /bin/zsh -lc 'ls -la runtime/interface; find runtime/interface -type f | head -30'
$ /bin/zsh -lc "cd tool/oskm_runtime && wc -l *.py .env.example && echo '=== bootstrap.py ===' && cat bootstrap.py && echo '=== __main__.py ===' && cat __main__.py && echo '=== .env.example ===' && cat .env.example"
$ /bin/zsh -lc "cd tool/oskm_runtime && echo '=== state.py ===' && cat state.py && echo '=== environment.py ===' && cat environment.py"
$ /bin/zsh -lc "cd tool/oskm_runtime && sed -n '120,177p' state.py"
$ /bin/zsh -lc "cd tool/oskm_runtime && sed -n '1,120p' cli_install.py"
$ /bin/zsh -lc "cd tool/oskm_runtime && grep -n \"unmanaged\\|load_state\\|needs_refresh\\|def \" install.py | head -60"
$ /bin/zsh -lc "cd tool/oskm_runtime && sed -n '150,303p' bootstrap.py"
$ /bin/zsh -lc "cd tool/oskm_runtime && grep -n \"default_runtime_root\" -A 12 cli_install.py | head -40; echo '=== doctor ==='; cat doctor.py"
$ /bin/zsh -lc "cd tool/oskm_runtime && sed -n '400,451p' install.py; echo '=== build_state/_install_artifacts ==='; sed -n '245,360p' install.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY -V && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json unmanaged/knowledge.db && stat -f '"'%Sm %N' -t '%F %T' runtime/knowledge.db runtime/.oskm-runtime.json unmanaged/knowledge.db"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && mkdir -p work/pyz1 && cd work/pyz1 && unzip -q ../../runtime/oskm-cli.pyz && ls && echo '=== files ===' && find . -name '*.py' | sort"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY - <<'"'EOF'
import zipfile
z = zipfile.ZipFile('runtime/oskm-cli.pyz')
names = z.namelist()
print(len(names), 'entries')
for n in sorted(names):
    print(' ', n)
EOF"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY - <<'"'EOF'
import re, zipfile
z = zipfile.ZipFile('runtime/oskm-cli.pyz')
pat = re.compile(r'urllib|requests|http://|https://|socket|needs_refresh|oskm_runtime|bootstrap|download|refresh|\\.oskm-runtime', re.I)
hits = {}
for n in z.namelist():
    if not n.endswith('.py'):
        continue
    text = z.read(n).decode('utf-8', 'replace')
    found = [f'{i+1}: {line.strip()[:120]}' for i, line in enumerate(text.splitlines()) if pat.search(line)]
    if found:
        hits[n] = found
for n, found in sorted(hits.items()):
    print(f'--- {n} ({len(found)})')
    for line in found[:12]:
        print('   ', line)
print('total files with hits:', len(hits))
EOF"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY - <<'"'EOF'
import re, zipfile
z = zipfile.ZipFile('runtime/oskm-cli.pyz')
pat = re.compile(r'urlopen|urlretrieve|http\\.client|socket\\.|subprocess|os\\.system')
for n in z.namelist():
    if not n.endswith('.py'):
        continue
    text = z.read(n).decode('utf-8','replace')
    for i, line in enumerate(text.splitlines(), 1):
        if pat.search(line):
            print(f'{n}:{i}: {line.strip()[:140]}')
print('--- cli.py head 130 ---')
print('\\n'.join(z.read('oskm_cli/cli.py').decode().splitlines()[:130]))
EOF"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal OSKM_RUNTIME_ROOT=$PWD/runtime && $PY tool/bootstrap.py doctor; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_RUNTIME_ROOT=$PWD/runtime && $PY runtime/oskm-cli.pyz --version; $PY runtime/oskm-cli.pyz --help 2>&1 | head -40'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_RUNTIME_ROOT=$PWD/runtime && $PY - <<'"'EOF'
import sys
sys.path.insert(0, 'tool')
from oskm_runtime import state
from pathlib import Path
print('today() =', state.today())
for label, db in (('managed runtime', 'runtime/knowledge.db'), ('unmanaged', 'unmanaged/knowledge.db')):
    p = Path(db).resolve()
    print(f'{label}: needs_refresh={state.needs_refresh(p)}  state_file={state.state_path(p).is_file()}  db_usable={state.database_is_usable(p)}')
EOF"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal && echo '### query 1: arch overview (real endpoint configured)' && "'$PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview 2>&1 | head -25; echo "exit=${PIPESTATUS[0]:-$?}"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo '### before' && shasum -a 256 runtime/knowledge.db runtime/.oskm-runtime.json && echo '### queries with a DEAD endpoint (closed port 9) to prove the query path never dials out' && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:9/dead && "'$PY runtime/oskm-cli.pyz --db runtime/knowledge.db ask --list 2>&1 | head -8; echo "ask_exit=$?"; $PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table arch overview 2>&1 | tail -6; echo "arch_exit=$?"; $PY runtime/oskm-cli.pyz --db runtime/knowledge.db sql --query '"'select count(*) from components' 2>&1 | head -8; echo \"sql_exit="'$?"; echo '"'### after' && shasum -a 256 runtime/knowledge.db runtime/.oskm-runtime.json && cat runtime/.oskm-runtime.json | head -6"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:9/dead && $PY runtime/oskm-cli.pyz sql --help 2>&1 | head -20; echo '"'### real sql query against stale managed db'; "'$PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table sql '"'select name from components order by name limit 5' 2>&1 | head -12; echo \"exit="'$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_RUNTIME_ROOT=$PWD/runtime && echo '"'### bootstrap.py refuses query subcommands' && "'$PY tool/bootstrap.py arch overview; echo "exit=$?"; echo '"'### unknown/ask also refused'; "'$PY tool/bootstrap.py ask --list; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:9/dead && $PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table sql --sql '"'select name from components order by name limit 5'; echo \"exit="'$?"; echo '"'### same query against the UNMANAGED db'; "'$PY runtime/oskm-cli.pyz --db unmanaged/knowledge.db --format table sql --sql '"'select name from components order by name limit 5'; echo \"exit="'$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && cp -a runtime work/runtime-copy && cp -a unmanaged work/unmanaged-copy && ls -la work/runtime-copy work/unmanaged-copy && shasum -a 256 work/runtime-copy/knowledge.db work/unmanaged-copy/knowledge.db'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal OSKM_RUNTIME_ROOT=$PWD/work/runtime-copy && time $PY tool/bootstrap.py --runtime-root work/runtime-copy refresh; echo "exit=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && echo '### refreshed copy state' && cat work/runtime-copy/.oskm-runtime.json && echo '### hashes' && shasum -a 256 work/runtime-copy/knowledge.db work/runtime-copy/oskm-cli.pyz && echo '### fixture runtime UNCHANGED?' && shasum -a 256 runtime/knowledge.db runtime/.oskm-runtime.json && grep '\"date\"' runtime/.oskm-runtime.json | head -2 && ls -a work/runtime-copy"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal OSKM_RUNTIME_ROOT=$PWD/work/runtime-copy && echo '"'### refresh again (already fresh) — should be a no-op, no download' && "'$PY tool/bootstrap.py --runtime-root work/runtime-copy refresh; echo "exit=$?"; echo '"'### refresh with a DEAD endpoint on the fresh copy — still no-op (no download attempted)'; OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:9/dead "'$PY tool/bootstrap.py --runtime-root work/runtime-copy refresh; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal OSKM_RUNTIME_ROOT=$PWD/unmanaged && echo '"'### doctor on the unmanaged dir' && "'$PY tool/bootstrap.py --runtime-root unmanaged doctor; echo "exit=$?"; echo; echo '"'### refresh on the unmanaged dir (real endpoint configured)' && "'$PY tool/bootstrap.py --runtime-root unmanaged refresh; echo "exit=$?"; echo; echo '"'### unmanaged dir after refresh' && ls -a unmanaged && shasum -a 256 unmanaged/knowledge.db"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_RUNTIME_ROOT=$PWD/work/runtime-copy && $PY - <<'"'EOF'
import json, pathlib
p = pathlib.Path('work/runtime-copy/.oskm-runtime.json')
s = json.loads(p.read_text())
s['date'] = '20261115'; s['db']['date'] = '20261115'; s['sdk']['date'] = '20261115'
p.write_text(json.dumps(s, ensure_ascii=False, indent=2) + '\\n')
print('simulated stale state date ->', s['date'])
EOF
echo '### stale + DEAD endpoint: refresh must fail loudly and leave the old runtime usable' && OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:9/dead "'$PY tool/bootstrap.py --runtime-root work/runtime-copy refresh; echo "exit=$?"; echo '"'### old db still there and queryable' && shasum -a 256 work/runtime-copy/knowledge.db && "'$PY work/runtime-copy/oskm-cli.pyz --db work/runtime-copy/knowledge.db --format table arch overview 2>&1 | head -8; ls -a work/runtime-copy'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal OSKM_RUNTIME_ROOT=$PWD/work/unmanaged-copy && echo '"'### before' && ls -a work/unmanaged-copy && echo '### explicit install (takeover) on the unmanaged copy' && "'$PY tool/bootstrap.py --runtime-root work/unmanaged-copy install; echo "exit=$?"; echo '"'### after' && ls -a work/unmanaged-copy && cat work/unmanaged-copy/.oskm-runtime.json | head -12 && echo '### now refresh sees it as managed' && "'$PY tool/bootstrap.py --runtime-root work/unmanaged-copy refresh; echo "exit=$?"; echo '"'### real unmanaged fixture untouched?' && ls -a unmanaged && shasum -a 256 unmanaged/knowledge.db"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && sed -n '110,152p' tool/oskm_runtime/bootstrap.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY - <<'"'EOF'
import re, zipfile
z = zipfile.ZipFile('runtime/oskm-cli.pyz')
t = z.read('oskm_cli/cli.py').decode()
pat = re.compile(r'stale|过期|date|今天|today', re.I)
for i, line in enumerate(t.splitlines(), 1):
    if pat.search(line):
        print(f'{i}: {line.rstrip()[:150]}')
EOF"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && export PY=/opt/homebrew/opt/python@3.12/bin/python3.12 OSKM_RUNTIME_ROOT=$PWD/runtime && $PY - <<'"'EOF'
import sys
from pathlib import Path
sys.path.insert(0, 'tool')
from oskm_runtime import state
managed = Path('runtime/knowledge.db').resolve()
unmanaged = Path('unmanaged/knowledge.db').resolve()
print('today:', state.today())
print('managed needs_refresh (default today) :', state.needs_refresh(managed))
print('managed needs_refresh (--date 20261116):', state.needs_refresh(managed, current_date='20261116'))
print('managed needs_refresh (--date 20261117):', state.needs_refresh(managed, current_date='20261117'))
print('unmanaged needs_refresh (any date)    :', state.needs_refresh(unmanaged), state.needs_refresh(unmanaged, current_date='20261117'))
print('unmanaged state file exists           :', state.state_path(unmanaged).is_file())
EOF
echo '### final fixture integrity' && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json unmanaged/knowledge.db && ls -a runtime unmanaged && grep -n '\"date\"' runtime/.oskm-runtime.json"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && cat > answer.md <<'ANSWER_EOF'
# 过期托管运行时 + 直接查询：会不会下载？怎么更新？自管库怎么办？

实测日期 2026-11-17（"'`state.today()` 返回 `20261117`），夹具托管运行时状态文件里 `date=20261116`，即已过期一天。

## 结论速览

1. **直接跑 oskm-cli 查询不会触发任何下载。** CLI 是只读独立产物，`open_session()` 明确"不刷新、不联网、不跑 integrity_check"；`needs_refresh()` 的唯一调用方是 `bootstrap.py refresh`。过期数据只会被**原样查询**，不报警、不自动更新。
2. **正确的更新动作是显式跑 `bootstrap.py refresh`**（幂等，过期才下载），需要强制/指定日期时用 `install`。查询前不会有人替你做这件事。
3. **没有 `.oskm-runtime.json` 的自管库永远不会被 `refresh` 碰**：`load_state()` 返回 `None` → `needs_refresh()` 直接返回 `False` → 打印"已是最新"并退出 0，不下载、不覆盖、不创建状态文件。只有显式 `install --runtime-root <该目录>` 才会接管并覆盖它。

## 环境

```sh
cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit
export PY=/opt/homebrew/opt/python@3.12/bin/python3.12
export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
export OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal
# 让 .env 查找落在工作区内，避免碰 ~/.oskm
export OSKM_RUNTIME_ROOT=$PWD/runtime
```

## A. 工具自己怎么判定"过期"

```sh
$PY - <<'"'EOF'
import sys; from pathlib import Path; sys.path.insert(0, 'tool')
from oskm_runtime import state
managed, unmanaged = Path('runtime/knowledge.db').resolve(), Path('unmanaged/knowledge.db').resolve()
print('today:', state.today())
print('managed needs_refresh (default today)  :', state.needs_refresh(managed))
print('managed needs_refresh (--date 20261116):', state.needs_refresh(managed, current_date='20261116'))
print('unmanaged needs_refresh (any date)     :', state.needs_refresh(unmanaged), state.needs_refresh(unmanaged, current_date='20261117'))
print('unmanaged state file exists            :', state.state_path(unmanaged).is_file())
EOF
"'```

```
today: 20261117
managed needs_refresh (default today)  : True
managed needs_refresh (--date 20261116): False
unmanaged needs_refresh (any date)     : False False
unmanaged state file exists            : False
```

判定是**廉价检查**：状态结构 + `db.date`/`sdk.date` 是否等于当天 + 文件在不在 + SDK 目录非空 + SQLite 能只读打开且 `scans` 可读；不跑 `PRAGMA integrity_check`。`source == "local"` 的托管运行时跳过日期比较。

`doctor` 也照实报过期日期，但退出码仍是 0（过期不等于坏）：

```sh
$PY tool/bootstrap.py doctor
```

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: .../runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Runtime state: version 3, date 20261116, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
exit=0
```

## B. 直接查询（真端点已配置）：正常出结果，无下载

```sh
$PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
```

```
{ "product": "synthetic", "scan_id": 1, "subsystems": 2,
  "counts": { "repos": 1, "components": 2, "install_modules": 3, ... } }
exit=0
```

查询前后 `runtime/knowledge.db` 与 `runtime/.oskm-runtime.json` 的 sha256 完全一致，状态文件里仍是 `"date": "20261116"`：

```
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  runtime/knowledge.db
81e96054030951e863cf6777d1662d31208de3140b076b715451795f582aa432  runtime/.oskm-runtime.json
```

## C. 反证：把端点换成死端口，查询照样成功

```sh
export OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:9/dead   # 端口 9，无人监听
$PY runtime/oskm-cli.pyz --db runtime/knowledge.db ask --list          # exit=0
$PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table arch overview
$PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table sql --sql '"'select name from components order by name limit 5'
"'```

```
key       count
--------  -----
graphics  1
startup   1
name
----------
ace_engine
init
```

三类查询（`ask` / `arch` / `sql`）在端点不可达时全部 exit=0，输出无差异 → 查询路径根本没有网络代码。对 `oskm-cli.pyz` 45 个 `.py` 成员做全量 grep，也没有 `urlopen` / `urlretrieve` / `http.client` / `socket.` / `subprocess`；`oskm_cli/query/arkts/query.py` 里的 `urllib.parse.quote` 只用于拼展示用的远端链接，不发请求。

CLI 自己的 docstring 与错误文案也这么说：

- `oskm_cli/cli.py:9` —— "这是**独立产物**：不下载、不写盘、不认识 `~/.oskm`、不读 `.env`。"
- `oskm_cli/cli.py:87` —— "CLI **自己不下载数据**，所以文案一律指向 skill 的 `bootstrap.py`。"
- `oskm_cli/cli.py:113-116` —— `open_session()`："打开库。**不刷新、不联网、不跑 integrity_check。** … 自动刷新移到了 skill 的 bootstrap"
- 库缺失时报 `database not found: …。CLI 不会为任意缺失路径自动下载。`（退出码 3）

另外 `bootstrap.py` 不再透传查询命令：

```sh
$PY tool/bootstrap.py arch overview
```

```
错误: 未知命令 arch。bootstrap.py 只负责安装，查询请直接调 CLI：
  python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db <ask|arch|diff|sql> …
可用命令: doctor, install, refresh, update-cli, download-db, validate-db, cli-path
exit=2
```

## D. 正确的更新动作：显式 `refresh`（会下载）

为不动夹具，在**逐字节相同的副本**上演示（`cp -a runtime work/runtime-copy`）：

```sh
export OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal
$PY tool/bootstrap.py --runtime-root work/runtime-copy refresh
```

```
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: .../work/runtime-copy
exit=0        # 耗时 0.107s
```

刷新后状态文件 `date` / `db.date` / `sdk.date` 全部变成 `20261117`：

```
{ "version": 3, "source": "INTERNAL_CI", "date": "20261117",
  "updated_at": "2026-11-17T15:47:12+08:00",
  "db": { "date": "20261117", "path": "knowledge.db", "sha256": "f561e39f…" },
  "sdk": { "date": "20261117", "sdk-js": {...}, "sdk_c": {...} },
  "cli": { "path": "oskm-cli.pyz", "sha256": "ad760c16…" } }
```

紧接着再跑一次就是 no-op（幂等，不再产生请求）：

```sh
$PY tool/bootstrap.py --runtime-root work/runtime-copy refresh
```

```
==> 运行时已是最新，无需刷新: .../work/runtime-copy
exit=0
```

刷新失败时的行为也验证了（把副本状态改回 `20261115` 再用死端点）：

```
==> 下载 INTERNAL_CI 运行时: 20261117
错误: 下载失败（网络或代理不可用）: http://127.0.0.1:9/dead/20261117: <urlopen error [Errno 61] Connection refused>. …
exit=1
```

旧库原封不动且仍可查询（`knowledge.db` sha 不变，`arch overview` 正常返回）——安装是"临时目录里下好 + 校验 + 原子替换，失败逆序回滚"，所以过期数据在刷新失败时依然可用。

### 用户该敲的命令（把 `<root>` 换成实际运行时根目录）

```sh
# 1) 先看清楚状态与日期
python3 <skill>/bootstrap.py --runtime-root <root> doctor

# 2) 过期才更新（推荐，幂等）
python3 <skill>/bootstrap.py --runtime-root <root> refresh

# 变体：
#   refresh --date 20261117        按指定日期判定/安装
#   install                        无条件重装（DB + 两套 SDK + CLI）
#   install --skip-db / --skip-sdk 只补其中一部分
#   download-db --date D --output PATH   只取某一天的 knowledge.db
#   update-cli [--force]           只补齐/更换 CLI 产物（不下载 DB）
#   validate-db <root>/knowledge.db      完整 schema 契约校验

# 3) 更新完照常查询
python3 <root>/oskm-cli.pyz --db <root>/knowledge.db arch overview
```

下载配置从环境变量或 `.env` 读（顺序：真实环境变量 > `<runtime-root>/.env` > skill 的 `oskm_runtime/.env`），本次为 `OSKM_DOWNLOAD_SOURCE=INTERNAL_CI` + `OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal`；`INTERNAL_CI` 的取法是 `GET <endpoint>/<YYYYMMDD>`。端点没配时 `doctor` 会区分：运行时已完整 → `WARN`（查询可用，只是按日期刷新会失败）；什么都没装 → `FAIL`。

## E. 自管库（无 `.oskm-runtime.json`）：不会被刷新，也不会被覆盖

```sh
$PY tool/bootstrap.py --runtime-root unmanaged doctor      # 关注 Runtime state 那行
$PY tool/bootstrap.py --runtime-root unmanaged refresh
ls -a unmanaged && shasum -a 256 unmanaged/knowledge.db
```

```
Runtime state: 非托管（没有 .oskm-runtime.json），`bootstrap.py refresh` 不会碰它
==> 运行时已是最新，无需刷新: .../unmanaged
exit=0
.  ..  knowledge.db                                    # 没有多出 .oskm-runtime.json / oskm-cli.pyz / interface
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  unmanaged/knowledge.db
```

- `refresh` 对它是 **no-op**：`needs_refresh()` 见到 `load_state() is None` 立刻 `return False`（`state.py` 注释："A database without a state file is an unmanaged input and is left alone for backwards compatibility with hand-made `artifacts/*/knowledge.db` files."）。不下载、不覆盖、不写状态文件，退出码 0（提示文案是"已是最新"，实际含义是"非托管，不管"）。
- 自管库**照常可查**，只是没有任何日期新鲜度概念：

```sh
$PY runtime/oskm-cli.pyz --db unmanaged/knowledge.db --format table sql --sql '"'select name from components order by name limit 5'
# name / ace_engine / init      exit=0
"'```

- 想更新自管库只能自己动手：要么用 `download-db --date D --output <path>` 另存再替换，要么显式把它交给托管——`install` **会**接管并覆盖（在 `work/unmanaged-copy` 上验证）：

```sh
$PY tool/bootstrap.py --runtime-root work/unmanaged-copy install
```

```
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: .../work/unmanaged-copy
exit=0
# 目录里出现 .oskm-runtime.json / oskm-cli.pyz / interface/，此后 refresh 就认它是托管的了
```

顺带：对只放了 `knowledge.db` 的目录跑 `doctor`，会因为该目录旁边没有 `oskm-cli.pyz` 而报 `CLI: FAIL`（退出码 1）——这是"CLI 没装在这个根目录"，不是库坏了；查询时用别处的 CLI 加 `--db` 指过去即可（如上）。

## 本次对下载端点产生的请求

| 动作 | 端点 | 请求 |
| --- | --- | --- |
| `arch overview` / `ask --list` / `sql`（真端点） | `…:61481/internal` | 0 |
| 同样查询（死端点反证） | `…:9/dead` | 0（查询路径不联网） |
| `refresh`（副本，过期） | `…:61481/internal` | 1 × `GET /internal/20261117` |
| `refresh`（副本，已最新） | `…:61481/internal` | 0 |
| `refresh`（自管库） | `…:61481/internal` | 0 |
| `install`（自管库副本） | `…:61481/internal` | 1 × `GET /internal/20261117` |

即：**只有显式 `refresh`/`install` 会打到端点，查询一次都不会。**

## 夹具完整性（全程未修改 fixtures）

`runtime/` 与 `unmanaged/` 保持原状，所有会写盘的动作都在 `work/` 下的副本上做：

```
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  runtime/knowledge.db
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  runtime/oskm-cli.pyz
81e96054030951e863cf6777d1662d31208de3140b076b715451795f582aa432  runtime/.oskm-runtime.json   # date 仍为 20261116
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  unmanaged/knowledge.db      # 目录内仍只有 knowledge.db
```

未访问、未修改 `~/.oskm`（所有 bootstrap 调用都通过 `--runtime-root` / `OSKM_RUNTIME_ROOT` 指向工作区，`.env` 查找因此不会落到 `~/.oskm/.env`）。

## 一句话总结

过期只影响 `refresh` 的判定，不影响查询：**直接跑 oskm-cli 一定会用旧数据出结果且绝不下载**；要新数据就显式 `bootstrap.py --runtime-root <root> refresh`（或 `install`）；没有 `.oskm-runtime.json` 的自管库对 `refresh` 完全透明，永远不会被刷新或覆盖，除非你显式对它跑 `install`。
ANSWER_EOF
wc -l answer.md && head -12 answer.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && ls -a . work && echo '--- no leftover install temp dirs in fixtures ---' && find runtime unmanaged -maxdepth 1 -name '.oskm-runtime-*' -print | wc -l"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && rmdir work/pyz1 && ls work'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && find work/pyz1 | head'
```

### Agent 最终回答

```markdown
全部实测完成，结论已写入 `answer.md`。

**会不会下载**
- 直接跑查询**不会**下载。`python3 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview` 正常返回，`runtime/knowledge.db` 与 `runtime/.oskm-runtime.json` 的 sha256 前后一致，状态文件里仍是 `date=20261116`。
- 反证：把端点换成死端口 `http://127.0.0.1:9/dead` 后，`ask --list` / `arch overview` / `sql --sql …` 全部 exit=0、输出无差异；对 `oskm-cli.pyz` 内 45 个 `.py` 全量 grep 也没有 `urlopen`/`http.client`/`socket.`/`subprocess`。
- 工具同时确认库已过期：`needs_refresh(runtime/knowledge.db)` → `True`（今天 `20261117` vs 状态 `20261116`），但过期只影响 `refresh` 的判定，查询路径不看它。`bootstrap.py arch overview` 直接 exit=2 —— 它只装不查。

**正确的更新动作**
- `python3 tool/bootstrap.py --runtime-root <root> refresh`：在逐字节相同的副本上实测，输出 `==> 下载 INTERNAL_CI 运行时: 20261117` → `运行时安装完成`，状态文件三段日期全部变 `20261117`；再跑一次即 `运行时已是最新，无需刷新`（幂等，0 请求）。
- 变体：`install`（无条件重装）、`--date YYYYMMDD`、`--skip-db/--skip-sdk`、`download-db`、`update-cli`、`validate-db`。刷新失败时（死端点）报 `下载失败…Connection refused` exit=1，旧库原封不动仍可查询。

**自管库（无 `.oskm-runtime.json`）**
- `refresh --runtime-root unmanaged` 是 no-op：打印“已是最新”、exit=0，目录里仍只有 `knowledge.db`，sha 不变，不写状态文件；`doctor` 明确报 `非托管（没有 .oskm-runtime.json），bootstrap.py refresh 不会碰它`。它照常可查（`--db unmanaged/knowledge.db sql --sql …` 正常）。
- 只有显式 `install --runtime-root <该目录>` 才会接管覆盖 —— 在 `work/unmanaged-copy` 上验证：装出 `.oskm-runtime.json` / `oskm-cli.pyz` / `interface/`，此后 `refresh` 就认它是托管的。

**边界与产物**
- 夹具未被修改（`runtime/`、`unmanaged/` 哈希与文件清单原样，无残留 `.oskm-runtime-*` 临时目录），所有写盘动作都在 `work/` 副本上；未访问 `~/.oskm`（靠 `--runtime-root` / `OSKM_RUNTIME_ROOT` 让 `.env` 查找落在工作区）。
- 端点总共只被显式 `refresh`/`install` 打到 2 次，查询 0 次。
- 详见 `answer.md`（命令、输出片段、代码依据、请求计数表都在里面）。
```

### Agent 写入的 answer.md

```markdown
# 过期托管运行时 + 直接查询：会不会下载？怎么更新？自管库怎么办？

实测日期 2026-11-17（`state.today()` 返回 `20261117`），夹具托管运行时状态文件里 `date=20261116`，即已过期一天。

## 结论速览

1. **直接跑 oskm-cli 查询不会触发任何下载。** CLI 是只读独立产物，`open_session()` 明确"不刷新、不联网、不跑 integrity_check"；`needs_refresh()` 的唯一调用方是 `bootstrap.py refresh`。过期数据只会被**原样查询**，不报警、不自动更新。
2. **正确的更新动作是显式跑 `bootstrap.py refresh`**（幂等，过期才下载），需要强制/指定日期时用 `install`。查询前不会有人替你做这件事。
3. **没有 `.oskm-runtime.json` 的自管库永远不会被 `refresh` 碰**：`load_state()` 返回 `None` → `needs_refresh()` 直接返回 `False` → 打印"已是最新"并退出 0，不下载、不覆盖、不创建状态文件。只有显式 `install --runtime-root <该目录>` 才会接管并覆盖它。

## 环境

```sh
cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit
export PY=/opt/homebrew/opt/python@3.12/bin/python3.12
export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
export OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61481/internal
# 让 .env 查找落在工作区内，避免碰 ~/.oskm
export OSKM_RUNTIME_ROOT=$PWD/runtime
```

## A. 工具自己怎么判定"过期"

```sh
$PY - <<'EOF'
import sys; from pathlib import Path; sys.path.insert(0, 'tool')
from oskm_runtime import state
managed, unmanaged = Path('runtime/knowledge.db').resolve(), Path('unmanaged/knowledge.db').resolve()
print('today:', state.today())
print('managed needs_refresh (default today)  :', state.needs_refresh(managed))
print('managed needs_refresh (--date 20261116):', state.needs_refresh(managed, current_date='20261116'))
print('unmanaged needs_refresh (any date)     :', state.needs_refresh(unmanaged), state.needs_refresh(unmanaged, current_date='20261117'))
print('unmanaged state file exists            :', state.state_path(unmanaged).is_file())
EOF
```

```
today: 20261117
managed needs_refresh (default today)  : True
managed needs_refresh (--date 20261116): False
unmanaged needs_refresh (any date)     : False False
unmanaged state file exists            : False
```

判定是**廉价检查**：状态结构 + `db.date`/`sdk.date` 是否等于当天 + 文件在不在 + SDK 目录非空 + SQLite 能只读打开且 `scans` 可读；不跑 `PRAGMA integrity_check`。`source == "local"` 的托管运行时
… [输出截断，完整内容见工作区] …
al` | 0 |
| `refresh`（自管库） | `…:61481/internal` | 0 |
| `install`（自管库副本） | `…:61481/internal` | 1 × `GET /internal/20261117` |

即：**只有显式 `refresh`/`install` 会打到端点，查询一次都不会。**

## 夹具完整性（全程未修改 fixtures）

`runtime/` 与 `unmanaged/` 保持原状，所有会写盘的动作都在 `work/` 下的副本上做：

```
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  runtime/knowledge.db
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  runtime/oskm-cli.pyz
81e96054030951e863cf6777d1662d31208de3140b076b715451795f582aa432  runtime/.oskm-runtime.json   # date 仍为 20261116
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  unmanaged/knowledge.db      # 目录内仍只有 knowledge.db
```

未访问、未修改 `~/.oskm`（所有 bootstrap 调用都通过 `--runtime-root` / `OSKM_RUNTIME_ROOT` 指向工作区，`.env` 查找因此不会落到 `~/.oskm/.env`）。

## 一句话总结

过期只影响 `refresh` 的判定，不影响查询：**直接跑 oskm-cli 一定会用旧数据出结果且绝不下载**；要新数据就显式 `bootstrap.py --runtime-root <root> refresh`（或 `install`）；没有 `.oskm-runtime.json` 的自管库对 `refresh` 完全透明，永远不会被刷新或覆盖，除非你显式对它跑 `install`。
```

## 执行记录

### 1. [夹具准备] 装一个 date=20261116 的托管运行时（已过期）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit/runtime install --source INTERNAL_CI --date 20261116
stderr:
==> 下载 INTERNAL_CI 运行时: 20261116
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit` · exit=0 · 0.1s

### 2. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
全部实测完成，结论已写入 `answer.md`。

**会不会下载**
- 直接跑查询**不会**下载。`python3 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview` 正常返回，`runtime/knowledge.db` 与 `runtime/.oskm-runtime.json` 的 sha256 前后一致，状态文件里仍是 `date=20261116`。
- 反证：把端点换成死端口 `http://127.0.0.1:9/dead` 后，`ask --list` / `arch overview` / `sql --sql …` 全部 exit=0、输出无差异；对 `oskm-cli.pyz` 内 45 个 `.py` 全量 grep 也没有 `urlopen`/`http.client`/`socket.`/`subprocess`。
- 工具同时确认库已过期：`needs_refresh(runtime/knowledge.db)` → `True`（今天 `20261117` vs 状态 `20261116`），但过期只影响 `refresh` 的判定，查询路径不看它。`bootstrap.py arch overview` 直接 exit=2 —— 它只装不查。

**正确的更新动作**
- `python3 tool/bootstrap.py --runtime-root <root> refresh`：在逐字节相同的副本上实测，输出 `==> 下载 INTERNAL_CI 运行时: 20261117` → `运行时安装完成`，状态文件三段日期全部变 `20261117`；再跑一次即 `运行时已是最新，无需刷新`（幂等，0 请求）。
- 变体：`install`（无条件重装）、`--date YYYYMMDD`、`--skip-db/--skip-sdk`、`download-db`、`update-cli`、`validate-db`。刷新失败时（死端点）报 `下载失败…Connection refused` exit=1，旧库原封不动仍可查询。

**自管库（无 `.oskm-runtime.json`）**
- `refresh --runtime-root unmanaged` 是 no-op：打印“已是最新”、exit=0，目录里仍只有 `knowledge.db`，sha 不变，不写状态文件；`doctor` 明确报 `非托管（没有 .oskm-runtime.json），bootstrap.py refresh 不会碰它`。它照常可查（`--db unmanaged/knowledge.db sql --sql …` 正常）。
- 只有显式 `install --runtime-root <该目录>` 才会接管覆盖 —— 在 `work/unmanaged-copy` 上验证：装出 `.oskm-runtime.json` / `oskm-cli.pyz` / `interface/`，此后 `refresh` 就认它是托管的。

**边界与产物**
- 夹具未被修改（`runtime/`、`unmanaged/` 哈希与文件清单原样，无残留 `.oskm-runtime-*` 临时目录），所有写盘动作都在 `work/` 副本上；未访问 `~/.oskm`（靠 `--runtime-root` / `OSKM_RUNTIME_ROOT` 让 `.env` 查找落在工作区）。
- 端点总共只被显式 `refresh`/`install` 打到 2 次，查询 0 次。
- 详见 `answer.md`（命令、输出片段、代码依据、请求计数表都在里面）。stderr:
2026-11-17T07:44:57.642829Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc \\\"cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit && mkdir -p work && cd work && rm -rf pyz && mkdir pyz && cd pyz && unzip -q ../../runtime/oskm-cli.pyz && ls && echo '=== network / refresh references in CLI ===' && grep -rn \\\\\\\"urllib\\\\\\\\|requests\\\\\\\\|http://\\\\\\\\|https://\\\\\\\\|socket\\\\\\\\|needs_refresh\\\\\\\\|oskm_runtime\\\\\\\\|download\\\\\\\" --include='*.py' . | grep -v \\\\\\\"\\\"'^./_bootstrap\\\" | head -40'` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit` · exit=0 · 560.1s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（2 条）

```json
[
  {
    "seq": 2,
    "ts": "2026-11-17T15:47:12.466+08:00",
    "method": "GET",
    "path": "/internal/20261117",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 3,
    "ts": "2026-11-17T15:48:27.788+08:00",
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

## 被测前状态

- 托管运行时 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit/runtime`：`date=20261116`（今天 20261117，已过期）
- 自管库 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit/unmanaged/knowledge.db`：sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44
- 自管库没有 `.oskm-runtime.json`

## 断言结果

自动断言 6/6 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 工具的请求都是"按日期取归档"（没有凭空的 URL，也没有单独下 CLI） | auto | Pass | [{"method": "GET", "path": "/internal/20261117"}, {"method": "GET", "path": "/internal/20261117"}] |
| 2 | 自管库保持原样：没有状态文件、内容未被改写 | auto | Pass | 状态文件存在=False；sha 未变=True |
| 3 | 托管运行时仍然可用（没有被查询搞坏） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e07-refresh-is-explicit/runtime/knowledge.db |
| 4 | 回答说明直接查询不会触发下载 | auto | Pass | 相关表述见转录的 agent 最终回答 |
| 5 | 回答给出显式更新入口 refresh | auto | Pass | agent 回答中出现 refresh |
| 6 | 自管库（无状态文件）是否被正确说明为不刷新/不覆盖 | manual | 人工 | 全部实测完成，结论已写入 `answer.md`。  **会不会下载** - 直接跑查询**不会**下载。`python3 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview` 正常返回，`runtime/knowledge.db` 与 `runtime/.oskm-runtime.json` 的 sha256 前后一致，状态文
… [输出截断，完整内容见工作区] …
261116`），但过期只影响 `refresh` 的判定，查询路径不看它。`bootstrap.py arch overview` 直接 exit=2 —— 它只装不查。  **正确的更新动作**  |
| 7 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
