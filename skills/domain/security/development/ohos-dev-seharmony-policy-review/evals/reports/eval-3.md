# SELinux 策略提交自检报告

**扫描范围**：evals/files/violation_heavy.diff（stdin，3 个策略文件）
**diff 性质**：新增权限（6 条新增 allow，无对应删除，多处违反自检项）
**涉及策略文件**：3 个  **新增规则行**：6 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | FAIL | sepolicy/base/public/some_base_file.te 纯新增 4 条规则（无同块删除配对）：`allow my_service default_service:binder { call };`、`allow my_service dev_node:chr_file { ioctl read };`、`allow my_service sa_foundation_bms:samgr_class { get };` 等——base/ 禁止新增策略 |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | NA | 无新增/修改 neverallow |
| S5 | SA 服务 neverallow 看护 | WARNING | demo.te 新增 `allow demo_service sa_demo:samgr_class { get };`——SA 服务新增 samgr_class 授权，需确认是否配套 neverallow 看护（如 `neverallow { domain -xxx } sa_demo:samgr_class *;`） |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | NA | 未修改 neverallow 与白名单 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | FAIL | some_base_file.te：`allow my_service default_service:binder { call };` — 使用 default_service 作为授权目标，授予全域权限 |
| S17 | allow/allowxperm 配 avc 日志注释 | WARNING | 6 条新增 allow 中 3 条 hunk 内无 #avc:（default_service、sa_foundation_bms、appdat:file 三处），需补查全文后定级 |
| S18 | allow 落点 system/vendor、public 不放 allow | FAIL | sepolicy/ohos_policy/demo/demo_comp/public/demo.te（public/ 目录）新增 `allow demo_service sa_demo:samgr_class { get };` — public/ 禁止新增 allow |
| S19 | allow 块间空行分隔 | FAIL | 2 处相邻无空行：some_base_file.te 的 `allow my_service dev_node:chr_file { ioctl read };`（与上一条 allow 间仅有 #avc: 注释）、type.te 的 `allow demo_service appdat:dir { getattr };` |
| S20 | appdat 建议改用 normal_app_data | SUGGESTION | type.te：`allow demo_service appdat:file { read };` 与 `allow demo_service appdat:dir { getattr };` — 建议改用 normal_app_data 宏（展开为 { normal_hap_data_file appdat }，普通应用数据的标准抽象） |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无同主体同客体 binder call+transfer 组合 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | PASS | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：6 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **600 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S2] sepolicy/base/public/some_base_file.te：`allow my_service default_service:binder { call };`、`allow my_service dev_node:chr_file { ioctl read };`、`allow my_service sa_foundation_bms:samgr_class { get };` — base/ 禁止新增策略，应迁移至 sepolicy/ohos_policy/<子系统>/<组件>/system/
- [S16] some_base_file.te：`allow my_service default_service:binder { call };` — 禁用 default_service 默认标签作为授权目标 → 改为具体服务类型
- [S18] demo_comp/public/demo.te：`allow demo_service sa_demo:samgr_class { get };` — public/ 禁止新增 allow → 迁移至 system/
- [S19] some_base_file.te：`allow my_service dev_node:chr_file { ioctl read };` — 相邻 allow 间无空行（#avc: 注释属于 allow 块不构成分隔）→ 补空行
- [S19] type.te：`allow demo_service appdat:dir { getattr };` — 相邻 allow 间无空行 → 补空行

## 建议修复（SUGGESTION 建议，提交者评估后决策）
- [S20] demo_comp/system/type.te：`allow demo_service appdat:file { read };`、`allow demo_service appdat:dir { getattr };` → 改用 normal_app_data 宏覆盖普通应用数据客体

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S5] demo_comp/public/demo.te：`allow demo_service sa_demo:samgr_class { get };` → 安全评审确认 SA 服务看护 neverallow 是否配套
- [S17] some_base_file.te 三条无 #avc: 的 allow → 补查全文确认 avc 注释缺失情况，确认缺失升级为 FAIL
