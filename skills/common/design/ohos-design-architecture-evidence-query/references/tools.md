# oskm 查询工具索引

> **本文件由 `python3.12 ~/.oskm/oskm-cli.pyz ask --list --markdown` 生成，不要手改。**
> 等价：`oskm-cli ask --list --markdown`（CLI 是独立产物，见
> `packages/oskm/cli/README.md`）。
> 会话类工具（open_session/attach_secondary/diff_scans…）不在此列——
> 在 CLI 里它们退化成 `--db` / `--scan-id` 参数与 `diff` 子命令。

| 工具 | 模块 | 参数 | 说明 |
|---|---|---|---|
| `arkts_kit_modules` | arkts | `limit`?, `page_token`?, `relation_type`?, `condition`?, `include_unspecified`?, `include_candidates`?, `kit_key`, `view`? | Kit 的去重成员模块，或未解析的引用。relation_type 可只取一条来路。注意引用**条数**不等于模块数：同一模块常在 if arkts static / dynamic 两个分支里各 import 一次。被引用也不证明该模块的全部 API 都由这个 Kit 导出 |
| `arkts_module_kits` | arkts | `limit`?, `page_token`?, `relation_type`?, `condition`?, `include_unspecified`?, `include_candidates`?, `module_key` | 模块所属的 Kit/标签分组。relation_type 区分"模块自己声明的归属"与"被入口引用"——两者会不一致，而且不一致是正常的 |
| `get_arkts_kit` | arkts | `kit_key`, `limit`?, `source_page_token`?, `evidence_page_token`? | Kit 详情、入口文件与分页原文证据。member_routes 给出成员的两条来路（模块自己的 @kit 标签 / 入口的 import）各自多少、重合多少；没有入口文件的 label_only 分组改给 mentioned_in（谁提过它） |
| `get_arkts_module` | arkts | `module_key`, `limit`?, `declaration_page_token`?, `evidence_page_token`? | 模块详情、各语言版本的声明文件、实现 so（含镜像实际位置）及分页归属/引用证据。implementation 为 null 表示没有实现证据，不等于"没有实现"——看 module.implementation_kind 区分 type_only / arkts_builtin / unknown |
| `list_arkts_declarations` | arkts | `limit`?, `page_token`?, `query`?, `role`?, `language_variant`?, `read_status`? | 分页查询声明文件本身（模块声明与 Kit 入口），含读取状态与仓内位置 |
| `list_arkts_kits` | arkts | `limit`?, `page_token`?, `query`?, `origin`? | 分页查询 SDK Kit 与标签分组。origin=label_only 的分组没有入口文件，不可 import；列出成员不表示这些 API 在本产品可用 |
| `list_arkts_modules` | arkts | `limit`?, `page_token`?, `query`?, `declaration_scope`?, `implementation_kind`?, `declaration_format`?, `language_coverage`?, `membership`?, `component`?, `implemented_by`? | 分页查询 SDK 逻辑模块（同一模块的动/静两份声明合为一个模块）。除按声明位置/实现方式筛选外，还可用 component 或 implemented_by 反查"某个部件/某个 .so 实现了哪些 SDK 接口" |
| `component_attached` | component | `component_id`, `collector`? | 部件关联的各域记录 |
| `component_dependencies` | component | `component_id` | 正向依赖 |
| `component_dependents` | component | `component_id` | 反向依赖 |
| `component_features` | component | `component_id` | 特性名+编译参数值 |
| `component_innerapis` | component | `component_id` | InnerAPI+安装模块 |
| `component_syscaps` | component | `component_id` | SysCap 声明 |
| `get_component` | component | `name` | 按名查找部件 |
| `search_components` | component | `query`, `limit`?, `subsystem`? | 模糊搜索部件 |
| `elf_dependencies` | elf | `dest`, `direction`?, `max_distance`?, `limit`? | ELF 依赖闭包（按最短距离去重的可达节点，不是路径枚举） |
| `elf_dependents` | elf | `dest` | 直接反向依赖 |
| `search_elf_modules` | elf | `query`, `partition`?, `component`?, `limit`? | 模糊搜索 ELF 模块 |
| `get_gn_arg` | gn_args | `name` | 按名查编译参数 |
| `search_gn_args` | gn_args | `query`, `value_type`?, `has_override`?, `limit`? | 模糊搜索编译参数 |
| `get_hdi` | hdi | `service_name`?, `node`? | 按 serviceName/node 查 HDI设备 |
| `search_hdis` | hdi | `query`, `component`?, `hcb`?, `limit`? | 模糊搜索 HDI设备 |
| `get_install_module` | install | `label` | 按 label 查安装模块 |
| `installed_at` | install | `dest` | 路径→安装模块 |
| `owner_of` | install | `dest` | 镜像路径→部件 |
| `search_install_modules` | install | `query`, `type`?, `component`?, `limit`? | 模糊搜索安装模块 |
| `list_issues` | issues | `collector`?, `severity`?, `advisory`?, `component`?, `limit`? | 质量问题清单 |
| `get_native_headers` | native | `dest` | 按镜像库路径查 Native SDK 头文件清单 |
| `search_native_headers` | native | `query`, `match_strategy`?, `component`?, `limit`? | 模糊搜索 Native SDK 库与头文件映射 |
| `aggregate` | query | `table`, `group_by`, `filters`?, `page`? | 通用聚合 |
| `list_entities` | query | `table`, `filters`?, `sort`?, `desc`?, `page`? | 通用分页列表 |
| `sql_query` | query | `sql`, `params`?, `limit`? | 受限只读 SQL |
| `get_repo` | repos | `name` | 按名查找代码仓 |
| `git_url` | repos | `path`, `line`? | 路径→git URL |
| `list_repos` | repos | `limit`? | 列出代码仓 |
| `get_sa` | sa | `sa_id` | 按 ID 查 SA服务 |
| `search_sas` | sa | `query`, `distributed`?, `auto_restart`?, `component`?, `limit`? | 模糊搜索 SA服务 |
| `get_schema` | schema | `table`? | 表结构自描述 |
| `get_tables` | schema | — | 已注册表名列表 |
| `get_service` | service | `cfg`, `name`? | 按 cfg 查找系统服务 |
| `search_services` | service | `query`, `type`?, `component`?, `limit`? | 模糊搜索系统服务 |
| `service_hosted` | service | `service_id`, `collector`? | 宿主的 SA服务/HDI设备 |
| `get_link_stats` | session | — | 关联命中率 |
| `get_scan_info` | session | — | 扫描元数据 |
| `list_scans` | session | `limit`? | 列出所有扫描 |
