# E6 cli-resolution-chain（with-skill 臂）

- 开始时间：2026-11-17T16:24:26+08:00
- 结束时间：2026-11-17T16:29:33+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain`
- 夹具服务端：http://127.0.0.1:62052
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/agent-start --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：306.6 s
- 事件计数：`{"thread.started": 1, "item.completed": 55, "item:error": 1, "turn.started": 1, "item:reasoning": 16, "item:agent_message": 14, "item.started": 24, "item:command_execution": 48, "turn.completed": 1}`
- 读到 skill 文档：是（14 处）
- 执行的命令数：24
- token 用量：`{"input_tokens": 433533, "cached_input_tokens": 394496, "output_tokens": 11761, "reasoning_output_tokens": 3984}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc "ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/ && echo '---' && ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/installed-runtime /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/empty-runtime /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/plain-tool /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/source-tree"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && cat plain-tool/bootstrap.py && echo '=== oskm_runtime ===' && ls -la plain-tool/oskm_runtime && echo '=== source-tree ===' && find source-tree -maxdepth 4 | head -50"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && grep -rn \"OSKM_CLI\\|cli-path\\|cli_path\" --include=*.py -l . | head -20"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && grep -rn "OSKM_CLI" plain-tool/oskm_runtime/ | head -40'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && cat plain-tool/oskm_runtime/cli_install.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && sed -n '130,260p' plain-tool/oskm_runtime/cli_install.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && cat plain-tool/oskm_runtime/environment.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && grep -n \"cli-path\\|cli_path\\|CliInstallError\\|exit\\|SystemExit\\|return 2\\|return 5\" plain-tool/oskm_runtime/bootstrap.py | head -60"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && sed -n '120,175p' plain-tool/oskm_runtime/doctor.py && echo '=== diff plain vs source-tree runtime ===' && diff -rq plain-tool/oskm_runtime source-tree/skills/ohos-design-architecture-evidence-query/oskm_runtime"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && sed -n '236,303p' plain-tool/oskm_runtime/bootstrap.py"
$ /bin/zsh -lc 'ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/ && head -c 120 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz | cat -v | head -3'
$ /bin/zsh -lc 'env | grep -i oskm; echo "exit=$?"; echo '"'---'; sed -n '1,120p' /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/plain-tool/oskm_runtime/doctor.py | grep -n \"EXIT\\|_report_cli\" ; grep -n \"EXIT_OK\\|EXIT_USAGE\\|EXIT_ERROR\\|EXIT_DB\" /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/plain-tool/oskm_runtime/bootstrap.py | head -12"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && grep -n "_report_cli" -A 30 plain-tool/oskm_runtime/doctor.py | head -45'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz && echo "### A1: plain-tool + OSKM_CLI set (all 3 candidates available)" && OSKM_CLI="$FIX" $PY plain-tool/bootstrap.py cli-path --runtime-root "$PWD/installed-runtime"; echo "exit=$?"; echo "### A2: source-tree bootstrap + OSKM_CLI set" && OSKM_CLI="$FIX" $PY source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py cli-path --runtime-root "$PWD/installed-runtime"; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "### A3: plain-tool, OSKM_CLI unset -> installed pyz" && env -u OSKM_CLI $PY plain-tool/bootstrap.py cli-path --runtime-root "$PWD/installed-runtime"; echo "exit=$?"; echo "### A4: source-tree bootstrap, OSKM_CLI unset -> source tree" && env -u OSKM_CLI $PY source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py cli-path --runtime-root "$PWD/installed-runtime"; echo "exit=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && sed -n '40,70p' plain-tool/oskm_runtime/bootstrap.py && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz && echo \"### doctor: OSKM_CLI set\" && OSKM_CLI=\""'$FIX" $PY plain-tool/bootstrap.py doctor --runtime-root "$PWD/installed-runtime" | grep -i "''^CLI:"; echo "### doctor: no OSKM_CLI, plain-tool" && env -u OSKM_CLI $PY plain-tool/bootstrap.py doctor --runtime-root "$PWD/installed-runtime" | grep -i "''^CLI:"; echo "### doctor: no OSKM_CLI, source-tree bootstrap" && env -u OSKM_CLI $PY source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py doctor --runtime-root "$PWD/installed-runtime" | grep -i "''^CLI:"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "### B1: cli-path, all three candidates absent (empty-runtime, plain-tool, no OSKM_CLI)" && env -u OSKM_CLI -u OSKM_RUNTIME_ROOT $PY plain-tool/bootstrap.py cli-path --runtime-root "$PWD/empty-runtime"; echo "exit=$?"; echo; echo "### B2: same, stdout only" && env -u OSKM_CLI -u OSKM_RUNTIME_ROOT $PY plain-tool/bootstrap.py cli-path --runtime-root "$PWD/empty-runtime" 2>/dev/null; echo "stdout-exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "### B3: OSKM_CLI points at a missing path" && env -u OSKM_RUNTIME_ROOT OSKM_CLI="$PWD/empty-runtime/nope.pyz" $PY plain-tool/bootstrap.py cli-path --runtime-root "$PWD/empty-runtime" 2>&1 | head -5; echo "### B4: doctor with empty runtime" && env -u OSKM_CLI -u OSKM_RUNTIME_ROOT $PY plain-tool/bootstrap.py doctor --runtime-root "$PWD/empty-runtime" 2>&1 | sed -n '"'1,12p'; echo \"doctor-exit-check:\"; env -u OSKM_CLI -u OSKM_RUNTIME_ROOT "'$PY plain-tool/bootstrap.py doctor --runtime-root "$PWD/empty-runtime" >/dev/null 2>&1; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "### nuance: source-tree bootstrap + empty runtime still resolves via candidate 2" && env -u OSKM_CLI -u OSKM_RUNTIME_ROOT $PY source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py cli-path --runtime-root "$PWD/empty-runtime"; echo "exit=$?"; echo "### source layout in that tree:"; cat source-tree/cli/oskm_cli/__init__.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/agent-start && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && mkdir -p scratch-broken-runtime && printf 'this is not a zipapp\\n' > scratch-broken-runtime/oskm-cli.pyz && env -u OSKM_CLI -u OSKM_RUNTIME_ROOT "'$PY ../plain-tool/bootstrap.py cli-path --runtime-root "$PWD/scratch-broken-runtime" 2>&1 | sed -n '"'1,8p'; rm scratch-broken-runtime/oskm-cli.pyz; rmdir scratch-broken-runtime; ls -la"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && grep -n "''^def '"\\|"'^class '"\\|"'^ARTIFACT_NAME'"\\|"'^SOURCE_LAYOUT'"\\|"'^ENV = '"\\|"'^INSTALLED'"\\|"'^SOURCE'"\\|"'^CLI_PATH_ENV'"\\|"'^RUNTIME_ROOT_ENV'"\\|"'^DEFAULT_RUNTIME_ROOT" plain-tool/oskm_runtime/cli_install.py plain-tool/oskm_runtime/environment.py | head -40 && echo '"'---' && grep -n \"def cmd_cli_path\\|EXIT_OK = \\|EXIT_ERROR = \\|EXIT_USAGE = \" plain-tool/oskm_runtime/bootstrap.py && grep -n \"def _report_cli\" plain-tool/oskm_runtime/doctor.py"
$ /bin/zsh -lc "cat > /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/agent-start/answer.md <<'ANSWER_EOF'
# bootstrap.py cli-path 的 CLI 解析链（实测结论）

运行环境：解释器 "'`/opt/homebrew/opt/python@3.12/bin/python3.12`（3.12.16），
工作目录 `…/e06-cli-resolution-chain/agent-start`。环境中已预置
`OSKM_RUNTIME_ROOT=…/installed-runtime`，`OSKM_CLI` 未预置（按任务要求手工指向夹具）。
未访问、未修改 `~/.oskm`，未修改 `fixtures/`。

## 一、直接回答

### 1. 三个候选都在时，`cli-path` 选谁？

**选第 1 级：`$OSKM_CLI`**，即
`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz`。

解析顺序是**固定的三级、取第一个命中**（`plain-tool/oskm_runtime/cli_install.py:195` 的 `resolve_cli`）：

1. `$OSKM_CLI`（kind=`env`）——显式 `.pyz` 文件，或含 `cli/oskm_cli/__init__.py` 的源码树目录；优先级最高，给开发/CI 覆盖用（`plain-tool/oskm_runtime/environment.py:18`）。
2. **源码树**（kind=`source`）——从 `cli_install.py` **自身文件位置**向上找 `cli/oskm_cli/__init__.py`（`find_source_tree`，`plain-tool/oskm_runtime/cli_install.py:148`）。
3. `<runtime-root>/oskm-cli.pyz`（kind=`installed`）——`install` 从 `knowledge.tar.gz` 解出来的那一份；runtime root 取 `--runtime-root` > `$OSKM_RUNTIME_ROOT` > `~/.oskm`（`plain-tool/oskm_runtime/cli_install.py:189`）。

三步**全程不联网**，CLI 也不单独下载（旧的 `$OSKM_CLI_ENDPOINT` 通道已删）。

两个容易搞错的点，实测已确认：

- `$OSKM_CLI` **压过源码树**。即使用「在源码树内的那个 bootstrap」也一样：
  SKILL.md 里说的「源码树优先」是相对**下载**而言（能不下载就不下载），
  不是相对 `$OSKM_CLI`；在三级候选里 env 永远排第一。
- 第 2 级看的是 **bootstrap.py 自己所在的目录树**，不是 `cwd`。所以
  `plain-tool/bootstrap.py`（不在源码树内）永远命中不了第 2 级，会回退到第 3 级；
  `source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py` 才会命中源码树。

### 2. 三个候选都不存在时，错误应该怎么提示？

`resolve_cli` 抛 `CliInstallError`，`cmd_cli_path`（`plain-tool/oskm_runtime/bootstrap.py:251`）把它
按「`错误: <原因>` + **三级候选逐条尝试记录** + **三条可行做法**」打到 **stderr**，
退出码 **1**（bootstrap 的 `EXIT_ERROR`，见 `plain-tool/oskm_runtime/bootstrap.py:47`；
注意这不是查询 CLI 的 2/3/5 那套码），stdout 保持为空，便于管道使用。

提示必须包含：
- 一句总述「找不到可用的 oskm-cli 产物」，并说明它随 `knowledge.tar.gz` 一起发布、
  正常情况下 `install` 会装到哪个**具体绝对路径**；
- 逐条列出 1/2/3 各自**为什么没命中**（未设置 / 向上没找到 `cli/oskm_cli/__init__.py` / 文件不存在）；
- 三条可操作的出路：跑 `bootstrap.py install`；或源码仓构建后手工复制
  `cli/dist/oskm-cli.pyz` 到 `<runtime-root>/`；或用 `OSKM_CLI` 直接指过去。

两个补充分级（实测）：
- `$OSKM_CLI` 设了但指错：第 1 行写「不是 .pyz 文件，也不是含 `cli/oskm_cli/__init__.py` 的源码树」，不静默吞掉。
- 产物**存在但坏掉**（例如不是 zipapp）：第 3 行原样报出 `verify_pyz` 的结构性错误
  （`CLI 产物不是可执行 zipapp（缺少 shebang）: <路径>`），比笼统的「不存在」更有用。
- `doctor` 把同一条消息渲染成 `CLI: FAIL: …`，并连带 `Modules: oskm_cli (FAIL), oskm_schema (FAIL)`，整体退出码 1。

## 二、执行过的关键命令与输出

### A. 三级候选齐全：env 胜出（两个入口都一样）

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz
OSKM_CLI="$FIX" $PY plain-tool/bootstrap.py cli-path --runtime-root "$PWD/installed-runtime"
OSKM_CLI="$FIX" $PY source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py '"\\
    cli-path --runtime-root \""'$PWD/installed-runtime"
```

两条都输出（`exit=0`）：

```
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz
```

### B. 去掉 `$OSKM_CLI`：第 2 级 vs 第 3 级按入口分流

```bash
env -u OSKM_CLI $PY plain-tool/bootstrap.py cli-path --runtime-root "$PWD/installed-runtime"
env -u OSKM_CLI $PY source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py '"\\
    cli-path --runtime-root \""'$PWD/installed-runtime"
```

```
…/installed-runtime/oskm-cli.pyz      # 入口不在源码树内 -> 第 3 级 installed
…/source-tree                          # 入口在源码树内   -> 第 2 级 source
```

### C. `doctor` 打出候选类型（kind）与版本，佐证 A/B

```bash
OSKM_CLI="$FIX" $PY plain-tool/bootstrap.py doctor --runtime-root "$PWD/installed-runtime" | grep '"'"'^CLI:'"'
env -u OSKM_CLI  "'$PY plain-tool/bootstrap.py doctor --runtime-root "$PWD/installed-runtime" | grep '"'"'^CLI:'"'
env -u OSKM_CLI  "'$PY source-tree/skills/…/bootstrap.py doctor --runtime-root "$PWD/installed-runtime" | grep '"'"'^CLI:'"'
"'```

```
CLI: …/fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
CLI: …/installed-runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
CLI: …/source-tree (source, oskm-cli 9.9.9)
```

版本号差异（源码树 `cli/oskm_cli/__init__.py` 是 `__version__ = '"'9.9.9'"'`）证明第 2 级
确实解析到了源码树，而不是同名的已装产物。

### D. 三级全缺：错误提示与退出码

```bash
env -u OSKM_CLI -u OSKM_RUNTIME_ROOT $PY plain-tool/bootstrap.py cli-path '"\\
    --runtime-root \""'$PWD/empty-runtime"          # 2>/dev/null 时 stdout 全空
```

```
错误: 找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布，所以正常情况下
`bootstrap.py install` 会把它装到 …/empty-runtime/oskm-cli.pyz。已尝试：
  1. $OSKM_CLI 未设置
  2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py
  3. …/empty-runtime/oskm-cli.pyz —— 不存在
可行做法：
  · 跑 `bootstrap.py install` 从运行时归档里装（含 CLI）
  · 或在源码仓构建后手动复制：python3 cli/scripts/build_cli.py，再把 cli/dist/oskm-cli.pyz 放到 …/empty-runtime/oskm-cli.pyz
  · 或用 OSKM_CLI 直接指向一个 .pyz / 源码树
exit=1
```

### E. `$OSKM_CLI` 指错路径

```bash
OSKM_CLI="$PWD/empty-runtime/nope.pyz" $PY plain-tool/bootstrap.py cli-path '"\\
    --runtime-root \""'$PWD/empty-runtime"
```

```
  1. $OSKM_CLI=…/empty-runtime/nope.pyz —— 不是 .pyz 文件，也不是含 cli/oskm_cli/__init__.py 的源码树
```

### F. 产物存在但损坏（临时目录，跑完已删）

```bash
mkdir -p scratch-broken-runtime && printf '"'this is not a zipapp\\n' > scratch-broken-runtime/oskm-cli.pyz
env -u OSKM_CLI -u OSKM_RUNTIME_ROOT "'$PY ../plain-tool/bootstrap.py cli-path '"\\
    --runtime-root \""'$PWD/scratch-broken-runtime"
```

```
  3. …/scratch-broken-runtime/oskm-cli.pyz —— CLI 产物不是可执行 zipapp（缺少 shebang）: …/scratch-broken-runtime/oskm-cli.pyz
```

### G. `doctor` 的失败渲染

```bash
env -u OSKM_CLI -u OSKM_RUNTIME_ROOT $PY plain-tool/bootstrap.py doctor --runtime-root "$PWD/empty-runtime"
```

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
        FAIL: 下载配置无效。…
CLI: FAIL: 找不到可用的 oskm-cli 产物。…（三级尝试记录同上）
Modules: oskm_runtime (OK), oskm_cli (FAIL: No module named '"'oskm_cli'), oskm_schema (FAIL: No module named 'oskm_schema')
exit=1
"'```

## 三、一个必须注意的边界

「三个候选都不存在」这个前提，**要求入口 bootstrap 不在源码树内**。用源码树内那个
bootstrap 配空运行时根目录时，第 2 级仍然命中，命令 `exit=0` 并打印 `…/source-tree`：

```bash
env -u OSKM_CLI -u OSKM_RUNTIME_ROOT $PY source-tree/skills/…/bootstrap.py cli-path '"\\
    --runtime-root \""'$PWD/empty-runtime"
# -> …/source-tree   (exit=0)
```

所以要复现 D 的错误，只能用 `plain-tool/bootstrap.py`（或把源码树 `cli/oskm_cli/__init__.py` 移走）。
ANSWER_EOF
wc -l /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/agent-start/answer.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain && ls -la agent-start empty-runtime installed-runtime && ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/'
```

### Agent 最终回答

```markdown
**结论**
- `cli-path` 选 **第 1 级 `$OSKM_CLI`** → `/private/var/folders/.../fixtures/oskm-cli.pyz`；实测用 `plain-tool` 与 `source-tree` 两个入口结果一致，`exit=0`。
- 顺序固定为 `$OSKM_CLI`(env) → 源码树(source) → `<runtime-root>/oskm-cli.pyz`(installed)，取第一个命中，三步都不联网（`plain-tool/oskm_runtime/cli_install.py:195`）。
- SKILL.md 的「源码树优先」是相对**下载**说的，不压 `$OSKM_CLI`；且第 2 级看的是 **bootstrap.py 自身所在目录树**，不是 `cwd` —— `plain-tool` 入口命中不了源码树，会回退到 installed。
- 佐证：`doctor` 分别打出 `(env, oskm-cli 1.0.0)` / `(installed, 1.0.0)` / `(source, 9.9.9)`，源码树版本号 `9.9.9` 证明第 2 级确实解析到 `source-tree/cli/oskm_cli/__init__.py`。

**三候选全缺时的报错**
- `resolve_cli` 抛 `CliInstallError`，`cmd_cli_path` 打 `错误: <原因>` 到 **stderr**、退出码 **1**（`plain-tool/oskm_runtime/bootstrap.py:251`，非查询 CLI 的 2/3/5），stdout 为空。
- 消息含：总述 + `install` 会装到的**绝对路径**；1/2/3 逐条未命中原因；三条出路（`install` / 构建后手工复制 `cli/dist/oskm-cli.pyz` / 用 `OSKM_CLI` 指过去）。
- 分级更细：`$OSKM_CLI` 指错写「不是 .pyz 文件，也不是含 `cli/oskm_cli/__init__.py` 的源码树」；产物存在但损坏则原样报 `CLI 产物不是可执行 zipapp（缺少 shebang）: <路径>`；`doctor` 渲染成 `CLI: FAIL: …` 并连带 `oskm_cli`/`oskm_schema` FAIL。
- 边界：想复现全缺错误必须用**源码树外**的入口——`source-tree/.../bootstrap.py` 配 `empty-runtime` 仍命中第 2 级并 `exit=0`。

**产出**
- 结论、命令与输出片段写入 `answer.md:1`（含 A–G 七组实测）。夹具与运行时目录未改动，临时用的 `scratch-broken-runtime` 已删除，未触碰 `~/.oskm`。
```

### Agent 写入的 answer.md

```markdown
# bootstrap.py cli-path 的 CLI 解析链（实测结论）

运行环境：解释器 `/opt/homebrew/opt/python@3.12/bin/python3.12`（3.12.16），
工作目录 `…/e06-cli-resolution-chain/agent-start`。环境中已预置
`OSKM_RUNTIME_ROOT=…/installed-runtime`，`OSKM_CLI` 未预置（按任务要求手工指向夹具）。
未访问、未修改 `~/.oskm`，未修改 `fixtures/`。

## 一、直接回答

### 1. 三个候选都在时，`cli-path` 选谁？

**选第 1 级：`$OSKM_CLI`**，即
`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/fixtures/oskm-cli.pyz`。

解析顺序是**固定的三级、取第一个命中**（`plain-tool/oskm_runtime/cli_install.py:195` 的 `resolve_cli`）：

1. `$OSKM_CLI`（kind=`env`）——显式 `.pyz` 文件，或含 `cli/oskm_cli/__init__.py` 的源码树目录；优先级最高，给开发/CI 覆盖用（`plain-tool/oskm_runtime/environment.py:18`）。
2. **源码树**（kind=`source`）——从 `cli_install.py` **自身文件位置**向上找 `cli/oskm_cli/__init__.py`（`find_source_tree`，`plain-tool/oskm_runtime/cli_install.py:148`）。
3. `<runtime-root>/oskm-cli.pyz`（kind=`installed`）——`install` 从 `knowledge.tar.gz` 解出来的那一份；runtime root 取 `--runtime-root` > `$OSKM_RUNTIME_ROOT` > `~/.oskm`（`plain-tool/oskm_runtime/cli_install.py:189`）。

三步**全程不联网**，CLI 也不单独下载（旧的 `$OSKM_CLI_ENDPOINT` 通道已删）。

两个容易搞错的点，实测已确认：

- `$OSKM_CLI` **压过源码树**。即使用「在源码树内的那个 bootstrap」也一样：
  SKILL.md 里说的「源码树优先」是相对**下载**而言（能不下载就不下载），
  不是相对 `$OSKM_CLI`；在三级候选里 env 永远排第一。
- 第 2 级看的是 **bootstrap.py 自己所在的目录树**，不是 `cwd`。所以
  `plain-tool/bootstrap.py`（不在源码树内）永远命中不了第 2 级，会回退到第 3 级；
  `source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py` 才会命中源码树。

### 2. 三个候选都不存在时，错误应该怎么提示？

`resolve_cli` 抛 `CliInstallError`，`cmd_cli_path`（`plain-tool/oskm_runtime/bootstrap.py:251`）把它
按「`错误: <原因>` + **三级候选逐条尝试记录** + **三条可行做法**」打到 **stderr**，
退出码 **1**（bootstrap 的 `EXIT_ERROR`，见 `plain-tool/oskm_runtime/bootstrap.py:47`；
注意这不是查询 CLI 的 2/3/5 那套码），stdout 保持为空，便于管道使用。

提示必须包含：
- 一句总述「找不到可用的 oskm-cli 产物」，并说明它随 `knowledge.tar.gz` 一起发布、
  正常情况下 `install` 会装到哪个**具体绝对路径**；
- 逐条列出 1/2/3 各自**为什么没命中**（未设置 / 向上没找到 `cli/oskm_cli/__init__.py` / 文件不存在）；
- 三条可操作的出路：跑 `bootstrap.py install`；或源码仓构建后手工复制
  `cli/dist/oskm-cli.pyz` 到 `<runtime-ro
… [输出截断，完整内容见工作区] …
-broken-runtime"
```

```
  3. …/scratch-broken-runtime/oskm-cli.pyz —— CLI 产物不是可执行 zipapp（缺少 shebang）: …/scratch-broken-runtime/oskm-cli.pyz
```

### G. `doctor` 的失败渲染

```bash
env -u OSKM_CLI -u OSKM_RUNTIME_ROOT $PY plain-tool/bootstrap.py doctor --runtime-root "$PWD/empty-runtime"
```

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
        FAIL: 下载配置无效。…
CLI: FAIL: 找不到可用的 oskm-cli 产物。…（三级尝试记录同上）
Modules: oskm_runtime (OK), oskm_cli (FAIL: No module named 'oskm_cli'), oskm_schema (FAIL: No module named 'oskm_schema')
exit=1
```

## 三、一个必须注意的边界

「三个候选都不存在」这个前提，**要求入口 bootstrap 不在源码树内**。用源码树内那个
bootstrap 配空运行时根目录时，第 2 级仍然命中，命令 `exit=0` 并打印 `…/source-tree`：

```bash
env -u OSKM_CLI -u OSKM_RUNTIME_ROOT $PY source-tree/skills/…/bootstrap.py cli-path \
    --runtime-root "$PWD/empty-runtime"
# -> …/source-tree   (exit=0)
```

所以要复现 D 的错误，只能用 `plain-tool/bootstrap.py`（或把源码树 `cli/oskm_cli/__init__.py` 移走）。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结论**
- `cli-path` 选 **第 1 级 `$OSKM_CLI`** → `/private/var/folders/.../fixtures/oskm-cli.pyz`；实测用 `plain-tool` 与 `source-tree` 两个入口结果一致，`exit=0`。
- 顺序固定为 `$OSKM_CLI`(env) → 源码树(source) → `<runtime-root>/oskm-cli.pyz`(installed)，取第一个命中，三步都不联网（`plain-tool/oskm_runtime/cli_install.py:195`）。
- SKILL.md 的「源码树优先」是相对**下载**说的，不压 `$OSKM_CLI`；且第 2 级看的是 **bootstrap.py 自身所在目录树**，不是 `cwd` —— `plain-tool` 入口命中不了源码树，会回退到 installed。
- 佐证：`doctor` 分别打出 `(env, oskm-cli 1.0.0)` / `(installed, 1.0.0)` / `(source, 9.9.9)`，源码树版本号 `9.9.9` 证明第 2 级确实解析到 `source-tree/cli/oskm_cli/__init__.py`。

**三候选全缺时的报错**
- `resolve_cli` 抛 `CliInstallError`，`cmd_cli_path` 打 `错误: <原因>` 到 **stderr**、退出码 **1**（`plain-tool/oskm_runtime/bootstrap.py:251`，非查询 CLI 的 2/3/5），stdout 为空。
- 消息含：总述 + `install` 会装到的**绝对路径**；1/2/3 逐条未命中原因；三条出路（`install` / 构建后手工复制 `cli/dist/oskm-cli.pyz` / 用 `OSKM_CLI` 指过去）。
- 分级更细：`$OSKM_CLI` 指错写「不是 .pyz 文件，也不是含 `cli/oskm_cli/__init__.py` 的源码树」；产物存在但损坏则原样报 `CLI 产物不是可执行 zipapp（缺少 shebang）: <路径>`；`doctor` 渲染成 `CLI: FAIL: …` 并连带 `oskm_cli`/`oskm_schema` FAIL。
- 边界：想复现全缺错误必须用**源码树外**的入口——`source-tree/.../bootstrap.py` 配 `empty-runtime` 仍命中第 2 级并 `exit=0`。

**产出**
- 结论、命令与输出片段写入 `answer.md:1`（含 A–G 七组实测）。夹具与运行时目录未改动，临时用的 `scratch-broken-runtime` 已删除，未触碰 `~/.oskm`。stderr:
2026-11-17T08:27:32.770124Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc \\\"cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/agent-start && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && mkdir -p scratch-broken-runtime && printf 'this is not a zipapp\\\\\\\\n' > scratch-broken-runtime/oskm-cli.pyz && env -u OSKM_CLI -u OSKM_RUNTIME_ROOT \\\"'$PY ../plain-tool/bootstrap.py cli-path --runtime-root \\\"$PWD/scratch-broken-runtime\\\" 2>&1 | sed -n '\\\"'1,8p'; echo \\\\\\\"exit=\\\"'${pipestatus[1]}\\\"; rm -rf scratch-broken-runtime; ls -la'` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e06-cli-resolution-chain/agent-start` · exit=0 · 306.6s

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
| 3 | 解析顺序与失败提示是否与实现一致（人工核对转录） | manual | 人工 | **结论** - `cli-path` 选 **第 1 级 `$OSKM_CLI`** → `/private/var/folders/.../fixtures/oskm-cli.pyz`；实测用 `plain-tool` 与 `source-tree` 两个入口结果一致，`exit=0`。 - 顺序固定为 `$OSKM_CLI`(env) → 源码树(source) → `<runtime-ro
… [输出截断，完整内容见工作区] …
9.9.9)`，源码树版本号 `9.9.9` 证明第 2 级确实解析到 `source-tree/cli/oskm_cli/__init__.py`。  **三候选全缺时的报错** - `resolv |
| 4 | 整个过程工具没有联网 | auto | Pass | [] |
| 5 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
