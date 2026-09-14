# SELinux 策略提交自检报告

**扫描范围**：evals/files/mixed_sepolicy_whitelist_contexts.diff（stdin，sepolicy + whitelist/flex + 根级 service_contexts 共 3 个文件）
**diff 性质**：新增权限 + 配置变更（2 条新增 allow、flex 白名单与 service_contexts 新文件）
**涉及策略文件**：3 个  **新增规则行**：2 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | PASS | 策略位于 ohos_policy/test/test_system/system/ 单一目录，未触碰 base/ |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | NA | 无新增/修改 neverallow |
| S5 | SA 服务 neverallow 看护 | WARNING | service_contexts 新增 `"test_service" u:object_r:sa_test_service:s0` 映射——需确认 sa_test_service 类型已在 .te 中定义且配套看护 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | NA | 未修改非 flex 白名单（本 diff 的白名单为 whitelist/flex，归 S22） |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | PASS | `allow test_service data_file:file { read };` 与 `allow test_service data_file:file { write };` 上方均配有 #avc: denied 注释 |
| S18 | allow 落点 system/vendor、public 不放 allow | PASS | test.te 位于 system/ 目录，落点正确 |
| S19 | allow 块间空行分隔 | PASS | 两个 allow 块之间有空行分隔 |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | WARNING | 根级 service_contexts 新增映射行 `"test_service" u:object_r:sa_test_service:s0` — 需 samgr 责任田评审（服务名到类型映射、类型定义位置） |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | WARNING | whitelist/flex/test_whitelist.json 新增条目 `"domain": "test_service"`、`"rule": "allow"` — 需 flex 专项评审（条目必要性、范围最小化、无过宽条目） |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | PASS | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：2 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **200 B**

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S21] service_contexts：`"test_service" u:object_r:sa_test_service:s0` → samgr 责任田评审
- [S22] whitelist/flex/test_whitelist.json：`"domain": "test_service"`、`"rule": "allow"` → flex 专项评审
- [S5] service_contexts 新增 sa_test_service 映射 → 安全评审确认类型定义与看护配套
