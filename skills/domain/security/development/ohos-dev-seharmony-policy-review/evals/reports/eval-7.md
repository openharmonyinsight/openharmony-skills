# SELinux 策略提交自检报告

**扫描范围**：evals/files/file_contexts_only.diff（stdin，仅 file_contexts 1 个文件）
**diff 性质**：标签映射变更（无策略规则增删）
**涉及策略文件**：1 个  **新增规则行**：0 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | NA | 无策略规则新增 |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | NA | 无新增/修改 neverallow |
| S5 | SA 服务 neverallow 看护 | NA | 无新增 SA 服务标签 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签定义 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | NA | 未修改 neverallow 与白名单 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | NA | 无策略代码段 |
| S17 | allow/allowxperm 配 avc 日志注释 | NA | 无新增 allow/allowxperm |
| S18 | allow 落点 system/vendor、public 不放 allow | NA | 无新增 allow |
| S19 | allow 块间空行分隔 | NA | 无新增 allow |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts（本 diff 为 file_contexts 文件标签映射，非 SA 服务映射） |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | NA | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：0 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **0 B**

说明：file_contexts 变更（`/system/bin/new_binary u:object_r:test_exec:s0`、`/vendor/bin/test_vendor u:object_r:vendor_test_exec:s0`）不涉及策略规则增删，ROM 增量为 0 B；新增类型 test_exec、vendor_test_exec 需确认已在 .te 中定义并评估写执行管控（S7 由语义分析补充确认）。
