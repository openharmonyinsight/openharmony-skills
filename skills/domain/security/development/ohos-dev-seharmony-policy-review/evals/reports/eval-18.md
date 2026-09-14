# SELinux 策略提交自检报告

**扫描范围**：evals/files/s2a_pairing_negative.diff（stdin，1 个策略文件，F4 配对签名回归集）
**diff 性质**：新增权限 + 修改既有行（同块同类签名配对边界场景综合）
**涉及策略文件**：1 个  **新增规则行**：6 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | FAIL | base/te/pairing.te 四处纯新增违规（同块删除不得跨签名豁免）：`allow fresh_one data_file:file { read };`（删除的注释行不提供豁免）、`allow fresh_two data_file:file { read };`（删除的 attribute 语句不提供豁免）、`allow fresh_three data_file:file { read };`（一条删除最多豁免一条同签名新增）、`allow fresh_four data_file:file { read };`（删除行 object:class 不同不豁免）；两条修改豁免：`allow mod_domain target_file:file { read open };`（权限集扩展）、`allow renamed_domain target_file:file { read };`（主体 rename，object:class 不变仍配对） |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | NA | 无新增/修改 neverallow |
| S5 | SA 服务 neverallow 看护 | NA | 无新增 SA 服务标签 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | NA | 未修改 neverallow 与白名单 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | WARNING | 6 条新增 allow hunk 内均无 #avc: 注释，需补查全文后定级 |
| S18 | allow 落点 system/vendor、public 不放 allow | NA | 落点问题已由 S2-A 判 FAIL（base/te 非法落点），S18-B/C 主体分区判定不适用 |
| S19 | allow 块间空行分隔 | FAIL | 同块 `+allow mod_domain target_file:file { read open };` 与 `+allow fresh_three data_file:file { read };` 相邻无空行 |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | PASS | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：6 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：4 条 × 100B（可抵消）
- access_vector 范围变更（M）：1 处 × 100B（按新增计，删减不抵消；mod_domain 权限集扩展识别为 M）
- **预计 ROM 增量**：(A − D + M) × 100B = **300 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S2] base/te/pairing.te：`allow fresh_one data_file:file { read };` — 删除的注释行不得为新增 allow 提供修改豁免 → 迁移至 ohos_policy/ 并补 #avc: 注释
- [S2] base/te/pairing.te：`allow fresh_two data_file:file { read };` — 删除的 attribute 语句不得豁免新增 allow → 同上
- [S2] base/te/pairing.te：`allow fresh_three data_file:file { read };` — 一条删除最多豁免一条同签名新增，第二条为纯新增 → 同上
- [S2] base/te/pairing.te：`allow fresh_four data_file:file { read };` — 删除行（other_domain other_target:file）object:class 与新增不同，不构成修改 → 同上
- [S19] base/te/pairing.te：`allow fresh_three data_file:file { read };` — 与同块新增 allow 相邻无空行 → 补空行

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S17] pairing.te 6 条新增 allow 均无 #avc: → 补查全文确认，确认缺失升级为 FAIL
