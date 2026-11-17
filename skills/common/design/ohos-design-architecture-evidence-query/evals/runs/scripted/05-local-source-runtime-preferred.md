# E5 local-source-runtime-preferred（scripted 臂）

- 开始时间：2026-11-17T16:18:05+08:00
- 结束时间：2026-11-17T16:18:06+08:00
- 执行臂：`scripted`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred`
- 夹具服务端：http://127.0.0.1:61799
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

## 用户请求（来自 evals.json）

当前目录是完整 OpenHarmony 源码根，包含 .gn、非空的 interface/sdk-js 和 interface/sdk_c、out/sample-product/oskm/knowledge.db 或 artifacts/sample-product/knowledge.db，以及本地 cli/dist/oskm-cli.pyz。请安装运行时，并避免不必要的网络请求。

## 期望结果（来自 evals.json）

install 优先使用源码树中的 DB、CLI 和两套 SDK，记录 source: local 和源码根路径；cli-path 也应优先源码树 CLI；本地候选完整时不得调用下载端点。

## evals.json 断言

| 断言 | 类型 |
|---|---|
| source: local | `contains` |
| 不使用下载 | `contains` |
| 本地 DB、CLI、sdk-js 和 sdk_c 完整时优先本地且不访问网络 | `llm_judge` |

## 执行记录

### 1. 在源码根里安装（不显式给 --source-root）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/runtime install --date 20261117
stderr:
==> 使用源码本地运行时: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/source/out/sample-product/oskm/knowledge.db
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/source` · exit=0 · 0.11s

### 2. 状态文件

```console
$ cat /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/runtime/.oskm-runtime.json
{
  "version": 3,
  "source": "local",
  "date": "20261117",
  "updated_at": "2026-11-17T16:18:05+08:00",
  "source_root": "/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/source",
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

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred` · exit=0 · 0.01s

### 3. 源码 DB 与已装 DB 的 sha256

```console
$ shasum -a 256 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/source/out/sample-product/oskm/knowledge.db /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/runtime/knowledge.db
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/source/out/sample-product/oskm/knowledge.db
f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44  /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/runtime/knowledge.db
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred` · exit=0 · 0.02s

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

自动断言 8/8 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 本地候选完整时工具一次网络请求都不发 | auto | Pass | [] |
| 2 | 状态文件记录 source=local | auto | Pass | source=local |
| 3 | 状态文件记录源码根路径 | auto | Pass | source_root=/private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/source |
| 4 | 装进来的 DB 就是源码树那一份（sha256 相同） | auto | Pass | installed=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 source=f561e39f648cfd6b391d6b2b0e1a5ec32e9ab5c8990dc9cbedf2f1685fcd1b44 |
| 5 | 装进来的 CLI 就是源码树 cli/dist 那一份 | auto | Pass | installed=3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5 source=3e78cf73a94bcf9df24409db686092d7acb74b35ad3e891c6493b9b57cd171f5 |
| 6 | 两套 SDK 都从源码树复制过来且非空 | auto | Pass | sdk-js=1 sdk_c=1 |
| 7 | 源码树本身没有被改动（DB 仍在原位） | auto | Pass | /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/source/out/sample-product/oskm/knowledge.db / /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/source/cli/dist/oskm-cli.pyz |
| 8 | 安装日志说明用了源码本地运行时 | auto | Pass | ==> 使用源码本地运行时: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-local-source-runtime-preferred/source/out/sample-product/oskm/knowledge.db ==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-scripted-d88ey2af/scripted/e05-l |

**结论：PASS**
