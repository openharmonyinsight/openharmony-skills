# SELinux 策略提交自检报告

**扫描范围**：evals/files/real_pr8186_pc_only.diff（stdin，base/public/domain.te + storage_daemon.te 2 个文件）
**diff 性质**：neverallow 拆分 + 产品宏例外项与包裹（真实 PR #8186 形态）
**涉及策略文件**：2 个  **新增规则行**：5 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | FAIL | base/public/domain.te 纯新增 3 行（无同块同签名配对）：`neverallow { ... pc_only(\`-storage_daemon') ... } dev_file:blk_file *;`（原 neverallow 按类别拆分的延续行）、`pc_only(\`` 与 `')` 包裹行及内部 `neverallow storage_daemon dev_file:blk_file { append relabelfrom relabelto map unlink link rename };` — base/ 新增策略需走 base 专项评审 |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | SUGGESTION | domain.te 新增 neverallow 主体含 domain、storage_daemon 等；stdin 未绑定目标树，引用列表见扫描输出，建议以目标 ref 重跑完成落点判定 |
| S5 | SA 服务 neverallow 看护 | NA | 无新增 SA 服务标签 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | WARNING | domain.te 修改既有 neverallow（dev_file 类别拆分为 file/chr_file 与 blk_file 两行）并新增例外与包裹，需安全评审确认既有评审记录覆盖 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | PASS | storage_daemon.te 的 `allow storage_daemon dev_block_file:blk_file { ioctl };` 与 `allowxperm storage_daemon dev_block_file:blk_file ioctl { 0x4c00 0x4c01 0x1263 };` 上方均配有 #avc: denied 注释 |
| S18 | allow 落点 system/vendor、public 不放 allow | PASS | storage_daemon.te 位于 system/ 目录，主体为系统组件；domain.te 无新增 allow |
| S19 | allow 块间空行分隔 | FAIL | storage_daemon.te 宏体内 `allow storage_daemon dev_block_file:blk_file { ioctl };` 与 `allowxperm storage_daemon dev_block_file:blk_file ioctl { 0x4c00 0x4c01 0x1263 };` 相邻无空行（#avc: 注释属于 allow 块不构成分隔） |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | FAIL | 例外项 `pc_only(\`-storage_daemon')` 于 neverallow 主体集内为合法用法（不报违规）；违规三处：① domain.te `pc_only(\`')` 包裹 `neverallow storage_daemon dev_file:blk_file { append relabelfrom relabelto map unlink link rename };`；② storage_daemon.te `pc_only(\`')` 包裹 `allow storage_daemon dev_block_file:blk_file { ioctl };`；③ 同处包裹 `allowxperm storage_daemon dev_block_file:blk_file ioctl { 0x4c00 0x4c01 0x1263 };` |

## ROM 增量估算
- 新增策略规则行（A）：5 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：1 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **400 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S23] base/public/domain.te：`pc_only(\`')` 包裹 `neverallow storage_daemon dev_file:blk_file { append relabelfrom relabelto map unlink link rename };` — 产品宏不应包裹 neverallow → 改为在既有 neverallow 主体集内使用 `-` 例外项
- [S23] storage_daemon.te：`pc_only(\`')` 包裹 `allow storage_daemon dev_block_file:blk_file { ioctl };` 与 `allowxperm storage_daemon dev_block_file:blk_file ioctl { 0x4c00 0x4c01 0x1263 };` — 产品宏不应包裹 allow/allowxperm → 评估是否所有形态都需要该权限；若仅 PC 形态，需评审说明并采用例外项机制
- [S2] base/public/domain.te 拆分新增的 neverallow 延续行 — base/ 变更需 base 专项评审通道确认
- [S19] storage_daemon.te：`allowxperm storage_daemon dev_block_file:blk_file ioctl { 0x4c00 0x4c01 0x1263 };` — 与上一条 allow 间无空行 → 补空行

## 建议修复（SUGGESTION 建议，提交者评估后决策）
- [S4] domain.te 新增 neverallow → 以目标 ref 重跑 scan.py 完成 type 定义位置判定

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S11] base/public/domain.te：neverallow 拆分与例外项调整 → 安全评审确认（既有评审记录是否覆盖拆分后的两条语句）
