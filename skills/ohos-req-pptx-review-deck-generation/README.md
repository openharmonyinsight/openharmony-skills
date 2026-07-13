# ohos-req-pptx-review-deck-generation

OpenHarmony 需求评审 PPT 生成 Skill。**生成的是 OpenHarmony 专用评审稿**（每页固定打
OpenHarmony logo、套用 OH 评审结构），不面向通用/非 OH 的 PPT 场景。面向维护者的说明
文档（Agent 加载入口是 [`SKILL.md`](SKILL.md)）。

## 这个 Skill 做什么

把需求/方案文档转成一份风格统一的 16:9 PowerPoint 评审稿。核心是 `deckbuilder.py`
———一个 batteries-included 的 `python-pptx` 封装：调用方只提供内容（标题、表格行、
框图节点），所有坐标、配色、字体、间距、箭头绘制都由库内部负责，杜绝手搓 `python-pptx`
导致的版式错乱、框体重叠、"图变成文字列表"等问题。

需求变更评审场景下，按 [`references/requirement-review-template.md`](references/requirement-review-template.md)
的固定 8 页结构生成（封面 → 需求价值描述 → 需求设计方案 → 需求变更背景 →
需求变更影响性分析 → 版本交付计划 → 兼容性分析 → 风险评估）。

## 目录结构

| 路径 | 说明 |
| --- | --- |
| `SKILL.md` | Skill 主文件，Agent 加载入口，含 YAML Front Matter 元数据 |
| `README.md` | 本文件，面向维护者 |
| `scripts/deckbuilder.py` | 核心库；调用方 `from deckbuilder import Deck`（需把 `scripts/` 加入 `sys.path`）|
| `scripts/oh_logo.png` | OpenHarmony logo，自动放置在每页左下角（须与 `deckbuilder.py` 同目录）|
| `references/requirement-review-template.md` | 需求变更评审固定 8 页模板（生成时以此为准） |
| `examples/requirement_review_example.py` | 完整可运行的填充示例脚本 |
| `evals/cases.yaml` | 评测用例索引 |
| `evals/prompts/` | 评测输入 prompt |
| `evals/expected/` | 评测期望判定标准 |

## 本地验证

```bash
python3 -c "import pptx" 2>/dev/null || pip install python-pptx
python3 examples/requirement_review_example.py   # 产出一份示例 deck
```

生成后用 SKILL.md「Verification」一节的 overflow 边界检查做冒烟测试（overflow 必须为 0）。

## 元数据（见 SKILL.md Front Matter）

| 字段 | 值 |
| --- | --- |
| `name` | `ohos-req-pptx-review-deck-generation` |
| `scope` / `stage` | `common` / `requirements` |
| `domain` / `capability` | `pptx` / `review-deck-generation` |
| `status` | `trial` |

命名与放置遵循 OpenHarmony Skills 命名空间与目录放置规范
（`ohos-<stage>-<domain>-<capability>`）。

## 维护要点

- 改样式只动 `scripts/deckbuilder.py`（`PALETTE` / `_style_table` / `_header` / `cover`），
  不要在调用脚本里手算坐标或传 `RGBColor`。
- 配色为浅色主题 + 红色主色：标题用近黑墨色（克制），结论/标题下划线/主箭头用红色（accent）；结构统一柔灰；价值页正文与表格表头用蓝色；`★变更` 框用浅琥珀色高亮，风险用柔砖红。
- 改动后必须跑 `evals/` 用例与 overflow 检查再提交。
