# E4 invalid-archive-preserves-runtime（with-skill 臂）

- 开始时间：2026-11-17T16:21:41+08:00
- 结束时间：2026-11-17T16:26:33+08:00
- 执行臂：`with-skill`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime`
- 夹具服务端：http://127.0.0.1:61948
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

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

- 命令：`codex exec --skip-git-repo-check --sandbox danger-full-access -C /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime --json -o agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）
- 退出码：0；耗时：291.9 s
- 事件计数：`{"thread.started": 1, "item.completed": 56, "item:error": 1, "turn.started": 1, "item:reasoning": 19, "item:agent_message": 10, "item.started": 26, "item:command_execution": 52, "turn.completed": 1}`
- 读到 skill 文档：是（15 处）
- 执行的命令数：26
- token 用量：`{"input_tokens": 487837, "cached_input_tokens": 451200, "output_tokens": 9531, "reasoning_output_tokens": 2671}`
- 越界命令（工作区外找文档/实现/宿主进程）：0 条

### Agent 执行过的命令

```console
$ /bin/zsh -lc 'cat /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/SKILL.md'
$ /bin/zsh -lc "pwd; ls -la; echo '---'; ls -la runtime; echo '---'; cat runtime/.oskm-runtime.json"
$ /bin/zsh -lc "cat PROMPT.md; echo '---'; ls -la /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/"
$ /bin/zsh -lc 'ls -R /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/references | head -60'
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/; cat bootstrap.py; echo '=== oskm_runtime ==='; ls -la oskm_runtime"
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/; sed -n '1,200p' references/usage.md"
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/; grep -n "refresh" references/usage.md | head -60'
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/; sed -n '1,140p' oskm_runtime/bootstrap.py"
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query/; sed -n '285,345p' references/usage.md"
$ /bin/zsh -lc 'env | grep -i oskm; echo "exit=$?"; /opt/homebrew/opt/python@3.12/bin/python3.12 --version; ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime/runtime/interface'
$ /bin/zsh -lc 'cd "$OSKM_RUNTIME_ROOT" && shasum -a 256 knowledge.db oskm-cli.pyz && echo '"'--- tree ---' && find . -type f | sort | head -40 && echo '--- counts ---' && find interface/sdk-js -type f | wc -l && find interface/sdk_c -type f | wc -l && echo '--- mtimes ---' && ls -lT knowledge.db oskm-cli.pyz .oskm-runtime.json interface/sdk-js interface/sdk_c"
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py doctor; echo "doctor exit=$?"'
$ /bin/zsh -lc 'cd "$OSKM_RUNTIME_ROOT" && /opt/homebrew/opt/python@3.12/bin/python3.12 oskm-cli.pyz --db knowledge.db ask get_scan_info 2>&1 | head -40; echo "cli exit=$?"'
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime && mkdir -p probe && curl -sS -D probe/headers.txt -o probe/knowledge.tar.gz "$OSKM_DOWNLOAD_ENDPOINT" ; echo "curl exit=$?"; echo '"'--- headers ---'; cat probe/headers.txt; echo '--- file ---'; ls -l probe; file probe/knowledge.tar.gz; tar -tzf probe/knowledge.tar.gz | head -20"
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && grep -n \"INTERNAL_CI\\|def .*url\\|urljoin\\|POST\\|Request(\" oskm_runtime/db_download.py | head -40"
$ /bin/zsh -lc "cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && sed -n '100,235p' oskm_runtime/db_download.py"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime && curl -sS -D probe/headers.txt -o probe/knowledge.tar.gz "$OSKM_DOWNLOAD_ENDPOINT/20261118"; echo "curl exit=$?"; echo '"'--- headers ---'; cat probe/headers.txt; echo '--- archive ---'; ls -l probe/knowledge.tar.gz; file probe/knowledge.tar.gz; tar -tzf probe/knowledge.tar.gz"
$ /bin/zsh -lc "cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime/probe && mkdir -p extracted && tar -xzf knowledge.tar.gz -C extracted && ls -lR extracted | head -30 && echo '--- head bytes ---' && head -c 32 extracted/knowledge.db | xxd | head -3 && echo '--- python sqlite3 ---' && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import sqlite3
con=sqlite3.connect('extracted/knowledge.db')
try:
    print(con.execute('PRAGMA integrity_check').fetchone())
except Exception as exc:
    print('EXC:', type(exc).__name__, exc)
\""
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && SKILL_DIR=$PWD && /opt/homebrew/opt/python@3.12/bin/python3.12 "$SKILL_DIR/bootstrap.py" refresh --runtime-root "$OSKM_RUNTIME_ROOT" --source INTERNAL_CI --date 20261118 > /tmp/oskm_refresh_out.txt 2> /tmp/oskm_refresh_err.txt; echo "refresh exit=$?"; echo '"'--- stdout ---'; cat /tmp/oskm_refresh_out.txt; echo '--- stderr ---'; cat /tmp/oskm_refresh_err.txt"
$ /bin/zsh -lc 'cd "$OSKM_RUNTIME_ROOT" && echo '"'--- sha256 after ---' && shasum -a 256 knowledge.db oskm-cli.pyz && echo '--- state ---' && cat .oskm-runtime.json && echo '--- full tree (incl. hidden) ---' && find . | sort && echo '--- parent dir ---' && ls -la .. && echo '--- sqlite integrity ---' && /opt/homebrew/opt/python@3.12/bin/python3.12 -c \"
import sqlite3
con=sqlite3.connect('knowledge.db')
print(con.execute('PRAGMA integrity_check').fetchone())
print('scans rows:', con.execute('select count(*) from scans').fetchone())
\""
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py doctor; echo "doctor exit=$?"; echo '"'=== query still works ==='; cd \""'$OSKM_RUNTIME_ROOT" && /opt/homebrew/opt/python@3.12/bin/python3.12 oskm-cli.pyz --db knowledge.db arch overview 2>&1 | head -25; echo "query exit=${PIPESTATUS[0]:-$?}"'
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py validate-db "$OSKM_RUNTIME_ROOT/knowledge.db" 2>&1 | tail -20; echo "validate-db exit=${PIPESTATUS[0]}"'
$ /bin/zsh -lc 'cd /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/home/.codex/skills/ohos-design-architecture-evidence-query && /opt/homebrew/opt/python@3.12/bin/python3.12 bootstrap.py refresh --date 20261118; echo "second refresh exit=$?"; echo '"'--- runtime fingerprint after 2nd attempt ---'; cd \""'$OSKM_RUNTIME_ROOT" && shasum -a 256 knowledge.db oskm-cli.pyz && /opt/homebrew/opt/python@3.12/bin/python3.12 -c "
import json,pathlib
s=json.loads(pathlib.Path('"'.oskm-runtime.json').read_text())
print('state date:', s['date'], '| db.date:', s['db']['date'], '| updated_at:', s['updated_at'])
\" && find . | sort | wc -l && ls -a | grep -i 'bak\\|backup\\|tmp\\|oskm-refresh' || echo 'no backup/tmp residue'"
$ /bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime && shasum -a 256 probe/knowledge.tar.gz && ls -la probe'
$ /bin/zsh -lc "cat > /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime/answer.md <<'EOF'
# refresh 遇 SQLite 损坏归档：结论与实测

## 直接回答

- **测试服务正常返回了归档**："'`GET http://127.0.0.1:61948/corrupt/20261118` → `HTTP/1.1 200 OK`、
  `Content-Type: application/gzip`、`Content-Length: 86182`，是一个结构合法的 tar.gz
  （含 `knowledge.db`、`oskm-cli.pyz`、`interface/sdk-js`、`interface/sdk_c`）。
  坏的是里面的 `knowledge.db`：文件头是 `THIS-IS-NOT-SQLITE…`，`sqlite3` 打开报
  `DatabaseError: file is not a database`。
  （注意：`INTERNAL_CI` 的真实下载 URL 是 `$OSKM_DOWNLOAD_ENDPOINT/<date>`；直接 GET
  裸端点 `/corrupt` 会拿到 `404` + JSON，这不是故障，是路径没拼日期。）
- **refresh 被这份归档挡住，退出码 1，且已有运行时原样保留**：
  报错 `SQLite integrity_check 未通过: 文件头无效`。刷新后 `knowledge.db` 与
  `oskm-cli.pyz` 的 sha256 与刷新前**逐字节相同**，`.oskm-runtime.json` 仍是
  `date 20261117`（`updated_at` 未变），两套 SDK 文件仍在，运行时根目录下**没有**残留
  备份/临时目录（`_install_artifacts` 的“先备份、失败逆序还原”生效，坏库没有落盘）。
- **旧运行时依旧可用**：`doctor` 退出 0（`db=✓, sdk=✓, cli=✓`，库可打开），
  `validate-db` 返回 `{"ok": true}`，`arch overview` / `ask get_scan_info` 正常出结果。
- **失败是确定性的**：连跑两次 refresh，两次都是同一条错误 + 退出码 1，指纹不变。
- 结论一句话：**归档能正常下载，但校验（文件头 + integrity_check）判定为坏库，refresh
  以退出码 1 失败并回滚，已装的 20261117 运行时完好可用，没有被半装状态污染。**

## 环境与解释器

```
OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61948/corrupt
OSKM_RUNTIME_ROOT=…/e04-invalid-archive-preserves-runtime/runtime
PY=/opt/homebrew/opt/python@3.12/bin/python3.12   # Python 3.12.16
SKILL=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
```

## 关键命令与输出

### 1. 刷新前基线（doctor + 指纹 + 一次真实查询）

```bash
$PY $SKILL/bootstrap.py doctor
shasum -a 256 "$OSKM_RUNTIME_ROOT"/{knowledge.db,oskm-cli.pyz}
$PY "$OSKM_RUNTIME_ROOT"/oskm-cli.pyz --db "$OSKM_RUNTIME_ROOT"/knowledge.db ask get_scan_info
```

```
Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
doctor exit=0

f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  knowledge.db
3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5  oskm-cli.pyz

{"session_id":1,"scan_id":1,"product":"synthetic","cpu_arch":"arm64","status":"complete", …}
```

### 2. 确认测试服务与归档本身（curl + tar + sqlite3）

```bash
curl -sS -D probe/headers.txt -o probe/knowledge.tar.gz "$OSKM_DOWNLOAD_ENDPOINT/20261118"
tar -xzf probe/knowledge.tar.gz -C probe/extracted
head -c 32 probe/extracted/knowledge.db | xxd
$PY -c "import sqlite3; sqlite3.connect('"'probe/extracted/knowledge.db').execute('PRAGMA integrity_check')\"
"'```

```
HTTP/1.1 200 OK
Server: oskm-eval-fixture/1.0 Python/3.12.16
Content-Type: application/gzip
Content-Length: 86182

probe/knowledge.tar.gz: gzip compressed data, was "knowledge-corrupt.tar", original size 102400
归档内容: ./ knowledge.db oskm-cli.pyz interface/sdk-js/api/@internal/ohos.evalmarker.d.ts interface/sdk_c/evalmarker.h
sha256(归档) = 89eb9603626e387b06564a8c30d158bc83f799936a68c27f1db1f4aef942b26d

00000000: 5448 4953 2d49 532d 4e4f 542d 5351 4c49  THIS-IS-NOT-SQLI
00000010: 5445 3757 e199 c9e2 a502 a528 84e3 1adf  TE7W.......(....
EXC: DatabaseError file is not a database
```

### 3. 执行 refresh（目标日期 20261118）

```bash
$PY $SKILL/bootstrap.py refresh --runtime-root "$OSKM_RUNTIME_ROOT" '"\\
    --source INTERNAL_CI --date 20261118
echo \"refresh exit="'$?"
```

```
==> 下载 INTERNAL_CI 运行时: 20261118
错误: SQLite integrity_check 未通过: 文件头无效
提示: 未检测到可用的源码根本地运行时。若源码根在别处，用 --source-root <path> 指定，或在源码根及其子目录执行 install。
refresh exit=1
```

（第二次不带 `--source`/`--runtime-root`，靠环境变量跑，输出与退出码完全一致：`second refresh exit=1`。）

### 4. 刷新后复核运行时是否被保住

```bash
shasum -a 256 "$OSKM_RUNTIME_ROOT"/{knowledge.db,oskm-cli.pyz}
cat "$OSKM_RUNTIME_ROOT/.oskm-runtime.json"
find "$OSKM_RUNTIME_ROOT" | sort
$PY -c "import sqlite3; print(sqlite3.connect('"'"'$OSKM_RUNTIME_ROOT/knowledge.db'"').execute('PRAGMA integrity_check').fetchone())\"
"'$PY $SKILL/bootstrap.py doctor
$PY $SKILL/bootstrap.py validate-db "$OSKM_RUNTIME_ROOT/knowledge.db"
$PY "$OSKM_RUNTIME_ROOT"/oskm-cli.pyz --db "$OSKM_RUNTIME_ROOT"/knowledge.db arch overview
```

```
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  knowledge.db   # 与基线一致
3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5  oskm-cli.pyz   # 与基线一致

"date": "20261117", "updated_at": "2026-11-17T16:21:41+08:00"   # 未被改写
运行时目录条目数 11（与基线相同）：.oskm-runtime.json / knowledge.db / oskm-cli.pyz /
  interface/sdk-js/api/@internal/ohos.evalmarker.d.ts / interface/sdk_c/evalmarker.h
无 bak / backup / tmp / .oskm-refresh-* 残留

('"'ok',)                        # PRAGMA integrity_check
scans rows: (1,)
doctor exit=0                  # db=✓, sdk=✓, cli=✓，库可打开
{\"path\": \"…/runtime/knowledge.db\", \"ok\": true}   # validate-db 全量 schema 契约通过
arch overview → {\"product\":\"synthetic\",\"scan_id\":1,\"subsystems\":2, …}  # 查询仍可用，exit=0
"'```

## 判读

- 这与 `references/usage.md` 写明的契约一致：**当天构建未就绪、网络失败或新归档校验失败时，
  `refresh`/`install` 以退出码 1 报错，而已有运行时原样保留**——校验发生在落盘之前，
  坏 `knowledge.db` 从未替换旧库，所以不会出现“半装运行时给出看起来合理的空结果”那种更坏的状态。
- 校验点是 DB 侧的 `verify_sqlite`（文件头 + `PRAGMA integrity_check`）。本例连文件头都不是
  `SQLite format 3`，所以在最早的检查就被拒。
- 状态文件日期仍为 20261117，意味着运行时**依旧被判定为过期**；端点修好（或换到有
  20261118 有效构建的日期）后重跑同一条 `refresh` 即可，无需清理任何残留。
- 附带观察（非缺陷）：`OSKM_DOWNLOAD_ENDPOINT` 必须写成归档前缀，`INTERNAL_CI` 会自己拼
  `/<date>`；裸端点直接 GET 返回 404 + JSON，容易被误读成“服务挂了”。

## 本次产生的文件

- `answer.md`（本文）
- `probe/`：本次为验证测试服务而下载的归档与解包副本（`knowledge.tar.gz`、`headers.txt`、
  `extracted/`，其中 `extracted/knowledge.db` 是**故意损坏**的样本，不是可用库）。
  沙箱策略禁止 `rm`，未能自动清理，可由使用者手动删除；运行时目录 `runtime/` 未被写入任何新文件。
EOF
echo written; wc -l /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime/answer.md'
$ /bin/zsh -lc 'ls -la "$HOME/.oskm" 2>&1 | head -3; echo "---"; ls -la /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime/runtime'
```

### Agent 最终回答

```markdown
**结果**
- 测试服务正常：`GET $OSKM_DOWNLOAD_ENDPOINT/20261118` → `200 OK`、`application/gzip`、86182 字节，是结构合法的 tar.gz（`INTERNAL_CI` 自己拼 `/<date>`；裸端点 `/corrupt` 直接 GET 是 `404`+JSON，非故障）。
- 坏在库上：归档内 `knowledge.db` 头部是 `THIS-IS-NOT-SQLITE…`，`sqlite3` 报 `DatabaseError: file is not a database`。
- `refresh --date 20261118` 被挡住：`错误: SQLite integrity_check 未通过: 文件头无效`，**退出码 1**；连跑两次结果一致。
- 已有运行时**原样保留**：`knowledge.db` / `oskm-cli.pyz` 的 sha256 与刷新前逐字节相同（`f561e39f…` / `3e78cf73…`），`.oskm-runtime.json` 仍是 `date 20261117`、`updated_at` 未变，目录条目数不变，无 `bak`/`tmp`/`.oskm-refresh-*` 残留——坏库从未落盘。
- 旧运行时仍可用：`doctor` exit 0（`db=✓, sdk=✓, cli=✓`）、`validate-db` → `{"ok": true}`、`PRAGMA integrity_check` → `('ok',)`、`arch overview` 与 `ask get_scan_info` 正常出结果。

**产物**
- 结论与完整命令/输出片段写在 `answer.md`（工作区根目录）。
- 验证服务的下载样本留在 `probe/`（含故意损坏的 `probe/extracted/knowledge.db`）；沙箱禁止 `rm`，未能自动清理，可手动删除。`runtime/` 未新增任何文件，`~/.oskm` 全程未创建、未访问。

**下一步建议**
- 状态文件日期仍是 20261117，运行时照旧判为过期；端点修好后重跑同一条 `refresh --date 20261118` 即可，无需清理残留。
```

### Agent 写入的 answer.md

```markdown
# refresh 遇 SQLite 损坏归档：结论与实测

## 直接回答

- **测试服务正常返回了归档**：`GET http://127.0.0.1:61948/corrupt/20261118` → `HTTP/1.1 200 OK`、
  `Content-Type: application/gzip`、`Content-Length: 86182`，是一个结构合法的 tar.gz
  （含 `knowledge.db`、`oskm-cli.pyz`、`interface/sdk-js`、`interface/sdk_c`）。
  坏的是里面的 `knowledge.db`：文件头是 `THIS-IS-NOT-SQLITE…`，`sqlite3` 打开报
  `DatabaseError: file is not a database`。
  （注意：`INTERNAL_CI` 的真实下载 URL 是 `$OSKM_DOWNLOAD_ENDPOINT/<date>`；直接 GET
  裸端点 `/corrupt` 会拿到 `404` + JSON，这不是故障，是路径没拼日期。）
- **refresh 被这份归档挡住，退出码 1，且已有运行时原样保留**：
  报错 `SQLite integrity_check 未通过: 文件头无效`。刷新后 `knowledge.db` 与
  `oskm-cli.pyz` 的 sha256 与刷新前**逐字节相同**，`.oskm-runtime.json` 仍是
  `date 20261117`（`updated_at` 未变），两套 SDK 文件仍在，运行时根目录下**没有**残留
  备份/临时目录（`_install_artifacts` 的“先备份、失败逆序还原”生效，坏库没有落盘）。
- **旧运行时依旧可用**：`doctor` 退出 0（`db=✓, sdk=✓, cli=✓`，库可打开），
  `validate-db` 返回 `{"ok": true}`，`arch overview` / `ask get_scan_info` 正常出结果。
- **失败是确定性的**：连跑两次 refresh，两次都是同一条错误 + 退出码 1，指纹不变。
- 结论一句话：**归档能正常下载，但校验（文件头 + integrity_check）判定为坏库，refresh
  以退出码 1 失败并回滚，已装的 20261117 运行时完好可用，没有被半装状态污染。**

## 环境与解释器

```
OSKM_DOWNLOAD_SOURCE=INTERNAL_CI
OSKM_DOWNLOAD_ENDPOINT=http://127.0.0.1:61948/corrupt
OSKM_RUNTIME_ROOT=…/e04-invalid-archive-preserves-runtime/runtime
PY=/opt/homebrew/opt/python@3.12/bin/python3.12   # Python 3.12.16
SKILL=$CODEX_HOME/skills/ohos-design-architecture-evidence-query
```

## 关键命令与输出

### 1. 刷新前基线（doctor + 指纹 + 一次真实查询）

```bash
$PY $SKILL/bootstrap.py doctor
shasum -a 256 "$OSKM_RUNTIME_ROOT"/{knowledge.db,oskm-cli.pyz}
$PY "$OSKM_RUNTIME_ROOT"/oskm-cli.pyz --db "$OSKM_RUNTIME_ROOT"/knowledge.db ask get_scan_info
```

```
Runtime state: version 3, date 20261117, source INTERNAL_CI, db=✓, sdk=✓, cli=✓
Runtime database: 可打开（廉价检查；完整 schema 契约用 bootstrap.py validate-db）
doctor exit=0

f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  knowledge.db
3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5  oskm-cli.pyz

{"session_id":1,"scan_id":1,"product
… [输出截断，完整内容见工作区] …
            # PRAGMA integrity_check
scans rows: (1,)
doctor exit=0                  # db=✓, sdk=✓, cli=✓，库可打开
{"path": "…/runtime/knowledge.db", "ok": true}   # validate-db 全量 schema 契约通过
arch overview → {"product":"synthetic","scan_id":1,"subsystems":2, …}  # 查询仍可用，exit=0
```

## 判读

- 这与 `references/usage.md` 写明的契约一致：**当天构建未就绪、网络失败或新归档校验失败时，
  `refresh`/`install` 以退出码 1 报错，而已有运行时原样保留**——校验发生在落盘之前，
  坏 `knowledge.db` 从未替换旧库，所以不会出现“半装运行时给出看起来合理的空结果”那种更坏的状态。
- 校验点是 DB 侧的 `verify_sqlite`（文件头 + `PRAGMA integrity_check`）。本例连文件头都不是
  `SQLite format 3`，所以在最早的检查就被拒。
- 状态文件日期仍为 20261117，意味着运行时**依旧被判定为过期**；端点修好（或换到有
  20261118 有效构建的日期）后重跑同一条 `refresh` 即可，无需清理任何残留。
- 附带观察（非缺陷）：`OSKM_DOWNLOAD_ENDPOINT` 必须写成归档前缀，`INTERNAL_CI` 会自己拼
  `/<date>`；裸端点直接 GET 返回 404 + JSON，容易被误读成“服务挂了”。

## 本次产生的文件

- `answer.md`（本文）
- `probe/`：本次为验证测试服务而下载的归档与解包副本（`knowledge.tar.gz`、`headers.txt`、
  `extracted/`，其中 `extracted/knowledge.db` 是**故意损坏**的样本，不是可用库）。
  沙箱策略禁止 `rm`，未能自动清理，可由使用者手动删除；运行时目录 `runtime/` 未被写入任何新文件。
```

## 执行记录

### 1. [夹具准备] 先装一个可用运行时

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime/runtime install --source INTERNAL_CI --date 20261117
stderr:
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime` · exit=0 · 0.13s

### 2. codex exec（agent 臂）

```console
$ /usr/local/bin/codex exec --skip-git-repo-check --sandbox danger-full-access -C … < PROMPT.md
**结果**
- 测试服务正常：`GET $OSKM_DOWNLOAD_ENDPOINT/20261118` → `200 OK`、`application/gzip`、86182 字节，是结构合法的 tar.gz（`INTERNAL_CI` 自己拼 `/<date>`；裸端点 `/corrupt` 直接 GET 是 `404`+JSON，非故障）。
- 坏在库上：归档内 `knowledge.db` 头部是 `THIS-IS-NOT-SQLITE…`，`sqlite3` 报 `DatabaseError: file is not a database`。
- `refresh --date 20261118` 被挡住：`错误: SQLite integrity_check 未通过: 文件头无效`，**退出码 1**；连跑两次结果一致。
- 已有运行时**原样保留**：`knowledge.db` / `oskm-cli.pyz` 的 sha256 与刷新前逐字节相同（`f561e39f…` / `3e78cf73…`），`.oskm-runtime.json` 仍是 `date 20261117`、`updated_at` 未变，目录条目数不变，无 `bak`/`tmp`/`.oskm-refresh-*` 残留——坏库从未落盘。
- 旧运行时仍可用：`doctor` exit 0（`db=✓, sdk=✓, cli=✓`）、`validate-db` → `{"ok": true}`、`PRAGMA integrity_check` → `('ok',)`、`arch overview` 与 `ask get_scan_info` 正常出结果。

**产物**
- 结论与完整命令/输出片段写在 `answer.md`（工作区根目录）。
- 验证服务的下载样本留在 `probe/`（含故意损坏的 `probe/extracted/knowledge.db`）；沙箱禁止 `rm`，未能自动清理，可手动删除。`runtime/` 未新增任何文件，`~/.oskm` 全程未创建、未访问。

**下一步建议**
- 状态文件日期仍是 20261117，运行时照旧判为过期；端点修好后重跑同一条 `refresh --date 20261118` 即可，无需清理残留。stderr:
2026-11-17T08:24:28.669359Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/bin/zsh -lc 'cd /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime && shasum -a 256 probe/knowledge.tar.gz && rm -rf probe && ls -la'` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime` · exit=0 · 291.9s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（2 条）

```json
[
  {
    "seq": 4,
    "ts": "2026-11-17T16:23:42.364+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  },
  {
    "seq": 5,
    "ts": "2026-11-17T16:24:17.041+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/octet-stream",
    "body": null
  }
]
```

### agent 自己的探测请求（2 条）

```json
[
  {
    "seq": 2,
    "ts": "2026-11-17T16:22:51.626+08:00",
    "method": "GET",
    "path": "/corrupt",
    "user_agent": "curl/8.7.1",
    "accept": "*/*",
    "body": null
  },
  {
    "seq": 3,
    "ts": "2026-11-17T16:23:18.968+08:00",
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
  ".oskm-runtime.json": "82727dbf7233a82ea7629b906fb9b936f9fdbaf69602723e3542aa3f4026ba02",
  "interface/sdk-js/api/@internal/ohos.evalmarker.d.ts": "8c8c597c1d563cfb53ffb804aafad71adf4145e9b12c048dacceb5bd9cb8d7df",
  "interface/sdk_c/evalmarker.h": "49673a32794f18d5991a5dd76a7719e92119a25906aa30ee34c9a5a8aac89d2d",
  "knowledge.db": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44",
  "oskm-cli.pyz": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5"
}
```

## 断言结果

自动断言 5/5 通过；人工断言 1 条

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 是否如实报告 refresh 失败（而不是宣称成功） | manual | 人工 | **结果** - 测试服务正常：`GET $OSKM_DOWNLOAD_ENDPOINT/20261118` → `200 OK`、`application/gzip`、86182 字节，是结构合法的 tar.gz（`INTERNAL_CI` 自己拼 `/<date>`；裸端点 `/corrupt` 直接 GET 是 `404`+JSON，非故障）。 - 坏在库上：归档内 `knowledge.d
… [输出截断，完整内容见工作区] …
261117`、`updated_at` 未变，目录条目数不变，无 `bak`/`tmp`/`.oskm-refresh-*` 残留——坏库从未落盘。 - 旧运行时仍可用：`doctor` exit  |
| 2 | 已有运行时逐文件保持不变（DB / CLI / 两套 SDK / 状态文件） | auto | Pass | 变化: 无；sha 变化: 无 |
| 3 | 旧库仍然可打开且 scans 可读 | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-with-skill-roa6ye5j/with-skill/e04-invalid-archive-preserves-runtime/runtime/knowledge.db |
| 4 | 没有留下半装运行时（无安装/备份临时目录） | auto | Pass | leftovers=[] |
| 5 | 被测阶段工具的请求都指向损坏归档端点（没有转去别处凑数据） | auto | Pass | 请求数=2；[{"method": "GET", "path": "/corrupt/20261118"}, {"method": "GET", "path": "/corrupt/20261118"}] |
| 6 | 执行过程未越界（没有去工作区外找文档/实现/评估器） | auto | Pass | 所有命令都落在工作区、夹具与临时 CODEX_HOME 内 |

**结论：PASS**
