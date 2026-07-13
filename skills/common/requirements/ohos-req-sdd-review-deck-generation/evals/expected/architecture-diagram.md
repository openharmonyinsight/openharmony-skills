# Expected — architecture-diagram

## must（必须满足）

- 用 `architecture_slide`（或在数据流/分层语义下用 `flow_slide` /
  `layered_diagram_slide`）生成真正的框图：圆角矩形节点 + 自动绘制的箭头。
- 模块间连接线是带标注、带方向（`dir="f"` / `"both"`）的，能看出每条链路是什么、朝哪走。
- 变更点用 `"change": True` 标注（渲染为 `★变更` 徽标 + 加粗边框）。
- 边标签框紧贴文字、不遮挡箭头（`_edge_label` 用 `_text_width` 自适应宽度）。
- overflow 边界检查为 0。

## must_not（不允许出现）

- 把交互关系写成 bullet 要点列表 / 纯文字，而不是框 + 箭头。
- 在高层模块交互图里堆内部类名、私有字段（应留给控制面/数据面图与影响表）。
- 手动用 `add_shape` + 英寸坐标摆框、手画箭头。

