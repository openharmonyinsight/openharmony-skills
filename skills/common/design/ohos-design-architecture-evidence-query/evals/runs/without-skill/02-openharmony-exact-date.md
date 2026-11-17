# E2 openharmony-exact-date（without-skill 臂）

- 开始时间：2026-11-17T15:33:43+08:00
- 结束时间：2026-11-17T15:41:25+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date`
- 夹具服务端：http://127.0.0.1:61141
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

使用 OPENHARMONY_CI 安装 date=20261102，OSKM_DOWNLOAD_ENDPOINT 已配置为测试服务。请执行安装并说明实际请求语义。

## 期望结果（来自 evals.json）

向端点 POST，component 固定为 dayu600_7885_ai，开始和结束时间都来自同一个显式日期；下载物是 knowledge.tar.gz，不要求用户传 --component，也不使用 latest。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| OPENHARMONY_CI | `contains` |
| component: dayu600_7885_ai | `contains` |
| knowledge.tar.gz | `contains` |
| 一次请求同时表示开始和结束日期，不要求用户单独传两个日期 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：462.1 s
- 事件计数：`{"thread.started": 1, "item.completed": 56, "item:error": 1, "turn.started": 1, "item:reasoning": 21, "item:agent_message": 7, "item.started": 27, "item:command_execution": 54, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：27
- token 用量：`{"input_tokens": 685835, "cached_input_tokens": 633344, "output_tokens": 15413, "reasoning_output_tokens": 6896}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && ls -la && echo \"--- tree ---\" && find . -maxdepth 3 -not -path './.git/*' | head -100"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && env | grep -i oskm'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && cat PROMPT.md && echo "=== bootstrap.py ===" && cat tool/bootstrap.py && echo "=== .env.example ===" && cat tool/oskm_runtime/.env.example'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date/tool/oskm_runtime && wc -l *.py && echo "=== __main__.py ===" && cat __main__.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date/tool/oskm_runtime && cat __init__.py && echo "=== environment.py ===" && cat environment.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date/tool/oskm_runtime && cat bootstrap.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date/tool/oskm_runtime && cat db_download.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date/tool/oskm_runtime && sed -n '135,300p' db_download.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date/tool/oskm_runtime && sed -n '1,200p' install.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date/tool/oskm_runtime && sed -n '200,451p' install.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date/tool/oskm_runtime && sed -n '130,215p' bootstrap.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date/tool/oskm_runtime && sed -n '1,90p' state.py && echo \"=== doctor head ===\" && sed -n '1,60p' doctor.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py install --date 20261102; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && find runtime -maxdepth 3 | sort | head -40 && echo "=== state ===" && cat runtime/.oskm-runtime.json && echo "=== sizes ===" && du -sh runtime/* 2>/dev/null'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor; echo "EXIT=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && mkdir -p scratch && /opt/homebrew/opt/python@3.12/bin/python3.12 - <<'PY'
import io, json, sys
from pathlib import Path

HERE = Path.cwd()
sys.path.insert(0, str(HERE / 'tool'))

from oskm_runtime import db_download as dd

real_open = dd._open
log = []

class FakeResp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): self.close(); return False

def spy_open(request, *, timeout, attempts, retry_delay):
    body = request.data
    entry = {
        'method': request.get_method(),
        'url': request.full_url,
        'headers': dict(request.header_items()),
        'body': body.decode('utf-8') if body else None,
    }
    resp = real_open(request, timeout=timeout, attempts=attempts, retry_delay=retry_delay)
    raw = resp.read()
    entry['status'] = getattr(resp, 'status', None) or resp.getcode()
    entry['resp_len'] = len(raw)
    entry['resp_preview'] = raw[:1200].decode('utf-8', 'replace')
    log.append(entry)
    return FakeResp(raw)

dd._open = spy_open

out = HERE / 'scratch' / 'knowledge.db'
dd.download_database(source='OPENHARMONY_CI', date='20261102', output=out)

print(f'--- captured {len(log)} HTTP request(s) ---')
for i, e in enumerate(log, 1):
    print(f'\\n[{i}] {e[\"method\"]} {e[\"url\"]}  -> HTTP {e[\"status\"]}, {e[\"resp_len\"]} bytes')
    print('    headers:', json.dumps(e['headers'], ensure_ascii=False))
    if e['body']:
        print('    body:')
        print(json.dumps(json.loads(e['body']), ensure_ascii=False, indent=6))
    print('    response preview:', e['resp_preview'][:600].replace('\\n', ' '))
print('\\nlanded db:', out, out.stat().st_size, 'bytes')
PY
echo \"EXIT="'$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && P=/opt/homebrew/opt/python@3.12/bin/python3.12
echo "### A) download-db 20261101 (neighbouring day)"; $P tool/bootstrap.py download-db --date 20261101 --output scratch/db-20261101.db; echo "EXIT=$?"
echo; echo "### B) download-db 20261302 (invalid calendar date)"; $P tool/bootstrap.py download-db --date 20261302 --output scratch/db-bad.db; echo "EXIT=$?"
echo; echo "### C) download-db 2026110 (wrong format)"; $P tool/bootstrap.py download-db --date 2026110 --output scratch/db-short.db; echo "EXIT=$?"
echo; echo "### D) INTERNAL_CI contrast (same date, GET path semantics)"; OSKM_DOWNLOAD_SOURCE=INTERNAL_CI $P tool/bootstrap.py download-db --date 20261102 --output scratch/db-internal.db; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && P=/opt/homebrew/opt/python@3.12/bin/python3.12
echo "### validate-db"; $P tool/bootstrap.py validate-db runtime/knowledge.db; echo "EXIT=$?"
echo; echo "### cli-path"; $P tool/bootstrap.py cli-path
echo; echo "### CLI --version"; $P runtime/oskm-cli.pyz --version
echo; echo "### CLI help"; $P runtime/oskm-cli.pyz --help 2>&1 | head -30'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && shasum -a 256 runtime/knowledge.db scratch/knowledge.db scratch/db-20261101.db && ls -l runtime/knowledge.db scratch/*.db && echo "=== archive contents check (what the tarball carried) ===" && find runtime/interface -maxdepth 3 | sort'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 - <<'PY'
import io, json, sys
from pathlib import Path
HERE = Path.cwd(); sys.path.insert(0, str(HERE / 'tool'))
from oskm_runtime import db_download as dd
real_open = dd._open
class FakeResp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): self.close(); return False
seen = []
def spy(request, *, timeout, attempts, retry_delay):
    r = real_open(request, timeout=timeout, attempts=attempts, retry_delay=retry_delay)
    raw = r.read()
    seen.append((request.get_method(), request.full_url,
                 json.loads(request.data) if request.data else None,
                 raw[:200].decode('utf-8','replace')))
    return FakeResp(raw)
dd._open = spy
for date in ('20261101', '20261102', '20261103'):
    seen.clear()
    try:
        dd.download_database(source='OPENHARMONY_CI', date=date,
                             output=HERE / 'scratch' / f'probe-{date}.db')
        status = 'ok'
    except Exception as exc:
        status = f'{type(exc).__name__}: {exc}'
    print(f'--- date={date} -> {status}')
    for m, u, b, resp in seen:
        win = (b.get('startTime'), b.get('endTime')) if b else None
        print(f'    {m} {u}')
        if b: print(f'    window startTime={win[0]} endTime={win[1]} component={b[\"component\"]}')
        if m == 'POST': print(f'    resp={resp}')
PY"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && shasum -a 256 scratch/probe-*.db && P=/opt/homebrew/opt/python@3.12/bin/python3.12
echo "=== arch overview ==="; $P runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview 2>&1 | head -25
echo; echo "=== tables ==="; $P runtime/oskm-cli.pyz --db runtime/knowledge.db sql "select name from sqlite_master where type='"'table' order by name\" 2>&1 | head -20"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && sed -n '90,177p' tool/oskm_runtime/state.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && P=/opt/homebrew/opt/python@3.12/bin/python3.12
echo "### refresh --date 20261102 (idempotent?)"; $P tool/bootstrap.py refresh --date 20261102; echo "EXIT=$?"
echo; echo "### needs_refresh() read-only probe"; $P - <<'"'PY'
import sys; from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'tool'))
from oskm_runtime import state
db = Path('runtime/knowledge.db')
for d in ('20261102', '20261117'):
    print(f'  needs_refresh(current_date={d}) -> {state.needs_refresh(db, current_date=d)}')
print('  today() ->', state.today())
PY
echo; echo \"### runtime unchanged?\"; grep -E '\"date\"|\"source\"' runtime/.oskm-runtime.json | head -4; shasum -a 256 runtime/knowledge.db"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && rm scratch/probe-20261101.db scratch/probe-20261102.db scratch/probe-20261103.db scratch/knowledge.db scratch/db-20261101.db && rmdir scratch && echo "scratch removed" && ls -la . && ls -la runtime'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && cat > answer.md <<'MD'
# OPENHARMONY_CI 安装 date=20261102

## 结论（直接回答）

"'`--date 20261102` 在 `OPENHARMONY_CI` 下**不是** URL 路径片段，也**不是**精确主键匹配，而是被翻译成
"当天时间窗"塞进一个 **POST JSON body**；工具只取返回列表的**第一条**构建，再用它的 `obsPath`
发第二个 GET 把 `knowledge.tar.gz` 拉下来。两次请求，端点原样使用（不追加 `/20261102`）。

安装已完成并通过自检：`runtime/` 下 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` +
`interface/sdk_c`，状态文件记录 `date=20261102`。

## 关键命令

```bash
cd <workspace>
P=/opt/homebrew/opt/python@3.12/bin/python3.12

$P tool/bootstrap.py doctor                       # 安装前：CLI FAIL / 运行时未安装
$P tool/bootstrap.py install --date 20261102      # 真正的安装
$P tool/bootstrap.py doctor                       # 安装后：全绿
$P tool/bootstrap.py validate-db runtime/knowledge.db
$P tool/bootstrap.py cli-path
$P runtime/oskm-cli.pyz --version
$P runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
$P tool/bootstrap.py refresh --date 20261102      # 幂等性验证
```

没有用 `--runtime-root`，也没有碰 `~/.oskm`：根目录由 `$OSKM_RUNTIME_ROOT` 解析到工作区的 `runtime/`。

## 关键输出

安装前 doctor（说明为什么要 install，以及 CLI 来自归档而非单独端点）：

```
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布 …
  1. $OSKM_CLI 未设置  2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py  3. <root>/oskm-cli.pyz —— 不存在
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。   EXIT=1
```

安装本体（stderr 只有两行，说明没有走源码树本地运行时，直接下载）：

```
==> 下载 OPENHARMONY_CI 运行时: 20261102
==> 运行时安装完成: <workspace>/runtime      EXIT=0
```

安装后 doctor / 校验 / 查询：

```
CLI: <workspace>/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓
EXIT=0

{"path": "runtime/knowledge.db", "ok": true}
oskm-cli 1.0.0
arch overview -> {"product": "synthetic", "scan_id": 1, "subsystems": 2, "counts": {"repos": 1, "components": 2, …}}
```

`runtime/.oskm-runtime.json`（出处记录，sha256 不是版本锁）：

```json
{"version": 3, "source": "OPENHARMONY_CI", "date": "20261102",
 "db":  {"date": "20261102", "path": "knowledge.db",
         "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44"},
 "sdk": {"date": "20261102", "sdk-js": {"path": "interface/sdk-js"}, "sdk_c": {"path": "interface/sdk_c"}},
 "cli": {"path": "oskm-cli.pyz", "sha256": "ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e"}}
```

## 实际请求语义（抓到的真实报文）

用 in-process spy 包住 `oskm_runtime.db_download._open`（**没有改工具代码、没有改夹具**）跑同一
下载路径，抓到两次请求：

```
[1] POST http://127.0.0.1:61141/openharmony/api/daily_build/build/list/component  -> HTTP 200
    headers: {"Accept": "application/json", "Content-type": "application/json"}
    body:
      {"projectName": "openharmony", "branch": "master", "pageNum": 1, "pageSize": 10,
       "deviceLevel": "", "component": "dayu600_7885_ai", "type": 1,
       "startTime": "2026110200000000", "endTime": "20261102235959",
       "sortType": "", "sortField": "", "hardwareBoard": "",
       "buildStatus": "success", "buildFailReason": "", "withDomain": 1}
    resp: {"data": {"list": {"dataList": [{"obsPath": "/openharmony/obs/20261102/knowledge.tar.gz"}]}}}

[2] GET http://127.0.0.1:61141/openharmony/obs/20261102/knowledge.tar.gz  -> HTTP 200, 93314 bytes
    headers: {"Accept": "application/octet-stream"}
```

逐条语义：

- **date → 时间窗，不是等值查询。** `startTime = date + "00000000"`（16 位），
  `endTime = date + "235959"`（14 位）。两个边界**位数不对称**：起点补 8 个 0，终点补 6 位时分秒。
  对 14 位 `YYYYMMDDHHMMSS` 型时间戳做字典序比较时仍能正确夹住一整天，但如果服务端做严格长度/格式
  校验，这是个坑（夹具服务接受了）。
- **端点不被改写。** `OPENHARMONY_CI` 直接 POST 到 `$OSKM_DOWNLOAD_ENDPOINT`；
  对照 `INTERNAL_CI` 才是 `GET <endpoint>/<YYYYMMDD>`（date 是路径片段）。实测对照：

  ```
  OSKM_DOWNLOAD_SOURCE=INTERNAL_CI bootstrap.py download-db --date 20261102 …
  错误: 下载失败（HTTP 404）: http://127.0.0.1:61141/openharmony/api/daily_build/build/list/component/20261102
  ```

- **固定查询条件。** `component=dayu600_7885_ai`（`environment.OPENHARMONY_COMPONENT`，不可通过 CLI
  参数改）、`projectName=openharmony`、`branch=master`、`type=1`、`buildStatus=success`、
  `withDomain=1`、`pageNum=1/pageSize=10`；`sortType`/`sortField` 传空串 → **排序完全由服务端默认决定**。
- **只取第一条。** 解析路径写死为 `data.list.dataList[0].obsPath`。所以真实语义是
  "该日窗口内、该组件、构建成功的列表里的第一条"，而**不是**"精确等于 20261102 的那一次构建"；
  客户端不会回头校验返回条目的日期是否真的等于 `--date`。缺键/空值/空列表一律报
  `该日期没有成功构建：<date>`（HTTP 200 也算失败）。
- **obsPath → 绝对 URL。** `urljoin(endpoint, obsPath)`：`obsPath` 以 `/` 开头时只保留
  scheme+host，路径被整体替换；相对路径则会拼在端点目录后面。下载文件名取 URL 最后一段
  （`knowledge.tar.gz`），不自己造名字。
- **date 校验在客户端、先于网络。** `--date` 必须是 8 位数字且是合法日历日：

  ```
  --date 20261302 -> 错误: --date 不是有效日期: 20261302   EXIT=1
  --date 2026110  -> 错误: --date 必须是 YYYYMMDD: 2026110 EXIT=1
  ```

- **重试/超时。** 每次请求 `timeout=90s`、`attempts=3`、`retry_delay=2s`；只有
  408/429/500/502/503/504 与 `OSError`（网络/DNS/代理/TLS）才重试，404 之类立即失败。
- **归档落地语义（install 走的是 `download_runtime_bundle`）。** 一个 tar 里同时带
  `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`；解压做越界路径/符号链接
  防护，校验 SQLite 头 + `PRAGMA integrity_check`，schema 契约由**归档自带的那个 CLI** 执行，
  然后原子替换到 `runtime/`，任一步失败逆序回滚（旧运行时不会被半装状态破坏）。
- **本地源码树优先于网络。** install 会先从 cwd 向上找 OpenHarmony 源码根
  （`.gn` + `interface/sdk-js` + `interface/sdk_c` + `out` 且 SDK 非空 + 有可用 CLI）；命中就
  **一个请求都不发**，状态里 `source` 写成 `local`。本工作区没有源码根，所以走了下载，
  状态里是 `source: OPENHARMONY_CI`。
- **install 与 refresh 的日期语义不同。** `install` 无条件下载（`--date` 缺省 = 系统当天，本机是
  20261117）；`refresh` 先做廉价判定，`state.date != current_date` 即视为过期。实测：

  ```
  bootstrap.py refresh --date 20261102 -> ==> 运行时已是最新，无需刷新   EXIT=0（零请求）
  needs_refresh(current_date=20261102) -> False
  needs_refresh(current_date=20261117) -> True
  ```

  推论：**不要**在这台机器上跑不带 `--date` 的 `refresh`，它会因为"今天"是 20261117 而把运行时
  重装成 20261117，覆盖掉本次要求的 20261102。要保住日期就每次显式带 `--date 20261102`。

## 夹具侧观察（不影响上述结论）

对 20261101 / 20261102 / 20261103 分别请求，服务端按窗口回声对应的
`/openharmony/obs/<date>/knowledge.tar.gz`，但三份 `knowledge.db` 的 sha256 完全相同
（`f561e39f…`）——测试服务对不同日期返回同一份载荷。也就是说：日期区分度来自**请求语义**，
在这个夹具上无法用产物内容反证；判断"请求到底怎么发的"只能看报文，上面已给出。
MD
wc -l answer.md && echo OK'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor | sed -n '1,8p'; echo \"EXIT="'$?"; ls -l answer.md; ls tool tool/oskm_runtime | head -20'
```

### Agent 最终回答

```markdown
**安装结果**
- `install --date 20261102` 成功，运行时落在 `runtime/`：`knowledge.db`(434176B) + `oskm-cli.pyz`(1.0.0) + `interface/sdk-js` + `interface/sdk_c` + `.oskm-runtime.json`(`version 3, date 20261102, source OPENHARMONY_CI`)。
- 验证通过：`doctor` 全绿(EXIT=0)、`validate-db` 返回 `{"ok": true}`、`oskm-cli.pyz --db runtime/knowledge.db arch overview` 可查询、`refresh --date 20261102` 零请求短路。未碰 `~/.oskm`，未改 `tool/`。

**实际请求语义**
- 日期不是路径片段、也不是等值键，而是 POST JSON 里的**当天时间窗**：`startTime="2026110200000000"`(16 位) / `endTime="20261102235959"`(14 位)——两个边界位数不对称，见 `tool/oskm_runtime/db_download.py:145`。
- 端点原样 POST，固定条件 `component=dayu600_7885_ai`、`buildStatus=success`、`type=1`、`pageSize=10`、`sortField/sortType` 空串(排序由服务端决定)；只取 `data.list.dataList[0].obsPath`，即"窗口内第一条成功构建"，客户端不回头校验它的日期。
- 第二跳 `urljoin(endpoint, obsPath)` → `GET /openharmony/obs/20261102/knowledge.tar.gz`(`Accept: application/octet-stream`)，一个 tar 同时带 DB+CLI+两套 SDK，原子安装、失败逆序回滚。
- 对照实测：`INTERNAL_CI` 才是 `GET <endpoint>/<date>`(同一端点返回 404)；非法日期(`20261302`/`2026110`)在客户端就被拦下，不发请求。
- 注意：本机"今天"是 20261117，不带 `--date` 的 `refresh` 会把运行时重装成 20261117，覆盖 20261102。

**产物**
- 结论、关键命令与抓包片段已写入 `answer.md`(工作区根目录)；抓包用 in-process spy 包住 `_open` 完成，未修改工具或夹具。
```

### Agent 写入的 answer.md

```markdown
# OPENHARMONY_CI 安装 date=20261102

## 结论（直接回答）

`--date 20261102` 在 `OPENHARMONY_CI` 下**不是** URL 路径片段，也**不是**精确主键匹配，而是被翻译成
"当天时间窗"塞进一个 **POST JSON body**；工具只取返回列表的**第一条**构建，再用它的 `obsPath`
发第二个 GET 把 `knowledge.tar.gz` 拉下来。两次请求，端点原样使用（不追加 `/20261102`）。

安装已完成并通过自检：`runtime/` 下 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` +
`interface/sdk_c`，状态文件记录 `date=20261102`。

## 关键命令

```bash
cd <workspace>
P=/opt/homebrew/opt/python@3.12/bin/python3.12

$P tool/bootstrap.py doctor                       # 安装前：CLI FAIL / 运行时未安装
$P tool/bootstrap.py install --date 20261102      # 真正的安装
$P tool/bootstrap.py doctor                       # 安装后：全绿
$P tool/bootstrap.py validate-db runtime/knowledge.db
$P tool/bootstrap.py cli-path
$P runtime/oskm-cli.pyz --version
$P runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
$P tool/bootstrap.py refresh --date 20261102      # 幂等性验证
```

没有用 `--runtime-root`，也没有碰 `~/.oskm`：根目录由 `$OSKM_RUNTIME_ROOT` 解析到工作区的 `runtime/`。

## 关键输出

安装前 doctor（说明为什么要 install，以及 CLI 来自归档而非单独端点）：

```
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布 …
  1. $OSKM_CLI 未设置  2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py  3. <root>/oskm-cli.pyz —— 不存在
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。   EXIT=1
```

安装本体（stderr 只有两行，说明没有走源码树本地运行时，直接下载）：

```
==> 下载 OPENHARMONY_CI 运行时: 20261102
==> 运行时安装完成: <workspace>/runtime      EXIT=0
```

安装后 doctor / 校验 / 查询：

```
CLI: <workspace>/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓
EXIT=0

{"path": "runtime/knowledge.db", "ok": true}
oskm-cli 1.0.0
arch overview -> {"product": "synthetic", "scan_id": 1, "subsystems": 2, "counts": {"repos": 1, "components": 2, …}}
```

`runtime/.oskm-runtime.json`（出处记录，sha256 不是版本锁）：

```json
{"version": 3, "source": "OP
… [输出截断，完整内容见工作区] …
ck`，schema 契约由**归档自带的那个 CLI** 执行，
  然后原子替换到 `runtime/`，任一步失败逆序回滚（旧运行时不会被半装状态破坏）。
- **本地源码树优先于网络。** install 会先从 cwd 向上找 OpenHarmony 源码根
  （`.gn` + `interface/sdk-js` + `interface/sdk_c` + `out` 且 SDK 非空 + 有可用 CLI）；命中就
  **一个请求都不发**，状态里 `source` 写成 `local`。本工作区没有源码根，所以走了下载，
  状态里是 `source: OPENHARMONY_CI`。
- **install 与 refresh 的日期语义不同。** `install` 无条件下载（`--date` 缺省 = 系统当天，本机是
  20261117）；`refresh` 先做廉价判定，`state.date != current_date` 即视为过期。实测：

  ```
  bootstrap.py refresh --date 20261102 -> ==> 运行时已是最新，无需刷新   EXIT=0（零请求）
  needs_refresh(current_date=20261102) -> False
  needs_refresh(current_date=20261117) -> True
  ```

  推论：**不要**在这台机器上跑不带 `--date` 的 `refresh`，它会因为"今天"是 20261117 而把运行时
  重装成 20261117，覆盖掉本次要求的 20261102。要保住日期就每次显式带 `--date 20261102`。

## 夹具侧观察（不影响上述结论）

对 20261101 / 20261102 / 20261103 分别请求，服务端按窗口回声对应的
`/openharmony/obs/<date>/knowledge.tar.gz`，但三份 `knowledge.db` 的 sha256 完全相同
（`f561e39f…`）——测试服务对不同日期返回同一份载荷。也就是说：日期区分度来自**请求语义**，
在这个夹具上无法用产物内容反证；判断"请求到底怎么发的"只能看报文，上面已给出。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**安装结果**
- `install --date 20261102` 成功，运行时落在 `runtime/`：`knowledge.db`(434176B) + `oskm-cli.pyz`(1.0.0) + `interface/sdk-js` + `interface/sdk_c` + `.oskm-runtime.json`(`version 3, date 20261102, source OPENHARMONY_CI`)。
- 验证通过：`doctor` 全绿(EXIT=0)、`validate-db` 返回 `{"ok": true}`、`oskm-cli.pyz --db runtime/knowledge.db arch overview` 可查询、`refresh --date 20261102` 零请求短路。未碰 `~/.oskm`，未改 `tool/`。

**实际请求语义**
- 日期不是路径片段、也不是等值键，而是 POST JSON 里的**当天时间窗**：`startTime="2026110200000000"`(16 位) / `endTime="20261102235959"`(14 位)——两个边界位数不对称，见 `tool/oskm_runtime/db_download.py:145`。
- 端点原样 POST，固定条件 `component=dayu600_7885_ai`、`buildStatus=success`、`type=1`、`pageSize=10`、`sortField/sortType` 空串(排序由服务端决定)；只取 `data.list.dataList[0].obsPath`，即"窗口内第一条成功构建"，客户端不回头校验它的日期。
- 第二跳 `urljoin(endpoint, obsPath)` → `GET /openharmony/obs/20261102/knowledge.tar.gz`(`Accept: application/octet-stream`)，一个 tar 同时带 DB+CLI+两套 SDK，原子安装、失败逆序回滚。
- 对照实测：`INTERNAL_CI` 才是 `GET <endpoint>/<date>`(同一端点返回 404)；非法日期(`20261302`/`2026110`)在客户端就被拦下，不发请求。
- 注意：本机"今天"是 20261117，不带 `--date` 的 `refresh` 会把运行时重装成 20261117，覆盖 20261102。

**产物**
- 结论、关键命令与抓包片段已写入 `answer.md`(工作区根目录)；抓包用 in-process spy 包住 `_open` 完成，未修改工具或夹具。stderr:
2026-11-17T07:33:43.348825Z ERROR codex_skills_extension::host_service: failed to install system skills: io error while remove existing system skills dir: Directory not empty (os error 66)
2026-11-17T07:39:31.345096Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc \\\"cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date && rm -rf scratch && ls -la . runtime && echo \\\\\\\"--- leftovers? ---\\\\\\\" && find runtime -name '.*tmp*' -o -name '.oskm-runtime-backup*' -o -name '.oskm-runtime-install*' | head\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e02-openharmony-exact-date` · exit=0 · 462.1s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（13 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T15:35:34.186+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/json",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "deviceLevel": "",
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "2026110200000000",
      "endTime": "20261102235959",
      "sortType": "",
      "sortField": "",
      "hardwareBoard": "",
      "buildStatus": "success",
      "buildFailReason": "",
      "withDomain": 1
    }
  },
  {
    "seq": 2,
    "ts": "2026-11-17T15:35:34.187+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 3,
    "ts": "2026-11-17T15:36:47.007+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/json",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "deviceLevel": "",
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "2026110200000000",
      "endTime": "20261102235959",
      "sortType": "",
      "sortField": "",
      "hardwareBoard": "",
      "buildStatus": "success",
      "buildFailReason": "",
      "withDomain": 1
    }
  },
  {
    "seq": 4,
    "ts": "2026-11-17T15:36:47.008+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 5,
    "ts": "2026-11-17T15:37:30.561+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/json",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "deviceLevel": "",
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "2026110100000000",
      "endTime": "20261101235959",
      "sortType": "",
      "sortField": "",
      "hardwareBoard": "",
      "buildStatus": "success",
      "buildFailReason": "",
      "withDomain": 1
    }
  },
  {
    "seq": 6,
    "ts": "2026-11-17T15:37:30.561+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261101/knowledge.tar.gz",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 7,
    "ts": "2026-11-17T15:37:30.755+08:00",
    "method": "GET",
    "path": "/openharmony/api/daily_build/build/list/component/20261102",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 8,
    "ts": "2026-11-17T15:37:59.529+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/json",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "deviceLevel": "",
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "2026110100000000",
      "endTime": "20261101235959",
      "sortType": "",
      "sortField": "",
      "hardwareBoard": "",
      "buildStatus": "success",
      "buildFailReason": "",
      "withDomain": 1
    }
  },
  {
    "seq": 9,
    "ts": "2026-11-17T15:37:59.529+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261101/knowledge.tar.gz",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 10,
    "ts": "2026-11-17T15:37:59.533+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/json",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "deviceLevel": "",
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "2026110200000000",
      "endTime": "20261102235959",
      "sortType": "",
      "sortField": "",
      "hardwareBoard": "",
      "buildStatus": "success",
      "buildFailReason": "",
      "withDomain": 1
    }
  },
  {
    "seq": 11,
    "ts": "2026-11-17T15:37:59.534+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 12,
    "ts": "2026-11-17T15:37:59.537+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/json",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "deviceLevel": "",
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "2026110300000000",
      "endTime": "20261103235959",
      "sortType": "",
      "sortField": "",
      "hardwareBoard": "",
      "buildStatus": "success",
      "buildFailReason": "",
      "withDomain": 1
    }
  },
  {
    "seq": 13,
    "ts": "2026-11-17T15:37:59.538+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261103/knowledge.tar.gz",
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

自动断言 8/9 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 工具的请求只落在"构建列表 POST + obs 归档 GET"两条路径上 | auto | Fail | POST=6 GET=7；[{"method": "POST", "path": "/openharmony/api/daily_build/build/list/component"}, {"method": "GET", "path": "/openharmony/obs/20261102/knowledge.tar.gz"}, {"method": "POST", "path": "/ope
… [输出截断，完整内容见工作区] …
ild/build/list/component"}, {"method": "GET", "path": "/openharmony/obs/20261103/knowledge.tar.gz"}] |
| 2 | component 固定为 dayu600_7885_ai（不需要用户传） | auto | Pass | component=dayu600_7885_ai |
| 3 | 起止时间都来自同一个显式日期 | auto | Pass | startTime=2026110200000000 endTime=20261102235959 |
| 4 | 只取构建成功的记录 | auto | Pass | buildStatus=success |
| 5 | 下载物是 knowledge.tar.gz | auto | Pass | /openharmony/obs/20261102/knowledge.tar.gz |
| 6 | 请求里没有 latest 语义 | auto | Pass | request log 无 latest |
| 7 | 状态文件记录 source=OPENHARMONY_CI 与 date=20261102 | auto | Pass | {"source": "OPENHARMONY_CI", "date": "20261102"} |
| 8 | 四件产物装齐 | auto | Pass | db=True cli=True |
| 9 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：FAIL**
