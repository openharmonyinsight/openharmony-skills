# E7 refresh-is-explicit（scripted 臂）

- 开始时间：2026-11-17T16:18:06+08:00
- 结束时间：2026-11-17T16:18:07+08:00
- 执行臂：`scripted`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit`
- 夹具服务端：http://127.0.0.1:61801
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

## 执行记录

### 1. [夹具准备] 装一个 date=20261116 的托管运行时（已过期）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime install --source INTERNAL_CI --date 20261116
stderr:
==> 下载 INTERNAL_CI 运行时: 20261116
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit` · exit=0 · 0.12s

### 2. ① 端点设为黑洞，直接调 CLI 查询（运行时已过期）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime/oskm-cli.pyz --db /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime/knowledge.db ask get_scan_info
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
    {
      "collector": "args",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "arkts",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "components",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "elf_modules",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "hdi",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "install_modules",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "links",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "native",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "repos",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "sas",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    },
    {
      "collector": "services",
      "status": "complete",
      "schema_version": "4.0.0",
      "record_count": 1
    }
  ],
  "attached_aliases": []
}
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit` · exit=0 · 0.08s

### 3. ② 显式 refresh（不带 --date）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime refresh --source INTERNAL_CI
stderr:
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit` · exit=0 · 0.09s

### 4. ③ 已是最新时再 refresh

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime refresh --source INTERNAL_CI --date 20261117
stderr:
==> 运行时已是最新，无需刷新: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit` · exit=0 · 0.06s

### 5. ④ 对自管库执行 refresh

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/unmanaged refresh --source INTERNAL_CI --date 20261117
stderr:
==> 运行时已是最新，无需刷新: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/unmanaged
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit` · exit=0 · 0.06s

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

## 被测前状态

- 托管运行时 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime`：`date=20261116`（今天 20261117，已过期）
- 自管库 `/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/unmanaged/knowledge.db`：sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44
- 自管库没有 `.oskm-runtime.json`

## 断言结果

自动断言 4/4 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | ① 过期运行时上直接查询不触发任何下载 | auto | Pass | [] |
| 2 | ② 只有显式 refresh 才下载，并把 date 推到今天 | auto | Pass | 工具请求=1；date=20261117 |
| 3 | ③ 已是最新时 refresh 判定无需刷新、不下载 | auto | Pass | 工具请求数=0；stderr===> 运行时已是最新，无需刷新: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e07-refresh-is-explicit/runtime |
| 4 | ④ 自管库不会被刷新、接管或下载 | auto | Pass | 状态文件存在=False；sha 未变=True；工具请求数=0 |

**结论：PASS**
