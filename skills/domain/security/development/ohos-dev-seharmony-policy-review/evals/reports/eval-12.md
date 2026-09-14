# SELinux 策略提交自检报告

**扫描范围**：evals/files/s20b_binder_call_transfer.diff（stdin，1 个策略文件，binder 两种授权写法）
**diff 性质**：新增权限（两条分离 allow + 一条合并 allow，覆盖 binder call/transfer 全部形态）
**涉及策略文件**：1 个  **新增规则行**：3 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | PASS | 策略位于 ohos_policy/test/test_binder/system/，单一目录 |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | NA | 无新增/修改 neverallow |
| S5 | SA 服务 neverallow 看护 | WARNING | 新增对 sa_target 的 binder 访问（test_service、other_service 两主体），需确认 sa_target 类型定义与看护配套 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | NA | 无 debug 相关权限 |
| S10 | 开发者模式 developer_only 隔离 | NA | 无 developer 相关权限 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | NA | 未修改 neverallow 与白名单 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无 allow sh 主体 |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | 无 hap 相关授权 |
| S16 | 禁用默认标签 | PASS | 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | PASS | 三条新增 allow 上方均配有 #avc: denied 注释（call、transfer、call transfer 各一条） |
| S18 | allow 落点 system/vendor、public 不放 allow | PASS | allow 位于 system/ 目录 |
| S19 | allow 块间空行分隔 | PASS | 三条 allow 块之间均有空行分隔 |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | SUGGESTION | 两种写法均检出：分离写法 `allow test_service sa_target:binder { call };` + `allow test_service sa_target:binder { transfer };`（同主体同客体 call+transfer 齐备）；合并写法 `allow other_service sa_target:binder { call transfer };` — 均建议改用 binder_call 宏补全 binder 通信权限 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | PASS | 未使用产品形态宏 |

## ROM 增量估算
- 新增策略规则行（A）：3 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **300 B**

## 建议修复（SUGGESTION 建议，提交者评估后决策）
- [S20b] binder.te：`allow test_service sa_target:binder { call };` + `allow test_service sa_target:binder { transfer };` → 改用 `binder_call(test_service, sa_target)` 宏（定义于 sepolicy/base/public/glb_scontext.te）。注意宏为非等价替换：展开除 call/transfer 外还包含服务端反向 transfer 与 fd use，ROM 增加约 300B；需结合实际调用链确认是否需要全部宏权限
- [S20b] binder.te：`allow other_service sa_target:binder { call transfer };`（合并写法）→ 同上，改用 `binder_call(other_service, sa_target)` 宏

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S5] binder.te：对 sa_target 的 binder 访问 → 安全评审确认 SA 客体类型定义与看护配套
