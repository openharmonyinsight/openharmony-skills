# E6 cli-resolution-chain（with-skill 臂）

- 开始时间：2026-11-17T15:41:25+08:00
- 结束时间：2026-11-17T15:48:25+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain`
- 夹具服务端：http://127.0.0.1:61444
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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/agent-start --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：419.9 s
- 事件计数：`{"thread.started": 1, "item.completed": 59, "item:error": 1, "turn.started": 1, "item:reasoning": 17, "item:agent_message": 16, "item.started": 25, "item:command_execution": 46, "item:file_change": 4, "turn.completed": 1}`
- 读到 skill 文档：是（12 处）
- 执行的命令数：23
- token 用量：`{"input_tokens": 505355, "cached_input_tokens": 463872, "output_tokens": 14602, "reasoning_output_tokens": 5651}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc 'ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/'
$ /bin/zsh -lc "sed -n '100,185p' /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain; find . -maxdepth 4 | head -100; echo ---; ls -la agent-start; echo ---; env | grep -i oskm'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/plain-tool; wc -l bootstrap.py oskm_runtime/*.py; echo ---; cat oskm_runtime/cli_install.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/plain-tool; cat oskm_runtime/environment.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/plain-tool; grep -n \"\" oskm_runtime/cli_install.py | sed -n '150,300p'"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/plain-tool; grep -n \"cli-path\\|cli_path\\|add_parser\\|def cmd_\\|def main\" oskm_runtime/bootstrap.py | head -60; echo === ; sed -n '1,29p' bootstrap.py"
$ /bin/zsh -lc 'ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/; echo ===; ls -laR /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/installed-runtime /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/empty-runtime /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/source-tree'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain; sed -n '245,275p' plain-tool/oskm_runtime/bootstrap.py; echo \"---- installed-runtime ----\"; ls -la installed-runtime; echo \"---- empty-runtime ----\"; ls -la empty-runtime; echo \"---- source-tree ----\"; find source-tree -maxdepth 6 -print"
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures; echo "---- cli-tree ----"; find cli-tree -maxdepth 4; echo "---- source ----"; find source -maxdepth 3 | head -30; echo "---- pyz sha ----"; shasum -a 256 oskm-cli.pyz'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg; shasum -a 256 fixtures/oskm-cli.pyz with-skill/e06-cli-resolution-chain/installed-runtime/oskm-cli.pyz; echo "---- source versions ----"; grep -n "__version__" with-skill/e06-cli-resolution-chain/source-tree/cli/oskm_cli/__init__.py fixtures/cli-tree/cli/oskm_cli/__init__.py; echo "---- pyz version ----"; /opt/homebrew/opt/python@3.12/bin/python3.12 fixtures/oskm-cli.pyz --version; /opt/homebrew/opt/python@3.12/bin/python3.12 with-skill/e06-cli-resolution-chain/installed-runtime/oskm-cli.pyz --version'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/plain-tool; sed -n '274,303p' oskm_runtime/bootstrap.py; echo \"---- head of bootstrap.py ----\"; sed -n '1,60p' oskm_runtime/bootstrap.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain
FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
echo "== A1: OSKM_CLI set + installed-runtime, plain-tool/bootstrap.py =="
env OSKM_CLI="$FIX" OSKM_RUNTIME_ROOT="$PWD/installed-runtime" $PY plain-tool/bootstrap.py cli-path; echo "exit=$?"
echo "== A2: same env, source-tree bootstrap.py =="
env OSKM_CLI="$FIX" OSKM_RUNTIME_ROOT="$PWD/installed-runtime" $PY source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
echo "== B1: no OSKM_CLI, plain-tool (outside source tree) =="
env -u OSKM_CLI OSKM_RUNTIME_ROOT="$PWD/installed-runtime" $PY plain-tool/bootstrap.py cli-path; echo "exit=$?"
echo "== B2: no OSKM_CLI, source-tree bootstrap =="
env -u OSKM_CLI OSKM_RUNTIME_ROOT="$PWD/installed-runtime" $PY source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py cli-path; echo "exit=$?"
echo "== B3: no OSKM_CLI, plain-tool, --runtime-root empty-runtime =="
env -u OSKM_CLI $PY plain-tool/bootstrap.py --runtime-root "$PWD/empty-runtime" cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain
FIX=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
describe() { # $1 = oskm_runtime parent dir, $2 = runtime root
  env -u OSKM_CLI ${OSKM_CLI_OVERRIDE:+OSKM_CLI="$OSKM_CLI_OVERRIDE"} PYTHONPATH="$1" $PY - "$2" <<'"'EOF'
import sys
from oskm_runtime import cli_install
print(cli_install.resolve_cli(sys.argv[1]).describe())
EOF
}
echo \"-- kind for env override (plain-tool) --\"; OSKM_CLI_OVERRIDE=\""'$FIX" describe "$PWD/plain-tool" "$PWD/installed-runtime"
echo "-- kind for source tree --"; describe "$PWD/source-tree/skills/ohos-design-architecture-evidence-query" "$PWD/installed-runtime"
echo "-- kind for installed --"; describe "$PWD/plain-tool" "$PWD/installed-runtime"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
echo "== C1: run plain-tool/bootstrap.py FROM INSIDE source-tree (cwd should not matter) =="
cd source-tree && env -u OSKM_CLI OSKM_RUNTIME_ROOT="/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/installed-runtime" $PY ../plain-tool/bootstrap.py cli-path; echo "exit=$?"
echo "== C2: OSKM_CLI set to a nonexistent path =="
cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain
env OSKM_CLI="$PWD/empty-runtime/nope.pyz" OSKM_RUNTIME_ROOT="$PWD/installed-runtime" $PY plain-tool/bootstrap.py cli-path; echo "exit=$?"
echo "== C3: OSKM_CLI set to a dir that is not a source tree, empty runtime root =="
env OSKM_CLI="$PWD/empty-runtime" $PY plain-tool/bootstrap.py --runtime-root "$PWD/empty-runtime" cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
echo "== E: doctor with empty runtime root (no OSKM_CLI) =="
env -u OSKM_CLI $PY plain-tool/bootstrap.py --runtime-root "$PWD/empty-runtime" doctor; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
$PY - <<'"'EOF'
import os, pathlib, subprocess, sys, tempfile
root = pathlib.Path.cwd()
src = root / 'installed-runtime' / 'oskm-cli.pyz'
py = '/opt/homebrew/opt/python@3.12/bin/python3.12'
with tempfile.TemporaryDirectory(dir=str(root / 'agent-start')) as tmp:
    truncated = pathlib.Path(tmp) / 'oskm-cli.pyz'
    truncated.write_bytes(src.read_bytes()[:3000])
    env = {**os.environ, 'OSKM_RUNTIME_ROOT': tmp}
    env.pop('OSKM_CLI', None)
    proc = subprocess.run([py, str(root / 'plain-tool' / 'bootstrap.py'), 'cli-path'],
                          env=env, capture_output=True, text=True)
    print('== D1: installed candidate exists but truncated ==')
    print('exit=', proc.returncode)
    print(proc.stderr.strip() or proc.stdout.strip())
EOF
echo \"== D2: OSKM_CLI -> a source tree (fixtures/cli-tree) ==\"
env OSKM_CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/cli-tree OSKM_RUNTIME_ROOT=\""'$PWD/installed-runtime" PYTHONPATH="$PWD/plain-tool" $PY -c "from oskm_runtime import cli_install; print(cli_install.resolve_cli(None).describe())"'
$ /bin/zsh -lc 'ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/agent-start; ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/empty-runtime /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/installed-runtime'
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; grep -n \"OSKM_CLI\\|cli-path\\|三级\\|源码树\" references/usage.md | head -40"
$ /bin/zsh -lc "sed -n '78,112p' /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/references/usage.md"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
FIXPYZ=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz
$PY - "$FIXPYZ" <<'"'EOF'
import os, pathlib, shutil, subprocess, sys, tempfile
ws = pathlib.Path.cwd(); pyz = sys.argv[1]
py = '/opt/homebrew/opt/python@3.12/bin/python3.12'
boot = str(ws / 'plain-tool' / 'bootstrap.py')
with tempfile.TemporaryDirectory(dir=str(ws / 'agent-start')) as tmp:
    shutil.copy(pyz, pathlib.Path(tmp) / 'oskm-cli.pyz')
    env = {**os.environ, 'OSKM_RUNTIME_ROOT': tmp}; env.pop('OSKM_CLI', None)
    p = subprocess.run([py, boot, 'cli-path'], env=env, capture_output=True, text=True)
    print('== 修复法1: 复制 pyz 进运行时根目录 ==', 'exit=', p.returncode)
    print(p.stdout.strip() or p.stderr.strip())
    env2 = {**os.environ, 'OSKM_CLI': pyz}
    p2 = subprocess.run([py, boot, '--runtime-root', tmp.replace(tmp, tmp), 'cli-path'],
                        env=env2, capture_output=True, text=True)
    print('== 修复法2: OSKM_CLI 显式指过去 ==', 'exit=', p2.returncode)
    print(p2.stdout.strip() or p2.stderr.strip())
EOF
echo \"== 确认 empty-runtime 仍为空 ==\"; ls -A empty-runtime | wc -l"
```

### Agent 最终回答

```markdown
**答案：选第 1 级候选 `$OSKM_CLI`**
三级顺序是 `$OSKM_CLI` → 源码树 → `<runtime-root>/oskm-cli.pyz`（`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/plain-tool/oskm_runtime/cli_install.py:195`）。三者同时可用时 `cli-path` 输出 `fixtures/oskm-cli.pyz`（kind=`env`，exit=0）——两份 bootstrap 入口实测一致，"源码树优先"只在第 2 级 vs 第 3 级之间成立，压不过 `$OSKM_CLI`。

**实测到的两个坑**
- 第 2 级锚点是**工具文件自身位置**，不是 cwd：在 `source-tree/` 里跑 `../plain-tool/bootstrap.py cli-path` 仍返回 `installed-runtime/oskm-cli.pyz`；跑源码树内那份才返回 `source-tree`（version 9.9.9，可与 pyz 的 1.0.0 区分）。
- `$OSKM_CLI` 不可用时不硬失败，记一条 attempt 后继续降级（指不存在的路径时照常 exit=0）。

**三级全缺的报错**
- `CliInstallError` 被 `cmd_cli_path` 捕获（`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/plain-tool/oskm_runtime/bootstrap.py:251`），打 `错误: …` 到 **stderr**，**exit=1**。
- 报文三段式：结论 + **逐候选编号明细**（`$OSKM_CLI 未设置` / `源码树 —— 向上没找到 cli/oskm_cli/__init__.py` / `<绝对路径> —— 不存在`）+ 三条可行做法；路径随 `--runtime-root` 变，且不暗示 CLI 能单独下载。
- 候选"在但不可用"时第 3 行改为带校验原因（`CLI 产物不是有效 zip: …`），`doctor` 复用同一报文并附三级顺序提示。
- 本环境 `OSKM_DOWNLOAD_ENDPOINT=未配置`，故 `install` 这条离线不可行；实测有效的是复制 pyz 进运行时根目录或用 `OSKM_CLI` 指过去。

结论、关键命令与输出片段已写入 `answer.md`（`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/agent-start/answer.md:1`）。`~/.oskm` 未触碰，夹具只读，`empty-runtime` 保持为空（修复验证用一次性临时根目录并已清理）。
```

### Agent 写入的 answer.md

```markdown
# `bootstrap.py cli-path`：候选选择与三级全缺时的报错

缩写（下文命令里的变量）：

- `WS` = `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain`
- `FIX` = `/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures`
- `PY` = `/opt/homebrew/opt/python@3.12/bin/python3.12`

运行时根目录全程显式指定（`--runtime-root` 或 `OSKM_RUNTIME_ROOT`），未读写 `~/.oskm`；夹具目录只读。

---

## 结论一：本夹具下 `cli-path` 应选 **第 1 级候选 `$OSKM_CLI`**

三级候选按序尝试，第一个**可用**的就用，三步都不联网：

| # | 候选 | 校验 |
|---|---|---|
| 1 | `$OSKM_CLI`（`.pyz` 文件，或含 `cli/oskm_cli/__init__.py` 的源码目录） | `verify_pyz` 结构校验 |
| 2 | 源码树：从 **bootstrap 自身文件**向上探测 `cli/oskm_cli/__init__.py` | 无（开发路径） |
| 3 | `<runtime-root>/oskm-cli.pyz`（`install` 从 `knowledge.tar.gz` 解出来的那份） | `verify_pyz` 结构校验 |

所以「已安装 pyz + `OSKM_CLI` + 源码树」三者同时可用时，答案是 **`$OSKM_CLI` 指向的 `FIX/oskm-cli.pyz`**（kind=`env`）。

- 「源码树优先」只发生在**第 2 级 vs 第 3 级**之间，**不能**压过第 1 级；`$OSKM_CLI` 就是给开发/CI 钉住某个特定构建用的显式开关。
- 三个候选都不做版本/摘要锁定，`cli-path` 只报「最终用了哪一个」，版本另问 `--version`。

### 实测命令与输出

```bash
cd "$WS"
FIXPYZ="$FIX/oskm-cli.pyz"

# A1：OSKM_CLI + installed-runtime，plain-tool/bootstrap.py（不在源码树内）
env OSKM_CLI="$FIXPYZ" OSKM_RUNTIME_ROOT="$WS/installed-runtime" \
  $PY plain-tool/bootstrap.py cli-path
# A2：同样环境，换成源码树内的 bootstrap.py
env OSKM_CLI="$FIXPYZ" OSKM_RUNTIME_ROOT="$WS/installed-runtime" \
  $PY source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py cli-path
```

两者都输出（exit=0）：

```
/private/var/folders/.../oskm-eval-with-skill-0cuwbrkg/fixtures/oskm-cli.pyz
```

即 **A2 里源码树也在场，仍然被 `$OSKM_CLI` 压掉**。用 `describe()` 看 kind/version 更直白：

```
$FIX/cli-tree                                (env,       oskm-cli 9.9.9)   # OSKM_CLI 指源码目录也算第 1 级
$FIX/oskm-cli.pyz                            (env,       oskm-cli 1.0.0)   # ← 本任务的答案
$WS/source-tree                              (source,    oskm-cli 9.9.9)   # 第 2 级
$WS/installed-runtime/oskm-cli.pyz           (installed, oskm-cli 1.0.0)   # 第 3 级
```

### 降级顺序
… [输出截断，完整内容见工作区] …
pty-runtime" doctor   # exit=1
```

```
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
CLI: FAIL: 找不到可用的 oskm-cli 产物。…（同上三段式报文）
Modules: oskm_runtime (OK), oskm_cli (FAIL: No module named 'oskm_cli'), oskm_schema (FAIL: …)
提示: 运行时来自单个 knowledge.tar.gz … CLI 按三级候选解析（$OSKM_CLI → 源码树 →
      <runtime-root>/oskm-cli.pyz），全程不单独下载 CLI。
错误: 运行时依赖检查未通过。
```

## 本环境下的正确修复动作

`OSKM_DOWNLOAD_ENDPOINT=未配置`，所以报文里的第一条「跑 `bootstrap.py install`」在此**离线不可行**；应按后两条走：

```bash
# 最省事：把可用的 pyz 放进运行时根目录（补上第 3 级候选）
cp "$FIX/oskm-cli.pyz" "$RUNTIME_ROOT/oskm-cli.pyz"
# 或：显式指过去（第 1 级候选，不动运行时目录）
OSKM_CLI="$FIX/oskm-cli.pyz" $PY plain-tool/bootstrap.py --runtime-root "$RUNTIME_ROOT" cli-path
```

两条都已实测（exit=0）：复制后 `cli-path` 返回 `<runtime-root>/oskm-cli.pyz`；`OSKM_CLI` 指过去则返回 `$FIX/oskm-cli.pyz`。
为了不污染本次评估的 `$WS/empty-runtime`（它要保持为空），验证时用的是 `$WS/agent-start` 下的一次性临时运行时根目录，用后自动清理。

无论哪条，修完都要再跑一次 `bootstrap.py cli-path` 确认实际选中的候选，别假定。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**答案：选第 1 级候选 `$OSKM_CLI`**
三级顺序是 `$OSKM_CLI` → 源码树 → `<runtime-root>/oskm-cli.pyz`（`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/plain-tool/oskm_runtime/cli_install.py:195`）。三者同时可用时 `cli-path` 输出 `fixtures/oskm-cli.pyz`（kind=`env`，exit=0）——两份 bootstrap 入口实测一致，"源码树优先"只在第 2 级 vs 第 3 级之间成立，压不过 `$OSKM_CLI`。

**实测到的两个坑**
- 第 2 级锚点是**工具文件自身位置**，不是 cwd：在 `source-tree/` 里跑 `../plain-tool/bootstrap.py cli-path` 仍返回 `installed-runtime/oskm-cli.pyz`；跑源码树内那份才返回 `source-tree`（version 9.9.9，可与 pyz 的 1.0.0 区分）。
- `$OSKM_CLI` 不可用时不硬失败，记一条 attempt 后继续降级（指不存在的路径时照常 exit=0）。

**三级全缺的报错**
- `CliInstallError` 被 `cmd_cli_path` 捕获（`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/plain-tool/oskm_runtime/bootstrap.py:251`），打 `错误: …` 到 **stderr**，**exit=1**。
- 报文三段式：结论 + **逐候选编号明细**（`$OSKM_CLI 未设置` / `源码树 —— 向上没找到 cli/oskm_cli/__init__.py` / `<绝对路径> —— 不存在`）+ 三条可行做法；路径随 `--runtime-root` 变，且不暗示 CLI 能单独下载。
- 候选"在但不可用"时第 3 行改为带校验原因（`CLI 产物不是有效 zip: …`），`doctor` 复用同一报文并附三级顺序提示。
- 本环境 `OSKM_DOWNLOAD_ENDPOINT=未配置`，故 `install` 这条离线不可行；实测有效的是复制 pyz 进运行时根目录或用 `OSKM_CLI` 指过去。

结论、关键命令与输出片段已写入 `answer.md`（`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/agent-start/answer.md:1`）。`~/.oskm` 未触碰，夹具只读，`empty-runtime` 保持为空（修复验证用一次性临时根目录并已清理）。stderr:
/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain\\nPY=/opt/homebrew/opt/python@3.12/bin/python3.12\\nSCRATCH=\\\"$PWD/agent-start/.scratch-cli-check\\\"; mkdir -p \\\"$SCRATCH\\\"\\nhead -c 3000 installed-runtime/oskm-cli.pyz > \\\"$SCRATCH/oskm-cli.pyz\\\"\\necho \\\"== D1: installed candidate exists but i…176 chars truncated…a source tree (fixtures/cli-tree) ==\\\"\\nenv OSKM_CLI=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/fixtures/cli-tree OSKM_RUNTIME_ROOT=\\\"$PWD/installed-runtime\\\" PYTHONPATH=\\\"$PWD/plain-tool\\\" $PY -c \\\"from oskm_runtime import cli_install; print(cli_install.resolve_cli(None).describe())\\\"\\nrm -rf \\\"$SCRATCH\\\"'` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolution-chain/agent-start` · exit=0 · 419.9s

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
| 3 | 解析顺序与失败提示是否与实现一致（人工核对转录） | manual | 人工 | **答案：选第 1 级候选 `$OSKM_CLI`** 三级顺序是 `$OSKM_CLI` → 源码树 → `<runtime-root>/oskm-cli.pyz`（`/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e06-cli-resolutio
… [输出截断，完整内容见工作区] …
runtime/oskm-cli.pyz`；跑源码树内那份才返回 `source-tree`（version 9.9.9，可与 pyz 的 1.0.0 区分）。 - `$OSKM_CLI` 不可用时不 |
| 4 | 整个过程工具没有联网 | auto | Pass | [] |
| 5 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
