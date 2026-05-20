#!/usr/bin/env python3
"""
测试 search.py 脚本的功能
"""

import subprocess
import sys
import os
import json

def run_search(query, *args):
    """运行搜索命令"""
    cmd = ['python3', 'scripts/search.py', query] + list(args)
    result = subprocess.run(
        cmd,
        cwd=os.path.join(os.path.dirname(__file__), '..'),
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr

def test_basic_search():
    """测试基本搜索功能"""
    print("测试 1: 基本搜索 (lambda)")
    returncode, stdout, stderr = run_search('lambda', '--max-results', '1')
    
    if returncode != 0:
        print(f"  ❌ 失败: 返回码 {returncode}")
        print(f"  错误: {stderr}")
        return False
    
    if 'lambda' in stdout.lower():
        print("  ✓ 通过: 找到 lambda 相关结果")
        return True
    else:
        print("  ❌ 失败: 未找到预期结果")
        return False

def test_json_output():
    """测试 JSON 输出格式"""
    print("\n测试 2: JSON 输出格式")
    returncode, stdout, stderr = run_search('lambda', '--json', '--max-results', '1')
    
    if returncode != 0:
        print(f"  ❌ 失败: 返回码 {returncode}")
        return False
    
    try:
        data = json.loads(stdout)
        if 'count' in data and 'results' in data:
            print(f"  ✓ 通过: JSON 格式正确，找到 {data['count']} 个结果")
            return True
        else:
            print("  ❌ 失败: JSON 格式不正确")
            return False
    except json.JSONDecodeError as e:
        print(f"  ❌ 失败: JSON 解析错误 - {e}")
        return False

def test_fuzzy_matching():
    """测试模糊匹配"""
    print("\n测试 3: 模糊匹配 (lambdaa -> lambda)")
    returncode, stdout, stderr = run_search('lambdaa', '--max-results', '1')
    
    if returncode != 0:
        print(f"  ❌ 失败: 返回码 {returncode}")
        return False
    
    if 'lambda' in stdout.lower():
        print("  ✓ 通过: 模糊匹配成功")
        return True
    else:
        print("  ❌ 失败: 模糊匹配未生效")
        return False

def test_no_fuzzy():
    """测试禁用模糊匹配"""
    print("\n测试 4: 禁用模糊匹配 (--no-fuzzy)")
    returncode, stdout, stderr = run_search('lambdaa', '--no-fuzzy')
    
    if returncode != 0:
        print(f"  ❌ 失败: 返回码 {returncode}")
        return False
    
    if '未找到' in stdout or 'count": 0' in stdout:
        print("  ✓ 通过: 禁用模糊匹配成功")
        return True
    else:
        print("  ❌ 失败: 应该未找到结果")
        return False

def test_chinese_query():
    """测试中文查询"""
    print("\n测试 5: 中文查询 (匿名函数)")
    returncode, stdout, stderr = run_search('匿名函数', '--max-results', '1')
    
    if returncode != 0:
        print(f"  ❌ 失败: 返回码 {returncode}")
        return False
    
    if 'lambda' in stdout.lower() or '匿名' in stdout:
        print("  ✓ 通过: 中文查询成功")
        return True
    else:
        print("  ❌ 失败: 中文查询未找到预期结果")
        return False

def test_english_output():
    """测试英文输出"""
    print("\n测试 6: 英文输出 (--lang en)")
    returncode, stdout, stderr = run_search('lambda', '--lang', 'en', '--max-results', '1')
    
    if returncode != 0:
        print(f"  ❌ 失败: 返回码 {returncode}")
        return False
    
    if 'Result' in stdout or 'Concept' in stdout:
        print("  ✓ 通过: 英文输出成功")
        return True
    else:
        print("  ❌ 失败: 未使用英文输出")
        return False

def test_help():
    """测试帮助信息"""
    print("\n测试 7: 帮助信息 (--help)")
    returncode, stdout, stderr = run_search('--help')
    
    if returncode == 0 and ('usage:' in stdout or 'positional arguments' in stdout):
        print("  ✓ 通过: 帮助信息显示正常")
        return True
    else:
        print("  ❌ 失败: 帮助信息显示异常")
        return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("search.py 功能测试")
    print("=" * 60)
    
    tests = [
        test_basic_search,
        test_json_output,
        test_fuzzy_matching,
        test_no_fuzzy,
        test_chinese_query,
        test_english_output,
        test_help
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
