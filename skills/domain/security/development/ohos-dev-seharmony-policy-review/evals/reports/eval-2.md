# SELinux 策略提交自检报告

**扫描范围**：evals/files/rename_refactor_commit.diff（stdin，base/ 与 ohos_policy/ 多文件）
**diff 性质**：rename 重构（属性化）：debug_hap 类型重命名为 debug_hap_attr 属性，既有规则逐行 1:1 替换，非新增权限
**涉及策略文件**：22 个  **新增规则行**：46 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS | 版权年份行属 license 头，按规则跳过；其余新增行无品牌类敏感词 |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | FAIL | base/public/attributes 中 9 条既有属性移动至新文件 attributes_for_hap（rename/整理性质，逐条注明移动来源）；净新增仅 `attribute debug_hap_attr;` 1 条——base 禁止新增属性定义 |
| S3 | 新增参数标签 parameter_attr | NA | 无新增 parameter_attr 标签 |
| S4 | neverallow 落点（type 全 public→public） | SUGGESTION | domain.te 两条 neverallow 为主体替换（debug_hap→debug_hap_attr）；stdin 未绑定目标树，引用列表见扫描输出，建议以目标 ref 重跑完成落点判定 |
| S5 | SA 服务 neverallow 看护 | NA | 无新增 SA 服务标签 |
| S6 | 系统参数禁止三方应用配置 | NA | 无 parameter_service 相关授权 |
| S7 | 写执行目录 neverallow 管控 | NA | 无新增文件标签 |
| S9 | debug 功能 debug_only 隔离 | PASS | debug 相关 allow 均保持在既有 debug_only/developer_only 包裹内（rename 未改变包裹状态） |
| S10 | 开发者模式 developer_only 隔离 | PASS | developer_only 包裹状态未改变 |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | WARNING | domain.te、hiperf.te、lldb.te、native_daemon.te 共 4 处 neverallow 主体由 debug_hap 替换为 debug_hap_attr，需安全评审确认既有评审记录仍然有效 |
| S12 | sh 主体权限需 DFX+安全评审 | NA | 无新增 allow sh 主体（sh.te 仅为客体 rename） |
| S13 | su 主体放行/客体 debug_only | NA | 无 su 主体/客体 |
| S15 | hap 权限范围 | NA | hap 相关规则为 rename 替换，未扩大范围 |
| S16 | 禁用默认标签 | PASS | 未使用默认标签 |
| S17 | allow/allowxperm 配 avc 日志注释 | WARNING | 全部 allow 为 −/+ 1:1 rename 替换（pre-existing）：原行 avc 注释状态为既有状态，本次重构未改变；i18n、sh.te、inputmethod 等处 hunk 内可见既有 #avc: 注释 |
| S18 | allow 落点 system/vendor、public 不放 allow | WARNING | liteos/toybox/public/sh.te 的 `allow sh debug_hap_attr:dir { read open };` 为既有规则的 rename（pre-existing：原 `allow sh debug_hap:dir` 已位于 public/，本次未新引入 public 落点），建议后续 MR 顺带迁移至 system/ |
| S19 | allow 块间空行分隔 | PASS | 脚本标记 18 处 rename 替换行与既有 allow 相邻（如 aa.te `allow debug_hap_attr aa:binder { call };` 紧贴既有 foundation 行）——均为 pre-existing 相邻结构，本次 rename 未改变块间分隔，按 Step 2 rename 基调标注不硬报 |
| S20 | appdat 建议改用 normal_app_data | NA | 无 appdat 客体 |
| S20b | binder 通信权限完整性（binder_call 宏建议） | NA | binder 相关为既有 binder_call 宏调用的参数 rename，无新增手写 call/transfer 组合 |
| S21 | service_contexts 需 samgr 责任田评审 | NA | 未修改 service_contexts |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | NA | 未修改 flex 白名单 |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | PASS | 未新增产品形态宏使用 |

## ROM 增量估算
- 新增策略规则行（A）：57 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：54 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **300 B**

## 必须修复（FAIL 违反，修复后才能合入）
- [S2] sepolicy/base/public/attributes_for_hap：`attribute debug_hap_attr;` — 净新增属性定义落入 base/（其余 9 条为既有属性移动，已按 rename 注明）→ base/ 禁止新增；如确需新增属性，随属性化方案单独评审

## 建议修复（SUGGESTION 建议，提交者评估后决策）
- [S4] domain.te 等 4 处 neverallow：stdin 未绑定目标树无法完成 type 定义位置判定 → 以目标 ref 重跑 scan.py 复核落点

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S11] domain.te / hiperf.te / lldb.te / native_daemon.te：`neverallow ... developer_only(\`-debug_hap_attr ...') ...` — neverallow 主体替换需安全评审确认（既有评审记录是否覆盖本次 rename）
- [S17] 全部 rename allow 行：avc 注释为既有状态（pre-existing），建议在迁移 MR 中保持原注释不动，避免重构引入注释漂移
- [S18] liteos/toybox/public/sh.te：`allow sh debug_hap_attr:dir { read open };` — public/ 落点为既有状态（pre-existing），建议后续 MR 迁移
