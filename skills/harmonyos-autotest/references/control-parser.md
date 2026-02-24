# 控件解析指南

导出设备当前页面的控件树，并分析控件属性。

## ⚠️ 控件识别流程（必须遵守）

```
┌─────────────────────────────────────────────────────────────┐
│  步骤 1: 导出控件树                                          │
│  - 使用 dumpLayout 导出控件树 JSON                           │
│  - 分析控件树，尝试定位目标控件                               │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  控件树中能否找到目标控件？  │
            └─────────────────────────────┘
                    │           │
                   能           否
                    │           │
                    ▼           ▼
        ┌──────────────┐  ┌──────────────────────────────────┐
        │ 使用定位器    │  │ 步骤 2: 截图 + AI 分析            │
        │ BY.text/key  │  │ 1. 截取当前屏幕                    │
        │ /type/id     │  │ 2. 调用 mcp__4_5v_mcp__analyze_image │
        └──────────────┘  │ 3. AI 返回目标坐标                 │
                          │ 4. 使用 driver.touch((x, y))      │
                          └──────────────────────────────────┘
```

## 截图 + AI 分析命令

```bash
# 1. 截取当前屏幕
hdc shell uitest screenCap -p /data/local/tmp/screen.png
hdc file recv /data/local/tmp/screen.png {PROJECT_ROOT}/output/screenshots/screen.png
```

```python
# 2. 使用 AI 分析截图（调用 mcp__4_5v_mcp__analyze_image）
# prompt 示例: "分析这个截图，找到[搜索输入框]的位置，返回其中心坐标 (x, y)"
```

```python
# 3. 使用 AI 返回的坐标操作
self.driver.touch((x, y))
```

## 导出命令

```bash
hdc shell uitest dumpLayout
hdc file recv /data/local/tmp/layout.json {PROJECT_ROOT}/output/controls/
```

## 字段中英文映射

| 英文 | 中文 | 说明 |
|------|------|------|
| text | 文本 | 控件显示文本 |
| type | 类型 | 控件类型 (Button, Text, Image, List等) |
| id | 标识符 | 控件 resource_id |
| key | 键值 | 用户设置的控件 key |
| bounds | 边界 | 控件边界坐标 [left, top, right, bottom] |
| description | 描述 | 控件描述信息 |
| clickable | 可点击 | **仅供参考**，不准确！ |
| enabled | 可用 | 控件是否可用 |
| scrollable | 可滚动 | 控件是否可滚动 |

> **重要**: `clickable` 字段不准确，只能作为参考！

## 搜索操作的正确流程

> **搜索操作必须先点击搜索输入框，再输入搜索内容，不能直接点击搜索按钮！**

**正确流程**：
1. 先点击搜索输入框（触发输入框获取焦点）
2. 再输入搜索内容
3. 最后点击搜索按钮执行搜索

**控件识别要点**：
- 搜索输入框：类型通常为 `SearchField`、`TextInput`、`TextField`
- 搜索按钮：类型为 `Button`，文本为"搜索"
- 搜索输入框可能没有明显的"搜索"文本，需要通过类型或位置识别

## 输出格式

```json
{
  "success": true,
  "snapshot_path": "{PROJECT_ROOT}/output/controls/controls_zh_20260217.json",
  "controls_count": 125,
  "control_tree": {...},
  "controls_flat": [
    {
      "type": "Button",
      "text": "登录",
      "id": "login_btn",
      "key": "",
      "bounds": [100, 200, 300, 280],
      "locators": {
        "by_text": "BY.text('登录')",
        "by_id": "BY.id('login_btn')",
        "by_type": "BY.type('Button')"
      }
    }
  ]
}
```

## 定位器优先级

为每个可交互控件生成推荐的定位器，按优先级排序：
1. `BY.text("文本")` - 如果 text 非空且唯一
2. `BY.key("key值")` - 如果 key 非空
3. `BY.id("id值")` - 如果 id 非空
4. `BY.type("类型")` - 作为补充
