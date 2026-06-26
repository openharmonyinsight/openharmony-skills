# Expected — wide-table

## must（必须满足）

- 用 `table_slide(title, headers, rows, col_widths=..., highlight_last=True)`。
- `col_widths` 作为相对权重传入，由库自动缩放占满可用宽度、不溢出画布。
- 合计行通过 `highlight_last=True` 体现：加粗 + 浅蓝底色，与浅蓝表头呼应。
- 表格网格线为柔和蓝灰（非刺眼纯黑），与浅色主题协调。
- 行数较多时字号自动收缩；overflow 边界检查为 0。

## must_not（不允许出现）

- 列宽写死英寸导致最后一列出血 / 文字被截。
- 手动逐格设置边框/底色、手算行高。
- 把表格拆成多个文本框拼接。
