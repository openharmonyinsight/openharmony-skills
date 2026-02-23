# 测试用例编写指南

将调试通过的测试步骤生成为正式的 Hypium 测试用例。

## 测试用例结构

### Python 测试文件 (.py)

```python
#!/usr/bin/env python
# coding: utf-8
from devicetest.core.test_case import TestCase, Step
from hypium import *
import time


class Test{ClassName}(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        TestCase.__init__(self, self.TAG, controllers)
        self.driver = UiDriver(self.device1)

    def setup(self):
        """测试前置操作"""
        Step('回到桌面')
        self.driver.swipe_to_home()
        time.sleep(3)

        Step('启动应用')
        self.driver.start_app("{package_name}")
        time.sleep(3)  # 启动应用后必须等待3秒

    def process(self):
        """测试主流程"""
        # Step 1
        Step('{step_description}')
        {step_code}
        time.sleep(3)

    def teardown(self):
        """测试后置操作"""
        Step('清理环境')
        self.driver.stop_app("{package_name}")
```

### JSON 配置文件 (.json)

```json
{
  "description": "Config for {TestClassName}",
  "environment": [{"type": "device", "label": "phone"}],
  "driver": {"type": "DeviceTest", "py_file": ["test_{test_name}.py"]}
}
```

## Sleep 等待规范（强制要求）

> **每个操作后必须添加 `time.sleep()`！这是强制要求！**

| 操作类型 | 等待时间 | 说明 |
|---------|---------|------|
| `start_app()` 启动应用后 | **3秒** | 应用启动需要较长时间加载 |
| `touch()` 点击操作后 | **至少3秒** | 等待页面响应和动画 |
| `input_text()` 输入操作后 | **至少3秒** | 等待输入完成和响应 |
| `swipe()` 滑动操作后 | **至少3秒** | 等待滑动动画完成 |
| 页面跳转后 | **3秒** | 等待新页面加载 |

```python
# 正确示例
self.driver.start_app("com.example.app")
time.sleep(3)  # 启动应用后等待3秒

self.driver.touch(BY.text("按钮"))
time.sleep(3)  # 点击后等待3秒
```

## 智能重试逻辑

```python
def click_with_retry(self, locator, fallback_locator=None, timeout=10000):
    """带重试的点击操作"""
    try:
        component = self.driver.wait_for_component(locator, timeout)
        self.driver.touch(component)
        return True
    except Exception as e:
        if fallback_locator:
            try:
                component = self.driver.wait_for_component(fallback_locator, timeout)
                self.driver.touch(component)
                return True
            except Exception:
                pass
        raise e
```

## 断言生成

```python
# 元素可见断言
def assert_element_visible(self, locator):
    component = self.driver.find_component(locator)
    assert component is not None, f"元素 {locator} 应该可见"

# 文本相等断言
def assert_text_equals(self, locator, expected_text):
    component = self.driver.find_component(locator)
    actual_text = component.getText()
    assert actual_text == expected_text, f"文本应为 '{expected_text}'，实际为 '{actual_text}'"
```

## 输出文件

```
{PROJECT_ROOT}/testcases/
├── test_{test_name}.py      # 测试用例 Python 文件
└── test_{test_name}.json    # 测试配置文件
```

**重要**:
- 使用环境变量 `HARMONYOS_PROJECT_ROOT` 获取项目根目录
- 测试用例必须成对生成：`.py` 和 `.json` 文件
