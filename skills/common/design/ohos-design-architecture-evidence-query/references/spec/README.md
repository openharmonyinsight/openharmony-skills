# oskm 查询工具规格索引

本索引只覆盖 **CLI 查询工具**的功能与参数。skill 的运行时下载、安装、CLI 解析与
排错见 [../usage.md](../usage.md)。

共 14 个模块、52 个工具。每个模块一份规格表，位于 `references/spec/`。

## 模块与工具清单

| 模块 | 工具数 | 文件 | 覆盖能力 |
|------|-------|------|---------|
| session | 10 | [session.md](./session.md) | 会话生命周期、多会话、跨库对比（ATTACH + diff_scans） |
| repos | 3 | [repos.md](./repos.md) | 代码仓查找、列表与 git 访问 URL 构建 |
| component | 8 | [component.md](./component.md) | 部件查找、搜索、依赖、特性、SysCap、InnerAPI |
| service | 3 | [service.md](./service.md) | 系统服务查找、搜索、宿主 SA 服务/HDI 设备导航 |
| install | 4 | [install.md](./install.md) | 安装模块查找、搜索、路径归属、镜像路径反查 |
| gn_args | 2 | [gn_args.md](./gn_args.md) | 编译参数查找与搜索 |
| elf | 3 | [elf.md](./elf.md) | ELF 搜索、依赖闭包 BFS、反向依赖 |
| native | 2 | [native.md](./native.md) | Native SDK 库与 SDK 头文件映射 |
| sa | 2 | [sa.md](./sa.md) | SA 服务按 ID 查找、按库名/配置搜索 |
| hdi | 2 | [hdi.md](./hdi.md) | HDI 按 serviceName/node 查找、模糊搜索 |
| arkts | 7 | [arkts.md](./arkts.md) | SDK 模块、Kit、声明文件、双向关系、实现映射反查、证据与分页 |
| query | 3 | [query.md](./query.md) | 通用列表/聚合/SQL 逃生口 |
| issues | 1 | [issues.md](./issues.md) | 扫描质量问题清单 |
| schema | 2 | [schema.md](./schema.md) | 数据库表/列/FK 自描述 |

## 工具速查

| 工具 | 模块 | 参数 | 一句话 |
|------|------|------|--------|
| `open_session` | session | `db_path, scan_id?, product?` | 连接已扫描库，返回 session_id |
| `close_session` | session | `session_id?` | 关闭指定或当前会话 |
| `switch_session` | session | `session_id` | 切换 active session |
| `list_sessions` | session | — | 列出所有已打开的会话 |
| `get_scan_info` | session | — | 当前扫描元数据 |
| `list_scans` | session | `limit?` | 库中所有扫描 |
| `get_link_stats` | session | — | feature/innerapi 关联命中率 |
| `attach_secondary` | session | `db_path, alias?` | ATTACH 另一个数据库到当前连接 |
| `detach_secondary` | session | `alias` | DETACH 别名数据库 |
| `diff_scans` | session | `entity, scan_a, scan_b, db_b?, fields?` | 两个扫描的结构化差异对比 |
| `get_repo` | repos | `name` | 按仓名查找代码仓 |
| `list_repos` | repos | `limit?` | 列出所有仓 |
| `git_url` | repos | `path, line?` | 工作区路径/GN label → git 仓访问 URL |
| `get_component` | component | `name` | 按名查找部件 |
| `search_components` | component | `query, limit?, subsystem?` | 模糊搜索部件 |
| `component_attached` | component | `component_id, collector?` | 部件关联的各域记录 |
| `component_dependencies` | component | `component_id` | 正向依赖 |
| `component_dependents` | component | `component_id` | 反向依赖 |
| `component_features` | component | `component_id` | 特性名 + gn_arg 值 |
| `component_syscaps` | component | `component_id` | 声明的系统能力名列表 |
| `component_innerapis` | component | `component_id` | InnerAPI + 安装模块 |
| `get_service` | service | `cfg, name?` | 按配置文件路径查找服务 |
| `search_services` | service | `query, type?, component?, limit?` | 模糊搜索服务 |
| `service_hosted` | service | `service_id, collector?` | 服务宿主的 SA/HDI |
| `get_install_module` | install | `label` | 按 GN label 查安装模块 |
| `search_install_modules` | install | `query, type?, component?, limit?` | 模糊搜索安装模块 |
| `owner_of` | install | `dest` | 镜像路径 → 部件 |
| `installed_at` | install | `dest` | 镜像路径 → 安装模块列表 |
| `get_gn_arg` | gn_args | `name` | 按名查编译参数 |
| `search_gn_args` | gn_args | `query, value_type?, has_override?, limit?` | 模糊搜索开关 |
| `search_elf_modules` | elf | `query, partition?, component?, limit?` | 模糊搜索 ELF |
| `elf_dependencies` | elf | `dest, direction?, max_distance?, limit?` | ELF 依赖闭包（节点去重，带 `total`/`truncated`）|
| `elf_dependents` | elf | `dest` | 谁依赖了这个 ELF |
| `search_native_headers` | native | `query, match_strategy?, component?, limit?` | 模糊搜索 Native SDK 库与头文件映射 |
| `get_native_headers` | native | `dest` | 按镜像库路径查 Native SDK 头文件清单 |
| `get_sa` | sa | `sa_id` | 按 SA ID 查找 SA 服务 |
| `search_sas` | sa | `query, distributed?, auto_restart?, component?, limit?` | 模糊搜索 SA 服务 |
| `get_hdi` | hdi | `service_name?, node?` | 按 serviceName/node 查 HDI 设备 |
| `search_hdis` | hdi | `query, component?, hcb?, limit?` | 模糊搜索 HDI |
| `list_entities` | query | `table, filters?, sort?, desc?, page?` | 通用分页列表 |
| `aggregate` | query | `table, group_by, filters?, page?` | 通用聚合 |
| `sql_query` | query | `sql, params?, limit?` | 受限只读 SQL |
| `list_issues` | issues | `collector?, severity?, advisory?, component?, limit?` | 质量问题清单 |
| `get_schema` | schema | `table?` | 表/列/FK 自描述 |
| `get_tables` | schema | — | 已注册表名列表 |
| `list_arkts_kits` | arkts | `query?, origin?, limit?, page_token?` | Kit 与标签分组 |
| `get_arkts_kit` | arkts | `kit_key, limit?, source_page_token?, evidence_page_token?` | Kit 入口、成员两条来路与证据；无入口时给 `mentioned_in` |
| `list_arkts_modules` | arkts | `query?, declaration_scope?, implementation_kind?, declaration_format?, language_coverage?, membership?, component?, implemented_by?, limit?, page_token?` | 逻辑模块清单；`component`/`implemented_by` 从部件或 .so 反查 SDK 接口 |
| `list_arkts_declarations` | arkts | `query?, role?, language_variant?, read_status?, limit?, page_token?` | 声明文件清单（含读取状态与仓内位置）|
| `get_arkts_module` | arkts | `module_key, limit?, declaration_page_token?, evidence_page_token?` | 模块、声明文件、实现 .so、Kit 两条来路与证据 |
| `arkts_kit_modules` | arkts | `kit_key, view?, relation_type?, condition?, limit?, page_token?` | Kit 对应模块或未解析引用 |
| `arkts_module_kits` | arkts | `module_key, relation_type?, condition?, limit?, page_token?` | 模块对应 Kit/标签分组 |

## 通用约定

- 所有工具返回 JSON 可序列化值（dict / list / scalar）
- `id` 始终是数据库 surrogate id（INTEGER），跨工具引用一致
- arkts 工具使用稳定业务键 kit_key/module_key，不输出 surrogate id；顶层 limit/page_token 分页规则见其专用规格
- `scan_id` 由 session 管理，工具参数中不出现
- 分页：`page: {limit: int, page_token?: str}` → `{items: [...], total: int, next_page_token: str?}`
- 错误：`{"error": {"code": "ERROR_CODE", "message": "..."}}`，详见各模块规格
- 缺失值：`null`（字段存在但无值）vs 字段不存在（键缺失）

## 留给 sql_query 的低频场景

以下场景不设 typed 工具，由 `sql_query` 覆盖：

| 场景 | 示例 SQL |
|------|---------|
| innerapi 反查（按 external_name 找提供方） | `SELECT c.name FROM components c JOIN innerapis i ON i.component_id = c.id WHERE i.external_name = ?` |
| 特性反查（按特性名找声明部件） | `SELECT c.name FROM components c JOIN features f ON f.component_id = c.id WHERE f.value = ?` |
| syscap 反查（按 syscap 名找提供部件） | `SELECT c.name FROM components c JOIN syscaps s ON s.component_id = c.id WHERE s.value = ?` |
| 分区级查询（总大小、最大文件） | `SELECT partition, SUM(size) FROM install_targets WHERE scan_id = ? GROUP BY partition` |
| 跨扫描对比 | 用 `diff_scans` typed 工具，或 `attach_secondary` + `sql_query` 手动 JOIN |

## 跨库对比流程

```
1. open_session(db_path="/path/to/current.db", scan_id=2)    → session_id=1
2. attach_secondary(db_path="/path/to/baseline.db", alias="baseline")
3. diff_scans(entity="components", scan_a=2, scan_b=1, db_b="baseline")
   → {added: [...], removed: [...], changed: [...]}
4. sql_query(sql="SELECT ... FROM features JOIN baseline.features ...")  ← 自定义跨库 JOIN
5. detach_secondary(alias="baseline")
6. close_session()
```

详见 [session.md](./session.md) 与 [usage.md §5](../usage.md)。
