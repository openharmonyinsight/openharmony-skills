#!/usr/bin/env python3
"""
test_map_domain.py - map_domain.py 单元测试
"""

import unittest
import sys
import os
import json

# 添加脚本目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

class TestMapDomain(unittest.TestCase):
    """测试domain映射功能"""
    
    def test_map_api_module(self):
        """测试API模块映射"""
        import subprocess
        
        # 测试已知API模块
        result = subprocess.run(
            ['python3', 'scripts/map_domain.py', '@ohos.util.stream'],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), '..')
        )
        
        data = json.loads(result.stdout)
        
        self.assertEqual(data['status'], 'mapped')
        self.assertEqual(data['domain'], '0xD003F00')
        self.assertEqual(data['subsystem'], '公共基础类库')
    
    def test_map_kit_module(self):
        """测试Kit展开"""
        import subprocess
        
        result = subprocess.run(
            ['python3', 'scripts/map_domain.py', '@kit.ArkTS'],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), '..')
        )
        
        data = json.loads(result.stdout)
        
        self.assertEqual(data['status'], 'expanded')
        self.assertEqual(data['kit'], 'ArkTS')
        self.assertIn('@ohos.util.stream', data['modules'])
    
    def test_unmapped_module(self):
        """测试未映射模块"""
        import subprocess
        
        result = subprocess.run(
            ['python3', 'scripts/map_domain.py', '@ohos.nonexistent'],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), '..')
        )
        
        data = json.loads(result.stdout)
        
        self.assertEqual(data['status'], 'unmapped')
        self.assertIn('NOT FOUND', data['reason'])

if __name__ == '__main__':
    unittest.main()