# Excel 报告格式详细说明

本文档包含 Excel 报告生成的详细实现代码和使用指南。

## Excel 表格输出格式

API 文档质量检查结果输出为 **Excel 表格文件（.xlsx）**，支持筛选、排序和批量处理。

### 表格结构

| 列名 | key | 说明 | 示例值 |
|------|-----|------|--------|
| **文件名** | `filename` | 被检查的文件路径 | `docs/apis/system-storage.md` |
| **Designer** | `designer` | 被检查文件的设计人，取文档中的 `<!--Designer: xxx-->` 注释，缺省 `-` | `zhangsan` |
| **问题类型** | `issueType` | 问题所属的质量维度 | `资料正确性`、`资源丰富性/完整性` 等 |
| **问题行号** | `lineNumber` | 问题所在的具体行号 | `42`、`156-160` |
| **问题原因** | `reason` | 问题的详细描述 | `示例代码存在语法错误：未闭合的括号` |
| **建议修改方案** | `suggestion` | 具体的修复建议 | `在第42行添加缺失的右括号 }` |
| **问题严重级别** | `severity` | 优先级分类 | `严重`、`高`、`中`、`低` |

> **数据契约**：Excel 端只消费 `generateReport()` 产出的 `report.excelData`（见 `workflow-details.md` 步骤 5），
> 不得从原始 issue 上直接读字段。历史缺陷就是两端字段名不一致——检查器产出 `line`/`lineEnd`，
> Excel 端读 `issue.lineNumber` 与 `issue.filename`，结果行号恒为 `-`、文件名恒为 `undefined`。
> `lineNumber`/`severity`/`designer` 的换算只发生在 `toExcelRow()` 一处。

## 生成 Excel 报告

```javascript
const EXCEL_COLUMNS = [
  { header: '文件名', key: 'filename', width: 40 },
  { header: 'Designer', key: 'designer', width: 20 },
  { header: '问题类型', key: 'issueType', width: 20 },
  { header: '问题行号', key: 'lineNumber', width: 15 },
  { header: '问题原因', key: 'reason', width: 50 },
  { header: '建议修改方案', key: 'suggestion', width: 50 },
  { header: '问题严重级别', key: 'severity', width: 15 }
];

// 入参是 generateReport() 的返回值（report.excelData 已是标准化行），不是 issuesByDimension
function generateExcelReport(report, outputPath) {
  const rows = report?.excelData;
  if (!Array.isArray(rows)) {
    throw new Error('generateExcelReport: 入参必须是 generateReport() 的返回值（含 excelData 数组）');
  }

  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('API文档检查结果');
  worksheet.columns = EXCEL_COLUMNS;

  // 表头样式
  const headerRow = worksheet.getRow(1);
  headerRow.font = { bold: true, color: { argb: 'FFFFFF' } };
  headerRow.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: '4472C4' } };
  headerRow.alignment = { vertical: 'middle', horizontal: 'center' };

  const visibleKeys = EXCEL_COLUMNS.map(c => c.key);
  rows.forEach((row, index) => {
    // 落盘前逐行校验实际值：定位信息缺失必须报错，不能写成 undefined/'-'
    for (const key of visibleKeys) {
      const value = row[key];
      if (value === undefined || value === null || String(value).trim() === '') {
        throw new Error(`generateExcelReport: 第 ${index + 1} 行 "${key}" 为空（ruleId=${row.ruleId ?? 'unknown'}）`);
      }
    }
    if (row.lineNumber === '-' && row.reason && !/全文|文档级/.test(row.reason)) {
      // 行号未知只在文档级问题上可接受，其余情况说明检查器没有回填 line
      console.warn(`[excel] 第 ${index + 1} 行行号未知（ruleId=${row.ruleId}），请确认检查器是否漏填 line`);
    }

    const excelRow = worksheet.addRow(Object.fromEntries(visibleKeys.map(key => [key, row[key]])));
    excelRow.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: getSeverityColor(row.priority) }
    };
  });

  worksheet.autoFilter = {
    from: { row: 1, column: 1 },
    to: { row: worksheet.rowCount, column: EXCEL_COLUMNS.length }
  };
  worksheet.views = [{ state: 'frozen', ySplit: 1 }];

  return workbook.xlsx.writeFile(outputPath);
}

// 获取严重级别颜色（入参是英文 priority，不是已翻译的中文 severity）
function getSeverityColor(priority) {
  const colors = {
    critical: 'FFC7CE',  // 红色 - 严重
    high: 'FFEB9C',      // 黄色 - 高
    medium: 'C6EFCE',    // 绿色 - 中
    low: 'DDEBF7'        // 蓝色 - 低
  };
  return colors[priority] ?? 'FFFFFF';
}
```

> `translatePriority()`、`formatLineNumber()`、`toExcelRow()` 定义在 `workflow-details.md` 步骤 5，
> 本文档不再重复实现，避免出现两份各自演化的字段换算逻辑。

### 调用顺序

```javascript
const result = executeChecks(parsed, loaded, options);   // 步骤 3：含 ledger 与 sdk 状态
const report = generateReport(result, parsed.fileName);  // 步骤 5：产出 excelData / summary
await generateExcelReport(report, 'api-doc-check-result.xlsx');
```

### 汇总必须呈现的执行状态

`report.summary` 中的 `rulesNotExecuted`、`rulesFailed`、`sdkCheckState`/`sdkCheckReason` 必须写入 Markdown 汇总（见下文模板）。
未执行的检查不是"0 问题"，读者需要能一眼看出哪些结论是没有验证过的。

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
- **质量得分**: {score}

### 执行状态（未执行的检查不计入"0 问题"）
- 已执行规则数: {rulesExecuted}
- 未执行: {rulesNotExecuted}（含原因）
- 执行失败: {rulesFailed}（含原因）
- SDK 源码一致性检查: {sdkCheckState}（{sdkCheckReason}）

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

### Designer
- 取被检文档中的 `<!--Designer: xxx-->` 注释（`extractDesigner()`）
- 文档未标注时填 `-`，不得留空或写 `undefined`

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
