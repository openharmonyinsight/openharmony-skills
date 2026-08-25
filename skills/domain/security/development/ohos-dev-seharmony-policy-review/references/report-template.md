# SELinux Policy Self-Check Report Template (report body in Chinese)

Output the report in Chinese. Start with the scan scope and diff-nature tone, then the results table, then **actionable items grouped into three disposals**.
**Every disposal item and every FAIL/SUGGESTION/WARNING row in the results table must quote the concrete policy content** (the original diff line) — not just `file:line`. Exception: S1 sensitive words are masked as `***`.
Status tokens: PASS / SUGGESTION / WARNING / FAIL / NA (no emoji).

```
# SELinux 策略提交自检报告

**扫描范围**：<commit/区间说明>
**diff 性质**：<新增权限 / rename 重构 / 删减策略 / 混合（逐行判定基调说明）>
**涉及策略文件**：<N> 个  **新增规则行**：<N> 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 策略、注释不出现敏感词 | PASS/SUGGESTION/WARNING/FAIL/NA | <文件:行> `<原文，敏感词以 *** 匿名>` |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | ... | <文件:行> `<策略原文>` 纯新增/修改既有行 |
| S3 | 新增参数标签 parameter_attr | ... | <文件:行> `<type 原文>` |
| S4 | neverallow 落点（type 全 public→public） | ... | <文件:行> `<neverallow 原文>` type 定义位置结论 |
| S5 | SA 服务 neverallow 看护 | ... | ... |
| S6 | 系统参数禁止三方应用配置 | ... | ... |
| S7 | 写执行目录 neverallow 管控 | ... | ... |
| S9 | debug 功能 debug_only 隔离 | ... | ... |
| S10 | 开发者模式 developer_only 隔离 | ... | ... |
| S11 | 修改 neverallow/非flex白名单需安全评审/命名规范 | ... | ... |
| S12 | sh 主体权限需 DFX+安全评审 | ... | ... |
| S13 | su 主体放行/客体 debug_only | ... | ... |
| S15 | hap 权限范围 | ... | ... |
| S16 | 禁用默认标签 | ... | ... |
| S17 | allow/allowxperm 配 avc 日志注释 | ... | ... |
| S18 | allow 落点 system/vendor、public 不放 allow | ... | ... |
| S19 | allow 块间空行分隔 | ... | ... |
| S20 | appdat 建议改用 normal_app_data | ... | ... |
| S20b | binder 通信权限完整性（binder_call 宏建议） | ... | ... |
| S21 | service_contexts 需 samgr 责任田评审 | ... | <文件> `<映射行原文>` |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | ... | <文件> `<白名单条目原文>` |
| S23 | pc_only/tablet_only/tablet_hybrid_only 仅作为例外项 | ... | <文件:行> `<宏使用原文>` |

## ROM 增量估算
- 新增策略规则行（A）：<N> 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：<N> 条 × 100B（可抵消）
- access_vector 范围变更（M）：<N> 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **<±N> B**

## 必须修复（FAIL 违反，修复后才能合入）
<!-- 三个分组均为实际命中才输出；某组无命中项则整组省略，不输出空标题；每项引用策略原文 -->
- [Sx] <文件:行>：`<策略原文>` — <问题描述> → <修复建议>

## 建议修复（SUGGESTION 建议，提交者评估后决策）
- [Sx] <文件:行>：`<策略原文>` → <优化建议及权衡（如 binder_call 宏非等价替换、ROM 增加约 300B）>

## 需评审决策（WARNING 需确认，结论回填后再合入）
<!-- 仅列需外部组织/责任田确认的项，按「文件修改 → 确认组织」归组，逐项注明确认方并引用原文；
     AI 自验证项（如 S17 #avc: 补查全文）在第二部分完成后直接定级（缺失 → FAIL），不放入本组 -->
- [S3] <文件:行>：`type xxx, parameter_attr;` → init 责任田确认
- [S5/S6/S7] <文件:行>：`<涉及 allow/type 原文>` → 安全评审确认（看护/范围/写执行管控）
- [S11] <文件:行>：`<neverallow/白名单原文>` → 安全评审确认（需已有评审记录）
- [S12] <文件:行>：`<allow sh ... 原文>` → DFX + 安全评审确认
- [S21] <文件>：`<service_contexts 映射行原文>` → samgr 责任田评审
- [S22] <文件>：`<白名单条目原文>` → flex 专项评审
```
