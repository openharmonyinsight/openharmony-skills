# SELinux 策略提交自检报告

**扫描范围**：evals/files/s21_s22_contexts_whitelist.diff（stdin，service_contexts + 白名单 3 个文件）
**diff 性质**：配置变更（service_contexts 映射 + flex 白名单 + 非 flex 白名单，无策略规则增删）
**涉及策略文件**：3 个  **新增规则行**：0 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | NA | 未新增策略至 base/ |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | NA | 无新增/修改 neverallow |
| S5 | SA 服务 neverallow 看护 | WARNING | service_contexts 新增 `"new_service" u:object_r:sa_new_service:s0` 映射——需确认 sa_new_service 类型已在 .te 中定义且配套看护 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | WARNING | whitelist/other/perm_whitelist.json（非 flex 白名单，perm_group_whitelist.json 不在范围内）新增 `"name": "new_perm"`、`"scope": "global"` 条目——需安全评审确认评审记录 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | NA | 无策略代码段 |
| S17 | allow/allowxperm 配 avc 日志注释 | NA | 无新增 allow/allowxperm |
| S18 | allow 落点 system/vendor、public 不放 allow | NA | 无新增 allow |
| S19 | allow 块间空行分隔 | NA | 无新增 allow |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | WARNING | sepolicy/ohos_policy/startup/init/system/service_contexts 新增映射行 `"new_service" u:object_r:sa_new_service:s0` — 需 samgr 责任田评审（服务名到类型映射、类型定义位置） |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | WARNING | whitelist/flex/test_whitelist.json 新增 `"rule": "allow"`、`"target": "data_file"` 条目 — 需 flex 专项评审（条目必要性、范围最小化、无过宽条目） |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | NA | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：0 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **0 B**

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S21] sepolicy/ohos_policy/startup/init/system/service_contexts：`"new_service" u:object_r:sa_new_service:s0` → samgr 责任田评审
- [S22] whitelist/flex/test_whitelist.json：`"rule": "allow"`、`"target": "data_file"` → flex 专项评审
- [S11c] whitelist/other/perm_whitelist.json：`"name": "new_perm"`、`"scope": "global"` → 安全评审确认（非 flex 白名单修改需已有评审记录）
- [S5] service_contexts 新增 sa_new_service 映射 → 安全评审确认类型定义与看护配套
