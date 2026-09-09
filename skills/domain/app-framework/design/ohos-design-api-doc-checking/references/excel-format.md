# Excel 报告格式详细说明

本文档包含 Excel 报告生成的详细实现代码和使用指南。

## Excel 表格输出格式

API 文档质量检查结果输出为 **Excel 表格文件（.xlsx）**，支持筛选、排序和批量处理。

### 表格结构

| 列名 | 说明 | 示例值 |
|------|------|--------|
| **文件名** | 被检查的文件路径 | `docs/apis/system-storage.md` |
| **问题类型** | 问题所属的质量维度 | `资料正确性`、`资源丰富性/完整性` 等 |
| **问题行号** | 问题所在的具体行号 | `42`、`156-160` |
| **问题原因** | 问题的详细描述 | `示例代码存在语法错误：未闭合的括号` |
| **建议修改方案** | 具体的修复建议 | `在第42行添加缺失的右括号 }` |
| **问题严重级别** | 优先级分类 | `严重`、`高`、`中`、`低` |

## 生成 Excel 报告

```javascript
function generateExcelReport(issuesByDimension, outputPath) {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('API文档检查结果');
  
  // 定义表头
  worksheet.columns = [
    { header: '文件名', key: 'filename', width: 40 },
    { header: '问题类型', key: 'issueType', width: 20 },
    { header: '问题行号', key: 'lineNumber', width: 15 },
    { header: '问题原因', key: 'reason', width: 50 },
    { header: '建议修改方案', key: 'suggestion', width: 50 },
    { header: '问题严重级别', key: 'severity', width: 15 }
  ];
  
  // 设置表头样式
  const headerRow = worksheet.getRow(1);
  headerRow.font = { bold: true, color: { argb: 'FFFFFF' } };
  headerRow.fill = {
    type: 'pattern',
    pattern: 'solid',
    fgColor: { argb: '4472C4' }
  };
  headerRow.alignment = { vertical: 'middle', horizontal: 'center' };
  
  // 填充数据
  const allIssues = flattenIssues(issuesByDimension);
  allIssues.forEach(issue => {
    const row = worksheet.addRow({
      filename: issue.filename,
      issueType: issue.type,
      lineNumber: issue.lineNumber || '-',
      reason: issue.description,
      suggestion: issue.suggestedFix,
      severity: translatePriority(issue.priority)
    });
    
    // 根据严重级别设置行颜色
    const severityColor = getSeverityColor(issue.priority);
    row.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: severityColor }
    };
  });
  
  // 添加筛选器
  worksheet.autoFilter = {
    from: { row: 1, column: 1 },
    to: { row: worksheet.rowCount, column: 6 }
  };
  
  // 冻结首行
  worksheet.views = [{ state: 'frozen', ySplit: 1 }];
  
  return workbook.xlsx.writeFile(outputPath);
}

// 获取严重级别颜色
function getSeverityColor(priority) {
  const colors = {
    critical: 'FFC7CE',  // 红色 - 严重
    high: 'FFEB9C',      // 黄色 - 高
    medium: 'C6EFCE',    // 绿色 - 中
    low: 'DDEBF7'        // 蓝色 - 低
  };
  return colors[priority] || 'FFFFFF';
}

// 优先级翻译
function translatePriority(priority) {
  const map = {
    critical: '严重',
    high: '高',
    medium: '中',
    low: '低'
  };
  return map[priority] || priority;
}

// 扁平化问题数据
function flattenIssues(issuesByDimension) {
  const allIssues = [];
  for (const issues of Object.values(issuesByDimension)) {
    allIssues.push(...issues);
  }
  return allIssues;
}
```

## Excel 表格使用指南

### 1. 筛选功能
- 点击表头的下拉箭头可筛选特定类型的问题
- 可组合多个条件进行复杂筛选（如：严重级别="严重" 且 问题类型="资料正确性"）

### 2. 排序功能
- 点击列标题可按该列升序/降序排序
- 建议排序方式：
  - 按「问题严重级别」排序：优先处理严重问题
  - 按「文件名」排序：集中处理同一文件的问题
  - 按「问题类型」排序：批量处理同类问题

### 3. 条件格式说明
| 颜色 | 严重级别 | 处理建议 |
|------|----------|----------|
| 🔴 红色背景 | 严重 | 合并前必须修复 |
| 🟡 黄色背景 | 高 | 强烈建议修复 |
| 🟢 绿色背景 | 中 | 建议修复 |
| 🔵 蓝色背景 | 低 | 可选改进 |

## Markdown 汇总报告（可选）

除 Excel 表格外，可同时生成简要的 Markdown 汇总报告：

```markdown
## API 文档质量检查汇总

### 统计概览
- **检查文件数**: {fileCount}
- **发现问题数**: {totalIssues}
- 严重: {critical} | 高: {high} | 中: {medium} | 低: {low}

### 详细结果
Excel 文件: `{outputPath}`

### 问题分布（按维度）
| 维度 | 问题数 | 占比 |
|------|--------|------|
| 资源易找性 | {count} | {percentage} |
| 资源丰富性/完整性 | {count} | {percentage} |
| ... | ... | ... |
```

## 数据格式规范

### 文件名
- 使用相对于项目根目录的相对路径
- 示例：`docs/apis/@ohos.storage.d.ts.md`

### 问题行号
- 单行：`42`
- 多行范围：`156-160`
- 多个不连续行：`42, 58, 90`
- 未知行号：`-`

### 问题类型（7大维度）
- `资源易找性`
- `资源丰富性/完整性`
- `资料正确性`
- `资源清晰易懂`
- `能力有效性`
- `能力易用性`
- `能力丰富性`

### 问题严重级别
- `严重` (critical) - 会导致功能异常
- `高` (high) - 严重影响体验
- `中` (medium) - 一般问题
- `低` (low) - 轻微问题
