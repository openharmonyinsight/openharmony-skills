# E8 synthetic-database-smoke（scripted 臂）

- 开始时间：2026-11-17T16:18:07+08:00
- 结束时间：2026-11-17T16:18:08+08:00
- 执行臂：`scripted`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e08-synthetic-database-smoke`
- 夹具服务端：http://127.0.0.1:61804
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

## 用户请求（来自 evals.json）

已解压 skill 并单独构建 oskm-cli.pyz，测试夹具已生成 product=synthetic 的合成 knowledge.db。请用 bootstrap.py cli-path 定位 CLI，再直接调用 CLI 查询 scan 信息。

## 期望结果（来自 evals.json）

cli-path 找到测试提供的 pyz；直接调用 oskm-cli.pyz --db < synthetic db > ask get_scan_info 返回 product=synthetic。该步骤只验证两个产物能组合运行，不校验真实产品业务数据。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| get_scan_info | `contains` |
| synthetic | `contains` |
| 只验证 skill 与 CLI 的组合链路，不依赖真实数据库业务统计 | `llm_judge` |

## 执行记录

### 1. 用 cli-path 定位 CLI

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e08-synthetic-database-smoke/plain-tool/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e08-synthetic-database-smoke/runtime cli-path
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/fixtures/oskm-cli.pyz
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e08-synthetic-database-smoke` · exit=0 · 0.09s

### 2. 直接调 CLI 查扫描信息

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/fixtures/oskm-cli.pyz --db /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e08-synthetic-database-smoke/artifacts/synthetic/knowledge.db ask get_scan_info
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

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e08-synthetic-database-smoke` · exit=0 · 0.08s

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

自动断言 4/4 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | cli-path 找到测试提供的 pyz | auto | Pass | stdout=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/fixtures/oskm-cli.pyz |
| 2 | get_scan_info 返回 product=synthetic | auto | Pass | {   "session_id": 1,   "scan_id": 1,   "product": "synthetic",   "cpu_arch": "arm64",   "workspace_root": "/src",   "status": "complete",   "started_at": "2026-11-02T00:00:00Z",   "finished_at": "2026 |
| 3 | 查询是只读的：合成库 sha256 未变 | auto | Pass | sha256=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 |
| 4 | 工具没有联网 | auto | Pass | [] |

**结论：PASS**
