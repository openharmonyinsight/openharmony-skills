# E0 live-smoke（live-smoke 臂）

- 开始时间：2026-11-17T16:18:08+08:00
- 结束时间：2026-11-17T16:18:18+08:00
- 执行臂：`live-smoke`
- skill：`/private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query`（name=ohos-design-architecture-evidence-query, version=3.1.0）
- Python：`/opt/homebrew/opt/python@3.12/bin/python3.12`
- 工作区：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6`
- 夹具服务端：（未使用）
- oskm 源码树（夹具来源）：`/private/tmp/oskm-release-3.1.0-full/packages/oskm`

## 用户请求（来自 evals.json）

用真实 OPENHARMONY_CI 端点装 date=20261116 的运行时并查询

## 期望结果（来自 evals.json）

安装成功、CLI 可查、工具索引与 CLI 一致

## evals.json 断言

| 断言 | 类型 |
|---|---|

## 执行记录

### 1. doctor

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py doctor
Python: 3.12.16 (OK, requires Python 3.10+)
Source / Endpoint: OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI, OSKM_DOWNLOAD_ENDPOINT=已配置
CLI: /private/tmp/oskm-release-3.1.0-full/packages/oskm (source, oskm-cli 1.0.0)
Modules: oskm_runtime (OK), oskm_cli (OK), oskm_schema (OK)
Runtime root: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime
Runtime state: 未安装（没有 knowledge.db）；执行 bootstrap.py install 安装
提示: 运行时来自单个 knowledge.tar.gz——里面就是 knowledge.db + oskm-cli.pyz + 两套 SDK，install 一次装齐；不要求 Git。CLI 按三级候选解析（$OSKM_CLI → 源码树 → <runtime-root>/oskm-cli.pyz），全程不单独下载 CLI。
提示: bootstrap.py 不跑查询。查询直接调 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db …
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 0.06s

### 2. install --source OPENHARMONY_CI --date 20261116

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/bootstrap.py --runtime-root /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime install --source OPENHARMONY_CI --date 20261116
stderr:
==> 下载 OPENHARMONY_CI 运行时: 20261116
==> 运行时安装完成: /private/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 9.8s

### 3. 状态文件

```console
$ cat /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/.oskm-runtime.json
{
  "version": 3,
  "source": "OPENHARMONY_CI",
  "date": "20261116",
  "updated_at": "2026-11-17T16:18:18+08:00",
  "db": {
    "date": "20261116",
    "path": "knowledge.db",
    "sha256": "110cbe5ad107ba54eacd5eaecccb9b94c9a2a91b4ce78ecc21957e22c54c18a1"
  },
  "sdk": {
    "date": "20261116",
    "sdk-js": {
      "path": "interface/sdk-js"
    },
    "sdk_c": {
      "path": "interface/sdk_c"
    }
  },
  "cli": {
    "path": "oskm-cli.pyz",
    "sha256": "ad760c16b3a56a994f23f42530e47ea5e63568ab0f1469afc1efead5cd5eb49e"
  }
}
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 0.01s

### 4. 运行时体积

```console
$ du -sh /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime && find /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime -maxdepth 2 -type d | sort
339M	/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/interface
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/interface/sdk-js
/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/interface/sdk_c
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 0.11s

### 5. CLI 版本

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/oskm-cli.pyz --version
oskm-cli 1.0.0
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 0.09s

### 6. ask get_scan_info

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/oskm-cli.pyz --db /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/knowledge.db ask get_scan_info
{
  "session_id": 1,
  "scan_id": 1,
  "product": "wukong100",
  "cpu_arch": "arm64",
  "workspace_root": "/devcloud/slavespace/usr1/081f8aba80800f0f0fcec015bd66c7e0/harmony_code/codearts_workspace",
  "status": "degraded",
  "started_at": "2026-11-16T14:26:28+00:00",
  "finished_at": "2026-11-16T14:27:04+00:00",
  "collectors": [
    {
      "collector": "args",
      "status": "complete",
      "schema_version": "1.0.0",
      "record_count": 3017
    },
    {
      "collector": "arkts",
      "status": "degraded",
      "schema_version": "7.0.0",
      "record_count": 1338
    },
    {
      "collector": "arkts_links",
      "status": "complete",
      "schema_version": "3.0.0",
      "record_count": 1
    },
    {
      "collector": "component_links",
      "status": "complete",
      "schema_version": "1.0.0",
      "record_count": 1
    },
    {
      "collector": "components",
      "status": "degraded",
      "schema_version": "2.1.0",
      "record_count": 385
    },
    {
      "collector": "elf_modules",
      "status": "complete",
      "schema_version": "3.0.0",
      "record_count": 3697
    },
    {
      "collector": "hdi",
      "status": "degraded",
      "schema_version": "2.1.0",
      "record_count": 59
    },
    {
      "collector": "install_modules",
      "status": "degraded",
      "schema_version": "1.0.0",
      "record_count": 5948
    },
    {
      "collector": "native_headers",
      "status": "complete",
      "schema_version": "1.2.0",
      "record_count": 446
    },
    {
      "collector": "repos",
      "status": "complete",
      "schema_version": "1.0.0",
      "record_count": 528
    },
    {
      "collector": "sas",
      "status": "complete",
      "schema_version": "2.1.0",
      "record_count": 166
    },
    {
      "collector": "services",
      "status": "degraded",
      "schema_version": "4.1.0",
      "record_count": 171
    }
  ],
  "attached_aliases": []
}
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 0.08s

### 7. arch overview

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/oskm-cli.pyz --db /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/knowledge.db arch overview
{
  "product": "wukong100",
  "scan_id": 1,
  "subsystems": 57,
  "counts": {
    "repos": 528,
    "components": 385,
    "install_modules": 5948,
    "install_targets": 7039,
    "elf_modules": 3697,
    "services": 171,
    "sas": 166,
    "hdis": 59,
    "gn_args": 3017,
    "arkts_modules": 1338,
    "arkts_kits": 51
  },
  "top_subsystems": [
    {
      "key": "thirdparty",
      "count": 111
    },
    {
      "key": "hdf",
      "count": 72
    },
    {
      "key": "security",
      "count": 15
    },
    {
      "key": "multimedia",
      "count": 13
    },
    {
      "key": "communication",
      "count": 11
    },
    {
      "key": "hiviewdfx",
      "count": 10
    },
    {
      "key": "resourceschedule",
      "count": 10
    },
    {
      "key": "applications",
      "count": 8
    },
    {
      "key": "distributeddatamgr",
      "count": 8
    },
    {
      "key": "telephony",
      "count": 8
    }
  ]
}
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 0.08s

### 8. ask --list（统计工具数）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/oskm-cli.pyz --db /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/knowledge.db ask --list | tee /dev/stderr | grep -cE "^ {3,4}\*?[a-z_]+"
52
stderr:
arkts
    arkts_kit_modules          Kit 的去重成员模块，或未解析的引用。relation_type 可只取一条来路。注意引用**条数**不等于模块数：同一模块常在 if arkts static / dynamic 两个分支里各 import 一次。被引用也不证明该模块的全部 API 都由这个 Kit 导出
    arkts_module_kits          模块所属的 Kit/标签分组。relation_type 区分"模块自己声明的归属"与"被入口引用"——两者会不一致，而且不一致是正常的
    get_arkts_kit              Kit 详情、入口文件与分页原文证据。member_routes 给出成员的两条来路（模块自己的 @kit 标签 / 入口的 import）各自多少、重合多少；没有入口文件的 label_only 分组改给 mentioned_in（谁提过它）
    get_arkts_module           模块详情、各语言版本的声明文件、实现 so（含镜像实际位置）及分页归属/引用证据。implementation 为 null 表示没有实现证据，不等于"没有实现"——看 module.implementation_kind 区分 type_only / arkts_builtin / unknown
    list_arkts_declarations    分页查询声明文件本身（模块声明与 Kit 入口），含读取状态与仓内位置
    list_arkts_kits            分页查询 SDK Kit 与标签分组。origin=label_only 的分组没有入口文件，不可 import；列出成员不表示这些 API 在本产品可用
    list_arkts_modules         分页查询 SDK 逻辑模块（同一模块的动/静两份声明合为一个模块）。除按声明位置/实现方式筛选外，还可用 component 或 implemented_by 反查"某个部件/某个 .so 实现了哪些 SDK 接口"
component
    component_attached         部件关联的各域记录
    component_dependencies     正向依赖
    component_dependents       反向依赖
    component_features         特性名+编译参数值
    component_innerapis        InnerAPI+安装模块
    component_syscaps          SysCap 声明
    get_component              按名查找部件
    search_components          模糊搜索部件
elf
    elf_dependencies           ELF 依赖闭包（按最短距离去重的可达节点，不是路径枚举）
    elf_dependents             直接反向依赖
    search_elf_modules         模糊搜索 ELF 模块
gn_args
    get_gn_arg                 按名查编译参数
    search_gn_args             模糊搜索编译参数
hdi
    get_hdi                    按 serviceName/node 查 HDI设备
    search_hdis                模糊搜索 HDI设备
install
    get_install_module         按 label 查安装模块
    installed_at               路径→安装模块
    owner_of                   镜像路径→部件
    search_install_modules     模糊搜索安装模块
issues
    list_issues                质量问题清单
native
    get_native_headers         按镜像库路径查 Native SDK 头文件清单
    search_native_headers      模糊搜索 Native SDK 库与头文件映射
query
    aggregate                  通用聚合
    list_entities              通用分页列表
    sql_query                  受限只读 SQL
repos
    get_repo                   按名查找代码仓
    git_url                    路径→git URL
    list_repos                 列出代码仓
sa
    get_sa                     按 ID 查 SA服务
    search_sas                 模糊搜索 SA服务
schema
    get_schema                 表结构自描述
    get_tables                 已注册表名列表
service
    get_service                按 cfg 查找系统服务
    search_services            模糊搜索系统服务
    service_hosted             宿主的 SA服务/HDI设备
session
   *attach_secondary           挂载对比库
   *close_session              关闭会话
   *detach_secondary           卸载对比库
   *diff_scans                 两次扫描差异对比
    get_link_stats             关联命中率
    get_scan_info              扫描元数据
    list_scans                 列出所有扫描
   *list_sessions              列出所有会话
   *open_session               连接知识库
   *switch_session             切换会话

* = 会话类，CLI 里由 --db/--scan-id 或 `diff` 代替
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 0.08s

### 9. ask --list --markdown（生成工具索引）

```console
$ /opt/homebrew/opt/python@3.12/bin/python3.12 /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/oskm-cli.pyz --db /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime/knowledge.db ask --list --markdown > /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/tools-regen.md
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 0.08s

### 10. 与 references/tools.md 逐行对比

```console
$ diff <(grep "^| `" /private/tmp/oskm-release-3.1.0-full/packages/oskm/skills/ohos-design-architecture-evidence-query/references/tools.md) <(grep "^| `" /var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/tools-regen.md) && echo IDENTICAL
IDENTICAL
stderr:
/bin/bash: command substitution: line 1: syntax error: unexpected end of file
```

cwd=`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6` · exit=0 · 0.01s

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

## 环境

- 端点：`https://dcp.openharmony.cn/api/daily_build/build/list/component`
- 下载方式：`OPENHARMONY_CI`
- 日期：`20261116`
- 运行时根：`/var/folders/2g/nr0w8xh97c3d722vdm7skyf00000gn/T/oskm-eval-live-smoke-u01qdgk6/live-runtime`（隔离 HOME，不碰开发者自己的 `~/.oskm`）

## 断言结果

自动断言 4/4 通过

| # | 断言 | 类型 | 结果 | 证据 |
|---:|---|---|---|---|
| 1 | 安装成功且状态文件记录 source/date | auto | Pass | {"version": 3, "source": "OPENHARMONY_CI", "date": "20261116", "updated_at": "2026-11-17T16:18:18+08:00", "db": {"date": "20261116", "path": "knowledge.db", "sha256": "110cbe5ad107ba54eacd5eaecccb9b94c9a2a91b4ce78ecc21957e22c54c18a1"}, "sdk": {"date": "20261116", "sdk-js": {"path": "interface/sdk-js |
| 2 | CLI 能读出扫描元数据 | auto | Pass | product=wukong100 |
| 3 | arch overview 返回真实计数 | auto | Pass | {"repos": 528, "components": 385, "install_modules": 5948, "install_targets": 7039, "elf_modules": 3697, "services": 171, "sas": 166, "hdis": 59, "gn_args": 3017, "arkts_modules": 1338, "arkts_kits": 51} |
| 4 | references/tools.md 与 CLI 生成的索引逐行一致 | auto | Pass | IDENTICAL |

**结论：PASS**
