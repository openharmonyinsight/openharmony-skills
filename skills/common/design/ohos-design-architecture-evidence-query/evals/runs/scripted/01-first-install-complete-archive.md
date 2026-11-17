# E1 first-install-complete-archive（scripted 臂）

- 开始时间：2026-11-17T16:18:03+08:00
- 结束时间：2026-11-17T16:18:03+08:00
- 执行臂：`scripted`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive`
- 夹具服务端：http://127.0.0.1:61789
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

## 用户请求（来自 evals.json）

运行根目录为空，测试夹具已提供一个本地 knowledge.tar.gz，内含 knowledge.db、oskm-cli.pyz、interface/sdk-js 和 interface/sdk_c。请从任意 Agent 启动目录安装该 skill 的托管运行时，并报告安装后的布局、状态与当前工作目录。

## 期望结果（来自 evals.json）

使用绝对路径调用 bootstrap.py install，把 knowledge.db、oskm-cli.pyz、interface/sdk-js 和 interface/sdk_c 一次装到同一个 runtime root；状态文件包含 db、sdk、cli 三段，不需要单独的 CLI 下载端点；安装完成后回到 Agent 启动目录。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| knowledge.db | `contains` |
| oskm-cli.pyz | `contains` |
| interface/sdk-js | `contains` |
| interface/sdk_c | `contains` |
| 四个产物位于同一 runtime root，未使用单独的 CLI 下载端点，且安装后当前目录等于 Agent 启动目录 | `llm_judge` |

## 执行记录

### 1. 记录 Agent 启动目录

```console
$ pwd
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/agent-start
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/agent-start` · exit=0 · 0.0s

### 2. 用绝对路径安装托管运行时（不 cd 到 skill 目录）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime install --source INTERNAL_CI --date 20261117
stderr:
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/agent-start` · exit=0 · 0.09s

### 3. 确认当前目录未变

```console
$ pwd
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/agent-start
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/agent-start` · exit=0 · 0.0s

### 4. 运行时布局

```console
$ find /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime -maxdepth 3 | sort
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/.oskm-runtime.json
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/interface
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/interface/sdk-js
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/interface/sdk-js/api
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/interface/sdk_c
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/interface/sdk_c/evalmarker.h
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/knowledge.db
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/oskm-cli.pyz
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive` · exit=0 · 0.01s

### 5. 状态文件

```console
$ cat /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/.oskm-runtime.json
{
  "version": 3,
  "source": "INTERNAL_CI",
  "date": "20261117",
  "updated_at": "2026-11-17T16:18:03+08:00",
  "db": {
    "date": "20261117",
    "path": "knowledge.db",
    "sha256": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44"
  },
  "sdk": {
    "date": "20261117",
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

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive` · exit=0 · 0.0s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 1,
    "ts": "2026-11-17T16:18:03.406+08:00",
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

## 断言结果

自动断言 9/9 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | knowledge.db 装到了运行时根目录 | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/knowledge.db |
| 2 | oskm-cli.pyz 与 DB 并排（同一次安装装齐） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/runtime/oskm-cli.pyz |
| 3 | interface/sdk-js 非空 | auto | Pass | 1 个文件 |
| 4 | interface/sdk_c 非空 | auto | Pass | 1 个文件 |
| 5 | 状态文件同时记录 db / sdk / cli 三段 | auto | Pass | ["cli", "date", "db", "sdk", "source", "updated_at", "version"] |
| 6 | 工具每次安装只发一条"按日期取归档"的请求（没有盲探端点，也没有单独的 CLI 下载端点） | auto | Pass | 请求数=1，其中按日期归档请求=1；oskm-cli.pyz 已随归档装好=True；[{"method": "GET", "path": "/internal/20261117"}] |
| 7 | Agent 启动目录没有被安装产物污染 | auto | Pass | 启动目录内容: [] |
| 8 | 运行时根目录没有残留安装临时目录 | auto | Pass | leftovers=[] |
| 9 | 安装前后当前目录一致（未用 cd 污染 Agent 启动目录） | auto | Pass | pwd=['/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/agent-start', '/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e01-first-install-complete-archive/agent-start'] |

**结论：PASS**
