# 项目模板说明

基于官方 Hypium 框架（版本 >= 6.0.7.210）。

## 项目目录结构

```
{project_root}/
├── config/                        # 配置文件目录
│   └── user_config.xml           # 设备和环境配置
├── testcases/                     # 测试用例目录
│   ├── Example.py                # 测试用例 Python 文件
│   └── Example.json              # 测试用例配置文件
├── aw/                            # 自定义模块目录
│   └── Utils.py                  # 工具函数
├── resource/                      # 测试资源目录
│   └── images/                   # 图片资源
├── main.py                        # 测试入口
├── requirements.txt               # Python 依赖
└── output/                        # 输出文件目录
    ├── controls/                 # 控件树快照
    ├── screenshots/              # 测试截图
    ├── reports/                  # 测试报告
    ├── logs/                     # 测试日志
    └── temp/                     # 临时文件
```

## 项目命名规则

```
{app_name}_{test_feature}_{timestamp}
```

示例: `toutiao_search_test_20260218_153045`

## 文件模板

### config/user_config.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<user_config>
    <environment>
        <device type="usb-hdc">
            <sn></sn>
        </device>
    </environment>
    <testcases>
        <dir></dir>
    </testcases>
    <loglevel>DEBUG</loglevel>
    <devicelog>ON</devicelog>
</user_config>
```

### main.py

```python
from xdevice.__main__ import main_process

if __name__ == "__main__":
    main_process("run -l Example -ta agent_mode:bin;screenshot:true")
```

### testcases/Example.py

```python
#!/usr/bin/env python
# coding: utf-8
from devicetest.core.test_case import TestCase, Step
from hypium import *


class Example(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        TestCase.__init__(self, self.TAG, controllers)
        self.driver = UiDriver(self.device1)

    def setup(self):
        Step('1.回到桌面')
        self.driver.swipe_to_home()

    def process(self):
        Step('2.启动应用')
        self.driver.start_app(package_name="com.example.app")

    def teardown(self):
        Step('3.关闭应用')
        self.driver.stop_app("com.example.app")
```

### testcases/Example.json

```json
{
  "description": "Config for ExampleTest",
  "environment": [{"type": "device", "label": "phone"}],
  "driver": {"type": "DeviceTest", "py_file": ["Example.py"]}
}
```

### aw/Utils.py

```python
from hypium import UiDriver


def get_app_version_code(driver: UiDriver, bundle: str) -> int:
    """获取应用版本号"""
    info = driver.shell('bm dump -n {} |grep versionCode'.format(bundle))
    if 'versionCode' not in info:
        return 0
    token = info.splitlines()[-1]
    code_str = token.replace('"versionCode":', '').replace(',', '').strip()
    return int(code_str)
```

### requirements.txt

```
hypium>=6.0.7.210
```

## 环境变量

项目使用环境变量 `HARMONYOS_PROJECT_ROOT` 来定位项目根目录：

```python
import os
PROJECT_ROOT = os.environ.get('HARMONYOS_PROJECT_ROOT', './output')
```

## 文件输出规范

| 文件类型 | 输出目录 |
|---------|---------|
| 控件树快照 | `{PROJECT_ROOT}/output/controls/` |
| 测试截图 | `{PROJECT_ROOT}/output/screenshots/` |
| 测试报告 | `{PROJECT_ROOT}/output/reports/` |
| 日志文件 | `{PROJECT_ROOT}/output/logs/` |
| 临时文件 | `{PROJECT_ROOT}/output/temp/` |

## 运行测试

```bash
# 方式 1: 使用 main.py
cd {PROJECT_ROOT}
python main.py

# 方式 2: 使用 xdevice 命令
cd {PROJECT_ROOT}
xdevice run -l Example -ta agent_mode:bin;screenshot:true
```

## 完整模板

完整的项目模板位于 `assets/HypiumProjectTemplate/` 目录。
