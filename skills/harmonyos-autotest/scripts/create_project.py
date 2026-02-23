#!/usr/bin/env python3
"""
创建 HarmonyOS 自动化测试项目目录
用法: python create_project.py <app_name> <test_feature> [output_dir]
"""
import os
import sys
from datetime import datetime


def create_project(app_name: str, test_feature: str, output_dir: str = None):
    """创建测试项目目录结构"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = f"{app_name}_{test_feature}_{timestamp}"

    if output_dir:
        project_root = os.path.join(output_dir, project_name)
    else:
        project_root = os.path.join(os.getcwd(), "projects", project_name)

    # 创建目录结构
    dirs = [
        "config",
        "testcases",
        "aw",
        "resource/images",
        "output/controls",
        "output/screenshots",
        "output/reports",
        "output/logs",
        "output/temp"
    ]

    for d in dirs:
        os.makedirs(os.path.join(project_root, d), exist_ok=True)

    # 生成配置文件
    generate_config(project_root)
    generate_main_py(project_root)
    generate_example_test(project_root, app_name)
    generate_utils(project_root)
    generate_requirements(project_root)

    print(f"项目创建成功: {project_root}")
    print(f"\n下一步:")
    print(f"  cd {project_root}")
    print(f"  pip3 install -r requirements.txt")
    print(f"  # 修改 config/user_config.xml 配置设备 SN")
    print(f"  # 在 testcases/ 目录下编写测试用例")

    return project_root


def generate_config(project_root: str):
    """生成 config/user_config.xml"""
    config_content = '''<?xml version="1.0" encoding="UTF-8"?>
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
'''
    with open(os.path.join(project_root, "config", "user_config.xml"), "w") as f:
        f.write(config_content)


def generate_main_py(project_root: str):
    """生成 main.py"""
    main_content = '''from xdevice.__main__ import main_process

if __name__ == "__main__":
    main_process("run -l Example -ta agent_mode:bin;screenshot:true")
'''
    with open(os.path.join(project_root, "main.py"), "w") as f:
        f.write(main_content)


def generate_example_test(project_root: str, app_name: str):
    """生成示例测试用例"""
    py_content = f'''#!/usr/bin/env python
# coding: utf-8
from devicetest.core.test_case import TestCase, Step
from hypium import *
import time


class Example(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        TestCase.__init__(self, self.TAG, controllers)
        self.driver = UiDriver(self.device1)

    def setup(self):
        """测试前置操作"""
        Step('1.回到桌面')
        self.driver.swipe_to_home()
        time.sleep(3)

    def process(self):
        """测试主流程"""
        Step('2.启动应用')
        # self.driver.start_app(package_name="com.example.{app_name}")
        time.sleep(3)

    def teardown(self):
        """测试后置操作"""
        Step('3.清理环境')
        # self.driver.stop_app("com.example.{app_name}")
'''
    with open(os.path.join(project_root, "testcases", "Example.py"), "w") as f:
        f.write(py_content)

    json_content = '''{
  "description": "Config for Example Test",
  "environment": [
    {
      "type": "device",
      "label": "phone"
    }
  ],
  "driver": {
    "type": "DeviceTest",
    "py_file": [
      "Example.py"
    ]
  }
}
'''
    with open(os.path.join(project_root, "testcases", "Example.json"), "w") as f:
        f.write(json_content)


def generate_utils(project_root: str):
    """生成 aw/Utils.py"""
    utils_content = '''from hypium import UiDriver


def get_app_version_code(driver: UiDriver, bundle: str) -> int:
    """获取应用版本号"""
    info = driver.shell('bm dump -n {} |grep versionCode'.format(bundle))
    if 'versionCode' not in info:
        return 0
    token = info.splitlines()[-1]
    code_str = token.replace('"versionCode":', '').replace(',', '').strip()
    return int(code_str)
'''
    with open(os.path.join(project_root, "aw", "Utils.py"), "w") as f:
        f.write(utils_content)


def generate_requirements(project_root: str):
    """生成 requirements.txt"""
    with open(os.path.join(project_root, "requirements.txt"), "w") as f:
        f.write("hypium>=6.0.7.210\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python create_project.py <app_name> <test_feature> [output_dir]")
        print("示例: python create_project.py toutiao search_test")
        sys.exit(1)

    app_name = sys.argv[1]
    test_feature = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    create_project(app_name, test_feature, output_dir)
