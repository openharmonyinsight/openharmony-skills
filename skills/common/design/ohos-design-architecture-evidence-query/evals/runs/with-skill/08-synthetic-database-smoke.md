# E8 synthetic-database-smoke（with-skill 臂）

- 开始时间：2026-11-17T15:42:10+08:00
- 结束时间：2026-11-17T15:45:31+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e08-synthetic-database-smoke`
- 夹具服务端：http://127.0.0.1:61469
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

已解压 skill 并单独构建 oskm-cli.pyz，测试夹具已生成 product=synthetic 的合成 knowledge.db。请用 bootstrap.py cli-path 定位 CLI，再直接调用 CLI 查询 scan 信息。

## 期望结果（来自 evals.json）

cli-path 找到测试提供的 pyz；直接调用 oskm-cli.pyz --db < synthetic db > ask get_scan_info 返回 product=synthetic。该步骤只验证两个产物能组合运行，不校验真实产品业务数据。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| get_scan_info | `contains` |
| synthetic | `contains` |
| 只验证 skill 与 CLI 的组合链路，不依赖真实数据库业务统计 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e08-synthetic-database-smoke --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：200.1 s
- 事件计数：`{"thread.started": 1, "item.completed": 38, "item:error": 1, "turn.started": 1, "item:reasoning": 10, "item:agent_message": 10, "item.started": 17, "item:command_execution": 34, "turn.completed": 1}`
- 读到 skill 文档：是（9 处）
- 执行的命令数：17
- token 用量：`{"input_tokens": 178931, "cached_input_tokens": 157440, "output_tokens": 6836, "reasoning_output_tokens": 1574}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc "ls -la; echo \"---\"; find . -maxdepth 3 -not -path '*/.git/*' | head -60"
$ /bin/zsh -lc 'cat "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md"'
$ /bin/zsh -lc 'cat PROMPT.md; echo "=== skill dir ==="; ls -la "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/"; echo "=== plain-tool ==="; ls -la plain-tool; echo "=== runtime ==="; ls -la runtime; echo "=== artifacts ==="; ls -la artifacts/synthetic'
$ /bin/zsh -lc 'ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/ 2>/dev/null; echo "---"; /opt/homebrew/opt/python@3.12/bin/python3.12 --version'
$ /bin/zsh -lc 'cat "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/bootstrap.py"; echo "=== diff plain-tool vs skill bootstrap ==="; diff -q "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/bootstrap.py" plain-tool/bootstrap.py && echo IDENTICAL'
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" --help 2>&1 | head -40'
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; RT="$PWD/runtime"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" --runtime-root "$RT" doctor; echo "EXIT=$?"'
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; RT="$PWD/runtime"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" --runtime-root "$RT" cli-path; echo "EXIT=$?"'
$ /bin/zsh -lc 'CLI=$(/opt/homebrew/opt/python@3.12/bin/python3.12 "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/bootstrap.py" --runtime-root "$PWD/runtime" cli-path); echo "CLI=$CLI"; ls -l "$CLI"; shasum -a 256 "$CLI"; echo "--- version ---"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --version; echo "EXIT=$?"'
$ /bin/zsh -lc 'echo "OSKM_CLI=$OSKM_CLI"; env | grep -i oskm; echo "--- ask --help ---"; CLI="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --help 2>&1 | head -50'
$ /bin/zsh -lc 'CLI="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz"; DB="$PWD/artifacts/synthetic/knowledge.db"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --db "$DB" ask get_scan_info; echo "EXIT=$?"'
$ /bin/zsh -lc 'CLI="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --product synthetic ask get_scan_info --format table; echo "EXIT=$?"'
$ /bin/zsh -lc 'CLI="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --product synthetic --format table ask get_scan_info; echo "EXIT=$?"'
$ /bin/zsh -lc 'SKILL_DIR="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/runtime" validate-db "$PWD/artifacts/synthetic/knowledge.db" 2>&1 | head -30; echo "EXIT=${PIPESTATUS[0]}"'
$ /bin/zsh -lc 'CLI="/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --db "$PWD/artifacts/synthetic/knowledge.db" arch overview 2>&1 | head -40; echo "EXIT=${PIPESTATUS[0]}"'
$ /bin/zsh -lc 'echo "HOME=$HOME"; ls -la "$HOME/.oskm" 2>&1 | head -5; echo "--- runtime dir (should still be empty) ---"; ls -la "$PWD/runtime"; echo "--- git status of workspace files ---"; ls -la "$PWD"'
$ /bin/zsh -lc "cat > answer.md <<'EOF'
# e08 合成库冒烟：skill + oskm-cli 组合验证

结论：**通过**。"'`bootstrap.py cli-path` 成功定位到单独构建的 `oskm-cli.pyz`，直接调用该 CLI 能打开
`product=synthetic` 的合成 `knowledge.db` 并返回 `get_scan_info`，快照 `status=complete`，
11 个采集器全部 `complete`。全程未联网、未安装、未触碰 `~/.oskm`。

## 环境

| 项 | 值 |
|---|---|
| Python | 3.12.16 (`/opt/homebrew/opt/python@3.12/bin/python3.12`) |
| SKILL_DIR | `<eval>/home/.codex/skills/ohos-design-architecture-evidence-query` |
| 运行时根 | `<workspace>/runtime`（保持为空，本次不需要 install） |
| CLI | `<fixtures>/oskm-cli.pyz` |
| DB | `<workspace>/artifacts/synthetic/knowledge.db` |

为便于复制，先固定两个变量：

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
```

## 1. 前置检查：`bootstrap.py doctor`

```bash
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/runtime" doctor
```

关键输出：

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
        FAIL: 下载配置无效。请在 <runtime-root>/.env 或 skill 的 oskm_runtime/.env 中配置 OSKM_DOWNLOAD_ENDPOINT…
CLI: /private/…/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: /private/…/e08-synthetic-database-smoke/runtime
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。
EXIT=1
```

两处 FAIL 都是**预期且不影响本次任务**：

- `OSKM_DOWNLOAD_ENDPOINT` 未配置 → 只影响联网下载；本场景夹具已就位，按 skill §5「不要对任意缺失的
  `--db` 路径自动下载」，不跑 `install`。
- `Runtime state: 未安装` → 运行时根目录里没有 `knowledge.db`；本场景直接用 `--db` 指向夹具库，
  不需要把库装进运行时根。

重要的是 CLI 三级解析已命中第一级（`env`，即 `$OSKM_CLI`），并识别出 `oskm-cli 1.0.0`，
三个模块 `oskm_runtime / oskm_cli / oskm_schema` 均可导入。

## 2. `cli-path` 定位 CLI

```bash
CLI=$($PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/runtime" cli-path); echo "$CLI"
```

输出（exit 0）：

```
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz
```

与任务给定的产物一致，实测校验：

```bash
ls -l "$CLI"; shasum -a 256 "$CLI"; $PY "$CLI" --version
```

```
-rwxr-xr-x@ 1 song  staff  83741 Nov 17 15:33 /private/…/fixtures/oskm-cli.pyz
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  /private/…/fixtures/oskm-cli.pyz
oskm-cli 1.0.0
```

大小 83741 bytes、sha256 前缀 `ad760c16b3a56a99…`，与 PROMPT.md 声明完全吻合。

## 3. 直接调 CLI 查 scan 信息

### 3.1 显式 `--db`，默认 JSON

```bash
$PY "$CLI" --db "$PWD/artifacts/synthetic/knowledge.db" ask get_scan_info
```

输出（exit 0，节选）：

```json
{
  "session_id": 1,
  "scan_id": 1,
  "product": "synthetic",
  "cpu_arch": "arm64",
  "workspace_root": "/src",
  "status": "complete",
  "started_at": "2026-11-02T00:00:00Z",
  "finished_at": "2026-11-02T00:00:01Z",
  "collectors": [ … 11 条，见下 … ],
  "attached_aliases": []
}
```

### 3.2 `--product synthetic` + 表格输出

`--format` 是**全局参数**，必须放在子命令 `ask` 之前，否则会报 `unrecognized arguments`（exit 2）：

```bash
$PY "$CLI" --product synthetic --format table ask get_scan_info
```

输出（exit 0）：

```
collector        status    schema_version  record_count
---------------  --------  --------------  ------------
args             complete  4.0.0           1
arkts            complete  4.0.0           1
components       complete  4.0.0           1
elf_modules      complete  4.0.0           1
hdi              complete  4.0.0           1
install_modules  complete  4.0.0           1
links            complete  4.0.0           1
native           complete  4.0.0           1
repos            complete  4.0.0           1
sas              complete  4.0.0           1
services         complete  4.0.0           1
```

`--product synthetic` 由 cwd 推导出 `artifacts/synthetic/knowledge.db`，与显式 `--db` 结果一致。

### 3.3 schema 契约校验（bootstrap 转发给 CLI）

```bash
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/runtime" validate-db "$PWD/artifacts/synthetic/knowledge.db"
```

```
{"path": "/private/…/artifacts/synthetic/knowledge.db", "ok": true}
```

### 3.4 端到端再验一条 `arch` 查询

```bash
$PY "$CLI" --db "$PWD/artifacts/synthetic/knowledge.db" arch overview
```

```json
{
  "product": "synthetic", "scan_id": 1, "subsystems": 2,
  "counts": {"repos":1,"components":2,"install_modules":3,"install_targets":3,
             "elf_modules":0,"services":2,"sas":0,"hdis":1,"gn_args":1,
             "arkts_modules":0,"arkts_kits":0},
  "top_subsystems": [{"key":"graphics","count":1},{"key":"startup","count":1}]
}
```

说明 CLI 不止能读会话元数据，`arch` 编排链路同样可用。

## 4. 证据边界提示（不是失败）

`arch overview` 的 `counts.elf_modules = 0`，而 `get_scan_info` 里 `elf_modules` 采集器
`status=complete, record_count=1`。合成库只有占位行、没有真实 ELF 模块，属夹具设计使然。
按 skill §5 的硬约束：`elf_modules=0` 表示「该证据未采集」，**不能**据此回答依赖/影响面问题，
也不能编造数量。本场景只验组合可运行，不下产品结论。

## 5. 合规性自查

- 未访问、未创建 `~/.oskm`：`ls "$HOME/.oskm"` → `No such file or directory`。
- 未修改 `fixtures/`（只读 + 计算摘要），未修改 `artifacts/synthetic/knowledge.db`。
- `<workspace>/runtime` 仍为空目录，未执行任何 `install` / `refresh` / 联网下载。
- 所有命令都在工作区、夹具目录与 `CODEX_HOME` 内执行；未用 `ps` / `pgrep` / `lsof` 反查宿主进程。

## 6. 对任务的直接回答

1. **CLI 位置**（`bootstrap.py cli-path` 输出）：
   `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz`
   ——经 `$OSKM_CLI` 环境变量解析（doctor 标注来源为 `env`），版本 `oskm-cli 1.0.0`，
   83741 bytes，sha256 `ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e`。
2. **scan 信息**：`scan_id=1`（`session_id=1`），`product=synthetic`，`cpu_arch=arm64`，
   `workspace_root=/src`，`status=complete`，扫描时间 `2026-11-02T00:00:00Z → 00:00:01Z`，
   11 个采集器（args / arkts / components / elf_modules / hdi / install_modules / links /
   native / repos / sas / services）全部 `complete`、`schema_version=4.0.0`、各 `record_count=1`，
   `attached_aliases=[]`。
3. **组合可用性**：skill 的 bootstrap（`doctor` / `cli-path` / `validate-db`）与单独构建的 CLI
   产物可以正常配合工作，`ask` / `arch` 两条查询入口均返回 exit 0。
EOF
wc -l answer.md'
```

### Agent 最终回答

```markdown
验证完成，结论已写入 `answer.md`。

**关键结果**
- `bootstrap.py --runtime-root <workspace>/runtime cli-path` → `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz`（来源 `env`/`$OSKM_CLI`，`oskm-cli 1.0.0`，83741 bytes，sha256 `ad760c16b3a56a99…5eb49e`，与 PROMPT.md 一致）。
- `ask get_scan_info`：`scan_id=1`、`product=synthetic`、`cpu_arch=arm64`、`workspace_root=/src`、`status=complete`，11 个采集器全部 `complete`（`schema_version=4.0.0`、`record_count=1`），`attached_aliases=[]`。
- 旁证：`bootstrap.py validate-db` 返回 `{"ok": true}`；`arch overview` 返回 2 个子系统（`graphics`、`startup`），说明 `arch` 编排链路同样可用。

**注意点**
- `doctor` 以 exit 1 结束，两处 FAIL 是预期的：`OSKM_DOWNLOAD_ENDPOINT` 未配置、运行时根未 install。按 skill §5 不自动下载，改用 `--db`/`--product synthetic` 直指夹具库。
- `--format` 是全局参数，放在 `ask` 之后会报 `unrecognized arguments`（exit 2）；正确写法是 `--product synthetic --format table ask get_scan_info`。
- `arch overview` 的 `elf_modules=0`，合成库只有占位行，不能据此回答依赖/影响面问题。

**合规**
- 未访问或创建 `~/.oskm`；`fixtures/` 与 `artifacts/synthetic/knowledge.db` 未修改；`runtime/` 仍为空，无联网 install/refresh。

需要我把 `runtime` 也真正 `install` 一遍（需要配置 `OSKM_DOWNLOAD_ENDPOINT`，或从 `fixtures/knowledge.tar.gz` 本地安装）来跑一次完整运行时路径吗？
```

### Agent 写入的 answer.md

```markdown
# e08 合成库冒烟：skill + oskm-cli 组合验证

结论：**通过**。`bootstrap.py cli-path` 成功定位到单独构建的 `oskm-cli.pyz`，直接调用该 CLI 能打开
`product=synthetic` 的合成 `knowledge.db` 并返回 `get_scan_info`，快照 `status=complete`，
11 个采集器全部 `complete`。全程未联网、未安装、未触碰 `~/.oskm`。

## 环境

| 项 | 值 |
|---|---|
| Python | 3.12.16 (`/opt/homebrew/opt/python@3.12/bin/python3.12`) |
| SKILL_DIR | `<eval>/home/.codex/skills/ohos-design-architecture-evidence-query` |
| 运行时根 | `<workspace>/runtime`（保持为空，本次不需要 install） |
| CLI | `<fixtures>/oskm-cli.pyz` |
| DB | `<workspace>/artifacts/synthetic/knowledge.db` |

为便于复制，先固定两个变量：

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
SKILL_DIR="$CODEX_HOME/skills/ohos-design-architecture-evidence-query"
```

## 1. 前置检查：`bootstrap.py doctor`

```bash
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/runtime" doctor
```

关键输出：

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
        FAIL: 下载配置无效。请在 <runtime-root>/.env 或 skill 的 oskm_runtime/.env 中配置 OSKM_DOWNLOAD_ENDPOINT…
CLI: /private/…/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: /private/…/e08-synthetic-database-smoke/runtime
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
错误: 运行时依赖检查未通过。
EXIT=1
```

两处 FAIL 都是**预期且不影响本次任务**：

- `OSKM_DOWNLOAD_ENDPOINT` 未配置 → 只影响联网下载；本场景夹具已就位，按 skill §5「不要对任意缺失的
  `--db` 路径自动下载」，不跑 `install`。
- `Runtime state: 未安装` → 运行时根目录里没有 `knowledge.db`；本场景直接用 `--db` 指向夹具库，
  不需要把库装进运行时根。

重要的是 CLI 三级解析已命中第一级（`env`，即 `$OSKM_CLI`），并识别出 `oskm-cli 1.0.0`，
三个模块 `oskm_runtime / oskm_cli / oskm_schema` 均可导入。

## 2. `cli-path` 定位 CLI

```bash
CLI=$($PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/runtime" cli-path); echo "$CLI"
```

输出（exit 0）：

```
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz
```

与任务给定的产物一致，实测校验：

```bash
ls -l "$CLI"; shasum -a 256 "$CLI"; $PY "$CLI" -
… [输出截断，完整内容见工作区] …
改 `artifacts/synthetic/knowledge.db`。
- `<workspace>/runtime` 仍为空目录，未执行任何 `install` / `refresh` / 联网下载。
- 所有命令都在工作区、夹具目录与 `CODEX_HOME` 内执行；未用 `ps` / `pgrep` / `lsof` 反查宿主进程。

## 6. 对任务的直接回答

1. **CLI 位置**（`bootstrap.py cli-path` 输出）：
   `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz`
   ——经 `$OSKM_CLI` 环境变量解析（doctor 标注来源为 `env`），版本 `oskm-cli 1.0.0`，
   83741 bytes，sha256 `ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e`。
2. **scan 信息**：`scan_id=1`（`session_id=1`），`product=synthetic`，`cpu_arch=arm64`，
   `workspace_root=/src`，`status=complete`，扫描时间 `2026-11-02T00:00:00Z → 00:00:01Z`，
   11 个采集器（args / arkts / components / elf_modules / hdi / install_modules / links /
   native / repos / sas / services）全部 `complete`、`schema_version=4.0.0`、各 `record_count=1`，
   `attached_aliases=[]`。
3. **组合可用性**：skill 的 bootstrap（`doctor` / `cli-path` / `validate-db`）与单独构建的 CLI
   产物可以正常配合工作，`ask` / `arch` 两条查询入口均返回 exit 0。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
验证完成，结论已写入 `answer.md`。

**关键结果**
- `bootstrap.py --runtime-root <workspace>/runtime cli-path` → `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz`（来源 `env`/`$OSKM_CLI`，`oskm-cli 1.0.0`，83741 bytes，sha256 `ad760c16b3a56a99…5eb49e`，与 PROMPT.md 一致）。
- `ask get_scan_info`：`scan_id=1`、`product=synthetic`、`cpu_arch=arm64`、`workspace_root=/src`、`status=complete`，11 个采集器全部 `complete`（`schema_version=4.0.0`、`record_count=1`），`attached_aliases=[]`。
- 旁证：`bootstrap.py validate-db` 返回 `{"ok": true}`；`arch overview` 返回 2 个子系统（`graphics`、`startup`），说明 `arch` 编排链路同样可用。

**注意点**
- `doctor` 以 exit 1 结束，两处 FAIL 是预期的：`OSKM_DOWNLOAD_ENDPOINT` 未配置、运行时根未 install。按 skill §5 不自动下载，改用 `--db`/`--product synthetic` 直指夹具库。
- `--format` 是全局参数，放在 `ask` 之后会报 `unrecognized arguments`（exit 2）；正确写法是 `--product synthetic --format table ask get_scan_info`。
- `arch overview` 的 `elf_modules=0`，合成库只有占位行，不能据此回答依赖/影响面问题。

**合规**
- 未访问或创建 `~/.oskm`；`fixtures/` 与 `artifacts/synthetic/knowledge.db` 未修改；`runtime/` 仍为空，无联网 install/refresh。

需要我把 `runtime` 也真正 `install` 一遍（需要配置 `OSKM_DOWNLOAD_ENDPOINT`，或从 `fixtures/knowledge.tar.gz` 本地安装）来跑一次完整运行时路径吗？
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e08-synthetic-database-smoke` · exit=0 · 200.1s

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

自动断言 5/5 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 回答里出现 get_scan_info | auto | Pass | answer/输出中出现 get_scan_info |
| 2 | 回答里出现 synthetic | auto | Pass | answer/输出中出现 synthetic |
| 3 | 是否明确说明该场景只验证组合链路、不代表真实产品数据 | manual | 人工 | 验证完成，结论已写入 `answer.md`。  **关键结果** - `bootstrap.py --runtime-root <workspace>/runtime cli-path` → `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-c
… [输出截断，完整内容见工作区] …
]`。 - 旁证：`bootstrap.py validate-db` 返回 `{"ok": true}`；`arch overview` 返回 2 个子系统（`graphics`、`startup` |
| 4 | 查询是只读的：合成库 sha256 未变 | auto | Pass | sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 |
| 5 | 工具没有联网 | auto | Pass | [] |
| 6 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
