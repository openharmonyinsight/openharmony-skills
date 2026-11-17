# E6 cli-resolution-chain（scripted 臂）

- 开始时间：2026-11-17T16:18:06+08:00
- 结束时间：2026-11-17T16:18:06+08:00
- 执行臂：`scripted`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain`
- 夹具服务端：http://127.0.0.1:61800
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

## 用户请求（来自 evals.json）

运行时目录中存在已安装的 oskm-cli.pyz，同时设置了 OSKM_CLI，源码树也可用。请说明 bootstrap.py cli-path 应选择哪个候选；随后假设三个候选都不存在，再说明错误应如何提示。

## 期望结果（来自 evals.json）

解析顺序为 $OSKM_CLI → 源码树 CLI → <runtime-root>/oskm-cli.pyz。全部候选不存在时退出失败并提示运行 bootstrap.py install；CLI 不从网络自动下载。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| $OSKM_CLI | `contains` |
| <runtime-root>/oskm-cli.pyz | `contains` |
| bootstrap.py install | `contains` |
| 源码树 CLI 优先于已安装产物，失败提示可操作，且不会联网下载 CLI | `llm_judge` |

## 执行记录

### 1. a) 三个候选都在，且设置了 OSKM_CLI

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/installed-runtime cli-path
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/fixtures/oskm-cli.pyz
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/agent-start` · exit=0 · 0.09s

### 2. b) 去掉 OSKM_CLI，工具代码在源码树里

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/source-tree/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/installed-runtime cli-path
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/source-tree
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/agent-start` · exit=0 · 0.06s

### 3. c) 再去掉源码树，只剩已安装产物

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/plain-tool/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/installed-runtime cli-path
/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/installed-runtime/oskm-cli.pyz
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/agent-start` · exit=0 · 0.06s

### 4. d) 三个候选都不存在

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/plain-tool/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/empty-runtime cli-path
stderr:
错误: 找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布，所以正常情况下 `bootstrap.py install` 会把它装到 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/empty-runtime/oskm-cli.pyz。已尝试：
  1. $OSKM_CLI 未设置
  2. 源码树 —— 向上没找到 cli/oskm_cli/__init__.py
  3. /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/empty-runtime/oskm-cli.pyz —— 不存在
可行做法：
  · 跑 `bootstrap.py install` 从运行时归档里装（含 CLI）
  · 或在源码仓构建后手动复制：python3 cli/scripts/build_cli.py，再把 cli/dist/oskm-cli.pyz 放到 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/empty-runtime/oskm-cli.pyz
  · 或用 OSKM_CLI 直接指向一个 .pyz / 源码树
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/agent-start` · exit=1 · 0.06s

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

自动断言 6/6 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | a) 选中 $OSKM_CLI | auto | Pass | stdout=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/fixtures/oskm-cli.pyz |
| 2 | b) 选中源码树 CLI | auto | Pass | stdout=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/source-tree |
| 3 | c) 选中 <runtime-root>/oskm-cli.pyz | auto | Pass | stdout=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-chain/installed-runtime/oskm-cli.pyz |
| 4 | d) 失败并给出可操作的下一步 | auto | Pass | rc=1；stderr=错误: 找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布，所以正常情况下 `bootstrap.py install` 会把它装到 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-r
… [输出截断，完整内容见工作区] …
3. /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06 |
| 5 | d) 失败信息说明 CLI 不从网络自动下载 | auto | Pass | 错误: 找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布，所以正常情况下 `bootstrap.py install` 会把它装到 /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e06-cli-resolution-ch |
| 6 | 整个过程工具没有联网 | auto | Pass | [] |

**结论：PASS**
