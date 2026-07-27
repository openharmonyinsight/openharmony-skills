---
id: issue-N
type: feature | bugfix | decision
title: "[Title]"
spec_schema: ohos-sdd/v1
profile: none | arkweb | arkui | arkgraphic | arkdata | security-sensitive | custom   # 主类型,owner 定;合法集合由 validate 扫描 profiles/* 的 name 得出,保留值 none/custom/security-sensitive
complexity: simple | standard | complex | critical
lineage: new | legacy | migrated | new-on-legacy | bugfix-on-feature
status: draft | approved | implementing | verifying | done | archived
owner: ""
source_issue: ""
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
related: []
related_tasks: []
related_decisions: []
subprofiles: []   # meta-router 推断写回;有值时用 block seq(如 `- component`),无则 []
profile_source: owner   # owner | inferred
code_refs: []   # > 记录涉及的仓路径（如 "openharmony_master/base/web/webview"），不存放源码文件
commits: []     # > 记录实现提交的 commit SHA，而非在 .codespec/ 中放置完整源码
---
