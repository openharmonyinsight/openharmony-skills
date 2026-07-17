#!/usr/bin/env python3
"""
run_tests.py - 运行所有测试
"""

import unittest
import os
import sys

# 添加tests目录到路径
sys.path.insert(0, os.path.dirname(__file__))

def run_all_tests():
    """运行所有测试"""
    
    # 发现所有测试
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(__file__), pattern='test_*.py')
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回结果
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_all_tests())