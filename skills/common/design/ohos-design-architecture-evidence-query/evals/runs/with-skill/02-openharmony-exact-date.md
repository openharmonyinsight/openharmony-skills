# E2 openharmony-exact-date（with-skill 臂）

- 开始时间：2026-11-17T16:18:33+08:00
- 结束时间：2026-11-17T16:24:26+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date`
- 夹具服务端：http://127.0.0.1:61813
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：352.2 s
- 事件计数：`{"thread.started": 1, "item.completed": 52, "item:error": 1, "turn.started": 1, "item:reasoning": 16, "item:agent_message": 13, "item.started": 22, "item:command_execution": 44, "turn.completed": 1}`
- 读到 skill 文档：是（19 处）
- 执行的命令数：22
- token 用量：`{"input_tokens": 416325, "cached_input_tokens": 380800, "output_tokens": 12260, "reasoning_output_tokens": 4956}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && ls -la && echo "---ENV---" && env | grep -i oskm'
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && ls -la && echo "---" && cat /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date/PROMPT.md'
$ /bin/zsh -lc "sed -n '1,200p' /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/bootstrap.py"
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/oskm_runtime && ls -la && wc -l *.py'
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && grep -rn "date" oskm_runtime/bootstrap.py | head -60'
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && sed -n '1,180p' oskm_runtime/db_download.py"
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && sed -n '180,330p' oskm_runtime/db_download.py"
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && cat oskm_runtime/environment.py'
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && cat oskm_runtime/state.py && echo \"=====INSTALL=====\" && sed -n '1,140p' oskm_runtime/install.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" doctor; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && find runtime -maxdepth 2 | head -40 && echo "=====STATE=====" && cat runtime/.oskm-runtime.json'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" doctor; echo "doctor_exit=$?"; echo "=====CLI-PATH====="; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" cli-path; echo "clipath_exit=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && cat > probe_request.py <<'PY'
\"\"\"Log the exact HTTP request(s) the OPENHARMONY_CI installer issues.\"\"\"
import io, json, os, sys
from pathlib import Path

SKILL_DIR = Path(os.environ['CODEX_HOME']) / 'skills' / 'ohos-design-architecture-evidence-query'
sys.path.insert(0, str(SKILL_DIR))

from oskm_runtime import db_download
from oskm_runtime.environment import download_config

real_urlopen = db_download.urlopen

def logged_urlopen(request, timeout=None):
    body = request.data
    print('--- REQUEST ---')
    print('method :', request.get_method())
    print('url    :', request.full_url)
    print('headers:', json.dumps(dict(request.headers), ensure_ascii=False))
    if body:
        print('body   :', json.dumps(json.loads(body), ensure_ascii=False, indent=2))
    response = real_urlopen(request, timeout=timeout)
    raw = response.read()
    print('--- RESPONSE ---')
    print('status :', response.status, response.reason)
    try:
        print('json   :', json.dumps(json.loads(raw), ensure_ascii=False, indent=2)[:2000])
    except Exception:
        print('bytes  :', len(raw))
    return io.BytesIO(raw)

db_download.urlopen = logged_urlopen

for date in sys.argv[1:]:
    print(f'===== _fetch_openharmony_obs_path(date={date}) =====')
    try:
        print('resolved download URL ->',
              db_download._fetch_openharmony_obs_path(
                  download_config(), date, timeout=10, attempts=1, retry_delay=0))
    except db_download.DownloadError as exc:
        print('DownloadError ->', exc)
PY
/opt/homebrew/opt/python@3.12/bin/python3.12 probe_request.py 20261102"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 probe_request.py 20261101 20261103 2>&1 | grep -v '"'^ *"'"' | grep -Ev '"'^(  |'"\\}|body|headers)' "
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && cat > probe_download.py <<'PY'
\"\"\"Log every HTTP request issued by _download_archive for one date.\"\"\"
import io, json, os, sys, tempfile
from pathlib import Path

SKILL_DIR = Path(os.environ['CODEX_HOME']) / 'skills' / 'ohos-design-architecture-evidence-query'
sys.path.insert(0, str(SKILL_DIR))
from oskm_runtime import db_download
from oskm_runtime.environment import download_config

real_urlopen = db_download.urlopen
def logged_urlopen(request, timeout=None):
    print(f'>>> {request.get_method()} {request.full_url}')
    print('    headers:', json.dumps(dict(request.headers), ensure_ascii=False))
    if request.data:
        print('    body   :', request.data.decode())
    response = real_urlopen(request, timeout=timeout)
    raw = response.read()
    print(f'    <- {response.status} {response.reason}, {len(raw)} bytes')
    return io.BytesIO(raw)
db_download.urlopen = logged_urlopen

date = sys.argv[1]
with tempfile.TemporaryDirectory() as work_dir:
    archive = db_download._download_archive(
        config=download_config(), date=date, work_dir=Path(work_dir),
        timeout=15, attempts=1, retry_delay=0)
    print('archive saved as:', archive.name)
    print('members:', db_download._archive_member_names(archive)[:12])
PY
/opt/homebrew/opt/python@3.12/bin/python3.12 probe_download.py 20261102"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query" && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== refresh same date (expect no-op) ===" && $PY "$SKILL_DIR/bootstrap.py" refresh --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102; echo "exit=$?"; echo "=== install --date 2026-11-02 (bad format) ===" && $PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" --date 2026-11-02; echo "exit=$?"; echo "=== install --date 20261332 (invalid date) ===" && $PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261332; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && CLI="$OSKM_RUNTIME_ROOT/oskm-cli.pyz" && DB="$OSKM_RUNTIME_ROOT/knowledge.db" && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY "$CLI" --version; echo "=== validate-db ==="; SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"; $PY "$SKILL_DIR/bootstrap.py" validate-db "$DB"; echo "exit=$?"; echo "=== get_scan_info ==="; $PY "$CLI" --db "$DB" ask get_scan_info 2>&1 | head -40'
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && grep -n \"timeout\\|attempts\\|retry_delay\\|def download_runtime_bundle\\|OSKM_\" oskm_runtime/db_download.py | sed -n '1,60p' && echo \"=====INSTALL CALL=====\" && grep -n \"download_runtime_bundle\" -A 18 oskm_runtime/install.py | head -50"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date && cat > answer.md <<'MD'
# OPENHARMONY_CI + date=20261102：安装结果与实际请求语义

运行时根目录（"'`OSKM_RUNTIME_ROOT`）安装前为空，现已装齐 `knowledge.db` + `oskm-cli.pyz` +
`interface/sdk-js` + `interface/sdk_c`，`doctor` 全绿，CLI 可查询。

## 1. 执行过的关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"

$PY "$SKILL_DIR/bootstrap.py" doctor                                             # 装前体检
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102
$PY "$SKILL_DIR/bootstrap.py" doctor                                             # 装后体检
$PY "$SKILL_DIR/bootstrap.py" cli-path
$PY "$SKILL_DIR/bootstrap.py" validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask get_scan_info
$PY "$SKILL_DIR/bootstrap.py" refresh --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102

# 只读探针：打印安装器真实发出的 HTTP 请求（不改动 skill / fixtures）
$PY probe_request.py 20261102        # 只发列表 POST，打印请求体与响应
$PY probe_download.py 20261102       # 走完整 POST → GET 两段，落到临时目录
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" --date 2026-11-02
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261332
```

## 2. 关键输出片段

装前 `doctor`（exit=1）：

```
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
CLI: FAIL: 找不到可用的 oskm-cli 产物。… 已尝试：$OSKM_CLI 未设置 / 源码树 / <root>/oskm-cli.pyz 不存在
错误: 运行时依赖检查未通过。
```

`install --date 20261102`（exit=0）：

```
==> 下载 OPENHARMONY_CI 运行时: 20261102
==> 运行时安装完成: …/e02-openharmony-exact-date/runtime
```

装后 `doctor`（exit=0）：

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
```

`validate-db` 与 CLI 自检：

```
{"path": "…/runtime/knowledge.db", "ok": true}
oskm-cli 1.0.0
get_scan_info → {"scan_id": 1, "product": "synthetic", "cpu_arch": "arm64", "status": "complete",
                 "started_at": "2026-11-02T00:00:00Z", "collectors": [args/arkts/components/elf_modules/hdi … 均 complete]}
```

`refresh --date 20261102`（幂等，无网络）：

```
==> 运行时已是最新，无需刷新: …/e02-openharmony-exact-date/runtime
```

`--date` 前置校验（未发任何请求即退出 1）：

```
错误: --date 必须是 YYYYMMDD: 2026-11-02
错误: --date 不是有效日期: 20261332
```

## 3. 实际请求语义（对任务的直接回答）

`--date 20261102` 在 `OPENHARMONY_CI` 下**不是拼进 URL 路径**，而是变成对构建列表 API 的一次
POST 查询条件（当天时间窗），再由响应里的 `obsPath` 决定第二个 GET 的下载地址。共两次 HTTP 请求：

**① POST 列表查询**（探针实测原文）

```
POST http://127.0.0.1:61813/openharmony/api/daily_build/build/list/component
Accept: application/json
Content-Type: application/json

{"projectName":"openharmony","branch":"master","pageNum":1,"pageSize":10,"deviceLevel":"",
 "component":"dayu600_7885_ai","type":1,
 "startTime":"2026110200000000","endTime":"20261102235959",
 "sortType":"","sortField":"","hardwareBoard":"","buildStatus":"success",
 "buildFailReason":"","withDomain":1}
```

- 日期语义 = **同一天闭区间**：`startTime = <date> + "00000000"`（16 位），`endTime = <date> + "235959"`（14 位），
  两个字段格式不对称，客户端按字符串原样发送，不做补零对齐。
- `component` 硬编码为 `dayu600_7885_ai`，不可通过参数改；`buildStatus=success`、`type=1`、
  `branch=master`、`projectName=openharmony`、`withDomain=1` 同为固定值。
- `sortType` / `sortField` 留空 → 排序完全交给服务端；客户端**不做日期二次过滤**。
- 分页固定 `pageNum=1, pageSize=10`，且**只取 `data.list.dataList[0].obsPath`**：
  同一天有多次成功构建时，用服务端返回的第一条，不会遍历或挑选。

**② GET 归档下载**

```
obsPath = "/openharmony/obs/20261102/knowledge.tar.gz"
urljoin(endpoint, obsPath) → http://127.0.0.1:61813/openharmony/obs/20261102/knowledge.tar.gz
GET … Accept: application/octet-stream  → 200 OK, 94326 bytes，保存为 knowledge.tar.gz
成员: knowledge.db, oskm-cli.pyz, interface/sdk-js/…, interface/sdk_c/…
```

- `urljoin` 语义：`obsPath` 以 `/` 开头时是**站点根绝对路径**，endpoint 的整个 path
  （`/openharmony/api/daily_build/build/list/component`）被丢弃，只保留 scheme+host；
  若服务端返回相对路径，才会相对 endpoint 所在目录解析。
- 归档名取自 URL 路径末段，`knowledge.tar.gz` 是唯一发布单元，CLI 不单独下载。

**失败与回退语义**

- `obsPath` 缺失或为空 → `DownloadError: 该日期没有成功构建，或 obsPath 为空（20261102）`；
  响应不是合法 JSON → `…构建响应不是有效 JSON（<date>）`。
- **没有"就近日期回退"**：请求窗口只覆盖当天，拿不到就是失败退出，不会自动改试前一天/后一天。
- HTTP 层只对 `408/429/500/502/503/504` 重试；其余（如 404）立即失败并提示检查该日期/资源是否存在。
  默认 `timeout=90s, attempts=3, retry_delay=2s`。
- 与 `INTERNAL_CI` 的差别：后者是 `url = f'"'{endpoint}/{date}'"'` 的单次 GET，日期直接进路径；
  `OPENHARMONY_CI` 才有上面这套 POST 查询窗口。

**日期还参与幂等判定**

- 安装成功后 `date` 与 `sha256` 写入 `<root>/.oskm-runtime.json`（`version: 3`）。
- `refresh --date 20261102` 命中同一日期 → 直接 no-op，不联网；换一个日期才会重新下载安装。
- `install`/`refresh` 缺省 `--date` 时取系统当天（`state.today()`），本次显式指定为 20261102。

## 4. 落盘结果

```
runtime/knowledge.db
runtime/oskm-cli.pyz
runtime/interface/sdk-js/…
runtime/interface/sdk_c/…
runtime/.oskm-runtime.json
```

`.oskm-runtime.json` 关键字段：

```json
{"version": 3, "source": "OPENHARMONY_CI", "date": "20261102",
 "db":  {"date": "20261102", "path": "knowledge.db",
         "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44"},
 "sdk": {"date": "20261102", "sdk-js": {"path": "interface/sdk-js"}, "sdk_c": {"path": "interface/sdk_c"}},
 "cli": {"path": "oskm-cli.pyz",
         "sha256": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5"}}
```

## 5. 夹具说明

本地夹具服务对任意日期都回显对应的 `obsPath`（实测 20261101 / 20261103 同样返回 200），
所以"该日期确有成功构建"这一约束在真实 CI 侧才成立；客户端只负责把日期收敛成当天窗口并取首条。
DB 为合成快照（`product=synthetic`，各采集器 `record_count=1`），可打开、schema 校验通过，
适合验证安装链路，不代表真实产品证据规模。
MD
echo "written: $(wc -l < answer.md) lines"; ls -la answer.md probe_request.py probe_download.py'
$ /bin/zsh -lc 'ls -la "$HOME/.oskm" 2>&1 | head -3; echo "--- runtime ---"; ls -la "$OSKM_RUNTIME_ROOT"; echo "--- git-ish check: fixtures untouched (no writes outside workspace) ---"; ls "$CODEX_HOME/skills/ohos-design-architecture-evidence-query"'
```

### Agent 最终回答

```markdown
**安装结果**
- `bootstrap.py install --date 20261102` 成功（exit=0），`$OSKM_RUNTIME_ROOT` 装齐 `knowledge.db`、`oskm-cli.pyz`(1.0.0)、`interface/sdk-js`、`interface/sdk_c`。
- 装后 `doctor` 全绿：`Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓`；`validate-db` 返回 `{"ok": true}`；`ask get_scan_info` 可查（`product=synthetic`, `status=complete`）。
- `refresh --date 20261102` 为 no-op（“运行时已是最新”），`~/.oskm` 未被创建，skill 与夹具目录未改动。

**实际请求语义**（用只读探针 `probe_request.py` / `probe_download.py` 实测，非凭记忆）
- 日期不进 URL，而是变成对列表 API 的一次 `POST`：`startTime="2026110200000000"`、`endTime="20261102235959"`（同一天窗口，两字段位数不对称，原样发送），固定 `component=dayu600_7885_ai`、`buildStatus=success`、`type=1`、`branch=master`、`pageNum=1/pageSize=10`、`sortType/sortField` 留空。
- 响应只取 `data.list.dataList[0].obsPath` → `urljoin(endpoint, obsPath)`。因 `obsPath` 以 `/` 开头，endpoint 的 path 被整段丢弃，实得 `GET http://127.0.0.1:61813/openharmony/obs/20261102/knowledge.tar.gz`（94326 字节，`Accept: application/octet-stream`）。
- 无“就近日期回退”：`obsPath` 缺失/空即 `该日期没有成功构建`；HTTP 仅对 `408/429/5xx` 重试，默认 `timeout=90s, attempts=3, retry_delay=2s`。`--date` 格式校验前置（`2026-11-02`、`20261332` 均在发请求前 exit=1）。
- 对比 `INTERNAL_CI`：那条路径才是单次 `GET {endpoint}/{date}`，日期直接进路径。
- 夹具对任意日期都回显 `obsPath`（实测 20261101/20261103 也 200），所以“当天确有成功构建”只在真实 CI 侧成立，客户端不做日期二次过滤。

**产出文件**
- `answer.md`：命令、输出片段与完整语义说明。
- `probe_request.py`、`probe_download.py`：可复现请求的只读探针（monkeypatch `urlopen` 打印请求，不修改 skill）。
```

### Agent 写入的 answer.md

```markdown
# OPENHARMONY_CI + date=20261102：安装结果与实际请求语义

运行时根目录（`OSKM_RUNTIME_ROOT`）安装前为空，现已装齐 `knowledge.db` + `oskm-cli.pyz` +
`interface/sdk-js` + `interface/sdk_c`，`doctor` 全绿，CLI 可查询。

## 1. 执行过的关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"

$PY "$SKILL_DIR/bootstrap.py" doctor                                             # 装前体检
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102
$PY "$SKILL_DIR/bootstrap.py" doctor                                             # 装后体检
$PY "$SKILL_DIR/bootstrap.py" cli-path
$PY "$SKILL_DIR/bootstrap.py" validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask get_scan_info
$PY "$SKILL_DIR/bootstrap.py" refresh --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102

# 只读探针：打印安装器真实发出的 HTTP 请求（不改动 skill / fixtures）
$PY probe_request.py 20261102        # 只发列表 POST，打印请求体与响应
$PY probe_download.py 20261102       # 走完整 POST → GET 两段，落到临时目录
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" --date 2026-11-02
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261332
```

## 2. 关键输出片段

装前 `doctor`（exit=1）：

```
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
CLI: FAIL: 找不到可用的 oskm-cli 产物。… 已尝试：$OSKM_CLI 未设置 / 源码树 / <root>/oskm-cli.pyz 不存在
错误: 运行时依赖检查未通过。
```

`install --date 20261102`（exit=0）：

```
==> 下载 OPENHARMONY_CI 运行时: 20261102
==> 运行时安装完成: …/e02-openharmony-exact-date/runtime
```

装后 `doctor`（exit=0）：

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-d
… [输出截断，完整内容见工作区] …
ime.json`（`version: 3`）。
- `refresh --date 20261102` 命中同一日期 → 直接 no-op，不联网；换一个日期才会重新下载安装。
- `install`/`refresh` 缺省 `--date` 时取系统当天（`state.today()`），本次显式指定为 20261102。

## 4. 落盘结果

```
runtime/knowledge.db
runtime/oskm-cli.pyz
runtime/interface/sdk-js/…
runtime/interface/sdk_c/…
runtime/.oskm-runtime.json
```

`.oskm-runtime.json` 关键字段：

```json
{"version": 3, "source": "OPENHARMONY_CI", "date": "20261102",
 "db":  {"date": "20261102", "path": "knowledge.db",
         "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44"},
 "sdk": {"date": "20261102", "sdk-js": {"path": "interface/sdk-js"}, "sdk_c": {"path": "interface/sdk_c"}},
 "cli": {"path": "oskm-cli.pyz",
         "sha256": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5"}}
```

## 5. 夹具说明

本地夹具服务对任意日期都回显对应的 `obsPath`（实测 20261101 / 20261103 同样返回 200），
所以"该日期确有成功构建"这一约束在真实 CI 侧才成立；客户端只负责把日期收敛成当天窗口并取首条。
DB 为合成快照（`product=synthetic`，各采集器 `record_count=1`），可打开、schema 校验通过，
适合验证安装链路，不代表真实产品证据规模。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**安装结果**
- `bootstrap.py install --date 20261102` 成功（exit=0），`$OSKM_RUNTIME_ROOT` 装齐 `knowledge.db`、`oskm-cli.pyz`(1.0.0)、`interface/sdk-js`、`interface/sdk_c`。
- 装后 `doctor` 全绿：`Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓`；`validate-db` 返回 `{"ok": true}`；`ask get_scan_info` 可查（`product=synthetic`, `status=complete`）。
- `refresh --date 20261102` 为 no-op（“运行时已是最新”），`~/.oskm` 未被创建，skill 与夹具目录未改动。

**实际请求语义**（用只读探针 `probe_request.py` / `probe_download.py` 实测，非凭记忆）
- 日期不进 URL，而是变成对列表 API 的一次 `POST`：`startTime="2026110200000000"`、`endTime="20261102235959"`（同一天窗口，两字段位数不对称，原样发送），固定 `component=dayu600_7885_ai`、`buildStatus=success`、`type=1`、`branch=master`、`pageNum=1/pageSize=10`、`sortType/sortField` 留空。
- 响应只取 `data.list.dataList[0].obsPath` → `urljoin(endpoint, obsPath)`。因 `obsPath` 以 `/` 开头，endpoint 的 path 被整段丢弃，实得 `GET http://127.0.0.1:61813/openharmony/obs/20261102/knowledge.tar.gz`（94326 字节，`Accept: application/octet-stream`）。
- 无“就近日期回退”：`obsPath` 缺失/空即 `该日期没有成功构建`；HTTP 仅对 `408/429/5xx` 重试，默认 `timeout=90s, attempts=3, retry_delay=2s`。`--date` 格式校验前置（`2026-11-02`、`20261332` 均在发请求前 exit=1）。
- 对比 `INTERNAL_CI`：那条路径才是单次 `GET {endpoint}/{date}`，日期直接进路径。
- 夹具对任意日期都回显 `obsPath`（实测 20261101/20261103 也 200），所以“当天确有成功构建”只在真实 CI 侧成立，客户端不做日期二次过滤。

**产出文件**
- `answer.md`：命令、输出片段与完整语义说明。
- `probe_request.py`、`probe_download.py`：可复现请求的只读探针（monkeypatch `urlopen` 打印请求，不修改 skill）。stderr:
2026-11-17T08:18:33.533576Z ERROR codex_skills_extension::host_service: failed to install system skills: io error while remove existing system skills dir: Directory not empty (os error 66)
2026-11-17T08:18:33.542599Z ERROR codex_skills_extension::host_service: failed to install system skills: io error while remove existing system skills dir: Directory not empty (os error 66)
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e02-openharmony-exact-date` · exit=0 · 352.2s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（7 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T16:20:15.900+08:00",
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
    "ts": "2026-11-17T16:20:15.901+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 3,
    "ts": "2026-11-17T16:20:55.216+08:00",
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
    "ts": "2026-11-17T16:21:20.901+08:00",
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
    "seq": 5,
    "ts": "2026-11-17T16:21:20.902+08:00",
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
    "seq": 6,
    "ts": "2026-11-17T16:21:59.298+08:00",
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
    "seq": 7,
    "ts": "2026-11-17T16:21:59.299+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
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
| 1 | 工具的请求只落在"构建列表 POST + obs 归档 GET"两条路径上 | auto | Pass | POST=5 GET=2；[{"method": "POST", "path": "/openharmony/api/daily_build/build/list/component"}, {"method": "GET", "path": "/openharmony/obs/20261102/knowledge.tar.gz"}, {"method": "POST", "path": "/ope
… [输出截断，完整内容见工作区] …
ild/build/list/component"}, {"method": "GET", "path": "/openharmony/obs/20261102/knowledge.tar.gz"}] |
| 2 | component 固定为 dayu600_7885_ai（不需要用户传） | auto | Pass | component=dayu600_7885_ai |
| 3 | 起止时间都来自同一个显式日期 | auto | Pass | startTime=2026110200000000 endTime=20261102235959 |
| 4 | 只取构建成功的记录 | auto | Pass | buildStatus=success |
| 5 | 下载物是 knowledge.tar.gz | auto | Pass | /openharmony/obs/20261102/knowledge.tar.gz |
| 6 | 请求里没有 latest 语义 | auto | Pass | request log 无 latest |
| 7 | 状态文件记录 source=OPENHARMONY_CI 与 date=20261102 | auto | Pass | {"source": "OPENHARMONY_CI", "date": "20261102"} |
| 8 | 四件产物装齐 | auto | Pass | db=True cli=True |
| 9 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
