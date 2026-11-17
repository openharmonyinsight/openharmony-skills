# E2 openharmony-exact-date（with-skill 臂）

- 开始时间：2026-11-17T15:33:43+08:00
- 结束时间：2026-11-17T15:42:10+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date`
- 夹具服务端：http://127.0.0.1:61144
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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：507.6 s
- 事件计数：`{"thread.started": 1, "item.completed": 66, "item:error": 1, "turn.started": 1, "item:reasoning": 23, "item:agent_message": 17, "item.started": 26, "item:command_execution": 51, "turn.completed": 1}`
- 读到 skill 文档：是（15 处）
- 执行的命令数：26
- token 用量：`{"input_tokens": 638180, "cached_input_tokens": 590464, "output_tokens": 16756, "reasoning_output_tokens": 7588}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md"'
$ /bin/zsh -lc 'ls -la "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/" && ls -la'
$ /bin/zsh -lc "cd \"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query\" && sed -n '95,140p' SKILL.md && echo \"=== bootstrap.py ===\" && cat bootstrap.py && echo \"=== runtime tree ===\" && ls -R oskm_runtime | head -60"
$ /bin/zsh -lc 'cat "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date/PROMPT.md"; ls "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/references"'
$ /bin/zsh -lc "cd \"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query\" && grep -n -i -A6 -B2 \"OPENHARMONY_CI\\|date\\|daily_build\\|component\" references/usage.md | head -150"
$ /bin/zsh -lc 'cd "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query" && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py install --help'
$ /bin/zsh -lc 'cd "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date" && echo "SOURCE=$OSKM_DOWNLOAD_SOURCE" && echo "ENDPOINT=$OSKM_DOWNLOAD_ENDPOINT" && echo "RUNTIME_ROOT=$OSKM_RUNTIME_ROOT" && env | grep -i oskm'
$ /bin/zsh -lc 'cd "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query" && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py doctor --runtime-root "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date/runtime"; echo "exit=$?"'
$ /bin/zsh -lc 'cd "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date" && SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" install --source OPENHARMONY_CI --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102 2>&1 | tee /tmp/oskm-install.log; echo "exit=${PIPESTATUS[0]:-$?}"'
$ /bin/zsh -lc 'cd "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date" && ls -la runtime && echo "=== state ===" && cat runtime/.oskm-runtime.json && echo "=== cli-path ===" && SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" cli-path --runtime-root "$OSKM_RUNTIME_ROOT"'
$ /bin/zsh -lc 'ls -la "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/" && find "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg" -maxdepth 3 -iname "*fixture*" -not -path "*/runtime/*" 2>/dev/null | head -20'
$ /bin/zsh -lc 'ls -laR "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures" | head -60'
$ /bin/zsh -lc "cd \"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/oskm_runtime\" && wc -l *.py && grep -n \"startTime\\|endTime\\|component\\|obsPath\\|dataList\\|buildStatus\\|urlopen\\|Request(\\|method\\|json.dumps\\|date\" db_download.py | head -60"
$ /bin/zsh -lc "cd \"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/oskm_runtime\" && sed -n '30,55p;85,135p' db_download.py && echo \"-----138-200-----\" && sed -n '136,200p' db_download.py"
$ /bin/zsh -lc "cd \"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/oskm_runtime\" && grep -n \"OPENHARMONY_COMPONENT\\|DOWNLOAD_SOURCES\\|OPENHARMONY_CI =\\|INTERNAL_CI =\\|SOURCE_ENV\\|ENDPOINT_ENV\" environment.py && echo \"-----200-235-----\" && sed -n '198,235p' db_download.py"
$ /bin/zsh -lc "mkdir -p \"/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date/probe\" && cat > \"/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date/probe/logproxy.py\" <<'PY'
\"\"\"Read-only logging proxy: records what bootstrap.py actually sends, then forwards to the fixture.\"\"\"
import json, sys, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = \"http://127.0.0.1:61144\"
LOG = sys.argv[2] if len(sys.argv) > 2 else \"requests.jsonl\"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 61555


class Handler(BaseHTTPRequestHandler):
    protocol_version = \"HTTP/1.1\"

    def _handle(self, method):
        length = int(self.headers.get(\"Content-Length\") or 0)
        body = self.rfile.read(length) if length else b\"\"
        url = UPSTREAM + self.path
        fwd_headers = {k: v for k, v in self.headers.items()
                       if k.lower() not in (\"host\", \"content-length\")}
        req = urllib.request.Request(url, data=body or None,
                                     headers=fwd_headers, method=method)
        record = {\"method\": method, \"path\": self.path, \"url\": url,
                  \"request_headers\": dict(self.headers.items()),
                  \"request_body\": body.decode(\"utf-8\", \"replace\") if body else \"\"}
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = resp.read()
                record[\"status\"] = resp.status
                record[\"response_headers\"] = dict(resp.headers.items())
                ctype = resp.headers.get(\"Content-Type\", \"\")
                record[\"response_body\"] = (payload.decode(\"utf-8\", \"replace\")[:4000]
                                           if \"json\" in ctype else
                                           f\"<{len(payload)} bytes binary>\")
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in (\"transfer-encoding\", \"connection\"):
                        self.send_header(k, v)
                self.send_header(\"Content-Length\", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
        except urllib.error.HTTPError as exc:
            payload = exc.read()
            record[\"status\"] = exc.code
            record[\"response_body\"] = payload.decode(\"utf-8\", \"replace\")[:4000]
            self.send_response(exc.code)
            self.send_header(\"Content-Length\", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        with open(LOG, \"a\", encoding=\"utf-8\") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + \"\\n\")

    def do_POST(self):
        self._handle(\"POST\")

    def do_GET(self):
        self._handle(\"GET\")

    def log_message(self, *args):
        pass


ThreadingHTTPServer((\"127.0.0.1\", PORT), Handler).serve_forever()
PY
echo written"
$ /bin/zsh -lc "cd \"/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date/probe\" && nohup /opt/homebrew/opt/python@3.12/bin/python3.12 logproxy.py 61555 requests.jsonl > proxy.log 2>&1 & sleep 1.5; curl -s -o /dev/null -w \"proxy_probe_status=%{http_code}\\n\" http://127.0.0.1:61555/healthz"
$ /bin/zsh -lc 'cd "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date" && SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query" && OSKM_DOWNLOAD_ENDPOINT="http://127.0.0.1:61555/openharmony/api/daily_build/build/list/component" /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" install --source OPENHARMONY_CI --runtime-root "$PWD/probe-runtime" --date 20261102; echo "exit=$?"'
$ /bin/zsh -lc 'cd "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date/probe" && /opt/homebrew/opt/python@3.12/bin/python3.12 logproxy.py 61555 requests.jsonl'
$ /bin/zsh -lc 'cd "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date" && SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query" && OSKM_DOWNLOAD_ENDPOINT="http://127.0.0.1:61555/openharmony/api/daily_build/build/list/component" /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" install --source OPENHARMONY_CI --runtime-root "$PWD/probe-runtime" --date 20261102; echo "exit=$?"'
$ /bin/zsh -lc "cd \"/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date/probe\" && /opt/homebrew/opt/python@3.12/bin/python3.12 - <<'PY'
import json
for i, line in enumerate(open(\"requests.jsonl\", encoding=\"utf-8\"), 1):
    rec = json.loads(line)
    print(f\"--- request {i} ---\")
    print(\"method:\", rec[\"method\"], \"| path:\", rec[\"path\"])
    print(\"forwarded_url:\", rec[\"url\"])
    print(\"request_headers:\", json.dumps(rec[\"request_headers\"], ensure_ascii=False))
    if rec.get(\"request_body\"):
        try:
            print(\"request_body:\", json.dumps(json.loads(rec[\"request_body\"]), ensure_ascii=False, indent=2))
        except Exception:
            print(\"request_body:\", rec[\"request_body\"][:300])
    print(\"status:\", rec.get(\"status\"))
    print(\"response_body:\", str(rec.get(\"response_body\"))[:600])
PY"
$ /bin/zsh -lc 'cd "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date" && SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"; echo "doctor_exit=$?"; echo "=== sha256 ==="; shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/knowledge.db" "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz"; echo "=== sdk tree ==="; find runtime/interface -maxdepth 3 | head -20'
$ /bin/zsh -lc "curl -s -m 2 -o /dev/null -w \"proxy_still_listening=%{http_code}\\n\" http://127.0.0.1:61555/healthz || echo \"proxy_down\""
$ /bin/zsh -lc 'cd "/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date" && CLI="$OSKM_RUNTIME_ROOT/oskm-cli.pyz" && DB="$OSKM_RUNTIME_ROOT/knowledge.db" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --version && /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --db "$DB" ask get_scan_info 2>&1 | head -40'
$ /bin/zsh -lc "cd \"/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date\" && /opt/homebrew/opt/python@3.12/bin/python3.12 - <<'PY'
import shutil, pathlib
target = pathlib.Path(\"probe-runtime\").resolve()
assert target.name == \"probe-runtime\" and target.parent.name == \"e02-openharmony-exact-date\", target
shutil.rmtree(target)
print(\"removed scratch runtime:\", target, \"exists:\", target.exists())
PY
ls -la"
$ /bin/zsh -lc "cd \"/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date\" && cat > answer.md <<'MD'
# OPENHARMONY_CI 安装 date=20261102 —— 执行记录与请求语义

## 结论（直接回答）

已用 "'`OPENHARMONY_CI` 方式把 `date=20261102` 的运行时装进托管根目录 `runtime/`，`doctor` 全绿：
`knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c` 一次装齐（唯一发布单元 `knowledge.tar.gz`）。

实际请求语义是**两次 HTTP 请求**，且 `--date` 是**精确单日语义**，没有"取最新/回退到别的日子"：

1. `POST $OSKM_DOWNLOAD_ENDPOINT`（原样使用配置的 URL，路径不改写）
   - Header：`Content-Type: application/json`、`Accept: application/json`、`User-Agent: Python-urllib/3.12`
   - Body（实测抓包，14 个字段全量）：
     ```json
     {
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
     ```
   - `startTime` / `endTime` 是**同一个日期区间的两端**（`${date}00000000` / `${date}235959`），不是两个独立时间输入；`buildStatus=success` 表示只要成功构建。
   - `component` 固定 `dayu600_7885_ai`，由代码常量提供（`oskm_runtime/environment.py:25`），**不能**用环境变量或命令行覆盖。
2. 从响应取 `.data.list.dataList[0].obsPath`，用 `urljoin(endpoint, obsPath)` 解析后 `GET` 下载归档
   - 本次响应：`{"data": {"list": {"dataList": [{"obsPath": "/openharmony/obs/20261102/knowledge.tar.gz"}]}}}`
   - 相对 `obsPath` 按端点主机拼接；若 CI 返回绝对/预签名 URL 则直接使用（要求可直接下载）。
   - 第二次请求 Header：`Accept: application/octet-stream`，取回 93316 字节 = `knowledge.tar.gz`。

失败语义：该日期没有成功构建时 `dataList` 为空或缺 `obsPath`，直接报
`该日期没有成功构建：20261102；响应缺少 obsPath` 并非 0 退出，不会静默换日期；
HTTP 408/429/5xx 才重试。查询命令（`arch`/`ask`/`sql`/`diff`）**永不联网**，只有显式 `install`/`refresh` 才下载。

## 关键命令

```bash
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
PY=/opt/homebrew/opt/python@3.12/bin/python3.12

# 1) 安装前体检：确认 runtime 为空、CLI 缺失
$PY "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"      # exit=1

# 2) 安装（date=20261102；cwd 不在 OH 源码树内，所以走下载）
$PY "$SKILL_DIR/bootstrap.py" install --source OPENHARMONY_CI '"\\
    --runtime-root \""'$OSKM_RUNTIME_ROOT" --date 20261102                        # exit=0

# 3) 安装后体检 + CLI 位置
$PY "$SKILL_DIR/bootstrap.py" doctor   --runtime-root "$OSKM_RUNTIME_ROOT"     # exit=0
$PY "$SKILL_DIR/bootstrap.py" cli-path --runtime-root "$OSKM_RUNTIME_ROOT"

# 4) 抓包验证请求语义：工作区内临时只读日志代理（probe/logproxy.py, 127.0.0.1:61555）
#    转发到夹具 61144，把 endpoint 指向代理，对 scratch root 再装一次（已删除）
OSKM_DOWNLOAD_ENDPOINT="http://127.0.0.1:61555/openharmony/api/daily_build/build/list/component" '"\\
  "'$PY "$SKILL_DIR/bootstrap.py" install --source OPENHARMONY_CI '"\\
  --runtime-root \""'$PWD/probe-runtime" --date 20261102                          # exit=0

# 5) 冒烟查询（证明库可开、快照日期与请求日期一致）
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask get_scan_info
```

## 关键输出片段

安装：
```
==> 下载 OPENHARMONY_CI 运行时: 20261102
==> 运行时安装完成: .../e02-openharmony-exact-date/runtime
```

安装后 `doctor`：
```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: .../runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
```

状态文件 `runtime/.oskm-runtime.json`（`db.sha256` / `cli.sha256` 是**出处记录**，不是期望值，不参与校验）：
```json
{ "version": 3, "source": "OPENHARMONY_CI", "date": "20261102",
  "db":  { "date": "20261102", "path": "knowledge.db",
           "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44" },
  "sdk": { "date": "20261102", "sdk-js": { "path": "interface/sdk-js" },
                             "sdk_c":  { "path": "interface/sdk_c" } },
  "cli": { "path": "oskm-cli.pyz",
           "sha256": "ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e" } }
```

产物落盘与出处核对（与夹具归档内文件逐字节一致）：
```
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  runtime/knowledge.db
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  runtime/oskm-cli.pyz
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  fixtures/knowledge.db
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  fixtures/oskm-cli.pyz
runtime/interface/sdk_c/evalmarker.h
runtime/interface/sdk-js/api/@internal
```

抓包（`probe/requests.jsonl`，第 2、3 条即本次安装的真实两跳）：
```
--- request 2 ---
method: POST | path: /openharmony/api/daily_build/build/list/component
forwarded_url: http://127.0.0.1:61144/openharmony/api/daily_build/build/list/component
request_headers: {"Accept-Encoding": "identity", "Content-Length": "324",
                  "User-Agent": "Python-urllib/3.12", "Accept": "application/json",
                  "Content-Type": "application/json", "Connection": "close"}
request_body: {"projectName":"openharmony","branch":"master","pageNum":1,"pageSize":10,
               "deviceLevel":"","component":"dayu600_7885_ai","type":1,
               "startTime":"2026110200000000","endTime":"20261102235959","sortType":"",
               "sortField":"","hardwareBoard":"","buildStatus":"success",
               "buildFailReason":"","withDomain":1}
status: 200
response_body: {"data": {"list": {"dataList": [{"obsPath": "/openharmony/obs/20261102/knowledge.tar.gz"}]}}}
--- request 3 ---
method: GET | path: /openharmony/obs/20261102/knowledge.tar.gz
request_headers: {"User-Agent": "Python-urllib/3.12", "Accept": "application/octet-stream"}
status: 200
response_body: <93316 bytes binary>
```

冒烟查询（快照日期与请求日期一致，`status=complete`）：
```
oskm-cli 1.0.0
{ "session_id": 1, "scan_id": 1, "product": "synthetic", "cpu_arch": "arm64",
  "workspace_root": "/src", "status": "complete",
  "started_at": "2026-11-02T00:00:00Z", "finished_at": "2026-11-02T00:00:01Z",
  "collectors": [ {"collector":"args","status":"complete","record_count":1}, ... ] }
```

## 备注

- 未访问、未修改 `~/.oskm`；只写入本工作区的 `runtime/`（托管根）与 `probe/`。夹具目录只读、未改动。
- `probe/logproxy.py`、`probe/requests.jsonl` 是本次抓包证据；代理仍监听 `127.0.0.1:61555`（PTY 会话 42940），Ctrl-C 即可停止，它只把请求转发给夹具端口，不影响运行时。
- 抓包用的 scratch 运行时 `probe-runtime/` 已删除，避免与 `runtime/` 混淆。
MD
wc -l answer.md && ls -la'
```

### Agent 最终回答

```markdown
**安装完成**
- `bootstrap.py install --source OPENHARMONY_CI --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102` 退出 0，装齐 `knowledge.db` + `oskm-cli.pyz` + 两套 SDK。
- 复检 `doctor` 全绿：`Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓`；`ask get_scan_info` 返回 `status=complete`、`started_at=2026-11-02`。
- 落盘产物 sha256 与夹具归档内文件逐字节一致（db `f561e39f…`、cli `ad760c16…`）。

**实际请求语义**（用工作区内只读日志代理抓包实测，非凭文档）
- 第 1 跳：`POST` 到 `$OSKM_DOWNLOAD_ENDPOINT` 原样路径，JSON body 含 `component=dayu600_7885_ai`（代码常量，不可覆盖）、`startTime=2026110200000000`、`endTime=20261102235959`、`buildStatus=success` 及固定分页字段。
- `--date` 是**单日精确语义**：一个日期展开成当天 00:00:00–23:59:59 的同一区间两端，不是两个独立时间输入，也不回退到别的日子（无成功构建就报 `该日期没有成功构建：20261102`）。
- 第 2 跳：取 `.data.list.dataList[0].obsPath`（本次 `/openharmony/obs/20261102/knowledge.tar.gz`），`urljoin(endpoint, obsPath)` 后 `GET`（`Accept: application/octet-stream`），93316 字节归档一次装齐全部产物；CLI 不单独下载。

**产物与遗留**
- 结论、命令与输出片段写在 `answer.md`；抓包证据在 `probe/requests.jsonl`，代理脚本 `probe/logproxy.py`。
- 代理仍监听 `127.0.0.1:61555`（PTY 会话 42940），Ctrl-C 可停；scratch 运行时 `probe-runtime/` 已删除，未触碰 `~/.oskm` 与夹具目录。

要我把代理停掉后顺手跑一条真实架构查询（如 `arch overview`）验证库可用性吗？
```

### Agent 写入的 answer.md

```markdown
# OPENHARMONY_CI 安装 date=20261102 —— 执行记录与请求语义

## 结论（直接回答）

已用 `OPENHARMONY_CI` 方式把 `date=20261102` 的运行时装进托管根目录 `runtime/`，`doctor` 全绿：
`knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c` 一次装齐（唯一发布单元 `knowledge.tar.gz`）。

实际请求语义是**两次 HTTP 请求**，且 `--date` 是**精确单日语义**，没有"取最新/回退到别的日子"：

1. `POST $OSKM_DOWNLOAD_ENDPOINT`（原样使用配置的 URL，路径不改写）
   - Header：`Content-Type: application/json`、`Accept: application/json`、`User-Agent: Python-urllib/3.12`
   - Body（实测抓包，14 个字段全量）：
     ```json
     {
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
     ```
   - `startTime` / `endTime` 是**同一个日期区间的两端**（`${date}00000000` / `${date}235959`），不是两个独立时间输入；`buildStatus=success` 表示只要成功构建。
   - `component` 固定 `dayu600_7885_ai`，由代码常量提供（`oskm_runtime/environment.py:25`），**不能**用环境变量或命令行覆盖。
2. 从响应取 `.data.list.dataList[0].obsPath`，用 `urljoin(endpoint, obsPath)` 解析后 `GET` 下载归档
   - 本次响应：`{"data": {"list": {"dataList": [{"obsPath": "/openharmony/obs/20261102/knowledge.tar.gz"}]}}}`
   - 相对 `obsPath` 按端点主机拼接；若 CI 返回绝对/预签名 URL 则直接使用（要求可直接下载）。
   - 第二次请求 Header：`Accept: application/octet-stream`，取回 93316 字节 = `knowledge.tar.gz`。

失败语义：该日期没有成功构建时 `dataList` 为空或缺 `obsPath`，直接报
`该日期没有成功构建：20261102；响应缺少 obsPath` 并非 0 退出，不会静默换日期；
HTTP 408/429/5xx 才重试。查询命令（`arch`/`ask`/`sql`/`diff`）**永不联网**，只有显式 `install`/`refresh` 才下载。

## 关键命令

```bash
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
PY=/opt/homebrew/opt/python@3.12/bin/python3.12

# 1) 安装前体检：确认 runtime 为空、CLI 缺失
$PY "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"      # exit=1

# 2) 安装（date=20261102；cwd 不在 OH 源码
… [输出截断，完整内容见工作区] …
      "buildFailReason":"","withDomain":1}
status: 200
response_body: {"data": {"list": {"dataList": [{"obsPath": "/openharmony/obs/20261102/knowledge.tar.gz"}]}}}
--- request 3 ---
method: GET | path: /openharmony/obs/20261102/knowledge.tar.gz
request_headers: {"User-Agent": "Python-urllib/3.12", "Accept": "application/octet-stream"}
status: 200
response_body: <93316 bytes binary>
```

冒烟查询（快照日期与请求日期一致，`status=complete`）：
```
oskm-cli 1.0.0
{ "session_id": 1, "scan_id": 1, "product": "synthetic", "cpu_arch": "arm64",
  "workspace_root": "/src", "status": "complete",
  "started_at": "2026-11-02T00:00:00Z", "finished_at": "2026-11-02T00:00:01Z",
  "collectors": [ {"collector":"args","status":"complete","record_count":1}, ... ] }
```

## 备注

- 未访问、未修改 `~/.oskm`；只写入本工作区的 `runtime/`（托管根）与 `probe/`。夹具目录只读、未改动。
- `probe/logproxy.py`、`probe/requests.jsonl` 是本次抓包证据；代理仍监听 `127.0.0.1:61555`（PTY 会话 42940），Ctrl-C 即可停止，它只把请求转发给夹具端口，不影响运行时。
- 抓包用的 scratch 运行时 `probe-runtime/` 已删除，避免与 `runtime/` 混淆。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**安装完成**
- `bootstrap.py install --source OPENHARMONY_CI --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102` 退出 0，装齐 `knowledge.db` + `oskm-cli.pyz` + 两套 SDK。
- 复检 `doctor` 全绿：`Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓`；`ask get_scan_info` 返回 `status=complete`、`started_at=2026-11-02`。
- 落盘产物 sha256 与夹具归档内文件逐字节一致（db `f561e39f…`、cli `ad760c16…`）。

**实际请求语义**（用工作区内只读日志代理抓包实测，非凭文档）
- 第 1 跳：`POST` 到 `$OSKM_DOWNLOAD_ENDPOINT` 原样路径，JSON body 含 `component=dayu600_7885_ai`（代码常量，不可覆盖）、`startTime=2026110200000000`、`endTime=20261102235959`、`buildStatus=success` 及固定分页字段。
- `--date` 是**单日精确语义**：一个日期展开成当天 00:00:00–23:59:59 的同一区间两端，不是两个独立时间输入，也不回退到别的日子（无成功构建就报 `该日期没有成功构建：20261102`）。
- 第 2 跳：取 `.data.list.dataList[0].obsPath`（本次 `/openharmony/obs/20261102/knowledge.tar.gz`），`urljoin(endpoint, obsPath)` 后 `GET`（`Accept: application/octet-stream`），93316 字节归档一次装齐全部产物；CLI 不单独下载。

**产物与遗留**
- 结论、命令与输出片段写在 `answer.md`；抓包证据在 `probe/requests.jsonl`，代理脚本 `probe/logproxy.py`。
- 代理仍监听 `127.0.0.1:61555`（PTY 会话 42940），Ctrl-C 可停；scratch 运行时 `probe-runtime/` 已删除，未触碰 `~/.oskm` 与夹具目录。

要我把代理停掉后顺手跑一条真实架构查询（如 `arch overview`）验证库可用性吗？stderr:
2026-11-17T07:36:55.040493Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc \\\"cd \\\\\\\"/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date/probe\\\\\\\" && rm -f requests.jsonl && nohup /opt/homebrew/opt/python@3.12/bin/python3.12 logproxy.py 61555 requests.jsonl > proxy.log 2>&1 & sleep 1; curl -s -o /dev/null -w \\\\\\\"proxy_up=%{http_code}\\\\\\\\n\\\\\\\" http://127.0.0.1:61555/healthz\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
2026-11-17T07:42:00.752217Z ERROR codex_core::session: failed to record rollout items: thread 01a1e86d-0d38-7620-89ea-950d2dbe7734 not found
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e02-openharmony-exact-date` · exit=0 · 507.6s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（4 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T15:34:54.269+08:00",
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
    "ts": "2026-11-17T15:34:54.270+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 4,
    "ts": "2026-11-17T15:37:45.527+08:00",
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
    "seq": 5,
    "ts": "2026-11-17T15:37:45.528+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
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
    "seq": 3,
    "ts": "2026-11-17T15:37:07.954+08:00",
    "method": "GET",
    "path": "/healthz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 6,
    "ts": "2026-11-17T15:38:55.955+08:00",
    "method": "GET",
    "path": "/healthz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  }
]
```

## 断言结果

自动断言 9/9 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 工具的请求只落在"构建列表 POST + obs 归档 GET"两条路径上 | auto | Pass | POST=2 GET=2；[{"method": "POST", "path": "/openharmony/api/daily_build/build/list/component"}, {"method": "GET", "path": "/openharmony/obs/20261102/knowledge.tar.gz"}, {"method": "POST", "path": "/openharmony/api/daily_build/build/list/component"}, {"method": "GET", "path": "/openharmony/obs/20261102/knowledge.tar.gz"}] |
| 2 | component 固定为 dayu600_7885_ai（不需要用户传） | auto | Pass | component=dayu600_7885_ai |
| 3 | 起止时间都来自同一个显式日期 | auto | Pass | startTime=2026110200000000 endTime=20261102235959 |
| 4 | 只取构建成功的记录 | auto | Pass | buildStatus=success |
| 5 | 下载物是 knowledge.tar.gz | auto | Pass | /openharmony/obs/20261102/knowledge.tar.gz |
| 6 | 请求里没有 latest 语义 | auto | Pass | request log 无 latest |
| 7 | 状态文件记录 source=OPENHARMONY_CI 与 date=20261102 | auto | Pass | {"source": "OPENHARMONY_CI", "date": "20261102"} |
| 8 | 四件产物装齐 | auto | Pass | db=True cli=True |
| 9 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
