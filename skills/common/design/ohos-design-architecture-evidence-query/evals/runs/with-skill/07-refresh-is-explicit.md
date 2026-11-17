# E7 refresh-is-explicit（with-skill 臂）

- 开始时间：2026-11-17T16:26:04+08:00
- 结束时间：2026-11-17T16:33:28+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit`
- 夹具服务端：http://127.0.0.1:62101
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：415.5 s
- 事件计数：`{"thread.started": 1, "item.completed": 62, "item:error": 1, "turn.started": 1, "item:reasoning": 18, "item:agent_message": 17, "item.started": 26, "item:command_execution": 52, "turn.completed": 1}`
- 读到 skill 文档：是（12 处）
- 执行的命令数：26
- token 用量：`{"input_tokens": 555690, "cached_input_tokens": 512256, "output_tokens": 13402, "reasoning_output_tokens": 4135}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && ls -la && echo "--- runtime ---" && ls -la runtime && echo "--- unmanaged ---" && ls -la unmanaged && echo "--- state ---" && cat runtime/.oskm-runtime.json'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query; ls -R $SK | head -60; echo "=== grep refresh ==="; rg -n "refresh|stale|过期|oskm-runtime.json|自动" $SK/references/usage.md | head -60'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && cat PROMPT.md'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '20,70p;220,340p' "'$SK/references/usage.md'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query; wc -l $SK/oskm_runtime/*.py $SK/bootstrap.py; echo "=== state.py ==="; cat $SK/oskm_runtime/state.py'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query; cat $SK/bootstrap.py; echo "=== doctor.py ==="; cat $SK/oskm_runtime/doctor.py'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '1,140p' "'$SK/oskm_runtime/bootstrap.py'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '140,303p' "'$SK/oskm_runtime/bootstrap.py'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY -V && echo "--- baseline digest (managed runtime) ---" && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz unmanaged/knowledge.db && echo "--- mtimes ---" && stat -f '"'%N %Sm' runtime/.oskm-runtime.json runtime/knowledge.db runtime/oskm-cli.pyz unmanaged/knowledge.db && echo \"--- interface tree ---\" && find runtime/interface -maxdepth 2 | head -20"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal && echo "### doctor ###" && $PY "$SK/bootstrap.py" --runtime-root "$PWD/runtime" doctor; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal && echo "### cli-path ###" && $PY "$SK/bootstrap.py" --runtime-root "$PWD/runtime" cli-path && echo "### get_scan_info (managed, stale) ###" && time $PY runtime/oskm-cli.pyz --db runtime/knowledge.db ask get_scan_info --format table; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal && echo "### 1) ask get_scan_info (managed, stale date=20261116) ###" && time $PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table ask get_scan_info; echo "exit=$?"; echo; echo "### 2) arch overview ###" && time $PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview | head -c 1200; echo; echo "exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "### 3) same query with DEAD endpoint (proves query never dials out) ###" && OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/internal $PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table ask get_scan_info; echo "exit=$?"; echo; echo "### digests + state after queries ###" && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz && $PY -c "import json;print('"'state date =',json.load(open('runtime/.oskm-runtime.json'))['date'])\" && stat -f '%N %Sm' runtime/.oskm-runtime.json runtime/knowledge.db"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal && echo "### 4) query the UNMANAGED db (no .oskm-runtime.json) ###" && $PY runtime/oskm-cli.pyz --db unmanaged/knowledge.db --format table ask get_scan_info | head -5; echo "exit=$?"; echo "--- unmanaged dir contents after query (state file must NOT appear) ---"; ls -la unmanaged; shasum -a 256 unmanaged/knowledge.db'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal && echo "### 5) MISSING --db path: does it auto-download? ###" && $PY runtime/oskm-cli.pyz --db "$PWD/does-not-exist/knowledge.db" ask get_scan_info; echo "exit=$?"; ls -la does-not-exist 2>&1 | head -3; echo; echo "### 6) explicit refresh pointed at the UNMANAGED dir ###" && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && $PY "$SK/bootstrap.py" --runtime-root "$PWD/unmanaged" refresh; echo "exit=$?"; echo "--- unmanaged dir after refresh ---"; ls -la unmanaged; shasum -a 256 unmanaged/knowledge.db'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && mkdir -p tmp-refresh-demo && cp -R runtime tmp-refresh-demo/runtime && ls -la tmp-refresh-demo/runtime && shasum -a 256 tmp-refresh-demo/runtime/knowledge.db'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && echo "### 7a) refresh on stale COPY, DEAD endpoint ###" && OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/internal $PY "$SK/bootstrap.py" --runtime-root "$PWD/tmp-refresh-demo/runtime" refresh 2>&1 | tail -6; echo "exit=${pipestatus[1]}"; echo "--- copy preserved? ---"; shasum -a 256 tmp-refresh-demo/runtime/knowledge.db; grep -o '"'\"date\": \"[0-9]*\"' tmp-refresh-demo/runtime/.oskm-runtime.json | head -1; ls tmp-refresh-demo/runtime"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && echo "### 7b) refresh on stale COPY, LIVE endpoint ###" && time OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal $PY "$SK/bootstrap.py" --runtime-root "$PWD/tmp-refresh-demo/runtime" refresh 2>&1 | tail -12; echo "exit=${pipestatus[1]}"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && echo "### copy state after refresh ###" && cat tmp-refresh-demo/runtime/.oskm-runtime.json && echo "### 7c) second refresh (already fresh -> no-op) ###" && OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal $PY "$SK/bootstrap.py" --runtime-root "$PWD/tmp-refresh-demo/runtime" refresh; echo "exit=$?"'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && echo \"### FIXTURE runtime unchanged (still stale, same bytes) ###\" && shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz unmanaged/knowledge.db && grep -o '\"date\": \"[0-9]*\"' runtime/.oskm-runtime.json | head -1 && stat -f '%N %Sm' runtime/.oskm-runtime.json runtime/knowledge.db unmanaged/knowledge.db"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY - <<'"'EOF'
import re, zipfile
names = zipfile.ZipFile('runtime/oskm-cli.pyz').namelist()
hits = []
for n in names:
    if not n.endswith('.py'):
        continue
    data = zipfile.ZipFile('runtime/oskm-cli.pyz').read(n)
    for kw in (b'urllib', b'http.client', b'socket', b'OSKM_DOWNLOAD', b'needs_refresh', b'.oskm-runtime.json'):
        if kw in data:
            hits.append((n, kw.decode()))
print('modules:', len(names))
print('network/state refs:', hits if hits else 'NONE')
EOF"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && rm -r tmp-refresh-demo && echo "scratch copy removed" && ls -la'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY - <<'"'EOF'
import zipfile
z = zipfile.ZipFile('runtime/oskm-cli.pyz')
for n in ('oskm_cli/cli.py', 'oskm_cli/query/arkts/query.py'):
    text = z.read(n).decode('utf-8', 'replace')
    for i, line in enumerate(text.splitlines(), 1):
        if 'urllib' in line or 'OSKM_DOWNLOAD' in line:
            print(f'{n}:{i}: {line.strip()}')
EOF"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && cat > answer.md <<'ANSWER'
# oskm 运行时过期：查询会不会下载？该怎么更新？自管库会怎样？

## 直接回答

1. **不会下载。** 只跑 "'`oskm-cli` 查询时，**任何情况下都不联网**。托管运行时状态文件里
   `date=20261116`（今天 20261117）已过期，查询照样秒回；把端点换成不可达地址
   （`http://127.0.0.1:1/internal`）查询依然成功。`--db` 路径缺失时也不自动下载，
   直接退出码 `3` 报错。刷新早已从查询路径上摘掉（2026-11-12 起 `bootstrap.py`
   只负责装），连 `.oskm-refresh-retry` 退避标记也一并删了——没有任何隐式触发点。
2. **数据过期时的正确动作是显式刷新**：
   `python3 <skill>/bootstrap.py --runtime-root <runtime-root> refresh`
   （`install` 的幂等版：先做廉价检查，**过期才重装**；需要指定历史日期就用
   `install --date YYYYMMDD`）。刷新失败时退出码 `1`，**已有运行时原样保留**。
   `doctor` 只报告日期与就绪状态，同样不下载。
3. **没有 `.oskm-runtime.json` 的库是"自管"输入，永远不会被刷新或覆盖**：
   查询它只需 `--db` 指向该文件；`needs_refresh()` 在没有状态文件时直接返回
   `False`，所以既不联网也不改字节，甚至**显式** `refresh` 指向它也只是打印
   "运行时已是最新，无需刷新"，不会替它创建状态文件。状态文件就是托管标记。

---

## 环境与基线

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12     # Python 3.12.16
export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
export OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal

shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz unmanaged/knowledge.db
# f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  runtime/knowledge.db
# 3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5  runtime/oskm-cli.pyz
# f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  unmanaged/knowledge.db
```

`runtime/.oskm-runtime.json`（version 3，`date=20261116` → 比今天旧 = 过期）：

```json
{ "version": 3, "source": "INTERNAL_CI", "date": "20261116",
  "db": { "date": "20261116", "path": "knowledge.db", "sha256": "f561e39f…" },
  "sdk": { "date": "20261116", "sdk-js": {…}, "sdk_c": {…} },
  "cli": { "path": "oskm-cli.pyz", "sha256": "3e78cf73…" } }
```

## 证据 1：`doctor` 认出过期，但不下载

```bash
$PY "$SK/bootstrap.py" --runtime-root "$PWD/runtime" doctor
```

```text
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Runtime state: version 3, date 20261116, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
exit=0
提示: bootstrap.py 不跑查询。查询直接调 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db …
```

`date 20261116` 就是过期信号；doctor 只读不装，也没有 `.oskm-refresh-retry` 之类标记产生。

## 证据 2：过期运行时上的查询，零网络、零改动

```bash
$PY "$SK/bootstrap.py" --runtime-root "$PWD/runtime" cli-path
# …/e07-refresh-is-explicit/runtime/oskm-cli.pyz

time $PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table ask get_scan_info
$PY runtime/oskm-cli.pyz --db runtime/knowledge.db arch overview
```

```text
collector        status    schema_version  record_count
args             complete  4.0.0           1
components       complete  4.0.0           1
elf_modules      complete  4.0.0           1
…（11 个采集器全 complete）
0.08s user 0.01s system 96% cpu 0.095 total      exit=0

arch overview → {"product":"synthetic","scan_id":1,"subsystems":2,
                 "counts":{"components":2,"elf_modules":0,…}}   exit=0
```

`--format` 是**全局** flag，要写在子命令之前（`--db X --format table ask …`）；写在
`ask` 后面会 `error: unrecognized arguments`，退出码 2。

**把端点换成死地址，同一条查询仍然成功**（证明查询路径根本不发起连接）：

```bash
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/internal '"\\
  "'$PY runtime/oskm-cli.pyz --db runtime/knowledge.db --format table ask get_scan_info
# 输出与上面完全一致，exit=0，耗时 ~0.08s
```

查询后校验，产物一个字节都没变，状态日期仍是旧的：

```text
f561e39f…  runtime/knowledge.db          （未变）
3e78cf73…  runtime/oskm-cli.pyz          （未变）
state date = 20261116                    （未被"顺手刷新"）
```

补充：`oskm-cli.pyz` 里 45 个模块中没有任何下载代码——全文只命中两处字符串，
`oskm_cli/cli.py:97`（一句提示配置 `OSKM_DOWNLOAD_ENDPOINT` 的错误文案）与
`oskm_cli/query/arkts/query.py:6`（`from urllib.parse import quote`，纯字符串转义）。
CLI 没有 `urlopen`、没有 `needs_refresh`、不读 `.oskm-runtime.json`。

## 证据 3：`--db` 缺失也不自动下载（退出码 3）

```bash
$PY runtime/oskm-cli.pyz --db "$PWD/does-not-exist/knowledge.db" ask get_scan_info
```

```text
error: database not found: …/does-not-exist/knowledge.db. 检查 --db 路径；托管运行时请用
… `python3 <skill>/bootstrap.py install --runtime-root ~/.oskm` 安装，再用 --db ~/.oskm/knowledge.db 查询。
CLI 不会为任意缺失路径自动下载。
exit=3
ls: does-not-exist: No such file or directory      # 目录也没被创建
```

## 证据 4：显式 `refresh` 才是更新动作（在副本上演示，夹具未动）

为不修改夹具，把 `runtime` 复制成 `tmp-refresh-demo/runtime` 后在副本上跑，演示完已删除。

**4a 过期 → 死端点：报错但保留旧运行时**

```bash
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:1/internal '"\\
  "'$PY "$SK/bootstrap.py" --runtime-root "$PWD/tmp-refresh-demo/runtime" refresh
```

```text
==> 下载 INTERNAL_CI 运行时: 20261117
错误: 下载失败（网络或代理不可用）: http://127.0.0.1:1/internal/20261117:
      <urlopen error [Errno 61] Connection refused>. 检查网络、DNS、HTTPS_PROXY/HTTP_PROXY/NO_PROXY 和证书配置。
exit=1
副本校验：knowledge.db 摘要仍为 f561e39f…，state date 仍为 20261116，目录内容完整
```

即"过期才下载"，且半装状态不会留下——失败时旧产物原样还原。

**4b 过期 → 活端点：下载并更新到当天**

```bash
OSKM_DOWNLOAD_SOURCE=INTERNAL_CI OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal '"\\
  "'$PY "$SK/bootstrap.py" --runtime-root "$PWD/tmp-refresh-demo/runtime" refresh
```

```text
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: …/tmp-refresh-demo/runtime
exit=0
新 state: "date": "20261117", db.date=20261117, sdk.date=20261117, cli.sha256=3e78cf73…
```

**4c 再刷一次：幂等，不联网**

```text
==> 运行时已是最新，无需刷新: …/tmp-refresh-demo/runtime      exit=0
```

注意托管运行时**只覆盖最新一份**，不建按日期命名的历史目录；要留存某天快照请用
`bootstrap.py download-db --date YYYYMMDD --output PATH`。

## 证据 5：自管库（无 `.oskm-runtime.json`）不被刷新、不被覆盖

```bash
# 查询：只需 --db，工作正常
$PY runtime/oskm-cli.pyz --db unmanaged/knowledge.db --format table ask get_scan_info
# exit=0；查询后 ls -la unmanaged 仍只有 knowledge.db（没有生成 .oskm-runtime.json）
# 摘要仍为 f561e39f…

# 显式把 refresh 指向它，也什么都不做
$PY "$SK/bootstrap.py" --runtime-root "$PWD/unmanaged" refresh
```

```text
==> 运行时已是最新，无需刷新: …/unmanaged      exit=0
unmanaged/ 目录：仍然只有 knowledge.db，mtime 保持 Nov 17 16:18:33，摘要 f561e39f… 未变
```

原因在 `oskm_runtime/state.py:needs_refresh()`：`load_state()` 找不到状态文件就返回
`None`，`needs_refresh()` 随即 `return False`——自管库被当作向后兼容的手工
`artifacts/*/knowledge.db` 输入，**始终不会自动联网**，也不会被 install 事务覆盖。
反过来，想让某个目录变成"托管"，只能对它显式跑一次 `install`（那会写入状态文件）。

## 夹具完整性

演示结束后 `runtime/`、`unmanaged/` 与基线完全一致：

```text
f561e39f…  runtime/knowledge.db      mtime Nov 17 16:26:04
3e78cf73…  runtime/oskm-cli.pyz
f561e39f…  unmanaged/knowledge.db    mtime Nov 17 16:18:33
runtime/.oskm-runtime.json  "date": "20261116"   mtime Nov 17 16:26:04
```

未访问或修改 `~/.oskm`；所有 `--runtime-root` 都指向本工作区路径；临时副本
`tmp-refresh-demo/` 已删除。

## 操作要点速查

| 情况 | 动作 | 会不会联网 |
|---|---|---|
| 只查询（运行时过期） | `python3 <root>/oskm-cli.pyz --db <root>/knowledge.db ask/arch/diff/sql …` | 否 |
| 想更新到当天 | `python3 <skill>/bootstrap.py --runtime-root <root> refresh` | 仅过期时 |
| 想装指定历史日期 | `… bootstrap.py --runtime-root <root> install --date YYYYMMDD` | 是 |
| 想看是否就绪/过期 | `… bootstrap.py --runtime-root <root> doctor` | 否 |
| 只想留存某天 DB | `… bootstrap.py download-db --date D --output PATH` | 是 |
| 自管库（无状态文件） | 直接 `--db <path>` 查询 | 否，且 refresh 也不碰它 |
| `--db` 路径不存在 | 修好路径或先 `install`；CLI 退出码 3 | 否 |

**语义提醒**：过期只影响"数据是哪天的快照"，不影响查询可用性——查询会照常返回
旧快照的结果，所以看到 `date` 不是当天时要么显式 `refresh`，要么在结论里说明
用的是 20261116 的快照。另外 `arch overview` 里 `elf_modules=0` 表示该证据未采集，
不能用它回答依赖/影响面问题。
ANSWER
echo "written:" && wc -l answer.md'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && ls -la && echo \"--- fixture check ---\" && grep -o '\"date\": \"[0-9]*\"' runtime/.oskm-runtime.json | head -1 && ls unmanaged"
```

### Agent 最终回答

```markdown
全部命令都实跑过了，结论写进了 `answer.md`（夹具 `runtime/` 与 `unmanaged/` 一个字节都没动，`state date` 仍是 `20261116`）。

**会不会下载**
- 不会。过期运行时（`date=20261116` vs 今天 `20261117`）上直接查询照常返回，耗时 ~0.08s；把端点换成不可达的 `http://127.0.0.1:1/internal` 同一条查询仍成功，证明查询路径根本不发起连接。
- `--db` 指向不存在的路径也不下载，直接退出码 `3` 并提示先 `install`；目录都不会被创建。
- `oskm-cli.pyz` 的 45 个模块里没有任何下载代码，全文只命中 `oskm_cli/cli.py:97` 的一句提示文案和 `oskm_cli/query/arkts/query.py:6` 的 `urllib.parse.quote`（纯转义）。
- `bootstrap.py doctor` 只报 `Runtime state: version 3, date 20261116, …`，同样不联网。

**正确的更新动作**
- 显式 `python3 <skill>/bootstrap.py --runtime-root <root> refresh`：廉价检查，过期才重装；要指定历史日期用 `install --date YYYYMMDD`。
- 我在副本 `tmp-refresh-demo/runtime` 上实测：死端点 → `==> 下载 INTERNAL_CI 运行时: 20261117` 后退出码 `1`，旧库摘要与 `date=20261116` 原样保留；活端点 → 安装完成，状态变成 `date/db.date/sdk.date = 20261117`；再刷一次输出 `==> 运行时已是最新，无需刷新`。副本已删除。
- 托管运行时只覆盖最新一份，不留按日期的历史目录；要留快照用 `download-db --date D --output PATH`。

**没有 `.oskm-runtime.json` 的自管库**
- 查询只需 `--db unmanaged/knowledge.db`，正常工作，且查询后不会生成状态文件，摘要 `f561e39f…` 不变。
- 显式 `refresh --runtime-root unmanaged` 也只打印 `==> 运行时已是最新，无需刷新`，退出码 `0`，不建状态文件、不覆盖字节（`state.py:needs_refresh()` 无状态文件即 `return False`）。想让它变托管只能对它显式 `install`。

一个易踩点：`--format` 是全局 flag，要写成 `--db X --format table ask get_scan_info`，放在 `ask` 后面会报 `unrecognized arguments`（退出码 2）。另外这个库 `arch overview` 显示 `elf_modules=0`，属于证据未采集，不能用它回答依赖或影响面问题。
```

### Agent 写入的 answer.md

```markdown
# oskm 运行时过期：查询会不会下载？该怎么更新？自管库会怎样？

## 直接回答

1. **不会下载。** 只跑 `oskm-cli` 查询时，**任何情况下都不联网**。托管运行时状态文件里
   `date=20261116`（今天 20261117）已过期，查询照样秒回；把端点换成不可达地址
   （`http://127.0.0.1:1/internal`）查询依然成功。`--db` 路径缺失时也不自动下载，
   直接退出码 `3` 报错。刷新早已从查询路径上摘掉（2026-11-12 起 `bootstrap.py`
   只负责装），连 `.oskm-refresh-retry` 退避标记也一并删了——没有任何隐式触发点。
2. **数据过期时的正确动作是显式刷新**：
   `python3 <skill>/bootstrap.py --runtime-root <runtime-root> refresh`
   （`install` 的幂等版：先做廉价检查，**过期才重装**；需要指定历史日期就用
   `install --date YYYYMMDD`）。刷新失败时退出码 `1`，**已有运行时原样保留**。
   `doctor` 只报告日期与就绪状态，同样不下载。
3. **没有 `.oskm-runtime.json` 的库是"自管"输入，永远不会被刷新或覆盖**：
   查询它只需 `--db` 指向该文件；`needs_refresh()` 在没有状态文件时直接返回
   `False`，所以既不联网也不改字节，甚至**显式** `refresh` 指向它也只是打印
   "运行时已是最新，无需刷新"，不会替它创建状态文件。状态文件就是托管标记。

---

## 环境与基线

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12     # Python 3.12.16
export OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
export OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:62101/internal

shasum -a 256 runtime/knowledge.db runtime/oskm-cli.pyz unmanaged/knowledge.db
# f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  runtime/knowledge.db
# 3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5  runtime/oskm-cli.pyz
# f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  unmanaged/knowledge.db
```

`runtime/.oskm-runtime.json`（version 3，`date=20261116` → 比今天旧 = 过期）：

```json
{ "version": 3, "source": "INTERNAL_CI", "date": "20261116",
  "db": { "date": "20261116", "path": "knowledge.db", "sha256": "f561e39f…" },
  "sdk": { "date": "20261116", "sdk-js": {…}, "sdk_c": {…} },
  "cli": { "path": "oskm-cli.pyz", "sha256": "3e78cf73…" } }
```

## 证据 1：`doctor` 认出过期，但不下载

```bash
$PY "$SK/bootstrap.py" --runtime-root "$PWD/runtime" doctor
```

```text
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=INTERNAL_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: …/runtime/oskm-cli.pyz (installed, oskm-cli 1.0.0)
Runtime state: version 3, date 20261116, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价
… [输出截断，完整内容见工作区] …
edge.db      mtime Nov 17 16:26:04
3e78cf73…  runtime/oskm-cli.pyz
f561e39f…  unmanaged/knowledge.db    mtime Nov 17 16:18:33
runtime/.oskm-runtime.json  "date": "20261116"   mtime Nov 17 16:26:04
```

未访问或修改 `~/.oskm`；所有 `--runtime-root` 都指向本工作区路径；临时副本
`tmp-refresh-demo/` 已删除。

## 操作要点速查

| 情况 | 动作 | 会不会联网 |
|---|---|---|
| 只查询（运行时过期） | `python3 <root>/oskm-cli.pyz --db <root>/knowledge.db ask/arch/diff/sql …` | 否 |
| 想更新到当天 | `python3 <skill>/bootstrap.py --runtime-root <root> refresh` | 仅过期时 |
| 想装指定历史日期 | `… bootstrap.py --runtime-root <root> install --date YYYYMMDD` | 是 |
| 想看是否就绪/过期 | `… bootstrap.py --runtime-root <root> doctor` | 否 |
| 只想留存某天 DB | `… bootstrap.py download-db --date D --output PATH` | 是 |
| 自管库（无状态文件） | 直接 `--db <path>` 查询 | 否，且 refresh 也不碰它 |
| `--db` 路径不存在 | 修好路径或先 `install`；CLI 退出码 3 | 否 |

**语义提醒**：过期只影响"数据是哪天的快照"，不影响查询可用性——查询会照常返回
旧快照的结果，所以看到 `date` 不是当天时要么显式 `refresh`，要么在结论里说明
用的是 20261116 的快照。另外 `arch overview` 里 `elf_modules=0` 表示该证据未采集，
不能用它回答依赖/影响面问题。
```

## 执行记录

### 1. [夹具准备] 装一个 date=20261116 的托管运行时（已过期）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit/runtime install --source INTERNAL_CI --date 20261116
stderr:
==> 下载 INTERNAL_CI 运行时: 20261116
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit` · exit=0 · 0.13s

### 2. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
全部命令都实跑过了，结论写进了 `answer.md`（夹具 `runtime/` 与 `unmanaged/` 一个字节都没动，`state date` 仍是 `20261116`）。

**会不会下载**
- 不会。过期运行时（`date=20261116` vs 今天 `20261117`）上直接查询照常返回，耗时 ~0.08s；把端点换成不可达的 `http://127.0.0.1:1/internal` 同一条查询仍成功，证明查询路径根本不发起连接。
- `--db` 指向不存在的路径也不下载，直接退出码 `3` 并提示先 `install`；目录都不会被创建。
- `oskm-cli.pyz` 的 45 个模块里没有任何下载代码，全文只命中 `oskm_cli/cli.py:97` 的一句提示文案和 `oskm_cli/query/arkts/query.py:6` 的 `urllib.parse.quote`（纯转义）。
- `bootstrap.py doctor` 只报 `Runtime state: version 3, date 20261116, …`，同样不联网。

**正确的更新动作**
- 显式 `python3 <skill>/bootstrap.py --runtime-root <root> refresh`：廉价检查，过期才重装；要指定历史日期用 `install --date YYYYMMDD`。
- 我在副本 `tmp-refresh-demo/runtime` 上实测：死端点 → `==> 下载 INTERNAL_CI 运行时: 20261117` 后退出码 `1`，旧库摘要与 `date=20261116` 原样保留；活端点 → 安装完成，状态变成 `date/db.date/sdk.date = 20261117`；再刷一次输出 `==> 运行时已是最新，无需刷新`。副本已删除。
- 托管运行时只覆盖最新一份，不留按日期的历史目录；要留快照用 `download-db --date D --output PATH`。

**没有 `.oskm-runtime.json` 的自管库**
- 查询只需 `--db unmanaged/knowledge.db`，正常工作，且查询后不会生成状态文件，摘要 `f561e39f…` 不变。
- 显式 `refresh --runtime-root unmanaged` 也只打印 `==> 运行时已是最新，无需刷新`，退出码 `0`，不建状态文件、不覆盖字节（`state.py:needs_refresh()` 无状态文件即 `return False`）。想让它变托管只能对它显式 `install`。

一个易踩点：`--format` 是全局 flag，要写成 `--db X --format table ask get_scan_info`，放在 `ask` 后面会报 `unrecognized arguments`（退出码 2）。另外这个库 `arch overview` 显示 `elf_modules=0`，属于证据未采集，不能用它回答依赖或影响面问题。stderr:
/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && rm -rf tmp-refresh-demo && mkdir -p tmp-refresh-demo &…207 chars truncated…tp://127.0.0.1:1/internal $PY \\\"$SK/bootstrap.py\\\" --runtime-root \\\"$PWD/tmp-refresh-demo/runtime\\\" refresh; echo \\\"exit=$?\\\"; echo \\\"--- copy still intact & still stale ---\\\"; $PY -c \\\"import json;print('\\\"'date =',json.load(open('tmp-refresh-demo/runtime/.oskm-runtime.json'))['date'])\\\\\\\"; shasum -a 256 tmp-refresh-demo/runtime/knowledge.db\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit` · exit=0 · 415.5s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 2,
    "ts": "2026-11-17T16:29:21.954+08:00",
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

- 托管运行时 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit/runtime`：`date=20261116`（今天 20261117，已过期）
- 自管库 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit/unmanaged/knowledge.db`：sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44
- 自管库没有 `.oskm-runtime.json`

## 断言结果

自动断言 6/6 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 工具的请求都是"按日期取归档"（没有凭空的 URL，也没有单独下 CLI） | auto | Pass | [{"method": "GET", "path": "/internal/20261117"}] |
| 2 | 自管库保持原样：没有状态文件、内容未被改写 | auto | Pass | 状态文件存在=False；sha 未变=True |
| 3 | 托管运行时仍然可用（没有被查询搞坏） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e07-refresh-is-explicit/runtime/knowledge.db |
| 4 | 回答说明直接查询不会触发下载 | auto | Pass | 相关表述见转录的 agent 最终回答 |
| 5 | 回答给出显式更新入口 refresh | auto | Pass | agent 回答中出现 refresh |
| 6 | 自管库（无状态文件）是否被正确说明为不刷新/不覆盖 | manual | 人工 | 全部命令都实跑过了，结论写进了 `answer.md`（夹具 `runtime/` 与 `unmanaged/` 一个字节都没动，`state date` 仍是 `20261116`）。  **会不会下载** - 不会。过期运行时（`date=20261116` vs 今天 `20261117`）上直接查询照常返回，耗时 ~0.08s；把端点换成不可达的 `http://127.0.0.1:1/i
… [输出截断，完整内容见工作区] …
网。  **正确的更新动作** - 显式 `python3 <skill>/bootstrap.py --runtime-root <root> refresh`：廉价检查，过期才重装；要指定历史日期 |
| 7 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
