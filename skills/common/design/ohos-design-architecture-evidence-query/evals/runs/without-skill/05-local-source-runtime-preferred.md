# E5 local-source-runtime-preferred（without-skill 臂）

- 开始时间：2026-11-17T15:37:14+08:00
- 结束时间：2026-11-17T15:42:34+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred`
- 夹具服务端：http://127.0.0.1:61302
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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：320.2 s
- 事件计数：`{"thread.started": 1, "item.completed": 54, "item:error": 1, "turn.started": 1, "item:reasoning": 18, "item:agent_message": 11, "item.started": 24, "item:command_execution": 48, "turn.completed": 1}`
- 读到 skill 文档：否
- 执行的命令数：24
- token 用量：`{"input_tokens": 509670, "cached_input_tokens": 465152, "output_tokens": 10465, "reasoning_output_tokens": 3927}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred && ls -la && echo "---- tool ----" && find tool -type f | head -50 && echo "---- source top ----" && ls -la source'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred && echo "ENV:" && env | grep -i -E "oskm|download" ; echo "---- runtime ----" && ls -la runtime 2>/dev/null'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/tool && wc -l bootstrap.py oskm_runtime/*.py oskm_runtime/.env.example && echo "==== bootstrap.py ====" && cat bootstrap.py && echo "==== __main__.py ====" && cat oskm_runtime/__main__.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/tool && cat oskm_runtime/bootstrap.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/tool && sed -n '130,200p' oskm_runtime/bootstrap.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/tool && cat oskm_runtime/cli_install.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/tool && cat oskm_runtime/install.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/tool && sed -n '130,300p' oskm_runtime/install.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/tool && cat oskm_runtime/environment.py && echo "==== .env.example ====" && cat oskm_runtime/.env.example && echo "==== state.py ====" && cat oskm_runtime/state.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/tool && sed -n '120,215p' oskm_runtime/cli_install.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/tool && sed -n '1,60p' oskm_runtime/state.py && echo \"==== doctor.py ====\" && cat oskm_runtime/doctor.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source && cat .gn && echo \"---- tree ----\" && find . -not -path './.git/*' | sort && echo \"---- sizes ----\" && ls -la cli/dist out/sample-product/oskm 2>/dev/null"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source && which python3 && python3 -VV && /opt/homebrew/opt/python@3.12/bin/python3.12 -VV && head -c 60 cli/dist/oskm-cli.pyz | head -1 && echo && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import zipfile
z=zipfile.ZipFile('cli/dist/oskm-cli.pyz')
names=z.namelist()
print(len(names),'entries')
print([n for n in names if n.count('/')<=1][:40])
print('database.py present:', 'oskm_cli/database.py' in names)
\""
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import sqlite3
c=sqlite3.connect('file:out/sample-product/oskm/knowledge.db?mode=ro',uri=True)
print([r[0] for r in c.execute(\\\"select name from sqlite_master where type='table' order by name\\\")])
print('scans rows:', c.execute('select count(*) from scans').fetchone())
\""
$ /bin/zsh -lc 'which python3.12; cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY ../tool/bootstrap.py doctor; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred && $PY ../tool/bootstrap.py --runtime-root "$WS/runtime" install --source-root "$WS/source"; echo "exit=$?"'
$ /bin/zsh -lc 'WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred; cd "$WS/source" && find "$WS/runtime" -not -path '"'*/.oskm-runtime-backup*' | sort && echo \"==== state ====\" && cat \""'$WS/runtime/.oskm-runtime.json"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY ../tool/bootstrap.py doctor; echo "doctor exit=$?"; echo "==== cli-path ===="; $PY ../tool/bootstrap.py cli-path; echo "==== refresh ===="; $PY ../tool/bootstrap.py refresh; echo "refresh exit=$?"'
$ /bin/zsh -lc 'WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; cd "$WS/source" && $PY ../tool/bootstrap.py validate-db "$WS/runtime/knowledge.db"; echo "validate exit=$?"; echo "==== --version ===="; $PY "$WS/runtime/oskm-cli.pyz" --version; echo "==== --help ===="; $PY "$WS/runtime/oskm-cli.pyz" --help 2>&1 | head -40'
$ /bin/zsh -lc 'WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; cd "$WS/source" && echo "==== arch --help ====" && $PY "$WS/runtime/oskm-cli.pyz" arch --help 2>&1 | head -20 && echo "==== arch overview ====" && $PY "$WS/runtime/oskm-cli.pyz" --db "$WS/runtime/knowledge.db" arch overview 2>&1 | head -40'
$ /bin/zsh -lc 'WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; cd "$WS/source" && OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:9/internal $PY ../tool/bootstrap.py --runtime-root "$WS/runtime" install --source-root "$WS/source" 2>&1; echo "exit=${PIPESTATUS[0]:-$?}"'
$ /bin/zsh -lc 'WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; cd "$WS/source" && echo "==== install (auto-discover from cwd) ====" && $PY ../tool/bootstrap.py install 2>&1 && echo "==== integrity ====" && shasum -a 256 out/sample-product/oskm/knowledge.db "$WS/runtime/knowledge.db" cli/dist/oskm-cli.pyz "$WS/runtime/oskm-cli.pyz" && echo "==== source tree unchanged ====" && find . -newer .gn -not -name '"'answer.md' | sort && ls -la \""'$WS/runtime"'
$ /bin/zsh -lc 'WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred; PY=/opt/homebrew/opt/python@3.12/bin/python3.12; cd "$WS/source" && $PY "$WS/runtime/oskm-cli.pyz" --db "$WS/runtime/knowledge.db" ask --list 2>&1 | head -12 && echo "==== arch provides sample ====" && $PY "$WS/runtime/oskm-cli.pyz" --db "$WS/runtime/knowledge.db" --format table arch overview 2>&1 | head -20'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source && cat > answer.md <<'EOF'
# OSKM 托管运行时安装结论（本地源码根优先，零下载）

## 直接回答

- 当前目录就是完整 OpenHarmony 源码根（"'`.gn` 为文件、`interface/sdk-js` 与 `interface/sdk_c` 非空、`out/` 存在），
  并且 `out/sample-product/oskm/knowledge.db` 与 `cli/dist/oskm-cli.pyz` 都在。
- 因此**正确做法是用源码树本地构建装运行时，不联网**：在源码根执行 `bootstrap.py install`
  （或显式 `--source-root <源码根>`）。`install` 内部的 `find_local_runtime()` 会命中
  DB + 两套 SDK + 自带 `oskm_cli.database` 的 pyz，走 `_stage_local_runtime()` 复制安装，
  完全跳过 `download_runtime_bundle()`，所以配置的 `OSKM_DOWNLOAD_ENDPOINT` 一次都没被请求。
- 运行时已装到 `OSKM_RUNTIME_ROOT`：`../runtime/`，含 `knowledge.db`、`oskm-cli.pyz`、
  `interface/sdk-js`、`interface/sdk_c`、`.oskm-runtime.json`（`"source": "local"`）。
- `doctor` 全绿（exit 0），`refresh` 判定"已是最新"（`source=local` 时不按日期强刷），
  `validate-db` 返回 `{"ok": true}`，`arch overview` / `ask --list` 正常出结果。
- 坑点：`/usr/bin/python3` 是 **3.9.6**，低于 skill 要求的 3.10+，且 pyz 的 shebang 是
  `#!/usr/bin/env python3`。必须用 `/opt/homebrew/opt/python@3.12/bin/python3.12` 显式调用
  （`python3.12` 也在 PATH 上），别直接 `./oskm-cli.pyz`。
- 未访问、未修改 `~/.oskm`；源码树文件 sha256 与 mtime 保持不变。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred
cd "$WS/source"                      # cwd 必须是源码根或其子目录，否则探测不到本地构建

# 1) 安装前体检：已经提示检测到源码根本地构建、install 不联网
$PY ../tool/bootstrap.py doctor

# 2) 安装（本地源码根优先；OSKM_RUNTIME_ROOT 已在环境里，这里再显式写一次）
$PY ../tool/bootstrap.py --runtime-root "$WS/runtime" install --source-root "$WS/source"

# 3) 安装后校验
$PY ../tool/bootstrap.py doctor
$PY ../tool/bootstrap.py cli-path
$PY ../tool/bootstrap.py refresh
$PY ../tool/bootstrap.py validate-db "$WS/runtime/knowledge.db"

# 4) 用装好的 CLI 查询（固定文件名，不带版本号）
$PY "$WS/runtime/oskm-cli.pyz" --version
$PY "$WS/runtime/oskm-cli.pyz" --db "$WS/runtime/knowledge.db" arch overview
$PY "$WS/runtime/oskm-cli.pyz" --db "$WS/runtime/knowledge.db" ask --list

# 5) 离线证明：把端点换成不可达地址再装一次，仍然成功 => 全程没有 HTTP 请求
OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:9/internal '"\\
  "'$PY ../tool/bootstrap.py --runtime-root "$WS/runtime" install --source-root "$WS/source"
```

## 关键输出片段

安装（走本地，无 `==> 下载 INTERNAL_CI 运行时` 这一行）：

```
==> 使用源码本地运行时: .../source/out/sample-product/oskm/knowledge.db
==> 运行时安装完成: .../runtime
```

安装前 `doctor`（exit 1，CLI 未装，但已给出本地构建提示）：

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。...
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
提示: 检测到源码根本地构建: .../source/out/sample-product/oskm/knowledge.db
      在源码根或其子目录执行 bootstrap.py install，或传 --source-root <path>，将优先使用本地构建，不联网。
```

安装后 `doctor`（exit 0）：

```
Python: 3.12.16 (OK, requires Python 3.10+)
CLI: .../runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime state: version 3, date 20261117, source local, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
```

`refresh`（幂等，不再触发任何下载）：

```
==> 运行时已是最新，无需刷新: .../runtime
```

schema 契约与查询：

```
{"path": ".../runtime/knowledge.db", "ok": true}
oskm-cli 1.0.0
{ "product": "synthetic", "scan_id": 1, "subsystems": 2,
  "counts": { "repos": 1, "components": 2, "install_modules": 3, "services": 2, "hdis": 1, ... },
  "top_subsystems": [ {"key": "graphics", "count": 1}, {"key": "startup", "count": 1} ] }
```

`.oskm-runtime.json`（`source: local` + `source_root` 指向源码树，说明出处是本地构建）：

```json
{ "version": 3, "source": "local", "date": "20261117",
  "source_root": ".../e05-local-source-runtime-preferred/source",
  "db":  { "date": "20261117", "path": "knowledge.db", "sha256": "f561e39f...fcd1b44" },
  "sdk": { "date": "20261117", "sdk-js": {"path": "interface/sdk-js"}, "sdk_c": {"path": "interface/sdk_c"} },
  "cli": { "path": "oskm-cli.pyz", "sha256": "ad760c16...cd5eb49e" } }
```

产物一致性（运行时里的 DB/CLI 与源码树逐字节相同）：

```
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  out/sample-product/oskm/knowledge.db
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  .../runtime/knowledge.db
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  cli/dist/oskm-cli.pyz
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  .../runtime/oskm-cli.pyz
```

离线证明（端点换成 127.0.0.1:9 仍成功）：

```
==> 使用源码本地运行时: .../source/out/sample-product/oskm/knowledge.db
==> 运行时安装完成: .../runtime
exit=0
```

## 复现要点 / 常见错误

- 不在源码根（或其子目录）执行且不给 `--source-root`：`_candidate_source_roots()` 只从 cwd 向上探测，
  探测不到就回退 `_download_bundle()`，那时才会真的打 `OSKM_DOWNLOAD_ENDPOINT`。
- `--source-root` 是权威参数：路径不是合法源码根会直接 `ValueError: 不是有效的 OpenHarmony 源码根`，
  不会静默退回 cwd 或联网。
- 本地构建缺任一条件都会静默回退下载：两套 SDK 目录必须非空、必须找到结构合格的
  `oskm-cli.pyz`（shebang + zip + `__main__.py` + `oskm_cli/cli.py` + CRC）、且该 pyz 必须能给出
  `oskm_cli.database.validate_db`，DB 还要通过 schema 校验。本夹具四项全满足。
- 回退发生时的信号是 stderr 上多出一行 `==> 下载 INTERNAL_CI 运行时: <date>`；本次没有这一行。
EOF
wc -l answer.md && ls -la answer.md'
```

### Agent 最终回答

```markdown
**装好了**
- 用本地源码根安装，全程零下载：`install` 命中 `out/sample-product/oskm/knowledge.db` + `cli/dist/oskm-cli.pyz`，走 `_stage_local_runtime()` 复制安装，跳过 `download_runtime_bundle()`。
- 运行时落在 `$OSKM_RUNTIME_ROOT`（`../runtime/`）：`knowledge.db`、`oskm-cli.pyz`、`interface/sdk-js`、`interface/sdk_c`、`.oskm-runtime.json`（`"source": "local"`）。
- `doctor` exit 0（`db=✓ sdk=✓ cli=✓`，oskm-cli 1.0.0）；`refresh` 报"已是最新"；`validate-db` 返回 `{"ok": true}`；`arch overview` / `ask --list` 正常出结果。

**关键命令**
- `/opt/homebrew/opt/python@3.12/bin/python3.12 ../tool/bootstrap.py doctor`
- `... bootstrap.py --runtime-root "$WS/runtime" install --source-root "$WS/source"`
- `... bootstrap.py validate-db "$WS/runtime/knowledge.db"`
- `python3.12 "$WS/runtime/oskm-cli.pyz" --db "$WS/runtime/knowledge.db" arch overview`

**零联网的证据**
- 安装日志只有 `==> 使用源码本地运行时` 与 `==> 运行时安装完成`，没有 `==> 下载 INTERNAL_CI 运行时` 那一行。
- 把 `OSKM_DOWNLOAD_ENDPOINT` 换成不可达的 `http://127.0.0.1:9/internal` 再装一次，仍然 exit 0 → 说明安装路径不依赖端点，夹具服务不会收到请求。
- 运行时 DB/CLI 与源码树 sha256 完全一致，源码树 mtime 未变；未触碰 `~/.oskm`。

**两个坑**
- `/usr/bin/python3` 是 3.9.6，低于 skill 的 3.10+ 要求，且 pyz shebang 是 `#!/usr/bin/env python3`；必须用 `python3.12` 显式调用，不要 `./oskm-cli.pyz`。
- `install` 只在 cwd 是源码根/其子目录或显式传 `--source-root` 时才走本地；否则静默回退联网下载。

结论与全部输出片段已写入 answer.md:1。要不要我顺手跑几条实际查询（比如 `arch trace` / `arch provides`）验证数据面？
```

### Agent 写入的 answer.md

```markdown
# OSKM 托管运行时安装结论（本地源码根优先，零下载）

## 直接回答

- 当前目录就是完整 OpenHarmony 源码根（`.gn` 为文件、`interface/sdk-js` 与 `interface/sdk_c` 非空、`out/` 存在），
  并且 `out/sample-product/oskm/knowledge.db` 与 `cli/dist/oskm-cli.pyz` 都在。
- 因此**正确做法是用源码树本地构建装运行时，不联网**：在源码根执行 `bootstrap.py install`
  （或显式 `--source-root <源码根>`）。`install` 内部的 `find_local_runtime()` 会命中
  DB + 两套 SDK + 自带 `oskm_cli.database` 的 pyz，走 `_stage_local_runtime()` 复制安装，
  完全跳过 `download_runtime_bundle()`，所以配置的 `OSKM_DOWNLOAD_ENDPOINT` 一次都没被请求。
- 运行时已装到 `OSKM_RUNTIME_ROOT`：`../runtime/`，含 `knowledge.db`、`oskm-cli.pyz`、
  `interface/sdk-js`、`interface/sdk_c`、`.oskm-runtime.json`（`"source": "local"`）。
- `doctor` 全绿（exit 0），`refresh` 判定"已是最新"（`source=local` 时不按日期强刷），
  `validate-db` 返回 `{"ok": true}`，`arch overview` / `ask --list` 正常出结果。
- 坑点：`/usr/bin/python3` 是 **3.9.6**，低于 skill 要求的 3.10+，且 pyz 的 shebang 是
  `#!/usr/bin/env python3`。必须用 `/opt/homebrew/opt/python@3.12/bin/python3.12` 显式调用
  （`python3.12` 也在 PATH 上），别直接 `./oskm-cli.pyz`。
- 未访问、未修改 `~/.oskm`；源码树文件 sha256 与 mtime 保持不变。

## 关键命令

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred
cd "$WS/source"                      # cwd 必须是源码根或其子目录，否则探测不到本地构建

# 1) 安装前体检：已经提示检测到源码根本地构建、install 不联网
$PY ../tool/bootstrap.py doctor

# 2) 安装（本地源码根优先；OSKM_RUNTIME_ROOT 已在环境里，这里再显式写一次）
$PY ../tool/bootstrap.py --runtime-root "$WS/runtime" install --source-root "$WS/source"

# 3) 安装后校验
$PY ../tool/bootstrap.py doctor
$PY ../tool/bootstrap.py cli-path
$PY ../tool/bootstrap.py refresh
$PY ../tool/bootstrap.py validate-db "$WS/runtime/knowledge.db"

# 4) 用装好的 CLI 查询（固定文件名，不带版本号）
$PY "$WS/runtime/oskm-cli.pyz" --version
$PY "$WS/runtime/oskm-cli.pyz" --db "$WS/runtime/knowledge.db" arch overview
$PY "$WS/runtime/oskm-cli.pyz" --db "$WS/runtime/knowledge.db" ask --list

# 5) 离线证明：把端点换成不可达地址再装一次，仍然成功 => 全程没有 HTTP 请求
OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOW
… [输出截断，完整内容见工作区] …
b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  out/sample-product/oskm/knowledge.db
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  .../runtime/knowledge.db
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  cli/dist/oskm-cli.pyz
ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e  .../runtime/oskm-cli.pyz
```

离线证明（端点换成 127.0.0.1:9 仍成功）：

```
==> 使用源码本地运行时: .../source/out/sample-product/oskm/knowledge.db
==> 运行时安装完成: .../runtime
exit=0
```

## 复现要点 / 常见错误

- 不在源码根（或其子目录）执行且不给 `--source-root`：`_candidate_source_roots()` 只从 cwd 向上探测，
  探测不到就回退 `_download_bundle()`，那时才会真的打 `OSKM_DOWNLOAD_ENDPOINT`。
- `--source-root` 是权威参数：路径不是合法源码根会直接 `ValueError: 不是有效的 OpenHarmony 源码根`，
  不会静默退回 cwd 或联网。
- 本地构建缺任一条件都会静默回退下载：两套 SDK 目录必须非空、必须找到结构合格的
  `oskm-cli.pyz`（shebang + zip + `__main__.py` + `oskm_cli/cli.py` + CRC）、且该 pyz 必须能给出
  `oskm_cli.database.validate_db`，DB 还要通过 schema 校验。本夹具四项全满足。
- 回退发生时的信号是 stderr 上多出一行 `==> 下载 INTERNAL_CI 运行时: <date>`；本次没有这一行。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**装好了**
- 用本地源码根安装，全程零下载：`install` 命中 `out/sample-product/oskm/knowledge.db` + `cli/dist/oskm-cli.pyz`，走 `_stage_local_runtime()` 复制安装，跳过 `download_runtime_bundle()`。
- 运行时落在 `$OSKM_RUNTIME_ROOT`（`../runtime/`）：`knowledge.db`、`oskm-cli.pyz`、`interface/sdk-js`、`interface/sdk_c`、`.oskm-runtime.json`（`"source": "local"`）。
- `doctor` exit 0（`db=✓ sdk=✓ cli=✓`，oskm-cli 1.0.0）；`refresh` 报"已是最新"；`validate-db` 返回 `{"ok": true}`；`arch overview` / `ask --list` 正常出结果。

**关键命令**
- `/opt/homebrew/opt/python@3.12/bin/python3.12 ../tool/bootstrap.py doctor`
- `... bootstrap.py --runtime-root "$WS/runtime" install --source-root "$WS/source"`
- `... bootstrap.py validate-db "$WS/runtime/knowledge.db"`
- `python3.12 "$WS/runtime/oskm-cli.pyz" --db "$WS/runtime/knowledge.db" arch overview`

**零联网的证据**
- 安装日志只有 `==> 使用源码本地运行时` 与 `==> 运行时安装完成`，没有 `==> 下载 INTERNAL_CI 运行时` 那一行。
- 把 `OSKM_DOWNLOAD_ENDPOINT` 换成不可达的 `http://127.0.0.1:9/internal` 再装一次，仍然 exit 0 → 说明安装路径不依赖端点，夹具服务不会收到请求。
- 运行时 DB/CLI 与源码树 sha256 完全一致，源码树 mtime 未变；未触碰 `~/.oskm`。

**两个坑**
- `/usr/bin/python3` 是 3.9.6，低于 skill 的 3.10+ 要求，且 pyz shebang 是 `#!/usr/bin/env python3`；必须用 `python3.12` 显式调用，不要 `./oskm-cli.pyz`。
- `install` 只在 cwd 是源码根/其子目录或显式传 `--source-root` 时才走本地；否则静默回退联网下载。

结论与全部输出片段已写入 answer.md:1。要不要我顺手跑几条实际查询（比如 `arch trace` / `arch provides`）验证数据面？
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source` · exit=0 · 320.2s

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
| 3 | 状态文件记录源码根路径 | auto | Pass | source_root=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source |
| 4 | 装进来的 DB 就是源码树那一份（sha256 相同） | auto | Pass | installed=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 source=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 |
| 5 | 装进来的 CLI 就是源码树 cli/dist 那一份 | auto | Pass | installed=ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e source=ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e |
| 6 | 两套 SDK 都从源码树复制过来且非空 | auto | Pass | sdk-js=1 sdk_c=1 |
| 7 | 源码树本身没有被改动（DB 仍在原位） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source/out/sample-product/oskm/knowledge.db / /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e05-local-source-runtime-preferred/source/cli/dist/oskm-cli.pyz |
| 8 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
