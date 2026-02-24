# UI 比对指南 (UI Comparison Guide)

## 概述

UI 比对者（UI Comparator）负责比对 Android 和 HarmonyOS 应用的 UI 界面，确保视觉和交互一致性。

## 比对模式

### 模式1：自动化 UI 比对（推荐）

使用 Hypium 自动化框架进行实时 UI 比对：

```bash
python scripts/compare_ui_auto.py --android <android-package> --harmonyos <harmonyos-package>
```

**自动化流程**：

1. **启动迁移前 Android 应用**：
   ```bash
   hdc shell aa start -b <android-package> -a <android-activity>
   ```
   示例：
   ```bash
   hdc shell aa start -b com.simplemobiletools.gallery.pro -a com.simplemobiletools.gallery.pro.activities.SplashActivity.Orange
   ```

2. **等待应用启动完成**（建议等待 3-5 秒）

3. **截取 Android 应用首界面截图**

4. **使用 Hypium 进行组件交互测试**（可选）：
   - 查找可点击组件
   - 执行点击操作
   - 截取操作后的界面

5. **关闭 Android 应用**

6. **启动迁移后鸿蒙应用**：
   ```bash
   hdc shell aa start -b <harmonyos-bundle> -a <ability>
   ```
   示例：
   ```bash
   hdc shell aa start -b com.example.myapplication -a EntryAbility
   ```

7. **重复步骤 2-4**，对鸿蒙应用执行相同操作

8. **比对两个应用的截图**，生成差异报告

**Hypium 自动化示例代码**：

```python
from hypium import UiDriver, BY, UiParam
from hypium.action.app.launcher import Launcher
import time

class UIComparator:
    def __init__(self):
        self.driver = UiDriver.connect()
        self.screenshots = {
            "android": {},
            "harmonyos": {}
        }

    def start_android_app(self, package, activity):
        """启动 Android 应用"""
        import subprocess
        cmd = f"hdc shell aa start -b {package} -a {activity}"
        subprocess.run(cmd, shell=True)
        time.sleep(3)  # 等待应用启动

    def start_harmonyos_app(self, bundle, ability):
        """启动鸿蒙应用"""
        import subprocess
        cmd = f"hdc shell aa start -b {bundle} -a {ability}"
        subprocess.run(cmd, shell=True)
        time.sleep(3)  # 等待应用启动

    def take_screenshot(self, app_type, screen_name):
        """截屏并保存"""
        filename = f"screenshots/{app_type}_{screen_name}.png"
        self.driver.capture_screen(filename)
        return filename

    def find_and_click_components(self):
        """查找可点击组件并执行点击操作"""
        # 查找所有可点击组件
        clickable_components = self.driver.find_all_components(BY.clickable(True))

        # 对前几个组件执行点击
        for i, component in enumerate(clickable_components[:3]):
            try:
                # 获取组件信息
                text = component.get_text() or f"component_{i}"
                component.click()
                time.sleep(1)
                # 截图记录点击后的状态
                self.take_screenshot("after_click", text)
                # 返回
                self.driver.press_back()
                time.sleep(1)
            except Exception as e:
                print(f"点击组件失败: {e}")

    def compare_screenshots(self, android_screenshot, harmonyos_screenshot):
        """比对两个截图的差异"""
        from hypium.host.cv import CV
        # 使用图像对比算法
        diff_result = CV.compare_image(android_screenshot, harmonyos_screenshot)
        return diff_result

    def run_comparison(self, android_pkg, android_activity, harmonyos_bundle, harmonyos_ability):
        """执行完整的 UI 比对流程"""
        # 1. 启动 Android 应用
        self.start_android_app(android_pkg, android_activity)
        android_main = self.take_screenshot("android", "main")

        # 2. 执行组件交互测试
        self.find_and_click_components()

        # 3. 关闭 Android 应用
        Launcher.clear_recent_task(self.driver)

        # 4. 启动鸿蒙应用
        self.start_harmonyos_app(harmonyos_bundle, harmonyos_ability)
        harmonyos_main = self.take_screenshot("harmonyos", "main")

        # 5. 执行组件交互测试
        self.find_and_click_components()

        # 6. 比对截图
        diff = self.compare_screenshots(android_main, harmonyos_main)

        # 7. 关闭驱动
        self.driver.close()

        return diff

# 使用示例
comparator = UIComparator()
result = comparator.run_comparison(
    android_pkg="com.simplemobiletools.gallery.pro",
    android_activity="com.simplemobiletools.gallery.pro.activities.SplashActivity.Orange",
    harmonyos_bundle="com.example.myapplication",
    harmonyos_ability="EntryAbility"
)
```

### 模式2：布局文件比对

比对 Android XML 布局与 HarmonyOS ETS 布局：

```bash
python scripts/compare_ui.py --layout <android-xml-dir> <harmonyos-ets-dir>
```

### 模式3：截图比对

比对 Android 和 HarmonyOS 的界面截图：

```bash
python scripts/compare_ui.py --screenshot <android-screenshots> <harmonyos-screenshots>
```

## 组件映射表

### 布局容器映射

| Android | HarmonyOS | 说明 |
|---------|-----------|------|
| LinearLayout(vertical) | Column | 垂直排列 |
| LinearLayout(horizontal) | Row | 水平排列 |
| FrameLayout | Stack | 层叠布局 |
| RelativeLayout | RelativeContainer | 相对定位 |
| ConstraintLayout | RelativeContainer | 约束布局 |
| ScrollView | Scroll | 滚动容器 |
| NestedScrollView | Scroll | 嵌套滚动 |
| ViewPager | Swiper | 滑动翻页 |
| ViewPager2 | Swiper | 滑动翻页 |

### 列表组件映射

| Android | HarmonyOS | 说明 |
|---------|-----------|------|
| RecyclerView | List | 垂直列表 |
| RecyclerView(Grid) | Grid | 网格列表 |
| ListView | List | 列表（旧版） |
| GridView | Grid | 网格（旧版） |

### 基础组件映射

| Android | HarmonyOS | 关键属性对比 |
|---------|-----------|-------------|
| TextView | Text | text -> text, textSize -> fontSize |
| EditText | TextInput | hint -> placeholder |
| Button | Button | 事件处理方式不同 |
| ImageView | Image | src -> src |
| CheckBox | Checkbox | checked -> selected |
| RadioButton | Radio | 需配合 Radio Group |
| Switch | Toggle | checked -> isChecked |
| ProgressBar | Progress | 进度条 |
| SeekBar | Slider | 滑块 |
| RatingBar | Rating | 评分 |

### 特殊组件映射

| Android | HarmonyOS | 迁移要点 |
|---------|-----------|----------|
| WebView | Web | 需配置 WebController |
| VideoView | Video | 需配置视频控制器 |
| SearchView | Search | 事件绑定方式不同 |
| CalendarView | CalendarPicker | 日期选择器 |
| DatePicker | DatePicker | 需处理回调 |
| TimePicker | TimePicker | 时间选择器 |
| TabLayout | Tabs | 配合 TabContent 使用 |
| BottomNavigationView | Tabs | 底部导航 |
| Toolbar | Navigation | 顶部导航 |
| CardView | Column + 样式 | 需添加圆角阴影 |
| FloatingActionButton | Button | 设置圆形样式 |

## 样式属性映射

### 尺寸属性

| Android | HarmonyOS | 示例 |
|---------|-----------|------|
| layout_width | width | match_parent -> '100%', wrap_content -> 'auto' |
| layout_height | height | 同上 |
| layout_margin | margin | {left, top, right, bottom} |
| padding | padding | 同上 |
| minWidth | minWidth | - |
| minHeight | minHeight | - |
| maxWidth | maxWidth | - |
| maxHeight | maxHeight | - |

### 背景和颜色

| Android | HarmonyOS | 说明 |
|---------|-----------|------|
| background | .backgroundColor() | 颜色背景 |
| backgroundTint | .backgroundColor() | 着色 |
| foreground | - | 前景色较少使用 |
| alpha | .opacity() | 透明度 |
| visibility | .visibility() | Visibility.Visible/Hidden |

### 文本样式

| Android | HarmonyOS | 示例 |
|---------|-----------|------|
| textColor | .fontColor() | 文字颜色 |
| textSize | .fontSize() | 字号，单位 'fp' |
| textStyle | .fontWeight() | bold -> FontWeight.Bold |
| fontFamily | .fontFamily() | 字体 |
| textAlign | .textAlign() | 对齐方式 |
| lineHeight | .lineHeight() | 行高 |
| maxLines | .maxLines() | 最大行数 |
| ellipsize | .textOverflow() | 省略方式 |

### 边框和圆角

| Android | HarmonyOS | 示例 |
|---------|-----------|------|
| cornerRadius | .borderRadius() | 圆角 |
| strokeWidth + strokeColor | .border() | 边框 |
| elevation | .shadow() | 阴影 |

### 布局约束

| Android | HarmonyOS | 说明 |
|---------|-----------|------|
| gravity | .align() | 对齐方式 |
| layout_gravity | - | 父容器决定 |
| layout_weight | flexGrow/flexShrink | 权重分配 |
| layout_centerInParent | align | 居中 |

## 比对检查清单

### 布局结构检查

- [ ] 页面层级结构是否一致
- [ ] 组件排列顺序是否正确
- [ ] 容器类型是否正确映射
- [ ] 嵌套层级是否合理

### 视觉样式检查

- [ ] 颜色是否一致（主题色、背景色、文字色）
- [ ] 字体大小是否一致
- [ ] 间距是否一致（margin、padding）
- [ ] 圆角、边框是否一致
- [ ] 阴影效果是否一致

### 尺寸适配检查

- [ ] 不同屏幕尺寸下的显示
- [ ] 横竖屏切换适配
- [ ] 折叠屏适配（如适用）

### 交互元素检查

- [ ] 按钮样式是否一致
- [ ] 输入框样式是否一致
- [ ] 列表项样式是否一致
- [ ] 开关、选择器等是否一致

### 动画效果检查

- [ ] 页面转场动画
- [ ] 列表滑动动画
- [ ] 按钮点击反馈
- [ ] 加载动画

## 截图比对注意事项

### 截图命名规范

建议使用相同的命名规范：

```
login_page.png          # Android
login_page.png          # HarmonyOS

main_activity.png
main_page.png

settings_fragment.png
settings_page.png
```

### 截图要求

| 要求 | 说明 |
|------|------|
| 分辨率 | 建议使用相同设备或模拟器分辨率 |
| 状态栏 | 统一是否包含状态栏 |
| 比例 | 使用相同的屏幕比例 |
| 主题 | 确保使用相同的主题（深色/浅色） |

### 差异阈值

| 差异类型 | 可接受范围 |
|---------|-----------|
| 像素级差异 | < 5% (渲染差异) |
| 布局位置 | < 10px |
| 颜色 | Delta E < 3 |
| 尺寸 | < 3% |

## 常见 UI 迁移问题

### 问题1：dp 到 vp 转换

Android 使用 dp，HarmonyOS 使用 vp，两者接近但不完全相同：

```
1 dp ≈ 1 vp (在 160dpi 下)
1 dp ≈ 0.5 vp (在 320dpi 下)
```

建议直接使用数值，HarmonyOS 会自动适配。

### 问题2：颜色资源

Android 颜色定义在 `colors.xml`：

```xml
<color name="primary">#FF6200</color>
```

HarmonyOS 在 `resources/base/element/color.json`：

```json
{
  "color": [
    {"name": "primary", "value": "#FF6200"}
  ]
}
```

使用方式：

```typescript
.textAlign(TextAlign.Center)
.fontColor($r('app.color.primary'))
```

### 问题3：字符串资源

Android 在 `strings.xml`，HarmonyOS 在 `resources/base/element/string.json`。

### 问题4：列表性能

RecyclerView 使用 ViewHolder 复用，HarmonyOS 的 LazyForEach 有类似机制：

```typescript
LazyForEach(this.data, (item: Item) => {
  ListItem() {
    // 列表项内容
  }
}, (item: Item) => item.id.toString())  // 唯一标识
```

### 问题5：Fragment 迁移

Fragment 在 HarmonyOS 中有多种迁移方案：

| 场景 | HarmonyOS 方案 |
|------|---------------|
| 独立页面 | 转为独立 Page |
| 可复用 UI 组件 | 转为 @Component |
| ViewPager 片段 | 转为 Swiper 的子组件 |
| Dialog 片段 | 转为 CustomDialog |

## 输出报告模板

```markdown
## UI 界面比对报告

### 概览
- Android 组件总数: X
- HarmonyOS 组件总数: Y
- 已匹配组件: M
- 缺失组件: N
- 发现差异: D

### 差异详情

#### CRITICAL
...

#### MAJOR
...

#### MINOR
...

### 组件类型统计

#### Android 组件
- LinearLayout: 5 -> Column/Row
- RecyclerView: 3 -> List
...

#### HarmonyOS 组件
- Column: 8
- List: 3
...

### 优化建议
...
```

## 与其他角色协作

| 角色 | 协作方式 |
|------|----------|
| Translator | 提供 UI 差异的修复代码 |
| Feature Comparator | 确认 UI 组件对应功能 |
| Validator | 验证 UI 代码质量 |
| Tester | 验证 UI 显示效果 |

## Hypium 自动化测试 API 参考

### 基础设置

```python
from hypium import UiDriver, BY, UiParam
from hypium.action.app.launcher import Launcher

# 连接设备
driver = UiDriver.connect()

# 或指定设备SN
# driver = UiDriver.connect(device_sn="your_device_sn")

# 完成后关闭驱动
driver.close()
```

### 应用启动命令

使用 hdc 命令启动应用：

| 平台 | 命令格式 | 示例 |
|------|-----------|------|
| Android | `hdc shell aa start -b <package> -a <activity>` | `hdc shell aa start -b com.simplemobiletools.gallery.pro -a com.simplemobiletools.gallery.pro.activities.SplashActivity.Orange` |
| HarmonyOS | `hdc shell aa start -b <bundle> -a <ability>` | `hdc shell aa start -b com.example.myapplication -a EntryAbility` |

### 截图操作

```python
# 截取整个屏幕
driver.capture_screen("screenshot.png")

# 截取指定区域（使用控件）
driver.capture_screen("area.png", area=BY.id("icon"))

# 截取指定区域（使用Rect）
from hypium import Rect
driver.capture_screen("area2.png", area=Rect(left, right, top, bottom))

# 模拟用户截屏操作（音量键+电源键）
driver.take_screenshot()
```

### 组件查找

```python
# 查找单个组件
component = driver.find_component(BY.text("设置"))
component = driver.find_component(BY.id("button_id"))
component = driver.find_component(BY.type("Button"))

# 在滚动区域内查找
component = driver.find_component(BY.text("底部"), scroll_target=BY.type("Scroll"))

# 查找所有匹配的组件
components = driver.find_all_components(BY.type("Button"))

# 获取第3个按钮（index从0开始）
component = driver.find_all_components(BY.type("Button"), 2)
```

### 组件交互

```python
# 点击操作
driver.click(BY.text("按钮"))
component.click()  # 组件对象调用

# 双击
driver.double_click(BY.text("测试按钮"))

# 长按
driver.long_click(BY.text("按钮"), press_time=5)

# 输入文本
driver.input_text(BY.type("TextInput"), "输入内容")

# 滑动操作
driver.swipe(UiParam.UP)  # 向上滑动
driver.swipe(UiParam.DOWN)  # 向下滑动
driver.swipe(UiParam.LEFT)  # 向左滑动
driver.swipe(UiParam.RIGHT)  # 向右滑动
```

### 获取组件属性

```python
# 获取组件文本
text = driver.get_component_property(BY.text("按钮"), "text")

# 获取组件状态
enabled = driver.get_component_property(BY.text("按钮"), "enabled")
clickable = driver.get_component_property(BY.text("按钮"), "clickable")

# 获取组件边框
bounds = driver.get_component_bound(BY.text("按钮"))
```

### 等待和检查

```python
# 等待指定秒数
driver.wait(3)

# 检查组件是否存在
driver.assert_check_component_exist(BY.text("按钮"), expect_exist=True)

# 检查图片是否存在
driver.check_image_exist("icon.png", expect_exist=True, timeout=10)
```

### 常用选择器 (BY)

| 方法 | 说明 | 示例 |
|------|------|------|
| `BY.text("文字")` | 通过文本查找 | `BY.text("设置")` |
| `BY.id("id值")` | 通过id查找 | `BY.id("button_id")` |
| `BY.key("key值")` | 通过key查找 | `BY.key("submit_btn")` |
| `BY.type("类型")` | 通过组件类型查找 | `BY.type("Button")` |
| `BY.clickable(True)` | 查找可点击的组件 | `BY.clickable(True)` |
| `BY.enabled(True)` | 查找启用的组件 | `BY.enabled(True)` |

### 常用 UiParam 常量

| 常量 | 说明 |
|-------|------|
| `UiParam.UP` | 向上 |
| `UiParam.DOWN` | 向下 |
| `UiParam.LEFT` | 向左 |
| `UiParam.RIGHT` | 向右 |

### 完整测试流程示例

```python
from hypium import UiDriver, BY, UiParam
from hypium.action.app.launcher import Launcher
import time
import subprocess

def run_ui_comparison():
    # 1. 连接设备
    driver = UiDriver.connect()

    try:
        # 2. 启动Android应用
        android_cmd = "hdc shell aa start -b com.simplemobiletools.gallery.pro -a com.simplemobiletools.gallery.pro.activities.SplashActivity.Orange"
        subprocess.run(android_cmd, shell=True)
        time.sleep(3)

        # 3. 截图
        driver.capture_screen("screenshots/android_main.png")

        # 4. 查找并点击关键组件
        try:
            settings_btn = driver.find_component(BY.text("设置"))
            settings_btn.click()
            time.sleep(1)
            driver.capture_screen("screenshots/android_settings.png")
            driver.press_back()
            time.sleep(1)
        except:
            print("未找到设置按钮")

        # 5. 清理后台应用
        Launcher.clear_recent_task(driver)

        # 6. 启动鸿蒙应用
        harmonyos_cmd = "hdc shell aa start -b com.example.myapplication -a EntryAbility"
        subprocess.run(harmonyos_cmd, shell=True)
        time.sleep(3)

        # 7. 截图
        driver.capture_screen("screenshots/harmonyos_main.png")

        # 8. 查找并点击关键组件
        try:
            settings_btn = driver.find_component(BY.text("设置"))
            settings_btn.click()
            time.sleep(1)
            driver.capture_screen("screenshots/harmonyos_settings.png")
            driver.press_back()
            time.sleep(1)
        except:
            print("未找到设置按钮")

    finally:
        # 9. 关闭驱动
        driver.close()

if __name__ == "__main__":
    run_ui_comparison()
```
