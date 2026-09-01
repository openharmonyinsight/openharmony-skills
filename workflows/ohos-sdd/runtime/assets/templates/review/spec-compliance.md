# Spec Compliance Review

> 独立记录实现对 `spec.md` 的逐 AC 符合性。不得用代码质量结论替代规格符合性结论。

## Review Metadata

| Item | Value |
|------|-------|
| Change ID | [issue/draft id] |
| Spec Revision | `[spec.md hash/revision]` |
| Plan Revision | `[execution-plan.md hash/revision]` |
| Base / Head | `[base SHA]` / `[head SHA]` |
| Reviewer / Date | [reviewer] / [date] |

## Verdict

- [ ] Approved
- [ ] Needs Changes
- [ ] Blocked

## AC → Task → Code → Commit → Review

| AC | Task | Code Ref | Commit | Verification Evidence | Result | Gap |
|----|------|----------|--------|-----------------------|--------|-----|
| AC-1 | TASK-1 | `[path:line/symbol]` | `[SHA]` | `verification.md#[anchor]` | PASS/FAIL | [无/缺口] |

## Extra Implementation

| Extra Behavior | File:Line | Risk | Required Action |
|----------------|-----------|------|-----------------|
| [未在 Spec/Plan 声明的行为] | `[path:line]` | [兼容/安全/维护风险] | Remove / Revise Spec / Accept |

## Interpretation Deviations

| Topic | Spec Says | Implementation Does | Required Action |
|-------|-----------|---------------------|-----------------|
| [规则/边界] | [规格原文] | [实际行为] | [修复或修订源头] |

## Spec Quality Boundary

| Check | Result | Evidence |
|-------|--------|----------|
| AC 可从终端用户或 Public/System/InnerAPI 表面观察 | PASS/FAIL | [AC + 返回值/回调/错误码/事件/用户行为] |
| THEN 未混入内部数据结构、状态机、调用链、类/方法、锁或算法 | PASS/FAIL | [spec.md AC 审阅] |
| 变更/废弃 API 当前与目标开放级别一致、完整 | PASS/FAIL/N/A | [API 变更表] |
| API/错误码事实含精确签名/数值、触发条件、外部行为、来源和 AC/验证映射 | PASS/FAIL/N/A | [API 与错误码事实表 + 测试证据] |
| 每个 AC 的测试入口、Red 条件和通过标准真实可执行 | PASS/FAIL | [验证映射 + 测试证据] |

## Anti-Fake Completion Check

| Check | Result | Evidence |
|-------|--------|----------|
| 每个 AC 均有真实 Code Ref 和 Commit | PASS/FAIL | [路径/SHA] |
| 正向、异常、边界和兼容路径均按 Spec 闭合 | PASS/FAIL | [测试/日志] |
| 没有用声明、占位实现或无关测试冒充完成 | PASS/FAIL | [diff/验证] |

## Conclusion

[结论、阻塞项、需回修的 Spec/Plan 项]
