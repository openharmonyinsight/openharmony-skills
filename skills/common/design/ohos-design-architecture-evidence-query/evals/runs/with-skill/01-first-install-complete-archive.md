# E1 first-install-complete-archive（with-skill 臂）

- 开始时间：2026-11-17T15:33:43+08:00
- 结束时间：2026-11-17T15:37:03+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive`
- 夹具服务端：http://127.0.0.1:61146
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

运行根目录为空，测试夹具已提供一个本地 knowledge.tar.gz，内含 knowledge.db、oskm-cli.pyz、interface/sdk-js 和 interface/sdk_c。请从任意 Agent 启动目录安装该 skill 的托管运行时，并报告安装后的布局、状态与当前工作目录。

## 期望结果（来自 evals.json）

使用绝对路径调用 bootstrap.py install，把 knowledge.db、oskm-cli.pyz、interface/sdk-js 和 interface/sdk_c 一次装到同一个 runtime root；状态文件包含 db、sdk、cli 三段，不需要单独的 CLI 下载端点；安装完成后回到 Agent 启动目录。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| knowledge.db | `contains` |
| oskm-cli.pyz | `contains` |
| interface/sdk-js | `contains` |
| interface/sdk_c | `contains` |
| 四个产物位于同一 runtime root，未使用单独的 CLI 下载端点，且安装后当前目录等于 Agent 启动目录 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：200.2 s
- 事件计数：`{"thread.started": 1, "item.completed": 39, "item:error": 1, "turn.started": 1, "item:reasoning": 11, "item:agent_message": 11, "item.started": 16, "item:command_execution": 32, "turn.completed": 1}`
- 读到 skill 文档：是（9 处）
- 执行的命令数：16
- token 用量：`{"input_tokens": 214710, "cached_input_tokens": 191104, "output_tokens": 6385, "reasoning_output_tokens": 1557}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc 'pwd; echo "---"; env | grep -i oskm; echo "---"; ls -la'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; ls -la "$SK"; echo "=== refs ==="; ls -R "$SK/references" | head -60'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive && ls -la; echo "=== runtime ==="; ls -la runtime; echo "=== fixtures? ==="; ls -la .. | head -20'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; cat "$SK/bootstrap.py"; echo "=== runtime pkg ==="; ls -la "$SK/oskm_runtime"'
$ /bin/zsh -lc 'cat /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start/PROMPT.md'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; python3 --version; which python3; /opt/homebrew/opt/python@3.12/bin/python3.12 --version; echo "=== help ==="; python3 "$SK/bootstrap.py" --help; echo "=== install help ==="; python3 "$SK/bootstrap.py" install --help'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '1,140p' \""'$SK/references/usage.md"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && echo "AGENT_CWD=$PWD" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SK/bootstrap.py" doctor; echo "exit=$?"; echo "PWD after=$PWD"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && AGENT_CWD="$PWD" && echo "AGENT_CWD=$AGENT_CWD" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SK/bootstrap.py" install; echo "install exit=$?"; cd "$AGENT_CWD"; echo "PWD after install=$PWD"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "===== doctor ====="; $PY "$SK/bootstrap.py" doctor; echo "doctor exit=$?"; echo "===== cli-path ====="; $PY "$SK/bootstrap.py" cli-path; echo "cli-path exit=$?"; echo "===== PWD ====="; pwd'
$ /bin/zsh -lc 'RT=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/runtime; echo "===== top level ====="; ls -la "$RT"; echo "===== interface ====="; ls -la "$RT/interface"; echo "===== counts ====="; echo "sdk-js files: $(find "$RT/interface/sdk-js" -type f | wc -l)"; echo "sdk_c files: $(find "$RT/interface/sdk_c" -type f | wc -l)"; echo "total files: $(find "$RT" -type f | wc -l)"; echo "===== state file ====="; cat "$RT/.oskm-runtime.json"'
$ /bin/zsh -lc 'RT=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/runtime; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; echo "===== interface tree ====="; find "$RT/interface" | sed "s|$RT/||"; echo "===== cli --version ====="; $PY "$RT/oskm-cli.pyz" --version; echo "exit=$?"'
$ /bin/zsh -lc 'RT=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/runtime; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; echo "===== get_scan_info ====="; $PY "$RT/oskm-cli.pyz" --db "$RT/knowledge.db" ask get_scan_info; echo "exit=$?"; echo "===== ~/.oskm check ====="; ls -la "$HOME/.oskm" 2>&1 | head -5'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && AGENT_CWD="$PWD" && $PY "$SK/bootstrap.py" refresh; echo "refresh exit=$?"; cd "$AGENT_CWD"; echo "PWD=$PWD"'
$ /bin/zsh -lc "cat > /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start/answer.md <<'EOF'
# 安装 OpenHarmony 架构证据托管运行时（INTERNAL_CI · 20261117）

## 直接回答

- **安装成功**：一次 "'`bootstrap.py install` 就从 `OSKM_DOWNLOAD_ENDPOINT` 拉到完整
  `knowledge.tar.gz` 并装齐四样东西（`knowledge.db` + `oskm-cli.pyz` +
  `interface/sdk-js` + `interface/sdk_c`），退出码 0。
- **运行时根目录**：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/runtime`
  （由 `OSKM_RUNTIME_ROOT` 决定，**没有**用默认的 `~/.oskm`；`$HOME/.oskm` 至今不存在）。
- **状态**：`doctor` 全绿 —— Python 3.12.16、CLI installed（oskm-cli 1.0.0）、
  `oskm_runtime/oskm_cli/oskm_schema` 三个模块可导入、状态文件 version 3 /
  date 20261117 / source INTERNAL_CI / `db=✓ sdk=✓ cli=✓`、库可打开。
- **当前工作目录**：安装前后都是 Agent 启动目录
  `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start`。
  按 skill 的 `AGENT_CWD="$PWD" … cd "$AGENT_CWD"` 写法执行，安装不会把 cwd 带走。

## 关键命令

```bash
SK=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
PY=/opt/homebrew/opt/python@3.12/bin/python3.12      # 系统 python3 是 3.9.6，低于要求的 3.10+
cd .../e01-first-install-complete-archive/agent-start
AGENT_CWD="$PWD"
$PY "$SK/bootstrap.py" doctor                        # 安装前体检：CLI/DB 均缺失
$PY "$SK/bootstrap.py" install                       # 下载 + 解压 + 安装（--source/--date 取自环境与系统日期）
cd "$AGENT_CWD"                                      # 回到 Agent 启动目录
$PY "$SK/bootstrap.py" doctor                        # 安装后体检：全绿
$PY "$SK/bootstrap.py" cli-path                      # 确认实际 CLI 位置
$PY "$SK/bootstrap.py" refresh                       # 幂等性：已是最新，无需刷新
RT="$OSKM_RUNTIME_ROOT"
$PY "$RT/oskm-cli.pyz" --version
$PY "$RT/oskm-cli.pyz" --db "$RT/knowledge.db" ask get_scan_info
```

## 关键输出片段

安装前 `doctor`（缺 CLI、未安装）：

```text
CLI: FAIL: 找不到可用的 oskm-cli 产物。… 3. <runtime>/oskm-cli.pyz —— 不存在
Modules: oskm_runtime (OK), oskm_cli (FAIL: No module named '"'oskm_cli'), oskm_schema (FAIL: …)
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。            # exit=1
"'```

`install`：

```text
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: …/e01-first-install-complete-archive/runtime   # exit=0
```

安装后 `doctor`：

```text
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: …/runtime
Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）  # exit=0
```

`refresh`（幂等）与 CLI 自检：

```text
==> 运行时已是最新，无需刷新: …/runtime     # exit=0
oskm-cli 1.0.0
```

`ask get_scan_info` 摘要：`product=synthetic`、`cpu_arch=arm64`、`status=complete`，
11 个采集器（args/arkts/components/elf_modules/hdi/install_modules/links/native/repos/sas/services）
全部 `complete`，各 `record_count=1`。

## 安装后的布局

```text
<runtime-root>/                     # OSKM_RUNTIME_ROOT
├── .oskm-runtime.json              # 状态文件 version 3（535 B，权限 0600）
├── knowledge.db                    # 434176 B，sha256 f561e39f…d1b44
├── oskm-cli.pyz                    # 83741 B，可执行，sha256 ad760c16…b49e
└── interface/
    ├── sdk-js/api/@internal/ohos.evalmarker.d.ts
    └── sdk_c/evalmarker.h
```

要点：
- SDK 直接落在 `interface/sdk-js`、`interface/sdk_c`，**没有**多套一层
  `interface/interface/…`，与 DB 中 `source_path`/`header_path` 的相对解析规则一致。
- CLI 与 `knowledge.db` **并排**在运行时根目录，固定文件名、不带版本号；版本问
  `oskm-cli.pyz --version`（实测 1.0.0）。
- 状态文件 `cli`/`db` 段记的 `{path, sha256}` 是出处记录，不参与校验。
- 未创建 `.env`（可选文件）；`~/.oskm` 未被访问或修改。

## 后续查询入口

```bash
RT="$OSKM_RUNTIME_ROOT"
/opt/homebrew/opt/python@3.12/bin/python3.12 "$RT/oskm-cli.pyz" --db "$RT/knowledge.db" arch overview
```

注意：查询路径不会自动联网，数据过期时显式跑 `bootstrap.py refresh`。
EOF
echo "written:"; ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start'
```

### Agent 最终回答

```markdown
**Installed**
- Ran pre-install `doctor` → CLI/DB missing (exit 1), then `install` with `python3.12` (system `python3` is 3.9.6, below the 3.10+ floor), then `cd` back to the start dir.
- `install` output: `==> 下载 INTERNAL_CI 运行时: 20261117` / `==> 运行时安装完成: …/runtime`, exit 0 — one archive installed all four artifacts.
- `refresh` is a no-op afterwards (`运行时已是最新`), confirming idempotency.

**Layout** (`OSKM_RUNTIME_ROOT`, not `~/.oskm` — `$HOME/.oskm` still doesn't exist)
- `runtime/knowledge.db` (434176 B), `runtime/oskm-cli.pyz` (83741 B, executable) sitting side by side, `runtime/.oskm-runtime.json` (version 3, mode 0600).
- `runtime/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts` and `runtime/interface/sdk_c/evalmarker.h` — no doubled `interface/interface/` nesting.

**Status**
- `doctor` all green: Python 3.12.16 OK, `CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)`, modules `oskm_runtime/oskm_cli/oskm_schema` OK, `Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`, DB opens.
- `cli-path` resolves to `runtime/oskm-cli.pyz`; `oskm-cli.pyz --version` → `oskm-cli 1.0.0`.
- Smoke query `ask get_scan_info` → `product=synthetic`, `cpu_arch=arm64`, `status=complete`, 11 collectors all `complete` with `record_count=1`.

**Working Directory**
- Unchanged before/after install: `/var/folders/…/e01-first-install-complete-archive/agent-start` (kept via `AGENT_CWD="$PWD" … cd "$AGENT_CWD"`).

Write-up with commands and output snippets is in `answer.md` (agent-start dir). Next logical step if you want it: run an actual architecture query, e.g. `python3.12 "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview`.
```

### Agent 写入的 answer.md

```markdown
# 安装 OpenHarmony 架构证据托管运行时（INTERNAL_CI · 20261117）

## 直接回答

- **安装成功**：一次 `bootstrap.py install` 就从 `OSKM_DOWNLOAD_ENDPOINT` 拉到完整
  `knowledge.tar.gz` 并装齐四样东西（`knowledge.db` + `oskm-cli.pyz` +
  `interface/sdk-js` + `interface/sdk_c`），退出码 0。
- **运行时根目录**：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/runtime`
  （由 `OSKM_RUNTIME_ROOT` 决定，**没有**用默认的 `~/.oskm`；`$HOME/.oskm` 至今不存在）。
- **状态**：`doctor` 全绿 —— Python 3.12.16、CLI installed（oskm-cli 1.0.0）、
  `oskm_runtime/oskm_cli/oskm_schema` 三个模块可导入、状态文件 version 3 /
  date 20261117 / source INTERNAL_CI / `db=✓ sdk=✓ cli=✓`、库可打开。
- **当前工作目录**：安装前后都是 Agent 启动目录
  `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start`。
  按 skill 的 `AGENT_CWD="$PWD" … cd "$AGENT_CWD"` 写法执行，安装不会把 cwd 带走。

## 关键命令

```bash
SK=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
PY=/opt/homebrew/opt/python@3.12/bin/python3.12      # 系统 python3 是 3.9.6，低于要求的 3.10+
cd .../e01-first-install-complete-archive/agent-start
AGENT_CWD="$PWD"
$PY "$SK/bootstrap.py" doctor                        # 安装前体检：CLI/DB 均缺失
$PY "$SK/bootstrap.py" install                       # 下载 + 解压 + 安装（--source/--date 取自环境与系统日期）
cd "$AGENT_CWD"                                      # 回到 Agent 启动目录
$PY "$SK/bootstrap.py" doctor                        # 安装后体检：全绿
$PY "$SK/bootstrap.py" cli-path                      # 确认实际 CLI 位置
$PY "$SK/bootstrap.py" refresh                       # 幂等性：已是最新，无需刷新
RT="$OSKM_RUNTIME_ROOT"
$PY "$RT/oskm-cli.pyz" --version
$PY "$RT/oskm-cli.pyz" --db "$RT/knowledge.db" ask get_scan_info
```

## 关键输出片段

安装前 `doctor`（缺 CLI、未安装）：

```text
CLI: FAIL: 找不到可用的 oskm-cli 产物。… 3. <runtime>/oskm-cli.pyz —— 不存在
Modules: oskm_runtime (OK), oskm_cli (FAIL: No module named 'oskm_cli'), oskm_schema (FAIL: …)
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。            # exit=1
```

`install`：

```text
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: …/e01-first-install-complete-archive/runtime   # exit=0
```

安装后 `doctor`：

```text
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: …/runtime
Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）  # exit=0
```

`refresh`（幂等）与 CLI 自检：

```text
==> 运行时已是最新，无需刷新: …/runtime     # exit=0
oskm-cli 1.0.0
```

`ask get_scan_info` 摘要：`product=synthetic`、`cpu_arch=arm64`、`status=complete`，
11 个采集器（args/arkts/components/elf_modules/hdi/install_modules/links/native/repos/sas/services）
全部 `complete`，各 `record_count=1`。

## 安装后的布局

```text
<runtime-root>/                     # OSKM_RUNTIME_ROOT
├── .oskm-runtime.json              # 状态文件 version 3（535 B，权限 0600）
├── knowledge.db                    # 434176 B，sha256 f561e39f…d1b44
├── oskm-cli.pyz                    # 83741 B，可执行，sha256 ad760c16…b49e
└── interface/
    ├── sdk-js/api/@internal/ohos.evalmarker.d.ts
    └── sdk_c/evalmarker.h
```

要点：
- SDK 直接落在 `interface/sdk-js`、`interface/sdk_c`，**没有**多套一层
  `interface/interface/…`，与 DB 中 `source_path`/`header_path` 的相对解析规则一致。
- CLI 与 `knowledge.db` **并排**在运行时根目录，固定文件名、不带版本号；版本问
  `oskm-cli.pyz --version`（实测 1.0.0）。
- 状态文件 `cli`/`db` 段记的 `{path, sha256}` 是出处记录，不参与校验。
- 未创建 `.env`（可选文件）；`~/.oskm` 未被访问或修改。

## 后续查询入口

```bash
RT="$OSKM_RUNTIME_ROOT"
/opt/homebrew/opt/python@3.12/bin/python3.12 "$RT/oskm-cli.pyz" --db "$RT/knowledge.db" arch overview
```

注意：查询路径不会自动联网，数据过期时显式跑 `bootstrap.py refresh`。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**Installed**
- Ran pre-install `doctor` → CLI/DB missing (exit 1), then `install` with `python3.12` (system `python3` is 3.9.6, below the 3.10+ floor), then `cd` back to the start dir.
- `install` output: `==> 下载 INTERNAL_CI 运行时: 20261117` / `==> 运行时安装完成: …/runtime`, exit 0 — one archive installed all four artifacts.
- `refresh` is a no-op afterwards (`运行时已是最新`), confirming idempotency.

**Layout** (`OSKM_RUNTIME_ROOT`, not `~/.oskm` — `$HOME/.oskm` still doesn't exist)
- `runtime/knowledge.db` (434176 B), `runtime/oskm-cli.pyz` (83741 B, executable) sitting side by side, `runtime/.oskm-runtime.json` (version 3, mode 0600).
- `runtime/interface/sdk-js/api/@internal/ohos.evalmarker.d.ts` and `runtime/interface/sdk_c/evalmarker.h` — no doubled `interface/interface/` nesting.

**Status**
- `doctor` all green: Python 3.12.16 OK, `CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)`, modules `oskm_runtime/oskm_cli/oskm_schema` OK, `Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`, DB opens.
- `cli-path` resolves to `runtime/oskm-cli.pyz`; `oskm-cli.pyz --version` → `oskm-cli 1.0.0`.
- Smoke query `ask get_scan_info` → `product=synthetic`, `cpu_arch=arm64`, `status=complete`, 11 collectors all `complete` with `record_count=1`.

**Working Directory**
- Unchanged before/after install: `/var/folders/…/e01-first-install-complete-archive/agent-start` (kept via `AGENT_CWD="$PWD" … cd "$AGENT_CWD"`).

Write-up with commands and output snippets is in `answer.md` (agent-start dir). Next logical step if you want it: run an actual architecture query, e.g. `python3.12 "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview`.stderr:
2026-11-17T07:33:43.344327Z ERROR codex_skills_extension::host_service: failed to install system skills: io error while create system skills subdir: Invalid argument (os error 22)
2026-11-17T07:33:43.353276Z ERROR codex_skills_extension::host_service: failed to install system skills: io error while remove existing system skills dir: Directory not empty (os error 66)
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/agent-start` · exit=0 · 200.2s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T15:34:59.171+08:00",
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

## 断言结果

自动断言 9/9 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | knowledge.db 装到了运行时根目录 | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/runtime/knowledge.db |
| 2 | oskm-cli.pyz 与 DB 并排（同一次安装装齐） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e01-first-install-complete-archive/runtime/oskm-cli.pyz |
| 3 | interface/sdk-js 非空 | auto | Pass | 1 个文件 |
| 4 | interface/sdk_c 非空 | auto | Pass | 1 个文件 |
| 5 | 状态文件同时记录 db / sdk / cli 三段 | auto | Pass | ["cli", "date", "db", "sdk", "source", "updated_at", "version"] |
| 6 | 工具每次安装只发一条"按日期取归档"的请求（没有盲探端点，也没有单独的 CLI 下载端点） | auto | Pass | 请求数=1，其中按日期归档请求=1；oskm-cli.pyz 已随归档装好=True；[{"method": "GET", "path": "/internal/20261117"}] |
| 7 | Agent 启动目录没有被安装产物污染 | auto | Pass | 启动目录内容: ['PROMPT.md', 'agent-last-message.md', 'answer.md', 'codex-events.jsonl', 'codex-stderr.log'] |
| 8 | 运行时根目录没有残留安装临时目录 | auto | Pass | leftovers=[] |
| 9 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
