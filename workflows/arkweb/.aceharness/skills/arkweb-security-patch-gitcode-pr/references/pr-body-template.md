# PR Body Template

用途：显示在 GitCode PR 页面，承载评审信息、IssueNo、变更描述和验证结果。PR body 不能补救 commit message 缺失的 CVE 或 `Signed-off-by`。

## 字段要求

| 字段 | 要求 |
|------|------|
| GitCode Issue 编号 | 必须写入 `IssueNo` 或“关联的issue” |
| Chromium 漏洞 issue | 必须写完整链接 `https://issues.chromium.org/issues/<issue_id>`，不能只写裸 issue id |
| CVE | 有则写 |
| 修复 PR/CL/commit | 必须写 |
| 引入 bug PR/CL | 可作为证据摘要说明，不能当修复来源 |
| 漏洞详细描述 | 必须中文优先写清楚触发点、漏洞成因、攻击或绕过方式、修复方式 |
| 安全专项分析 | 必须提炼影响分析报告中 `Security impact deep dive` 的公开内容 |
| 影响版本/分支 | 写摘要和依据 |
| ArkWeb 当前工程结论 | 写 affected/unaffected/unknown、影响判定原因和简短源码依据 |
| 责任田 | 必须写责任田、归属理由 |
| 影响特性树 | 必须写受影响特性树路径 |
| 五性/RAM/ROM | 汇总稳定性、安全性、性能、兼容性、业务逻辑正确性、RAM/ROM |
| 测试建议 | 汇总安全回归、兼容回归、自动化建议 |
| 最终工作流结果 | 如当前 issue 存在 `13_final_report.*`，汇总合入、编译、提交、风险结论；不存在则写“未提供当前 issue 最终报告” |
| Signed-off-by | 不需要，属于 commit message |
| 本机路径/`.ace-outputs`/`run-*`/本地归档文件名/token | 禁止 |
| 完整工作流报告 | 禁止 |
| 批量处理信息 | 禁止；PR body 只写当前 Chromium issue 的分析、修复、验证和提交结论 |

## 批量模式边界

如果输入来自批量归档目录，本模板仍然只对应当前一个 Chromium issue，且 PR 页面不能承载批量处理过程。

- 只能读取并提炼当前 issue 目录下的 `03_impact_decision.*`、`04_final_archive.*`、合入/验证/风险/提交产物和当前 issue 的 `13_final_report.*`。
- 不得读取根目录批量最终总结来填充当前 PR body；如只有根目录批量总结而没有当前 issue 的最终报告，则“最终工作流结果”写“未提供当前 issue 最终报告”。
- 不得写入 `00_batch_plan`、`batch_status`、批量统计、批量失败清单、批量处理顺序、其它 issue 的 CVE/commit/PR、overlap 总览或跨 issue 合并建议。
- 如果当前 issue 因文件重叠被阻塞，只能写当前 issue 的阻塞原因和涉及的相对文件；不得列出其它 issue 的提交或 PR 信息。

## 信息来源

PR body 是评审上下文主载体，应优先汇总以下公开内容：

1. 影响判定产物
   - 影响判定结论和判定原因。
   - Issue -> PR/CL -> projectRoot 源码证据链。
   - Chromium 影响版本/分支结论及证据缺口。
   - ArkWeb 当前工程是否受影响及相对源码路径/符号依据。
   - 安全专项分析：必须提炼 `Security impact deep dive` 中的漏洞类别、攻击面、触发条件、可利用性、安全边界影响、未修复后果、本地受影响证据、安全专项测试建议。
   - 责任田、归属原因、影响特性树。
   - 五性、RAM/ROM、风险等级、测试建议。
2. 归档产物
   - 漏洞/缺陷摘要、patch 定位、影响判定摘要、责任田与质量属性。
   - 只能提炼公开结论；不得复制本地 issue 归档目录、`.ace-outputs`、报告路径或 JSON 全文。
3. 最终报告产物
   - 如当前 issue 目录下存在 `13_final_report.*`，汇总自动合入结果、编译验证结果、提交/PR 结果、遗留风险。
   - 如不存在当前 issue 的最终报告，写“未提供当前 issue 最终报告”，不得使用根目录批量最终总结，也不得编造合入/编译/提交状态。
4. 输出中不得出现上述产物文件名、绝对路径、`.ace-outputs` 路径或章节来源标记；只写提炼后的公开结论。

## 填充规则

- `IssueNo` 或“关联的issue”必须填 GitCode Issue 编号，例如 `#12345`。
- `Description` 中文优先，保留完整上游 Chromium issue 链接、漏洞详细描述、安全专项分析、修复 PR/CL 判定依据、影响范围结论、影响判定原因、ArkWeb 当前工程结论、责任田及理由、影响特性树、五性/RAM/ROM 和测试建议。
- `Sig` 按目标仓库要求填写；未知时不要编造，写待确认或沿用仓库默认模板。
- `TDD Self-Verification Results` 只写本工作流实际做过的验证。不要写“未自动合入/未编译测试/未提交上库”作为本流程失败项。

## PR body 模板

```markdown
**IssueNo**: #<gitcode-issue-number>
**Description**:
- CVE: <CVE-YYYY-NNNN or N/A>
- Chromium 漏洞 issue: https://issues.chromium.org/issues/<chromium-issue-id>
- 漏洞类型/风险: <public vulnerability type and risk summary>
- 漏洞详细描述: <触发点/受影响功能、漏洞成因、攻击或绕过方式、安全影响、修复方式>
- 安全专项分析: <漏洞类别、攻击面、触发条件、可利用性、安全边界影响、未修复后果、本地受影响证据、安全专项测试建议>
- 上游修复: <fixing CL/commit and selection reason; explain why this is the fixing PR/CL, not the introducing PR/CL>
- 影响范围: <Chromium affected version/branch conclusion with issue/PR evidence>
- ArkWeb 当前工程结论: <affected|unaffected|unknown>
- 影响判定原因: <why affected/unaffected/unknown; include source-level evidence using relative paths and symbols>
- 责任田: <ownership team>
- 责任田归属理由: <why this team owns the issue>
- 影响特性树: <feature-tree paths>
- 五性/RAM/ROM: <stability/security/performance/compatibility/business logic/RAM/ROM summary>
- 修改范围: <relative changed files and local adaptation summary>
- 测试建议: <security regression, compatibility regression, automation suggestions>
- 最终工作流结果: <summary from current issue 13_final_report if present; otherwise 未提供当前 issue 最终报告>
**Sig**: <SIG or pending confirmation>

### 影响判定依据
- Issue 证据: <full Chromium issue URL, Milestone/Severity/CVE/labels/key issue description>
- 修复 PR/CL 证据: <selected fixing CL/commit/status/branch/patch semantics>
- 本地源码证据: <relative paths, functions, missing or present fix logic>
- Chromium 版本/分支结论: <affected/fixed/unknown with basis>
- 证据缺口: <unknown branch-head/cherry-pick/etc., if any>

### 安全专项分析
- 漏洞类别: <category>
- 攻击面: <attack surface>
- 触发条件: <trigger conditions>
- 可利用性: <exploitability>
- 安全边界影响: <permission/sandbox/privacy/origin boundary impact>
- 未修复后果: <consequences if not fixed>
- 本地受影响证据: <relative code paths/symbols only>
- 安全专项测试建议:
  - <test recommendation 1>
  - <test recommendation 2>

### 责任田与特性树
- 责任田: <ownership team>
- 归属理由: <domain, module, security boundary, API ownership>
- 影响特性树:
  - <feature tree path 1>
  - <feature tree path 2>

### 质量属性与风险
- 稳定性: <yes/no and reason>
- 安全性: <yes/no and reason>
- 性能: <yes/no/low and reason>
- 兼容性: <yes/no and reason>
- 业务逻辑正确性: <yes/no and reason>
- RAM/ROM: <impact and reason>
- 风险等级: <level and reason>

### Feature or Bugfix
- [x] Bugfix

### TDD Self-Verification Results
- [ ] Pass
- [ ] Fail
- [x] Not Involved

### Verification Details
- <actual verification performed or reason not involved>
```

## 脱敏检查

```bash
grep -E '(^|[[:space:]])/(home|tmp|var|mnt)/|\.ace-outputs|run-[0-9]{12,}|00_batch_plan|batch_status|13_batch_summary|批量统计|批量失败|批量处理顺序|overlap 总览|blocked_overlap_conflict|03_impact_decision\.md|04_final_archive\.md|13_final_report\.md|12_submit_result\.md|Source archive file|Input issue archive directory|Workflow execution facts|target subrepo|GITCODE_TOKEN|gitcode-askpass' "$pr_body_file"
```

命中即停止，重新提炼公开摘要。
