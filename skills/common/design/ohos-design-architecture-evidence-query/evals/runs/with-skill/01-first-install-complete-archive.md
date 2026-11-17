# E1 first-install-complete-archive（with-skill 臂）

- 开始时间：2026-11-17T16:40:02+08:00
- 结束时间：2026-11-17T16:42:48+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/with-skill/e01-first-install-complete-archive`
- 夹具服务端：http://127.0.0.1:62352
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/with-skill/e01-first-install-complete-archive/agent-start --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：165.7 s
- 事件计数：`{"thread.started": 1, "item.completed": 39, "item:error": 1, "turn.started": 1, "item:reasoning": 11, "item:agent_message": 11, "item.started": 16, "item:command_execution": 32, "turn.completed": 1}`
- 读到 skill 文档：是（17 处）
- 执行的命令数：16
- token 用量：`{"input_tokens": 258365, "cached_input_tokens": 228352, "output_tokens": 6443, "reasoning_output_tokens": 1536}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc "pwd; ls -la; echo \"---ENV---\"; env | grep -i -E 'oskm|codex' | sort"
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '80,140p' \""'$SK/SKILL.md"; echo "=====TREE====="; ls -la "$SK"; echo "-----"; ls -la "$SK/references" 2>/dev/null'
$ /bin/zsh -lc 'cat PROMPT.md; echo "=====EVENTS====="; cat codex-events.jsonl; echo "=====RUNTIME====="; ls -la "$OSKM_RUNTIME_ROOT"; echo "=====PARENT====="; ls -la ..'
$ /bin/zsh -lc 'cat "$CODEX_HOME/skills/ohos-design-architecture-evidence-query/bootstrap.py"; echo "=====PY====="; python3 --version; which python3; /opt/homebrew/opt/python@3.12/bin/python3.12 --version'
$ /bin/zsh -lc "grep -n -i -E 'doctor|install|refresh|cli-path|OSKM_RUNTIME_ROOT|OSKM_DOWNLOAD_SOURCE|INTERNAL_CI|tar.gz' \""'$CODEX_HOME/skills/ohos-design-architecture-evidence-query/references/usage.md" | head -80'
$ /bin/zsh -lc 'SK="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SK/bootstrap.py" doctor; echo "EXIT=$?"'
$ /bin/zsh -lc "sed -n '10,60p' \""'$CODEX_HOME/skills/ohos-design-architecture-evidence-query/references/usage.md"'
$ /bin/zsh -lc 'AGENT_CWD="$PWD"; SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"; echo "AGENT_CWD=$AGENT_CWD"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" 2>&1 | tail -40; echo "EXIT=${pipestatus[1]}"; cd "$AGENT_CWD"; echo "BACK_TO=$PWD"'
$ /bin/zsh -lc 'SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; echo "=====DOCTOR====="; $PY "$SKILL_DIR/bootstrap.py" doctor; echo "DOCTOR_EXIT=$?"; echo "=====CLI-PATH====="; $PY "$SKILL_DIR/bootstrap.py" cli-path; echo "CLIPATH_EXIT=$?"'
$ /bin/zsh -lc 'R="$OSKM_RUNTIME_ROOT"; echo "=====TOP====="; ls -la "$R"; echo "=====INTERFACE====="; ls -la "$R/interface"; echo "=====SDK-JS(head)====="; ls "$R/interface/sdk-js" | head -8; echo "count=$(ls "$R/interface/sdk-js" | wc -l)"; echo "=====SDK_C(head)====="; ls "$R/interface/sdk_c" | head -8; echo "count=$(ls "$R/interface/sdk_c" | wc -l)"; echo "=====STATE====="; cat "$R/.oskm-runtime.json"; echo; echo "=====TREE(depth2)====="; find "$R" -maxdepth 2 | sed "s|$R|<runtime-root>|" | sort | head -30; echo "=====SIZES====="; du -sh "$R/knowledge.db" "$R/oskm-cli.pyz" "$R/interface/sdk-js" "$R/interface/sdk_c" 2>/dev/null; echo "=====TOTAL FILES====="; find "$R" -type f | wc -l'
$ /bin/zsh -lc 'SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; R="$OSKM_RUNTIME_ROOT"; echo "=====VALIDATE-DB====="; $PY "$SKILL_DIR/bootstrap.py" validate-db --runtime-root "$R"; echo "VALIDATE_EXIT=$?"; echo "=====CLI VERSION====="; $PY "$R/oskm-cli.pyz" --version; echo "=====SCAN INFO====="; $PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" ask get_scan_info; echo "SCAN_EXIT=$?"'
$ /bin/zsh -lc 'R="$OSKM_RUNTIME_ROOT"; echo "=====ALL FILES====="; find "$R" | sed "s|$R|<runtime-root>|" | sort; echo "=====HOME .oskm====="; ls -la "$HOME/.oskm" 2>&1 | head -5; echo "=====CWD====="; pwd; ls -la'
$ /bin/zsh -lc 'SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; $PY "$SKILL_DIR/bootstrap.py" validate-db --help; echo "-----"; $PY "$SKILL_DIR/bootstrap.py" validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"; echo "VALIDATE_EXIT=$?"'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; R="$OSKM_RUNTIME_ROOT"; $PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" ask search_native_headers --query evalmarker; echo "EXIT=$?"; echo "=====ARCH OVERVIEW====="; $PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" arch overview | head -30; echo "=====FINAL PWD====="; pwd'
$ /bin/zsh -lc "cat > answer.md <<'EOF'
# oskm 托管运行时首次安装（完整归档）——结论

## 直接回答

- **安装成功**：从任意 Agent 启动目录（本次为 "'`agent-start/`）用 skill 的 `bootstrap.py install` 一次装齐 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`，无需源码树、无需 Git。
- **状态**：`doctor` 退出码 `0`；状态文件 `version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`；`validate-db` 返回 `{"ok": true}`；CLI 可执行且能打开库（`oskm-cli 1.0.0`）。
- **当前工作目录**：安装结束后仍为 Agent 启动目录
  `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/with-skill/e01-first-install-complete-archive/agent-start`
  （按 skill 约定先记 `AGENT_CWD="$PWD"`，install 后 `cd "$AGENT_CWD"` 回来；bootstrap 自身不改变调用方 cwd，但显式回退保证行为一致）。
- **未触碰 `~/.oskm`**：该路径不存在，全程只用 `OSKM_RUNTIME_ROOT` 指向的 `runtime/`。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12          # 系统 python3 是 3.9.6，低于 skill 要求的 ≥3.10
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
AGENT_CWD="$PWD"

$PY "$SKILL_DIR/bootstrap.py" doctor                                     # 安装前：FAIL（退出码 1）
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" # 安装
cd "$AGENT_CWD"

$PY "$SKILL_DIR/bootstrap.py" doctor                                     # 安装后：OK（退出码 0）
$PY "$SKILL_DIR/bootstrap.py" cli-path
$PY "$SKILL_DIR/bootstrap.py" validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --version
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask get_scan_info
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview
```

注：`validate-db` 收的是**位置参数**（`knowledge.db` 路径），不是 `--runtime-root`；写成 `--runtime-root` 会 `错误: validate-db 需要一个路径`，退出码 2。

## 关键输出片段

安装前 `doctor`（未安装，预期失败）：

```text
CLI: FAIL: 找不到可用的 oskm-cli 产物。…已尝试：1. $OSKM_CLI 未设置 2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py 3. <runtime-root>/oskm-cli.pyz —— 不存在
Modules: oskm_runtime (OK), oskm_cli (FAIL: No module named '"'oskm_cli'), oskm_schema (FAIL: No module named 'oskm_schema')
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。      EXIT=1
"'```

`install`：

```text
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /…/e01-first-install-complete-archive/runtime
EXIT=0
```

安装后 `doctor`：

```text
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: /…/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: /…/e01-first-install-complete-archive/runtime
Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
DOCTOR_EXIT=0
```

`cli-path` / `validate-db` / `--version`：

```text
/…/e01-first-install-complete-archive/runtime/oskm-cli.pyz        CLIPATH_EXIT=0
{"path": "/…/runtime/knowledge.db", "ok": true}                   VALIDATE_EXIT=0
oskm-cli 1.0.0
```

`ask get_scan_info`（快照自检）：

```text
"product": "synthetic", "cpu_arch": "arm64", "scan_id": 1, "status": "complete"
collectors: args/arkts/components/elf_modules/hdi/install_modules/links/native/repos/sas/services
            全部 status=complete, schema_version=4.0.0, record_count=1
```

`arch overview`：

```text
product=synthetic, subsystems=2 (graphics, startup)
counts: repos=1, components=2, install_modules=3, install_targets=3, elf_modules=0,
        services=2, sas=0, hdis=1, gn_args=1, arkts_modules=0, arkts_kits=0
```

## 安装后的布局

```text
<runtime-root>/                                    # = $OSKM_RUNTIME_ROOT，本次为 …/e01-first-install-complete-archive/runtime
├── .oskm-runtime.json                             # 状态文件 version 3（535 B，权限 600）
├── knowledge.db                                   # 424 KB，sha256 f561e39f…d1b44
├── oskm-cli.pyz                                   # 84 KB，可执行，sha256 3e78cf73…d171f5
└── interface/
    ├── sdk-js/api/@internal/ohos.evalmarker.d.ts   # ArkTS API / Kit 声明
    └── sdk_c/evalmarker.h                          # Native SDK 头文件
```

- 文件总数 5（含状态文件）；`interface/` 只有一层，没有 `interface/interface/…` 多套一层的问题，DB 里的 `source_path` / `header_path` 相对 `<runtime-root>` 可解析。
- 没有出现 `.env`（可选，本次不需要；真实环境变量已提供 `OSKM_DOWNLOAD_SOURCE` / `OSKM_DOWNLOAD_ENDPOINT`）。

`.oskm-runtime.json` 关键内容：

```json
{ "version": 3, "source": "INTERNAL_CI", "date": "20261117",
  "updated_at": "2026-11-17T16:40:50+08:00",
  "db":  { "date": "20261117", "path": "knowledge.db", "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44" },
  "sdk": { "date": "20261117", "sdk-js": { "path": "interface/sdk-js" }, "sdk_c": { "path": "interface/sdk_c" } },
  "cli": { "path": "oskm-cli.pyz", "sha256": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5" } }
```

## 当前工作目录

```text
$ pwd
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/with-skill/e01-first-install-complete-archive/agent-start
```

目录内容：`PROMPT.md`、`agent-last-message.md`、`codex-events.jsonl`、`codex-stderr.log`、本次新增的 `answer.md`。
安装没有往启动目录写任何运行时产物——产物只落在 `<runtime-root>`。

## 注意点（供后续查询参考）

- **Python 版本**：宿主 `python3` 为 3.9.6，低于 skill 要求的 3.10+；本次显式用 `/opt/homebrew/opt/python@3.12/bin/python3.12`（3.12.16）。
- **下载路径**：cwd 不在 OpenHarmony 源码树内，所以 `install` 直接走 `INTERNAL_CI`（`$OSKM_DOWNLOAD_ENDPOINT/20261117`），日期默认取当天 `20261117`。
- **数据过期不会自动刷新**：查询路径不联网；需要新数据时显式 `bootstrap.py refresh`。
- **这份快照的证据边界**：`elf_modules=0`、`arkts_modules=0`、`arkts_kits=0`、`sas=0`，属于"该证据未采集/为空"，不能据此回答 ELF 依赖、影响面或 ArkTS/Kit 类问题，也不得编造数量（`ask search_native_headers --query evalmarker` 本次返回 `total=0`，即头文件在 SDK 目录里存在但未进库索引）。
EOF
echo "written"; wc -l answer.md; pwd'
```

### Agent 最终回答

```markdown
**安装结果**
- 从 Agent 启动目录一次 `install` 装齐完整归档，`doctor` 退出码 `0`，`validate-db` 返回 `{"ok": true}`，CLI 版本 `oskm-cli 1.0.0`。
- 状态：`.oskm-runtime.json` `version 3, date 20261117, source INTERNAL_CI, db=✓ sdk=✓ cli=✓`；DB 与 CLI 都记了 sha256。
- 当前工作目录未变，仍是 `agent-start`（install 前记 `AGENT_CWD`，之后 `cd` 回去）；启动目录只新增了 `answer.md`。

**安装后布局**（`$OSKM_RUNTIME_ROOT`，即 `…/e01-first-install-complete-archive/runtime`）
```
runtime/
├── .oskm-runtime.json                            # 535 B, 0600
├── knowledge.db                                  # 424 KB
├── oskm-cli.pyz                                  # 84 KB, 可执行
└── interface/
    ├── sdk-js/api/@internal/ohos.evalmarker.d.ts
    └── sdk_c/evalmarker.h
```

**关键命令**
- `python3.12 "$SKILL_DIR/bootstrap.py" doctor` → 安装前 FAIL（无 CLI、无 DB），安装后 OK。
- `python3.12 "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT"` → `==> 下载 INTERNAL_CI 运行时: 20261117` / `==> 运行时安装完成`。
- `cli-path` → `<runtime-root>/oskm-cli.pyz`；`ask get_scan_info` → `status=complete`，11 个采集器全 `complete`。

**注意点**
- 宿主 `python3` 是 3.9.6，低于 skill 要求的 ≥3.10，必须用 `/opt/homebrew/opt/python@3.12/bin/python3.12`。
- `validate-db` 收位置参数（DB 路径），写 `--runtime-root` 会退出码 2。
- 未访问 `~/.oskm`（该目录不存在）。
- 这份快照 `elf_modules=0`、`arkts_modules=0`、`arkts_kits=0`、`sas=0`，是"未采集/为空"而非"没有依赖"，后续 ELF 依赖、影响面、ArkTS/Kit 类问题不可用它作答。

结论已写入 answer.md:1，需要我再跑一次 `refresh` 验证幂等或做一次 `arch trace` 示例吗？
```

### Agent 写入的 answer.md

```markdown
# oskm 托管运行时首次安装（完整归档）——结论

## 直接回答

- **安装成功**：从任意 Agent 启动目录（本次为 `agent-start/`）用 skill 的 `bootstrap.py install` 一次装齐 `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`，无需源码树、无需 Git。
- **状态**：`doctor` 退出码 `0`；状态文件 `version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓`；`validate-db` 返回 `{"ok": true}`；CLI 可执行且能打开库（`oskm-cli 1.0.0`）。
- **当前工作目录**：安装结束后仍为 Agent 启动目录
  `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/with-skill/e01-first-install-complete-archive/agent-start`
  （按 skill 约定先记 `AGENT_CWD="$PWD"`，install 后 `cd "$AGENT_CWD"` 回来；bootstrap 自身不改变调用方 cwd，但显式回退保证行为一致）。
- **未触碰 `~/.oskm`**：该路径不存在，全程只用 `OSKM_RUNTIME_ROOT` 指向的 `runtime/`。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12          # 系统 python3 是 3.9.6，低于 skill 要求的 ≥3.10
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
AGENT_CWD="$PWD"

$PY "$SKILL_DIR/bootstrap.py" doctor                                     # 安装前：FAIL（退出码 1）
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT" # 安装
cd "$AGENT_CWD"

$PY "$SKILL_DIR/bootstrap.py" doctor                                     # 安装后：OK（退出码 0）
$PY "$SKILL_DIR/bootstrap.py" cli-path
$PY "$SKILL_DIR/bootstrap.py" validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --version
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask get_scan_info
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview
```

注：`validate-db` 收的是**位置参数**（`knowledge.db` 路径），不是 `--runtime-root`；写成 `--runtime-root` 会 `错误: validate-db 需要一个路径`，退出码 2。

## 关键输出片段

安装前 `doctor`（未安装，预期失败）：

```text
CLI: FAIL: 找不到可用的 oskm-cli 产物。…已尝试：1. $OSKM_CLI 未设置 2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py 3. <runtime-root>/oskm-cli.pyz —— 不存在
Modules: oskm_runtime (OK), oskm_cli (FAIL: No module named 'oskm_cli'), oskm_schema (FAIL: No module named 'oskm_schema')
Runtime state: 未安装（没有 knowledge.d
… [输出截断，完整内容见工作区] …
path": "interface/sdk_c" } },
  "cli": { "path": "oskm-cli.pyz", "sha256": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5" } }
```

## 当前工作目录

```text
$ pwd
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/with-skill/e01-first-install-complete-archive/agent-start
```

目录内容：`PROMPT.md`、`agent-last-message.md`、`codex-events.jsonl`、`codex-stderr.log`、本次新增的 `answer.md`。
安装没有往启动目录写任何运行时产物——产物只落在 `<runtime-root>`。

## 注意点（供后续查询参考）

- **Python 版本**：宿主 `python3` 为 3.9.6，低于 skill 要求的 3.10+；本次显式用 `/opt/homebrew/opt/python@3.12/bin/python3.12`（3.12.16）。
- **下载路径**：cwd 不在 OpenHarmony 源码树内，所以 `install` 直接走 `INTERNAL_CI`（`$OSKM_DOWNLOAD_ENDPOINT/20261117`），日期默认取当天 `20261117`。
- **数据过期不会自动刷新**：查询路径不联网；需要新数据时显式 `bootstrap.py refresh`。
- **这份快照的证据边界**：`elf_modules=0`、`arkts_modules=0`、`arkts_kits=0`、`sas=0`，属于"该证据未采集/为空"，不能据此回答 ELF 依赖、影响面或 ArkTS/Kit 类问题，也不得编造数量（`ask search_native_headers --query evalmarker` 本次返回 `total=0`，即头文件在 SDK 目录里存在但未进库索引）。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**安装结果**
- 从 Agent 启动目录一次 `install` 装齐完整归档，`doctor` 退出码 `0`，`validate-db` 返回 `{"ok": true}`，CLI 版本 `oskm-cli 1.0.0`。
- 状态：`.oskm-runtime.json` `version 3, date 20261117, source INTERNAL_CI, db=✓ sdk=✓ cli=✓`；DB 与 CLI 都记了 sha256。
- 当前工作目录未变，仍是 `agent-start`（install 前记 `AGENT_CWD`，之后 `cd` 回去）；启动目录只新增了 `answer.md`。

**安装后布局**（`$OSKM_RUNTIME_ROOT`，即 `…/e01-first-install-complete-archive/runtime`）
```
runtime/
├── .oskm-runtime.json                            # 535 B, 0600
├── knowledge.db                                  # 424 KB
├── oskm-cli.pyz                                  # 84 KB, 可执行
└── interface/
    ├── sdk-js/api/@internal/ohos.evalmarker.d.ts
    └── sdk_c/evalmarker.h
```

**关键命令**
- `python3.12 "$SKILL_DIR/bootstrap.py" doctor` → 安装前 FAIL（无 CLI、无 DB），安装后 OK。
- `python3.12 "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT"` → `==> 下载 INTERNAL_CI 运行时: 20261117` / `==> 运行时安装完成`。
- `cli-path` → `<runtime-root>/oskm-cli.pyz`；`ask get_scan_info` → `status=complete`，11 个采集器全 `complete`。

**注意点**
- 宿主 `python3` 是 3.9.6，低于 skill 要求的 ≥3.10，必须用 `/opt/homebrew/opt/python@3.12/bin/python3.12`。
- `validate-db` 收位置参数（DB 路径），写 `--runtime-root` 会退出码 2。
- 未访问 `~/.oskm`（该目录不存在）。
- 这份快照 `elf_modules=0`、`arkts_modules=0`、`arkts_kits=0`、`sas=0`，是"未采集/为空"而非"没有依赖"，后续 ELF 依赖、影响面、ArkTS/Kit 类问题不可用它作答。

结论已写入 answer.md:1，需要我再跑一次 `refresh` 验证幂等或做一次 `arch trace` 示例吗？
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/with-skill/e01-first-install-complete-archive/agent-start` · exit=0 · 165.7s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T16:40:50.971+08:00",
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
| 1 | knowledge.db 装到了运行时根目录 | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/with-skill/e01-first-install-complete-archive/runtime/knowledge.db |
| 2 | oskm-cli.pyz 与 DB 并排（同一次安装装齐） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-08s944lq/with-skill/e01-first-install-complete-archive/runtime/oskm-cli.pyz |
| 3 | interface/sdk-js 非空 | auto | Pass | 1 个文件 |
| 4 | interface/sdk_c 非空 | auto | Pass | 1 个文件 |
| 5 | 状态文件同时记录 db / sdk / cli 三段 | auto | Pass | ["cli", "date", "db", "sdk", "source", "updated_at", "version"] |
| 6 | 工具每次安装只发一条"按日期取归档"的请求（没有盲探端点，也没有单独的 CLI 下载端点） | auto | Pass | 请求数=1，其中按日期归档请求=1；oskm-cli.pyz 已随归档装好=True；[{"method": "GET", "path": "/internal/20261117"}] |
| 7 | Agent 启动目录没有被安装产物污染 | auto | Pass | 启动目录内容: ['PROMPT.md', 'agent-last-message.md', 'answer.md', 'codex-events.jsonl', 'codex-stderr.log'] |
| 8 | 运行时根目录没有残留安装临时目录 | auto | Pass | leftovers=[] |
| 9 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
