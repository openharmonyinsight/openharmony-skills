# E3 internal-exact-date（without-skill 臂）

- 开始时间：2026-11-17T16:18:33+08:00
- 结束时间：2026-11-17T16:21:31+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e03-internal-exact-date`
- 夹具服务端：http://127.0.0.1:61810
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e03-internal-exact-date --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：178.0 s
- 事件计数：`{"thread.started": 1, "item.completed": 46, "item:error": 1, "turn.started": 1, "item:reasoning": 14, "item:agent_message": 10, "item.started": 21, "item:command_execution": 42, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：21
- token 用量：`{"input_tokens": 281402, "cached_input_tokens": 259072, "output_tokens": 4884, "reasoning_output_tokens": 1369}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'ls -la && echo "---" && find tool -type f | head -50'
$ /bin/zsh -lc 'cat tool/bootstrap.py 2>/dev/null | head -100'
$ /bin/zsh -lc 'cat tool/oskm_runtime/.env.example; echo "=== bootstrap.py ==="; cat tool/oskm_runtime/bootstrap.py'
$ /bin/zsh -lc 'echo "=== db_download.py ==="; cat tool/oskm_runtime/db_download.py; echo "=== environment.py ==="; cat tool/oskm_runtime/environment.py'
$ /bin/zsh -lc "grep -n \"INTERNAL_CI\\|def download_database\\|internal\" tool/oskm_runtime/db_download.py | head -40"
$ /bin/zsh -lc "sed -n '/_internal/,/"'^def /p'"' tool/oskm_runtime/db_download.py | head -60; echo \"=== download_database ===\"; awk '/"'^def download_database/,0'"' tool/oskm_runtime/db_download.py | head -70"
$ /bin/zsh -lc "sed -n '190,250p' tool/oskm_runtime/db_download.py"
$ /bin/zsh -lc "grep -n \"def install_runtime\\|def _do_install\\|download_runtime_bundle\\|RUNTIME_ROOT_ENV\\|ENDPOINT_ENV\\|SOURCE_ENV\" tool/oskm_runtime/install.py tool/oskm_runtime/environment.py | head -30"
$ /bin/zsh -lc "sed -n '360,460p' tool/oskm_runtime/install.py"
$ /bin/zsh -lc 'cat PROMPT.md; echo "=== env ==="; env | grep -i oskm'
$ /bin/zsh -lc '/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor; echo "EXIT=$?"'
$ /bin/zsh -lc '/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py install --date 20261102 2>&1 | tee /tmp/install-20261102.log; echo "EXIT=${pipestatus[1]}"'
$ /bin/zsh -lc 'ls -la runtime && echo "=== state ===" && cat runtime/.oskm-state.json 2>/dev/null || ls -a runtime'
$ /bin/zsh -lc "curl -sS -o /tmp/probe.tar.gz -w \"HTTP=%{http_code} SIZE=%{size_download} TYPE=%{content_type}\\n\" \"http://127.0.0.1:61810/internal/20261102\"; tar tzf /tmp/probe.tar.gz 2>/dev/null | head"
$ /bin/zsh -lc 'cat runtime/.oskm-runtime.json; echo; echo "=== doctor ==="; /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor 2>&1 | tail -12; echo "EXIT=$?"'
$ /bin/zsh -lc '/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py validate-db runtime/knowledge.db 2>&1 | tail -20; echo "EXIT=${pipestatus[1]}"'
$ /bin/zsh -lc '/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py refresh --date 20261102 2>&1; echo "EXIT=${pipestatus[1]}"'
$ /bin/zsh -lc "cd tool && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
from oskm_runtime.environment import download_config
c = download_config()
print('source  =', c.source)
print('endpoint=', c.endpoint)
print('URL     =', f'{c.endpoint}/20261102')
\""
$ /bin/zsh -lc 'ls -R runtime/interface | head -20; echo "=== CLI version ==="; /opt/homebrew/opt/python@3.12/bin/python3.12 runtime/oskm-cli.pyz --version 2>&1 | head -3'
$ /bin/zsh -lc "sed -n '205,215p' tool/oskm_runtime/db_download.py | cat -n; echo \"=== env endpoint lines ===\"; grep -n \"def _endpoint\" -A 8 tool/oskm_runtime/environment.py"
$ /bin/zsh -lc "cat > answer.md <<'EOF'
# INTERNAL_CI 下载 date=20261102 的运行时

## 直接回答（URL）

INTERNAL_CI 只有**一次 GET**，URL 就是把日期直接拼在 endpoint 后面：

"'```
http://127.0.0.1:61810/internal/20261102
```

规则来自 `tool/oskm_runtime/db_download.py:209`：

```python
if config.source == INTERNAL_CI:
    url = f'"'{config.endpoint}/{date}'
    archive = work_dir / 'knowledge.tar.gz'
"'```

- endpoint 先被 `environment._endpoint()`（`tool/oskm_runtime/environment.py:127`）`strip().rstrip('"'/')"'` 归一化，
  所以 `.../internal` 和 `.../internal/` 都会拼成 `.../internal/20261102`，不会出现双斜杠。
- 与 OPENHARMONY_CI 不同：后者要先 POST 组件查询接口拿 OBS 归档地址再下载；INTERNAL_CI 无 POST、无查询、无重定向，
  URL 完全由 `OSKM_DOWNLOAD_ENDPOINT` + `YYYYMMDD` 决定。
- 响应体一律落盘为 `knowledge.tar.gz`（文件名固定，不取 URL 的 basename），
  里面是 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`。

## 执行过的关键命令

```bash
# 0) 环境（已由夹具设好）
env | grep -i oskm
#   OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
#   OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61810/internal
#   OSKM_RUNTIME_ROOT=.../e03-internal-exact-date/runtime

# 1) 安装前体检：运行时为空
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor      # EXIT=1（未安装）

# 2) 真正下载并安装指定日期
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py install --date 20261102   # EXIT=0

# 3) 独立验证该 URL 确实提供归档
curl -sS -o /tmp/probe.tar.gz -w "HTTP=%{http_code} SIZE=%{size_download} TYPE=%{content_type}'"\\n\" \\
  \"http://127.0.0.1:61810/internal/20261102\"

# 4) 安装后校验
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor            # EXIT=0
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py validate-db runtime/knowledge.db
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py refresh --date 20261102  # 幂等
"'```

## 关键输出片段

`install`：

```
==> 下载 INTERNAL_CI 运行时: 20261102
==> 运行时安装完成: .../e03-internal-exact-date/runtime
```

URL 探测（证明该地址就是归档来源）：

```
HTTP=200 SIZE=94314 TYPE=application/gzip
./
interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
interface/sdk_c/evalmarker.h
knowledge.db
oskm-cli.pyz
```

代码里现算的 URL（与上面 curl 的地址一致）：

```
source  = INTERNAL_CI
endpoint= http://127.0.0.1:61810/internal
URL     = http://127.0.0.1:61810/internal/20261102
```

安装后 `doctor`：

```
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: .../runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
```

`validate-db`：

```
{"path": "runtime/knowledge.db", "ok": true}
```

`refresh --date 20261102`（幂等，未重复下载）：

```
==> 运行时已是最新，无需刷新: .../e03-internal-exact-date/runtime
```

## 落盘结果

`runtime/.oskm-runtime.json`：

```json
{
  "version": 3,
  "source": "INTERNAL_CI",
  "date": "20261102",
  "db":  { "date": "20261102", "path": "knowledge.db",
           "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44" },
  "sdk": { "date": "20261102",
           "sdk-js": { "path": "interface/sdk-js" },
           "sdk_c":  { "path": "interface/sdk_c" } },
  "cli": { "path": "oskm-cli.pyz",
           "sha256": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5" }
}
```

目录内容：`runtime/knowledge.db`(434176 B)、`runtime/oskm-cli.pyz`(84742 B)、
`runtime/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts`、`runtime/interface/sdk_c/evalmarker.h`。

## 备注

- 全程只用任务给定的运行时根目录，没有读写 `~/.oskm`；fixtures 目录未改动。
- 查询不归 `bootstrap.py` 管，装完后直接调 CLI：
  `/opt/homebrew/opt/python@3.12/bin/python3.12 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview`
EOF
wc -l answer.md'
```

### Agent 最终回答

```markdown
**执行结果**
- `install --date 20261102` 已真跑通（EXIT=0）：`==> 下载 INTERNAL_CI 运行时: 20261102` → `==> 运行时安装完成`。
- 安装前 `doctor` EXIT=1（运行时为空），安装后 EXIT=0：`Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`。
- `validate-db runtime/knowledge.db` → `{"path": "runtime/knowledge.db", "ok": true}`；`refresh --date 20261102` 幂等命中“已是最新”。
- 落盘：`runtime/knowledge.db`、`runtime/oskm-cli.pyz`（oskm-cli 1.0.0）、`runtime/interface/sdk-js`、`runtime/interface/sdk_c`，状态见 `runtime/.oskm-runtime.json:1`。

**URL 说明**
- 实际请求：`http://127.0.0.1:61810/internal/20261102`，`curl` 验证 `HTTP=200 SIZE=94314 TYPE=application/gzip`。
- 拼接规则在 `tool/oskm_runtime/db_download.py:210`：INTERNAL_CI 就是 `f'{config.endpoint}/{date}'`，单次 GET，无 POST 查询、无 OBS 二段跳转（那是 OPENHARMONY_CI 的路径）。
- endpoint 先经 `tool/oskm_runtime/environment.py:127` 的 `strip().rstrip('/')` 归一化，因此结尾带不带 `/` 都拼成同一个地址，不会出双斜杠。
- 响应体固定存为 `knowledge.tar.gz`（不取 URL basename），归档内含 DB + CLI + 两套 SDK，由 `install` 一次装齐。

结论已写入 `answer.md:1`。全程未触碰 `~/.oskm`，也未修改 fixtures。要不要我顺手用装好的 CLI 跑一条查询（如 `arch overview`）验证数据库内容？
```

### Agent 写入的 answer.md

```markdown
# INTERNAL_CI 下载 date=20261102 的运行时

## 直接回答（URL）

INTERNAL_CI 只有**一次 GET**，URL 就是把日期直接拼在 endpoint 后面：

```
http://127.0.0.1:61810/internal/20261102
```

规则来自 `tool/oskm_runtime/db_download.py:209`：

```python
if config.source == INTERNAL_CI:
    url = f'{config.endpoint}/{date}'
    archive = work_dir / 'knowledge.tar.gz'
```

- endpoint 先被 `environment._endpoint()`（`tool/oskm_runtime/environment.py:127`）`strip().rstrip('/')` 归一化，
  所以 `.../internal` 和 `.../internal/` 都会拼成 `.../internal/20261102`，不会出现双斜杠。
- 与 OPENHARMONY_CI 不同：后者要先 POST 组件查询接口拿 OBS 归档地址再下载；INTERNAL_CI 无 POST、无查询、无重定向，
  URL 完全由 `OSKM_DOWNLOAD_ENDPOINT` + `YYYYMMDD` 决定。
- 响应体一律落盘为 `knowledge.tar.gz`（文件名固定，不取 URL 的 basename），
  里面是 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`。

## 执行过的关键命令

```bash
# 0) 环境（已由夹具设好）
env | grep -i oskm
#   OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
#   OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61810/internal
#   OSKM_RUNTIME_ROOT=.../e03-internal-exact-date/runtime

# 1) 安装前体检：运行时为空
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor      # EXIT=1（未安装）

# 2) 真正下载并安装指定日期
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py install --date 20261102   # EXIT=0

# 3) 独立验证该 URL 确实提供归档
curl -sS -o /tmp/probe.tar.gz -w "HTTP=%{http_code} SIZE=%{size_download} TYPE=%{content_type}\n" \
  "http://127.0.0.1:61810/internal/20261102"

# 4) 安装后校验
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor            # EXIT=0
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py validate-db runtime/knowledge.db
/opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py refresh --date 20261102  # 幂等
```

## 关键输出片段

`install`：

```
==> 下载 INTERNAL_CI 运行时: 20261102
==> 运行时安装完成: .../e03-internal-exact-date/runtime
```

URL 探测（证明该地址就是归档来源）：

```
HTTP=200 SIZE=94314 TYPE=application/gzip
./
interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
interface/sdk_c/evalmarker.h
knowledge.db
oskm-cli.pyz
```

代码里现算的 URL（与上面 curl 的地址一致）：

```
source  = INTERNAL_CI
endpoint= http://127.0.0.1:61810/internal
URL     = http://127.0.0.1:61810/internal/20261102
```

安装后 `doctor`：

```
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: .../runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
```

`validate-db`：

```
{"path": "runtime/knowledge.db", "ok": true}
```

`refresh --date 20261102`（幂等，未重复下载）：

```
==> 运行时已是最新，无需刷新: .../e03-internal-exact-date/runtime
```

## 落盘结果

`runtime/.oskm-runtime.json`：

```json
{
  "version": 3,
  "source": "INTERNAL_CI",
  "date": "20261102",
  "db":  { "date": "20261102", "path": "knowledge.db",
           "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44" },
  "sdk": { "date": "20261102",
           "sdk-js": { "path": "interface/sdk-js" },
           "sdk_c":  { "path": "interface/sdk_c" } },
  "cli": { "path": "oskm-cli.pyz",
           "sha256": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5" }
}
```

目录内容：`runtime/knowledge.db`(434176 B)、`runtime/oskm-cli.pyz`(84742 B)、
`runtime/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts`、`runtime/interface/sdk_c/evalmarker.h`。

## 备注

- 全程只用任务给定的运行时根目录，没有读写 `~/.oskm`；fixtures 目录未改动。
- 查询不归 `bootstrap.py` 管，装完后直接调 CLI：
  `/opt/homebrew/opt/python@3.12/bin/python3.12 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview`
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**执行结果**
- `install --date 20261102` 已真跑通（EXIT=0）：`==> 下载 INTERNAL_CI 运行时: 20261102` → `==> 运行时安装完成`。
- 安装前 `doctor` EXIT=1（运行时为空），安装后 EXIT=0：`Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`。
- `validate-db runtime/knowledge.db` → `{"path": "runtime/knowledge.db", "ok": true}`；`refresh --date 20261102` 幂等命中“已是最新”。
- 落盘：`runtime/knowledge.db`、`runtime/oskm-cli.pyz`（oskm-cli 1.0.0）、`runtime/interface/sdk-js`、`runtime/interface/sdk_c`，状态见 `runtime/.oskm-runtime.json:1`。

**URL 说明**
- 实际请求：`http://127.0.0.1:61810/internal/20261102`，`curl` 验证 `HTTP=200 SIZE=94314 TYPE=application/gzip`。
- 拼接规则在 `tool/oskm_runtime/db_download.py:210`：INTERNAL_CI 就是 `f'{config.endpoint}/{date}'`，单次 GET，无 POST 查询、无 OBS 二段跳转（那是 OPENHARMONY_CI 的路径）。
- endpoint 先经 `tool/oskm_runtime/environment.py:127` 的 `strip().rstrip('/')` 归一化，因此结尾带不带 `/` 都拼成同一个地址，不会出双斜杠。
- 响应体固定存为 `knowledge.tar.gz`（不取 URL basename），归档内含 DB + CLI + 两套 SDK，由 `install` 一次装齐。

结论已写入 `answer.md:1`。全程未触碰 `~/.oskm`，也未修改 fixtures。要不要我顺手用装好的 CLI 跑一条查询（如 `arch overview`）验证数据库内容？stderr:
2026-11-17T08:18:33.532732Z ERROR codex_skills_extension::host_service: failed to install system skills: io error while remove existing system skills dir: Directory not empty (os error 66)
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e03-internal-exact-date` · exit=0 · 178.0s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T16:19:42.634+08:00",
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
    "ts": "2026-11-17T16:19:54.727+08:00",
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
