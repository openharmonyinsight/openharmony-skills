# 操作执行指南

在 HarmonyOS 设备上执行 UI 操作。

## 必要的导入

```python
from hypium import *
from hypium.model.basic_data_type import UiParam  # 包含 UP, DOWN, LEFT, RIGHT 等常量
```

## 触摸操作

| 操作 | Hypium API | 示例 |
|------|-----------|------|
| 点击 | `driver.touch(target)` | `driver.touch(BY.text("登录"))` |
| 双击 | `driver.touch(target, mode=UiParam.DOUBLE)` | `driver.touch(BY.text("确认"), mode=UiParam.DOUBLE)` |
| 长按 | `driver.touch(target, mode=UiParam.LONG)` | `driver.touch((0.8, 0.9), mode=UiParam.LONG)` |
| 滚动查找点击 | `driver.touch(target, scroll_target=area)` | `driver.touch(BY.text("退出"), scroll_target=BY.type("Scroll"))` |

## 滑动/拖拽操作

| 操作 | Hypium API | 示例 |
|------|-----------|------|
| 方向滑动 | `driver.swipe(UiParam.UP, distance=60)` | `driver.swipe(UiParam.UP, distance=40)` |
| 精确滑动 | `driver.slide((x1,y1), (x2,y2))` | `driver.slide((100, 200), (300, 400))` |
| 区域内滑动 | `driver.slide(start, end, area=target)` | `driver.slide((0, 0), (100, 0), area=BY.type("Slider"))` |

## 输入操作

| 操作 | Hypium API | 示例 |
|------|-----------|------|
| 输入文本 | `driver.input_text(target, text)` | `driver.input_text(BY.type("TextInput"), "hello")` |
| 清除文本 | `driver.clear_text(target)` | `driver.clear_text(BY.type("TextInput"))` |

## 按键操作

| 操作 | Hypium API | 示例 |
|------|-----------|------|
| 返回键 | `driver.press_back()` | 返回上一页 |
| Home键 | `driver.press_home()` | 回到桌面 |
| 电源键 | `driver.press_power()` | 电源操作 |

## 应用操作

| 操作 | Hypium API | 示例 |
|------|-----------|------|
| 启动应用 | `driver.start_app(package_name)` | `driver.start_app("com.ss.android.article.news")` |
| 停止应用 | `driver.stop_app(package_name)` | 停止应用 |

## 等待操作

| 操作 | Hypium API | 示例 |
|------|-----------|------|
| 固定等待 | `driver.wait(seconds)` | `driver.wait(2)` |
| 等待控件 | `driver.wait_for_component(by, timeout)` | 返回控件对象 |

## 定位策略 (BY 选择器)

```python
BY.text("文本内容")      # 按显示文本定位
BY.id("resource_id")    # 按 ID 定位
BY.key("component_key") # 按 key 定位
BY.type("Button")       # 按控件类型定位
BY.description("描述")  # 按描述定位
```

## 方向常量 (UiParam)

```python
from hypium.model.basic_data_type import UiParam

UiParam.UP      # 上滑（手指向上，内容向下滚动）
UiParam.DOWN    # 下滑（手指向下，内容向上滚动）
UiParam.LEFT    # 左滑
UiParam.RIGHT   # 右滑
UiParam.DOUBLE  # 双击
UiParam.LONG    # 长按
UiParam.FAST    # 快速
UiParam.SLOW    # 慢速
```

## 坐标操作

```python
# 绝对坐标
driver.touch((100, 200))

# 比例坐标 (屏幕宽高的比例)
driver.touch((0.5, 0.8))  # 屏幕中心偏下

# 区域内坐标
driver.touch((0.5, 0.5), area=BY.type("Image"))
```

## 步骤转换示例

```python
# 步骤描述
{"action": "click", "target": {"locator": "text", "value": "推荐"}}
# 执行代码
driver.touch(BY.text("推荐"))

# 步骤描述
{"action": "swipe", "swipe_direction": "UP"}
# 执行代码
driver.swipe(UiParam.UP, distance=80)

# 步骤描述
{"action": "input", "target": {"locator": "type", "value": "TextInput"}, "input_value": "今日新闻"}
# 执行代码
driver.input_text(BY.type("TextInput"), "今日新闻")
```

## 输出格式

```json
{
  "success": true,
  "step_id": 1,
  "action": "click",
  "target": "BY.text('登录')",
  "execution_time_ms": 156,
  "screenshot_after": "{PROJECT_ROOT}/output/screenshots/step_001.png",
  "error": null
}
```

## 详细API文档

完整的 Hypium API 文档请参考: `references/hypium_api.md`
