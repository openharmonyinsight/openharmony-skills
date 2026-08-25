# SELinux 策略提交自检报告

**扫描范围**：evals/files/s23_context_wrapper.diff（stdin，1 个策略文件，F5 宏作用域 context 行追踪回归集）
**diff 性质**：新增权限 + 产品宏包裹（宏开闭为 context 行 / 新增 wrapper 包住既有规则边界场景）
**涉及策略文件**：1 个  **新增规则行**：1 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | NA | secret_data 为类型名非品牌词，S1 仅检测品牌类词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | PASS | 策略位于 ohos_policy/test/test_wrap/system/，单一目录 |
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
| S17 | allow/allowxperm 配 avc 日志注释 | WARNING | `allow wrap_service secret_data:file { read };` hunk 内无 #avc: 注释，需补查全文后定级 |
| S18 | allow 落点 system/vendor、public 不放 allow | PASS | 新增 allow 位于 system/ 目录 |
| S19 | allow 块间空行分隔 | PASS | 宏块间由空行分隔 |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | FAIL | 两处违规：① 既有 `pc_only(\`')` wrapper（开闭均为 context 行）内部新增 `allow wrap_service secret_data:file { read };` — 宏作用域跨 context+added 行追踪，新增规则必须报违规；② 新增 `pc_only(\`')` wrapper 包住既有规则 `allow existing_service existing_target:file { read };` — 新增 wrapper 使既有规则变为形态隔离，同样违规。对照组：既有 watch_only wrapper 仅包裹既有规则（无新增内容）不判违规 |

## ROM 增量估算
- 新增策略规则行（A）：1 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **100 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S23] wrap.te：既有 `pc_only(\`')` wrapper 内新增 `allow wrap_service secret_data:file { read };` — 向既有产品宏 wrapper 内新增规则使该权限仅 PC 形态生效 → 移出 wrapper，按普通 allow 走评审
- [S23] wrap.te：新增 `pc_only(\`')` wrapper 包住既有规则 `allow existing_service existing_target:file { read };` — 新增 wrapper 使既有权限变为形态隔离 → 移除新增 wrapper；如确需形态隔离应整体评审

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S17] wrap.te：`allow wrap_service secret_data:file { read };` 无 #avc: → 补查全文确认，确认缺失升级为 FAIL
