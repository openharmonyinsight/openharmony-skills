# PRD 需求分析报告模板

这是生成 PRD 需求分析报告的模板。

---

```markdown
# PRD 需求分析报告

**生成时间**: {{GENERATION_TIME}}
**分析工具**: PRD Analysis Skill v1.0

---

## 1. 文档信息

| 项目 | 内容 |
|------|------|
| PRD文件 | {{PRD_FILE_NAME}} |
| 文档路径 | {{PRD_FILE_PATH}} |
| 版本号 | {{PRD_VERSION}} |
| 创建日期 | {{PRD_DATE}} |
| 文档作者 | {{PRD_AUTHOR}} |
| 产品名称 | {{PRODUCT_NAME}} |

---

## 2. 需求概述

### 2.1 需求统计

| 统计项 | 数量 | 百分比 |
|--------|------|--------|
| 总需求数 | {{TOTAL_COUNT}} | 100% |
| P0需求 | {{P0_COUNT}} | {{P0_PERCENT}}% |
| P1需求 | {{P1_COUNT}} | {{P1_PERCENT}}% |
| P2需求 | {{P2_COUNT}} | {{P2_PERCENT}}% |

### 2.2 优先级分布

```
{{PRIORITY_DISTRIBUTION_GRAPH}}
```

---

## 3. KEP清单

### 3.1 KEP汇总

| KEP ID | 名称 | 优先级 | 状态 |
|--------|------|--------|------|
{{KEP_TABLE_ROWS}}
| ... | ... | ... | ... |

### 3.2 KEP分类统计

| 分类 | 数量 | KEP列表 |
|------|------|---------|
| 核心功能 (P0) | {{P0_KEP_COUNT}} | {{P0_KEP_LIST}} |
| 重要功能 (P1) | {{P1_KEP_COUNT}} | {{P1_KEP_LIST}} |
| 扩展功能 (P2) | {{P2_KEP_COUNT}} | {{P2_KEP_LIST}} |

### 3.3 KEP完整性验证

| 检查项 | 结果 | 详情 |
|--------|------|------|
| KEP ID格式 | {{KEP_ID_FORMAT_RESULT}} | {{KEP_ID_FORMAT_DETAIL}} |
| KEP命名规范 | {{KEP_NAMING_RESULT}} | {{KEP_NAMING_DETAIL}} |
| 用户故事完整性 | {{USER_STORY_RESULT}} | {{USER_STORY_DETAIL}} |
| 验收标准可测性 | {{ACCEPTANCE_CRITERIA_RESULT}} | {{ACCEPTANCE_CRITERIA_DETAIL}} |

---

## 4. 需求完整性检查

### 4.1 章节完整性

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 产品概述 | {{PRODUCT_OVERVIEW_STATUS}} | {{PRODUCT_OVERVIEW_DETAIL}} |
| 用户角色 | {{USER_ROLES_STATUS}} | {{USER_ROLES_DETAIL}} |
| KEP定义 | {{KEP_DEFINED_STATUS}} | {{KEP_DEFINED_DETAIL}} |
| 功能规格 | {{FUNCTIONAL_SPECS_STATUS}} | {{FUNCTIONAL_SPECS_DETAIL}} |
| 验收标准 | {{ACCEPTANCE_CRITERIA_STATUS}} | {{ACCEPTANCE_CRITERIA_DETAIL}} |
| 非功能需求 | {{NON_FUNCTIONAL_STATUS}} | {{NON_FUNCTIONAL_DETAIL}} |

### 4.2 完整性评分

**总分**: {{COMPLETENESS_SCORE}} / 12

**评级**: {{COMPLETENESS_LEVEL}}

```
{{COMPLETENESS_BAR_GRAPH}}
```

### 4.3 缺失项汇总

{{MISSING_ITEMS_LIST}}

---

## 5. 需求冲突检测

### 5.1 冲突汇总

{{#if CONFLICTS_FOUND}}
| 冲突类型 | 严重程度 | 描述 | 建议 |
|----------|----------|------|------|
{{CONFLICT_TABLE_ROWS}}
| ... | ... | ... | ... |
{{else}}
✅ 未发现明显需求冲突
{{/if}}

### 5.2 详细说明

{{CONFLICT_DETAILS}}

---

## 6. 模块划分建议

### 6.1 建议的服务模块

{{#if MODULE_SUGGESTIONS}}
| 模块名称 | 类型 | 对应KEP | SA分配 |
|----------|------|---------|--------|
{{MODULE_TABLE_ROWS}}
| ... | ... | ... | ... |
{{/if}}

### 6.2 模块依赖关系

```
{{MODULE_DEPENDENCY_GRAPH}}
```

### 6.3 SA分配方案

**推荐方案**: 单SA模式

```
SA ID: {{RECOMMENDED_SA_ID}}
SA Name: {{RECOMMENDED_SA_NAME}}
Process: {{RECOMMENDED_PROCESS_NAME}}

包含模块:
{{SA_MODULE_LIST}}
```

---

## 7. 风险评估

### 7.1 技术风险

| 风险项 | 级别 | 缓解措施 |
|--------|------|----------|
{{TECHNICAL_RISK_ROWS}}

### 7.2 进度风险

| 风险项 | 级别 | 缓解措施 |
|--------|------|----------|
{{SCHEDULE_RISK_ROWS}}

---

## 8. 改进建议

### 8.1 PRD文档改进

{{PRD_IMPROVEMENT_SUGGESTIONS}}

### 8.2 需求澄清

{{CLARIFICATION_NEEDED}}

---

## 9. 附录

### 9.1 完整需求列表

{{FULL_REQUIREMENT_LIST}}

### 9.2 术语表

| 术语 | 定义 |
|------|------|
{{GLOSSARY_ROWS}}

### 9.3 参考资料

- PRD文档: {{PRD_FILE_PATH}}
- 架构设计: {{ARCHITECTURE_DOC_PATH}}
- 功能设计: {{FUNCTION_DESIGN_DOC_PATH}}

---

**报告结束**

*本报告由 PRD Analysis Skill 自动生成*
```

---

## 模板变量参考

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{GENERATION_TIME}}` | 报告生成时间戳 | 2026-01-31 20:00:00 |
| `{{PRD_FILE_NAME}}` | PRD 文件名 | prd_v17.md |
| `{{PRD_VERSION}}` | PRD 版本号 | V17.0 |
| `{{TOTAL_COUNT}}` | 需求总数 | 25 |
| `{{P0_COUNT}}` | P0 需求数量 | 8 |
| `{{P0_PERCENT}}` | P0 百分比 | 32% |
| `{{KEP_TABLE_ROWS}}` | KEP 表格行 | Markdown 表格行 |
| `{{COMPLETENESS_SCORE}}` | 完整性评分 | 10/12 |
| `{{COMPLETENESS_LEVEL}}` | 完整性等级 | 良好 |

---

## JSON 输出格式

使用 `--format json` 时，报告结构如下：

```json
{
  "meta": {
    "generated_at": "2026-01-31T20:00:00Z",
    "tool_version": "1.0.0",
    "prd_file": "prd_v17.md"
  },
  "document_info": {
    "file": "prd_v17.md",
    "path": "/path/to/prd_v17.md",
    "version": "V17.0",
    "date": "2026-01-31",
    "author": "架构组",
    "product": "HM Desktop 7.0"
  },
  "requirements": {
    "total": 25,
    "p0": 8,
    "p1": 12,
    "p2": 5
  },
  "kep_list": [
    {
      "id": "KEP1-01",
      "name": "查看磁盘信息",
      "priority": "P0",
      "user_story": "作为桌面用户...",
      "acceptance_criteria": ["1. 点击后2秒内显示", "2. 显示所有磁盘"]
    }
  ],
  "completeness": {
    "score": 10,
    "max_score": 12,
    "level": "Good",
    "sections": {
      "product_overview": true,
      "user_roles": true,
      "kep_defined": true,
      "functional_specs": true,
      "acceptance_criteria": true,
      "non_functional": false
    },
    "missing": ["非功能需求-安全性部分"]
  },
  "conflicts": [
    {
      "type": "优先级冲突",
      "severity": "Medium",
      "description": "P0功能过多",
      "suggestion": "建议将部分P0降级为P1"
    }
  ],
  "module_suggestions": [
    {
      "name": "DiskInfoService",
      "type": "Information Service",
      "keps": ["KEP1-01", "KEP1-02"],
      "sa_id": 5001
    }
  ]
}
```
