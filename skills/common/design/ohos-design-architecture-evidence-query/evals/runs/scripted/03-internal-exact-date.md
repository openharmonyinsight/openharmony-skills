# E3 internal-exact-date（scripted 臂）

- 开始时间：2026-11-17T16:18:04+08:00
- 结束时间：2026-11-17T16:18:05+08:00
- 执行臂：`scripted`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e03-internal-exact-date`
- 夹具服务端：http://127.0.0.1:61794
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

## 用户请求（来自 evals.json）

使用 INTERNAL_CI 下载 date=20261102 的运行时，OSKM_DOWNLOAD_ENDPOINT 已配置为测试服务。请执行并说明 URL。

## 期望结果（来自 evals.json）

请求 $OSKM_DOWNLOAD_ENDPOINT/20261102，响应文件为 knowledge.tar.gz；指定日期不会退化成 latest 或系统当天。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| $OSKM_DOWNLOAD_ENDPOINT/$date | `contains` |
| knowledge.tar.gz | `contains` |
| 指定日期不会退化成 latest 或系统当天 | `llm_judge` |

## 执行记录

### 1. 按显式日期安装

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e03-internal-exact-date/runtime install --source INTERNAL_CI --date 20261102
stderr:
==> 下载 INTERNAL_CI 运行时: 20261102
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e03-internal-exact-date/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e03-internal-exact-date` · exit=0 · 0.13s

### 2. 状态文件

```console
$ cat /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e03-internal-exact-date/runtime/.oskm-runtime.json
{
  "version": 3,
  "source": "INTERNAL_CI",
  "date": "20261102",
  "updated_at": "2026-11-17T16:18:04+08:00",
  "db": {
    "date": "20261102",
    "path": "knowledge.db",
    "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44"
  },
  "sdk": {
    "date": "20261102",
    "sdk-js": {
      "path": "interface/sdk-js"
    },
    "sdk_c": {
      "path": "interface/sdk_c"
    }
  },
  "cli": {
    "path": "oskm-cli.pyz",
    "sha256": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5"
  }
}
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e03-internal-exact-date` · exit=0 · 0.01s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T16:18:04.638+08:00",
    "method": "GET",
    "path": "/internal/20261102",
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

## 断言结果

自动断言 5/5 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 工具的所有请求都是 GET $OSKM_DOWNLOAD_ENDPOINT/$date | auto | Pass | 请求数=1；[{"method": "GET", "path": "/internal/20261102"}] |
| 2 | URL 是 $OSKM_DOWNLOAD_ENDPOINT/$date | auto | Pass | /internal/20261102 |
| 3 | 没有退化成 latest 或系统当天 | auto | Pass | 当天是 20261117，工具实际请求 ['/internal/20261102'] |
| 4 | 状态文件记录 date=20261102 | auto | Pass | date=20261102 |
| 5 | 归档按 knowledge.tar.gz 落地并装齐四件产物 | auto | Pass | runtime=['.oskm-runtime.json', 'interface', 'knowledge.db', 'oskm-cli.pyz'] |

**结论：PASS**
