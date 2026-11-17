# E8 synthetic-database-smoke（with-skill 臂）

- 开始时间：2026-11-17T16:26:33+08:00
- 结束时间：2026-11-17T16:31:03+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke`
- 夹具服务端：http://127.0.0.1:62119
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：241.2 s
- 事件计数：`{"thread.started": 1, "item.completed": 39, "item:error": 1, "turn.started": 1, "item:reasoning": 11, "item:agent_message": 10, "item.started": 17, "item:command_execution": 34, "turn.completed": 1}`
- 读到 skill 文档：是（9 处）
- 执行的命令数：17
- token 用量：`{"input_tokens": 211952, "cached_input_tokens": 190720, "output_tokens": 6844, "reasoning_output_tokens": 1284}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke'
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && ls -la && sed -n '80,140p' SKILL.md"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && cat PROMPT.md && find artifacts runtime plain-tool -maxdepth 3 | head -50'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/bootstrap.py && /opt/homebrew/opt/python@3.12/bin/python3.12 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/bootstrap.py --help'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/ && shasum -a 256 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz && ls -la artifacts/synthetic/ runtime/'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query; RT="$PWD/runtime"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$RT"; echo "EXIT=$?"'
$ /bin/zsh -lc 'ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/source /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/cli-tree'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query; RT="$PWD/runtime"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" cli-path --runtime-root "$RT"; echo "EXIT=$?"; env | grep -i -E '"'OSKM|OPENHARMONY' | sed 's/"'^/ENV /'"'"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && CLI="$(/opt/homebrew/opt/python@3.12/bin/python3.12 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/bootstrap.py cli-path --runtime-root "$PWD/runtime")"; echo "CLI=$CLI"; DB="$PWD/artifacts/synthetic/knowledge.db"; /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --version; /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" --help 2>&1 | head -40'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz; /opt/homebrew/opt/python@3.12/bin/python3.12 "$CLI" ask --list 2>&1 | grep -i -E '"'scan|session' "
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz; DB="$PWD/artifacts/synthetic/knowledge.db"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; $PY "$CLI" --db "$DB" ask get_scan_info; echo "EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz; DB="$PWD/artifacts/synthetic/knowledge.db"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; $PY "$CLI" --db "$DB" --format table ask list_scans; echo "EXIT=$?"; $PY "$CLI" --product synthetic --format table ask get_scan_info; echo "PRODUCT_EXIT=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz; DB="$PWD/artifacts/synthetic/knowledge.db"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; $PY "$CLI" validate-db "$DB" 2>&1 | tail -20; echo "VALIDATE_EXIT=${PIPESTATUS[0]}"; $PY "$CLI" --db "$DB" --format table arch overview 2>&1 | head -25'
$ /bin/zsh -lc 'ls -la "$HOME/.oskm" 2>&1 | head -5; echo "---runtime---"; ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke/runtime'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz; DB="$PWD/artifacts/synthetic/knowledge.db"; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; $PY "$CLI" validate-db "$DB" >/dev/null; echo "VALIDATE_EXIT=$?"; $PY "$CLI" --db "$DB" arch overview; echo "OVERVIEW_EXIT=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke && cat > answer.md <<'EOF'
# e08 合成库冒烟：skill + oskm-cli.pyz 组合验证

## 结论（直接回答）

- **成功**：用 skill 的 "'`bootstrap.py cli-path` 定位到单独构建的 CLI，再直接调 CLI 查到了 scan 信息，全链路跑通，所有命令退出码为 `0`。
- **CLI 定位结果**：`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz`，解析来源为 `env`（环境变量 `OSKM_CLI`），版本 `oskm-cli 1.0.0`；`sha256=3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5`、`84742 bytes`，与任务给出的夹具一致。
- **scan 信息**：`product=synthetic`、`scan_id=1`、`cpu_arch=arm64`、`status=complete`、`workspace_root=/src`、`started_at=2026-11-02T00:00:00Z`、`finished_at=2026-11-02T00:00:01Z`；11 个采集器（args / arkts / components / elf_modules / hdi / install_modules / links / native / repos / sas / services）全部 `status=complete`、`schema_version=4.0.0`、`record_count=1`，无 `degraded`。
- **未安装、未联网**：没有跑 `install` / `refresh`（`doctor` 提示下载端点未配置，属预期）；查询全部走显式 `--db`，不触发任何下载。
- **边界遵守**：`~/.oskm` 不存在（未被创建或修改），`runtime/` 仍为空目录，`fixtures/` 只读未改动。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query
RT="$PWD/runtime"          # 任务指定的运行时根目录（非 ~/.oskm）
DB="$PWD/artifacts/synthetic/knowledge.db"

# 1) 校验夹具 CLI 摘要
shasum -a 256 /private/var/.../fixtures/oskm-cli.pyz

# 2) 运行时体检
$PY "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$RT"

# 3) 定位 CLI（本次任务要求的入口）
CLI=$($PY "$SKILL_DIR/bootstrap.py" cli-path --runtime-root "$RT")

# 4) 直接调 CLI 查 scan 信息
$PY "$CLI" --version
$PY "$CLI" --db "$DB" ask get_scan_info
$PY "$CLI" --db "$DB" --format table ask list_scans
$PY "$CLI" --product synthetic --format table ask get_scan_info   # 由 artifacts/<product>/knowledge.db 推导，同样成功

# 5) 附加冒烟：库契约校验 + 顶层架构概览
$PY "$CLI" validate-db "$DB"
$PY "$CLI" --db "$DB" arch overview
```

## 关键输出片段

`bootstrap.py doctor --runtime-root <workspace>/runtime`（退出码 1，仅因下载端点未配置；CLI 与模块检查均 OK）：

```text
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
        FAIL: 下载配置无效。请在 <runtime-root>/.env 或 skill 的 oskm_runtime/.env 中配置 OSKM_DOWNLOAD_ENDPOINT…
CLI: /private/var/.../fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: /private/var/.../e08-synthetic-database-smoke/runtime
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
```

`bootstrap.py cli-path`（退出码 0）：

```text
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz
```

`ask get_scan_info`（退出码 0，节选）：

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
  "collectors": [
    {"collector": "args", "status": "complete", "schema_version": "4.0.0", "record_count": 1},
    {"collector": "components", "status": "complete", "schema_version": "4.0.0", "record_count": 1},
    {"collector": "elf_modules", "status": "complete", "schema_version": "4.0.0", "record_count": 1}
  ],
  "attached_aliases": []
}
```

`--format table ask list_scans`：

```text
scan_id  product    cpu_arch  started_at            finished_at           status
-------  ---------  --------  --------------------  --------------------  --------
1        synthetic  arm64     2026-11-02T00:00:00Z  2026-11-02T00:00:01Z  complete
```

`validate-db` 与 `arch overview`（均退出码 0）：

```text
{"path": ".../artifacts/synthetic/knowledge.db", "ok": true}
```

```json
{"product": "synthetic", "scan_id": 1, "subsystems": 2,
 "counts": {"repos": 1, "components": 2, "install_modules": 3, "install_targets": 3,
            "elf_modules": 0, "services": 2, "sas": 0, "hdis": 1, "gn_args": 1,
            "arkts_modules": 0, "arkts_kits": 0},
 "top_subsystems": [{"key": "graphics", "count": 1}, {"key": "startup", "count": 1}]}
```

## 备注

- `doctor` 的 `FAIL` 只影响 `install`/`refresh` 的下载配置；本次不需要安装，CLI 已由 `OSKM_CLI` 解析到夹具产物，查询链路完整可用。
- 合成库中 `arch overview` 的 `counts.elf_modules=0`（`elf_modules` 采集器 `record_count=1`，但无 ELF 模块明细行）。按 skill 约束，这类计数为 0 的证据不可用于回答依赖/影响面问题；本场景只验证组合可运行，未做此类推断。
EOF
echo "written"; wc -l answer.md'
```

### Agent 最终回答

```markdown
跑通了，结论已写入 `answer.md`。

**验证结果**
- `bootstrap.py cli-path --runtime-root <workspace>/runtime` → `/private/var/…/fixtures/oskm-cli.pyz`（来源 `env`，即 `OSKM_CLI`），`--version` 报 `oskm-cli 1.0.0`，`sha256=3e78cf73a94bcf9d…`、84742 bytes 与夹具一致。
- `doctor` 的 Python/CLI/模块检查全部 OK；唯一 `FAIL` 是下载端点未配置（退出码 1），本次不安装所以不影响。
- CLI 直查 scan 信息成功：`product=synthetic`、`scan_id=1`、`cpu_arch=arm64`、`status=complete`、`workspace_root=/src`、`2026-11-02T00:00:00Z → 00:00:01Z`，11 个采集器全 `complete`、`schema_version=4.0.0`、`record_count=1`，无 `degraded`。
- 附加冒烟：`validate-db` → `{"ok": true}`；`arch overview` → 2 个子系统（`graphics`、`startup`），退出码均为 0。
- `--product synthetic` 推导路径也能查到同一份 scan 信息，两种方式等价。

**关键命令**
- `python3.12 $SKILL_DIR/bootstrap.py doctor --runtime-root "$PWD/runtime"`
- `CLI=$(python3.12 $SKILL_DIR/bootstrap.py cli-path --runtime-root "$PWD/runtime")`
- `python3.12 "$CLI" --db "$PWD/artifacts/synthetic/knowledge.db" ask get_scan_info`
- `python3.12 "$CLI" --db "$DB" --format table ask list_scans` / `--product synthetic … get_scan_info`

**边界**
- 未跑 `install`/`refresh`，无联网下载；查询全程显式 `--db`。
- `~/.oskm` 不存在（未创建），`runtime/` 仍为空，`fixtures/` 只读未改。
- 合成库 `counts.elf_modules=0`，按 skill 约束不据此回答依赖/影响面问题。

明细见 `answer.md:1`。需要的话我可以再补一条 `sql --file` 聚合查询或 `diff` 跨快照对比的冒烟。
```

### Agent 写入的 answer.md

```markdown
# e08 合成库冒烟：skill + oskm-cli.pyz 组合验证

## 结论（直接回答）

- **成功**：用 skill 的 `bootstrap.py cli-path` 定位到单独构建的 CLI，再直接调 CLI 查到了 scan 信息，全链路跑通，所有命令退出码为 `0`。
- **CLI 定位结果**：`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz`，解析来源为 `env`（环境变量 `OSKM_CLI`），版本 `oskm-cli 1.0.0`；`sha256=3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5`、`84742 bytes`，与任务给出的夹具一致。
- **scan 信息**：`product=synthetic`、`scan_id=1`、`cpu_arch=arm64`、`status=complete`、`workspace_root=/src`、`started_at=2026-11-02T00:00:00Z`、`finished_at=2026-11-02T00:00:01Z`；11 个采集器（args / arkts / components / elf_modules / hdi / install_modules / links / native / repos / sas / services）全部 `status=complete`、`schema_version=4.0.0`、`record_count=1`，无 `degraded`。
- **未安装、未联网**：没有跑 `install` / `refresh`（`doctor` 提示下载端点未配置，属预期）；查询全部走显式 `--db`，不触发任何下载。
- **边界遵守**：`~/.oskm` 不存在（未被创建或修改），`runtime/` 仍为空目录，`fixtures/` 只读未改动。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query
RT="$PWD/runtime"          # 任务指定的运行时根目录（非 ~/.oskm）
DB="$PWD/artifacts/synthetic/knowledge.db"

# 1) 校验夹具 CLI 摘要
shasum -a 256 /private/var/.../fixtures/oskm-cli.pyz

# 2) 运行时体检
$PY "$SKILL_DIR/bootstrap.py" doctor --runtime-root "$RT"

# 3) 定位 CLI（本次任务要求的入口）
CLI=$($PY "$SKILL_DIR/bootstrap.py" cli-path --runtime-root "$RT")

# 4) 直接调 CLI 查 scan 信息
$PY "$CLI" --version
$PY "$CLI" --db "$DB" ask get_scan_info
$PY "$CLI" --db "$DB" --format table ask list_scans
$PY "$CLI" --product synthetic --format table ask get_scan_info   # 由 artifacts/<product>/knowledge.db 推导，同样成功

# 5) 附加冒烟：库契约校验 + 顶层架构概览
$PY "$CLI" validate-db "$DB"
$PY "$CLI" --db "$DB" arch overview
```

## 关键输出片段

`bootstrap.py doctor --runtime-root <workspace>/runtime`（退出码 1，仅因下载端点未配置；CLI 与模块检查均 OK）：

```text
Python: 3.12.16 (OK, requires Python 3.10+)
Source / En
… [输出截断，完整内容见工作区] …
``text
scan_id  product    cpu_arch  started_at            finished_at           status
-------  ---------  --------  --------------------  --------------------  --------
1        synthetic  arm64     2026-11-02T00:00:00Z  2026-11-02T00:00:01Z  complete
```

`validate-db` 与 `arch overview`（均退出码 0）：

```text
{"path": ".../artifacts/synthetic/knowledge.db", "ok": true}
```

```json
{"product": "synthetic", "scan_id": 1, "subsystems": 2,
 "counts": {"repos": 1, "components": 2, "install_modules": 3, "install_targets": 3,
            "elf_modules": 0, "services": 2, "sas": 0, "hdis": 1, "gn_args": 1,
            "arkts_modules": 0, "arkts_kits": 0},
 "top_subsystems": [{"key": "graphics", "count": 1}, {"key": "startup", "count": 1}]}
```

## 备注

- `doctor` 的 `FAIL` 只影响 `install`/`refresh` 的下载配置；本次不需要安装，CLI 已由 `OSKM_CLI` 解析到夹具产物，查询链路完整可用。
- 合成库中 `arch overview` 的 `counts.elf_modules=0`（`elf_modules` 采集器 `record_count=1`，但无 ELF 模块明细行）。按 skill 约束，这类计数为 0 的证据不可用于回答依赖/影响面问题；本场景只验证组合可运行，未做此类推断。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
跑通了，结论已写入 `answer.md`。

**验证结果**
- `bootstrap.py cli-path --runtime-root <workspace>/runtime` → `/private/var/…/fixtures/oskm-cli.pyz`（来源 `env`，即 `OSKM_CLI`），`--version` 报 `oskm-cli 1.0.0`，`sha256=3e78cf73a94bcf9d…`、84742 bytes 与夹具一致。
- `doctor` 的 Python/CLI/模块检查全部 OK；唯一 `FAIL` 是下载端点未配置（退出码 1），本次不安装所以不影响。
- CLI 直查 scan 信息成功：`product=synthetic`、`scan_id=1`、`cpu_arch=arm64`、`status=complete`、`workspace_root=/src`、`2026-11-02T00:00:00Z → 00:00:01Z`，11 个采集器全 `complete`、`schema_version=4.0.0`、`record_count=1`，无 `degraded`。
- 附加冒烟：`validate-db` → `{"ok": true}`；`arch overview` → 2 个子系统（`graphics`、`startup`），退出码均为 0。
- `--product synthetic` 推导路径也能查到同一份 scan 信息，两种方式等价。

**关键命令**
- `python3.12 $SKILL_DIR/bootstrap.py doctor --runtime-root "$PWD/runtime"`
- `CLI=$(python3.12 $SKILL_DIR/bootstrap.py cli-path --runtime-root "$PWD/runtime")`
- `python3.12 "$CLI" --db "$PWD/artifacts/synthetic/knowledge.db" ask get_scan_info`
- `python3.12 "$CLI" --db "$DB" --format table ask list_scans` / `--product synthetic … get_scan_info`

**边界**
- 未跑 `install`/`refresh`，无联网下载；查询全程显式 `--db`。
- `~/.oskm` 不存在（未创建），`runtime/` 仍为空，`fixtures/` 只读未改。
- 合成库 `counts.elf_modules=0`，按 skill 约束不据此回答依赖/影响面问题。

明细见 `answer.md:1`。需要的话我可以再补一条 `sql --file` 聚合查询或 `diff` 跨快照对比的冒烟。
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e08-synthetic-database-smoke` · exit=0 · 241.2s

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
| 3 | 是否明确说明该场景只验证组合链路、不代表真实产品数据 | manual | 人工 | 跑通了，结论已写入 `answer.md`。  **验证结果** - `bootstrap.py cli-path --runtime-root <workspace>/runtime` → `/private/var/…/fixtures/oskm-cli.pyz`（来源 `env`，即 `OSKM_CLI`），`--version` 报 `oskm-cli 1.0.0`，`sha256=3e7
… [输出截断，完整内容见工作区] …
_count=1`，无 `degraded`。 - 附加冒烟：`validate-db` → `{"ok": true}`；`arch overview` → 2 个子系统（`graphics`、`s |
| 4 | 查询是只读的：合成库 sha256 未变 | auto | Pass | sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 |
| 5 | 工具没有联网 | auto | Pass | [] |
| 6 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
