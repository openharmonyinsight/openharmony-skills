# 步骤解析指南

将自然语言测试步骤解析为标准化的 JSON 格式。

## JSON Schema

```json
{
  "test_name": "string - 测试用例名称",
  "description": "string - 测试描述",
  "preconditions": [
    {
      "type": "app_launch|login|state",
      "package": "string - 包名（如需要）",
      "details": "string - 其他详情"
    }
  ],
  "steps": [
    {
      "step_id": 1,
      "action": "click|input|swipe|long_press|double_click|scroll|drag|pinch|key_press",
      "target": {
        "locator": "text|id|key|type|description|bounds|image|coordinate",
        "value": "string - 定位值"
      },
      "position_hint": {
        "direction": "top|bottom|left|right|center|top-right|top-left|bottom-right|bottom-left",
        "order": "first|second|third|...|last|second-to-last|...",
        "description": "string - 原始描述"
      },
      "input_value": "string - 输入内容（仅input操作）",
      "swipe_direction": "UP|DOWN|LEFT|RIGHT（仅swipe操作）",
      "wait_after": "number - 操作后等待时间（秒）",
      "description": "string - 步骤描述"
    }
  ],
  "postconditions": [
    {
      "type": "element_visible|element_gone|text_equals|app_state",
      "target": "string - 目标描述",
      "expected": "string - 预期值"
    }
  ]
}
```

## 操作类型关键词映射

| 中文关键词 | 英文关键词 | Action |
|-----------|-----------|--------|
| 点击、单击、按下 | click, tap, press | click |
| 输入、填写、设置 | input, type, enter | input |
| 滑动、滚动、拖动 | swipe, scroll, drag | swipe |
| 长按 | long press, hold | long_press |
| 双击 | double click, double tap | double_click |
| 拖拽 | drag | drag |
| 捏合、缩放 | pinch, zoom | pinch |
| 按键 | key, press key | key_press |

## 定位策略优先级

1. text（文本）- 优先使用
2. id（标识符）
3. key（键值）
4. type（类型）
5. description（描述）
6. bounds（坐标）- 最后手段

## 方位和顺序关键词

> **重要**: 当步骤中包含方位或顺序关键词时，必须在解析结果中添加 `position_hint` 字段！

### 方位关键词

| 关键词 | 说明 | 定位时的使用方式 |
|--------|------|------------------|
| 顶部、上方 | 页面或容器顶部 | 筛选 y 坐标较小的控件 |
| 底部、下方 | 页面或容器底部 | 筛选 y 坐标较大的控件 |
| 左侧、左边 | 页面或容器左侧 | 筛选 x 坐标较小的控件 |
| 右侧、右边 | 页面或容器右侧 | 筛选 x 坐标较大的控件 |
| 中间、中央 | 页面或容器中央 | 筛选居中的控件 |

### 顺序关键词

| 关键词 | 说明 | 定位时的使用方式 |
|--------|------|------------------|
| 第一个、首个 | 列表或同类控件中的第一个 | 按 y 坐标排序取第一个 |
| 第二个 | 列表或同类控件中的第二个 | 按 y 坐标排序取第二个 |
| 最后一个 | 列表或同类控件中的最后一个 | 按 y 坐标排序取最后一个 |
| 倒数第N个 | 从后往前数第N个 | 按 y 坐标倒序取第N个 |

## 解析示例

### 基本点击操作

```
输入: 点击"推荐"tab
输出:
{
  "step_id": 1,
  "action": "click",
  "target": {"locator": "text", "value": "推荐"},
  "description": "点击推荐tab"
}
```

### 输入操作

```
输入: 在搜索框输入"今日新闻"
输出:
{
  "step_id": 1,
  "action": "input",
  "target": {"locator": "key", "value": "search_input"},
  "input_value": "今日新闻",
  "description": "在搜索框输入内容"
}
```

### 方位关键词示例

```
输入: 点击顶部搜索框
输出:
{
  "step_id": 1,
  "action": "click",
  "target": {"locator": "type", "value": "SearchField"},
  "position_hint": {"direction": "top", "description": "顶部"},
  "description": "点击顶部搜索框"
}
```

### 顺序关键词示例

```
输入: 打开搜索显示出的第一个小程序
输出:
{
  "step_id": 1,
  "action": "click",
  "target": {"locator": "text", "value": "飞猪旅行"},
  "position_hint": {"order": "first", "description": "第一个"},
  "description": "打开第一个小程序"
}
```

### 搜索操作（拆分为多个原子操作）

```
输入: 在顶部搜索框搜索"飞猪旅行"，点击搜索
输出:
[
  {"step_id": 1, "action": "click", "target": {"locator": "type", "value": "SearchField"},
   "position_hint": {"direction": "top", "description": "顶部搜索框"}},
  {"step_id": 2, "action": "input", "target": {"locator": "type", "value": "SearchField"},
   "input_value": "飞猪旅行"},
  {"step_id": 3, "action": "click", "target": {"locator": "text", "value": "搜索"}}
]
```
