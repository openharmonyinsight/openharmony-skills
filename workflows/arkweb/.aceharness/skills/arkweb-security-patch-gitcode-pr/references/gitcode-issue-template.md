# GitCode Issue Template

用途：在上游 GitCode 仓库创建可关联 PR 的 issue。它不是 Chromium 漏洞 issue，也不能用 Chromium issue id 替代。

## 字段要求

| 字段 | 要求 |
|------|------|
| GitCode Issue 编号 | 创建后产生，用于 PR `IssueNo`/关联 issue |
| Chromium 漏洞 issue | 必须写完整链接 `https://issues.chromium.org/issues/<issue_id>`，只能作为上游漏洞来源，不能只写裸 issue id |
| CVE | 有则写；没有则写 `N/A` |
| 修复 PR/CL/commit | 必须写 |
| 引入 bug PR/CL | 只作为根因/版本证据，不作为修复来源 |
| 漏洞详细描述 | 必须中文优先写清楚触发点、漏洞成因、攻击或绕过方式、修复方式 |
| 安全专项分析 | 必须提炼影响分析报告中 `Security impact deep dive` 的公开内容 |
| 影响版本/分支 | 写摘要和依据 |
| ArkWeb 当前工程结论 | 写 affected/unaffected/unknown 和简短源码依据 |
| 责任田/特性树 | 必须写责任田、归属理由和影响特性树；优先来自 `03_impact_decision.*` |
| 本机路径/`.ace-outputs`/`run-*`/本地归档文件名/token | 禁止 |
| 完整工作流报告 | 禁止 |
| 批量处理信息 | 禁止；只允许写当前 Chromium issue 的分析、修复和验证结论 |

## 批量模式边界

如果输入来自批量归档目录，本模板仍然只对应当前一个 Chromium issue。

- 只能读取并提炼当前 issue 目录下的影响分析、归档、合入、验证、提交材料。
- 不得写入批量计划、批量状态、批量统计、批量失败清单、批量处理顺序、其它 issue 的 CVE/commit/PR、overlap 总览或跨 issue 合并建议。
- 如需要说明文件重叠风险，只能在当前 issue 的本地归档报告中保留；GitCode issue 正文不写批量对比信息。

## 标题模板

有 CVE：

```text
[ArkWeb][安全] <CVE-YYYY-NNNN>: <中文漏洞摘要>
```

无 CVE：

```text
[ArkWeb][安全] Chromium issue <id>: <中文漏洞摘要>
```

## 正文模板

```markdown
## 问题描述

本 issue 用于跟踪 ArkWeb 合入上游 Chromium 安全修复，并关联对应 GitCode PR。

## 漏洞详细描述

- CVE: <CVE-YYYY-NNNN or N/A>
- Chromium 漏洞 issue: https://issues.chromium.org/issues/<chromium-issue-id>
- 漏洞类型/风险: <public vulnerability type and risk summary>
- 触发点/受影响功能: <受影响 API、模块、调用链或功能入口>
- 漏洞成因: <缺失的校验、错误的信任边界或绕过条件>
- 攻击或绕过方式: <公开可描述的攻击路径，不写敏感利用细节>
- 安全影响: <public security impact summary, if security related>
- 修复方式: <上游修复增加的校验、限制或行为变化>

## 安全专项分析

- 漏洞类别: <category>
- 攻击面: <attack surface>
- 触发条件: <trigger conditions>
- 可利用性: <exploitability>
- 安全边界影响: <permission/sandbox/privacy/origin boundary impact>
- 未修复后果: <consequences if not fixed>
- 本地受影响证据: <relative code paths/symbols only>
- 安全专项测试建议: <security regression recommendations>

## 上游修复信息

- 修复 CL/commit: <chromium-cl-or-commit>
- Change-Id: <upstream-change-id-if-any>
- 修复 PR/CL 判定依据: <evidence showing this is the fixing PR/CL, not the introducing PR/CL>

## 影响范围

- Chromium 影响版本/分支: <milestone/branch conclusion with issue/PR evidence>
- ArkWeb 当前工程结论: <affected|unaffected|unknown, with short projectRoot source evidence using relative paths>

## 责任田与影响特性

- 责任田: <ownership team>
- 责任田归属理由: <why this team owns the issue>
- 影响特性树: <feature-tree paths>
- 五性/RAM/ROM: <stability/security/performance/compatibility/business logic/RAM/ROM summary>
- 测试建议: <security regression, compatibility regression, automation suggestions>

## 修改范围

- 修改文件: <relative-file-list>

## 验证

- 验证状态: <pass|not-run|not-involved with reason>
```

## 脱敏检查

```bash
grep -E '(^|[[:space:]])/(home|tmp|var|mnt)/|\.ace-outputs|run-[0-9]{12,}|00_batch_plan|batch_status|13_batch_summary|批量统计|批量失败|批量处理顺序|overlap 总览|blocked_overlap_conflict|03_impact_decision\.md|04_final_archive\.md|13_final_report\.md|12_submit_result\.md|Source archive file|Input issue archive directory|Workflow execution facts|target subrepo|GITCODE_TOKEN|gitcode-askpass' "$issue_body_file"
```

命中即停止，重新提炼公开摘要。
