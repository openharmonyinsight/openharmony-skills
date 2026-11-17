# E6 cli-resolution-chain（without-skill 臂）

- 开始时间：2026-11-17T16:26:11+08:00
- 结束时间：2026-11-17T16:33:41+08:00
- 执行臂：`without-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain`
- 夹具服务端：http://127.0.0.1:62107
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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/agent-start --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：420.9 s
- 事件计数：`{"thread.started": 1, "item.completed": 52, "item:error": 1, "turn.started": 1, "item:reasoning": 15, "item:agent_message": 14, "item.started": 22, "item:command_execution": 44, "turn.completed": 1}`
- 读到 skill 文档：是（7 处）
- 执行的命令数：22
- token 用量：`{"input_tokens": 439670, "cached_input_tokens": 396288, "output_tokens": 14549, "reasoning_output_tokens": 5117}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/ && echo "---TOOL---" && find /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/tool -type f | head -50'
$ /bin/zsh -lc 'echo "OSKM_CLI=$OSKM_CLI"; echo "CODEX_HOME=$CODEX_HOME"; pwd'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/tool && cat bootstrap.py && echo "===== oskm_runtime/bootstrap.py =====" && cat oskm_runtime/bootstrap.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/tool && wc -l oskm_runtime/*.py && echo "===== environment.py =====" && cat oskm_runtime/environment.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/tool && cat -n oskm_runtime/cli_install.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/tool && sed -n '100,245p' oskm_runtime/cli_install.py | cat -n | sed 's/"'^/ /'"' "
$ /bin/zsh -lc 'R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures; echo "== installed-runtime =="; ls -la $R/installed-runtime; echo "== empty-runtime =="; ls -la $R/empty-runtime; echo "== plain-tool =="; find $R/plain-tool -maxdepth 3; echo "== source-tree =="; find $R/source-tree -maxdepth 3 -not -path '"'*/.git/*' | head -40; echo \"== fixtures ==\"; ls -la "'$F'
$ /bin/zsh -lc 'R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; echo "== .env files anywhere in workspace =="; find $R -name '"'.env*' -maxdepth 4; echo \"== diff tool/bootstrap.py vs plain-tool/bootstrap.py ==\"; diff "'$R/tool/bootstrap.py $R/plain-tool/bootstrap.py && echo SAME; echo "== diff oskm_runtime dirs =="; diff -rq $R/tool/oskm_runtime $R/plain-tool/oskm_runtime && echo SAME'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures; $PY - <<EOF
import sys, hashlib, zipfile
sys.path.insert(0, "$R/tool")
from oskm_runtime import cli_install as ci
for label, p in [("fixtures", "$F/oskm-cli.pyz"), ("installed-runtime", "$R/installed-runtime/oskm-cli.pyz")]:
    ci.verify_pyz(p)
    print(f"{label}: verify_pyz OK, version={ci.pyz_version(p)}, sha256={hashlib.sha256(open(p,'"'rb').read()).hexdigest()[:16]}\")
print(\"source-tree version:\", ci._source_version(\""'$R/source-tree/cli/oskm_cli/__init__.py"))
print("find_source_tree(from plain-tool):", ci.find_source_tree("$R/tool/oskm_runtime/cli_install.py"))
print("find_source_tree(from source-tree skill):", ci.find_source_tree("$R/source-tree/skills/ohos-design-architecture-evidence-query/oskm_runtime/cli_install.py"))
EOF'
$ /bin/zsh -lc 'R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; ls -la $R/source-tree/skills/ohos-design-architecture-evidence-query/oskm_runtime/ | head; echo "== source-tree bootstrap.py identical? =="; diff $R/tool/bootstrap.py $R/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py && echo SAME; diff -rq $R/tool/oskm_runtime $R/source-tree/skills/ohos-design-architecture-evidence-query/oskm_runtime && echo RUNTIME_SAME'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/agent-start && cat > run_cases.sh <<'SH'
#"'!/bin/zsh
# 复现 bootstrap.py cli-path 的三级候选解析（只读运行，不改夹具）
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain
F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures
PLAIN=$R/plain-tool/bootstrap.py
INSRC=$R/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py
run() {  # run <label> <bootstrap> <runtime-root> [OSKM_CLI value or "-"]
  local label=$1 boot=$2 root=$3 cli=$4
  echo "------------------------------------------------------------"
  echo "### $label"
  echo "'"\\"'$ bootstrap=$boot"
  echo "'"\\"'$ --runtime-root=$root"
  if [[ $cli == "-" ]]; then echo '"'"'$ OSKM_CLI=(unset)'"'; env -u OSKM_CLI "'$PY $boot --runtime-root $root cli-path; else echo "'"\\"'$ OSKM_CLI=$cli"; OSKM_CLI=$cli $PY $boot --runtime-root $root cli-path; fi
  echo "exit=$?"
}
run "A 三候选齐备 + OSKM_CLI（plain-tool，不在源码树）" $PLAIN $R/installed-runtime $F/oskm-cli.pyz
run "B 三候选齐备 + OSKM_CLI（源码树内 bootstrap）" $INSRC $R/installed-runtime $F/oskm-cli.pyz
run "C 无 OSKM_CLI，plain-tool + 已装运行时" $PLAIN $R/installed-runtime -
run "D 无 OSKM_CLI，源码树内 bootstrap + 已装运行时" $INSRC $R/installed-runtime -
run "E 三候选全缺：无 OSKM_CLI + plain-tool + 空运行时" $PLAIN $R/empty-runtime -
run "F OSKM_CLI 指向不存在路径 + 空运行时" $PLAIN $R/empty-runtime $F/nope.pyz
run "G OSKM_CLI 指向源码树 + 空运行时" $PLAIN $R/empty-runtime $R/source-tree
SH
chmod +x run_cases.sh && ./run_cases.sh 2>&1 | tee cases.log'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures; cd $R/tool && $PY - <<EOF
import sys, os
sys.path.insert(0, "$R/tool")
from oskm_runtime import cli_install as ci
def show(label, env, root, anchor):
    os.environ.pop('"'OSKM_CLI', None)
    if env: os.environ['OSKM_CLI'] = env
    ci.__file__ = anchor  # 只影响 find_source_tree 的起点，模拟两个 bootstrap 位置
    import importlib; importlib.reload(ci)
    print(f\"{label}: {ci.resolve_cli(root).describe()}\")
show(\"A env+installed, plain-tool\", \""'$F/oskm-cli.pyz", "$R/installed-runtime", "$R/plain-tool/oskm_runtime/cli_install.py")
show("B env+installed, 源码树内", "$F/oskm-cli.pyz", "$R/installed-runtime", "$R/source-tree/skills/ohos-design-architecture-evidence-query/oskm_runtime/cli_install.py")
show("C 无 env, plain-tool", "", "$R/installed-runtime", "$R/plain-tool/oskm_runtime/cli_install.py")
show("D 无 env, 源码树内", "", "$R/installed-runtime", "$R/source-tree/skills/ohos-design-architecture-evidence-query/oskm_runtime/cli_install.py")
EOF'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; cd $R/agent-start && mkdir -p scratch-runtime && printf '"'not a zipapp at all\\n' > scratch-runtime/oskm-cli.pyz && echo \"=== doctor on empty-runtime (三候选全缺) ===\" && env -u OSKM_CLI "'$PY $R/plain-tool/bootstrap.py --runtime-root $R/empty-runtime doctor; echo "exit=$?"; echo "=== cli-path，已装产物不可用（缺 shebang）===" ; env -u OSKM_CLI $PY $R/plain-tool/bootstrap.py --runtime-root $R/scratch-runtime cli-path; echo "exit=$?"'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures; SK=$R/source-tree/skills/ohos-design-architecture-evidence-query; echo "--- A: OSKM_CLI 指向夹具 pyz（plain-tool，三候选齐备）---"; OSKM_CLI=$F/oskm-cli.pyz $PY -c "import sys;sys.path.insert(0,'"'"'$R/plain-tool'"');from oskm_runtime import cli_install as ci;print(ci.resolve_cli('"'$R/installed-runtime'"').describe())\"; echo \"--- B: 同上，但 bootstrap 在源码树内 ---\"; OSKM_CLI="'$F/oskm-cli.pyz $PY -c "import sys;sys.path.insert(0,'"'"'$SK'"');from oskm_runtime import cli_install as ci;print(ci.resolve_cli('"'$R/installed-runtime'"').describe())\"; echo \"--- C: 无 OSKM_CLI，plain-tool ---\"; env -u OSKM_CLI "'$PY -c "import sys;sys.path.insert(0,'"'"'$R/plain-tool'"');from oskm_runtime import cli_install as ci;print(ci.resolve_cli('"'$R/installed-runtime'"').describe())\"; echo \"--- D: 无 OSKM_CLI，源码树内 ---\"; env -u OSKM_CLI "'$PY -c "import sys;sys.path.insert(0,'"'"'$SK'"');from oskm_runtime import cli_install as ci;print(ci.resolve_cli('"'$R/installed-runtime'"').describe())\""
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; S=$R/agent-start/scratch-runtime; mkdir -p $S; printf '"'not a zipapp at all\\n' > "'$S/oskm-cli.pyz; echo "=== 已装产物存在但缺 shebang ==="; env -u OSKM_CLI $PY $R/plain-tool/bootstrap.py --runtime-root $S cli-path; echo "exit=$?"; F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures; head -c 20000 $F/oskm-cli.pyz > $S/oskm-cli.pyz; echo; echo "=== 已装产物被截断（zip 中央目录丢失）==="; env -u OSKM_CLI $PY $R/plain-tool/bootstrap.py --runtime-root $S cli-path 2>&1 | sed -n '"'1,12p'; echo \"exit="'${PIPESTATUS[0]}"'
$ /bin/zsh -lc "R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; sed -n '1,80p' "'$R/tool/oskm_runtime/doctor.py | grep -n -A6 -B2 '"'CLI'"
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; S=$R/agent-start/scratch-runtime; echo "=== OSKM_CLI 指向坏 pyz，但 installed-runtime 里有好产物 ==="; OSKM_CLI=$S/oskm-cli.pyz $PY $R/plain-tool/bootstrap.py --runtime-root $R/installed-runtime cli-path; echo "exit=$?"; echo "=== 同场景下 update-cli（会打印 kind + version）==="; OSKM_CLI=$S/oskm-cli.pyz $PY $R/plain-tool/bootstrap.py --runtime-root $R/installed-runtime update-cli; echo "exit=$?"'
$ /bin/zsh -lc 'PY=/opt/homebrew/opt/python@3.12/bin/python3.12; R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures; S=$R/agent-start/scratch-runtime; cp $F/oskm-cli.pyz $S/oskm-cli-noext; echo "=== OSKM_CLI 指向有效 zipapp 但文件名不带 .pyz ==="; OSKM_CLI=$S/oskm-cli-noext $PY $R/plain-tool/bootstrap.py --runtime-root $R/empty-runtime cli-path 2>&1 | sed -n '"'2,4p'; echo \"=== OSKM_CLI 设为空串 ===\"; OSKM_CLI=\"\" "'$PY $R/plain-tool/bootstrap.py --runtime-root $R/empty-runtime cli-path 2>&1 | sed -n '"'2,4p'"
$ /bin/zsh -lc "R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; grep -n \"EXIT_ERROR\\|EXIT_USAGE\\|EXIT_OK\" "'$R/tool/oskm_runtime/bootstrap.py | head -8; echo "--- cmd_cli_path ---"; sed -n '"'/"'^def cmd_cli_path/,/''^MANAGED_COMMANDS/p'"' "'$R/tool/oskm_runtime/bootstrap.py'
$ /bin/zsh -lc 'R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/tool; grep -n "''^ARTIFACT_NAME'"\\|"'^SOURCE_LAYOUT'"\\|"'^REQUIRED_MEMBERS'"\\|"'^ENV = '"\\|"'^INSTALLED = '"\\|"'^SOURCE = '"\\|"'^def verify_pyz'"\\|"'^def find_source_tree'"\\|"'^def _location_from_env'"\\|"'^def _location_from_installed'"\\|"'^def _location_from_source'"\\|"'^def default_runtime_root'"\\|"'^def resolve_cli'"\\|"'^def installed_path'"\\|raise CliInstallError(\" "'$R/oskm_runtime/cli_install.py; echo "--- environment.py ---"; grep -n "CLI_PATH_ENV'"\\|RUNTIME_ROOT_ENV\" "'$R/oskm_runtime/environment.py | head -5; echo "--- bootstrap.py ---"; grep -n "def cmd_cli_path'"\\|def cmd_update_cli\\|def resolve_root\\|"'^MANAGED = " $R/oskm_runtime/bootstrap.py; echo "--- doctor.py ---"; grep -n "def _report_cli'"\\|resolve_cli(root\" "'$R/oskm_runtime/doctor.py'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/agent-start && cat > answer.md <<'MD'
# "'`bootstrap.py cli-path` 的 CLI 候选解析：实测结论

## 0. 路径缩写（下文沿用）

```
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain
F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures
PLAIN=$R/plain-tool/bootstrap.py                                    # 不在源码树内
INSRC=$R/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py   # 在源码树内
```

工具代码：`$R/tool/bootstrap.py` + `$R/tool/oskm_runtime/`（与 `$R/plain-tool/`、源码树内那份逐字节相同，已用 `diff -rq` 验证）。

## 1. 直接回答（一）：三个候选都在时，`cli-path` 应该选哪个

**选候选 1 —— `$OSKM_CLI` 指向的那一份，即 `$F/oskm-cli.pyz`。**

优先级是硬编码的固定顺序，见 `$R/tool/oskm_runtime/cli_install.py:195`（`resolve_cli`）：

1. `$OSKM_CLI`（`environment.py:18` 定义 `CLI_PATH_ENV = '"'OSKM_CLI'"'`）——显式覆盖，最高优先级
2. 源码树——从 **`cli_install.py` 自身位置**向上找 `cli/oskm_cli/__init__.py`（`cli_install.py:148`）
3. `<runtime-root>/oskm-cli.pyz`——`install` 落盘的固定名产物（`cli_install.py:171`）

三条要点，都由实跑证实：

- **`$OSKM_CLI` 赢过源码树，也赢过已安装产物。** 即使 bootstrap 本身在源码树内（候选 2 明明可用），只要 `OSKM_CLI` 指向一个可用产物，就用它。
- **候选 2 的锚点是 bootstrap 脚本自己的位置，不是 cwd，也不是 `--runtime-root`。** 同一条命令、同一个 cwd，`$PLAIN` 落到候选 3，`$INSRC` 落到候选 2。
- **`--runtime-root` 只影响候选 3。** 候选 1、2 与运行时根目录无关。

`$OSKM_CLI` 的合法取值有两种（`cli_install.py:157`）：后缀为 `.pyz` 且通过 `verify_pyz()` 的文件，或含 `cli/oskm_cli/__init__.py` 的源码树目录。

## 2. 实测命令与输出

复现脚本：`$R/agent-start/run_cases.sh`，完整输出留在 `$R/agent-start/cases.log`。

```
$ OSKM_CLI=$F/oskm-cli.pyz $PY $PLAIN --runtime-root $R/installed-runtime cli-path
/private/var/.../oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz        # ← 候选 1 命中
exit=0

$ OSKM_CLI=$F/oskm-cli.pyz $PY $INSRC --runtime-root $R/installed-runtime cli-path
/private/var/.../oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz        # ← 源码树内也是候选 1
exit=0

$ env -u OSKM_CLI $PY $PLAIN --runtime-root $R/installed-runtime cli-path
/private/var/.../e06-cli-resolution-chain/installed-runtime/oskm-cli.pyz       # ← 候选 3
exit=0

$ env -u OSKM_CLI $PY $INSRC --runtime-root $R/installed-runtime cli-path
/private/var/.../e06-cli-resolution-chain/source-tree                          # ← 候选 2
exit=0
```

`cli-path` 只打印路径，看不出命中的是哪一级；用 `resolve_cli(...).describe()`（等价于 `update-cli` 的输出）拿到 kind 与版本：

```
A: /private/var/.../fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
B: /private/var/.../fixtures/oskm-cli.pyz (env, oskm-cli 1.0.0)
C: /private/var/.../installed-runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
D: /private/var/.../source-tree (source, oskm-cli 9.9.9)
```

夹具 pyz 与已安装 pyz 内容相同（`verify_pyz` 均通过，版本同为 1.0.0），源码树刻意标成 9.9.9，因此 kind/路径足以区分。

`$OSKM_CLI` 也可以指源码树目录（候选 1 的第二种形态）：

```
$ OSKM_CLI=$R/source-tree $PY $PLAIN --runtime-root $R/empty-runtime cli-path
/private/var/.../e06-cli-resolution-chain/source-tree
exit=0
```

## 3. 直接回答（二）：三个候选都不存在时，错误应该怎么提示

**实测输出（`$PLAIN --runtime-root $R/empty-runtime cli-path`，无 `OSKM_CLI`，`$PLAIN` 不在源码树内，`$R/empty-runtime` 为空）：**

```
错误: 找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布，所以正常情况下 `bootstrap.py install` 会把它装到 <empty-runtime>/oskm-cli.pyz。已尝试：
  1. $OSKM_CLI 未设置
  2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py
  3. <empty-runtime>/oskm-cli.pyz —— 不存在
可行做法：
  · 跑 `bootstrap.py install` 从运行时归档里装（含 CLI）
  · 或在源码仓构建后手动复制：python3 cli/scripts/build_cli.py，再把 cli/dist/oskm-cli.pyz 放到 <empty-runtime>/oskm-cli.pyz
  · 或用 OSKM_CLI 直接指向一个 .pyz / 源码树
exit=1
```

这段提示由 `cli_install.py:233` 抛出 `CliInstallError`，`cmd_cli_path`（`bootstrap.py:251`）捕获后打印。它满足的契约：

- **退出码 1（`EXIT_ERROR`），不是 0，也不是 2。** 2（`EXIT_USAGE`）只留给参数用法错误。
- **写到 stderr，stdout 保持干净。** `cli-path` 的 stdout 只在成功时输出那一行路径，便于 `$(...)` 直接取值；失败时 stdout 为空。
- **前缀 `错误: `**，与 bootstrap 其他命令一致。
- **三条候选逐条列出，一条不落**（`resolve_cli` 里的 `attempts` 列表），每条写明失败原因：未设置 / 向上没找到 `cli/oskm_cli/__init__.py` / 不存在。使用者不必回头读代码就知道检查哪三处。
- **给出可执行的下一步**，三条分别对应"装"、"自己构建后放到固定名"、"用环境变量指过去"。
- **路径全部展开成绝对路径**（`default_runtime_root` 会 `expanduser().resolve()`），不含 `~`，可直接复制粘贴。

### 3.1 两个值得注意的分支

**（a）"文件在但不是个能用的产物"——原样报出校验错误，而不是笼统的"不存在"**（`cli_install.py:220` 一带）：

```
$ printf '"'not a zipapp at all\\n' > scratch-runtime/oskm-cli.pyz
"'$ env -u OSKM_CLI $PY $PLAIN --runtime-root scratch-runtime cli-path
  3. <scratch>/oskm-cli.pyz —— CLI 产物不是可执行 zipapp（缺少 shebang）: <scratch>/oskm-cli.pyz

$ head -c 20000 $F/oskm-cli.pyz > scratch-runtime/oskm-cli.pyz   # 截断，中央目录丢失
  3. <scratch>/oskm-cli.pyz —— CLI 产物不是有效 zip: <scratch>/oskm-cli.pyz
```

`verify_pyz()`（`cli_install.py:100`）是结构性校验：shebang + 是 zip + CRC 完好 + 含 `__main__.py`、`oskm_cli/__init__.py`、`oskm_cli/cli.py`。它把"下载被截断/被 HTML 错误页替换"挡在 import 之前，避免炸出看不懂的 `ImportError`。

**（b）`$OSKM_CLI` 指向不可用产物时不硬失败，而是降级继续，但原因只在最终失败时才浮现：**

```
$ OSKM_CLI=<坏 pyz> $PY $PLAIN --runtime-root $R/installed-runtime cli-path
/private/var/.../installed-runtime/oskm-cli.pyz     # exit=0，静默用了候选 3
```

因此**排障时不要只看 `cli-path` 的路径输出**：它不告诉你"你设的 `OSKM_CLI` 被忽略了"。想确认实际生效的是哪一级，用 `update-cli`（打印 `describe()`，含 kind 与版本）或 `doctor`（`CLI: <path> (kind, oskm-cli x.y.z)`）。反过来，`OSKM_CLI` 写错又不存在其他候选时，第 1 条 attempt 会把原因写清楚：

```
  1. $OSKM_CLI=<...>/fixtures/nope.pyz —— 不是 .pyz 文件，也不是含 cli/oskm_cli/__init__.py 的源码树
```

同一句也用于"是有效 zipapp 但文件名不带 `.pyz` 后缀"的情况（实测 `oskm-cli-noext`）——后缀是候选 1 的硬条件。`OSKM_CLI` 设为空串等同未设置（`.strip()` 后判空），报 `1. $OSKM_CLI 未设置`。

### 3.2 `doctor` 里的同一份提示

`doctor`（`doctor.py:46`）复用同一个异常文本，前缀换成 `CLI: FAIL: `，并**继续**报完 Modules / Runtime root / Runtime state，最后以 `错误: 运行时依赖检查未通过。` 退出 1：

```
$ env -u OSKM_CLI $PY $PLAIN --runtime-root $R/empty-runtime doctor
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=未配置
        FAIL: 下载配置无效。...
CLI: FAIL: 找不到可用的 oskm-cli 产物。... 已尝试： 1./2./3. ... 可行做法： ...
Modules: oskm_runtime (OK), oskm_cli (FAIL: No module named '"'oskm_cli'), oskm_schema (FAIL: ...)
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
提示: 运行时来自单个 knowledge.tar.gz ... CLI 按三级候选解析（"'$OSKM_CLI → 源码树 → <runtime-root>/oskm-cli.pyz），全程不单独下载 CLI。
错误: 运行时依赖检查未通过。
exit=1
```

## 4. 本夹具下的一个现实提醒

错误文案把 `bootstrap.py install` 列为第一条可行做法，但**本次环境未配置 `OSKM_DOWNLOAD_ENDPOINT`**（`doctor` 已判 FAIL），所以第一条此时跑不通。在这个夹具里真正可行的是后两条：从源码仓 `python3 cli/scripts/build_cli.py` 构建后复制到 `<runtime-root>/oskm-cli.pyz`，或用 `OSKM_CLI` 直接指向 `$F/oskm-cli.pyz` / `$R/source-tree`。CLI 不单独下载——它和 `knowledge.db` 一起打在 `knowledge.tar.gz` 里，所以三级候选全程不联网。

## 5. 一句话总结

- 三者都在 → **`$OSKM_CLI` 赢**（kind=`env`）；未设 → 源码树（kind=`source`，锚点是 bootstrap 自身位置）；再没有 → `<runtime-root>/oskm-cli.pyz`（kind=`installed`）。
- 三者都缺 → `CliInstallError`，stderr 一行 `错误: ` 摘要 + **三条 attempt 逐条列因** + **三条可执行补救**，退出码 1，stdout 为空。

## 附：本次执行过的关键命令

```zsh
# 结构与一致性核对
find $R/tool -type f; diff -rq $R/tool/oskm_runtime $R/plain-tool/oskm_runtime
find $R -name '"'.env*' -maxdepth 4                       # 只有 .env.example，无 .env 干扰

# 产物校验与版本
"'$PY -c "...; ci.verify_pyz(p); ci.pyz_version(p)"        # fixtures 与 installed 均 OK, 1.0.0
$PY -c "...; ci._source_version('"'"'$R/source-tree/cli/oskm_cli/__init__.py'"')\"   # 9.9.9
"'$PY -c "...; ci.find_source_tree(<两个 bootstrap 的 cli_install.py>)"          # None / source-tree

# 解析矩阵（A–G，见 run_cases.sh 与 cases.log）
OSKM_CLI=$F/oskm-cli.pyz $PY $PLAIN --runtime-root $R/installed-runtime cli-path
OSKM_CLI=$F/oskm-cli.pyz $PY $INSRC --runtime-root $R/installed-runtime cli-path
env -u OSKM_CLI        $PY $PLAIN --runtime-root $R/installed-runtime cli-path
env -u OSKM_CLI        $PY $INSRC --runtime-root $R/installed-runtime cli-path
env -u OSKM_CLI        $PY $PLAIN --runtime-root $R/empty-runtime     cli-path   # 三候选全缺
OSKM_CLI=$F/nope.pyz   $PY $PLAIN --runtime-root $R/empty-runtime     cli-path
OSKM_CLI=$R/source-tree $PY $PLAIN --runtime-root $R/empty-runtime    cli-path

# kind/version 与边界
OSKM_CLI=<坏 pyz> $PY $PLAIN --runtime-root $R/installed-runtime update-cli
env -u OSKM_CLI $PY $PLAIN --runtime-root $R/empty-runtime doctor
```

未访问、未修改 `~/.oskm`；未修改 fixtures 目录（只读）；所有写操作都发生在 `$R/agent-start/`（`answer.md`、`run_cases.sh`、`cases.log`、`scratch-runtime/`）。
MD
wc -l answer.md && ls -la'
$ /bin/zsh -lc 'R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain; F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures; echo "== fixtures mtime (应为 16:18，未变) =="; ls -lT $F | awk '"'{print "'$6,$7,$8,$9,$10}'"'; echo \"== empty-runtime (应仍为空) ==\"; ls -A "'$R/empty-runtime | wc -l; echo "== ~/.oskm 是否存在 =="; ls -d ~/.oskm 2>&1 | tail -1'
```

### Agent 最终回答

```markdown
**结论：`cli-path` 选候选 1 —— `$OSKM_CLI`**
`resolve_cli()` 是固定三级顺序（`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/tool/oskm_runtime/cli_install.py:195`）：`$OSKM_CLI` → 源码树 → `<runtime-root>/oskm-cli.pyz`。三者齐备时 env 赢，实测：

- `OSKM_CLI=$F/oskm-cli.pyz` + `plain-tool/bootstrap.py` → 打印夹具路径，`describe()` 为 `(env, oskm-cli 1.0.0)`。
- 同一命令换成源码树内的 `bootstrap.py` → **仍是夹具路径**，即 env 压过候选 2。
- 去掉 `OSKM_CLI`：`plain-tool` 落到 `installed-runtime/oskm-cli.pyz (installed, 1.0.0)`；源码树内那份落到 `source-tree (source, 9.9.9)` —— 证明候选 2 的锚点是 bootstrap 自身位置，与 cwd、`--runtime-root` 无关（`--runtime-root` 只影响候选 3）。

**三候选全缺时的错误提示**
`empty-runtime` + 无 `OSKM_CLI` + `plain-tool` 实跑：stderr 输出 `错误: 找不到可用的 oskm-cli 产物…`，含 `已尝试：` 三条逐条列因（`1. $OSKM_CLI 未设置` / `2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py` / `3. <root>/oskm-cli.pyz —— 不存在`）与 `可行做法：` 三条补救（`install` / 构建后复制到固定名 / 用 `OSKM_CLI` 指过去），退出码 1，stdout 为空（便于 `$(...)` 取值）。相关分支我也验了：产物存在但坏掉时第 3 条原样报校验错（缺 shebang、不是有效 zip），`OSKM_CLI` 指坏产物会静默降级到候选 3 —— 所以排障要看 `update-cli` / `doctor`，别只看 `cli-path` 的路径。本环境 `OSKM_DOWNLOAD_ENDPOINT` 未配置，第一条补救实际跑不通，可用的是后两条。

**产出**
- `answer.md`：完整结论、命令与输出片段。
- `run_cases.sh` + `cases.log`：A–G 七组解析矩阵的可复现记录。
- `scratch-runtime/`：坏产物边界用例的临时目录。

夹具目录、`empty-runtime`、`~/.oskm` 均未改动（已核对 mtime 与是否存在）。
```

### Agent 写入的 answer.md

```markdown
# `bootstrap.py cli-path` 的 CLI 候选解析：实测结论

## 0. 路径缩写（下文沿用）

```
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
R=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain
F=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/fixtures
PLAIN=$R/plain-tool/bootstrap.py                                    # 不在源码树内
INSRC=$R/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py   # 在源码树内
```

工具代码：`$R/tool/bootstrap.py` + `$R/tool/oskm_runtime/`（与 `$R/plain-tool/`、源码树内那份逐字节相同，已用 `diff -rq` 验证）。

## 1. 直接回答（一）：三个候选都在时，`cli-path` 应该选哪个

**选候选 1 —— `$OSKM_CLI` 指向的那一份，即 `$F/oskm-cli.pyz`。**

优先级是硬编码的固定顺序，见 `$R/tool/oskm_runtime/cli_install.py:195`（`resolve_cli`）：

1. `$OSKM_CLI`（`environment.py:18` 定义 `CLI_PATH_ENV = 'OSKM_CLI'`）——显式覆盖，最高优先级
2. 源码树——从 **`cli_install.py` 自身位置**向上找 `cli/oskm_cli/__init__.py`（`cli_install.py:148`）
3. `<runtime-root>/oskm-cli.pyz`——`install` 落盘的固定名产物（`cli_install.py:171`）

三条要点，都由实跑证实：

- **`$OSKM_CLI` 赢过源码树，也赢过已安装产物。** 即使 bootstrap 本身在源码树内（候选 2 明明可用），只要 `OSKM_CLI` 指向一个可用产物，就用它。
- **候选 2 的锚点是 bootstrap 脚本自己的位置，不是 cwd，也不是 `--runtime-root`。** 同一条命令、同一个 cwd，`$PLAIN` 落到候选 3，`$INSRC` 落到候选 2。
- **`--runtime-root` 只影响候选 3。** 候选 1、2 与运行时根目录无关。

`$OSKM_CLI` 的合法取值有两种（`cli_install.py:157`）：后缀为 `.pyz` 且通过 `verify_pyz()` 的文件，或含 `cli/oskm_cli/__init__.py` 的源码树目录。

## 2. 实测命令与输出

复现脚本：`$R/agent-start/run_cases.sh`，完整输出留在 `$R/agent-start/cases.log`。

```
$ OSKM_CLI=$F/oskm-cli.pyz $PY $PLAIN --runtime-root $R/installed-runtime cli-path
/private/var/.../oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz        # ← 候选 1 命中
exit=0

$ OSKM_CLI=$F/oskm-cli.pyz $PY $INSRC --runtime-root $R/installed-runtime cli-path
/private/var/.../oskm-eval-without-skill-1czwlgti/fixtures/oskm-cli.pyz        # ← 源码树内也是候选 1
exit=0

$ env -u OSKM_CLI $PY $PLAIN --runtime-root $R/installed-runtime cli-path
/private/var/.../e06-cli-resolution-chain/installed-runtim
… [输出截断，完整内容见工作区] …
9.9
$PY -c "...; ci.find_source_tree(<两个 bootstrap 的 cli_install.py>)"          # None / source-tree

# 解析矩阵（A–G，见 run_cases.sh 与 cases.log）
OSKM_CLI=$F/oskm-cli.pyz $PY $PLAIN --runtime-root $R/installed-runtime cli-path
OSKM_CLI=$F/oskm-cli.pyz $PY $INSRC --runtime-root $R/installed-runtime cli-path
env -u OSKM_CLI        $PY $PLAIN --runtime-root $R/installed-runtime cli-path
env -u OSKM_CLI        $PY $INSRC --runtime-root $R/installed-runtime cli-path
env -u OSKM_CLI        $PY $PLAIN --runtime-root $R/empty-runtime     cli-path   # 三候选全缺
OSKM_CLI=$F/nope.pyz   $PY $PLAIN --runtime-root $R/empty-runtime     cli-path
OSKM_CLI=$R/source-tree $PY $PLAIN --runtime-root $R/empty-runtime    cli-path

# kind/version 与边界
OSKM_CLI=<坏 pyz> $PY $PLAIN --runtime-root $R/installed-runtime update-cli
env -u OSKM_CLI $PY $PLAIN --runtime-root $R/empty-runtime doctor
```

未访问、未修改 `~/.oskm`；未修改 fixtures 目录（只读）；所有写操作都发生在 `$R/agent-start/`（`answer.md`、`run_cases.sh`、`cases.log`、`scratch-runtime/`）。
```

## 执行记录

### 1. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结论：`cli-path` 选候选 1 —— `$OSKM_CLI`**
`resolve_cli()` 是固定三级顺序（`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/tool/oskm_runtime/cli_install.py:195`）：`$OSKM_CLI` → 源码树 → `<runtime-root>/oskm-cli.pyz`。三者齐备时 env 赢，实测：

- `OSKM_CLI=$F/oskm-cli.pyz` + `plain-tool/bootstrap.py` → 打印夹具路径，`describe()` 为 `(env, oskm-cli 1.0.0)`。
- 同一命令换成源码树内的 `bootstrap.py` → **仍是夹具路径**，即 env 压过候选 2。
- 去掉 `OSKM_CLI`：`plain-tool` 落到 `installed-runtime/oskm-cli.pyz (installed, 1.0.0)`；源码树内那份落到 `source-tree (source, 9.9.9)` —— 证明候选 2 的锚点是 bootstrap 自身位置，与 cwd、`--runtime-root` 无关（`--runtime-root` 只影响候选 3）。

**三候选全缺时的错误提示**
`empty-runtime` + 无 `OSKM_CLI` + `plain-tool` 实跑：stderr 输出 `错误: 找不到可用的 oskm-cli 产物…`，含 `已尝试：` 三条逐条列因（`1. $OSKM_CLI 未设置` / `2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py` / `3. <root>/oskm-cli.pyz —— 不存在`）与 `可行做法：` 三条补救（`install` / 构建后复制到固定名 / 用 `OSKM_CLI` 指过去），退出码 1，stdout 为空（便于 `$(...)` 取值）。相关分支我也验了：产物存在但坏掉时第 3 条原样报校验错（缺 shebang、不是有效 zip），`OSKM_CLI` 指坏产物会静默降级到候选 3 —— 所以排障要看 `update-cli` / `doctor`，别只看 `cli-path` 的路径。本环境 `OSKM_DOWNLOAD_ENDPOINT` 未配置，第一条补救实际跑不通，可用的是后两条。

**产出**
- `answer.md`：完整结论、命令与输出片段。
- `run_cases.sh` + `cases.log`：A–G 七组解析矩阵的可复现记录。
- `scratch-runtime/`：坏产物边界用例的临时目录。

夹具目录、`empty-runtime`、`~/.oskm` 均未改动（已核对 mtime 与是否存在）。
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/agent-start` · exit=0 · 420.9s

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
| 3 | 解析顺序与失败提示是否与实现一致（人工核对转录） | manual | 人工 | **结论：`cli-path` 选候选 1 —— `$OSKM_CLI`** `resolve_cli()` 是固定三级顺序（`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-without-skill-1czwlgti/without-skill/e06-cli-resolution-chain/tool/oskm_runti
… [输出截断，完整内容见工作区] …
ime/oskm-cli.pyz (installed, 1.0.0)`；源码树内那份落到 `source-tree (source, 9.9.9)` —— 证明候选 2 的锚点是 bootstrap |
| 4 | 整个过程工具没有联网 | auto | Pass | [] |
| 5 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
