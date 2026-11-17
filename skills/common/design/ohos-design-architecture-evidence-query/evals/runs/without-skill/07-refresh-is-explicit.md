# E7 refresh-is-explicit（without-skill 臂）

- 开始时间：2026-11-17T16:28:17+08:00
- 结束时间：2026-11-17T16:37:29+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit`
- 夹具服务端：http://127.0.0.1:62160
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：523.7 s
- 事件计数：`{"thread.started": 1, "item.completed": 74, "item:error": 1, "turn.started": 1, "item:reasoning": 21, "item:agent_message": 20, "item.started": 32, "item:command_execution": 64, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：32
- token 用量：`{"input_tokens": 787287, "cached_input_tokens": 728448, "output_tokens": 18744, "reasoning_output_tokens": 7275}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && ls -la && echo \"--- tree ---\" && find . -maxdepth 3 -not -path '*/.git/*' | head -100"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && cat runtime/.oskm-runtime.json 2>/dev/null; echo "--- runtime dir ---"; ls -la runtime unmanaged tool 2>/dev/null'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool && cat bootstrap.py && echo "=== __main__.py ===" && cat oskm_runtime/__main__.py && echo "=== __init__.py ===" && cat oskm_runtime/__init__.py && echo "=== .env.example ===" && cat oskm_runtime/.env.example'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && wc -l *.py && echo "=== state.py ===" && cat state.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && cat bootstrap.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && cat environment.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && sed -n '125,200p' bootstrap.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && cat install.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && cat doctor.py && echo \"=== db_download.py (head) ===\" && sed -n '1,120p' db_download.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && cat PROMPT.md && echo "=== events ===" && cat codex-events.jsonl'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import zipfile
z=zipfile.ZipFile('runtime/oskm-cli.pyz')
names=z.namelist()
print('members:',len(names))
for n in names[:40]: print(' ',n)
import re
pat=re.compile(rb'urllib|http|socket|urlretrieve|urlopen|requests\\.|download|oskm_runtime|oskm-runtime\\.json|OSKM_DOWNLOAD|needs_refresh|refresh')
print('--- hits ---')
for n in names:
    if not n.endswith('.py'): continue
    data=z.read(n)
    for i,line in enumerate(data.splitlines(),1):
        if pat.search(line):
            print(f'{n}:{i}: {line.decode(errors=\\\"replace\\\")[:160]}')
\""
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && sed -n '120,300p' db_download.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import zipfile
z=zipfile.ZipFile('runtime/oskm-cli.pyz')
src=z.read('oskm_cli/cli.py').decode()
lines=src.splitlines()
for i in range(70,120):
    print(i+1, lines[i])
\" "
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && cat > /tmp/snap.sh <<'EOF'
#"'!/bin/zsh
cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit
echo "### snapshot $1"
find runtime unmanaged -type f | sort | while read -r f; do
  printf '"'%s  %s  %s\\n' \""'$(shasum -a 256 "$f" | cut -c1-16)" "$(stat -f '"'%Sm' -t '%H:%M:%S' \""'$f")" "$f"
done
echo "--- journal_mode ---"
/opt/homebrew/opt/python@3.12/bin/python3.12 - <<'"'PY'
import sqlite3
for p in ('runtime/knowledge.db','unmanaged/knowledge.db'):
    c=sqlite3.connect(f'file:{p}?mode=ro',uri=True)
    print(p, c.execute('PRAGMA journal_mode').fetchone()[0], c.execute(\"select count(*) from scans\").fetchone()[0])
    c.close()
PY
EOF
chmod +x /tmp/snap.sh && /tmp/snap.sh BEFORE"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "== --version ==" && $PY runtime/oskm-cli.pyz --version; echo "== --help ==" && $PY runtime/oskm-cli.pyz --help 2>&1 | head -40'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && grep -n \"def resolve_cli\\|def ensure_cli\\|allow_download\\|ARTIFACT_NAME =\\|def default_runtime_root\\|def installed_path\" cli_install.py | head -30"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "== arch overview on STALE managed runtime ==" && $PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview; echo "exit=$?"; echo; echo "== ask --list ==" && $PY runtime/oskm-cli.pyz --db runtime/knowledge.db ask --list 2>&1 | head -12; echo; echo "== same query on UNMANAGED db ==" && $PY runtime/oskm-cli.pyz --db unmanaged/knowledge.db arch overview; echo "exit=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && sed -n '185,275p' cli_install.py"
$ /bin/zsh -lc '/tmp/snap.sh AFTER-QUERIES'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import zipfile,re
z=zipfile.ZipFile('runtime/oskm-cli.pyz')
pat=re.compile(r'\\b(urllib\\.request|urlopen|urlretrieve|http\\.client|socket|subprocess|os\\.system|ftplib|smtplib)\\b')
hits=0
for n in z.namelist():
    if not n.endswith('.py'): continue
    for i,l in enumerate(z.read(n).decode(errors='replace').splitlines(),1):
        if pat.search(l):
            hits+=1; print(f'{n}:{i}: {l.strip()[:140]}')
print('total network/exec hits in oskm-cli.pyz:', hits)
print('imports of urllib.request:', any('urllib.request' in z.read(n).decode(errors='replace') for n in z.namelist() if n.endswith('.py')))
\""
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal && W=$PWD && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && export OSKM_RUNTIME_ROOT=$W/runtime && echo "########## doctor: managed (stale) ##########" && $PY tool/bootstrap.py --runtime-root "$W/runtime" doctor; echo "exit=$?"; echo; echo "########## doctor: unmanaged ##########" && OSKM_RUNTIME_ROOT=$W/unmanaged $PY tool/bootstrap.py --runtime-root "$W/unmanaged" doctor; echo "exit=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import sys; sys.path.insert(0,'.')
from oskm_runtime import state
W='/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit'
print('today() =', state.today())
for label,db in (('managed  ',W+'/runtime/knowledge.db'),('unmanaged',W+'/unmanaged/knowledge.db')):
    st=state.load_state(db)
    print(f'{label} state_path={state.state_path(db).name} load_state={\\\"None (无状态文件)\\\" if st is None else \\\"date=\\\"+str(st.get(\\\"date\\\"))} needs_refresh={state.needs_refresh(db)}')
\""
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal OSKM_RUNTIME_ROOT=$PWD/unmanaged && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "== refresh on UNMANAGED root ==" && $PY tool/bootstrap.py --runtime-root "$PWD/unmanaged" refresh; echo "exit=$?"; echo; echo "== files in unmanaged/ afterwards ==" && ls -la unmanaged && shasum -a 256 unmanaged/knowledge.db'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && mkdir -p scratch && cp -R runtime scratch/managed-copy && cp -R unmanaged scratch/unmanaged-copy && find scratch -type f | sort && echo \"--- copy state date ---\" && grep -m2 '\"date\"' scratch/managed-copy/.oskm-runtime.json"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal OSKM_RUNTIME_ROOT=$PWD/scratch/managed-copy && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "== refresh #1 on stale copy ==" && $PY tool/bootstrap.py --runtime-root "$PWD/scratch/managed-copy" refresh; echo "exit=$?"; echo; echo "== state after refresh ==" && cat scratch/managed-copy/.oskm-runtime.json'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "== refresh #2 (already fresh copy) ==" && OSKM_RUNTIME_ROOT=$PWD/scratch/managed-copy $PY tool/bootstrap.py --runtime-root "$PWD/scratch/managed-copy" refresh; echo "exit=$?"; echo; echo "== refresh on UNMANAGED copy ==" && shasum -a 256 scratch/unmanaged-copy/knowledge.db && OSKM_RUNTIME_ROOT=$PWD/scratch/unmanaged-copy $PY tool/bootstrap.py --runtime-root "$PWD/scratch/unmanaged-copy" refresh; echo "exit=$?"; echo "-- files after --"; ls -a scratch/unmanaged-copy; shasum -a 256 scratch/unmanaged-copy/knowledge.db'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "== explicit install --runtime-root scratch/unmanaged-copy ==" && OSKM_RUNTIME_ROOT=$PWD/scratch/unmanaged-copy $PY tool/bootstrap.py --runtime-root "$PWD/scratch/unmanaged-copy" install; echo "exit=$?"; echo; echo "-- files after --"; find scratch/unmanaged-copy -type f | sort; echo "-- state --"; cat scratch/unmanaged-copy/.oskm-runtime.json 2>/dev/null | head -12'
$ /bin/zsh -lc "/tmp/snap.sh FINAL && cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && echo \"== query on REFRESHED copy ==\" && /opt/homebrew/opt/python@3.12/bin/python3.12 scratch/managed-copy/oskm-cli.pyz --db scratch/managed-copy/knowledge.db arch overview | head -8; echo \"== fixture runtime state date (must still be 20261116) ==\"; grep -m1 '\"date\"' runtime/.oskm-runtime.json"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/tool/oskm_runtime && grep -n \"def needs_refresh\\|if state is None:\\|return False\\|db.get('date') "'!= current" state.py | head && echo "--- bootstrap ---" && grep -n "def cmd_refresh'"\\|needs_refresh\\|MANAGED = \\|未知命令\\|def cmd_install\\|def _do_install\\|install_runtime(\" bootstrap.py && echo \"--- doctor ---\" && grep -n \"非托管\\|Runtime state\" doctor.py && echo \"--- install.py ---\" && grep -n \"def install_runtime\\|def build_state\\|_install_artifacts(\" install.py | head"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal OSKM_RUNTIME_ROOT=$PWD/runtime && echo "== try a QUERY through bootstrap.py (stale runtime) ==" && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py --runtime-root "$PWD/runtime" arch overview; echo "exit=$?"; echo; echo "== fixture state date still =="; grep -m1 '"'\"date\"' runtime/.oskm-runtime.json"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && cat > answer.md <<'ANSWER_EOF'
# oskm 运行时：过期数据、显式 refresh 与自管库

结论先行（全部由实跑验证，见下方命令与输出）。

## 直接回答

**1. 用户只跑 "'`oskm-cli` 查询，会不会触发下载？——不会，一次都不会。**
`oskm-cli.pyz` 是纯只读查询产物，自身不带任何联网能力：对 pyz 内全部 `.py` 成员做
`urllib.request|urlopen|urlretrieve|http.client|socket|subprocess|os.system` 扫描，命中 **0** 处
（只有 `urllib.parse.quote` 和把远端 URL 拼成**字符串**用于展示）。它的 `--help` 第一行就写着
"OpenHarmony 产品事实库的只读查询（独立产物，不下载数据）"，`open_session()` 的注释也明确
"**不刷新、不联网、不跑 integrity_check**"。

实测：在已配置 `OSKM_DOWNLOAD_SOURCE=INTERNAL_CI` + `OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal`
的前提下，对**已过期**（`date=20261116`，今天 `20261117`）的托管运行时连跑 `arch overview` 与 `ask --list`，
查询正常返回（exit 0），而 `runtime/` 与 `unmanaged/` 下**每个文件的 sha256 与 mtime 前后完全一致**，
状态文件里 `date` 仍是 `20261116`。也就是说：**过期数据会被照常查询，静默返回旧结果，不会自动更新。**

`bootstrap.py` 也不存在"查询顺带刷新"的旁路：它只认
`doctor / install / refresh / update-cli / download-db / validate-db / cli-path` 七条命令，
把 `arch overview` 传给它直接报"未知命令"并 exit 2。`state.needs_refresh()` 在整个工具里
**只有一个调用方**——`cmd_refresh`（`tool/oskm_runtime/bootstrap.py:193`）。刷新因此是**用户显式要求**的动作。

**2. 数据过期时正确的更新动作是什么？——显式跑 `refresh`。**

```bash
export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
export OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal
python3 tool/bootstrap.py --runtime-root <runtime-root> refresh
```

它跑廉价检查（状态结构、日期、文件存在、SDK 目录非空、SQLite 可开且 `scans` 可读；**不跑**
`PRAGMA integrity_check`），**只有过期/不完整才下载**：拉当天日期的 `knowledge.tar.gz`，
用归档自带的 CLI 做 schema 校验，然后**原子替换** DB + 两套 SDK + `oskm-cli.pyz` 并写回状态文件；
失败则回滚，旧库原样保留可继续查询。相关命令选择：

- `refresh` —— 幂等，过期才下载（日常推荐）
- `install` —— 无条件重装同一天产物
- `refresh --date YYYYMMDD` / `install --date YYYYMMDD` —— 钉到指定日期
- `update-cli [--force]` —— 只补齐/更换 CLI 产物，不重下 DB/SDK
- `download-db --date D --output PATH` —— 只取某天 `knowledge.db` 到指定路径，不装 SDK、不碰运行时
- `doctor` —— 看当前装的是哪天、来源、db/sdk/cli 三段是否齐

刷新完成后照常直接调 CLI 查询：
`python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db arch overview`

**3. 没有 `.oskm-runtime.json` 的自管库会怎样？——不会被刷新，也不会被覆盖。**
`needs_refresh()` 在读不到状态文件时**立即返回 `False`**（`tool/oskm_runtime/state.py:151`），
把它当作"用户自己管的输入"原样放过。实测 `refresh --runtime-root unmanaged`：
打印"运行时已是最新，无需刷新"、exit 0、**不联网、不创建 `.oskm-runtime.json`、`knowledge.db` 的
sha256 与 mtime 一字未动**。`doctor` 对这种目录也直说："非托管（没有 `.oskm-runtime.json`），
`bootstrap.py refresh` 不会碰它"。

注意两点：
- 这条 no-op 的文案是"已是最新"，但真实原因是"非托管、根本不参与刷新判定"，不是"检查过且新鲜"。
- **唯一**会改动自管库的是用户显式执行 `install --runtime-root <该目录>`：实测它会把该目录**转成托管运行时**
  （下载当天归档、写入 `.oskm-runtime.json`、覆盖 `knowledge.db`、装上 `oskm-cli.pyz` 与两套 SDK）。
  所以别把 `--runtime-root` 指向想保留的自管库目录；查自管库只需 `--db` 指向它，CLI 用别处装好的那个即可。

---

## 执行过的关键命令与输出

解释器 `/opt/homebrew/opt/python@3.12/bin/python3.12`（3.12.16），cwd 为任务给定的工作区。
**夹具目录未被修改**：涉及"会写盘"的 `refresh` / `install` 都在 `scratch/` 下的副本上做，
`runtime/` 与 `unmanaged/` 的前后快照逐字节相同（见最后一节）。

### 0) 基线快照（跑查询之前）

```
$ /tmp/snap.sh BEFORE        # find runtime unmanaged -type f | shasum -a 256 | stat mtime
c472e9d0852578fa  16:28:17  runtime/.oskm-runtime.json
8c8c597c1d563cfb  16:28:17  runtime/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
49673a32794f18d5  16:28:17  runtime/interface/sdk_c/evalmarker.h
f561e39f648cfd6b  16:28:17  runtime/knowledge.db
3e78cf73a94bcf9d  16:28:17  runtime/oskm-cli.pyz
f561e39f648cfd6b  16:18:33  unmanaged/knowledge.db
--- journal_mode ---
runtime/knowledge.db delete 1
unmanaged/knowledge.db delete 1
```

（`journal_mode=delete`，说明只读 SELECT 不会在库旁边留下 `-wal` / `-shm`，快照对比才干净。）

### 1) CLI 自身无联网能力

```
$ python3.12 -c "...zipfile 扫描 runtime/oskm-cli.pyz 全部 .py 成员..."
total network/exec hits in oskm-cli.pyz: 0
imports of urllib.request: False
```

`--help` 摘要：

```
$ python3.12 runtime/oskm-cli.pyz --help
usage: oskm-cli [-h] [--version] [--db DB] [--product PRODUCT]
                [--scan-id SCAN_ID] [--format {json,table}]
                {ask,arch,diff,sql,validate-db} ...

OpenHarmony 产品事实库的只读查询（独立产物，不下载数据）。
```

### 2) 直接查询过期运行时（下载端点已配置且可用）

```
$ export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal
$ python3.12 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
{
  "product": "synthetic",
  "scan_id": 1,
  "subsystems": 2,
  "counts": { "repos": 1, "components": 2, "install_modules": 3, "install_targets": 3, ... },
  "top_subsystems": [ { "key": "graphics", "count": 1 }, { "key": "startup", "count": 1 } ]
}
exit=0

$ python3.12 runtime/oskm-cli.pyz --db runtime/knowledge.db ask --list | head -12
arkts
    arkts_kit_modules          Kit 的去重成员模块，或未解析的引用。...
    ...
component
    component_attached         部件关联的各域记录
```

查询之后立刻复查快照 —— **与 BEFORE 完全一致**：

```
$ /tmp/snap.sh AFTER-QUERIES
c472e9d0852578fa  16:28:17  runtime/.oskm-runtime.json
f561e39f648cfd6b  16:28:17  runtime/knowledge.db
3e78cf73a94bcf9d  16:28:17  runtime/oskm-cli.pyz
f561e39f648cfd6b  16:18:33  unmanaged/knowledge.db
...（六个文件 sha256 + mtime 全部未变）
```

同一个 CLI 也能直接查自管库（同样不下载、不写盘）：

```
$ python3.12 runtime/oskm-cli.pyz --db unmanaged/knowledge.db arch overview
{ "product": "synthetic", "scan_id": 1, "subsystems": 2, ... }
exit=0
```

### 3) bootstrap 不接受查询命令（没有隐式刷新旁路）

```
$ python3.12 tool/bootstrap.py --runtime-root "$PWD/runtime" arch overview
错误: 未知命令 arch。bootstrap.py 只负责安装，查询请直接调 CLI：
  python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db <ask|arch|diff|sql> …
可用命令: doctor, install, refresh, update-cli, download-db, validate-db, cli-path
exit=2

$ grep -m1 '"'\"date\"' runtime/.oskm-runtime.json
  \"date\": \"20261116\"
"'```

### 4) doctor：过期状态与非托管状态各自怎么说

```
$ python3.12 tool/bootstrap.py --runtime-root "$PWD/runtime" doctor
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: .../runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: .../runtime
Runtime state: version 3, date 20261116, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
exit=0
```

（doctor 只**报告** `date 20261116`，自己不判定过期、也不下载；`resolve_cli(..., allow_download=False)`。）

```
$ python3.12 tool/bootstrap.py --runtime-root "$PWD/unmanaged" doctor
CLI: FAIL: 找不到可用的 oskm-cli 产物。...
  3. .../unmanaged/oskm-cli.pyz —— 不存在
Runtime state: 非托管（没有 .oskm-runtime.json），`bootstrap.py refresh` 不会碰它
错误: 运行时依赖检查未通过。
exit=1
```

（这里的 FAIL 只是"该目录没有 CLI 产物"，不是库坏了：自管库本来就用别处的 CLI 加 `--db` 查。）

### 5) 刷新判定本身

```
$ python3.12 -c "from oskm_runtime import state; ..."
today() = 20261117
managed   state_path=.oskm-runtime.json load_state=date=20261116 needs_refresh=True
unmanaged state_path=.oskm-runtime.json load_state=None (无状态文件) needs_refresh=False
```

### 6) 显式 refresh = 真正的下载 + 原子更新（在副本上跑）

```
$ mkdir -p scratch && cp -R runtime scratch/managed-copy && cp -R unmanaged scratch/unmanaged-copy
$ python3.12 tool/bootstrap.py --runtime-root "$PWD/scratch/managed-copy" refresh
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: .../scratch/managed-copy
exit=0

$ cat scratch/managed-copy/.oskm-runtime.json
{
  "version": 3,
  "source": "INTERNAL_CI",
  "date": "20261117",
  "updated_at": "2026-11-17T16:34:06+08:00",
  "db":  { "date": "20261117", "path": "knowledge.db", "sha256": "f561e39f..." },
  "sdk": { "date": "20261117", "sdk-js": {...}, "sdk_c": {...} },
  "cli": { "path": "oskm-cli.pyz", "sha256": "3e78cf73..." }
}
```

紧接着第二次 refresh —— **幂等，不再下载**：

```
$ python3.12 tool/bootstrap.py --runtime-root "$PWD/scratch/managed-copy" refresh
==> 运行时已是最新，无需刷新: .../scratch/managed-copy
exit=0
```

刷新后的副本查询正常：

```
$ python3.12 scratch/managed-copy/oskm-cli.pyz --db scratch/managed-copy/knowledge.db arch overview | head -8
{
  "product": "synthetic",
  "scan_id": 1,
  "subsystems": 2,
  ...
```

### 7) 自管库：refresh 是 no-op，只有显式 install 才会改它

```
$ python3.12 tool/bootstrap.py --runtime-root "$PWD/unmanaged" refresh
==> 运行时已是最新，无需刷新: .../unmanaged
exit=0

$ ls -la unmanaged && shasum -a 256 unmanaged/knowledge.db
-rw-r--r--  1 song  staff  434176 Nov 17 16:18 knowledge.db        # 没有 .oskm-runtime.json
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  unmanaged/knowledge.db
```

副本上同样验证（refresh 前后 sha 一致、目录里仍只有 `knowledge.db`）：

```
$ shasum -a 256 scratch/unmanaged-copy/knowledge.db
f561e39f648cfd6b...   # before
$ python3.12 tool/bootstrap.py --runtime-root "$PWD/scratch/unmanaged-copy" refresh
==> 运行时已是最新，无需刷新: .../scratch/unmanaged-copy
exit=0
$ ls -a scratch/unmanaged-copy ; shasum -a 256 scratch/unmanaged-copy/knowledge.db
.  ..  knowledge.db
f561e39f648cfd6b...   # after —— 未变，且没有生成状态文件
```

对照：**显式** `install` 指向同一目录就会把它变成托管运行时（这就是唯一会覆盖自管库的路径）：

```
$ python3.12 tool/bootstrap.py --runtime-root "$PWD/scratch/unmanaged-copy" install
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: .../scratch/unmanaged-copy
exit=0

$ find scratch/unmanaged-copy -type f | sort
scratch/unmanaged-copy/.oskm-runtime.json          <- 新建，自管变托管
scratch/unmanaged-copy/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
scratch/unmanaged-copy/interface/sdk_c/evalmarker.h
scratch/unmanaged-copy/knowledge.db                <- 被归档里的库覆盖
scratch/unmanaged-copy/oskm-cli.pyz

$ head -12 scratch/unmanaged-copy/.oskm-runtime.json
{
  "version": 3,
  "source": "INTERNAL_CI",
  "date": "20261117",
  ...
```

### 8) 收尾快照：夹具一字未动

```
$ /tmp/snap.sh FINAL
c472e9d0852578fa  16:28:17  runtime/.oskm-runtime.json
8c8c597c1d563cfb  16:28:17  runtime/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
49673a32794f18d5  16:28:17  runtime/interface/sdk_c/evalmarker.h
f561e39f648cfd6b  16:28:17  runtime/knowledge.db
3e78cf73a94bcf9d  16:28:17  runtime/oskm-cli.pyz
f561e39f648cfd6b  16:18:33  unmanaged/knowledge.db

$ grep -m1 '"'\"date\"' runtime/.oskm-runtime.json
  \"date\": \"20261116\"          # 仍是夹具原始的过期日期
"'```

全程未读写 `~/.oskm`：每次调 `bootstrap.py` 都把 `OSKM_RUNTIME_ROOT` 指向工作区内的路径，
并用 `--runtime-root` 显式覆盖，`.env` 查找因此不会落到 `~/.oskm/.env`。

---

## 代码依据（与实跑一致）

- `tool/oskm_runtime/state.py:137` `needs_refresh()` —— 刷新判定的唯一实现，**只做廉价检查**；
  `tool/oskm_runtime/state.py:151` 状态文件不存在时 `return False`（自管库放过）；
  `tool/oskm_runtime/state.py:160` `db.date`/`sdk.date` 与今天不同即判过期；
  `source == '"'local'"'` 的运行时跳过日期比较（源码树本地构建不按天过期）。
- `tool/oskm_runtime/bootstrap.py:181` `cmd_refresh()` —— `needs_refresh()` 为假就打印
  "运行时已是最新，无需刷新"并 exit 0；为真才走 `_do_install()` → `install.install_runtime()`。
- `tool/oskm_runtime/bootstrap.py:50` `MANAGED` 七条命令 + `tool/oskm_runtime/bootstrap.py:290`
  "未知命令"分支 —— 查询不在 bootstrap 里，所以没有"查询前顺手刷新"的触发点。
- `tool/oskm_runtime/install.py:406` `install_runtime()` —— 临时目录里下载/校验，再
  `_install_artifacts()`（`tool/oskm_runtime/install.py:252`）原子替换 + 失败逆序回滚，
  最后由 `build_state()`（`tool/oskm_runtime/install.py:312`）写 `.oskm-runtime.json`。
- `tool/oskm_runtime/db_download.py` —— `INTERNAL_CI` 取 `<endpoint>/<YYYYMMDD>` 的
  `knowledge.tar.gz`，解包 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`，
  防御式解压（越界路径/软链直接中止）。CLI 随归档一起发布，**没有单独的 CLI 下载端点**。
- `tool/oskm_runtime/doctor.py:104` —— 非托管目录的原文提示
  "非托管（没有 .oskm-runtime.json），`bootstrap.py refresh` 不会碰它"。
- `runtime/oskm-cli.pyz` 内 `oskm_cli/cli.py:110` `open_session()` ——
  "打开库。**不刷新、不联网、不跑 integrity_check。**"；`oskm_cli/cli.py:84`
  `_database_not_found_message()` —— 库缺失时也只提示去跑 skill 的 `bootstrap.py install`，
  明写"CLI 本身不下载数据 / CLI 不会为任意缺失路径自动下载"。
ANSWER_EOF
wc -l answer.md && head -20 answer.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && ls -la && echo \"--- fixture integrity (must match BEFORE) ---\" && shasum -a 256 runtime/.oskm-runtime.json runtime/knowledge.db runtime/oskm-cli.pyz unmanaged/knowledge.db && grep -m1 '\"date\"' runtime/.oskm-runtime.json"
```

### Agent 最终回答

```markdown
**结论**
- 直接跑 `oskm-cli` 查询**不会下载**。`runtime/oskm-cli.pyz` 内 45 个模块对 `urllib.request|urlopen|socket|subprocess` 的扫描命中 0 处；实跑 `arch overview` / `ask --list` 后 `runtime/` 与 `unmanaged/` 全部文件的 sha256 与 mtime 一字未变，状态文件仍是 `date=20261116`——过期数据被照常查询、静默返回旧结果。
- `bootstrap.py` 也没有隐式刷新旁路：查询命令被拒（`arch` → “未知命令”，exit 2），`needs_refresh()` 的唯一调用方是 `tool/oskm_runtime/bootstrap.py:193`。
- 正确更新动作是**显式** `python3 tool/bootstrap.py --runtime-root <root> refresh`（需 `OSKM_DOWNLOAD_SOURCE`/`OSKM_DOWNLOAD_ENDPOINT` 或 `.env`）。实测输出 `==> 下载 INTERNAL_CI 运行时: 20261117`，原子替换 DB+SDK+CLI 并写回状态；再跑一次即 `==> 运行时已是最新，无需刷新`，不再下载。要钉日期用 `--date`，只补 CLI 用 `update-cli`，只取某天库用 `download-db`。
- 自管库（无 `.oskm-runtime.json`）**不会被刷新也不会被覆盖**：`tool/oskm_runtime/state.py:151` 在无状态文件时直接 `return False`，`refresh --runtime-root unmanaged` 是 no-op（不联网、不建状态文件、`knowledge.db` sha 与 mtime 不变），`doctor` 也明说“非托管…`bootstrap.py refresh` 不会碰它”。唯一会改它的是用户显式 `install --runtime-root <该目录>`——实测会下载并把它转成托管运行时、覆盖原库，所以别把 `--runtime-root` 指向想保留的自管目录；查自管库只需 `--db` 指向它。

**产物**
- 完整命令、关键输出片段与代码依据已写入 `answer.md`。
- 会写盘的 `refresh`/`install` 演示都在 `scratch/` 的副本上做，夹具 `runtime/`、`unmanaged/`、`tool/` 保持原始状态（收尾快照逐字节一致），全程未触碰 `~/.oskm`。
- 一个小提醒：非托管目录上 `refresh` 打印的是“运行时已是最新”，真实原因其实是“不参与刷新判定”，文案容易让人误以为检查过日期。

需要我把 `scratch/` 清掉，只留 `answer.md` 吗？
```

### Agent 写入的 answer.md

```markdown
# oskm 运行时：过期数据、显式 refresh 与自管库

结论先行（全部由实跑验证，见下方命令与输出）。

## 直接回答

**1. 用户只跑 `oskm-cli` 查询，会不会触发下载？——不会，一次都不会。**
`oskm-cli.pyz` 是纯只读查询产物，自身不带任何联网能力：对 pyz 内全部 `.py` 成员做
`urllib.request|urlopen|urlretrieve|http.client|socket|subprocess|os.system` 扫描，命中 **0** 处
（只有 `urllib.parse.quote` 和把远端 URL 拼成**字符串**用于展示）。它的 `--help` 第一行就写着
"OpenHarmony 产品事实库的只读查询（独立产物，不下载数据）"，`open_session()` 的注释也明确
"**不刷新、不联网、不跑 integrity_check**"。

实测：在已配置 `OSKM_DOWNLOAD_SOURCE=INTERNAL_CI` + `OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal`
的前提下，对**已过期**（`date=20261116`，今天 `20261117`）的托管运行时连跑 `arch overview` 与 `ask --list`，
查询正常返回（exit 0），而 `runtime/` 与 `unmanaged/` 下**每个文件的 sha256 与 mtime 前后完全一致**，
状态文件里 `date` 仍是 `20261116`。也就是说：**过期数据会被照常查询，静默返回旧结果，不会自动更新。**

`bootstrap.py` 也不存在"查询顺带刷新"的旁路：它只认
`doctor / install / refresh / update-cli / download-db / validate-db / cli-path` 七条命令，
把 `arch overview` 传给它直接报"未知命令"并 exit 2。`state.needs_refresh()` 在整个工具里
**只有一个调用方**——`cmd_refresh`（`tool/oskm_runtime/bootstrap.py:193`）。刷新因此是**用户显式要求**的动作。

**2. 数据过期时正确的更新动作是什么？——显式跑 `refresh`。**

```bash
export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
export OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62160/internal
python3 tool/bootstrap.py --runtime-root <runtime-root> refresh
```

它跑廉价检查（状态结构、日期、文件存在、SDK 目录非空、SQLite 可开且 `scans` 可读；**不跑**
`PRAGMA integrity_check`），**只有过期/不完整才下载**：拉当天日期的 `knowledge.tar.gz`，
用归档自带的 CLI 做 schema 校验，然后**原子替换** DB + 两套 SDK + `oskm-cli.pyz` 并写回状态文件；
失败则回滚，旧库原样保留可继续查询。相关命令选择：

- `refresh` —— 幂等，过期才下载（日常推荐）
- `install` —— 无条件重装同一天产物
- `refresh --date YYYYMMDD` / `install --date YYYYMMDD` —— 钉到指定日期
- `update-cli [--force]` —— 只补齐/更换 CLI 产物，不重下 DB/SDK
- `download-db --date D --output PATH` —— 只取某天 `knowledge.db` 到指定路径，不装 SDK、不碰运行时
- `doctor` —— 看当前装的是哪天、来源、db/sdk/cli 三段是否齐

刷新完成后照常直接调 CLI 查询：
`python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db arch overview`

**3. 没有 `.oskm-runtime.json` 的自管库会怎样？——不会被刷新，也不会被覆盖。**
`needs_refresh()` 在读不到状态文件时**立即返回 `False`**（`tool/oskm_runtime/st
… [输出截断，完整内容见工作区] …
ll()` → `install.install_runtime()`。
- `tool/oskm_runtime/bootstrap.py:50` `MANAGED` 七条命令 + `tool/oskm_runtime/bootstrap.py:290`
  "未知命令"分支 —— 查询不在 bootstrap 里，所以没有"查询前顺手刷新"的触发点。
- `tool/oskm_runtime/install.py:406` `install_runtime()` —— 临时目录里下载/校验，再
  `_install_artifacts()`（`tool/oskm_runtime/install.py:252`）原子替换 + 失败逆序回滚，
  最后由 `build_state()`（`tool/oskm_runtime/install.py:312`）写 `.oskm-runtime.json`。
- `tool/oskm_runtime/db_download.py` —— `INTERNAL_CI` 取 `<endpoint>/<YYYYMMDD>` 的
  `knowledge.tar.gz`，解包 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`，
  防御式解压（越界路径/软链直接中止）。CLI 随归档一起发布，**没有单独的 CLI 下载端点**。
- `tool/oskm_runtime/doctor.py:104` —— 非托管目录的原文提示
  "非托管（没有 .oskm-runtime.json），`bootstrap.py refresh` 不会碰它"。
- `runtime/oskm-cli.pyz` 内 `oskm_cli/cli.py:110` `open_session()` ——
  "打开库。**不刷新、不联网、不跑 integrity_check。**"；`oskm_cli/cli.py:84`
  `_database_not_found_message()` —— 库缺失时也只提示去跑 skill 的 `bootstrap.py install`，
  明写"CLI 本身不下载数据 / CLI 不会为任意缺失路径自动下载"。
```

## 执行记录

### 1. [夹具准备] 装一个 date=20261116 的托管运行时（已过期）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/runtime install --source INTERNAL_CI --date 20261116
stderr:
==> 下载 INTERNAL_CI 运行时: 20261116
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit` · exit=0 · 0.13s

### 2. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结论**
- 直接跑 `oskm-cli` 查询**不会下载**。`runtime/oskm-cli.pyz` 内 45 个模块对 `urllib.request|urlopen|socket|subprocess` 的扫描命中 0 处；实跑 `arch overview` / `ask --list` 后 `runtime/` 与 `unmanaged/` 全部文件的 sha256 与 mtime 一字未变，状态文件仍是 `date=20261116`——过期数据被照常查询、静默返回旧结果。
- `bootstrap.py` 也没有隐式刷新旁路：查询命令被拒（`arch` → “未知命令”，exit 2），`needs_refresh()` 的唯一调用方是 `tool/oskm_runtime/bootstrap.py:193`。
- 正确更新动作是**显式** `python3 tool/bootstrap.py --runtime-root <root> refresh`（需 `OSKM_DOWNLOAD_SOURCE`/`OSKM_DOWNLOAD_ENDPOINT` 或 `.env`）。实测输出 `==> 下载 INTERNAL_CI 运行时: 20261117`，原子替换 DB+SDK+CLI 并写回状态；再跑一次即 `==> 运行时已是最新，无需刷新`，不再下载。要钉日期用 `--date`，只补 CLI 用 `update-cli`，只取某天库用 `download-db`。
- 自管库（无 `.oskm-runtime.json`）**不会被刷新也不会被覆盖**：`tool/oskm_runtime/state.py:151` 在无状态文件时直接 `return False`，`refresh --runtime-root unmanaged` 是 no-op（不联网、不建状态文件、`knowledge.db` sha 与 mtime 不变），`doctor` 也明说“非托管…`bootstrap.py refresh` 不会碰它”。唯一会改它的是用户显式 `install --runtime-root <该目录>`——实测会下载并把它转成托管运行时、覆盖原库，所以别把 `--runtime-root` 指向想保留的自管目录；查自管库只需 `--db` 指向它。

**产物**
- 完整命令、关键输出片段与代码依据已写入 `answer.md`。
- 会写盘的 `refresh`/`install` 演示都在 `scratch/` 的副本上做，夹具 `runtime/`、`unmanaged/`、`tool/` 保持原始状态（收尾快照逐字节一致），全程未触碰 `~/.oskm`。
- 一个小提醒：非托管目录上 `refresh` 打印的是“运行时已是最新”，真实原因其实是“不参与刷新判定”，文案容易让人误以为检查过日期。

需要我把 `scratch/` 清掉，只留 `answer.md` 吗？stderr:
2026-11-17T08:33:49.956451Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc \\\"cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit && rm -rf scratch && mkdir -p scratch && cp -R runtime scratch/managed-copy && cp -R unmanaged scratch/unmanaged-copy && ls -la scratch/managed-copy && echo \\\\\\\"--- copy state date ---\\\\\\\" && grep '\\\\\\\"date\\\\\\\"' scratch/managed-copy/.oskm-runtime.json | head -3\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit` · exit=0 · 523.7s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（2 条）

```json
[
  {
    "seq": 2,
    "ts": "2026-11-17T16:34:06.788+08:00",
    "method": "GET",
    "path": "/internal/20261117",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 3,
    "ts": "2026-11-17T16:34:38.990+08:00",
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

- 托管运行时 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/runtime`：`date=20261116`（今天 20261117，已过期）
- 自管库 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/unmanaged/knowledge.db`：sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44
- 自管库没有 `.oskm-runtime.json`

## 断言结果

自动断言 6/6 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 工具的请求都是"按日期取归档"（没有凭空的 URL，也没有单独下 CLI） | auto | Pass | [{"method": "GET", "path": "/internal/20261117"}, {"method": "GET", "path": "/internal/20261117"}] |
| 2 | 自管库保持原样：没有状态文件、内容未被改写 | auto | Pass | 状态文件存在=False；sha 未变=True |
| 3 | 托管运行时仍然可用（没有被查询搞坏） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e07-refresh-is-explicit/runtime/knowledge.db |
| 4 | 回答说明直接查询不会触发下载 | auto | Pass | 相关表述见转录的 agent 最终回答 |
| 5 | 回答给出显式更新入口 refresh | auto | Pass | agent 回答中出现 refresh |
| 6 | 自管库（无状态文件）是否被正确说明为不刷新/不覆盖 | manual | 人工 | **结论** - 直接跑 `oskm-cli` 查询**不会下载**。`runtime/oskm-cli.pyz` 内 45 个模块对 `urllib.request\|urlopen\|socket\|subprocess` 的扫描命中 0 处；实跑 `arch overview` / `ask --list` 后 `runtime/` 与 `unmanaged/` 全部文件的 sha256 与
… [输出截断，完整内容见工作区] …
`.env`）。实测输出 `==> 下载 INTERNAL_CI 运行时: 20261117`，原子替换 DB+SDK+CLI 并写回状态；再跑一次即 `==> 运行时已是最新，无需刷新`，不再下载。 |
| 7 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
