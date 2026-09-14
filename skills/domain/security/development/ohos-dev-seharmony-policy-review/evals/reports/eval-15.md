# SELinux 策略提交自检报告

**扫描范围**：evals/files/r4_regressions.diff（stdin，3 个策略文件，R3/R4 评审反例回归集）
**diff 性质**：新增权限（base/ 纯新增 + 产品宏混排 + violator 命名违规综合场景）
**涉及策略文件**：3 个  **新增规则行**：6 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | FAIL | base/public/multi_hunk.te 第二 hunk 纯新增 `allow fresh_domain data_file:file { read };` — 第一 hunk 的删除行（非同类语句）不跨 hunk 豁免，判纯新增违规 |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | SUGGESTION | x.te 新增 `neverallow foo bar:binder { call transfer };` — 无仓库上下文（引用 foo、bar），建议在 selinux_adapter 仓根重跑完成落点判定 |
| S5 | SA 服务 neverallow 看护 | NA | 无新增 SA 服务标签 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | FAIL | x.te（system/ 分区）两处分区前缀违规：`attribute rgm_violator_bad;`（须 system_violator_ 前缀）、`typeattribute foo violator_bad;`（须 system_violator_ 前缀）——定义位置即作用分区，脚本确定性检查；另新增 neverallow 需安全评审 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 策略代码段未使用默认标签；注释行提及默认标签名称不触发（S16 仅检查代码段） |
| S17 | allow/allowxperm 配 avc 日志注释 | WARNING | 5 条新增 allow 中 4 条 hunk 内无 #avc:（fresh_domain、宏混排行、缩进行、y.te 的 `allow hunk1_service data_file:file { write };`）——x.te hunk 内的 #avc: 注释不跨 hunk/跨文件关联到 y.te，需逐文件补查全文后定级 |
| S18 | allow 落点 system/vendor、public 不放 allow | FAIL | base/public/multi_hunk.te（public/ 目录）新增 `allow fresh_domain data_file:file { read };` — public/ 禁止新增 allow；x.te、y.te 位于 system/ 落点正确 |
| S19 | allow 块间空行分隔 | PASS | 相邻 allow 块间有空行分隔 |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | PASS | `neverallow foo bar:binder { call transfer };` 为 neverallow 语句，S20b 仅针对 allow 语句，不建议宏 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | FAIL | x.te 混排行逐实例判定：`pc_only(\`bad_domain')` 参数不以 `-` 开头判违规；同行 `tablet_only(\`-good_domain')` 为合法例外项不判违规 |

## ROM 增量估算
- 新增策略规则行（A）：8 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **800 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S2] base/public/multi_hunk.te：`allow fresh_domain data_file:file { read };` — 跨 hunk 纯新增落入 base/ → 迁移至 sepolicy/ohos_policy/<子系统>/<组件>/system/
- [S18] base/public/multi_hunk.te：同上 — public/ 禁止新增 allow
- [S11d] x.te：`attribute rgm_violator_bad;` — system/ 分区定义须以 system_violator_ 开头 → 重命名
- [S11d] x.te：`typeattribute foo violator_bad;` — system/ 分区定义须以 system_violator_ 开头 → 重命名
- [S23] x.te：`pc_only(\`bad_domain')` 于 allow 主体集内参数非 `-` 例外项 → 改为 `-bad_domain` 例外形式或移除

## 建议修复（SUGGESTION 建议，提交者评估后决策）
- [S4] x.te：`neverallow foo bar:binder { call transfer };` → 以目标 ref 重跑 scan.py 完成 type 定义位置判定

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S11] x.te：`neverallow foo bar:binder { call transfer };` → 安全评审确认新增 neverallow
- [S17] y.te：`allow hunk1_service data_file:file { write };` 无 #avc:（x.te 的 avc 注释不跨文件关联）→ 补查 y.te 全文确认，确认缺失升级为 FAIL；multi_hunk.te 与 x.te 另 3 条同此处理
