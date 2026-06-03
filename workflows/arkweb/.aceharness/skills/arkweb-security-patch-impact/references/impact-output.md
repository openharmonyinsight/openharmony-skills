# Impact Output

Use this as the portable output contract for `{issue_id}/03_impact_decision.md` and `{issue_id}/03_impact_decision.json`.

## Markdown Sections

For each issue:

1. Input summary
   - issue id
   - selected upstream fix
   - modified files
   - patch files
2. Evidence chain
   - Issue evidence: fields, labels, comments and version signals extracted from `01_issue_analysis.*`
   - PR/CL evidence: selected fix, modified files, actual landing branch, cherry-pick or missing branch evidence from `02_patch_fetch.*`
   - projectRoot code evidence: current ArkWeb files, symbols, call paths, build flags, platform cuts or equivalent implementation under `context.projectRoot`
3. Chromium version impact
   - affected Chromium milestone, branch or version range, or `unknown`
   - evidence from MHTML/issue fields such as `FoundIn-*`, `Milestone`, `Merge-Request-*`, `Merge-Approved-*`, `Merged-*`, `FixedIn-*`
   - PR/CL branch landing evidence, including main commit, cherry-pick commit, release branch, branch-head, or missing evidence
   - conclusion basis and gaps
4. ArkWeb impact conclusion
   - `affected`, `unaffected`, or `unknown`
   - evidence and gaps
   - relationship to the Chromium version impact conclusion
5. Five-dimension analysis
   - stability
   - security
   - performance
   - compatibility
   - business logic correctness
6. Security impact deep dive, required when the issue is security-related
   - vulnerability class
   - attack surface
   - trigger condition
   - exploitability
   - permission, sandbox, privacy, certificate or origin boundary impact
   - consequence if unfixed
   - evidence for affected/unaffected/unknown
   - security-specific test recommendation
7. RAM/ROM impact
8. ownership team
9. impacted feature-tree paths
10. risk level and recommendation
11. test recommendation

## JSON Schema

```json
{
  "issues": [
    {
      "IssueID": "",
      "evidence_chain": {
        "issue_evidence": [],
        "pr_or_cl_evidence": [],
        "project_root_code_evidence": []
      },
      "chromium_version_impact": {
        "affected_versions": [],
        "fixed_versions": [],
        "unknown_versions": [],
        "issue_field_evidence": [
          {
            "field": "FoundIn|Milestone|Merge-Request|Merge-Approved|Merged|FixedIn|Label|Comment",
            "value": "",
            "meaning": "",
            "confidence": "high|medium|low"
          }
        ],
        "upstream_branch_evidence": [
          {
            "source": "Gerrit|Gitiles|PR|commit|patch",
            "url_or_commit": "",
            "branch": "main|refs/branch-heads/*|unknown",
            "landing_state": "landed|cherry-picked|requested|approved|unknown",
            "evidence": ""
          }
        ],
        "conclusion": "",
        "conclusion_basis": []
      },
      "arkweb_impact": "affected|unaffected|unknown",
      "merge_policy": {
        "force_merge": false,
        "impact_mode": "normal|force_affected",
        "source": "requirements|context|impact_mode_argument|default",
        "reason": ""
      },
      "impact_evidence": [],
      "arkweb_vs_chromium_version_relation": "",
      "稳定性相关": false,
      "安全性相关": false,
      "security_impact": {
        "is_security_related": false,
        "vulnerability_class": "",
        "attack_surface": "",
        "trigger_condition": "",
        "exploitability": "high|medium|low|unknown|not_applicable",
        "boundary_impact": {
          "permission": "",
          "sandbox": "",
          "privacy": "",
          "certificate_or_origin": ""
        },
        "unfixed_consequence": "",
        "affected_or_unaffected_evidence": [],
        "security_test_recommendation": ""
      },
      "性能相关": false,
      "兼容性相关": false,
      "业务逻辑正确性": false,
      "是否影响RAM": "是|否",
      "是否影响ROM": "是|否",
      "归属团队": "",
      "归属团队原因": "",
      "影响的特性": [],
      "风险评估级别": "高|中|低",
      "风险评估级别原因": "",
      "兼容性风险级别": "高|中|低",
      "兼容性风险级别原因": "",
      "是否建议保留": "是|否",
      "是否建议保留置信度": 0,
      "是否建议保留原因": "",
      "是否需要测试": "是|否",
      "测试建议": ""
    }
  ]
}
```

## Field Ownership

This stage owns:

- ArkWeb affected/unaffected/unknown conclusion
- Issue, PR/CL and projectRoot code evidence chain
- Chromium affected/fixed/unknown version conclusion and evidence
- PR/CL branch landing evidence
- five-dimension analysis
- security-specific impact analysis for security-related issues
- RAM/ROM decision
- ownership team
- impacted feature-tree paths
- risk level
- keep/drop recommendation
- test recommendation

This stage does not own:

- upstream fix discovery
- patch download
- modified file list generation
