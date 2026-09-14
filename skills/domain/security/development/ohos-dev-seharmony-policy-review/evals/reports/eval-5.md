# SELinux 策略提交自检报告

**扫描范围**：evals/files/s23_pc_only_violation.diff（stdin，1 个策略文件）
**diff 性质**：新增权限（2 条新增 allow + 1 条新增 neverallow，含产品宏包裹违规）
**涉及策略文件**：1 个  **新增规则行**：3 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | NA | secret_data 为类型名非品牌词，S1 仅检测品牌类词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | PASS | 策略位于 ohos_policy/test/test/system/，单一目录 |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | SUGGESTION | test.te 新增 `neverallow { domain -test_service } secret_data:file { write };` — stdin 未绑定目标树（引用 domain、secret_data），建议以目标 ref 重跑完成落点判定 |
| S5 | SA 服务 neverallow 看护 | NA | 无新增 SA 服务标签 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | WARNING | 新增 neverallow `neverallow { domain -test_service } secret_data:file { write };` — 单一例外项（-test_service）符合 S11a；新增 neverallow 需安全评审确认 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | WARNING | 2 条新增 allow（secret_data、watch_data）hunk 内均无 #avc: 注释，需补查全文后定级 |
| S18 | allow 落点 system/vendor、public 不放 allow | PASS | allow 位于 system/ 目录 |
| S19 | allow 块间空行分隔 | PASS | 宏块间有空行分隔 |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | FAIL | 三处违规：① `pc_only(\`allow test_service secret_data:file { read write };')` 包裹 allow；② `tablet_only(\`neverallow { domain -test_service } secret_data:file { write };')` 包裹 neverallow（产品宏不应包裹看护语句，其他形态将失去该 neverallow 保护）；③ `watch_only(\`allow test_service watch_data:file { read };')` 包裹 allow——检测覆盖全部 11 个产品宏，非仅 pc/tablet |

## ROM 增量估算
- 新增策略规则行（A）：3 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **300 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S23] test.te：`pc_only(\`')` 包裹 `allow test_service secret_data:file { read write };` — 产品宏仅可作为 `-` 例外项 → 移除包裹，权限若仅 PC 形态需要应在评审中说明并改用例外项机制
- [S23] test.te：`tablet_only(\`')` 包裹 `neverallow { domain -test_service } secret_data:file { write };` — 产品宏不应包裹 neverallow（其他形态将失去看护）→ 移除包裹
- [S23] test.te：`watch_only(\`')` 包裹 `allow test_service watch_data:file { read };` — 同上 → 移除包裹

## 建议修复（SUGGESTION 建议，提交者评估后决策）
- [S4] test.te：`neverallow { domain -test_service } secret_data:file { write };` → 以目标 ref 重跑 scan.py 完成 type 定义位置判定

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S11] test.te：`neverallow { domain -test_service } secret_data:file { write };` → 安全评审确认新增 neverallow 的例外项合理性
- [S17] test.te 两条新增 allow 无 #avc: → 补查全文确认，确认缺失升级为 FAIL
