# E7 refresh-is-explicit（with-skill 臂）

- 开始时间：2026-11-17T15:41:28+08:00
- 结束时间：2026-11-17T15:50:59+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit`
- 夹具服务端：http://127.0.0.1:61450
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

一个托管运行时已经过期，但用户只是直接执行 oskm-cli 查询，没有运行 refresh。请说明是否会下载，以及用户应如何更新运行时；再说明没有 .oskm-runtime.json 的自管库会怎样。

## 期望结果（来自 evals.json）

直接查询不会触发下载，应显式执行 bootstrap.py refresh 或 install；没有 .oskm-runtime.json 的自管库不会被刷新或覆盖。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| 查询不会自动下载 | `contains` |
| bootstrap.py refresh | `contains` |
| 自管库不会被刷新或覆盖 | `contains` |
| 刷新必须是显式动作，查询没有下载副作用 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：571.3 s
- 事件计数：`{"thread.started": 1, "item.completed": 75, "item:error": 1, "turn.started": 1, "item:reasoning": 21, "item:agent_message": 20, "item.started": 33, "item:command_execution": 66, "turn.completed": 1}`
- 读到 skill 文档：是（15 处）
- 执行的命令数：33
- token 用量：`{"input_tokens": 727754, "cached_input_tokens": 674688, "output_tokens": 20513, "reasoning_output_tokens": 6738}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && ls -la && echo \"---- tree ----\" && find . -maxdepth 3 -not -path '*/.git/*' | head -80"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && echo "=== PROMPT.md ===" && cat PROMPT.md && echo && echo "=== .oskm-runtime.json ===" && cat runtime/.oskm-runtime.json && echo && echo "=== runtime ls ===" && ls -la runtime runtime/interface runtime/interface/sdk-js runtime/interface/sdk_c 2>/dev/null | head -60 && echo "=== unmanaged ===" && ls -la unmanaged'
$ /bin/zsh -lc 'SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; find "$SKILL_DIR" -maxdepth 2 -type f | sort && echo "=== env ===" && env | grep -i -E '"'oskm|download' "
$ /bin/zsh -lc 'SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; wc -l "$SKILL_DIR"/bootstrap.py "$SKILL_DIR"/oskm_runtime/*.py && echo "=== state.py ===" && cat "$SKILL_DIR/oskm_runtime/state.py"'
$ /bin/zsh -lc 'SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; echo "=== doctor.py ===" && cat "$SKILL_DIR/oskm_runtime/doctor.py"'
$ /bin/zsh -lc 'SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; cat "$SKILL_DIR/oskm_runtime/bootstrap.py"'
$ /bin/zsh -lc "SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; grep -n \"needs_refresh\\|def refresh\\|非托管\\|unmanaged\" -r \""'$SKILL_DIR/oskm_runtime" "$SKILL_DIR/bootstrap.py" | head -40'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && echo \"=== BEFORE: hashes/mtimes ===\" && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json unmanaged/knowledge.db && stat -f '%N mtime=%Sm size=%z' -t '%Y-%m-%dT%H:%M:%S' runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json unmanaged/knowledge.db && echo && echo \"=== unmanaged dir contents ===\" && ls -a unmanaged"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/runtime" doctor; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI="$PWD/runtime/oskm-cli.pyz" && DB="$PWD/runtime/knowledge.db" && echo "=== query 1: arch overview (stale managed runtime, endpoint as given) ===" && time $PY "$CLI" --db "$DB" arch overview 2>&1 | head -40; echo "exit=${pipestatus[1]}"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI="$PWD/runtime/oskm-cli.pyz" && DB="$PWD/runtime/knowledge.db" && echo "=== query 2: ask get_scan_info ===" && $PY "$CLI" --db "$DB" ask get_scan_info 2>&1 | head -40; echo "exit=$?"; echo; echo "=== query 3: SAME query with DEAD endpoint (proves no network on query path) ===" && OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/dead $PY "$CLI" --db "$DB" arch overview 2>&1 | head -25; echo "exit=${pipestatus[1]}"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && echo \"=== AFTER queries: hashes ===\" && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json unmanaged/knowledge.db && echo \"=== state file date/updated_at ===\" && grep -E '\"date\"|\"updated_at\"' runtime/.oskm-runtime.json | head -4 && echo \"=== runtime dir listing (any temp/new files?) ===\" && ls -a runtime && echo \"=== unmanaged dir listing ===\" && ls -a unmanaged"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && CLI="$PWD/runtime/oskm-cli.pyz" && echo "=== query 4: unmanaged db (no .oskm-runtime.json), DEAD endpoint too ===" && OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/dead $PY "$CLI" --db "$PWD/unmanaged/knowledge.db" arch overview 2>&1 | head -20; echo "exit=${pipestatus[1]}"; echo; echo "=== unmanaged dir after query ===" && ls -a unmanaged && shasum -a 256 unmanaged/knowledge.db'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY - <<'"'EOF'
import sys
sys.path.insert(0, \"/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query\")
from oskm_runtime import state
base = \"/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit\"
managed = base + \"/runtime/knowledge.db\"
unmanaged = base + \"/unmanaged/knowledge.db\"
print(\"today() =\", state.today())
print(\"managed   state file:\", state.state_path(managed), \"exists:\", state.state_path(managed).is_file())
print(\"managed   load_state ->\", (state.load_state(managed) or {}).get(\"date\"), \"needs_refresh =\", state.needs_refresh(managed))
print(\"unmanaged state file:\", state.state_path(unmanaged), \"exists:\", state.state_path(unmanaged).is_file())
print(\"unmanaged load_state ->\", state.load_state(unmanaged), \"needs_refresh =\", state.needs_refresh(unmanaged))
EOF"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== CLI pyz top-level modules ===" && $PY -m zipfile -l runtime/oskm-cli.pyz | awk '"'{print "'$1}'"' | grep -v '/' | head -20 && echo \"=== does the CLI contain any network/download/refresh code? ===\" && "'$PY - <<'"'EOF'
import re, zipfile
z = zipfile.ZipFile(\"runtime/oskm-cli.pyz\")
pat = re.compile(r\"urlopen|urllib|http\\.client|socket|requests\\.|download|bootstrap|needs_refresh|oskm-runtime|OSKM_DOWNLOAD\", re.I)
hits = {}
for name in z.namelist():
    if not name.endswith((\".py\", \".pyc\")):
        continue
    data = z.read(name)
    try:
        text = data.decode(\"utf-8\", \"ignore\")
    except Exception:
        continue
    found = sorted(set(m.group(0).lower() for m in pat.finditer(text)))
    if found:
        hits[name] = found
print(\"matching files:\", len(hits))
for k, v in sorted(hits.items())[:20]:
    print(\" \", k, v)
EOF"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY - <<'"'EOF'
import re, zipfile
z = zipfile.ZipFile(\"runtime/oskm-cli.pyz\")
for name in (\"__main__.py\", \"oskm_cli/cli.py\", \"oskm_cli/query/arkts/query.py\"):
    text = z.read(name).decode(\"utf-8\", \"ignore\")
    print(\"=\" * 20, name)
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r\"urlopen|urllib|socket|download|bootstrap|needs_refresh|oskm-runtime\", line, re.I):
            print(f\"{i:5d}: {line.strip()[:160]}\")
EOF"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== bootstrap.py refuses query subcommands (no passthrough, so no implicit refresh) ===" && $PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/runtime" arch overview; echo "exit=$?"; echo; echo "=== CLI --version / top-level help ===" && $PY runtime/oskm-cli.pyz --version; $PY runtime/oskm-cli.pyz --help 2>&1 | head -30'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== query with MISSING --db (live endpoint) -> must NOT auto-download ===" && $PY runtime/oskm-cli.pyz --db "$PWD/scratch-does-not-exist/knowledge.db" arch overview; echo "exit=$?"; echo "--- did anything get created? ---"; ls -a . ; ls -a scratch-does-not-exist 2>&1 | head -3'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && mkdir -p scratch/unmanaged-copy && cp -R runtime scratch/runtime-copy && cp unmanaged/knowledge.db scratch/unmanaged-copy/knowledge.db && echo \"=== scratch prepared ===\" && find scratch -maxdepth 2 | sort && shasum -a 256 scratch/runtime-copy/knowledge.db scratch/unmanaged-copy/knowledge.db && grep '\"date\"' scratch/runtime-copy/.oskm-runtime.json | head -3"
$ /bin/zsh -lc "SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '1,60p' \""'$SKILL_DIR/oskm_runtime/install.py"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== doctor on SELF-MANAGED copy ===" && $PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/unmanaged-copy" doctor 2>&1 | grep -E '"'Runtime root|Runtime state|Runtime database'; echo; echo \"=== refresh on SELF-MANAGED copy ===\" && "'$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/unmanaged-copy" refresh; echo "exit=$?"; echo "--- files after ---"; ls -a scratch/unmanaged-copy; shasum -a 256 scratch/unmanaged-copy/knowledge.db'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== refresh on STALE MANAGED copy (endpoint live) ===" && time $PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/runtime-copy" refresh; echo "exit=$?"; echo "--- state after ---"; grep -E '"'\"version\"|\"source\"|\"date\"|\"updated_at\"' scratch/runtime-copy/.oskm-runtime.json | head -6; shasum -a 256 scratch/runtime-copy/knowledge.db scratch/runtime-copy/oskm-cli.pyz; ls -a scratch/runtime-copy"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== refresh AGAIN on the just-refreshed copy (idempotent, no 2nd download) ===" && $PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/runtime-copy" refresh; echo "exit=$?"; echo; echo "=== query the refreshed copy ===" && $PY scratch/runtime-copy/oskm-cli.pyz --db "$PWD/scratch/runtime-copy/knowledge.db" arch overview --format table 2>&1 | head -12'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && echo \"=== FIXTURE INTEGRITY (must match BEFORE snapshot) ===\" && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json unmanaged/knowledge.db && stat -f '%N mtime=%Sm' -t '%Y-%m-%dT%H:%M:%S' runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json unmanaged/knowledge.db && echo \"=== fixture dirs contain no new files ===\" && ls -a runtime unmanaged && echo \"=== state still stale? ===\" && grep -m2 -E '\"date\"|\"updated_at\"' runtime/.oskm-runtime.json"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== refreshed copy, table format ===" && $PY scratch/runtime-copy/oskm-cli.pyz --db "$PWD/scratch/runtime-copy/knowledge.db" --format table arch overview 2>&1 | head -14'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== cli-path (fixture runtime root) ===" && $PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/runtime" cli-path; echo "exit=$?"; echo "=== fixture state date still 20261116? ==="; grep -m1 '"'\"date\"' runtime/.oskm-runtime.json"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && cp -R runtime scratch/stale-copy && echo "=== refresh with DEAD endpoint on stale copy ===" && OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/dead $PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/stale-copy" refresh 2>&1 | tail -5; echo "exit=${pipestatus[1]}"; echo "--- old runtime still intact & queryable? ---"; shasum -a 256 scratch/stale-copy/knowledge.db; grep -m1 '"'\"date\"' scratch/stale-copy/.oskm-runtime.json; ls -a scratch/stale-copy; "'$PY scratch/stale-copy/oskm-cli.pyz --db "$PWD/scratch/stale-copy/knowledge.db" arch overview | head -6'
$ /bin/zsh -lc "SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; grep -n \"def install_runtime\\|def _install_artifacts\\|def _do_install\\|state_path\\|write_state\\|os.replace\\|backup\" \""'$SKILL_DIR/oskm_runtime/install.py" | head -30; echo "=== install_runtime body ==="; sed -n '"'/"'^def install_runtime/,/''^def /p'"' \""'$SKILL_DIR/oskm_runtime/install.py" | head -70'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && SKILL_DIR=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && mkdir -p scratch/unmanaged-install-test && cp unmanaged/knowledge.db scratch/unmanaged-install-test/knowledge.db && echo "before: $(shasum -a 256 scratch/unmanaged-install-test/knowledge.db)" && echo "=== install --runtime-root <self-managed dir> ===" && $PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/unmanaged-install-test" install 2>&1 | tail -4; echo "exit=${pipestatus[1]}"; echo "--- after ---"; ls -a scratch/unmanaged-install-test; shasum -a 256 scratch/unmanaged-install-test/knowledge.db 2>/dev/null; grep -m2 -E '"'\"source\"|\"date\"' scratch/unmanaged-install-test/.oskm-runtime.json 2>/dev/null"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && apply_patch <<'PATCH'
*** Begin Patch
*** Add File: answer.md
+# 过期托管运行时：查询不下载，refresh 才是显式更新动作

+结论先行（三个问题）：
+
+1. **用户只跑 "'`oskm-cli` 查询，不会触发任何下载**——即使状态文件里 `date=20261116`
+   已经比今天 `20261117` 旧。查询路径完全不联网，用旧快照照常秒回。
+2. **数据过期时的正确动作是显式刷新**：
+   `python3 <skill>/bootstrap.py --runtime-root <runtime> refresh`
+   （幂等，只在过期/不完整时才下载；要强制重装用 `install`，要指定日期加 `--date YYYYMMDD`）。
+   刷新前可用 `doctor` 看当前 `date`，刷新后用 `cli-path` 确认 CLI 位置。
+3. **没有 `.oskm-runtime.json` 的自管库不会被刷新、也不会被覆盖**：
+   `needs_refresh()` 对无状态文件的库直接返回 `False`，`refresh` 打印
+   "运行时已是最新，无需刷新" 就退出，不建状态文件、不改库、不联网；
+   查询用 `--db <path>` 直接读它即可。**唯一会写它的动作是用户自己把那个目录
+   当 `--runtime-root` 传给 `install`**（实测会把它变成托管运行时，见下）。
+
+---
+
+## 1. 环境确认（doctor：过期，但 ready）
+
+```bash
+SKILL_DIR=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
+PY=/opt/homebrew/opt/python@3.12/bin/python3.12
+RUNTIME=$PWD/runtime
+$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" doctor
+```
+
+```text
+Python: 3.12.16 (OK, requires Python 3.10+)
+Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
+CLI: .../e07-refresh-is-explicit/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
+Runtime state: version 3, date 20261116, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
+Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
+提示: bootstrap.py 不跑查询。查询直接调 <runtime-root>/oskm-cli.pyz --db ...
+exit=0
+```
+
+`date 20261116` 与今天 `20261117` 不一致 = 已过期，但 doctor 仍判 ready：
+过期只影响"下一次按日期刷新"，不影响查询可用性。
+
+## 2. 直接查询：不下载
+
+```bash
+CLI="$PWD/runtime/oskm-cli.pyz"; DB="$PWD/runtime/knowledge.db"
+time $PY "$CLI" --db "$DB" arch overview
+$PY "$CLI" --db "$DB" ask get_scan_info
+```
+
+```text
+{ "product": "synthetic", "scan_id": 1, "subsystems": 2, "counts": { ... } }
+0.08s user 0.01s system 96% cpu 0.096 total     # 秒回，没有几十秒的下载
+exit=0
+```
+
+**反证一：把端点换成死地址，同一条查询照样成功。**
+
+```bash
+OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/dead $PY "$CLI" --db "$DB" arch overview
+# exit=0，输出与上面完全一致
+```
+
+**反证二：查询前后文件一个字节都没变，也没多出临时文件。**
+
+```text
+f561e39f...5fcd1b44  runtime/knowledge.db          （查询前后相同）
+ad760c16...cd5eb49e  runtime/oskm-cli.pyz          （查询前后相同）
+3f04b0eb...829fa6bb  runtime/.oskm-runtime.json    （date 仍是 20261116）
+runtime mtime=2026-11-17T15:41:28                  （查询后未变）
+```
+
+**反证三：CLI 产物里根本没有下载代码。** 扫描 `oskm-cli.pyz` 全部 `.py`，
+命中 `urlopen/urllib/socket/download/bootstrap/OSKM_DOWNLOAD` 的只有 3 处：
+`oskm_cli/query/arkts/query.py` 的 `from urllib.parse import quote`（字符串转义，非网络），
+以及 `__main__.py` / `oskm_cli/cli.py` 里指向 skill 的**提示文案**。CLI 自己的 help 也写着：
+
+```text
+OpenHarmony 产品事实库的只读查询（独立产物，不下载数据）。
+```
+
+**反证四：`--db` 指向不存在的路径也不会自动下载。**
+
+```bash
+$PY runtime/oskm-cli.pyz --db "$PWD/scratch-does-not-exist/knowledge.db" arch overview
+```
+
+```text
+error: database not found: .../scratch-does-not-exist/knowledge.db. 检查 --db 路径；
+托管运行时请用 ... skill 的 `python3 <skill>/bootstrap.py install --runtime-root ~/.oskm` 安装...
+CLI 不会为任意缺失路径自动下载。
+exit=3        # 3 = 库打不开；目录没有被创建
+```
+
+**反证五：`bootstrap.py` 不再透传查询命令**，所以"查询前顺手刷新"这个挂载点已经不存在。
+
+```bash
+$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" arch overview
+# 错误: 未知命令 arch。bootstrap.py 只负责安装，查询请直接调 CLI：...
+# 可用命令: doctor, install, refresh, update-cli, download-db, validate-db, cli-path   exit=2
+```
+
+## 3. 正确的更新动作：显式 refresh
+
+判定函数（只读实测）：
+
+```bash
+$PY -c '"'from oskm_runtime import state; print(state.today(), state.needs_refresh(\"<runtime>/knowledge.db\"))'
+# today() = 20261117 ; managed needs_refresh = True ; unmanaged needs_refresh = False
+"'```
+
+刷新演示（为不动 fixtures，在 `scratch/runtime-copy` 这份副本上跑）：
+
+```bash
+$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/runtime-copy" refresh
+```
+
+```text
+==> 下载 INTERNAL_CI 运行时: 20261117
+==> 运行时安装完成: .../scratch/runtime-copy
+exit=0
+状态文件: "date": "20261116" -> "20261117", "updated_at": "2026-11-17T15:46:19+08:00"
+```
+
+再跑一次同一条命令，不下载：
+
+```text
+==> 运行时已是最新，无需刷新: .../scratch/runtime-copy      exit=0
+```
+
+刷新失败也不破坏已有运行时（死端点实测，`scratch/stale-copy`）：
+
+```text
+==> 下载 INTERNAL_CI 运行时: 20261117
+错误: 下载失败（网络或代理不可用）: http://127.0.0.1:1/dead/20261117:
+      <urlopen error [Errno 61] Connection refused>. 检查网络、DNS、HTTPS_PROXY/... exit=1
+# 旧库原样保留：sha256 未变、date 仍 20261116，查询照样 exit=0
+```
+
+推荐流程：
+
+```bash
+$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" doctor      # 看 date 是否过期
+$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" refresh     # 过期才下载（幂等）
+$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" cli-path    # 确认 CLI 实际位置
+$PY "$($PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" cli-path)" '"\\
+    --db \""'$RUNTIME/knowledge.db" arch overview                      # 再查询
+```
+
+源码树优先：cwd 在 OH 源码树内（或传 `--source-root <OH源码根>`）时，
+`install`/`refresh` 会先用本地 `out/**/oskm/knowledge.db` + `oskm-cli.pyz` + `interface/sdk-*`，可用则不联网。
+
+## 4. 自管库（无 .oskm-runtime.json）：不刷新、不覆盖
+
+```bash
+$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/unmanaged-copy" doctor
+$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/unmanaged-copy" refresh
+```
+
+```text
+Runtime state: 非托管（没有 .oskm-runtime.json），`bootstrap.py refresh` 不会碰它
+==> 运行时已是最新，无需刷新: .../scratch/unmanaged-copy      exit=0
+目录内容仍是: knowledge.db（没有 .oskm-runtime.json / interface / oskm-cli.pyz）
+sha256 f561e39f...5fcd1b44 未变
+```
+
+查询它完全正常，且同样不联网（死端点下 exit=0）：
+
+```bash
+OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/dead '"\\
+  "'$PY "$CLI" --db "$PWD/unmanaged/knowledge.db" arch overview   # exit=0
+```
+
+机制：`needs_refresh()` 读不到状态文件就返回 `False`（注释写明"没有状态文件的库是
+自管输入，为了兼容手工 `artifacts/*/knowledge.db` 而不去动它"）；`update_state()`
+对无状态文件也是 no-op。日期比较只对 `source != local` 的托管状态生效。
+
+**注意（唯一的例外）**：把自管库目录当 `--runtime-root` 传给 `install`，
+它会下载并原子替换该目录内容、写出状态文件，从此变成托管运行时（实测 `scratch/unmanaged-install-test`）：
+
+```text
+==> 下载 INTERNAL_CI 运行时: 20261117
+==> 运行时安装完成: .../scratch/unmanaged-install-test        exit=0
+after: .oskm-runtime.json  interface  knowledge.db  oskm-cli.pyz
+```
+
+所以手工库只应出现在 `--db` 里，不要出现在 `--runtime-root` 里。
+
+## 5. 边界与顺带观察
+
+- fixtures（`runtime/`、`unmanaged/`）**全程未被修改**：查询/refresh/install 演示都在
+  工作区内的 `scratch/` 副本上做；结束时 `runtime/.oskm-runtime.json` 仍是 `date=20261116`，
+  四个文件 sha256 与 mtime 与开始前一致。未访问 `~/.oskm`。
+- 下载端点只在**显式** `refresh` / `install` 时被请求（本次共 2 次成功请求，都发生在
+  `scratch/` 副本上）；所有查询请求数为 0。
+- `scratch/` 是本次演示产物（4 份副本），可整目录删除。
+- 证据边界：这份快照 `status=complete`，但 `arch overview` 里 `elf_modules=0`
+  （而 `get_scan_info` 的 `elf_modules` collector `record_count=1`）。按 skill 硬约束，
+  计数为 0 表示"该证据未采集"，**不能**用它回答依赖/影响面类问题，也不要把它当成"没有依赖"。
*** End Patch
PATCH
echo "written"; ls -la answer.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && cat > answer.md <<'EOF'
# 过期托管运行时：查询不下载，refresh 才是显式更新动作

结论先行（三个问题）：

1. **用户只跑 "'`oskm-cli` 查询，不会触发任何下载**——即使状态文件里 `date=20261116` 已经比今天 `20261117` 旧。查询路径完全不联网，用旧快照照常秒回。
2. **数据过期时的正确动作是显式刷新**：`python3 <skill>/bootstrap.py --runtime-root <runtime> refresh`（幂等，只在过期/不完整时才下载；要强制重装用 `install`，要指定日期加 `--date YYYYMMDD`）。刷新前可用 `doctor` 看当前 `date`，刷新后用 `cli-path` 确认 CLI 位置。
3. **没有 `.oskm-runtime.json` 的自管库不会被刷新、也不会被覆盖**：`needs_refresh()` 对无状态文件的库直接返回 `False`，`refresh` 打印“运行时已是最新，无需刷新”就退出，不建状态文件、不改库、不联网；查询用 `--db <path>` 直接读它即可。**唯一会写它的动作是用户自己把那个目录当 `--runtime-root` 传给 `install`**（实测会把它变成托管运行时，见 §4）。

---

## 1. 环境确认（doctor：过期，但 ready）

```bash
SKILL_DIR=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
RUNTIME=$PWD/runtime
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" doctor
```

```text
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: .../e07-refresh-is-explicit/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Runtime state: version 3, date 20261116, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
提示: bootstrap.py 不跑查询。查询直接调 <runtime-root>/oskm-cli.pyz --db ...
exit=0
```

`date 20261116` 与今天 `20261117` 不一致 = 已过期，但 doctor 仍判 ready：过期只影响“下一次按日期刷新”，不影响查询可用性。

## 2. 直接查询：不下载

```bash
CLI="$PWD/runtime/oskm-cli.pyz"; DB="$PWD/runtime/knowledge.db"
time $PY "$CLI" --db "$DB" arch overview
$PY "$CLI" --db "$DB" ask get_scan_info
```

```text
{ "product": "synthetic", "scan_id": 1, "subsystems": 2, "counts": { ... } }
0.08s user 0.01s system 96% cpu 0.096 total     # 秒回，没有几十秒的下载
exit=0
```

**反证一：把端点换成死地址，同一条查询照样成功。**

```bash
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/dead $PY "$CLI" --db "$DB" arch overview
# exit=0，输出与上面完全一致
```

**反证二：查询前后文件一个字节都没变，也没多出临时文件。**

```text
f561e39f...5fcd1b44  runtime/knowledge.db          （查询前后相同）
ad760c16...cd5eb49e  runtime/oskm-cli.pyz          （查询前后相同）
3f04b0eb...829fa6bb  runtime/.oskm-runtime.json    （date 仍是 20261116）
runtime/*.  mtime=2026-11-17T15:41:28              （查询后未变）
```

**反证三：CLI 产物里根本没有下载代码。** 扫描 `oskm-cli.pyz` 全部 `.py`，命中 `urlopen|urllib|socket|download|bootstrap|OSKM_DOWNLOAD` 的只有 3 处：`oskm_cli/query/arkts/query.py` 的 `from urllib.parse import quote`（字符串转义，非网络），以及 `__main__.py` / `oskm_cli/cli.py` 里指向 skill 的**提示文案**。CLI 自己的 help 也写着：

```text
OpenHarmony 产品事实库的只读查询（独立产物，不下载数据）。
```

**反证四：`--db` 指向不存在的路径也不会自动下载。**

```bash
$PY runtime/oskm-cli.pyz --db "$PWD/scratch-does-not-exist/knowledge.db" arch overview
```

```text
error: database not found: .../scratch-does-not-exist/knowledge.db. 检查 --db 路径；
托管运行时请用 ... skill 的 `python3 <skill>/bootstrap.py install --runtime-root ~/.oskm` 安装...
CLI 不会为任意缺失路径自动下载。
exit=3        # 3 = 库打不开；该目录也没有被创建
```

**反证五：`bootstrap.py` 不再透传查询命令**，所以“查询前顺手刷新”这个挂载点已经不存在。

```bash
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" arch overview
```

```text
错误: 未知命令 arch。bootstrap.py 只负责安装，查询请直接调 CLI：
  python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db <ask|arch|diff|sql> …
可用命令: doctor, install, refresh, update-cli, download-db, validate-db, cli-path
exit=2
```

## 3. 正确的更新动作：显式 refresh

判定函数（只读实测）：

```text
today() = 20261117
managed   load_state -> 20261116   needs_refresh = True
unmanaged load_state -> None       needs_refresh = False
```

刷新演示（为不动 fixtures，在 `scratch/runtime-copy` 这份副本上跑）：

```bash
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/runtime-copy" refresh
```

```text
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: .../scratch/runtime-copy
exit=0
状态文件: "date": "20261116" -> "20261117", "updated_at": "2026-11-17T15:46:19+08:00"
```

紧接着再跑同一条命令，不再下载：

```text
==> 运行时已是最新，无需刷新: .../scratch/runtime-copy      exit=0
```

刷新失败也不破坏已有运行时（死端点实测，`scratch/stale-copy`）：

```text
==> 下载 INTERNAL_CI 运行时: 20261117
错误: 下载失败（网络或代理不可用）: http://127.0.0.1:1/dead/20261117:
      <urlopen error [Errno 61] Connection refused>. 检查网络、DNS、HTTPS_PROXY/... exit=1
# 旧库原样保留：sha256 未变、date 仍 20261116，查询照样 exit=0
```

推荐流程：

```bash
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" doctor      # 看 date 是否过期
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" refresh     # 过期才下载（幂等）
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" cli-path    # 确认 CLI 实际位置
CLI=$($PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" cli-path)
$PY "$CLI" --db "$RUNTIME/knowledge.db" arch overview               # 再查询
```

源码树优先：cwd 在 OH 源码树内（或传 `--source-root <OH源码根>`）时，`install`/`refresh` 会先用本地 `out/**/oskm/knowledge.db` + `oskm-cli.pyz` + `interface/sdk-*`，可用则不联网。

## 4. 自管库（无 .oskm-runtime.json）：不刷新、不覆盖

```bash
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/unmanaged-copy" doctor
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$PWD/scratch/unmanaged-copy" refresh
```

```text
Runtime state: 非托管（没有 .oskm-runtime.json），`bootstrap.py refresh` 不会碰它
==> 运行时已是最新，无需刷新: .../scratch/unmanaged-copy      exit=0
目录内容仍是: knowledge.db（没有 .oskm-runtime.json / interface / oskm-cli.pyz）
sha256 f561e39f...5fcd1b44 未变
```

查询它完全正常，且同样不联网（死端点下 exit=0）：

```bash
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/dead '"\\
  "'$PY "$CLI" --db "$PWD/unmanaged/knowledge.db" arch overview   # exit=0，输出正常
```

机制：`needs_refresh()` 读不到状态文件就返回 `False`（docstring 写明“没有状态文件的库是自管输入，为兼容手工 `artifacts/*/knowledge.db` 而不去动它”）；`update_state()` 对无状态文件也是 no-op；按日期比较只对 `source != local` 的托管状态生效。

**注意（唯一的例外）**：把自管库目录当 `--runtime-root` 传给 `install`，它会下载并原子替换该目录内容、写出状态文件，从此变成托管运行时（实测 `scratch/unmanaged-install-test`）：

```text
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: .../scratch/unmanaged-install-test        exit=0
after: .oskm-runtime.json  interface  knowledge.db  oskm-cli.pyz
```

所以手工库只应出现在 `--db` 里，不要出现在 `--runtime-root` 里。

## 5. 边界与顺带观察

- fixtures（`runtime/`、`unmanaged/`）**全程未被修改**：查询与 refresh/install 演示都在工作区内的 `scratch/` 副本上做；结束时 `runtime/.oskm-runtime.json` 仍是 `date=20261116`，四个文件的 sha256 与 mtime 与开始前完全一致。未访问 `~/.oskm`。
- 下载端点只在**显式** `refresh` / `install` 时被请求（本次共 2 次成功请求，都发生在 `scratch/` 副本上）；所有查询产生的请求数为 0。
- `scratch/` 是本次演示产物（4 份副本），可整目录删除。
- 证据边界：这份快照 `status=complete`，但 `arch overview` 里 `elf_modules=0`（而 `get_scan_info` 的 `elf_modules` collector `record_count=1`）。按 skill 硬约束，计数为 0 表示“该证据未采集”，**不能**用它回答依赖/影响面类问题，也不要把它当成“没有依赖”。
EOF
echo "written:" && wc -l answer.md && ls -la answer.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && echo \"=== FINAL fixture integrity ===\" && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz runtime/.oskm-runtime.json unmanaged/knowledge.db && grep -m1 '\"date\"' runtime/.oskm-runtime.json && ls -a unmanaged && echo \"=== workspace ===\" && ls -la . && echo \"=== answer.md head ===\" && head -8 answer.md"
```

### Agent 最终回答

```markdown
**直接回答**
- 只跑查询**不会下载**：`arch overview` / `ask get_scan_info` 在 `date=20261116`（今天 `20261117`）的过期运行时上 0.096s 返回，把 `OSKM_DOWNLOAD_ENDPOINT` 换成死地址 `http://127.0.0.1:1/dead` 结果完全一样；查询前后 `runtime/` 三个文件的 sha256、mtime 均未变，也没多出临时文件。
- 机制上有四重保证：`oskm-cli.pyz` 内无任何网络代码（唯一的 `urllib` 是 `urllib.parse.quote`），CLI help 自称“独立产物，不下载数据”；缺失 `--db` 报 `exit=3` 并明说“CLI 不会为任意缺失路径自动下载”；`bootstrap.py` 已删除查询透传（`arch` 报未知命令 `exit=2`），所以不存在“查询前顺手刷新”的挂载点。
- 过期时的正确动作是**显式** `python3 <skill>/bootstrap.py --runtime-root <runtime> refresh`：实测在 `scratch/runtime-copy` 上下载 `INTERNAL_CI 20261117`，状态 `date` 由 `20261116` 变 `20261117`；紧接着再跑一次只打印“运行时已是最新，无需刷新”。刷新失败（死端点，`exit=1`）时旧库原样保留、查询照常可用。
- 没有 `.oskm-runtime.json` 的自管库：`needs_refresh()` 直接返回 `False`，`doctor` 报“非托管…`bootstrap.py refresh` 不会碰它”，`refresh` 空转退出且不建状态文件、不改库；`--db unmanaged/knowledge.db` 查询正常。**唯一例外**是用户自己把该目录当 `--runtime-root` 传给 `install` —— 实测会下载、原子替换并写入状态文件，把它变成托管运行时。

**产物与边界**
- 结论、命令与输出片段写在 `answer.md:1`（含推荐流程 `doctor → refresh → cli-path → 查询`）。
- fixtures 未被修改：`runtime/.oskm-runtime.json` 仍是 `date=20261116`，四个文件 sha256 与开始前一致，`unmanaged/` 仍只有 `knowledge.db`；所有 refresh/install 演示都在工作区内的 `scratch/` 副本上做，未访问 `~/.oskm`。下载端点仅被显式 refresh/install 命中 2 次，查询命中 0 次。
- 顺带一提：这份快照 `elf_modules=0`，按 skill 硬约束不能用它回答依赖/影响面问题（已在 `answer.md:175` 记录）。

需要我把 `scratch/` 清掉，或直接在真实 `runtime/` 上跑一次 `refresh` 把它更新到今天吗？
```

### Agent 写入的 answer.md

```markdown
# 过期托管运行时：查询不下载，refresh 才是显式更新动作

结论先行（三个问题）：

1. **用户只跑 `oskm-cli` 查询，不会触发任何下载**——即使状态文件里 `date=20261116` 已经比今天 `20261117` 旧。查询路径完全不联网，用旧快照照常秒回。
2. **数据过期时的正确动作是显式刷新**：`python3 <skill>/bootstrap.py --runtime-root <runtime> refresh`（幂等，只在过期/不完整时才下载；要强制重装用 `install`，要指定日期加 `--date YYYYMMDD`）。刷新前可用 `doctor` 看当前 `date`，刷新后用 `cli-path` 确认 CLI 位置。
3. **没有 `.oskm-runtime.json` 的自管库不会被刷新、也不会被覆盖**：`needs_refresh()` 对无状态文件的库直接返回 `False`，`refresh` 打印“运行时已是最新，无需刷新”就退出，不建状态文件、不改库、不联网；查询用 `--db <path>` 直接读它即可。**唯一会写它的动作是用户自己把那个目录当 `--runtime-root` 传给 `install`**（实测会把它变成托管运行时，见 §4）。

---

## 1. 环境确认（doctor：过期，但 ready）

```bash
SKILL_DIR=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
RUNTIME=$PWD/runtime
$PY "$SKILL_DIR/bootstrap.py" --runtime-root "$RUNTIME" doctor
```

```text
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: .../e07-refresh-is-explicit/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Runtime state: version 3, date 20261116, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
提示: bootstrap.py 不跑查询。查询直接调 <runtime-root>/oskm-cli.pyz --db ...
exit=0
```

`date 20261116` 与今天 `20261117` 不一致 = 已过期，但 doctor 仍判 ready：过期只影响“下一次按日期刷新”，不影响查询可用性。

## 2. 直接查询：不下载

```bash
CLI="$PWD/runtime/oskm-cli.pyz"; DB="$PWD/runtime/knowledge.db"
time $PY "$CLI" --db "$DB" arch overview
$PY "$CLI" --db "$DB" ask get_scan_info
```

```text
{ "product": "synthetic", "scan_id": 1, "subsystems": 2, "counts": { ... } }
0.08s user 0.01s system 96% cpu 0.096 total     # 秒回，没有几十秒的下载
exit=0
```

**反证一：把端点换成死地址，同一条查询照样成功。**

```bash
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/dead $PY "$CLI" --db "$DB" arch overview
# exit=0，输出与上面完全一致
```

**反证二：查询前后文件一个字节都没变，也没多出临时文件。**

```text
f561e39f...5fcd1b44  runtime/knowledge.db          （查询前后相同）
ad760c16...cd5eb49e  runtime/oskm-cli.pyz          （查询前后相同）
3f04b0eb...
… [输出截断，完整内容见工作区] …
ocstring 写明“没有状态文件的库是自管输入，为兼容手工 `artifacts/*/knowledge.db` 而不去动它”）；`update_state()` 对无状态文件也是 no-op；按日期比较只对 `source != local` 的托管状态生效。

**注意（唯一的例外）**：把自管库目录当 `--runtime-root` 传给 `install`，它会下载并原子替换该目录内容、写出状态文件，从此变成托管运行时（实测 `scratch/unmanaged-install-test`）：

```text
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: .../scratch/unmanaged-install-test        exit=0
after: .oskm-runtime.json  interface  knowledge.db  oskm-cli.pyz
```

所以手工库只应出现在 `--db` 里，不要出现在 `--runtime-root` 里。

## 5. 边界与顺带观察

- fixtures（`runtime/`、`unmanaged/`）**全程未被修改**：查询与 refresh/install 演示都在工作区内的 `scratch/` 副本上做；结束时 `runtime/.oskm-runtime.json` 仍是 `date=20261116`，四个文件的 sha256 与 mtime 与开始前完全一致。未访问 `~/.oskm`。
- 下载端点只在**显式** `refresh` / `install` 时被请求（本次共 2 次成功请求，都发生在 `scratch/` 副本上）；所有查询产生的请求数为 0。
- `scratch/` 是本次演示产物（4 份副本），可整目录删除。
- 证据边界：这份快照 `status=complete`，但 `arch overview` 里 `elf_modules=0`（而 `get_scan_info` 的 `elf_modules` collector `record_count=1`）。按 skill 硬约束，计数为 0 表示“该证据未采集”，**不能**用它回答依赖/影响面类问题，也不要把它当成“没有依赖”。
```

## 执行记录

### 1. [夹具准备] 装一个 date=20261116 的托管运行时（已过期）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit/runtime install --source INTERNAL_CI --date 20261116
stderr:
==> 下载 INTERNAL_CI 运行时: 20261116
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit` · exit=0 · 0.12s

### 2. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**直接回答**
- 只跑查询**不会下载**：`arch overview` / `ask get_scan_info` 在 `date=20261116`（今天 `20261117`）的过期运行时上 0.096s 返回，把 `OSKM_DOWNLOAD_ENDPOINT` 换成死地址 `http://127.0.0.1:1/dead` 结果完全一样；查询前后 `runtime/` 三个文件的 sha256、mtime 均未变，也没多出临时文件。
- 机制上有四重保证：`oskm-cli.pyz` 内无任何网络代码（唯一的 `urllib` 是 `urllib.parse.quote`），CLI help 自称“独立产物，不下载数据”；缺失 `--db` 报 `exit=3` 并明说“CLI 不会为任意缺失路径自动下载”；`bootstrap.py` 已删除查询透传（`arch` 报未知命令 `exit=2`），所以不存在“查询前顺手刷新”的挂载点。
- 过期时的正确动作是**显式** `python3 <skill>/bootstrap.py --runtime-root <runtime> refresh`：实测在 `scratch/runtime-copy` 上下载 `INTERNAL_CI 20261117`，状态 `date` 由 `20261116` 变 `20261117`；紧接着再跑一次只打印“运行时已是最新，无需刷新”。刷新失败（死端点，`exit=1`）时旧库原样保留、查询照常可用。
- 没有 `.oskm-runtime.json` 的自管库：`needs_refresh()` 直接返回 `False`，`doctor` 报“非托管…`bootstrap.py refresh` 不会碰它”，`refresh` 空转退出且不建状态文件、不改库；`--db unmanaged/knowledge.db` 查询正常。**唯一例外**是用户自己把该目录当 `--runtime-root` 传给 `install` —— 实测会下载、原子替换并写入状态文件，把它变成托管运行时。

**产物与边界**
- 结论、命令与输出片段写在 `answer.md:1`（含推荐流程 `doctor → refresh → cli-path → 查询`）。
- fixtures 未被修改：`runtime/.oskm-runtime.json` 仍是 `date=20261116`，四个文件 sha256 与开始前一致，`unmanaged/` 仍只有 `knowledge.db`；所有 refresh/install 演示都在工作区内的 `scratch/` 副本上做，未访问 `~/.oskm`。下载端点仅被显式 refresh/install 命中 2 次，查询命中 0 次。
- 顺带一提：这份快照 `elf_modules=0`，按 skill 硬约束不能用它回答依赖/影响面问题（已在 `answer.md:175` 记录）。

需要我把 `scratch/` 清掉，或直接在真实 `runtime/` 上跑一次 `refresh` 把它更新到今天吗？stderr:
2026-11-17T07:45:44.362704Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc \\\"cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit && rm -rf scratch && mkdir -p scratch && cp -R runtime scratch/runtime-copy && mkdir -p scratch/unmanaged-copy && cp unmanaged/knowledge.db scratch/unmanaged-copy/knowledge.db && echo \\\\\\\"=== scratch prepared ===\\\\\\\" && find scratch -maxdepth 2 | sort && shasum -a 256 scratch/runtime-copy/knowledge.db scratch/unmanaged-copy/knowledge.db && grep '\\\\\\\"date\\\\\\\"' scratch/runtime-copy/.oskm-runtime.json | head -2\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit` · exit=0 · 571.3s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（2 条）

```json
[
  {
    "seq": 2,
    "ts": "2026-11-17T15:46:19.379+08:00",
    "method": "GET",
    "path": "/internal/20261117",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 3,
    "ts": "2026-11-17T15:47:59.301+08:00",
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

## 被测前状态

- 托管运行时 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit/runtime`：`date=20261116`（今天 20261117，已过期）
- 自管库 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit/unmanaged/knowledge.db`：sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44
- 自管库没有 `.oskm-runtime.json`

## 断言结果

自动断言 6/6 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 工具的请求都是"按日期取归档"（没有凭空的 URL，也没有单独下 CLI） | auto | Pass | [{"method": "GET", "path": "/internal/20261117"}, {"method": "GET", "path": "/internal/20261117"}] |
| 2 | 自管库保持原样：没有状态文件、内容未被改写 | auto | Pass | 状态文件存在=False；sha 未变=True |
| 3 | 托管运行时仍然可用（没有被查询搞坏） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e07-refresh-is-explicit/runtime/knowledge.db |
| 4 | 回答说明直接查询不会触发下载 | auto | Pass | 相关表述见转录的 agent 最终回答 |
| 5 | 回答给出显式更新入口 refresh | auto | Pass | agent 回答中出现 refresh |
| 6 | 自管库（无状态文件）是否被正确说明为不刷新/不覆盖 | manual | 人工 | **直接回答** - 只跑查询**不会下载**：`arch overview` / `ask get_scan_info` 在 `date=20261116`（今天 `20261117`）的过期运行时上 0.096s 返回，把 `OSKM_DOWNLOAD_ENDPOINT` 换成死地址 `http://127.0.0.1:1/dead` 结果完全一样；查询前后 `runtime/` 三个文件的 
… [输出截断，完整内容见工作区] …
time> refresh`：实测在 `scratch/runtime-copy` 上下载 `INTERNAL_CI 20261117`，状态 `date` 由 `20261116` 变 `20261 |
| 7 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
