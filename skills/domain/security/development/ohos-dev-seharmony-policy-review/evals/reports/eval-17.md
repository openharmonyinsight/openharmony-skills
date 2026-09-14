# SELinux 策略提交自检报告

**扫描范围**：evals/files/s11d_violater_s4_exception.diff（stdin，1 个策略文件，violater 拼写变体与 S4 例外项排除回归集）
**diff 性质**：新增 violator 定义与 neverallow（命名规范与引用收集回归场景）
**涉及策略文件**：1 个  **新增规则行**：2 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | PASS | 策略位于 ohos_policy/test/comp/system/，单一目录 |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | SUGGESTION | probe.te 两条新增 neverallow；stdin 未绑定目标树，引用收集（- 例外项排除后）为 dev_file, domain 与 dev_file, domain, foo_type——foo_type 正常收集，例外项不进入引用列表；建议以目标 ref 重跑完成落点判定 |
| S5 | SA 服务 neverallow 看护 | NA | 无新增 SA 服务标签 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | FAIL | 两处命名前缀违规：`typeattribute foo rgm_violater_bar;`（violater 为上游真实拼写变体，同样检测；命名未使用文档规定前缀 violator_/rgm_violator_/system_violator_/vendor_violator_）、`attribute bad_violator_x;`（violator 出现在名称中部，必须为前缀）；另新增 neverallow 需安全评审 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | NA | 无新增 allow/allowxperm |
| S18 | allow 落点 system/vendor、public 不放 allow | NA | 无新增 allow |
| S19 | allow 块间空行分隔 | NA | 无新增 allow |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | PASS | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：5 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **500 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S11d] probe.te：`typeattribute foo rgm_violater_bar;` — violater 拼写变体同样受命名规范约束，必须使用文档规定前缀（rgm_violator_ 前缀为 rgm_violator_bar 而非 rgm_violater_bar）→ 重命名
- [S11d] probe.te：`attribute bad_violator_x;` — violator 必须为名称前缀，不得出现在中部 → 重命名为 violator_x 形式并确认分区前缀

## 建议修复（SUGGESTION 建议，提交者评估后决策）
- [S4] probe.te 两条 neverallow → 以目标 ref 重跑 scan.py 完成 type 定义位置判定

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S11] probe.te：两条新增 neverallow → 安全评审确认（violator 豁免项与看护配套，S11b 看护完整性并入安全评审确认）
