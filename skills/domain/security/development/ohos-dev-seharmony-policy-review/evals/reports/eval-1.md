# SELinux 策略提交自检报告

**扫描范围**：evals/files/mr8170_pr_scan.diff（stdin，2 个策略文件）
**diff 性质**：新增权限（2 条新增 allow，无对应删除）
**涉及策略文件**：2 个  **新增规则行**：2 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | WARNING | 涉及 busmanager/serial_manager 与 startup/init 两个目录；主体类型 init、serial_service 无交集，需确认是否为同一特性相关变更，无关特性应拆分 MR |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | NA | 无新增/修改 neverallow |
| S5 | SA 服务 neverallow 看护 | NA | 无新增 SA 服务标签或 samgr_class 授权 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签与写执行组合 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | NA | 未修改 neverallow 与白名单 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 新增 allow 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | WARNING | serial_service.te 的 `allow serial_service proc_file:file { open read getattr };` 已配 #avc: 注释（3 条 denied 记录）；init.te 的 `allow init proc_file:dir { getattr open setattr };` hunk 内未见 #avc:，需补查全文后定级 |
| S18 | allow 落点 system/vendor、public 不放 allow | PASS | serial_service.te、init.te 均在 system/ 目录，主体属系统组件，落点正确 |
| S19 | allow 块间空行分隔 | FAIL | init.te 的 `allow init proc_file:dir { getattr open setattr };` 紧贴既有 allow 插入（上下文 allow 与新增 allow 相邻也计入判定），块间无空行 |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | 无 binder call/transfer 授权 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | PASS | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：2 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **200 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S19] init.te：`allow init proc_file:dir { getattr open setattr };` — 紧贴既有 allow 块插入且无空行分隔 → 在新增 allow 块前后补空行

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S2] busmanager/serial_manager 与 startup/init：两个组件目录的变更无共享主体类型，需确认是否为同一特性相关变更；无关特性应拆分独立 MR
- [S17] init.te：`allow init proc_file:dir { getattr open setattr };` hunk 内未见 #avc: 注释，需补查 init.te 全文确认（本报告基于 diff 输入，无法执行 `git show` 全文核查），确认缺失后升级为 FAIL
