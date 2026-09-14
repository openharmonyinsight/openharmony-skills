# SELinux 策略提交自检报告

**扫描范围**：evals/files/s1_token_medial.diff（stdin，1 个策略文件，access_token 安全标识符回归集）
**diff 性质**：新增权限 + 类型定义（token 后缀/居中标识符不误报 + 相邻 allow 缺空行）
**涉及策略文件**：1 个  **新增规则行**：2 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | `type access_token_data, file_type;`、`sa_access_token_check`、`access_token_service`、`my_access_token_type` 均为 access_token 相关安全标识符（后缀型与 token 居中型），非品牌类敏感词，不触发 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | PASS | 策略位于 ohos_policy/test/test_s1_medial/system/，单一目录 |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | NA | 无新增/修改 neverallow |
| S5 | SA 服务 neverallow 看护 | WARNING | 新增 `type my_access_token_type, sa_service_attr;` SA 服务类型 + samgr_class 授权，需确认是否配套 neverallow 看护 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | NA | 未修改 neverallow 与白名单 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | WARNING | 2 条新增 allow（sa_access_token_check、access_token_service）hunk 内均无 #avc: 注释，需补查全文后定级 |
| S18 | allow 落点 system/vendor、public 不放 allow | PASS | allow 位于 system/ 目录 |
| S19 | allow 块间空行分隔 | FAIL | `allow foo_service sa_access_token_check:samgr_class { get };` 与 `allow bar_service access_token_service:samgr_class { get };` 相邻无空行 |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | PASS | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：2 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute；type 定义行不计入 A）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **200 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S19] s1_medial.te：`allow bar_service access_token_service:samgr_class { get };` — 与上一条 allow 间无空行 → 补空行

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S5] s1_medial.te：`type my_access_token_type, sa_service_attr;` → 安全评审确认 SA 服务看护 neverallow 是否配套
- [S17] s1_medial.te 两条新增 allow 无 #avc: → 补查全文确认，确认缺失升级为 FAIL
