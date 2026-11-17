# E4 invalid-archive-preserves-runtime（scripted 臂）

- 开始时间：2026-11-17T16:18:05+08:00
- 结束时间：2026-11-17T16:18:05+08:00
- 执行臂：`scripted`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e04-invalid-archive-preserves-runtime`
- 夹具服务端：http://127.0.0.1:61796
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

## 执行记录

### 1. [夹具准备] 先装一个可用运行时

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e04-invalid-archive-preserves-runtime/runtime install --source INTERNAL_CI --date 20261117
stderr:
==> 下载 INTERNAL_CI 运行时: 20261117
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e04-invalid-archive-preserves-runtime/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e04-invalid-archive-preserves-runtime` · exit=0 · 0.13s

### 2. 对损坏归档执行 refresh

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e04-invalid-archive-preserves-runtime/runtime refresh --source INTERNAL_CI --date 20261118
stderr:
==> 下载 INTERNAL_CI 运行时: 20261118
错误: SQLite integrity_check 未通过: 文件头无效
提示: 未检测到可用的源码根本地运行时。若源码根在别处，用 --source-root <path> 指定，或在源码根及其子目录执行 install。
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e04-invalid-archive-preserves-runtime` · exit=1 · 0.07s

## 夹具服务端请求（被测阶段）

判定只看**工具自己发出**的请求（`User-Agent: Python-urllib/*`，即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测单独列出，不参与契约判定。

### 工具请求（1 条）

```json
[
  {
    "seq": 2,
    "ts": "2026-11-17T16:18:05.339+08:00",
    "method": "GET",
    "path": "/corrupt/20261118",
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

```json
{
  ".oskm-runtime.json": "e0afe7da3ad518520c12fe4b6855501411b10d405838d206f1a6010dcede175a",
  "interface/sdk-js/api/@internal/ohos.evalmarker.d.ts": "8c8c597c1d563cfb53ffb804aafad71adf4145e9b12c048dacceb5bd9cb8d7df",
  "interface/sdk_c/evalmarker.h": "49673a32794f18d5991a5dd76a7719e92119a25906aa30ee34c9a5a8aac89d2d",
  "knowledge.db": "f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44",
  "oskm-cli.pyz": "3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5"
}
```

## 断言结果

自动断言 6/6 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | refresh 以非零状态失败 | auto | Pass | rc=1 |
| 2 | 失败信息指向归档/校验 | auto | Pass | ==> 下载 INTERNAL_CI 运行时: 20261118 错误: SQLite integrity_check 未通过: 文件头无效 提示: 未检测到可用的源码根本地运行时。若源码根在别处，用 --source-root <path> 指定，或在源码根及其子目录执行 install。 |
| 3 | 已有运行时逐文件保持不变（DB / CLI / 两套 SDK / 状态文件） | auto | Pass | 变化: 无；sha 变化: 无 |
| 4 | 旧库仍然可打开且 scans 可读 | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e04-invalid-archive-preserves-runtime/runtime/knowledge.db |
| 5 | 没有留下半装运行时（无安装/备份临时目录） | auto | Pass | leftovers=[] |
| 6 | 被测阶段工具的请求都指向损坏归档端点（没有转去别处凑数据） | auto | Pass | 请求数=1；[{"method": "GET", "path": "/corrupt/20261118"}] |

**结论：PASS**
