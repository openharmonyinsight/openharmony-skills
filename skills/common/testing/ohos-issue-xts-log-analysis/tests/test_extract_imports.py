#!/usr/bin/env python3
"""
test_extract_imports.py - extract_imports.py 单元测试
"""

import unittest
import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from extract_imports import extract_imports, classify_import

class TestExtractImports(unittest.TestCase):
    """测试import提取功能"""
    
    def setUp(self):
        """设置测试文件"""
        self.test_file = '/tmp/test_imports.ets'
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("""
import { describe, it, expect } from '@ohos/hypium';
import { stream } from '@kit.ArkTS';
import Want from '@ohos.app.ability.Want';
import Utils from '../common/Utils';
""")
    
    def tearDown(self):
        """清理测试文件"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_extract_imports(self):
        """测试import提取"""
        imports = extract_imports(self.test_file)
        
        self.assertEqual(len(imports), 4)
        
        # 验证import内容
        modules = [imp['module'] for imp in imports]
        self.assertIn('@ohos/hypium', modules)
        self.assertIn('@kit.ArkTS', modules)
        self.assertIn('@ohos.app.ability.Want', modules)
        self.assertIn('../common/Utils', modules)
    
    def test_classify_import(self):
        """测试import分类"""
        # 测试框架
        self.assertEqual(classify_import('@ohos/hypium'), 'test_framework')
        
        # Kit引用
        self.assertEqual(classify_import('@kit.ArkTS'), 'kit_module')
        
        # API模块
        self.assertEqual(classify_import('@ohos.app.ability.Want'), 'api_module')
        
        # 内部模块
        self.assertEqual(classify_import('../common/Utils'), 'internal_module')
        self.assertEqual(classify_import('./Utils'), 'internal_module')

if __name__ == '__main__':
    unittest.main()