# E3 internal-exact-date（without-skill 臂）

- 开始时间：2026-11-17T15:33:43+08:00
- 结束时间：2026-11-17T15:37:03+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e03-internal-exact-date`
- 夹具服务端：http://127.0.0.1:61143
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

使用 INTERNAL_CI 下载 date=20261102 的运行时，OSKM_DOWNLOAD_ENDPOINT 已配置为测试服务。请执行并说明 URL。

## 期望结果（来自 evals.json）

请求 $OSKM_DOWNLOAD_ENDPOINT/20261102，响应文件为 knowledge.tar.gz；指定日期不会退化成 latest 或系统当天。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| $OSKM_DOWNLOAD_ENDPOINT/$date | `contains` |
| knowledge.tar.gz | `contains` |
| 指定日期不会退化成 latest 或系统当天 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e03-internal-exact-date --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：200.2 s
- 事件计数：`{"thread.started": 1, "item.completed": 49, "item:error": 1, "turn.started": 1, "item:reasoning": 15, "item:agent_message": 12, "item.started": 21, "item:command_execution": 42, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：21
- token 用量：`{"input_tokens": 320495, "cached_input_tokens": 287872, "output_tokens": 5322, "reasoning_output_tokens": 1584}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'ls -la; echo "---"; find tool -type f | head -50; echo "---"; ls -la runtime 2>/dev/null; echo "---"; ls -la fixtures 2>/dev/null'
$ /bin/zsh -lc 'env | grep -i oskm'
$ /bin/zsh -lc 'cd tool && wc -l bootstrap.py oskm_runtime/*.py && echo "=== bootstrap.py ===" && cat bootstrap.py'
$ /bin/zsh -lc 'cd tool && echo "=== __main__.py ===" && cat oskm_runtime/__main__.py && echo "=== .env.example ===" && cat oskm_runtime/.env.example'
$ /bin/zsh -lc 'cd tool && cat oskm_runtime/db_download.py'
$ /bin/zsh -lc 'cd tool && cat oskm_runtime/environment.py'
$ /bin/zsh -lc "cd tool && sed -n '150,290p' oskm_runtime/db_download.py"
$ /bin/zsh -lc 'cd tool && cat oskm_runtime/bootstrap.py'
$ /bin/zsh -lc "cd tool && sed -n '135,200p' oskm_runtime/bootstrap.py"
$ /bin/zsh -lc '/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor; echo "exit=$?"'
$ /bin/zsh -lc "cd tool && grep -n \"print\\|def \\|download_runtime_bundle\\|download_database\" oskm_runtime/install.py | head -60"
$ /bin/zsh -lc '/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py install --date 20261102; echo "exit=$?"'
$ /bin/zsh -lc 'cd "$OSKM_RUNTIME_ROOT" && ls -la && echo "--- tree ---" && find . -maxdepth 3 | sort | head -40 && echo "--- state ---" && for f in *.json .*.json; do [ -f "$f" ] && echo "== $f" && cat "$f"; done 2>/dev/null'
$ /bin/zsh -lc "cd tool && grep -n \"def \\|date\\|STATE\" oskm_runtime/state.py | head -40"
$ /bin/zsh -lc 'cat "$OSKM_RUNTIME_ROOT/.oskm-runtime.json"; echo; echo "--- sdk ---"; find "$OSKM_RUNTIME_ROOT/interface" -maxdepth 2 | sort'
$ /bin/zsh -lc 'curl -sS -D - -o /dev/null "http://127.0.0.1:61143/internal/20261102" | head -20'
$ /bin/zsh -lc '/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor; echo "exit=$?"; echo "=== refresh (idempotent) ==="; /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py refresh --date 20261102; echo "exit=$?"'
$ /bin/zsh -lc 'cat "$OSKM_RUNTIME_ROOT/interface/sdk_c/evalmarker.h"; echo "=== cli ==="; /opt/homebrew/opt/python@3.12/bin/python3.12 "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --version 2>&1 | head -5; /opt/homebrew/opt/python@3.12/bin/python3.12 "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview 2>&1 | head -20'
$ /bin/zsh -lc "cd tool && grep -n \"url = f'{config.endpoint}/{date}'\\|archive = work_dir / 'knowledge.tar.gz'\\|def _download_archive\\|rstrip('/')\" oskm_runtime/db_download.py oskm_runtime/environment.py"
$ /bin/zsh -lc "cat > answer.md <<'EOF'
# INTERNAL_CI 下载 date=20261102 运行时

## 直接回答

- 使用的 URL："'`http://127.0.0.1:61143/internal/20261102`
- 规则：`INTERNAL_CI` 走 **GET `<OSKM_DOWNLOAD_ENDPOINT>/<YYYYMMDD>`**，响应体就是运行时归档，落盘名固定为 `knowledge.tar.gz`。端点末尾的 `/` 会先被剥掉，再直接拼接日期段——没有查询参数、没有 POST body、不做二次跳转取 OBS 地址。
- 拼接位置：`tool/oskm_runtime/db_download.py:210`（`url = f'"'{config.endpoint}/{date}'"'`），端点归一化在 `tool/oskm_runtime/environment.py:127`（`.rstrip('"'/')"'`）。
- 对比：`OPENHARMONY_CI` 才是 POST 到端点（component 固定 `dayu600_7885_ai`，用 `startTime`/`endTime` 圈住当天），再从响应 `data.list.dataList[0].obsPath` 里 `urljoin` 出真正的归档地址。本次用的是 `INTERNAL_CI`，所以只有那一层 GET。
- 执行结果：运行时已完整装到 `$OSKM_RUNTIME_ROOT`（date=20261102），包含 `knowledge.db`、`oskm-cli.pyz`、`interface/sdk-js`、`interface/sdk_c`。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12

# 1) 装前自检：确认 source/endpoint/runtime-root 解析正确（此时 CLI 与 DB 都还没装）
$PY tool/bootstrap.py doctor

# 2) 下载并安装指定日期的运行时（--runtime-root 由 $OSKM_RUNTIME_ROOT 提供，无需重复写）
$PY tool/bootstrap.py install --date 20261102

# 3) 复核 + 幂等性验证
$PY tool/bootstrap.py doctor
$PY tool/bootstrap.py refresh --date 20261102

# 4) 用装好的 CLI 验证运行时可用
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --version
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview

# 5) 直接确认 URL（只读请求，不落盘）
curl -sS -D - -o /dev/null "http://127.0.0.1:61143/internal/20261102"
```

说明：`install` 会先从 cwd 向上探测 OpenHarmony 源码根，找到本地构建就优先用本地；本工作区没有源码根，因此回退到下载分支（输出里的 `==> 下载 INTERNAL_CI 运行时`）。

## 关键输出

`doctor`（装前，节选）：

```
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。…… 可行做法：· 跑 `bootstrap.py install` 从运行时归档里装（含 CLI）
Runtime root: …/e03-internal-exact-date/runtime
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。   (exit=1)
```

`install --date 20261102`：

```
==> 下载 INTERNAL_CI 运行时: 20261102
==> 运行时安装完成: …/e03-internal-exact-date/runtime
exit=0
```

`doctor`（装后，节选）：

```
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
exit=0
```

`refresh --date 20261102`（幂等，未重复下载）：

```
==> 运行时已是最新，无需刷新: …/e03-internal-exact-date/runtime
```

URL 直接探测：

```
HTTP/1.1 200 OK
Server: oskm-eval-fixture/1.0 Python/3.12.16
Content-Type: application/gzip
Content-Length: 93314
```

CLI 查询验证：

```
oskm-cli 1.0.0
{ "product": "synthetic", "scan_id": 1, "subsystems": 2,
  "counts": { "repos": 1, "components": 2, "install_modules": 3, ... } }
```

## 落盘结果

`$OSKM_RUNTIME_ROOT`（`…/e03-internal-exact-date/runtime`）：

```
.oskm-runtime.json     # 状态：version 3 / source INTERNAL_CI / date 20261102
knowledge.db           # 434176 B, sha256 f561e39f…1b44
oskm-cli.pyz           #  83741 B, sha256 ad760c16…5eb49e
interface/sdk-js/api
interface/sdk_c/evalmarker.h
```

`.oskm-runtime.json` 里 `db.date`、`sdk.date` 均为 `20261102`，与请求的日期一致。

## 备注

- 未访问、未修改 `~/.oskm`；运行时根目录全程由 `$OSKM_RUNTIME_ROOT` 解析（`--runtime-root` 未显式传入也等价）。
- 未修改 `fixtures`，未改动 `tool/` 下任何代码。
- 归档内的 CLI 与 DB 一起发布，没有单独的 CLI 下载端点，所以一条 `install` 就装齐了四件套。
EOF
echo "written:"; wc -l answer.md'
$ /bin/zsh -lc 'git status --porcelain 2>/dev/null | head; echo "---"; ls -la; echo "--- runtime sha check ---"; shasum -a 256 "$OSKM_RUNTIME_ROOT/knowledge.db" | cut -c1-16'
```

### Agent 最终回答

```markdown
已跑通并验证，结论写进 `answer.md`。

**URL**
- 实际请求：`http://127.0.0.1:61143/internal/20261102`（GET，无查询参数、无 POST body）。
- 规则：`INTERNAL_CI` = `GET <OSKM_DOWNLOAD_ENDPOINT>/<YYYYMMDD>`，端点末尾 `/` 先剥掉再拼日期；响应体即运行时归档，落盘名固定 `knowledge.tar.gz`。拼接在 `tool/oskm_runtime/db_download.py:210`，端点归一化在 `tool/oskm_runtime/environment.py:127`。
- 对比：`OPENHARMONY_CI` 才需要 POST（component `dayu600_7885_ai` + 当天时间窗）再从 `obsPath` 二次取址；本次来源是 `INTERNAL_CI`，只有这一层 GET。

**执行**
- `python3.12 tool/bootstrap.py doctor` → 装前 `exit=1`，`source=INTERNAL_CI`、`endpoint=已配置`、`Runtime state: 未安装`，runtime root 正确解析到工作区 `runtime/`。
- `python3.12 tool/bootstrap.py install --date 20261102` → `==> 下载 INTERNAL_CI 运行时: 20261102` / `==> 运行时安装完成`，`exit=0`。
- `python3.12 tool/bootstrap.py refresh --date 20261102` → `运行时已是最新，无需刷新`（幂等）。
- `curl -sS -D - -o /dev/null http://127.0.0.1:61143/internal/20261102` → `200 OK`、`application/gzip`、`93314` 字节，独立确认 URL。

**结果**
- `$OSKM_RUNTIME_ROOT` 下装齐四件套：`knowledge.db`（sha256 `f561e39f…`）、`oskm-cli.pyz`、`interface/sdk-js/api`、`interface/sdk_c/evalmarker.h`，外加 `.oskm-runtime.json`（`version 3, source INTERNAL_CI, date 20261102`，`db.date`/`sdk.date` 都是 `20261102`）。
- 装后 `doctor` 全绿：`oskm_runtime/oskm_cli/oskm_schema (OK)`、`db=✓, sdk=✓, cli=✓`；`oskm-cli 1.0.0 arch overview` 正常返回 `scan_id 1, subsystems 2`。
- 未碰 `~/.oskm`，未改 `tool/` 与夹具。

需要我顺手跑一次 `bootstrap.py validate-db` 做完整 schema 契约校验吗？
```

### Agent 写入的 answer.md

```markdown
# INTERNAL_CI 下载 date=20261102 运行时

## 直接回答

- 使用的 URL：`http://127.0.0.1:61143/internal/20261102`
- 规则：`INTERNAL_CI` 走 **GET `<OSKM_DOWNLOAD_ENDPOINT>/<YYYYMMDD>`**，响应体就是运行时归档，落盘名固定为 `knowledge.tar.gz`。端点末尾的 `/` 会先被剥掉，再直接拼接日期段——没有查询参数、没有 POST body、不做二次跳转取 OBS 地址。
- 拼接位置：`tool/oskm_runtime/db_download.py:210`（`url = f'{config.endpoint}/{date}'`），端点归一化在 `tool/oskm_runtime/environment.py:127`（`.rstrip('/')`）。
- 对比：`OPENHARMONY_CI` 才是 POST 到端点（component 固定 `dayu600_7885_ai`，用 `startTime`/`endTime` 圈住当天），再从响应 `data.list.dataList[0].obsPath` 里 `urljoin` 出真正的归档地址。本次用的是 `INTERNAL_CI`，所以只有那一层 GET。
- 执行结果：运行时已完整装到 `$OSKM_RUNTIME_ROOT`（date=20261102），包含 `knowledge.db`、`oskm-cli.pyz`、`interface/sdk-js`、`interface/sdk_c`。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12

# 1) 装前自检：确认 source/endpoint/runtime-root 解析正确（此时 CLI 与 DB 都还没装）
$PY tool/bootstrap.py doctor

# 2) 下载并安装指定日期的运行时（--runtime-root 由 $OSKM_RUNTIME_ROOT 提供，无需重复写）
$PY tool/bootstrap.py install --date 20261102

# 3) 复核 + 幂等性验证
$PY tool/bootstrap.py doctor
$PY tool/bootstrap.py refresh --date 20261102

# 4) 用装好的 CLI 验证运行时可用
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --version
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview

# 5) 直接确认 URL（只读请求，不落盘）
curl -sS -D - -o /dev/null "http://127.0.0.1:61143/internal/20261102"
```

说明：`install` 会先从 cwd 向上探测 OpenHarmony 源码根，找到本地构建就优先用本地；本工作区没有源码根，因此回退到下载分支（输出里的 `==> 下载 INTERNAL_CI 运行时`）。

## 关键输出

`doctor`（装前，节选）：

```
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。…… 可行做法：· 跑 `bootstrap.py install` 从运行时归档里装（含 CLI）
Runtime root: …/e03-internal-exact-date/runtime
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。   (exit=1)
```

`install --date 20261102`：

```
==> 下载 INTERNAL_CI 运行时: 20261102
==> 运行时安装完成: …/e03-internal-exact-date/runtime
exit=0
```

`doctor`（装后，节选）：

```
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
exit=0
```

`refresh --date 20261102`（幂等，未重复下载）：

```
==> 运行时已是最新，无需刷新: …/e03-internal-exact-date/runtime
```

URL 直接探测：

```
HTTP/1.1 200 OK
Server: oskm-eval-fixture/1.0 Python/3.12.16
Content-Type: application/gzip
Content-Length: 93314
```

CLI 查询验证：

```
oskm-cli 1.0.0
{ "product": "synthetic", "scan_id": 1, "subsystems": 2,
  "counts": { "repos": 1, "components": 2, "install_modules": 3, ... } }
```

## 落盘结果

`$OSKM_RUNTIME_ROOT`（`…/e03-internal-exact-date/runtime`）：

```
.oskm-runtime.json     # 状态：version 3 / source INTERNAL_CI / date 20261102
knowledge.db           # 434176 B, sha256 f561e39f…1b44
oskm-cli.pyz           #  83741 B, sha256 ad760c16…5eb49e
interface/sdk-js/api
interface/sdk_c/evalmarker.h
```

`.oskm-runtime.json` 里 `db.date`、`sdk.date` 均为 `20261102`，与请求的日期一致。

## 备注

- 未访问、未修改 `~/.oskm`；运行时根目录全程由 `$OSKM_RUNTIME_ROOT` 解析（`--runtime-root` 未显式传入也等价）。
- 未修改 `fixtures`，未改动 `tool/` 下任何代码。
- 归档内的 CLI 与 DB 一起发布，没有单独的 CLI 下载端点，所以一条 `install` 就装齐了四件套。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
已跑通并验证，结论写进 `answer.md`。

**URL**
- 实际请求：`http://127.0.0.1:61143/internal/20261102`（GET，无查询参数、无 POST body）。
- 规则：`INTERNAL_CI` = `GET <OSKM_DOWNLOAD_ENDPOINT>/<YYYYMMDD>`，端点末尾 `/` 先剥掉再拼日期；响应体即运行时归档，落盘名固定 `knowledge.tar.gz`。拼接在 `tool/oskm_runtime/db_download.py:210`，端点归一化在 `tool/oskm_runtime/environment.py:127`。
- 对比：`OPENHARMONY_CI` 才需要 POST（component `dayu600_7885_ai` + 当天时间窗）再从 `obsPath` 二次取址；本次来源是 `INTERNAL_CI`，只有这一层 GET。

**执行**
- `python3.12 tool/bootstrap.py doctor` → 装前 `exit=1`，`source=INTERNAL_CI`、`endpoint=已配置`、`Runtime state: 未安装`，runtime root 正确解析到工作区 `runtime/`。
- `python3.12 tool/bootstrap.py install --date 20261102` → `==> 下载 INTERNAL_CI 运行时: 20261102` / `==> 运行时安装完成`，`exit=0`。
- `python3.12 tool/bootstrap.py refresh --date 20261102` → `运行时已是最新，无需刷新`（幂等）。
- `curl -sS -D - -o /dev/null http://127.0.0.1:61143/internal/20261102` → `200 OK`、`application/gzip`、`93314` 字节，独立确认 URL。

**结果**
- `$OSKM_RUNTIME_ROOT` 下装齐四件套：`knowledge.db`（sha256 `f561e39f…`）、`oskm-cli.pyz`、`interface/sdk-js/api`、`interface/sdk_c/evalmarker.h`，外加 `.oskm-runtime.json`（`version 3, source INTERNAL_CI, date 20261102`，`db.date`/`sdk.date` 都是 `20261102`）。
- 装后 `doctor` 全绿：`oskm_runtime/oskm_cli/oskm_schema (OK)`、`db=✓, sdk=✓, cli=✓`；`oskm-cli 1.0.0 arch overview` 正常返回 `scan_id 1, subsystems 2`。
- 未碰 `~/.oskm`，未改 `tool/` 与夹具。

需要我顺手跑一次 `bootstrap.py validate-db` 做完整 schema 契约校验吗？
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e03-internal-exact-date` · exit=0 · 200.2s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T15:34:59.156+08:00",
    "method": "GET",
    "path": "/internal/20261102",
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
    "ts": "2026-11-17T15:35:19.595+08:00",
    "method": "GET",
    "path": "/internal/20261102",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  }
]
```

## 断言结果

自动断言 6/6 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 工具的所有请求都是 GET $OSKM_DOWNLOAD_ENDPOINT/$date | auto | Pass | 请求数=1；[{"method": "GET", "path": "/internal/20261102"}] |
| 2 | URL 是 $OSKM_DOWNLOAD_ENDPOINT/$date | auto | Pass | /internal/20261102 |
| 3 | 没有退化成 latest 或系统当天 | auto | Pass | 当天是 20261117，工具实际请求 ['/internal/20261102'] |
| 4 | 状态文件记录 date=20261102 | auto | Pass | date=20261102 |
| 5 | 归档按 knowledge.tar.gz 落地并装齐四件产物 | auto | Pass | runtime=['.oskm-runtime.json', 'interface', 'knowledge.db', 'oskm-cli.pyz'] |
| 6 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
