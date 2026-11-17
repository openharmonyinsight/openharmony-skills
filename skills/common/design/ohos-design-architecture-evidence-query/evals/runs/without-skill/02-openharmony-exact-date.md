# E2 openharmony-exact-date（without-skill 臂）

- 开始时间：2026-11-17T16:18:33+08:00
- 结束时间：2026-11-17T16:30:53+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date`
- 夹具服务端：http://127.0.0.1:61808
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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：711.4 s
- 事件计数：`{"thread.started": 1, "item.completed": 81, "item:error": 1, "turn.started": 1, "item:reasoning": 26, "item:agent_message": 16, "item.started": 38, "item:command_execution": 76, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：38
- token 用量：`{"input_tokens": 1024107, "cached_input_tokens": 958720, "output_tokens": 25158, "reasoning_output_tokens": 11497}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && ls -la && echo \"--- tree ---\" && find . -maxdepth 3 -not -path '*/.git/*' | head -100"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && cat tool/bootstrap.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && cat PROMPT.md && echo "=== .env.example ===" && cat tool/oskm_runtime/.env.example && echo "=== wc ===" && wc -l tool/oskm_runtime/*.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && cat tool/oskm_runtime/bootstrap.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && cat tool/oskm_runtime/db_download.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && cat tool/oskm_runtime/environment.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && sed -n '128,260p' tool/oskm_runtime/db_download.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && sed -n '260,400p' tool/oskm_runtime/db_download.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && sed -n '1,200p' tool/oskm_runtime/install.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && sed -n '200,451p' tool/oskm_runtime/install.py && echo \"=== ENV ===\" && env | grep -i oskm; echo \"(exit "'$?)"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && cat tool/oskm_runtime/doctor.py && echo "=== state.py ===" && cat tool/oskm_runtime/state.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py install --date 20261102 2>&1 | tee /tmp/oskm-install-20261102.log; echo "EXIT=${PIPESTATUS[0]}"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && find runtime -maxdepth 3 | sort && echo "=== state ===" && cat runtime/.oskm-runtime.json'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py doctor; echo "EXIT=$?"'
$ /bin/zsh -lc "cd /tmp && cat > /tmp/oh_payload.json <<'EOF'
{\"projectName\": \"openharmony\", \"branch\": \"master\", \"pageNum\": 1, \"pageSize\": 10, \"deviceLevel\": \"\", \"component\": \"dayu600_7885_ai\", \"type\": 1, \"startTime\": \"2026110200000000\", \"endTime\": \"20261102235959\", \"sortType\": \"\", \"sortField\": \"\", \"hardwareBoard\": \"\", \"buildStatus\": \"success\", \"buildFailReason\": \"\", \"withDomain\": 1}
EOF
curl -sS -D /tmp/oh_headers.txt -X POST \"http://127.0.0.1:61808/openharmony/api/daily_build/build/list/component\" -H 'Accept: application/json' -H 'Content-Type: application/json' --data-binary @/tmp/oh_payload.json -o /tmp/oh_body.json -w 'HTTP %{http_code}\\n'; echo \"--- headers ---\"; cat /tmp/oh_headers.txt; echo \"--- body ---\"; /opt/homebrew/opt/python@3.12/bin/python3.12 -m json.tool /tmp/oh_body.json"
$ /bin/zsh -lc 'cd /tmp && for d in 20261101 20261102 20261103; do
  echo "=== date=$d (startTime=${d}00000000 endTime=${d}235959) ==="
  curl -sS -X POST "http://127.0.0.1:61808/openharmony/api/daily_build/build/list/component" '"\\
    -H 'Accept: application/json' -H 'Content-Type: application/json' \\
    --data-binary \"{\\\"projectName\\\":\\\"openharmony\\\",\\\"branch\\\":\\\"master\\\",\\\"pageNum\\\":1,\\\"pageSize\\\":10,\\\"deviceLevel\\\":\\\"\\\",\\\"component\\\":\\\"dayu600_7885_ai\\\",\\\"type\\\":1,\\\"startTime\\\":\\\""'${d}00000000'"\\\",\\\"endTime\\\":\\\""'${d}235959'"\\\",\\\"sortType\\\":\\\"\\\",\\\"sortField\\\":\\\"\\\",\\\"hardwareBoard\\\":\\\"\\\",\\\"buildStatus\\\":\\\"success\\\",\\\"buildFailReason\\\":\\\"\\\",\\\"withDomain\\\":1}\" \\
    -w '\\nHTTP %{http_code}\\n'
done"
$ /bin/zsh -lc 'cd /tmp && EP="http://127.0.0.1:61808/openharmony/api/daily_build/build/list/component"
probe () { echo "--- $1 ---"; curl -sS -X POST "$EP" -H '"'Content-Type: application/json' --data-binary \""'$2" -w '"'\\nHTTP %{http_code}\\n'; echo; }
probe \"wide window 20261101..20261103\" '{\"projectName\":\"openharmony\",\"branch\":\"master\",\"pageNum\":1,\"pageSize\":10,\"component\":\"dayu600_7885_ai\",\"type\":1,\"startTime\":\"2026110100000000\",\"endTime\":\"20261103235959\",\"buildStatus\":\"success\",\"withDomain\":1}'
probe \"no time bounds at all\" '{\"projectName\":\"openharmony\",\"branch\":\"master\",\"pageNum\":1,\"pageSize\":10,\"component\":\"dayu600_7885_ai\",\"type\":1,\"buildStatus\":\"success\",\"withDomain\":1}'
probe \"component=other\" '{\"projectName\":\"openharmony\",\"branch\":\"master\",\"pageNum\":1,\"pageSize\":10,\"component\":\"rk3568\",\"type\":1,\"startTime\":\"2026110200000000\",\"endTime\":\"20261102235959\",\"buildStatus\":\"success\",\"withDomain\":1}'
probe \"buildStatus=fail\" '{\"projectName\":\"openharmony\",\"branch\":\"master\",\"pageNum\":1,\"pageSize\":10,\"component\":\"dayu600_7885_ai\",\"type\":1,\"startTime\":\"2026110200000000\",\"endTime\":\"20261102235959\",\"buildStatus\":\"fail\",\"withDomain\":1}'
probe \"GET instead of POST\" '{}'"
$ /bin/zsh -lc "cd /tmp && echo \"--- GET the obsPath (as urljoin resolves it) ---\" && curl -sS -D - -o /tmp/oh_archive.tar.gz \"http://127.0.0.1:61808/openharmony/obs/20261102/knowledge.tar.gz\" -w 'HTTP %{http_code} size=%{size_download}\\n' && ls -l /tmp/oh_archive.tar.gz && echo \"--- archive members ---\" && tar tzvf /tmp/oh_archive.tar.gz && echo \"--- installed db sha256 vs archive db ---\" && shasum -a 256 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date/runtime/knowledge.db"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && echo \"--- sdk_c/evalmarker.h ---\" && cat runtime/interface/sdk_c/evalmarker.h && echo \"--- sdk-js marker ---\" && cat \"runtime/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts\" && echo \"--- db tables ---\" && /opt/homebrew/opt/python@3.12/bin/python3.12 - <<'PY'
import sqlite3
db = sqlite3.connect('runtime/knowledge.db')
print([r[0] for r in db.execute(\"select name from sqlite_master where type='table' order by name\")])
try:
    print('scans rows:', list(db.execute('select * from scans limit 5')))
except Exception as exc:
    print('scans err', exc)
PY"
$ /bin/zsh -lc "cd /tmp && echo \"--- unknown-date archive (no startTime) ---\"; curl -sS -o /tmp/oh_unknown.tar.gz -w 'HTTP %{http_code} size=%{size_download}\\n' \"http://127.0.0.1:61808/openharmony/obs/unknown-date/knowledge.tar.gz\"; echo \"--- bogus date 19990101 list ---\"; curl -sS -X POST \"http://127.0.0.1:61808/openharmony/api/daily_build/build/list/component\" -H 'Content-Type: application/json' --data-binary '{\"projectName\":\"openharmony\",\"branch\":\"master\",\"pageNum\":1,\"pageSize\":10,\"component\":\"dayu600_7885_ai\",\"type\":1,\"startTime\":\"1999010100000000\",\"endTime\":\"19990101235959\",\"buildStatus\":\"success\",\"withDomain\":1}' -w '\\nHTTP %{http_code}\\n'; echo \"--- bogus date archive GET ---\"; curl -sS -o /dev/null -w 'HTTP %{http_code}\\n' \"http://127.0.0.1:61808/openharmony/obs/19990101/knowledge.tar.gz\""
$ /bin/zsh -lc 'mkdir -p /tmp/ohprobe2 && cd /tmp/ohprobe2 && for d in 20261101 20261102 20261103 19990101 unknown-date; do curl -sS -o "$d.tar.gz" "http://127.0.0.1:61808/openharmony/obs/$d/knowledge.tar.gz"; done; shasum -a 256 *.tar.gz'
$ /bin/zsh -lc 'mkdir -p /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date/probe && echo ok'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && apply_patch <<'PATCH'
*** Begin Patch
*** Add File: probe/trace_requests.py
+\"\"\"Trace the exact HTTP requests oskm_runtime issues for OPENHARMONY_CI.
+
+Usage: python3 probe/trace_requests.py <output-dir>
+\"\"\"
+from __future__ import annotations
+
+import sys
+from pathlib import Path
+
+HERE = Path(__file__).resolve().parent
+sys.path.insert(0, str(HERE.parent / 'tool'))
+
+from oskm_runtime import db_download  # noqa: E402
+
+real_urlopen = db_download.urlopen
+
+
+def traced(request, *args, **kwargs):
+    print(f'--> {request.get_method()} {request.full_url}')
+    for name, value in request.header_items():
+        print(f'    header {name}: {value}')
+    if request.data:
+        print(f'    body {request.data.decode(\"utf-8\")}')
+    response = real_urlopen(request, *args, **kwargs)
+    print(f'<-- HTTP {response.status} '
+          f'Content-Type={response.headers.get(\"Content-Type\")} '
+          f'Content-Length={response.headers.get(\"Content-Length\")}')
+    return response
+
+
+db_download.urlopen = traced
+
+target = Path(sys.argv[1]).expanduser().resolve() / 'runtime-traced'
+print(f'== download_runtime_bundle(source=OPENHARMONY_CI, date=20261102) '
+      f'-> {target}')
+bundle = db_download.download_runtime_bundle(
+    source='OPENHARMONY_CI', date='20261102', output=target)
+print(f'== bundle ready: {bundle}')
+for path in sorted(bundle.rglob('*')):
+    if path.is_file():
+        print(f'   {path.relative_to(bundle)} ({path.stat().st_size} bytes)')
*** End Patch
PATCH
echo \"EXIT="'$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 probe/trace_requests.py probe 2>&1 | tee probe/trace-20261102.log; echo "EXIT=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && apply_patch <<'PATCH'
*** Begin Patch
*** Add File: probe/probe_error_paths.py
+\"\"\"Show how OPENHARMONY_CI reacts to list-API responses that lack the date.\"\"\"
+from __future__ import annotations
+
+import io
+import sys
+from pathlib import Path
+from urllib.error import HTTPError
+
+HERE = Path(__file__).resolve().parent
+sys.path.insert(0, str(HERE.parent / 'tool'))
+
+from oskm_runtime import db_download  # noqa: E402
+from oskm_runtime.db_download import DownloadError  # noqa: E402
+
+
+def fake_response(body: bytes, content_type='application/json'):
+    stream = io.BytesIO(body)
+    stream.headers = {'Content-Type': content_type}
+    stream.status = 200
+    return stream
+
+
+CASES = {
+    'empty dataList': fake_response(
+        b'{\"data\": {\"list\": {\"dataList\": []}}}'),
+    'obsPath missing': fake_response(b'{\"data\": {\"list\": {\"dataList\": [{}]}}}'),
+    'obsPath empty': fake_response(
+        b'{\"data\": {\"list\": {\"dataList\": [{\"obsPath\": \"\"}]}}}'),
+    'not JSON': fake_response(b'<html>gateway error</html>', 'text/html'),
+}
+
+output = HERE / 'never-written.db'
+for label, response in CASES.items():
+    db_download.urlopen = lambda request, *a, **k: response
+    try:
+        db_download.download_database(
+            source='OPENHARMONY_CI', date='20261102', output=output)
+        print(f'{label:16} -> UNEXPECTED SUCCESS')
+    except DownloadError as exc:
+        print(f'{label:16} -> DownloadError: {exc}')
+
+
+def http_404(request, *args, **kwargs):
+    raise HTTPError(request.full_url, 404, 'Not Found', {}, None)
+
+
+db_download.urlopen = http_404
+try:
+    db_download.download_database(
+        source='OPENHARMONY_CI', date='20261102', output=output)
+    print(f'{\"HTTP 404\":16} -> UNEXPECTED SUCCESS')
+except DownloadError as exc:
+    print(f'{\"HTTP 404\":16} -> DownloadError: {exc}')
+print(f'output file written? {output.exists()}')
*** End Patch
PATCH
/opt/homebrew/opt/python@3.12/bin/python3.12 probe/probe_error_paths.py 2>&1 | tee probe/error-paths.log"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && echo "--- install with non-YYYYMMDD date ---" && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py install --date 2026-11-02; echo "EXIT=$?"; echo "--- refresh --date 20261102 (already installed) ---"; /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py refresh --date 20261102; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && echo "--- validate-db ---" && /opt/homebrew/opt/python@3.12/bin/python3.12 tool/bootstrap.py validate-db runtime/knowledge.db; echo "EXIT=$?"; echo "--- cli version ---"; /opt/homebrew/opt/python@3.12/bin/python3.12 runtime/oskm-cli.pyz --version; echo "--- cli query ---"; /opt/homebrew/opt/python@3.12/bin/python3.12 runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview 2>&1 | head -20'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && echo \"--- any payload-date cross-check? ---\" && rg -n \"startTime|endTime|dataList|obsPath|withDomain|OPENHARMONY_COMPONENT\" tool/oskm_runtime/ && echo \"--- needs_refresh semantics (read-only) ---\" && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import sys; sys.path.insert(0,'tool')
from oskm_runtime import state
from pathlib import Path
db=Path('runtime/knowledge.db')
print('state date:', state.load_state(db)['date'])
print('needs_refresh(current=20261102):', state.needs_refresh(db, current_date='20261102'))
print('needs_refresh(current=20261117):', state.needs_refresh(db, current_date='20261117'))
print('today():', state.today())
\""
$ /bin/zsh -lc "cd /tmp && echo \"--- real GET on the list endpoint ---\"; curl -sS -X GET \"http://127.0.0.1:61808/openharmony/api/daily_build/build/list/component\" -w '\\nHTTP %{http_code}\\n'; echo \"--- GET endpoint/20261102 (INTERNAL_CI style) ---\"; curl -sS -o /dev/null -w 'HTTP %{http_code}\\n' \"http://127.0.0.1:61808/openharmony/api/daily_build/build/list/component/20261102\""
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import shutil, pathlib
p = pathlib.Path('probe/runtime-traced').resolve()
assert p.name == 'runtime-traced' and p.parent.name == 'probe', p
shutil.rmtree(p)
print('removed', p)
\" && ls -la probe && echo \"--- workspace top ---\" && ls -la"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
from urllib.parse import urljoin
api='http://127.0.0.1:61808/openharmony/api/daily_build/build/list/component'
for p in ['/openharmony/obs/20261102/knowledge.tar.gz','https://obs.example.com/x/knowledge.tar.gz','obs/20261102/knowledge.tar.gz']:
    print(repr(p),'->',urljoin(api,p))
\""
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && sed -n '/"'^def _do_install/,/''^def cmd_refresh/p'"' tool/oskm_runtime/bootstrap.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && apply_patch <<'PATCH'
*** Begin Patch
*** Add File: answer.md
+# OPENHARMONY_CI 安装 date=20261102：执行记录与请求语义
+
+## 0. 直接回答
+
+- **安装成功**。"'`runtime/` 里已经有 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js/` + `interface/sdk_c/`，状态文件 `runtime/.oskm-runtime.json` 记为 `version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓`，`doctor` 退出 0，`validate-db` 返回 `{"ok": true}`。
+- **实际请求语义**：`OPENHARMONY_CI` 下 `date` **不是 URL 的一部分**，它被展开成"一整天"的时间窗写进 POST body（`startTime`/`endTime`），组件名硬编码为 `dayu600_7885_ai`；真正的归档地址来自响应里的 `data.list.dataList[0].obsPath`，再 `urljoin` 到端点的 origin。整次安装**只有两个 HTTP 请求**：一次 POST 查列表，一次 GET 下归档。
+- **它不是"精确日期等值查询"**，而是"当天 00:00:00–23:59:59 的成功构建列表，取第 0 条"。客户端**不回验**返回的构建是否真属于 20261102；日期是否准，完全取决于服务端是否老实按窗口过滤。下面的夹具实测证明了这一点。
+
+## 1. 执行过的关键命令
+
+```bash
+PY=/opt/homebrew/opt/python@3.12/bin/python3.12
+
+# 安装前体检（CLI/DB 都还没有，按设计退出 1）
+$PY tool/bootstrap.py doctor
+
+# 正式安装（OSKM_DOWNLOAD_SOURCE / OSKM_DOWNLOAD_ENDPOINT / OSKM_RUNTIME_ROOT 已在环境里）
+$PY tool/bootstrap.py install --date 20261102
+
+# 安装后体检 + schema 契约校验 + 用装好的 CLI 查一次
+$PY tool/bootstrap.py doctor
+$PY tool/bootstrap.py validate-db runtime/knowledge.db
+$PY runtime/oskm-cli.pyz --version
+$PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
+
+# 幂等性：同日期 refresh 不联网
+$PY tool/bootstrap.py refresh --date 20261102
+
+# 语义取证：抓真实 HTTP 请求 / 打错误分支（脚本见 probe/）
+$PY probe/trace_requests.py probe      # 日志 probe/trace-20261102.log
+$PY probe/probe_error_paths.py         # 日志 probe/error-paths.log
+```
+
+## 2. 关键输出片段
+
+安装（stderr）：
+
+```
+==> 下载 OPENHARMONY_CI 运行时: 20261102
+==> 运行时安装完成: .../e02-openharmony-exact-date/runtime
+```
+
+安装后 `doctor`：
+
+```
+Python: 3.12.16 (OK, requires Python 3.10+)
+Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
+CLI: .../runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
+Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
+Runtime state: version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓
+Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
+EXIT=0
+```
+
+落盘结果（`find runtime`）与状态：
+
+```
+runtime/.oskm-runtime.json
+runtime/knowledge.db                     sha256 f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44
+runtime/oskm-cli.pyz                     sha256 3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5
+runtime/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
+runtime/interface/sdk_c/evalmarker.h
+```
+
+`validate-db` / CLI：
+
+```
+{"path": "runtime/knowledge.db", "ok": true}
+oskm-cli 1.0.0
+arch overview -> {"product": "synthetic", "scan_id": 1, "subsystems": 2, ...}
+```
+
+**真实请求轨迹**（`probe/trace_requests.py` 钩住 `db_download.urlopen`，不是手抄 payload）：
+
+```
+--> POST http://127.0.0.1:61808/openharmony/api/daily_build/build/list/component
+    header Accept: application/json
+    header Content-type: application/json
+    body {"projectName": "openharmony", "branch": "master", "pageNum": 1, "pageSize": 10,
+          "deviceLevel": "", "component": "dayu600_7885_ai", "type": 1,
+          "startTime": "2026110200000000", "endTime": "20261102235959",
+          "sortType": "", "sortField": "", "hardwareBoard": "",
+          "buildStatus": "success", "buildFailReason": "", "withDomain": 1}
+<-- HTTP 200 Content-Type=application/json Content-Length=93
+--> GET http://127.0.0.1:61808/openharmony/obs/20261102/knowledge.tar.gz
+    header Accept: application/octet-stream
+<-- HTTP 200 Content-Type=application/gzip Content-Length=94314
+```
+
+列表响应与解压后的归档内容：
+
+```json
+{"data": {"list": {"dataList": [{"obsPath": "/openharmony/obs/20261102/knowledge.tar.gz"}]}}}
+```
+
+```
+knowledge.tar.gz
+  knowledge.db                                          434176 B
+  oskm-cli.pyz                                           84742 B
+  interface/sdk-js/api/@internal/ohos.evalmarker.d.ts       55 B
+  interface/sdk_c/evalmarker.h                              51 B
+```
+
+## 3. 请求语义逐条拆解
+
+### 3.1 第一跳：POST 列表查询（`tool/oskm_runtime/db_download.py:136`）
+
+- URL **原样使用** `OSKM_DOWNLOAD_ENDPOINT`，不追加任何路径段（对比 `INTERNAL_CI` 是 `GET <endpoint>/<YYYYMMDD>`，日期直接进路径）。
+- 方法固定 `POST`，头固定 `Accept: application/json` + `Content-Type: application/json`（urllib 上线时规范化成 `Content-type`）。
+- `--date 20261102` 只落在两个字段上：
+  - `startTime = "2026110200000000"` —— `date` + `00000000`，**16 位**
+  - `endTime   = "20261102235959"` —— `date` + `235959`，**14 位**
+  - 语义是"当天零点到 23:59:59 的**时间窗**"，两端位数并不对称（一边补到 16 位、一边只到秒），这是代码里写死的格式，不是可配置项。
+- 其余字段全是硬编码常量：`projectName=openharmony`、`branch=master`、`component=dayu600_7885_ai`（`tool/oskm_runtime/environment.py:25`，**不能**用环境变量改）、`type=1`、`pageNum=1`、`pageSize=10`、`buildStatus=success`、`withDomain=1`、`sortType`/`sortField`/`deviceLevel`/`hardwareBoard`/`buildFailReason` 传空串。
+- 也就是"要什么日期"完全由这一次 POST 表达；`pageSize=10` 但客户端只用第 0 条。
+
+### 3.2 第二跳：GET 归档（`tool/oskm_runtime/db_download.py:181`、`:203`）
+
+- 取值路径写死为 `document['"'data']['list']['dataList'][0]['obsPath']"'` —— **无排序、无筛选、无日期回验，直接拿第 0 条**。
+- `url = urljoin(endpoint, obsPath)`。实测三种形态：
+  - `/openharmony/obs/20261102/knowledge.tar.gz`（本夹具）→ `http://127.0.0.1:61808/openharmony/obs/20261102/knowledge.tar.gz`
+  - `https://obs.example.com/x/knowledge.tar.gz` → 原样使用（`withDomain=1` 就是让服务端可以返回带域名的绝对 URL）
+  - `obs/20261102/knowledge.tar.gz`（**不带前导斜杠**）→ `http://127.0.0.1:61808/openharmony/api/daily_build/build/list/obs/20261102/knowledge.tar.gz`，会被解析到 API 路径底下，是个坑。
+- GET 只带 `Accept: application/octet-stream`；本地归档文件名取 URL path 的尾段（`_download_name`），因此**必须是 tar 系后缀**，`extract_runtime` 见到非 tar 直接报错。
+- 重试/超时：`timeout=90s`，`attempts=3`，`retry_delay=2s`；只有 HTTP 408/429/5xx 与 OSError 会重试，4xx（如 404）立刻失败。
+
+### 3.3 落盘：解压 → 校验 → 原子替换
+
+- `extract_runtime` 是防御式解压：拒绝越界路径、拒绝穿越符号链接写入、要求根目录**恰有一个** `knowledge.db` 且是普通文件、`oskm-cli.pyz` 至多一个、`interface/sdk-js/` 与 `interface/sdk_c/` 都必须非空。
+- `verify_sqlite` 校文件头魔数 + `PRAGMA integrity_check`。
+- schema 契约用**归档自带的那个 `oskm-cli.pyz`** 来校（`install.bundle_validator`），避免"新 CLI 校旧库"。
+- `_install_artifacts` 先把旧产物 `os.replace` 进同目录备份目录，任一步失败**逆序回滚**；最后写 `.oskm-runtime.json`（version 3）。
+- CLI 没有独立下载端点：它随 `knowledge.tar.gz` 一起发布、一起落到 `<runtime-root>/oskm-cli.pyz`。
+
+## 4. "date=20261102" 的可信边界（夹具实测）
+
+用 curl 直接打夹具，验证服务端到底怎么理解这个窗口：
+
+| 探测 | 结果 |
+| --- | --- |
+| `GET <endpoint>`（真 GET） | `HTTP 404 {"error":"not found"}` —— 列表端点是 POST-only |
+| `GET <endpoint>/20261102`（INTERNAL_CI 风格） | `HTTP 404` —— 日期不进 URL 路径 |
+| `startTime=2026110100000000`, `endTime=20261103235959`（跨 3 天） | 返回 `obs/20261101/...` —— **只按 `startTime` 定日期，`endTime` 被忽略** |
+| `component=rk3568` | 仍返回 `obs/20261102/...` —— 组件名被忽略 |
+| `buildStatus=fail` | 仍返回 `obs/20261102/...` —— 构建状态被忽略 |
+| 不带任何时间字段 | 返回 `obs/unknown-date/knowledge.tar.gz`，`HTTP 200`，客户端会照装不误 |
+| `obs/19990101/knowledge.tar.gz` | `HTTP 200` —— 任意日期都有货 |
+
+归档内容对比（`shasum -a 256`）：
+
+```
+f1c8df963be651232a190391b23b14a1d43e97bd168db9d65a5e91345cc073a9  19990101.tar.gz
+f1c8df963be651232a190391b23b14a1d43e97bd168db9d65a5e91345cc073a9  20261101.tar.gz
+f1c8df963be651232a190391b23b14a1d43e97bd168db9d65a5e91345cc073a9  20261102.tar.gz
+f1c8df963be651232a190391b23b14a1d43e97bd168db9d65a5e91345cc073a9  20261103.tar.gz
+f1c8df963be651232a190391b23b14a1d43e97bd168db9d65a5e91345cc073a9  unknown-date.tar.gz
+```
+
+即：**这套夹具里日期只体现在 URL 路径上，五个日期的归档字节完全相同**；里面 `knowledge.db` 的 `scans` 行固定是
+`(1, '"'synthetic', 'arm64', '/src', '2026-11-02T00:00:00Z', '2026-11-02T00:00:01Z')"'`。
+
+客户端侧同样没有日期回验，代码里 `date` 只出现在这几处（`rg -n` 结果）：
+
+```
+tool/oskm_runtime/db_download.py:153:        '"'startTime': f'{date}00000000',
+tool/oskm_runtime/db_download.py:154:        'endTime': f'{date}235959',
+tool/oskm_runtime/db_download.py:181:        obs_path = document['data']['list']['dataList'][0]['obsPath']
+"'```
+
+`.oskm-runtime.json` 里的 `"date": "20261102"` 是 `--date` 参数**原样回写**（`install.build_state`），不是从库里读出来的；安装过程只校 SQLite 完整性与 schema，不校"这份数据是不是 11-02 的"。
+
+**推论**：在真实 DCP 上，如果 20261102 当天有多次成功构建，装到的是服务端返回顺序里的 `dataList[0]`（`sortType`/`sortField` 传空，排序由服务端定），不保证是唯一或最新那一次；如果服务端不严格遵守窗口，客户端也不会发现。
+
+## 5. 失败与幂等语义（`probe/probe_error_paths.py` 实测）
+
+```
+empty dataList   -> DownloadError: 该日期没有成功构建：20261102；响应缺少 obsPath
+obsPath missing  -> DownloadError: 该日期没有成功构建：20261102；响应缺少 obsPath
+obsPath empty    -> DownloadError: 该日期没有成功构建，或 obsPath 为空（20261102）
+not JSON         -> DownloadError: OPENHARMONY_CI 构建响应不是有效 JSON（20261102）: Expecting value: ...
+HTTP 404         -> DownloadError: 下载失败（HTTP 404）: http://127.0.0.1:61808/openharmony/api/daily_build/build/list/component. ...
+output file written? False
+```
+
+- 失败时**不写任何目标文件**，已有运行时也不受影响（临时目录 + 原子替换 + 回滚）。
+- `--date` 格式先校：`install --date 2026-11-02` → `错误: --date 必须是 YYYYMMDD: 2026-11-02`，退出 1，**一个请求都不发**。
+- `refresh --date 20261102` → `==> 运行时已是最新，无需刷新`，退出 0，不联网。
+- `refresh` **不带** `--date` 会用 `today()`（当前 `20261117`）：只读验证 `state.needs_refresh(db, current_date='"'20261117') == True"'`，也就是它会按 20261117 重新下载并把 `state.date` 改写掉。想钉住 11-02 就必须显式带 `--date`（本次没有执行这个改写）。
+- `install` 会先找本地源码树（cwd 及其祖先里有 `.gn` + `interface/sdk-js` + `interface/sdk_c` + `out` 就离线复用，可用 `--source-root` 指定）；本工作区没有，所以走了下载分支。
+
+## 6. 产物与后续用法
+
+```bash
+# 查询一律直接调装好的 CLI（bootstrap.py 不管查询）
+$PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
+$PY runtime/oskm-cli.pyz --db runtime/knowledge.db ask --list
+$PY runtime/oskm-cli.pyz --help
+```
+
+取证脚本与日志保留在 `probe/`：`trace_requests.py`（钩 `urlopen` 打真实请求）、`trace-20261102.log`、`probe_error_paths.py`、`error-paths.log`。未触碰 `~/.oskm`，未修改 `tool/` 与夹具。
*** End Patch
PATCH
echo "EXIT=$?"; wc -l answer.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && rg -n "''^def _fetch_openharmony_obs_path|''^def _download_archive|''^def extract_runtime|''^def verify_sqlite" tool/oskm_runtime/db_download.py && rg -n "OPENHARMONY_COMPONENT = " tool/oskm_runtime/environment.py && echo "--- final state ---" && /opt/homebrew/opt/python@3.12/bin/python3.12 -c "import json;print(json.load(open('"'runtime/.oskm-runtime.json'))['date'])\" && ls -la . runtime"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && sed -n '199,222p' tool/oskm_runtime/db_download.py | cat -n | sed 's/"'^/  /'"' && rg -n \"    _fetch\\("'$" tool/oskm_runtime/db_download.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && apply_patch <<'PATCH'
*** Begin Patch
*** Update File: answer.md
@@
-URL 原样使用
-### 3.2 第二跳：GET 归档（"'`tool/oskm_runtime/db_download.py:181`、`:203`）
+### 3.2 第二跳：GET 归档（`tool/oskm_runtime/db_download.py:212` 分支、`:219` 发起 GET）
*** End Patch
PATCH
rg -n "3.2 第二跳" answer.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date && apply_patch <<'PATCH'
*** Begin Patch
*** Update File: answer.md
@@
-### 3.2 第二跳：GET 归档（"'`tool/oskm_runtime/db_download.py:181`、`:203`）
+### 3.2 第二跳：GET 归档（obsPath 解析 `tool/oskm_runtime/db_download.py:181`，分支 `:212`，发起 GET `:219`）
*** End Patch
PATCH
rg -n "3.2 第二跳|db_download.py:" answer.md'
```

### Agent 最终回答

```markdown
**Done**
- Ran `install --date 20261102` against the fixture: `runtime/knowledge.db`, `runtime/oskm-cli.pyz`, `runtime/interface/sdk-js`, `runtime/interface/sdk_c` all landed; `runtime/.oskm-runtime.json` reads `version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓`.
- `doctor` exits 0, `validate-db` returns `{"ok": true}`, and `oskm-cli.pyz --db runtime/knowledge.db arch overview` answers (`product: synthetic`, `scan_id: 1`).
- Write-up is in `answer.md`; trace scripts and logs are in `probe/`.

**Actual Request Semantics**
- Exactly two HTTP calls (traced by hooking `db_download.urlopen`, not hand-copied): `POST` to `OSKM_DOWNLOAD_ENDPOINT` verbatim, then `GET` on the returned `obsPath`.
- The date is a **day window in the POST body**, not a URL segment: `startTime="2026110200000000"` (16 digits), `endTime="20261102235959"` (14 digits) — asymmetric formats, both hard-coded at `tool/oskm_runtime/db_download.py:153`.
- Everything else is a constant: `component=dayu600_7885_ai` (`tool/oskm_runtime/environment.py:25`, not env-configurable), `projectName=openharmony`, `branch=master`, `type=1`, `buildStatus=success`, `pageNum=1/pageSize=10`, `withDomain=1`, empty sort fields.
- Artifact URL is `urljoin(endpoint, data.list.dataList[0].obsPath)` → `http://127.0.0.1:61808/openharmony/obs/20261102/knowledge.tar.gz`, fetched with `Accept: application/octet-stream`; filename must be a tar suffix.
- Contrast: `INTERNAL_CI` is `GET <endpoint>/<YYYYMMDD>` (exact addressing). Confirmed the fixture's list endpoint is POST-only — a real `GET` there returns 404.

**Date Fidelity Caveat**
- The client takes `dataList[0]` blindly and never re-checks the build's date; `state.date` is just the `--date` argument echoed by `install.build_state`, not read from the DB.
- Fixture probes show it keys only off `startTime`: a `20261101..20261103` window returns the 11-01 build, and `component`/`buildStatus`/`endTime` are ignored; with no time fields it serves `obs/unknown-date/...` at HTTP 200, which the client would install without complaint.
- All five dates serve byte-identical archives (`sha256 f1c8df96…`), so here the date only changes the URL path — the DB's `scans` row is fixed at `2026-11-02T00:00:00Z`.
- Failure paths verified in `probe/error-paths.log`: empty `dataList` → `该日期没有成功构建：20261102；响应缺少 obsPath`; non-JSON → `构建响应不是有效 JSON`; HTTP 404 fails fast while 408/429/5xx retry 3× at 2s with a 90s timeout; nothing is written on failure.

**Idempotency Note**
- `refresh --date 20261102` → `运行时已是最新，无需刷新` (no network). Bare `refresh` uses `today()` = `20261117`, and `state.needs_refresh` returns `True` — it would re-download and overwrite `state.date`, so keep `--date` explicit to stay pinned to 11-02. I did not run that.

Want me to also exercise `--skip-db` / `--skip-sdk`, or delete `probe/` now that the logs are summarized?
```

### Agent 写入的 answer.md

```markdown
# OPENHARMONY_CI 安装 date=20261102：执行记录与请求语义

## 0. 直接回答

- **安装成功**。`runtime/` 里已经有 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js/` + `interface/sdk_c/`，状态文件 `runtime/.oskm-runtime.json` 记为 `version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓`，`doctor` 退出 0，`validate-db` 返回 `{"ok": true}`。
- **实际请求语义**：`OPENHARMONY_CI` 下 `date` **不是 URL 的一部分**，它被展开成"一整天"的时间窗写进 POST body（`startTime`/`endTime`），组件名硬编码为 `dayu600_7885_ai`；真正的归档地址来自响应里的 `data.list.dataList[0].obsPath`，再 `urljoin` 到端点的 origin。整次安装**只有两个 HTTP 请求**：一次 POST 查列表，一次 GET 下归档。
- **它不是"精确日期等值查询"**，而是"当天 00:00:00–23:59:59 的成功构建列表，取第 0 条"。客户端**不回验**返回的构建是否真属于 20261102；日期是否准，完全取决于服务端是否老实按窗口过滤。下面的夹具实测证明了这一点。

## 1. 执行过的关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12

# 安装前体检（CLI/DB 都还没有，按设计退出 1）
$PY tool/bootstrap.py doctor

# 正式安装（OSKM_DOWNLOAD_SOURCE / OSKM_DOWNLOAD_ENDPOINT / OSKM_RUNTIME_ROOT 已在环境里）
$PY tool/bootstrap.py install --date 20261102

# 安装后体检 + schema 契约校验 + 用装好的 CLI 查一次
$PY tool/bootstrap.py doctor
$PY tool/bootstrap.py validate-db runtime/knowledge.db
$PY runtime/oskm-cli.pyz --version
$PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview

# 幂等性：同日期 refresh 不联网
$PY tool/bootstrap.py refresh --date 20261102

# 语义取证：抓真实 HTTP 请求 / 打错误分支（脚本见 probe/）
$PY probe/trace_requests.py probe      # 日志 probe/trace-20261102.log
$PY probe/probe_error_paths.py         # 日志 probe/error-paths.log
```

## 2. 关键输出片段

安装（stderr）：

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
EXIT=0
```

落盘结果（`find runtime`）与状态：

```
ru
… [输出截断，完整内容见工作区] …
nharmony/api/daily_build/build/list/component. ...
output file written? False
```

- 失败时**不写任何目标文件**，已有运行时也不受影响（临时目录 + 原子替换 + 回滚）。
- `--date` 格式先校：`install --date 2026-11-02` → `错误: --date 必须是 YYYYMMDD: 2026-11-02`，退出 1，**一个请求都不发**。
- `refresh --date 20261102` → `==> 运行时已是最新，无需刷新`，退出 0，不联网。
- `refresh` **不带** `--date` 会用 `today()`（当前 `20261117`）：只读验证 `state.needs_refresh(db, current_date='20261117') == True`，也就是它会按 20261117 重新下载并把 `state.date` 改写掉。想钉住 11-02 就必须显式带 `--date`（本次没有执行这个改写）。
- `install` 会先找本地源码树（cwd 及其祖先里有 `.gn` + `interface/sdk-js` + `interface/sdk_c` + `out` 就离线复用，可用 `--source-root` 指定）；本工作区没有，所以走了下载分支。

## 6. 产物与后续用法

```bash
# 查询一律直接调装好的 CLI（bootstrap.py 不管查询）
$PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
$PY runtime/oskm-cli.pyz --db runtime/knowledge.db ask --list
$PY runtime/oskm-cli.pyz --help
```

取证脚本与日志保留在 `probe/`：`trace_requests.py`（钩 `urlopen` 打真实请求）、`trace-20261102.log`、`probe_error_paths.py`、`error-paths.log`。未触碰 `~/.oskm`，未修改 `tool/` 与夹具。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**Done**
- Ran `install --date 20261102` against the fixture: `runtime/knowledge.db`, `runtime/oskm-cli.pyz`, `runtime/interface/sdk-js`, `runtime/interface/sdk_c` all landed; `runtime/.oskm-runtime.json` reads `version 3, date 20261102, source OPENHARMONY_CI, db=✓, sdk=✓, cli=✓`.
- `doctor` exits 0, `validate-db` returns `{"ok": true}`, and `oskm-cli.pyz --db runtime/knowledge.db arch overview` answers (`product: synthetic`, `scan_id: 1`).
- Write-up is in `answer.md`; trace scripts and logs are in `probe/`.

**Actual Request Semantics**
- Exactly two HTTP calls (traced by hooking `db_download.urlopen`, not hand-copied): `POST` to `OSKM_DOWNLOAD_ENDPOINT` verbatim, then `GET` on the returned `obsPath`.
- The date is a **day window in the POST body**, not a URL segment: `startTime="2026110200000000"` (16 digits), `endTime="20261102235959"` (14 digits) — asymmetric formats, both hard-coded at `tool/oskm_runtime/db_download.py:153`.
- Everything else is a constant: `component=dayu600_7885_ai` (`tool/oskm_runtime/environment.py:25`, not env-configurable), `projectName=openharmony`, `branch=master`, `type=1`, `buildStatus=success`, `pageNum=1/pageSize=10`, `withDomain=1`, empty sort fields.
- Artifact URL is `urljoin(endpoint, data.list.dataList[0].obsPath)` → `http://127.0.0.1:61808/openharmony/obs/20261102/knowledge.tar.gz`, fetched with `Accept: application/octet-stream`; filename must be a tar suffix.
- Contrast: `INTERNAL_CI` is `GET <endpoint>/<YYYYMMDD>` (exact addressing). Confirmed the fixture's list endpoint is POST-only — a real `GET` there returns 404.

**Date Fidelity Caveat**
- The client takes `dataList[0]` blindly and never re-checks the build's date; `state.date` is just the `--date` argument echoed by `install.build_state`, not read from the DB.
- Fixture probes show it keys only off `startTime`: a `20261101..20261103` window returns the 11-01 build, and `component`/`buildStatus`/`endTime` are ignored; with no time fields it serves `obs/unknown-date/...` at HTTP 200, which the client would install without complaint.
- All five dates serve byte-identical archives (`sha256 f1c8df96…`), so here the date only changes the URL path — the DB's `scans` row is fixed at `2026-11-02T00:00:00Z`.
- Failure paths verified in `probe/error-paths.log`: empty `dataList` → `该日期没有成功构建：20261102；响应缺少 obsPath`; non-JSON → `构建响应不是有效 JSON`; HTTP 404 fails fast while 408/429/5xx retry 3× at 2s with a 90s timeout; nothing is written on failure.

**Idempotency Note**
- `refresh --date 20261102` → `运行时已是最新，无需刷新` (no network). Bare `refresh` uses `today()` = `20261117`, and `state.needs_refresh` returns `True` — it would re-download and overwrite `state.date`, so keep `--date` explicit to stay pinned to 11-02. I did not run that.

Want me to also exercise `--skip-db` / `--skip-sdk`, or delete `probe/` now that the logs are summarized?stderr:
 cd ohprobe\\nfor d in 20261101 20261102 20261103 19990101 unknown-date; do\\n  curl -sS -o \\\"$d.tar.gz\\\" \\\"http://127.0.0.1:61808/openharmony/obs/$d/knowledge.tar.gz\\\"\\ndone\\nsha256sum *.tar.gz 2>/dev/null || shasum -a 256 *.tar.gz\\necho \\\"--- scans date inside each archive ---\\\"\\nfor d in 20261101 20261102 202…35 chars truncated… mkdir -p \\\"x$d\\\" && tar xzf \\\"$d.tar.gz\\\" -C \\\"x$d\\\" knowledge.db\\n  printf '\\\"'%-12s ' \\\\\\\"\\\"'$d\\\"\\n  /opt/homebrew/opt/python@3.12/bin/python3.12 -c \\\"\\nimport sqlite3,sys\\nc=sqlite3.connect('\\\"'x\\\"'$d/knowledge.db'\\\"')\\nprint(list(c.execute('select scan_id, started_at, finished_at from scans')))\\n\\\\\\\" 2>&1 | head -2\\ndone\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e02-openharmony-exact-date` · exit=0 · 711.4s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（4 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T16:20:08.362+08:00",
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
    "ts": "2026-11-17T16:20:08.362+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 21,
    "ts": "2026-11-17T16:23:55.597+08:00",
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
    "seq": 22,
    "ts": "2026-11-17T16:23:55.598+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  }
]
```

### agent 自己的探测请求（20 条）

```json
[
  {
    "seq": 3,
    "ts": "2026-11-17T16:20:40.474+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
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
    "ts": "2026-11-17T16:20:44.789+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
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
    "ts": "2026-11-17T16:20:44.802+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
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
    "seq": 6,
    "ts": "2026-11-17T16:20:44.811+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
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
    "seq": 7,
    "ts": "2026-11-17T16:21:25.560+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "2026110100000000",
      "endTime": "20261103235959",
      "buildStatus": "success",
      "withDomain": 1
    }
  },
  {
    "seq": 8,
    "ts": "2026-11-17T16:21:25.571+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "component": "dayu600_7885_ai",
      "type": 1,
      "buildStatus": "success",
      "withDomain": 1
    }
  },
  {
    "seq": 9,
    "ts": "2026-11-17T16:21:25.580+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "component": "rk3568",
      "type": 1,
      "startTime": "2026110200000000",
      "endTime": "20261102235959",
      "buildStatus": "success",
      "withDomain": 1
    }
  },
  {
    "seq": 10,
    "ts": "2026-11-17T16:21:25.588+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "2026110200000000",
      "endTime": "20261102235959",
      "buildStatus": "fail",
      "withDomain": 1
    }
  },
  {
    "seq": 11,
    "ts": "2026-11-17T16:21:25.595+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": {}
  },
  {
    "seq": 12,
    "ts": "2026-11-17T16:21:29.754+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 13,
    "ts": "2026-11-17T16:22:17.443+08:00",
    "method": "GET",
    "path": "/openharmony/obs/unknown-date/knowledge.tar.gz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 14,
    "ts": "2026-11-17T16:22:17.457+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "1999010100000000",
      "endTime": "19990101235959",
      "buildStatus": "success",
      "withDomain": 1
    }
  },
  {
    "seq": 15,
    "ts": "2026-11-17T16:22:17.466+08:00",
    "method": "GET",
    "path": "/openharmony/obs/19990101/knowledge.tar.gz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 16,
    "ts": "2026-11-17T16:22:37.994+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261101/knowledge.tar.gz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 17,
    "ts": "2026-11-17T16:22:38.005+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 18,
    "ts": "2026-11-17T16:22:38.013+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261103/knowledge.tar.gz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 19,
    "ts": "2026-11-17T16:22:38.021+08:00",
    "method": "GET",
    "path": "/openharmony/obs/19990101/knowledge.tar.gz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 20,
    "ts": "2026-11-17T16:22:38.029+08:00",
    "method": "GET",
    "path": "/openharmony/obs/unknown-date/knowledge.tar.gz",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 23,
    "ts": "2026-11-17T16:25:33.581+08:00",
    "method": "GET",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 24,
    "ts": "2026-11-17T16:25:33.590+08:00",
    "method": "GET",
    "path": "/openharmony/api/daily_build/build/list/component/20261102",
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
