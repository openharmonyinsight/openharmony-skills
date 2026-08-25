# SELinux 策略提交自检报告

**扫描范围**：evals/files/r5_regressions.diff（stdin，3 个策略文件，R5-F3/F5/F6 回归集）
**diff 性质**：新增权限（base/ 纯新增 + 缩进 sh/su 语句 + 上下文相邻边界场景）
**涉及策略文件**：3 个  **新增规则行**：8 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | FAIL | probe.te 新增 `allow ***_licensed_dev data_file:file { read };`（品牌词已匿名化）——license 子串出现在真实策略语句中不构成 license 头豁免；同文件顶部的 `# Copyright` / `# Licensed` 注释行按 license 头正常跳过 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | FAIL | base/te/probe.te 纯新增 2 条：`allow license_service data_file:file { read };`（license 子串不再使策略语句被当作 license 头跳过）、`allow ***_licensed_dev data_file:file { read };` |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | SUGGESTION | sh.te 新增 `neverallow { domain -sh } secret_data:file { write };`；stdin 未绑定目标树（引用 domain、secret_data，-sh 例外项已排除），建议以目标 ref 重跑完成落点判定 |
| S5 | SA 服务 neverallow 看护 | NA | 无新增 SA 服务标签 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | WARNING | sh.te 新增 neverallow（单一 -sh 例外项符合 S11a）需安全评审确认 |
| S12 | sh 主体权限需 DFX+安全评审 | WARNING | sh.te 新增 `    allow sh data_file:file { read };` — 缩进的 sh 主体语句同样检测（宏体缩进与顶层一致处理），需 DFX + 安全评审 |
| S13 | su 主体放行/客体 debug_only | FAIL | sh.te 新增 `    allow demo_service su:process { signal };` — su 作为客体且未用 debug_only 隔离（缩进语句同样检测） |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | WARNING | 新增 allow/allowxperm 中仅 adj_new 配有 #avc: 注释；license_service、***_licensed_dev、allow sh、allowxperm sh、allow demo_service su、ctrl_new 共 6 条 hunk 内无 #avc:，需补查全文后定级 |
| S18 | allow 落点 system/vendor、public 不放 allow | FAIL | probe.te 位于 base/te（落点问题由 S2-A 主导判 FAIL）；sh.te、adj.te 位于 system/ 落点正确 |
| S19 | allow 块间空行分隔 | FAIL | 2 处：probe.te `allow ***_licensed_dev data_file:file { read };` 紧贴上一条新增 allow；adj.te `allow adj_new data_file:file { read };` 紧贴上下文 allow（中间仅 #avc: 注释，注释属于 allow 块不构成分隔）。对照组不报：adj.te 空行分隔的 ctrl_new、双上下文相邻的 old_pair_a/old_pair_b |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | PASS | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：8 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **800 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S1] probe.te：`allow ***_licensed_dev data_file:file { read };` — 策略语句中出现品牌类敏感词 → 删除或改写该标识符
- [S2] base/te/probe.te：`allow license_service data_file:file { read };`、`allow ***_licensed_dev data_file:file { read };` — base/ 禁止新增策略 → 迁移至 sepolicy/ohos_policy/<子系统>/<组件>/system/
- [S13] sh.te：`    allow demo_service su:process { signal };` — su 作为客体必须用 debug_only 隔离 → 包裹或移除
- [S18] base/te/probe.te 两条新增 allow — base/te 落点违规（随 S2 一并迁移）
- [S19] probe.te：`allow ***_licensed_dev data_file:file { read };` — 与上一条 allow 间无空行 → 补空行
- [S19] adj.te：`allow adj_new data_file:file { read };` — 紧贴既有 allow 且仅有 #avc: 注释分隔 → 补空行

## 建议修复（SUGGESTION 建议，提交者评估后决策）
- [S4] sh.te：`neverallow { domain -sh } secret_data:file { write };` → 以目标 ref 重跑 scan.py 完成 type 定义位置判定

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S11] sh.te：`neverallow { domain -sh } secret_data:file { write };` → 安全评审确认新增 neverallow 例外项合理性
- [S12] sh.te：`    allow sh data_file:file { read };` → DFX + 安全评审确认
- [S17] 6 条无 #avc: 的新增规则 → 补查全文确认，确认缺失升级为 FAIL
