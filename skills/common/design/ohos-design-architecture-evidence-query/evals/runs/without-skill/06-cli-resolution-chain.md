# E6 cli-resolution-chain（without-skill 臂）

- 开始时间：2026-11-17T15:41:25+08:00
- 结束时间：2026-11-17T15:48:12+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain`
- 夹具服务端：http://127.0.0.1:61447
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

运行时目录中存在已安装的 oskm-cli.pyz，同时设置了 OSKM_CLI，源码树也可用。请说明 bootstrap.py cli-path 应选择哪个候选；随后假设三个候选都不存在，再说明错误应如何提示。

## 期望结果（来自 evals.json）

解析顺序为 $OSKM_CLI → 源码树 CLI → <runtime-root>/oskm-cli.pyz。全部候选不存在时退出失败并提示运行 bootstrap.py install；CLI 不从网络自动下载。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| $OSKM_CLI | `contains` |
| <runtime-root>/oskm-cli.pyz | `contains` |
| bootstrap.py install | `contains` |
| 源码树 CLI 优先于已安装产物，失败提示可操作，且不会联网下载 CLI | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain/agent-start --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：407.3 s
- 事件计数：`{"thread.started": 1, "item.completed": 55, "item:error": 1, "turn.started": 1, "item:reasoning": 19, "item:agent_message": 8, "item.started": 27, "item:command_execution": 54, "turn.completed": 1}`
- 读到 skill 文档：是（6 处）
- 执行的命令数：27
- token 用量：`{"input_tokens": 603351, "cached_input_tokens": 557568, "output_tokens": 14287, "reasoning_output_tokens": 5670}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && ls -la && echo "---- tool ----" && find tool -type f | head -50'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && echo "== agent-start ==" && ls -la agent-start && echo "== installed-runtime ==" && ls -la installed-runtime && echo "== empty-runtime ==" && ls -la empty-runtime && echo "== source-tree ==" && ls -la source-tree && echo "== plain-tool ==" && ls -la plain-tool'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && cat agent-start/PROMPT.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && echo "=== plain-tool/bootstrap.py ===" && cat plain-tool/bootstrap.py && echo "=== tool/bootstrap.py ===" && cat tool/bootstrap.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && wc -l tool/oskm_runtime/*.py && echo "=== __main__.py ===" && cat tool/oskm_runtime/__main__.py && echo "=== __init__.py ===" && cat tool/oskm_runtime/__init__.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && cat tool/oskm_runtime/environment.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && cat tool/oskm_runtime/cli_install.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && cat tool/oskm_runtime/bootstrap.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && sed -n '100,240p' tool/oskm_runtime/cli_install.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && sed -n '1,60p' tool/oskm_runtime/install.py && echo \"=== grep source tree detection ===\" && grep -n \"SOURCE_LAYOUT\\|source_root\\|find_source\\|def \" tool/oskm_runtime/install.py | head -60"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p && ls -la && echo "== fixtures ==" && ls -la fixtures | head -20 && echo "== source-tree layout ==" && find without-skill/e06-cli-resolution-chain/source-tree -maxdepth 4 | head -30'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && diff -r plain-tool tool && echo \"plain-tool == tool (identical)\"; echo \"== env/doctor hints ==\"; ls -la plain-tool/oskm_runtime; sed -n '1,80p' tool/oskm_runtime/doctor.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p && PY=/opt/homebrew/opt/python@3.12/bin/python3.12; $PY -V; echo "== sha256 of the two pyz =="; shasum -a 256 fixtures/oskm-cli.pyz without-skill/e06-cli-resolution-chain/installed-runtime/oskm-cli.pyz; echo "== fixtures/cli-tree =="; find fixtures/cli-tree -maxdepth 4; echo "== fixtures/source =="; find fixtures/source -maxdepth 3 | head -20; echo "== source-tree version =="; cat without-skill/e06-cli-resolution-chain/source-tree/cli/oskm_cli/__init__.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && grep -n \"cli-path\\|resolve_cli\\|allow_download\" tool/oskm_runtime/*.py | grep -v \""'^tool/oskm_runtime/cli_install.py" ; echo "== rest of resolve_cli (download branch?) =="; sed -n '"'205,260p' tool/oskm_runtime/cli_install.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12; BASE=$PWD; FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz; PT=$BASE/plain-tool/bootstrap.py
echo "### E1: OSKM_CLI=fixtures, runtime-root=installed-runtime"
OSKM_CLI="$FIX" OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$PT" --runtime-root "$BASE/installed-runtime" cli-path; echo "exit=$?"
echo "### E2: OSKM_CLI unset, runtime-root=installed-runtime"
env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$PT" --runtime-root "$BASE/installed-runtime" cli-path; echo "exit=$?"
echo "### E4: OSKM_CLI=fixtures, runtime-root=empty-runtime"
OSKM_CLI="$FIX" OSKM_RUNTIME_ROOT="$BASE/empty-runtime" $PY "$PT" --runtime-root "$BASE/empty-runtime" cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12; BASE=$PWD; PT=$BASE/plain-tool/bootstrap.py
echo "### E3: all three candidates absent (plain-tool + empty-runtime + OSKM_CLI unset)"; env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/empty-runtime" $PY "$PT" --runtime-root "$BASE/empty-runtime" cli-path; echo "exit=$?"
echo "### E3b: same, stderr only"; env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/empty-runtime" $PY "$PT" --runtime-root "$BASE/empty-runtime" cli-path 2>/dev/null; echo "exit=$? (stdout empty => message is on stderr)"
echo "### E6: OSKM_CLI bogus -> falls through to installed"; OSKM_CLI="$BASE/empty-runtime/nope.pyz" OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$PT" --runtime-root "$BASE/installed-runtime" cli-path; echo "exit=$?"
echo "### E6b: OSKM_CLI bogus + empty runtime -> error lists bogus attempt"; OSKM_CLI="$BASE/empty-runtime/nope.pyz" OSKM_RUNTIME_ROOT="$BASE/empty-runtime" $PY "$PT" --runtime-root "$BASE/empty-runtime" cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12; BASE=$PWD; FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz; ST=$BASE/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py
echo "### E7: source-tree entry + OSKM_CLI=fixtures (runtime=installed)"; OSKM_CLI="$FIX" OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$ST" --runtime-root "$BASE/installed-runtime" cli-path; echo "exit=$?"
echo "### E8: source-tree entry + OSKM_CLI unset (runtime=installed)"; env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$ST" --runtime-root "$BASE/installed-runtime" cli-path; echo "exit=$?"
echo "### E9: source-tree entry + OSKM_CLI unset (runtime=empty)"; env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/empty-runtime" $PY "$ST" --runtime-root "$BASE/empty-runtime" cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12; BASE=$PWD; FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz; PT=$BASE/plain-tool/bootstrap.py
echo "### doctor with OSKM_CLI=fixtures (installed runtime)"; OSKM_CLI="$FIX" OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$PT" --runtime-root "$BASE/installed-runtime" doctor 2>&1 | sed -n '"'1,12p'; echo \"exit="'${PIPESTATUS[0]}"
echo "### doctor with OSKM_CLI unset (empty runtime) -> FAIL line"; env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/empty-runtime" $PY "$PT" --runtime-root "$BASE/empty-runtime" doctor 2>&1 | sed -n '"'1,14p'"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12; BASE=$PWD; PT=$BASE/plain-tool/bootstrap.py
echo "### E10: cwd = source-tree, but entry is plain-tool, OSKM_CLI unset"; cd "$BASE/source-tree" && env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$PT" --runtime-root "$BASE/installed-runtime" cli-path; echo "exit=$?"
echo "### E11: OSKM_CLI -> fixtures/cli-tree (a source tree dir)"; cd "$BASE" && OSKM_CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/cli-tree OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$PT" --runtime-root "$BASE/installed-runtime" cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain/agent-start && PY=/opt/homebrew/opt/python@3.12/bin/python3.12; BASE=$(dirname $PWD); PT=$BASE/plain-tool/bootstrap.py; mkdir -p .scratch/broken-runtime && printf '"'not a zipapp at all\\n' > .scratch/bad.pyz && cp .scratch/bad.pyz .scratch/broken-runtime/oskm-cli.pyz
echo \"### E12: OSKM_CLI -> existing file that is not a usable pyz (falls through, attempt 1 keeps the verify error)\"; OSKM_CLI=\""'$PWD/.scratch/bad.pyz" OSKM_RUNTIME_ROOT="$BASE/empty-runtime" $PY "$PT" --runtime-root "$BASE/empty-runtime" cli-path; echo "exit=$?"
echo "### E13: installed candidate exists but is broken (attempt 3 reports it verbatim)"; env -u OSKM_CLI OSKM_RUNTIME_ROOT="$PWD/.scratch/broken-runtime" $PY "$PT" --runtime-root "$PWD/.scratch/broken-runtime" cli-path 2>&1 | sed -n '"'1,8p'"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12; BASE=$PWD; PT=$BASE/plain-tool/bootstrap.py; ST=$BASE/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py
echo "### kind label: installed"; env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$PT" --runtime-root "$BASE/installed-runtime" doctor 2>&1 | grep '"'"'^CLI:'"'
echo \"### kind label: source (source-tree entry, OSKM_CLI unset)\"; env -u OSKM_CLI OSKM_RUNTIME_ROOT=\""'$BASE/installed-runtime" $PY "$ST" --runtime-root "$BASE/installed-runtime" doctor 2>&1 | grep '"'"'^CLI:'"'
echo \"### chain summary line from doctor\"; env -u OSKM_CLI OSKM_RUNTIME_ROOT=\""'$BASE/installed-runtime" $PY "$PT" --runtime-root "$BASE/installed-runtime" doctor 2>&1 | grep '"'三级候选'"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain/agent-start && find .scratch -type f -print && rm .scratch/bad.pyz .scratch/broken-runtime/oskm-cli.pyz && rmdir .scratch/broken-runtime .scratch && ls -la'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p && ls -la fixtures && shasum -a 256 fixtures/oskm-cli.pyz && ls -la without-skill/e06-cli-resolution-chain/installed-runtime without-skill/e06-cli-resolution-chain/empty-runtime && ls -la ~/.oskm 2>&1 | head -3'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain/agent-start && cat > answer.md <<'ANSWER'
# bootstrap.py cli-path 的 CLI 候选解析

## 直接回答

**1) 本夹具下 "'`cli-path` 应选哪一个候选？→ 选 `$OSKM_CLI`。**

解析结果就是 `$OSKM_CLI` 指向的那一份：

```
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz
```

`doctor` 里它的 kind 标为 `env`（`CLI: …/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)`）。
`installed-runtime/oskm-cli.pyz` 与源码树**都不会**被选中：三级候选是**短路**的，第一个命中的就返回。

固定顺序（`tool/oskm_runtime/cli_install.py:190` 的 `resolve_cli`，`doctor` 的提示行原样写着这条链）：

```
$OSKM_CLI  →  源码树（cli/oskm_cli/__init__.py）  →  <runtime-root>/oskm-cli.pyz
```

两条容易踩的细节：

- **源码树候选锚定在 skill 自己的文件位置，不是 cwd。** `find_source_tree(Path(__file__))` 从 `oskm_runtime/cli_install.py` 向上找 `cli/oskm_cli/__init__.py`（`tool/oskm_runtime/cli_install.py:148`）。所以 `plain-tool/bootstrap.py`（不在源码树内）永远不会命中候选 2 —— 即使把 cwd 切到 `source-tree` 也一样（见 E10）；而 `source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py` 会命中，返回的是**源码树根目录**（不是 pyz 文件）。
- **只有 `$OSKM_CLI` 未设置时，源码树才压过已安装产物**；两者都在时仍是 env 赢（见 E7）。`$OSKM_CLI` 也可以指向一个源码树目录（见 E11）。

**2) 三个候选都不存在时，错误应如何提示？→ 退出码 1，stderr 打印一条“已尝试 + 可行做法”的清单。**

`cli-path` 成功时只往 stdout 打印一个路径（可直接进 shell 变量）；失败时 stdout 为空，全部信息在 stderr，前缀 `错误: `，退出码 `1`（`EXIT_ERROR`；`2` 只留给用法错误）。文案必须逐条说明每个候选**为什么**没命中，并给出可执行的下一步 —— 实测输出：

```
错误: 找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布，所以正常情况下 `bootstrap.py install` 会把它装到 <runtime-root>/oskm-cli.pyz。已尝试：
  1. $OSKM_CLI 未设置
  2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py
  3. <runtime-root>/oskm-cli.pyz —— 不存在
可行做法：
  · 跑 `bootstrap.py install` 从运行时归档里装（含 CLI）
  · 或在源码仓构建后手动复制：python3 cli/scripts/build_cli.py，再把 cli/dist/oskm-cli.pyz 放到 <runtime-root>/oskm-cli.pyz
  · 或用 OSKM_CLI 直接指向一个 .pyz / 源码树
```

（上面把长绝对路径缩写成 `<runtime-root>`；真实输出里三处都是完整解析后的绝对路径。）

提示质量的三个要点：

- **“文件在但坏了”要原样报出，不能只说“不存在”。** 候选 1/3 命中一个存在但通不过 `verify_pyz` 的文件时，对应那行换成校验原话（见 E12/E13）：`CLI 产物不是可执行 zipapp（缺少 shebang）`／`不是有效 zip`／`CRC 校验失败`／`缺少必需条目 [...]`，然后**继续**尝试下一级候选。
- **`$OSKM_CLI` 指错不致命。** 指向一个既不是 `.pyz` 也不是源码树的路径时，第 1 行写 `不是 .pyz 文件，也不是含 cli/oskm_cli/__init__.py 的源码树`，随后正常回退到候选 2/3（见 E6，仍然成功返回已安装产物）。
- **同一段文字在 `doctor` 里以 `CLI: FAIL: …` 出现**，且检查顺序是 Python → 配置 → CLI → 运行时状态；CLI 解析不出来时 `Modules` 行会连带报 `oskm_cli (FAIL: No module named '"'oskm_cli')"'`。第一个 FAIL 就是根因。

## 关键命令

`--runtime-root` 显式指向夹具目录，并同时 `export OSKM_RUNTIME_ROOT` 为同一目录 —— 后者是为了让 `main()` 里的 `.env` 查找（`env_file_candidates`）也落在夹具里，全程不碰 `~/.oskm`（已确认 `~/.oskm` 不存在）。

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
BASE=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain
FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz
PT=$BASE/plain-tool/bootstrap.py
ST=$BASE/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py

# E1 env 赢过 installed
OSKM_CLI="$FIX" OSKM_RUNTIME_ROOT="$BASE/installed-runtime" '"\\
  "'$PY "$PT" --runtime-root "$BASE/installed-runtime" cli-path
# E2 env 未设置 -> installed
env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/installed-runtime" '"\\
  "'$PY "$PT" --runtime-root "$BASE/installed-runtime" cli-path
# E3 三候选全缺 -> 错误清单 + exit 1
env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/empty-runtime" '"\\
  "'$PY "$PT" --runtime-root "$BASE/empty-runtime" cli-path
# E7/E8 源码树内的入口：env 仍然赢；env 未设置时源码树赢过 installed
OSKM_CLI="$FIX" OSKM_RUNTIME_ROOT="$BASE/installed-runtime" '"\\
  "'$PY "$ST" --runtime-root "$BASE/installed-runtime" cli-path
env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/installed-runtime" '"\\
  "'$PY "$ST" --runtime-root "$BASE/installed-runtime" cli-path
# kind / version 标签
$PY "$PT" --runtime-root "$BASE/installed-runtime" doctor | grep '"'"'^CLI:'"'
"'```

## 关键输出

| # | 条件 | `cli-path` 输出（尾部） | exit |
|---|---|---|---|
| E1 | plain-tool + `OSKM_CLI=fixtures/oskm-cli.pyz` + installed-runtime | `…/fixtures/oskm-cli.pyz` | 0 |
| E2 | plain-tool + env 未设置 + installed-runtime | `…/installed-runtime/oskm-cli.pyz` | 0 |
| E3 | plain-tool + env 未设置 + empty-runtime | `错误: 找不到可用的 oskm-cli 产物…`（3 条已尝试 + 3 条可行做法，stderr） | 1 |
| E4 | plain-tool + `OSKM_CLI=fixtures` + empty-runtime | `…/fixtures/oskm-cli.pyz`（env 与 runtime-root 无关） | 0 |
| E6 | `OSKM_CLI` 指向不存在的 `nope.pyz` + installed-runtime | `…/installed-runtime/oskm-cli.pyz`（回退成功） | 0 |
| E6b | `OSKM_CLI` 指向不存在的 `nope.pyz` + empty-runtime | 错误清单，第 1 行 `不是 .pyz 文件，也不是含 cli/oskm_cli/__init__.py 的源码树` | 1 |
| E7 | source-tree 入口 + `OSKM_CLI=fixtures` | `…/fixtures/oskm-cli.pyz`（env 压过源码树） | 0 |
| E8 | source-tree 入口 + env 未设置 | `…/source-tree`（源码树根目录，非 pyz） | 0 |
| E9 | source-tree 入口 + env 未设置 + empty-runtime | `…/source-tree`（候选 2 命中，故不会报“全缺”） | 0 |
| E10 | plain-tool，cwd 切到 `source-tree`，env 未设置 | `…/installed-runtime/oskm-cli.pyz`（源码树探测与 cwd 无关） | 0 |
| E11 | `OSKM_CLI=fixtures/cli-tree`（源码树目录） | `…/fixtures/cli-tree` | 0 |
| E12 | `OSKM_CLI` 指向内容为纯文本的 `bad.pyz` + empty-runtime | 错误清单，第 1 行 `CLI 产物不是可执行 zipapp（缺少 shebang）: …/bad.pyz` | 1 |
| E13 | env 未设置，`<runtime-root>/oskm-cli.pyz` 存在但是坏文件 | 错误清单，第 3 行同样是 `缺少 shebang` 原话 | 1 |

kind / version 标签（`doctor`）：

```
CLI: …/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
CLI: …/installed-runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
CLI: …/source-tree (source, oskm-cli 9.9.9)
提示: … CLI 按三级候选解析（$OSKM_CLI → 源码树 → <runtime-root>/oskm-cli.pyz），全程不单独下载 CLI。
```

## 环境说明

- `fixtures/oskm-cli.pyz` 与 `installed-runtime/oskm-cli.pyz` 内容完全相同（sha256 `ad760c16…5eb49e`），所以**只有路径能区分候选**；版本也同为 `1.0.0`，源码树用 `9.9.9` 作标记。
- CLI 不单独下载：三级候选全部本地判定，`resolve_cli` 全程不联网（本次也未配置 `OSKM_DOWNLOAD_ENDPOINT`，与结论无关）。
- 未修改 `fixtures/`、`installed-runtime/`、`empty-runtime/`、`source-tree/`、`tool/`；构造坏产物用的临时目录建在 `agent-start/.scratch`，跑完已删除。未访问 `~/.oskm`。
ANSWER
wc -l answer.md && head -20 answer.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && grep -n \"def resolve_cli\\|def find_source_tree\\|def verify_pyz\\|def _location_from_env\" tool/oskm_runtime/cli_install.py && grep -n \"def cmd_cli_path\" tool/oskm_runtime/bootstrap.py"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain/agent-start && sed -i '' 's|"'`tool/oskm_runtime/cli_install.py:190` 的 `resolve_cli`|`tool/oskm_runtime/cli_install.py:195` 的 `resolve_cli`，命令实现在 `tool/oskm_runtime/bootstrap.py:251`|'"' answer.md && grep -n \"cli_install.py:195\" answer.md"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12; BASE=$PWD; FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz; echo "-- headline: env wins --"; OSKM_CLI="$FIX" OSKM_RUNTIME_ROOT="$BASE/installed-runtime" $PY "$BASE/plain-tool/bootstrap.py" --runtime-root "$BASE/installed-runtime" cli-path; echo "exit=$?"; echo "-- headline: all three missing --"; env -u OSKM_CLI OSKM_RUNTIME_ROOT="$BASE/empty-runtime" $PY "$BASE/plain-tool/bootstrap.py" --runtime-root "$BASE/empty-runtime" cli-path 2>&1 | head -6; echo "-- workspace clean --"; ls -la agent-start'
```

### Agent 最终回答

```markdown
**结论**
- `cli-path` 应选候选 1：`$OSKM_CLI` → `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz`（`doctor` 标为 `(env, oskm-cli 1.0.0)`）。三级候选短路：`$OSKM_CLI` → 源码树 → `<runtime-root>/oskm-cli.pyz`，见 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain/tool/oskm_runtime/cli_install.py:195`。
- 源码树探测锚定 `cli_install.py` 自身位置向上找 `cli/oskm_cli/__init__.py`（`tool/oskm_runtime/cli_install.py:148`），与 cwd 无关：`plain-tool/bootstrap.py` 永远命中不了候选 2（cd 到 `source-tree` 也一样），只有源码树内那个入口会，且仍输给 `$OSKM_CLI`；它未设置时源码树压过已安装产物，返回的是目录 `…/source-tree`。
- 三候选全缺时：退出码 `1`，stdout 空、信息全在 stderr，前缀 `错误: 找不到可用的 oskm-cli 产物…`，逐条列出 `1. $OSKM_CLI 未设置`／`2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py`／`3. <root>/oskm-cli.pyz —— 不存在`，再给三条可行做法（`install`、源码构建后复制到 `<root>/oskm-cli.pyz`、用 `OSKM_CLI` 指过去），见 `tool/oskm_runtime/bootstrap.py:251`。
- “文件在但坏了”不降级成“不存在”：`verify_pyz` 的原话（缺 shebang／不是有效 zip／CRC 失败／缺条目）直接进对应候选行，然后继续尝试下一级；`$OSKM_CLI` 指错也只是回退，不致命。`doctor` 把同一段文字作为 `CLI: FAIL: …` 输出。

**验证**
- 跑了 13 组组合（两个入口 × env/无 env × installed/empty runtime，外加坏产物、bogus `OSKM_CLI`、cwd 干扰、`OSKM_CLI` 指向源码树目录），全部命令与输出表格记在 `answer.md:1`。
- 两个 pyz 内容相同（sha256 `ad760c16…5eb49e`），所以靠路径区分候选；源码树版本 `9.9.9` 作标记。
- 全程用 `--runtime-root` + `OSKM_RUNTIME_ROOT` 指向夹具目录，未访问 `~/.oskm`；`fixtures/`、两个 runtime 目录、`tool/`、`source-tree/` 均未改动，构造坏产物用的 `agent-start/.scratch` 已删除。
```

### Agent 写入的 answer.md

```markdown
# bootstrap.py cli-path 的 CLI 候选解析

## 直接回答

**1) 本夹具下 `cli-path` 应选哪一个候选？→ 选 `$OSKM_CLI`。**

解析结果就是 `$OSKM_CLI` 指向的那一份：

```
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz
```

`doctor` 里它的 kind 标为 `env`（`CLI: …/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)`）。
`installed-runtime/oskm-cli.pyz` 与源码树**都不会**被选中：三级候选是**短路**的，第一个命中的就返回。

固定顺序（`tool/oskm_runtime/cli_install.py:195` 的 `resolve_cli`，命令实现在 `tool/oskm_runtime/bootstrap.py:251`，`doctor` 的提示行原样写着这条链）：

```
$OSKM_CLI  →  源码树（cli/oskm_cli/__init__.py）  →  <runtime-root>/oskm-cli.pyz
```

两条容易踩的细节：

- **源码树候选锚定在 skill 自己的文件位置，不是 cwd。** `find_source_tree(Path(__file__))` 从 `oskm_runtime/cli_install.py` 向上找 `cli/oskm_cli/__init__.py`（`tool/oskm_runtime/cli_install.py:148`）。所以 `plain-tool/bootstrap.py`（不在源码树内）永远不会命中候选 2 —— 即使把 cwd 切到 `source-tree` 也一样（见 E10）；而 `source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py` 会命中，返回的是**源码树根目录**（不是 pyz 文件）。
- **只有 `$OSKM_CLI` 未设置时，源码树才压过已安装产物**；两者都在时仍是 env 赢（见 E7）。`$OSKM_CLI` 也可以指向一个源码树目录（见 E11）。

**2) 三个候选都不存在时，错误应如何提示？→ 退出码 1，stderr 打印一条“已尝试 + 可行做法”的清单。**

`cli-path` 成功时只往 stdout 打印一个路径（可直接进 shell 变量）；失败时 stdout 为空，全部信息在 stderr，前缀 `错误: `，退出码 `1`（`EXIT_ERROR`；`2` 只留给用法错误）。文案必须逐条说明每个候选**为什么**没命中，并给出可执行的下一步 —— 实测输出：

```
错误: 找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布，所以正常情况下 `bootstrap.py install` 会把它装到 <runtime-root>/oskm-cli.pyz。已尝试：
  1. $OSKM_CLI 未设置
  2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py
  3. <runtime-root>/oskm-cli.pyz —— 不存在
可行做法：
  · 跑 `bootstrap.py install` 从运行时归档里装（含 CLI）
  · 或在源码仓构建后手动复制：python3 cli/scripts/build_cli.py，再把 cli/dist/oskm-cli.pyz 放到 <runtime-root>/oskm-cli.pyz
  · 或用 OSKM_CLI 直接指向一个 .pyz / 源码树
```

（上面把长绝对路径缩写成 `<runtime-root>`；真实输出里三处都是完整解析后的绝对路径。）

提示质量的三个要点：

- **“文件在但坏了”要原样报出，不能只说“不存在”。** 候选 1/3 命中一个存在但通不过 `verify_pyz` 的文件时，对应那行换成校验原话（见 E12/E13）：`CLI 产物不是可执行 zipapp（缺少 shebang）`／`不是有效 zip`／`CRC 校验失败`／`缺少必需条目 [...]`，然后**继续**尝试下一级候选。
- **`$OSKM_CLI` 指错不致命。** 指向一个既不是 `.
… [输出截断，完整内容见工作区] …
env 未设置 | `…/installed-runtime/oskm-cli.pyz`（源码树探测与 cwd 无关） | 0 |
| E11 | `OSKM_CLI=fixtures/cli-tree`（源码树目录） | `…/fixtures/cli-tree` | 0 |
| E12 | `OSKM_CLI` 指向内容为纯文本的 `bad.pyz` + empty-runtime | 错误清单，第 1 行 `CLI 产物不是可执行 zipapp（缺少 shebang）: …/bad.pyz` | 1 |
| E13 | env 未设置，`<runtime-root>/oskm-cli.pyz` 存在但是坏文件 | 错误清单，第 3 行同样是 `缺少 shebang` 原话 | 1 |

kind / version 标签（`doctor`）：

```
CLI: …/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
CLI: …/installed-runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
CLI: …/source-tree (source, oskm-cli 9.9.9)
提示: … CLI 按三级候选解析（$OSKM_CLI → 源码树 → <runtime-root>/oskm-cli.pyz），全程不单独下载 CLI。
```

## 环境说明

- `fixtures/oskm-cli.pyz` 与 `installed-runtime/oskm-cli.pyz` 内容完全相同（sha256 `ad760c16…5eb49e`），所以**只有路径能区分候选**；版本也同为 `1.0.0`，源码树用 `9.9.9` 作标记。
- CLI 不单独下载：三级候选全部本地判定，`resolve_cli` 全程不联网（本次也未配置 `OSKM_DOWNLOAD_ENDPOINT`，与结论无关）。
- 未修改 `fixtures/`、`installed-runtime/`、`empty-runtime/`、`source-tree/`、`tool/`；构造坏产物用的临时目录建在 `agent-start/.scratch`，跑完已删除。未访问 `~/.oskm`。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结论**
- `cli-path` 应选候选 1：`$OSKM_CLI` → `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz`（`doctor` 标为 `(env, oskm-cli 1.0.0)`）。三级候选短路：`$OSKM_CLI` → 源码树 → `<runtime-root>/oskm-cli.pyz`，见 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain/tool/oskm_runtime/cli_install.py:195`。
- 源码树探测锚定 `cli_install.py` 自身位置向上找 `cli/oskm_cli/__init__.py`（`tool/oskm_runtime/cli_install.py:148`），与 cwd 无关：`plain-tool/bootstrap.py` 永远命中不了候选 2（cd 到 `source-tree` 也一样），只有源码树内那个入口会，且仍输给 `$OSKM_CLI`；它未设置时源码树压过已安装产物，返回的是目录 `…/source-tree`。
- 三候选全缺时：退出码 `1`，stdout 空、信息全在 stderr，前缀 `错误: 找不到可用的 oskm-cli 产物…`，逐条列出 `1. $OSKM_CLI 未设置`／`2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py`／`3. <root>/oskm-cli.pyz —— 不存在`，再给三条可行做法（`install`、源码构建后复制到 `<root>/oskm-cli.pyz`、用 `OSKM_CLI` 指过去），见 `tool/oskm_runtime/bootstrap.py:251`。
- “文件在但坏了”不降级成“不存在”：`verify_pyz` 的原话（缺 shebang／不是有效 zip／CRC 失败／缺条目）直接进对应候选行，然后继续尝试下一级；`$OSKM_CLI` 指错也只是回退，不致命。`doctor` 把同一段文字作为 `CLI: FAIL: …` 输出。

**验证**
- 跑了 13 组组合（两个入口 × env/无 env × installed/empty runtime，外加坏产物、bogus `OSKM_CLI`、cwd 干扰、`OSKM_CLI` 指向源码树目录），全部命令与输出表格记在 `answer.md:1`。
- 两个 pyz 内容相同（sha256 `ad760c16…5eb49e`），所以靠路径区分候选；源码树版本 `9.9.9` 作标记。
- 全程用 `--runtime-root` + `OSKM_RUNTIME_ROOT` 指向夹具目录，未访问 `~/.oskm`；`fixtures/`、两个 runtime 目录、`tool/`、`source-tree/` 均未改动，构造坏产物用的 `agent-start/.scratch` 已删除。stderr:
2026-11-17T07:45:51.690080Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain && rm -rf agent-start/.scratch && ls -la agent-start && echo \\\"== confirm fixtures untouched ==\\\" && cd ../../ && ls -la fixtures && shasum -a 256 fixtures/oskm-cli.pyz'` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/without-skill/e06-cli-resolution-chain/agent-start` · exit=0 · 407.3s

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

自动断言 4/4 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 回答给出 $OSKM_CLI → 源码树 → <runtime-root>/oskm-cli.pyz 的顺序 | auto | Pass | answer/输出中同时出现 OSKM_CLI 与 oskm-cli.pyz |
| 2 | 回答提到失败时提示 bootstrap.py install | auto | Pass | answer/输出中出现 bootstrap.py install |
| 3 | 解析顺序与失败提示是否与实现一致（人工核对转录） | manual | 人工 | **结论** - `cli-path` 应选候选 1：`$OSKM_CLI` → `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-8p4lbp2p/fixtures/oskm-cli.pyz`（`doctor` 标为 `(env, oskm-cli 1.0.0)`）。三级候选短路：`
… [输出截断，完整内容见工作区] …
tall.py:148`），与 cwd 无关：`plain-tool/bootstrap.py` 永远命中不了候选 2（cd 到 `source-tree` 也一样），只有源码树内那个入口会，且仍输给 |
| 4 | 整个过程工具没有联网 | auto | Pass | [] |
| 5 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
