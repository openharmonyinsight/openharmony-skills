# Verification

> 独立记录真实执行的验证。Expected Result 必须在执行前定义，Actual Result 必须来自 fresh output；不得只填写“PASS”。

## Verification Metadata

| Item | Value |
|------|-------|
| Change ID | [issue/draft id] |
| Commit / Head | `[SHA]` |
| Environment | [product/board/host/toolchain] |
| Executor / Date | [executor] / [date] |

## Verdict

- [ ] Approved
- [ ] Needs Changes
- [ ] Blocked

## Execution Records

| Task / AC | Command / Evidence | Expected Result | Actual Result | Fresh Evidence | Result |
|-----------|--------------------|-----------------|---------------|----------------|--------|
| TASK-1 / AC-1 | `[精确命令]` | [通过条件、数量、允许告警] | [真实输出摘要] | `[日志/报告路径 + 时间]` | PASS/FAIL/BLOCKED |

## Coverage and Regression

| Scope | Covered? | Evidence | Gap / Follow-up |
|-------|----------|----------|-----------------|
| Positive path | Yes/No | [证据] | [缺口] |
| Error / boundary path | Yes/No | [证据] | [缺口] |
| Compatibility / regression | Yes/No/N/A | [证据] | [缺口或 N/A 理由] |
| Profile-specific validation | Yes/No/N/A | [证据] | [缺口或 N/A 理由] |

## Anti-Fake Completion Check

| Check | Result | Evidence |
|-------|--------|----------|
| 命令与本次变更直接相关 | PASS/FAIL | [映射] |
| Actual Result 来自本次执行而非历史输出 | PASS/FAIL | [时间/日志] |
| 失败、跳过和环境阻塞均已显式记录 | PASS/FAIL | [记录] |
| 未用空测试集、过滤错误或仅编译成功替代行为验证 | PASS/FAIL | [输出] |

## Code-to-Spec Consistency Conclusion

[代码与规格是否一致、剩余验证风险、是否允许进入 GC]
