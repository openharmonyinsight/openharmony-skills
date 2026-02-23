# !/usr/bin/env python
# coding: utf-8
"""
#!!================================================================
#版权 (C) 2023, Huawei Technologies Co.
#==================================================================
#文 件 名：                 Example.py
#文件说明：                 Example TestScript
#作    者：                 author
#生成日期：                 2023-07-13
#!!================================================================
"""

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
        Step('2.启动设置应用')
        self.driver.start_app(package_name="com.huawei.hmos.settings", page_name="com.huawei.hmos.settings.MainAbility")

    def teardown(self):
        Step('3.关闭设置应用')
        self.driver.stop_app("com.huawei.hmos.settings")
