# E5 local-source-runtime-preferred（with-skill 臂）

- 开始时间：2026-11-17T15:37:41+08:00
- 结束时间：2026-11-17T15:41:28+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred`
- 夹具服务端：http://127.0.0.1:61323
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

当前目录是完整 OpenHarmony 源码根，包含 .gn、非空的 interface/sdk-js 和 interface/sdk_c、out/sample-product/oskm/knowledge.db 或 artifacts/sample-product/knowledge.db，以及本地 cli/dist/oskm-cli.pyz。请安装运行时，并避免不必要的网络请求。

## 期望结果（来自 evals.json）

install 优先使用源码树中的 DB、CLI 和两套 SDK，记录 source: local 和源码根路径；cli-path 也应优先源码树 CLI；本地候选完整时不得调用下载端点。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| source: local | `contains` |
| 不使用下载 | `contains` |
| 本地 DB、CLI、sdk-js 和 sdk_c 完整时优先本地且不访问网络 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：226.5 s
- 事件计数：`{"thread.started": 1, "item.completed": 43, "item:error": 1, "turn.started": 1, "item:reasoning": 13, "item:agent_message": 10, "item.started": 19, "item:command_execution": 38, "turn.completed": 1}`
- 读到 skill 文档：是（11 处）
- 执行的命令数：19
- token 用量：`{"input_tokens": 283132, "cached_input_tokens": 255232, "output_tokens": 7719, "reasoning_output_tokens": 1678}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source && ls -la && echo "--- .gn ---" && cat .gn 2>/dev/null | head -30 && echo "--- cli ---" && ls -la cli/dist/ && echo "--- out ---" && ls -la out/sample-product/oskm/ 2>/dev/null'
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; ls -la "$SKILL_DIR"; echo "--- refs ---"; ls -la "$SKILL_DIR/references" "$SKILL_DIR/references/spec" 2>/dev/null'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source && cat PROMPT.md; echo "=== interface ==="; ls -la interface interface/* | head -40; echo "=== env ==="; env | grep -i -E "oskm|python" '
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; cat "$SKILL_DIR/bootstrap.py"; echo "=== grep source-root in usage.md ==="; grep -n -E "source-root|source_root|OSKM_RUNTIME_ROOT|runtime-root" "$SKILL_DIR/references/usage.md" | head -60'
$ /bin/zsh -lc "SKILL_DIR=\"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query\"; sed -n '225,320p' \""'$SKILL_DIR/references/usage.md"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source && python3 -V; /opt/homebrew/opt/python@3.12/bin/python3.12 -V; echo "=== runtime root ==="; ls -la "$OSKM_RUNTIME_ROOT"'
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" --help 2>&1 | head -40; echo "=== doctor help ==="; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" doctor --help 2>&1 | head -30; echo "=== install help ==="; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" install --help 2>&1 | head -50'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred && ls -la; echo "=== install ==="; cd source && SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query" && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT"; echo "EXIT=$?"'
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source; echo "=== doctor ==="; $PY "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"; echo "EXIT=$?"; echo "=== cli-path ==="; $PY "$SKILL_DIR/bootstrap.py" cli-path --runtime-root "$OSKM_RUNTIME_ROOT"; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd "$OSKM_RUNTIME_ROOT" && ls -la && echo "=== state ===" && cat .oskm-runtime.json && echo && echo "=== sdk dirs ===" && ls -R interface | head -30 && du -sh interface/sdk-js interface/sdk_c knowledge.db oskm-cli.pyz 2>/dev/null'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; CLI="$OSKM_RUNTIME_ROOT/oskm-cli.pyz"; DB="$OSKM_RUNTIME_ROOT/knowledge.db"; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source; echo "=== version ==="; $PY $CLI --version; echo "=== get_scan_info ==="; $PY $CLI --db $DB ask get_scan_info 2>&1 | head -60'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; CLI="$OSKM_RUNTIME_ROOT/oskm-cli.pyz"; DB="$OSKM_RUNTIME_ROOT/knowledge.db"; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source; echo "=== arch overview (table) ==="; $PY $CLI --db $DB arch overview --format table 2>&1 | head -40; echo "EXIT=$?"'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; CLI="$OSKM_RUNTIME_ROOT/oskm-cli.pyz"; DB="$OSKM_RUNTIME_ROOT/knowledge.db"; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source; echo "=== arch overview ==="; $PY $CLI --db $DB --format table arch overview 2>&1 | head -30; echo "EXIT=$?"'
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source; echo "=== refresh (idempotent) ==="; $PY "$SKILL_DIR/bootstrap.py" refresh --runtime-root "$OSKM_RUNTIME_ROOT"; echo "EXIT=$?"; echo "=== source tree untouched? ==="; shasum -a 256 out/sample-product/oskm/knowledge.db cli/dist/oskm-cli.pyz interface/sdk_c/evalmarker.h; shasum -a 256 "$OSKM_RUNTIME_ROOT/knowledge.db" "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" "$OSKM_RUNTIME_ROOT/interface/sdk_c/evalmarker.h"'
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source; echo "=== validate-db ==="; $PY "$SKILL_DIR/bootstrap.py" validate-db "$OSKM_RUNTIME_ROOT/knowledge.db" --runtime-root "$OSKM_RUNTIME_ROOT" 2>&1 | tail -20; echo "EXIT=$?"'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; CLI="$OSKM_RUNTIME_ROOT/oskm-cli.pyz"; DB="$OSKM_RUNTIME_ROOT/knowledge.db"; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source; echo "=== arch overview json ==="; $PY $CLI --db $DB arch overview; echo "=== scan_info tail ==="; $PY $CLI --db $DB ask get_scan_info | tail -30'
$ /bin/zsh -lc "cat > /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source/answer.md <<'EOF'
# 安装 OpenHarmony 架构证据运行时（源码树本地优先，零网络请求）

## 直接回答

- 运行时**已安装成功**到托管根目录 "'`$OSKM_RUNTIME_ROOT`
  （`…/e05-local-source-runtime-preferred/runtime`），一次装齐 4 件套：
  `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`。
- **没有产生任何网络请求**：`install` 命中源码树本地构建（`source: local`），
  未回退到 `OSKM_DOWNLOAD_SOURCE=INTERNAL_CI` / `OSKM_DOWNLOAD_ENDPOINT` 下载流程。
- 源码树是**只读复制**，未被移动或修改（DB / CLI / 头文件 sha256 与运行时侧完全一致）。
- 未访问、未创建 `~/.oskm`；全程只用任务给出的 `--runtime-root`。
- 装好的 CLI 可正常查询，DB 通过完整 schema 契约校验。

## 关键命令（按执行顺序）

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12          # python3 是 3.9.6，低于要求的 3.10+
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
cd …/e05-local-source-runtime-preferred/source           # 源码根，install 从 cwd 向上探测

# 1) 体检：确认 Python、配置与"源码根本地构建"提示
$PY "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"

# 2) 安装：不传 --source / --date，让 install 优先用源码树本地构建
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT"

# 3) 复核：doctor / cli-path / validate-db
$PY "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"
$PY "$SKILL_DIR/bootstrap.py" cli-path --runtime-root "$OSKM_RUNTIME_ROOT"
$PY "$SKILL_DIR/bootstrap.py" validate-db "$OSKM_RUNTIME_ROOT/knowledge.db" --runtime-root "$OSKM_RUNTIME_ROOT"

# 4) 幂等性：refresh 不应联网、不应重装
$PY "$SKILL_DIR/bootstrap.py" refresh --runtime-root "$OSKM_RUNTIME_ROOT"

# 5) 冒烟查询
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --version
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask get_scan_info
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview
```

## 关键输出片段

安装前 `doctor`（缺 CLI / 未安装，并给出本地构建提示）：

```text
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。…
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
提示: 检测到源码根本地构建: …/source/out/sample-product/oskm/knowledge.db
      在源码根或其子目录执行 bootstrap.py install，或传 --source-root <path>，将优先使用本地构建，不联网。
```

`install`（走本地，无下载动作）：

```text
==> 使用源码本地运行时: …/source/out/sample-product/oskm/knowledge.db
==> 运行时安装完成: …/e05-local-source-runtime-preferred/runtime
EXIT=0
```

安装后 `doctor` / `cli-path`：

```text
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261117, source local, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
EXIT=0
--- cli-path ---
…/runtime/oskm-cli.pyz
```

状态文件 `runtime/.oskm-runtime.json`（`source: local` = 本次未联网的铁证）：

```json
{
  "version": 3,
  "source": "local",
  "date": "20261117",
  "source_root": "…/e05-local-source-runtime-preferred/source",
  "db":  { "path": "knowledge.db", "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44" },
  "sdk": { "sdk-js": { "path": "interface/sdk-js" }, "sdk_c": { "path": "interface/sdk_c" } },
  "cli": { "path": "oskm-cli.pyz", "sha256": "ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e" }
}
```

`validate-db` 与 `refresh`：

```text
{"path": "…/runtime/knowledge.db", "ok": true}
==> 运行时已是最新，无需刷新: …/runtime        # 本地运行时不因日期变化重装，也没联网
```

冒烟查询（`--format table` 是全局选项，要写在子命令前）：

```text
$ oskm-cli.pyz --version            → oskm-cli 1.0.0
$ … ask get_scan_info               → product=synthetic, scan_id=1, cpu_arch=arm64, status=complete
                                      各采集器 status=complete, schema_version=4.0.0
$ … --format table arch overview    → graphics 1 / startup 1
$ … arch overview (json)            → subsystems=2, components=2, repos=1, install_targets=3,
                                      services=2, hdis=1, gn_args=1, elf_modules=0, arkts_modules=0
```

## 运行时布局（安装结果）

```text
$OSKM_RUNTIME_ROOT/
├── .oskm-runtime.json      # version 3 托管标记，source=local
├── knowledge.db            # 434176 B，sha256 f561e39f…
├── oskm-cli.pyz            # 83741 B，sha256 ad760c16…，oskm-cli 1.0.0
└── interface/
    ├── sdk-js/api/@internal/ohos.evalmarker.d.ts
    └── sdk_c/evalmarker.h
```

## 只读性核对（源码树未被改动）

```text
f561e39f…  source/out/sample-product/oskm/knowledge.db   ==  runtime/knowledge.db
ad760c16…  source/cli/dist/oskm-cli.pyz                  ==  runtime/oskm-cli.pyz
49673a32…  source/interface/sdk_c/evalmarker.h           ==  runtime/interface/sdk_c/evalmarker.h
```

## 为什么能不联网（判定依据）

源码根同时具备 `.gn`（文件）、非空 `interface/sdk-js/`、非空 `interface/sdk_c/`、
`out/`，且 `out/sample-product/oskm/knowledge.db`（一层布局）与 `cli/dist/oskm-cli.pyz`
都在 → `install` 的"源码根优先"分支命中，DB 通过 schema 校验后直接复制装入，
不会回退到 `OSKM_DOWNLOAD_SOURCE` 的下载流程。cwd 就在源码根内，因此不需要 `--source-root`。

## 后续查询用法与证据边界

```bash
CLI="$OSKM_RUNTIME_ROOT/oskm-cli.pyz"; DB="$OSKM_RUNTIME_ROOT/knowledge.db"
$PY $CLI --db $DB arch overview|trace|impact|provides|interfaces|gn-args
$PY $CLI --db $DB ask <tool>          # 单点字段；$PY $CLI --db $DB ask --list 看全部工具
```

- 本库 `elf_modules=0`、`arkts_modules=0`：**不能**用它回答 ELF 依赖 / 反向依赖 /
  影响面或 ArkTS 模块类问题（计数为 0 = 该证据未采集，不等于"没有依赖"），也不要编数。
- 快照语义：`content_match` 恒为 `unverified`，git 提交号是扫描当时的，不代表现状。
- `install_targets=3` 是安装落点条数，**不是** `.img` 数量。
- 数据过期时显式跑 `bootstrap.py refresh`；查询本身不会触发任何下载。
EOF
echo "written:"; wc -l /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source/answer.md'
$ /bin/zsh -lc 'ls -la ~/.oskm 2>&1 | head -5; echo "=== git status of source dir (if repo) ==="; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source && ls -la && head -20 answer.md'
```

### Agent 最终回答

```markdown
**结果**
运行时已装好，全程零网络请求。`install` 在 cwd（源码根）向上探测到本地构建后直接使用，未回退到 `INTERNAL_CI` 下载流程；`~/.oskm` 从未创建，源码树只读未改。

**关键步骤**
- `python3.12 bootstrap.py doctor --runtime-root "$OSKM_RUNTIME_ROOT"` → 未安装，但提示“检测到源码根本地构建: …/source/out/sample-product/oskm/knowledge.db”。
- `python3.12 bootstrap.py install --runtime-root "$OSKM_RUNTIME_ROOT"` → `==> 使用源码本地运行时` / `==> 运行时安装完成`，退出码 0。
- 复核：`doctor` 报 `source local, db=✓, sdk=✓, cli=✓`、`oskm-cli 1.0.0`；`cli-path` 打印 `runtime/oskm-cli.pyz`；`validate-db` 返回 `{"ok": true}`。
- `refresh` → `运行时已是最新，无需刷新`（本地运行时不因日期重装，也没联网）。
- 冒烟查询：`ask get_scan_info` 得 `product=synthetic, scan_id=1, status=complete`；`--format table arch overview` 得 `graphics 1 / startup 1`。

**安装产物**
- `runtime/knowledge.db`、`runtime/oskm-cli.pyz`、`runtime/interface/sdk-js/`、`runtime/interface/sdk_c/`、`runtime/.oskm-runtime.json`（`"source": "local"`，`version 3`）。
- sha256 与源码侧逐一对齐（`f561e39f…` DB、`ad760c16…` CLI、`49673a32…` 头文件），证明是复制而非移动。

**注意点**
- `--format table` 是全局选项，必须写在子命令前（`… --db $DB --format table arch overview`），否则报 `unrecognized arguments`。
- 该库 `elf_modules=0`、`arkts_modules=0`，所以 ELF 依赖/影响面与 ArkTS 模块类问题在这份快照上不可用，不要拿 0 当“无依赖”。

结论、命令与输出片段已写入 `answer.md`（源码根目录下）。需要我接着用这份运行时跑一轮 `arch trace` / `arch impact` 之类的实证查询吗？
```

### Agent 写入的 answer.md

```markdown
# 安装 OpenHarmony 架构证据运行时（源码树本地优先，零网络请求）

## 直接回答

- 运行时**已安装成功**到托管根目录 `$OSKM_RUNTIME_ROOT`
  （`…/e05-local-source-runtime-preferred/runtime`），一次装齐 4 件套：
  `knowledge.db` + `oskm-cli.pyz` + `interface/sdk-js` + `interface/sdk_c`。
- **没有产生任何网络请求**：`install` 命中源码树本地构建（`source: local`），
  未回退到 `OSKM_DOWNLOAD_SOURCE=INTERNAL_CI` / `OSKM_DOWNLOAD_ENDPOINT` 下载流程。
- 源码树是**只读复制**，未被移动或修改（DB / CLI / 头文件 sha256 与运行时侧完全一致）。
- 未访问、未创建 `~/.oskm`；全程只用任务给出的 `--runtime-root`。
- 装好的 CLI 可正常查询，DB 通过完整 schema 契约校验。

## 关键命令（按执行顺序）

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12          # python3 是 3.9.6，低于要求的 3.10+
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
cd …/e05-local-source-runtime-preferred/source           # 源码根，install 从 cwd 向上探测

# 1) 体检：确认 Python、配置与"源码根本地构建"提示
$PY "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"

# 2) 安装：不传 --source / --date，让 install 优先用源码树本地构建
$PY "$SKILL_DIR/bootstrap.py" install --runtime-root "$OSKM_RUNTIME_ROOT"

# 3) 复核：doctor / cli-path / validate-db
$PY "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$OSKM_RUNTIME_ROOT"
$PY "$SKILL_DIR/bootstrap.py" cli-path --runtime-root "$OSKM_RUNTIME_ROOT"
$PY "$SKILL_DIR/bootstrap.py" validate-db "$OSKM_RUNTIME_ROOT/knowledge.db" --runtime-root "$OSKM_RUNTIME_ROOT"

# 4) 幂等性：refresh 不应联网、不应重装
$PY "$SKILL_DIR/bootstrap.py" refresh --runtime-root "$OSKM_RUNTIME_ROOT"

# 5) 冒烟查询
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --version
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" ask get_scan_info
$PY "$OSKM_RUNTIME_ROOT/oskm-cli.pyz" --db "$OSKM_RUNTIME_ROOT/knowledge.db" arch overview
```

## 关键输出片段

安装前 `doctor`（缺 CLI / 未安装，并给出本地构建提示）：

```text
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。…
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
提示: 检测到源码根本地构建: …/source/out/sample-product/oskm/knowledge.db
      在源码根
… [输出截断，完整内容见工作区] …
ad760c16…  source/cli/dist/oskm-cli.pyz                  ==  runtime/oskm-cli.pyz
49673a32…  source/interface/sdk_c/evalmarker.h           ==  runtime/interface/sdk_c/evalmarker.h
```

## 为什么能不联网（判定依据）

源码根同时具备 `.gn`（文件）、非空 `interface/sdk-js/`、非空 `interface/sdk_c/`、
`out/`，且 `out/sample-product/oskm/knowledge.db`（一层布局）与 `cli/dist/oskm-cli.pyz`
都在 → `install` 的"源码根优先"分支命中，DB 通过 schema 校验后直接复制装入，
不会回退到 `OSKM_DOWNLOAD_SOURCE` 的下载流程。cwd 就在源码根内，因此不需要 `--source-root`。

## 后续查询用法与证据边界

```bash
CLI="$OSKM_RUNTIME_ROOT/oskm-cli.pyz"; DB="$OSKM_RUNTIME_ROOT/knowledge.db"
$PY $CLI --db $DB arch overview|trace|impact|provides|interfaces|gn-args
$PY $CLI --db $DB ask <tool>          # 单点字段；$PY $CLI --db $DB ask --list 看全部工具
```

- 本库 `elf_modules=0`、`arkts_modules=0`：**不能**用它回答 ELF 依赖 / 反向依赖 /
  影响面或 ArkTS 模块类问题（计数为 0 = 该证据未采集，不等于"没有依赖"），也不要编数。
- 快照语义：`content_match` 恒为 `unverified`，git 提交号是扫描当时的，不代表现状。
- `install_targets=3` 是安装落点条数，**不是** `.img` 数量。
- 数据过期时显式跑 `bootstrap.py refresh`；查询本身不会触发任何下载。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结果**
运行时已装好，全程零网络请求。`install` 在 cwd（源码根）向上探测到本地构建后直接使用，未回退到 `INTERNAL_CI` 下载流程；`~/.oskm` 从未创建，源码树只读未改。

**关键步骤**
- `python3.12 bootstrap.py doctor --runtime-root "$OSKM_RUNTIME_ROOT"` → 未安装，但提示“检测到源码根本地构建: …/source/out/sample-product/oskm/knowledge.db”。
- `python3.12 bootstrap.py install --runtime-root "$OSKM_RUNTIME_ROOT"` → `==> 使用源码本地运行时` / `==> 运行时安装完成`，退出码 0。
- 复核：`doctor` 报 `source local, db=✓, sdk=✓, cli=✓`、`oskm-cli 1.0.0`；`cli-path` 打印 `runtime/oskm-cli.pyz`；`validate-db` 返回 `{"ok": true}`。
- `refresh` → `运行时已是最新，无需刷新`（本地运行时不因日期重装，也没联网）。
- 冒烟查询：`ask get_scan_info` 得 `product=synthetic, scan_id=1, status=complete`；`--format table arch overview` 得 `graphics 1 / startup 1`。

**安装产物**
- `runtime/knowledge.db`、`runtime/oskm-cli.pyz`、`runtime/interface/sdk-js/`、`runtime/interface/sdk_c/`、`runtime/.oskm-runtime.json`（`"source": "local"`，`version 3`）。
- sha256 与源码侧逐一对齐（`f561e39f…` DB、`ad760c16…` CLI、`49673a32…` 头文件），证明是复制而非移动。

**注意点**
- `--format table` 是全局选项，必须写在子命令前（`… --db $DB --format table arch overview`），否则报 `unrecognized arguments`。
- 该库 `elf_modules=0`、`arkts_modules=0`，所以 ELF 依赖/影响面与 ArkTS 模块类问题在这份快照上不可用，不要拿 0 当“无依赖”。

结论、命令与输出片段已写入 `answer.md`（源码根目录下）。需要我接着用这份运行时跑一轮 `arch trace` / `arch impact` 之类的实证查询吗？
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source` · exit=0 · 226.5s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（0 条）

```json
[]
```

### agent 自己的探测请求（0 条）

```json
[]
```

## 断言结果

自动断言 8/8 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 本地候选完整时工具一次网络请求都不发 | auto | Pass | [] |
| 2 | 状态文件记录 source=local | auto | Pass | source=local |
| 3 | 状态文件记录源码根路径 | auto | Pass | source_root=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source |
| 4 | 装进来的 DB 就是源码树那一份（sha256 相同） | auto | Pass | installed=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 source=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 |
| 5 | 装进来的 CLI 就是源码树 cli/dist 那一份 | auto | Pass | installed=ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e source=ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e |
| 6 | 两套 SDK 都从源码树复制过来且非空 | auto | Pass | sdk-js=1 sdk_c=1 |
| 7 | 源码树本身没有被改动（DB 仍在原位） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source/out/sample-product/oskm/knowledge.db / /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e05-local-source-runtime-preferred/source/cli/dist/oskm-cli.pyz |
| 8 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
