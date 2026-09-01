# Code Quality Review

> 独立记录已通过 Spec Compliance 的实现质量。若 Spec Compliance 未通过，本审查不得给出最终 Approved。

## Review Metadata

| Item | Value |
|------|-------|
| Change ID | [issue/draft id] |
| Base / Head | `[base SHA]` / `[head SHA]` |
| Reviewed Scope | `[commit / PR / diff range]` |
| Reviewer / Date | [reviewer] / [date] |

## Verdict

- [ ] Approved
- [ ] Needs Changes
- [ ] Blocked

## Plan Scope vs Actual Code Scope

| Task | Planned Files/Symbols | Actual Files/Symbols | Commit | Deviation | Result |
|------|-----------------------|----------------------|--------|-----------|--------|
| TASK-1 | `[planned path:symbol]` | `[actual path:symbol]` | `[SHA]` | 无/[重新审批记录] | PASS/FAIL |

## Findings

| Severity | File:Line | Finding | Impact | Required Fix |
|----------|-----------|---------|--------|--------------|
| Blocker/Major/Minor | `[path:line]` | [问题] | [影响] | [修复要求] |

## Quality Dimensions

| Dimension | Result | Evidence |
|-----------|--------|----------|
| Architecture / layering | PASS/FAIL/WARN | [证据] |
| Code-fact baseline / existing pattern alignment | PASS/FAIL/WARN/N/A | [文件:行、模式引用和偏差] |
| Class/interface structure matches approved design | PASS/FAIL/WARN/N/A | [类图、实际类型关系、ADR] |
| API / compatibility | PASS/FAIL/WARN | [证据] |
| State ownership / lifecycle / invariants | PASS/FAIL/WARN/N/A | [STATE-*、INV-*、创建/清理、AC/Task/验证] |
| Error handling / concurrency / security | PASS/FAIL/WARN/N/A | [证据] |
| Build / generated files | PASS/FAIL/WARN/N/A | [生成源、命令、结果] |
| Test quality / maintainability | PASS/FAIL/WARN | [证据] |

## Conclusion

[优点、阻塞问题、建议和最终判断]
