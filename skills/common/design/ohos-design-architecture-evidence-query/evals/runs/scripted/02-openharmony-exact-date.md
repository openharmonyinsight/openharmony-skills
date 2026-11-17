# E2 openharmony-exact-date（scripted 臂）

- 开始时间：2026-11-17T16:18:03+08:00
- 结束时间：2026-11-17T16:18:04+08:00
- 执行臂：`scripted`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e02-openharmony-exact-date`
- 夹具服务端：http://127.0.0.1:61791
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

## 用户请求（来自 evals.json）

使用 OPENHARMONY_CI 安装 date=20261102，OSKM_DOWNLOAD_ENDPOINT 已配置为测试服务。请执行安装并说明实际请求语义。

## 期望结果（来自 evals.json）

向端点 POST，component 固定为 dayu600_7885_ai，开始和结束时间都来自同一个显式日期；下载物是 knowledge.tar.gz，不要求用户传 --component，也不使用 latest。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| OPENHARMONY_CI | `contains` |
| component: dayu600_7885_ai | `contains` |
| knowledge.tar.gz | `contains` |
| 一次请求同时表示开始和结束日期，不要求用户单独传两个日期 | `llm_judge` |

## 执行记录

### 1. 按显式日期安装

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e02-openharmony-exact-date/runtime install --source OPENHARMONY_CI --date 20261102
stderr:
==> 下载 OPENHARMONY_CI 运行时: 20261102
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e02-openharmony-exact-date/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e02-openharmony-exact-date` · exit=0 · 0.13s

### 2. install 的参数面（确认没有 --component）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py install --help
usage: bootstrap.py install [-h] [--source {OPENHARMONY_CI,INTERNAL_CI}]
                            [--date DATE] [--source-root SOURCE_ROOT]
                            [--skip-db | --skip-sdk]

安装或刷新托管运行时（DB + 两套 SDK + CLI）

options:
  -h, --help            show this help message and exit
  --source {OPENHARMONY_CI,INTERNAL_CI}
                        下载方式；默认读 OSKM_DOWNLOAD_SOURCE，未配置时为 OPENHARMONY_CI
  --date DATE           YYYYMMDD；缺省取系统当天
  --source-root SOURCE_ROOT
                        OpenHarmony 源码根；指定后只优先使用该源码根的本地构建。不指定时从 cwd 向上探测最近的源码根
  --skip-db
  --skip-sdk
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e02-openharmony-exact-date` · exit=0 · 0.06s

### 3. 状态文件

```console
$ cat /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e02-openharmony-exact-date/runtime/.oskm-runtime.json
{
  "version": 3,
  "source": "OPENHARMONY_CI",
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

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e02-openharmony-exact-date` · exit=0 · 0.01s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（2 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T16:18:04.023+08:00",
    "method": "POST",
    "path": "/openharmony/api/daily_build/build/list/component",
    "user_agent": "Python-urllib/3.12",
    "accept": "application/json",
    "body": {
      "projectName": "openharmony",
      "branch": "master",
      "pageNum": 1,
      "pageSize": 10,
      "deviceLevel": "",
      "component": "dayu600_7885_ai",
      "type": 1,
      "startTime": "2026110200000000",
      "endTime": "20261102235959",
      "sortType": "",
      "sortField": "",
      "hardwareBoard": "",
      "buildStatus": "success",
      "buildFailReason": "",
      "withDomain": 1
    }
  },
  {
    "seq": 2,
    "ts": "2026-11-17T16:18:04.024+08:00",
    "method": "GET",
    "path": "/openharmony/obs/20261102/knowledge.tar.gz",
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

自动断言 9/9 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 工具的请求只落在"构建列表 POST + obs 归档 GET"两条路径上 | auto | Pass | POST=1 GET=1；[{"method": "POST", "path": "/openharmony/api/daily_build/build/list/component"}, {"method": "GET", "path": "/openharmony/obs/20261102/knowledge.tar.gz"}] |
| 2 | component 固定为 dayu600_7885_ai（不需要用户传） | auto | Pass | component=dayu600_7885_ai |
| 3 | 起止时间都来自同一个显式日期 | auto | Pass | startTime=2026110200000000 endTime=20261102235959 |
| 4 | 只取构建成功的记录 | auto | Pass | buildStatus=success |
| 5 | 下载物是 knowledge.tar.gz | auto | Pass | /openharmony/obs/20261102/knowledge.tar.gz |
| 6 | 请求里没有 latest 语义 | auto | Pass | request log 无 latest |
| 7 | 状态文件记录 source=OPENHARMONY_CI 与 date=20261102 | auto | Pass | {"source": "OPENHARMONY_CI", "date": "20261102"} |
| 8 | 四件产物装齐 | auto | Pass | db=True cli=True |
| 9 | install 没有 --component 参数（component 是固定值） | auto | Pass | install --help 输出无 --component |

**结论：PASS**
