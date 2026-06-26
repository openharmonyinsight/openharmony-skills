# Expected — req-review-from-doc

## must（必须满足）

- 使用 `from deckbuilder import Deck`，逐页调用 slide 方法后 `deck.save(...)`；
  不手搓 `python-pptx` 形状、不手算英寸坐标、不传 `RGBColor(...)`。
- 严格遵循 `references/requirement-review-template.md` 的固定 8 段结构（按此顺序）：
  1. 封面
  2. 需求性质与工作量概览
  3. 原始需求描述
  4. 特性及价值点
  5. 系统设计方案（3 页：跨仓模块交互框图 / 控制面·数据面 / 影响分析表）
  6. 兼容性分析
  7. RAM/ROM 评估
  8. 风险 Checklist + 需求拆解列表（工作量评估）
- 含独立的 **工作量评估**（拆解页有 per-task 人月 + 合计行，`highlight_last=True`）
  与 **RAM/ROM 评估** 表。
- 系统设计第 1 页用 `architecture_slide`，是高层模块交互框图（带方向/标注的连接线）。
- 文档中缺失的字段（需求来源/产品、适用地区、工作量人月、开发/设计人员、外部承诺）
  标注 `待评估 / TBD`，并在回复里列回给用户。
- 构建后跑 overflow 边界检查，结果为 0；回复给出输出路径 + 页数。

## must_not（不允许出现）

- 把系统设计页做成纯要点列表（bullet list）而非框图。
- 凭空编造文档没有的技术数字（人月、RAM/ROM 体积）当作确定值。
- 自创大纲、偏离 8 段模板。
