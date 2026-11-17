# E3 internal-exact-date（with-skill 臂）

- 开始时间：2026-11-17T15:33:43+08:00
- 结束时间：2026-11-17T15:37:41+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e03-internal-exact-date`
- 夹具服务端：http://127.0.0.1:61145
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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e03-internal-exact-date --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：237.7 s
- 事件计数：`{"thread.started": 1, "item.completed": 51, "item:error": 1, "turn.started": 1, "item:reasoning": 15, "item:agent_message": 12, "item.started": 23, "item:command_execution": 46, "turn.completed": 1}`
- 读到 skill 文档：是（16 处）
- 执行的命令数：23
- token 用量：`{"input_tokens": 429806, "cached_input_tokens": 392832, "output_tokens": 6994, "reasoning_output_tokens": 2021}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'pwd && ls -la && echo "---SKILL ROOT---" && ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills'
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; find "$SK" -type f | sort && echo "---" && wc -l "$SK"/bootstrap.py "$SK"/references/usage.md 2>/dev/null'
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e03-internal-exact-date/PROMPT.md; echo "---EVENTS---"; cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e03-internal-exact-date/codex-events.jsonl'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; grep -rn "INTERNAL_CI" "$SK" | head -60'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; cat "$SK/bootstrap.py"; echo "=== .env.example ==="; cat "$SK/oskm_runtime/.env.example"'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '150,290p' \""'$SK/oskm_runtime/db_download.py"'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '180,300p' \""'$SK/references/usage.md"'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '1,120p' \""'$SK/oskm_runtime/environment.py"'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; grep -n \"add_argument\\|add_parser\\|def main\\|set_defaults\" \""'$SK/oskm_runtime/bootstrap.py" | head -80'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '100,290p' \""'$SK/oskm_runtime/bootstrap.py"'
$ /bin/zsh -lc 'env | grep -i oskm; echo "--- python ---"; /opt/homebrew/opt/python@3.12/bin/python3.12 -V; echo "--- runtime dir ---"; ls -la runtime; echo "--- fixtures? ---"; ls -la .. | head'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; "$PY" "$SK/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"; echo "EXIT=$?"'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; "$PY" "$SK/bootstrap.py" install --source INTERNAL_CI --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd "$OSKM_RUNTIME_ROOT" && ls -la && echo "--- interface ---" && ls -la interface && du -sh interface/* && echo "--- state ---" && /opt/homebrew/opt/python@3.12/bin/python3.12 -m json.tool .oskm-runtime.json'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; "$PY" "$SK/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"; echo "DOCTOR_EXIT=$?"; echo "--- cli-path ---"; "$PY" "$SK/bootstrap.py" cli-path --runtime-root "$OSKM_RUNTIME_ROOT"; echo "CLIPATH_EXIT=$?"'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; grep -n "''^def '"\\|"'^    def " "$SK/oskm_runtime/environment.py" | sed -n '"'1,40p'; echo \"--- download_config / endpoint ---\"; sed -n '120,200p' \""'$SK/oskm_runtime/environment.py"'
$ /bin/zsh -lc 'CLI="$OSKM_RUNTIME_ROOT/oskm-cli.pyz"; DB="$OSKM_RUNTIME_ROOT/knowledge.db"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; "$PY" "$CLI" --version; "$PY" "$CLI" --db "$DB" ask get_scan_info; echo "EXIT=$?"'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; "$PY" - "$SK" <<'"'PY'
import sys
sys.path.insert(0, sys.argv[1])
from oskm_runtime.environment import download_config
cfg = download_config()
date = '20261102'
print('source   =', cfg.source)
print('endpoint =', cfg.endpoint)
print('URL      =', f'{cfg.endpoint}/{date}' if cfg.source == 'INTERNAL_CI' else 'n/a (POST + obsPath)')
PY"
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; grep -n \"download_archive\\|_fetch(\\|def install_runtime\\|extract_runtime\\|sdk\" \""'$SK/oskm_runtime/install.py" | head -40; echo "=== db_download fetch/_open ==="; sed -n '"'1,60p' \""'$SK/oskm_runtime/db_download.py"'
$ /bin/zsh -lc 'cd "$OSKM_RUNTIME_ROOT" && find interface -type f | sort && echo "--- sizes ---" && ls -l knowledge.db oskm-cli.pyz && sha256sum knowledge.db oskm-cli.pyz 2>/dev/null || shasum -a 256 knowledge.db oskm-cli.pyz'
$ /bin/zsh -lc "cat > answer.md <<'EOF'
# INTERNAL_CI 下载 date=20261102 运行时

## 直接回答：URL

"'```
GET http://127.0.0.1:61145/internal/20261102
```

- 拼接规则：`$OSKM_DOWNLOAD_ENDPOINT/$date`（`INTERNAL_CI` 分支），即
  `http://127.0.0.1:61145/internal` + `/` + `20261102`。
- 是**一次 GET**，直接返回唯一发布单元 `knowledge.tar.gz`；不先 POST 查构建列表、
  不读 `obsPath`（那是 `OPENHARMONY_CI` 的流程，component 固定 `dayu600_7885_ai`），
  也不使用旧的 `latest` 端点。
- endpoint 末尾若带 `/` 会被先 strip 掉（`_endpoint()` 里 `rstrip('"'/')"'`），所以不会
  出现 `//20261102`；URL 必须是 http(s) 且有 netloc，否则联网前就报错。
- 归档内含 4 件产物（`knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` +
  `interface/sdk_c`），CLI 没有单独的下载端点。

代码依据（skill 内部实现）：
`oskm_runtime/db_download.py:209`（`if config.source == INTERNAL_CI: url = f'"'{config.endpoint}/{date}'"'`）、
`oskm_runtime/environment.py:126`（endpoint 规范化）。
文档依据：`references/usage.md:205`、`oskm_runtime/.env.example:10`。

## 执行的关键命令

```bash
SK="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
PY=/opt/homebrew/opt/python@3.12/bin/python3.12

# 1) 先看运行时是否就绪（skill §3.1 的顺序）
"$PY" "$SK/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"

# 2) 按 INTERNAL_CI + 指定日期安装（DB + 两套 SDK + CLI 一次装齐）
"$PY" "$SK/bootstrap.py" install --source INTERNAL_CI '"\\
    --runtime-root \""'$OSKM_RUNTIME_ROOT" --date 20261102

# 3) 复核：doctor / cli-path / 快照信息
"$PY" "$SK/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"
"$PY" "$SK/bootstrap.py" cli-path --runtime-root "$OSKM_RUNTIME_ROOT"
"$PY" "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask get_scan_info
```

环境变量已就位，未做任何修改：`OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`、
`OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61145/internal`、
`OSKM_RUNTIME_ROOT=…/e03-internal-exact-date/runtime`。未传 `--source-root`，
cwd 也不在 OpenHarmony 源码树内，因此本地构建探测未命中，直接走下载流程。
未访问、未修改 `~/.oskm`。

## 关键输出片段

安装前 doctor（运行时为空，符合预期）：

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。…
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。          # exit 1
```

install：

```
==> 下载 INTERNAL_CI 运行时: 20261102
==> 运行时安装完成: /var/folders/…/e03-internal-exact-date/runtime
                                        # exit 0
```

安装后 doctor / cli-path：

```
CLI: /var/folders/…/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
                                        # exit 0
```

`ask get_scan_info`（证明下载到的确实是 20261102 那一份快照）：

```json
{ "scan_id": 1, "product": "synthetic", "cpu_arch": "arm64",
  "status": "complete", "started_at": "2026-11-02T00:00:00Z",
  "finished_at": "2026-11-02T00:00:01Z",
  "collectors": [ … 11 个采集器全部 status=complete, record_count=1 … ] }
```

## 落盘结果

`$OSKM_RUNTIME_ROOT`（`…/e03-internal-exact-date/runtime`）：

```
.oskm-runtime.json          version 3, source INTERNAL_CI, date 20261102
knowledge.db                434176 B  sha256 f561e39f…fcd1b44
oskm-cli.pyz                 83741 B  sha256 ad760c16…d5eb49e
interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
interface/sdk_c/evalmarker.h
```

`.oskm-runtime.json` 的 `db` / `sdk` / `cli` 三段都记为 `date: 20261102`，
sha256 与实测一致；两套 SDK 目录非空（没有触发 `SDK 源码缺失`）。

## 备注

- 省略 `--date` 时安装器会取本地时区的系统当天（今天是 2026-11-17），
  要历史快照必须显式传 `YYYYMMDD`——本次按要求显式传了 `20261102`。
- 查询路径不会自动联网；要换日期需显式再跑 `install` 或 `refresh`。
EOF
echo "written"; wc -l answer.md'
$ /bin/zsh -lc 'ls -la && head -12 answer.md'
```

### Agent 最终回答

```markdown
**结果**
- 已真跑通：`GET http://127.0.0.1:61145/internal/20261102` 一次请求拿到 `knowledge.tar.gz`，4 件产物装入 `runtime/`。
- URL 规则就是 `$OSKM_DOWNLOAD_ENDPOINT/$date`（endpoint 末尾 `/` 会被 strip）；INTERNAL_CI 不走 POST + `obsPath`，也不用 `latest`。实现见 `oskm_runtime/db_download.py:209` 与 `oskm_runtime/environment.py:126`，文档见 `references/usage.md:205`。

**执行与校验**
- `bootstrap.py doctor` → 安装前 exit 1（运行时为空，CLI/DB 缺失，符合预期）。
- `bootstrap.py install --source INTERNAL_CI --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102` → `==> 下载 INTERNAL_CI 运行时: 20261102`，exit 0。
- 安装后 `doctor` → `Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`；`cli-path` → `runtime/oskm-cli.pyz`（oskm-cli 1.0.0）。
- `oskm-cli.pyz --db … ask get_scan_info` → `status: complete`、`started_at: 2026-11-02T00:00:00Z`，11 个采集器全部 complete，证明拿到的正是该日期快照。
- 落盘：`knowledge.db`（sha256 `f561e39f…`）、`oskm-cli.pyz`（`ad760c16…`）、`interface/sdk-js`、`interface/sdk_c` 均非空；`.oskm-runtime.json` 三段日期都是 20261102。

**边界**
- 只用了工作区 `runtime/` 与 skill 目录；未访问/修改 `~/.oskm`，未传 `--source-root`，未反查宿主进程。

结论已写入 answer.md（含命令、输出片段与 URL 说明）。需要的话我可以顺手用这个库跑一条 `arch overview` 验证查询链路。
```

### Agent 写入的 answer.md

```markdown
# INTERNAL_CI 下载 date=20261102 运行时

## 直接回答：URL

```
GET http://127.0.0.1:61145/internal/20261102
```

- 拼接规则：`$OSKM_DOWNLOAD_ENDPOINT/$date`（`INTERNAL_CI` 分支），即
  `http://127.0.0.1:61145/internal` + `/` + `20261102`。
- 是**一次 GET**，直接返回唯一发布单元 `knowledge.tar.gz`；不先 POST 查构建列表、
  不读 `obsPath`（那是 `OPENHARMONY_CI` 的流程，component 固定 `dayu600_7885_ai`），
  也不使用旧的 `latest` 端点。
- endpoint 末尾若带 `/` 会被先 strip 掉（`_endpoint()` 里 `rstrip('/')`），所以不会
  出现 `//20261102`；URL 必须是 http(s) 且有 netloc，否则联网前就报错。
- 归档内含 4 件产物（`knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` +
  `interface/sdk_c`），CLI 没有单独的下载端点。

代码依据（skill 内部实现）：
`oskm_runtime/db_download.py:209`（`if config.source == INTERNAL_CI: url = f'{config.endpoint}/{date}'`）、
`oskm_runtime/environment.py:126`（endpoint 规范化）。
文档依据：`references/usage.md:205`、`oskm_runtime/.env.example:10`。

## 执行的关键命令

```bash
SK="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
PY=/opt/homebrew/opt/python@3.12/bin/python3.12

# 1) 先看运行时是否就绪（skill §3.1 的顺序）
"$PY" "$SK/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"

# 2) 按 INTERNAL_CI + 指定日期安装（DB + 两套 SDK + CLI 一次装齐）
"$PY" "$SK/bootstrap.py" install --source INTERNAL_CI \
    --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102

# 3) 复核：doctor / cli-path / 快照信息
"$PY" "$SK/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"
"$PY" "$SK/bootstrap.py" cli-path --runtime-root "$OSKM_RUNTIME_ROOT"
"$PY" "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask get_scan_info
```

环境变量已就位，未做任何修改：`OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`、
`OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61145/internal`、
`OSKM_RUNTIME_ROOT=…/e03-internal-exact-date/runtime`。未传 `--source-root`，
cwd 也不在 OpenHarmony 源码树内，因此本地构建探测未命中，直接走下载流程。
未访问、未修改 `~/.oskm`。

## 关键输出片段

安装前 doctor（运行时为空，符合预期）：

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。…
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。          # exit 1
```

install：

```
==> 下载 INTERNAL_CI 运行时: 20261102
==> 运行时安装完成: /var/folders/…/e03-internal-exact-date/runtime
                                        # exit 0
```

安装后 doctor / cli-path：

```
CLI: /var/folders/…/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
                                        # exit 0
```

`ask get_scan_info`（证明下载到的确实是 20261102 那一份快照）：

```json
{ "scan_id": 1, "product": "synthetic", "cpu_arch": "arm64",
  "status": "complete", "started_at": "2026-11-02T00:00:00Z",
  "finished_at": "2026-11-02T00:00:01Z",
  "collectors": [ … 11 个采集器全部 status=complete, record_count=1 … ] }
```

## 落盘结果

`$OSKM_RUNTIME_ROOT`（`…/e03-internal-exact-date/runtime`）：

```
.oskm-runtime.json          version 3, source INTERNAL_CI, date 20261102
knowledge.db                434176 B  sha256 f561e39f…fcd1b44
oskm-cli.pyz                 83741 B  sha256 ad760c16…d5eb49e
interface/sdk-js/api/@internal/ohos.evalmarker.d.ts
interface/sdk_c/evalmarker.h
```

`.oskm-runtime.json` 的 `db` / `sdk` / `cli` 三段都记为 `date: 20261102`，
sha256 与实测一致；两套 SDK 目录非空（没有触发 `SDK 源码缺失`）。

## 备注

- 省略 `--date` 时安装器会取本地时区的系统当天（今天是 2026-11-17），
  要历史快照必须显式传 `YYYYMMDD`——本次按要求显式传了 `20261102`。
- 查询路径不会自动联网；要换日期需显式再跑 `install` 或 `refresh`。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结果**
- 已真跑通：`GET http://127.0.0.1:61145/internal/20261102` 一次请求拿到 `knowledge.tar.gz`，4 件产物装入 `runtime/`。
- URL 规则就是 `$OSKM_DOWNLOAD_ENDPOINT/$date`（endpoint 末尾 `/` 会被 strip）；INTERNAL_CI 不走 POST + `obsPath`，也不用 `latest`。实现见 `oskm_runtime/db_download.py:209` 与 `oskm_runtime/environment.py:126`，文档见 `references/usage.md:205`。

**执行与校验**
- `bootstrap.py doctor` → 安装前 exit 1（运行时为空，CLI/DB 缺失，符合预期）。
- `bootstrap.py install --source INTERNAL_CI --runtime-root "$OSKM_RUNTIME_ROOT" --date 20261102` → `==> 下载 INTERNAL_CI 运行时: 20261102`，exit 0。
- 安装后 `doctor` → `Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`；`cli-path` → `runtime/oskm-cli.pyz`（oskm-cli 1.0.0）。
- `oskm-cli.pyz --db … ask get_scan_info` → `status: complete`、`started_at: 2026-11-02T00:00:00Z`，11 个采集器全部 complete，证明拿到的正是该日期快照。
- 落盘：`knowledge.db`（sha256 `f561e39f…`）、`oskm-cli.pyz`（`ad760c16…`）、`interface/sdk-js`、`interface/sdk_c` 均非空；`.oskm-runtime.json` 三段日期都是 20261102。

**边界**
- 只用了工作区 `runtime/` 与 skill 目录；未访问/修改 `~/.oskm`，未传 `--source-root`，未反查宿主进程。

结论已写入 answer.md（含命令、输出片段与 URL 说明）。需要的话我可以顺手用这个库跑一条 `arch overview` 验证查询链路。
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e03-internal-exact-date` · exit=0 · 237.7s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T15:35:10.827+08:00",
    "method": "GET",
    "path": "/internal/20261102",
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
