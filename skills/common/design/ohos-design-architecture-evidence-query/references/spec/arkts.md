# ArkTS 模块与 Kit 工具

首期采集模块、Kit 及直接关系，不解析成员 API、权限或版本可用性。工具查询只读
SQLite，不需要 Node；`interface/sdk-js` 是运行时源码输入，用来核对 DB 给出的声明
位置和实现关系，不是数据库，也不由查询过程重新扫描。

**模块与声明文件是两层。** 一个模块可以有两份声明：`X.d.ts`/`X.d.ets` 是 ArkTS 1.1
版本，`X.static.d.ets` 是 1.2 版本。模块查询返回逻辑模块；声明文件查询返回物理文件。
按名 import 落在模块上，读取状态落在声明文件上；两者数量随快照变化，不能互相换算。

| 工具 | 必填参数 | 可选参数 | 返回 |
|---|---|---|---|
| list_arkts_kits | 无 | query、origin、limit、page_token | Kit 列表，含来源数、去重模块数、未解析引用数 |
| list_arkts_modules | 无 | query、declaration_scope、implementation_kind、declaration_format、language_coverage、membership、**component**、**implemented_by**、limit、page_token | 逻辑模块列表、声明文件数及证据计数 |
| list_arkts_declarations | 无 | query、role、language_variant、read_status、limit、page_token | 声明文件列表，含读取状态与仓内位置 |
| get_arkts_kit | kit_key | limit、source_page_token、evidence_page_token | Kit、summary、**member_routes**、sources 分页、evidence 分页、quality；无入口文件时另给 **mentioned_in** |
| get_arkts_module | module_key | limit、declaration_page_token、evidence_page_token | module、declarations 分页（各带 source）、**implementation**（实现 so 及镜像位置，无实现时为 null）、**kit_routes**、issues 摘要、evidence 分页、quality |
| arkts_kit_modules | kit_key | view、relation_type、condition、include_unspecified、include_candidates、limit、page_token | 去重模块或未解析引用分页 |
| arkts_module_kits | module_key | relation_type、condition、include_unspecified、include_candidates、limit、page_token | 去重 Kit/标签分组分页 |

业务键不使用数据库代理 id：kit_key 如 `@kit.AbilityKit` 或 `label:API10LessDeprecatedModules`；
module_key 是**去掉语言后缀**的 SDK 相对路径，如 `api/@ohos.app.ability.UIAbility`（不带 `.d.ts`）；
声明文件的 source_path 是 workspace 相对路径，如 `interface/sdk-js/api/@ohos.app.ability.UIAbility.d.ts`。

运行时根目录下应存在统一归档解压出的 `interface/sdk-js/` 源码树，`source_path` 直接从该根目录解析。
DB 的模块、Kit、声明与 `.so` 关系以扫描快照为准；归档中的 SDK 快照可能漂移。读取声明前先看
source 的 `revision`、`content_match` 与 `source_metadata_stale`，不要把当前 HEAD 的内容
说成扫描时的字节（`content_match` 恒为 `unverified`）。源码目录缺失或路径不存在时明确报告
`SDK 源码缺失`，不要退化成“模块没有实现”或“Kit 没有成员”。

列表分页返回 `scan_id/input_digest/items/total/next_page_token/quality`。limit 默认为 50，范围 1..200；page_token 不超过 4 KiB，与扫描、内容/解析配置、过滤参数和视图绑定。使用 next_page_token 时维持相同过滤参数，直到 next_page_token=null。扫描发生变化返回 STALE_PAGE_TOKEN；过滤条件不一致返回 INVALID_PAGE_TOKEN。

query 是大小写敏感的普通子串，`%`、`_` 不作通配符。过滤值如下：

- origin：entry_backed / label_only。
- declaration_scope：api_named / api_auxiliary / internal_component / internal_ets /
  arkts_named / arkts_builtin —— 声明在哪，纯路径事实。
- implementation_kind：napi / arkui / arkts_builtin / arkts_language / type_only / unknown
  —— 怎么实现。目录是混的（api_named 下既有 napi 也有 arkui），所以与 scope 分开两列。
- declaration_format：d.ts / d.ets / static.d.ets，筛选"至少有一份该格式声明"的模块。
- language_coverage：dynamic / static / both，模块被哪些 ArkTS 语言版本声明。
- role：module / kit_entry，声明文件是模块声明还是 Kit 入口。
- language_variant：dynamic / static，单份声明文件属于哪个语言版本。
- read_status：ok / unreadable / encoding_failed / limit_exceeded / path_invalid。
- membership：declared / undeclared，只判断是否有 confirmed 的头部归属证据。
- component：按**实现它的 .so 所属部件名**精确筛选，例如 `ace_engine`（473 个 ArkUI 模块）。
  这是反向查询——从产品部件回到它实现了哪些 SDK 接口。
- implemented_by：按**实现库路径子串**筛选，例如 `libimage.z.so`。
  用子串是为了允许调用方只给文件名；库中保存的已经是按扫描架构归一后的完整路径。
- `implementation.installed_at` 来自 `install_targets.dest`，是镜像里的实际安装路径：
  `arm` 通常为 `system/lib/…`，`arm64` 通常为 `system/lib64/…`，但必须以 ELF
  采集结果为准。`implementation.impl_so_path` 由采集器按本次 `ScanRequest.cpu_arch`
  构造（默认 `arm64`）；ArkUI 在安装清单只有一个不同目标时优先采用该安装证据，
  多个目标则保留架构 fallback 并报告 ambiguous。`arkts_links` 只按完整路径精确
  关联；查询阶段不按来源或架构重写任一返回路径。
- relation_type：declared_membership（模块头部归属）/ entry_reference（Kit 入口直接引用）；省略时取并集。
- view：resolved（默认）/ unresolved；后者返回引用证据，包含 ambiguous、not_found、out_of_scope、unsupported。
  动/静双声明会折叠为同一个模块，不再算多候选；`ambiguous` 数量仍以返回的
  `quality.target_resolution` 为准。
- condition：dynamic / static / both / unknown / unspecified。dynamic/static 也匹配明确的 both；默认不将 unspecified 当作支持，include_unspecified=true 可纳入未声明条件。
- include_candidates：默认 false；设为 true 才把孤立 @kit 等候选证据计入关系查询。

## 两条来路：`member_routes` / `kit_routes`

Kit 与模块之间的成员关系有两条**互不相同**的来路：

- `declared_membership`——模块在自己文件头写了 `@kit X` 标签（模块的自本文声明）
- `entry_reference`——`@kit.X` 的入口文件 import 了它（入口的实际组成）

**两者会不一致，而且不一致是正常的。** 只给一个合计数就把"谁说的"抹掉了，
所以 `get_arkts_kit` 返回 `member_routes`、`get_arkts_module` 返回 `kit_routes`，
格式同为 `{total, both, declared_only, referenced_only}`，数的是**去重后的对端**。

`member_routes` / `kit_routes` 会分别给出 `total`、`both`、`declared_only` 和
`referenced_only`。这些数字随扫描输入变化，不要复制到结论里当常量。

> **引用条数 ≠ 模块数。** 同一个模块常在 `if arkts static` 和 `dynamic` 两个分支里
> 各 import 一次。`arkts_kit_modules` 返回的是去重模块，`evidence` 分页返回的是
> 逐条证据，别混。

## `mentioned_in`：没有入口文件时的回答

`origin=label_only` 的分组**根本没被定义**——只是某个模块头上写了个对不上任何入口的
标签，所以 `sources` 恒为空。空列表会被读成"查不到它的定义文件"，而事实是它没有定义
文件。因此 `get_arkts_kit` 在 `sources.total == 0` 时另给 `mentioned_in`：
`{note, total, items:[{source_path, module_key}]}`，回答"谁提过它"。
有入口的 Kit **不带这一项**，因为对它们这个问题没有意义。

## 实现映射

`get_arkts_module` 的 `implementation` 给出实现该模块的 .so：`impl_so_path` 是本次扫描
按 `cpu_arch` 构造的实现库镜像路径（arm 为 `system/lib/…`，arm64 为 `system/lib64/…`），
`installed_at` 是它在本产品镜像中的实际位置，`impl_match` 说明运行时名是怎么对上的
（`name_suffix` 是兜底匹配，证据弱一些）。新库中两者由完整路径精确关联，正常应相同。
**`implementation` 为 null 表示"不知道由谁实现"，不是解析失败**；有值而无 `installed_at`
表示扫描期望的实现路径不在本产品镜像里。两者是不同的事实。

详情 evidence 保留原文、UTF-8 字节半开区间和 1-based 码点行列；所有跨度对应扫描时的完整内容摘要。
文件头原文不入库（整段是许可证样板），只保留 `header_span`，需要时按扫描 revision 回
`interface/sdk-js` 源码切片；若只有当前 HEAD，必须说明内容可能漂移。一个模块可有多条证据，
Kit→模块列表通过 EXISTS 去重，不据此宣称整个模块 API 均由 Kit 导出。

quality 分 discovery、headers、entry_references、target_resolution 四项。目标 resolved 只证明本次输入中目标模块唯一，不能证明类型检查成功或运行环境支持。source 的 content_match 为 unverified，仓数据重写时标记 source_metadata_stale，保留扫描时 revision。

错误包括 COLLECTOR_NOT_RUN、COLLECTOR_FAILED、SCHEMA_UNSUPPORTED、NOT_FOUND、
INVALID_PARAM、MISSING_PARAM、INVALID_PAGE_TOKEN、STALE_PAGE_TOKEN、CAPABILITY_UNAVAILABLE。

`component` 筛选要跨到 `elf_modules`/`components`，那次扫描没采 ELF 时返回
**CAPABILITY_UNAVAILABLE**，不返回 0 条——"没采所以答不了"和"没有模块由这个部件实现"
是两回事。判据是 `collector_runs` 里有没有那个采集器，**不是表在不在**：
框架建库时会把全部已注册采集器的表都建出来，`--only arkts` 的库里 `elf_modules`
照样存在，只是一行没有。未知参数在 handler 中拒绝，不依赖客户端执行 JSON Schema 校验。旧库尚未扫描 arkts 时返回 COLLECTOR_NOT_RUN，不返回空清单冒充已采集。

查询发布包不包含 collectors。用 `ask` 的 ArkTS 工具查询模块、Kit、声明与关系；需要跨四张表聚合时使用 `sql`，可用表为 `arkts_modules`、`arkts_kits`、`arkts_sources`、`arkts_kit_relations`。
