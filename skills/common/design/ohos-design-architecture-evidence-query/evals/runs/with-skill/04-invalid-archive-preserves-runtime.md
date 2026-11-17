# E4 invalid-archive-preserves-runtime（with-skill 臂）

- 开始时间：2026-11-17T15:37:03+08:00
- 结束时间：2026-11-17T15:41:24+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime`
- 夹具服务端：http://127.0.0.1:61286
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0/packages/oskm`

## 用户请求（来自 evals.json）

已有可用运行时。现在使用一个 SQLite 损坏的 knowledge.tar.gz 执行 refresh，测试服务会正常返回该归档。请执行并报告结果。

## 期望结果（来自 evals.json）

refresh 以非零状态失败并报告归档校验错误；已有 knowledge.db、oskm-cli.pyz、两套 SDK 和状态文件保持不变，不得留下半装运行时。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| 失败 | `contains` |
| 已有运行时保持不变 | `contains` |
| 失败后不得替换任何旧产物或留下半装运行时 | `llm_judge` |

## Agent 执行审计

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：261.1 s
- 事件计数：`{"thread.started": 1, "item.completed": 49, "item:error": 1, "turn.started": 1, "item:reasoning": 15, "item:agent_message": 11, "item.started": 22, "item:command_execution": 44, "turn.completed": 1}`
- 读到 skill 文档：是（13 处）
- 执行的命令数：22
- token 用量：`{"input_tokens": 343979, "cached_input_tokens": 313088, "output_tokens": 8832, "reasoning_output_tokens": 2310}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && pwd && ls -la && echo "--- runtime ---" && ls -la runtime'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && cat runtime/.oskm-runtime.json && echo "--- interface ---" && ls -la runtime/interface && echo "--- PROMPT ---" && cat PROMPT.md'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; ls -la $SK && echo "--- refs ---" && ls -la $SK/references'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; cat $SK/bootstrap.py; echo "=== oskm_runtime ==="; ls -la $SK/oskm_runtime'
$ /bin/zsh -lc 'SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; grep -n -i -E "refresh|validate-db|corrupt|损坏|排错|回退|OSKM_DOWNLOAD" $SK/references/usage.md | head -80'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '185,215p;228,340p' "'$SK/references/usage.md'
$ /bin/zsh -lc "SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query; sed -n '540,620p' "'$SK/references/usage.md'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY --version && $PY "$SK/bootstrap.py" refresh --help 2>&1 | head -40'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY "$SK/bootstrap.py" doctor --runtime-root "$PWD/runtime"; echo "doctor exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY "$SK/bootstrap.py" --help 2>&1 | head -30 && echo "=== env ===" && env | grep -i -E "''^OSKM|''^CODEX_HOME" | sort'
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime/runtime && echo \"=== find ===\" && find . -type f | sort && echo \"=== sha256 ===\" && find . -type f -print0 | sort -z | xargs -0 shasum -a 256 && echo \"=== sdk dirs ===\" && find interface -type d | sort && echo \"=== state mtime ===\" && stat -f '%N %z %Sm' .oskm-runtime.json knowledge.db oskm-cli.pyz"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime/runtime && find . -type f -print0 | sort -z | xargs -0 shasum -a 256 > /tmp/oskm-pre-sha.txt && wc -l /tmp/oskm-pre-sha.txt && cat /tmp/oskm-pre-sha.txt'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "SOURCE=$OSKM_DOWNLOAD_SOURCE ENDPOINT=$OSKM_DOWNLOAD_ENDPOINT" && $PY "$SK/bootstrap.py" --runtime-root "$PWD/runtime" refresh --source INTERNAL_CI --date 20261118; echo "refresh exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime/runtime && echo "=== find (incl. dirs) ===" && find . | sort && echo "=== sha256 verify ===" && shasum -a 256 -c /tmp/oskm-pre-sha.txt; echo "verify exit=$?" && echo "=== state ===" && cat .oskm-runtime.json && echo "=== stat ===" && stat -f '"'%N %z %Sm' .oskm-runtime.json knowledge.db oskm-cli.pyz && echo \"=== backup/tmp leftovers in workspace ===\" && find /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime -maxdepth 2 -name '*backup*' -o -maxdepth 2 -name '*oskm-tmp*' -o -maxdepth 2 -name '*.tar.gz' | sort"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== doctor ===" && $PY "$SK/bootstrap.py" --runtime-root "$PWD/runtime" doctor; echo "doctor exit=$?"; echo "=== validate-db ===" && $PY "$SK/bootstrap.py" --runtime-root "$PWD/runtime" validate-db "$PWD/runtime/knowledge.db" 2>&1 | tail -20; echo "validate exit=${PIPESTATUS[0]}"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && R="$PWD/runtime" && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && echo "=== cli-path ===" && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && $PY "$SK/bootstrap.py" --runtime-root "$R" cli-path; echo "=== get_scan_info ===" && $PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" ask get_scan_info 2>&1 | head -40; echo "=== arch overview ===" && $PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" arch overview --format table 2>&1 | head -25'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY "$SK/bootstrap.py" download-db --help 2>&1 | head -20 && echo "=== raw HTTP head ===" && curl -sS -D - -o /dev/null "http://127.0.0.1:61286/corrupt/20261118" 2>&1 | head -12'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && R="$PWD/runtime" && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" --format table arch overview 2>&1 | head -30; echo "arch exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && mkdir -p .probe && SK=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/home/.codex/skills/ohos-design-architecture-evidence-query && PY=/opt/homebrew/opt/python@3.12/bin/python3.12 && $PY "$SK/bootstrap.py" download-db --source INTERNAL_CI --date 20261118 --output "$PWD/.probe/corrupt.db"; echo "download-db exit=$?"; ls -la .probe 2>/dev/null; if [ -f .probe/corrupt.db ]; then echo "=== head bytes ==="; xxd .probe/corrupt.db | head -3; echo "=== integrity_check ==="; $PY -c "
import sqlite3,sys
c=sqlite3.connect(sys.argv[1])
try:
    print(c.execute('"'PRAGMA integrity_check').fetchall())
except Exception as e:
    print('EXC:', type(e).__name__, e)
\" .probe/corrupt.db; fi"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && ls -a .probe && rmdir .probe && echo "probe removed" && ls -la && echo "=== final sha verify ===" && cd runtime && shasum -a 256 -c /tmp/oskm-pre-sha.txt; echo "verify exit=$?"'
$ /bin/zsh -lc "cat > /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime/answer.md <<'EOF'
# 结论：损坏归档的 refresh

**直接回答**："'`refresh` 确实动手了（目标日期 20261118 比已装的 20261117 新），HTTP 层面成功拿到归档
（`200 OK`、`Content-Type: application/gzip`、`Content-Length: 85179`），但在**落盘前**的校验环节被拒：
`SQLite integrity_check 未通过: 文件头无效`，进程以**退出码 1** 结束。

**已有运行时原样保留**：5 个文件的 sha256 全部与刷新前一致，`.oskm-runtime.json` 未被改写
（`date` 仍是 `20261117`，mtime 仍是 `15:37:03`），没有残留备份/临时目录；刷新后 `doctor` 退出 0、
`validate-db` 返回 `ok: true`、CLI 查询照常出结果。没有出现"半装"状态。

---

## 环境

- 运行时根：`<workspace>/runtime`（`OSKM_RUNTIME_ROOT` 已指向它；全程未访问 `~/.oskm`）
- `OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`，`OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61286/corrupt`
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`（3.12.16）

## 关键命令

```bash
WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime
SK=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
R="$WS/runtime"

# 0) 刷新前体检 + 记录指纹
$PY "$SK/bootstrap.py" --runtime-root "$R" doctor
( cd "$R" && find . -type f -print0 | sort -z | xargs -0 shasum -a 256 > /tmp/oskm-pre-sha.txt )

# 1) 用损坏归档执行 refresh（本次核心动作）
$PY "$SK/bootstrap.py" --runtime-root "$R" refresh --source INTERNAL_CI --date 20261118

# 2) 核验运行时是否被保全
( cd "$R" && shasum -a 256 -c /tmp/oskm-pre-sha.txt && cat .oskm-runtime.json )
$PY "$SK/bootstrap.py" --runtime-root "$R" doctor
$PY "$SK/bootstrap.py" --runtime-root "$R" validate-db "$R/knowledge.db"
$PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" ask get_scan_info
$PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" --format table arch overview

# 3) 独立复现：服务端确实正常返回，坏的是归档里的 SQLite
curl -sS -D - -o /dev/null "http://127.0.0.1:61286/corrupt/20261118"
$PY "$SK/bootstrap.py" download-db --source INTERNAL_CI --date 20261118 --output "$WS/.probe/corrupt.db"
```

## 关键输出

**refresh（退出码 1）**
```text
==> 下载 INTERNAL_CI 运行时: 20261118
错误: SQLite integrity_check 未通过: 文件头无效
提示: 未检测到可用的源码根本地运行时。若源码根在别处，用 --source-root <path> 指定，或在源码根及其子目录执行 install。
refresh exit=1
```

**服务端确实"正常返回该归档"（不是网络错）**
```text
HTTP/1.1 200 OK
Server: oskm-eval-fixture/1.0 Python/3.12.16
Content-Type: application/gzip
Content-Length: 85179
```

**独立下载也拒收，且不落盘**
```text
错误: SQLite integrity_check 未通过: 文件头无效
download-db exit=1
# .probe 目录为空 → 校验发生在写文件之前
```

**运行时保全核验（刷新后）**
```text
./.oskm-runtime.json: OK
./interface/sdk-js/api/@internal/ohos.evalmarker.d.ts: OK
./interface/sdk_c/evalmarker.h: OK
./knowledge.db: OK                      # f561e39f…fcd1b44，与刷新前一致
./oskm-cli.pyz: OK                      # ad760c16…cd5eb49e，与刷新前一致
verify exit=0

# .oskm-runtime.json 未改写
{"version":3,"source":"INTERNAL_CI","date":"20261117", ...}   # db/sdk/cli 三段仍为 20261117
mtime: .oskm-runtime.json / knowledge.db / oskm-cli.pyz 全部仍是 Nov 17 15:37:03 2026

# 无残留：find 只列出原有 5 个文件，没有 backup/tmp/*.tar.gz
```

**旧运行时仍可用**
```text
doctor exit=0        Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
validate-db          {"path": ".../runtime/knowledge.db", "ok": true}
ask get_scan_info    scan_id=1, product=synthetic, cpu_arch=arm64, status=complete（各采集器 complete）
arch overview        graphics 1 / startup 1（table 格式，exit 0）
```

## 判读

- 失败点在**下载后、安装前**的 DB 完整性校验：`integrity_check` 报 `文件头无效`，说明坏的是
  SQLite 文件本身，不是网络或解压。
- 退出码 **1** = 托管命令失败（下载/校验类），区别于 CLI 侧的 2（参数错）/3（库打不开）/5（工具 error）。
- 事务性回滚生效：旧产物未被替换，状态文件未被更新，日期仍是 20261117。
- 附带提示"未检测到可用的源码根本地运行时"只是本地构建回退探测未命中，不影响上面的结论。
- 后续动作：等 `20261118` 的合格构建就绪（或修好端点配置）后重跑同一条 `refresh` 即可；
  在此之前继续用 20261117 的库查询是安全的，只是要知道数据是 11-17 的快照。
- 未修改 fixtures，未访问 `~/.oskm`；临时探测目录 `.probe` 已删除。
EOF
echo "written"; wc -l /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime/answer.md'
```

### Agent 最终回答

```markdown
跑完了，`refresh` 被校验拦下，运行时完好无损。

**Refresh 结果**
- `bootstrap.py refresh --source INTERNAL_CI --date 20261118` → 退出码 `1`，输出：`==> 下载 INTERNAL_CI 运行时: 20261118` / `错误: SQLite integrity_check 未通过: 文件头无效`。
- 服务端确实正常返回归档，不是网络错：`curl -D -` 得到 `HTTP/1.1 200 OK`、`Content-Type: application/gzip`、`Content-Length: 85179`。
- 独立复现 `download-db --date 20261118` 同样报 `integrity_check 未通过` 且退出 1，`.probe/` 为空 → 校验发生在写盘之前。

**运行时保全核验**
- `runtime` 下 5 个文件 sha256 全部与刷新前一致（`shasum -c` → 全 `OK`，exit 0）；`knowledge.db` 仍是 `f561e39f…`。
- `.oskm-runtime.json` 未被改写：`date` 仍为 `20261117`，三个文件 mtime 仍是 `Nov 17 15:37:03`；`find` 无 backup/tmp/`*.tar.gz` 残留。
- 刷新后仍可用：`doctor` exit 0（`db=✓, sdk=✓, cli=✓`）、`validate-db` 返回 `{"ok": true}`、`ask get_scan_info` 报 `status=complete`、`arch overview` 正常输出（`graphics 1 / startup 1`）。

**判读**
- 失败点在下载后、安装前的 DB 完整性校验，事务回滚生效，不会出现"半装"运行时。退出码 1 属托管命令失败，区别于 CLI 的 2/3/5。
- 附带那句"未检测到可用的源码根本地运行时"只是本地构建回退探测未命中，与本结论无关。
- 下一步：等 `20261118` 合格构建就绪后重跑同一条 `refresh` 即可；期间用 11-17 快照查询是安全的。

结论与全部命令、输出片段已写入 `answer.md`（104 行）。未修改 fixtures，未访问 `~/.oskm`，临时 `.probe` 目录已删除。
```

### Agent 写入的 answer.md

```markdown
# 结论：损坏归档的 refresh

**直接回答**：`refresh` 确实动手了（目标日期 20261118 比已装的 20261117 新），HTTP 层面成功拿到归档
（`200 OK`、`Content-Type: application/gzip`、`Content-Length: 85179`），但在**落盘前**的校验环节被拒：
`SQLite integrity_check 未通过: 文件头无效`，进程以**退出码 1** 结束。

**已有运行时原样保留**：5 个文件的 sha256 全部与刷新前一致，`.oskm-runtime.json` 未被改写
（`date` 仍是 `20261117`，mtime 仍是 `15:37:03`），没有残留备份/临时目录；刷新后 `doctor` 退出 0、
`validate-db` 返回 `ok: true`、CLI 查询照常出结果。没有出现"半装"状态。

---

## 环境

- 运行时根：`<workspace>/runtime`（`OSKM_RUNTIME_ROOT` 已指向它；全程未访问 `~/.oskm`）
- `OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`，`OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61286/corrupt`
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`（3.12.16）

## 关键命令

```bash
WS=/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime
SK=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
PY=/opt/homebrew/opt/python@3.12/bin/python3.12
R="$WS/runtime"

# 0) 刷新前体检 + 记录指纹
$PY "$SK/bootstrap.py" --runtime-root "$R" doctor
( cd "$R" && find . -type f -print0 | sort -z | xargs -0 shasum -a 256 > /tmp/oskm-pre-sha.txt )

# 1) 用损坏归档执行 refresh（本次核心动作）
$PY "$SK/bootstrap.py" --runtime-root "$R" refresh --source INTERNAL_CI --date 20261118

# 2) 核验运行时是否被保全
( cd "$R" && shasum -a 256 -c /tmp/oskm-pre-sha.txt && cat .oskm-runtime.json )
$PY "$SK/bootstrap.py" --runtime-root "$R" doctor
$PY "$SK/bootstrap.py" --runtime-root "$R" validate-db "$R/knowledge.db"
$PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" ask get_scan_info
$PY "$R/oskm-cli.pyz" --db "$R/knowledge.db" --format table arch overview

# 3) 独立复现：服务端确实正常返回，坏的是归档里的 SQLite
curl -sS -D - -o /dev/null "http://127.0.0.1:61286/corrupt/20261118"
$PY "$SK/bootstrap.py" download-db --source INTERNAL_CI --date 20261118 --output "$WS/.probe/corrupt.db"
```

## 关键输出

**refresh（退出码 1）**
```text
==> 下载 INTERNAL_CI 运行时: 20261118
错误: SQLite integrity_check 未通过: 文件头无效
提示: 未检测到可用的源码根本地运行时。若源码根在别处，用 --source-root <path> 指定，或在源码根及其子目录执行 install。
refresh exit=1
```

**服务端确实"正常返回该归档"（不是网络错）**
```text
HTTP/1.1 200 OK
Server: oskm-eval-fixture/1.0 Python/3.12.16
Content-Type: application/gzip
Content-Length: 85179
```

**独立下载也拒收，且不落盘**
```text
错误: SQLite integrity_check 未通过: 文件头无效
download-db exit=1
# .probe 目录为空 → 校验发生在写文件之前
```

**运行时保全核验（刷新后）**
```text
./.oskm-runtime.json: OK
./interface/sdk-js/api/@internal/ohos.evalmarker.d.ts: OK
./interface/sdk_c/evalmarker.h: OK
./knowledge.db: OK                      # f561e39f…fcd1b44，与刷新前一致
./oskm-cli.pyz: OK                      # ad760c16…cd5eb49e，与刷新前一致
verify exit=0

# .oskm-runtime.json 未改写
{"version":3,"source":"INTERNAL_CI","date":"20261117", ...}   # db/sdk/cli 三段仍为 20261117
mtime: .oskm-runtime.json / knowledge.db / oskm-cli.pyz 全部仍是 Nov 17 15:37:03 2026

# 无残留：find 只列出原有 5 个文件，没有 backup/tmp/*.tar.gz
```

**旧运行时仍可用**
```text
doctor exit=0        Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
validate-db          {"path": ".../runtime/knowledge.db", "ok": true}
ask get_scan_info    scan_id=1, product=synthetic, cpu_arch=arm64, status=complete（各采集器 complete）
arch overview        graphics 1 / startup 1（table 格式，exit 0）
```

## 判读

- 失败点在**下载后、安装前**的 DB 完整性校验：`integrity_check` 报 `文件头无效`，说明坏的是
  SQLite 文件本身，不是网络或解压。
- 退出码 **1** = 托管命令失败（下载/校验类），区别于 CLI 侧的 2（参数错）/3（库打不开）/5（工具 error）。
- 事务性回滚生效：旧产物未被替换，状态文件未被更新，日期仍是 20261117。
- 附带提示"未检测到可用的源码根本地运行时"只是本地构建回退探测未命中，不影响上面的结论。
- 后续动作：等 `20261118` 的合格构建就绪（或修好端点配置）后重跑同一条 `refresh` 即可；
  在此之前继续用 20261117 的库查询是安全的，只是要知道数据是 11-17 的快照。
- 未修改 fixtures，未访问 `~/.oskm`；临时探测目录 `.probe` 已删除。
```

## 执行记录

### 1. [夹具准备] 先装一个可用运行时

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime/runtime install --source INTERNAL_CI --date 20261117
stderr:
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime` · exit=0 · 0.14s

### 2. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
跑完了，`refresh` 被校验拦下，运行时完好无损。

**Refresh 结果**
- `bootstrap.py refresh --source INTERNAL_CI --date 20261118` → 退出码 `1`，输出：`==> 下载 INTERNAL_CI 运行时: 20261118` / `错误: SQLite integrity_check 未通过: 文件头无效`。
- 服务端确实正常返回归档，不是网络错：`curl -D -` 得到 `HTTP/1.1 200 OK`、`Content-Type: application/gzip`、`Content-Length: 85179`。
- 独立复现 `download-db --date 20261118` 同样报 `integrity_check 未通过` 且退出 1，`.probe/` 为空 → 校验发生在写盘之前。

**运行时保全核验**
- `runtime` 下 5 个文件 sha256 全部与刷新前一致（`shasum -c` → 全 `OK`，exit 0）；`knowledge.db` 仍是 `f561e39f…`。
- `.oskm-runtime.json` 未被改写：`date` 仍为 `20261117`，三个文件 mtime 仍是 `Nov 17 15:37:03`；`find` 无 backup/tmp/`*.tar.gz` 残留。
- 刷新后仍可用：`doctor` exit 0（`db=✓, sdk=✓, cli=✓`）、`validate-db` 返回 `{"ok": true}`、`ask get_scan_info` 报 `status=complete`、`arch overview` 正常输出（`graphics 1 / startup 1`）。

**判读**
- 失败点在下载后、安装前的 DB 完整性校验，事务回滚生效，不会出现"半装"运行时。退出码 1 属托管命令失败，区别于 CLI 的 2/3/5。
- 附带那句"未检测到可用的源码根本地运行时"只是本地构建回退探测未命中，与本结论无关。
- 下一步：等 `20261118` 合格构建就绪后重跑同一条 `refresh` 即可；期间用 11-17 快照查询是安全的。

结论与全部命令、输出片段已写入 `answer.md`（104 行）。未修改 fixtures，未访问 `~/.oskm`，临时 `.probe` 目录已删除。stderr:
2026-11-17T07:39:58.573460Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime && rm -rf .probe && ls -la && echo \\\"=== final sha verify ===\\\" && cd runtime && shasum -a 256 -c /tmp/oskm-pre-sha.txt; echo \\\"verify exit=$?\\\"'` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime` · exit=0 · 261.1s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（2 条）

```json
[
  {
    "seq": 2,
    "ts": "2026-11-17T15:38:41.762+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 4,
    "ts": "2026-11-17T15:39:45.304+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  }
]
```

### agent 自己的探测请求（1 条）

```json
[
  {
    "seq": 3,
    "ts": "2026-11-17T15:39:28.732+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  }
]
```

## 被测前状态

```json
{
  ".oskm-runtime.json": "e69a21dfb000608193046e8bb01e187e8e8adb16ea8ee55c02aaf2d47d7cf9bd",
  "interface/sdk-js/api/@internal/ohos.evalmarker.d.ts": "8c8c597c1d563cfb53ffb804aafad71adf4145e9b12c048dacceb5bd9cb8d7df",
  "interface/sdk_c/evalmarker.h": "49673a32794f18d5991a5dd76a7719e92119a25906aa30ee34c9a5a8aac89d2d",
  "knowledge.db": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44",
  "oskm-cli.pyz": "ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e"
}
```

## 断言结果

自动断言 5/5 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 是否如实报告 refresh 失败（而不是宣称成功） | manual | 人工 | 跑完了，`refresh` 被校验拦下，运行时完好无损。  **Refresh 结果** - `bootstrap.py refresh --source INTERNAL_CI --date 20261118` → 退出码 `1`，输出：`==> 下载 INTERNAL_CI 运行时: 20261118` / `错误: SQLite integrity_check 未通过: 文件头无效`。 - 
… [输出截断，完整内容见工作区] …
`f561e39f…`。 - `.oskm-runtime.json` 未被改写：`date` 仍为 `20261117`，三个文件 mtime 仍是 `Nov 17 15:37:03`；`find` |
| 2 | 已有运行时逐文件保持不变（DB / CLI / 两套 SDK / 状态文件） | auto | Pass | 变化: 无；sha 变化: 无 |
| 3 | 旧库仍然可打开且 scans 可读 | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-0cuwbrkg/with-skill/e04-invalid-archive-preserves-runtime/runtime/knowledge.db |
| 4 | 没有留下半装运行时（无安装/备份临时目录） | auto | Pass | leftovers=[] |
| 5 | 被测阶段工具的请求都指向损坏归档端点（没有转去别处凑数据） | auto | Pass | 请求数=2；[{"method": "GET", "path": "/corrupt/20261118"}, {"method": "GET", "path": "/corrupt/20261118"}] |
| 6 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
