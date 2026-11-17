# E3 internal-exact-date（with-skill 臂）

- 开始时间：2026-11-17T16:18:33+08:00
- 结束时间：2026-11-17T16:21:41+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date`
- 夹具服务端：http://127.0.0.1:61812
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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：187.5 s
- 事件计数：`{"thread.started": 1, "item.completed": 40, "item:error": 1, "turn.started": 1, "item:reasoning": 11, "item:agent_message": 10, "item.started": 18, "item:command_execution": 36, "turn.completed": 1}`
- 读到 skill 文档：是（12 处）
- 执行的命令数：18
- token 用量：`{"input_tokens": 221557, "cached_input_tokens": 198272, "output_tokens": 6380, "reasoning_output_tokens": 1177}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date; echo "---"; ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date/runtime 2>/dev/null; echo "--- env"; env | grep -i oskm'
$ /bin/zsh -lc 'cat "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date && cat PROMPT.md; echo "=== skill dir ==="; ls -la "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/"'
$ /bin/zsh -lc 'cd "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/" && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py --help 2>&1 | head -60'
$ /bin/zsh -lc 'cd "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/" && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py doctor 2>&1 | tail -40'
$ /bin/zsh -lc 'cd "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/" && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py install --help 2>&1 | head -40; echo "=== runtime pkg ==="; ls oskm_runtime'
$ /bin/zsh -lc 'cd "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/" && AGENT_CWD="/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date" && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py install --source INTERNAL_CI --date 20261102 2>&1 | tail -40'
$ /bin/zsh -lc 'cd "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/" && sed -n 1,200p oskm_runtime/db_download.py'
$ /bin/zsh -lc 'cd "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/" && sed -n 200,400p oskm_runtime/db_download.py'
$ /bin/zsh -lc "cd \"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/\" && grep -n \"INTERNAL_CI\\|ENDPOINT\\|endpoint\" oskm_runtime/environment.py | head -40"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date/runtime && ls -la && echo "=== tree top ===" && find . -maxdepth 2 | head -30 && echo "=== sizes ===" && du -sh knowledge.db oskm-cli.pyz interface 2>/dev/null && echo "=== state ===" && ls -a && cat .oskm-state.json 2>/dev/null || cat .state.json 2>/dev/null'
$ /bin/zsh -lc 'cd "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/" && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py doctor 2>&1 | tail -20; echo "=== cli-path ==="; /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py cli-path 2>&1 | tail -5'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date/runtime && cat .oskm-runtime.json; echo; echo "=== HEAD exact URL ==="; curl -sS -D - -o /dev/null "http://127.0.0.1:61812/internal/20261102" 2>&1 | head -12'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date/runtime && /opt/homebrew/opt/python@3.12/bin/python3.12 oskm-cli.pyz --version; /opt/homebrew/opt/python@3.12/bin/python3.12 oskm-cli.pyz --db knowledge.db ask get_scan_info 2>&1 | head -40'
$ /bin/zsh -lc "cd \"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/\" && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
from oskm_runtime.environment import download_config
c = download_config()
print('source   =', c.source)
print('endpoint =', c.endpoint)
print('URL      =', f'{c.endpoint}/20261102')
\""
$ /bin/zsh -lc "cd \"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/\" && OSKM_DOWNLOAD_ENDPOINT=\"http://127.0.0.1:61812/internal/\" /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
from oskm_runtime.environment import download_config
c = download_config()
print('trailing-slash endpoint ->', f'{c.endpoint}/20261102')
\"; echo \"=== refresh (idempotent check, no re-download expected) ===\"; /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py refresh --source INTERNAL_CI --date 20261102 2>&1 | tail -5"
$ /bin/zsh -lc "cat > /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date/answer.md <<'EOF'
# INTERNAL_CI 下载 date=20261102 运行时

## 直接回答：URL 是什么

"'```
http://127.0.0.1:61812/internal/20261102
```

构成方式（`INTERNAL_CI` 分支，见 `oskm_runtime/db_download.py` 的 `_download_archive`）：

```python
if config.source == INTERNAL_CI:
    url = f'"'{config.endpoint}/{date}'
    archive = work_dir / 'knowledge.tar.gz'
"'```

- `config.endpoint` 来自 `OSKM_DOWNLOAD_ENDPOINT`，读取时做 `strip().rstrip('"'/')"'`（`oskm_runtime/environment.py:126`），
  所以 `http://127.0.0.1:61812/internal` 与 `http://127.0.0.1:61812/internal/` 拼出同一个 URL。
- `{date}` 是 `--date` 传入的 `YYYYMMDD`（缺省取系统当天；本次显式给 `20261102`），
  由 `validate_date()` 校验为 8 位数字且是合法日期。
- 请求方法 `GET`，头 `Accept: application/octet-stream`；响应落盘为 `knowledge.tar.gz`，
  再按运行时归档规则解出 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`。
- 对比：`OPENHARMONY_CI` 不是这种直接拼 URL，而是先 POST 构建查询接口拿 `obsPath` 再 `urljoin`。

## 执行的关键命令

1) 安装前体检（运行时为空，CLI 缺失）：

```bash
SKILL_DIR=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
cd "$SKILL_DIR" && "$PY" bootstrap.py doctor
```

```
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
CLI: FAIL: 找不到可用的 oskm-cli 产物。…
错误: 运行时依赖检查未通过。
```

2) 按 INTERNAL_CI + 指定日期安装（`--runtime-root` 默认取 `OSKM_RUNTIME_ROOT`）：

```bash
cd "$SKILL_DIR" && "$PY" bootstrap.py install --source INTERNAL_CI --date 20261102
```

```
==> 下载 INTERNAL_CI 运行时: 20261102
==> 运行时安装完成: …/e03-internal-exact-date/runtime
```

3) 安装后体检 + CLI 定位：

```bash
cd "$SKILL_DIR" && "$PY" bootstrap.py doctor
cd "$SKILL_DIR" && "$PY" bootstrap.py cli-path
```

```
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
…/runtime/oskm-cli.pyz
```

4) 直接对夹具服务验证 URL 本身可达（只发 HEAD，不重复落盘）：

```bash
curl -sS -D - -o /dev/null "http://127.0.0.1:61812/internal/20261102"
```

```
HTTP/1.1 200 OK
Server: oskm-eval-fixture/1.0 Python/3.12.16
Content-Type: application/gzip
Content-Length: 94326
```

5) 从代码侧复算 URL（无网络），并验证尾斜杠归一化：

```bash
cd "$SKILL_DIR" && "$PY" -c "
from oskm_runtime.environment import download_config
c = download_config(); print('"'URL =', f'{c.endpoint}/20261102')\"
OSKM_DOWNLOAD_ENDPOINT=\"http://127.0.0.1:61812/internal/\" \""'$PY" -c "…同上…"
```

```
source   = INTERNAL_CI
endpoint = http://127.0.0.1:61812/internal
URL      = http://127.0.0.1:61812/internal/20261102
trailing-slash endpoint -> http://127.0.0.1:61812/internal/20261102
```

6) 幂等性：`refresh` 不重复下载。

```bash
cd "$SKILL_DIR" && "$PY" bootstrap.py refresh --source INTERNAL_CI --date 20261102
```

```
==> 运行时已是最新，无需刷新: …/e03-internal-exact-date/runtime
```

7) 装好的 CLI 能真查（顺带确认快照日期就是 2026-11-02）：

```bash
cd "$OSKM_RUNTIME_ROOT" && "$PY" oskm-cli.pyz --version
cd "$OSKM_RUNTIME_ROOT" && "$PY" oskm-cli.pyz --db knowledge.db ask get_scan_info
```

```
oskm-cli 1.0.0
{ "scan_id": 1, "product": "synthetic", "cpu_arch": "arm64", "status": "complete",
  "started_at": "2026-11-02T00:00:00Z", "finished_at": "2026-11-02T00:00:01Z", … }
```

## 落地结果

`OSKM_RUNTIME_ROOT=…/e03-internal-exact-date/runtime` 内容：

```
knowledge.db        434176 bytes   sha256 f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44
oskm-cli.pyz         84742 bytes   sha256 3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5
interface/sdk-js/    interface/sdk_c/
.oskm-runtime.json   version 3, source INTERNAL_CI, date 20261102
```

单个 `knowledge.tar.gz` 是唯一发布单元，DB / 两套 SDK / CLI 一次装齐；CLI 不单独下载。
未触碰 `~/.oskm`，未修改 fixtures。
EOF
echo "written:"; wc -l /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date/answer.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date && ls -la && echo "=== ~/.oskm untouched? ===" && ls -la "$HOME/.oskm" 2>&1 | head -5'
```

### Agent 最终回答

```markdown
装好了，URL 是 `http://127.0.0.1:61812/internal/20261102`。

**URL 怎么来的**
- `INTERNAL_CI` 分支就是端点直接拼日期：`url = f'{config.endpoint}/{date}'`（`oskm_runtime/db_download.py`），落盘名固定 `knowledge.tar.gz`。
- `config.endpoint` 取 `OSKM_DOWNLOAD_ENDPOINT` 并做 `strip().rstrip('/')`（`oskm_runtime/environment.py:126`），所以带不带尾斜杠拼出同一 URL；`{date}` 由 `validate_date()` 校验成 8 位 `YYYYMMDD`。
- `GET` + `Accept: application/octet-stream`；对比 `OPENHARMONY_CI` 是先 POST 构建查询拿 `obsPath` 再 `urljoin`，不是这种直拼。

**执行与关键输出**
- `bootstrap.py doctor`（装前）：`Runtime state: 未安装（没有 knowledge.db）`、`CLI: FAIL`。
- `bootstrap.py install --source INTERNAL_CI --date 20261102`：`==> 下载 INTERNAL_CI 运行时: 20261102` → `==> 运行时安装完成: …/e03-internal-exact-date/runtime`。
- `doctor`（装后）：`CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)`、`Modules: 全部 OK`、`Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`。
- `curl -D - -o /dev/null http://127.0.0.1:61812/internal/20261102`：`HTTP/1.1 200 OK`、`Content-Type: application/gzip`、`Content-Length: 94326`。
- `refresh` 复跑：`运行时已是最新，无需刷新`（幂等，不重复下载）。
- CLI 真查通过：`oskm-cli.pyz --db knowledge.db ask get_scan_info` 返回 `status: complete`、`started_at: 2026-11-02T00:00:00Z`，与请求日期一致。

**落地结果**
- `runtime/knowledge.db`（434176 B）、`runtime/oskm-cli.pyz`（84742 B）、`runtime/interface/sdk-js`、`runtime/interface/sdk_c`、`runtime/.oskm-runtime.json`（记录 source/date/sha256）。
- 全程未创建或修改 `~/.oskm`，未动 fixtures。

结论与命令、输出片段已写入 `answer.md`（工作目录根，131 行）。需要我接着跑一条 `arch overview` 看看这份快照的子系统/部件构成吗？
```

### Agent 写入的 answer.md

```markdown
# INTERNAL_CI 下载 date=20261102 运行时

## 直接回答：URL 是什么

```
http://127.0.0.1:61812/internal/20261102
```

构成方式（`INTERNAL_CI` 分支，见 `oskm_runtime/db_download.py` 的 `_download_archive`）：

```python
if config.source == INTERNAL_CI:
    url = f'{config.endpoint}/{date}'
    archive = work_dir / 'knowledge.tar.gz'
```

- `config.endpoint` 来自 `OSKM_DOWNLOAD_ENDPOINT`，读取时做 `strip().rstrip('/')`（`oskm_runtime/environment.py:126`），
  所以 `http://127.0.0.1:61812/internal` 与 `http://127.0.0.1:61812/internal/` 拼出同一个 URL。
- `{date}` 是 `--date` 传入的 `YYYYMMDD`（缺省取系统当天；本次显式给 `20261102`），
  由 `validate_date()` 校验为 8 位数字且是合法日期。
- 请求方法 `GET`，头 `Accept: application/octet-stream`；响应落盘为 `knowledge.tar.gz`，
  再按运行时归档规则解出 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`。
- 对比：`OPENHARMONY_CI` 不是这种直接拼 URL，而是先 POST 构建查询接口拿 `obsPath` 再 `urljoin`。

## 执行的关键命令

1) 安装前体检（运行时为空，CLI 缺失）：

```bash
SKILL_DIR=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
cd "$SKILL_DIR" && "$PY" bootstrap.py doctor
```

```
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
CLI: FAIL: 找不到可用的 oskm-cli 产物。…
错误: 运行时依赖检查未通过。
```

2) 按 INTERNAL_CI + 指定日期安装（`--runtime-root` 默认取 `OSKM_RUNTIME_ROOT`）：

```bash
cd "$SKILL_DIR" && "$PY" bootstrap.py install --source INTERNAL_CI --date 20261102
```

```
==> 下载 INTERNAL_CI 运行时: 20261102
==> 运行时安装完成: …/e03-internal-exact-date/runtime
```

3) 安装后体检 + CLI 定位：

```bash
cd "$SKILL_DIR" && "$PY" bootstrap.py doctor
cd "$SKILL_DIR" && "$PY" bootstrap.py cli-path
```

```
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
…/runtime/oskm-cli.pyz
```

4) 直接对夹具服务验证 URL 本身可达（只发 HEAD，不重复落盘）：

```bash
curl -sS -D - -o /dev/null "http://127.0.0.1:61812/internal/20261102"
```

```
HTTP/1.1 200 OK
Server: oskm-eval-fixture/1.0 Python/3.12.16
Content-Type: application/gzip
Content-Length: 94326
```

5) 从代码侧复算 URL（无网络），并验证尾斜杠归一化：

```bash
cd "$SKILL_DIR" && "$PY" -c "
from oskm_runtime.environment import download_config
c = download_config(); print('URL =', f'{c.endpoint}/20261102')"
OSKM_DOWNLOAD_ENDPOINT="http://127.0.0.1:61812/internal/" "$PY" -c "…同上…"
```

```
source   = INTERNAL_CI
endpoint = http://127.0.0.1:61812/internal
URL      = http://127.0.0.1:61812/internal/20261102
trailing-slash endpoint -> http://127.0.0.1:61812/internal/20261102
```

6) 幂等性：`refresh` 不重复下载。

```bash
cd "$SKILL_DIR" && "$PY" bootstrap.py refresh --source INTERNAL_CI --date 20261102
```

```
==> 运行时已是最新，无需刷新: …/e03-internal-exact-date/runtime
```

7) 装好的 CLI 能真查（顺带确认快照日期就是 2026-11-02）：

```bash
cd "$OSKM_RUNTIME_ROOT" && "$PY" oskm-cli.pyz --version
cd "$OSKM_RUNTIME_ROOT" && "$PY" oskm-cli.pyz --db knowledge.db ask get_scan_info
```

```
oskm-cli 1.0.0
{ "scan_id": 1, "product": "synthetic", "cpu_arch": "arm64", "status": "complete",
  "started_at": "2026-11-02T00:00:00Z", "finished_at": "2026-11-02T00:00:01Z", … }
```

## 落地结果

`OSKM_RUNTIME_ROOT=…/e03-internal-exact-date/runtime` 内容：

```
knowledge.db        434176 bytes   sha256 f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44
oskm-cli.pyz         84742 bytes   sha256 3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5
interface/sdk-js/    interface/sdk_c/
.oskm-runtime.json   version 3, source INTERNAL_CI, date 20261102
```

单个 `knowledge.tar.gz` 是唯一发布单元，DB / 两套 SDK / CLI 一次装齐；CLI 不单独下载。
未触碰 `~/.oskm`，未修改 fixtures。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
装好了，URL 是 `http://127.0.0.1:61812/internal/20261102`。

**URL 怎么来的**
- `INTERNAL_CI` 分支就是端点直接拼日期：`url = f'{config.endpoint}/{date}'`（`oskm_runtime/db_download.py`），落盘名固定 `knowledge.tar.gz`。
- `config.endpoint` 取 `OSKM_DOWNLOAD_ENDPOINT` 并做 `strip().rstrip('/')`（`oskm_runtime/environment.py:126`），所以带不带尾斜杠拼出同一 URL；`{date}` 由 `validate_date()` 校验成 8 位 `YYYYMMDD`。
- `GET` + `Accept: application/octet-stream`；对比 `OPENHARMONY_CI` 是先 POST 构建查询拿 `obsPath` 再 `urljoin`，不是这种直拼。

**执行与关键输出**
- `bootstrap.py doctor`（装前）：`Runtime state: 未安装（没有 knowledge.db）`、`CLI: FAIL`。
- `bootstrap.py install --source INTERNAL_CI --date 20261102`：`==> 下载 INTERNAL_CI 运行时: 20261102` → `==> 运行时安装完成: …/e03-internal-exact-date/runtime`。
- `doctor`（装后）：`CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)`、`Modules: 全部 OK`、`Runtime state: version 3, date 20261102, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`。
- `curl -D - -o /dev/null http://127.0.0.1:61812/internal/20261102`：`HTTP/1.1 200 OK`、`Content-Type: application/gzip`、`Content-Length: 94326`。
- `refresh` 复跑：`运行时已是最新，无需刷新`（幂等，不重复下载）。
- CLI 真查通过：`oskm-cli.pyz --db knowledge.db ask get_scan_info` 返回 `status: complete`、`started_at: 2026-11-02T00:00:00Z`，与请求日期一致。

**落地结果**
- `runtime/knowledge.db`（434176 B）、`runtime/oskm-cli.pyz`（84742 B）、`runtime/interface/sdk-js`、`runtime/interface/sdk_c`、`runtime/.oskm-runtime.json`（记录 source/date/sha256）。
- 全程未创建或修改 `~/.oskm`，未动 fixtures。

结论与命令、输出片段已写入 `answer.md`（工作目录根，131 行）。需要我接着跑一条 `arch overview` 看看这份快照的子系统/部件构成吗？
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e03-internal-exact-date` · exit=0 · 187.5s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T16:19:14.898+08:00",
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
    "ts": "2026-11-17T16:20:01.345+08:00",
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
