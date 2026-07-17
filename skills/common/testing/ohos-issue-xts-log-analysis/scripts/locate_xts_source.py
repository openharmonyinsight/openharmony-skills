#!/usr/bin/env python3
"""
XTS源码定位脚本 - 根据改进方案实现

功能：
1. 步骤一：搜索 testcase 名称（最高优先级）
2. 步骤二：搜索 testsuite 名称
3. 步骤三：路径交集检查
4. 步骤四：搜索 HAP 名称（兜底方案）

用法：
    python3 locate_xts_source.py --testcase "testcase_name" --testsuite "testsuite_name" --hap "hap_name" --root "OH_ROOT"
    
输出：
    JSON格式的定位结果，包含源码文件路径和定位方法
"""

import os
import re
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional, Dict


class XtsSourceLocator:
    """XTS源码定位器"""
    
    def __init__(self, oh_root: str):
        """初始化定位器"""
        self.oh_root = Path(oh_root)
        if not self.oh_root.exists():
            raise ValueError(f"源码根路径不存在: {oh_root}")
    
    def locate_by_testcase(self, testcase_name: str) -> Tuple[Optional[Path], List[Path], str]:
        """
        步骤一：搜索 testcase 名称（最高优先级）
        
        返回: (源码文件, 匹配列表, 匹配方法)
        """
        print(f"[步骤一] 搜索 testcase: {testcase_name}")
        
        # 方法A: 搜索 it() 函数定义
        cmd = f'grep -r "it(\'{testcase_name}\'" {self.oh_root}/acts --include="*.test.ets" --include="*.test.ts" 2>/dev/null'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        matches_a = self._parse_grep_output(result.stdout)
        
        # 方法B: 搜索 @tc.name 注释
        cmd_b = f'grep -r "@tc.name   {testcase_name}" {self.oh_root}/acts --include="*.test.ets" --include="*.test.ts" 2>/dev/null'
        result_b = subprocess.run(cmd_b, shell=True, capture_output=True, text=True)
        
        matches_b = self._parse_grep_output(result_b.stdout)
        
        # 合并去重
        all_matches = list(set(matches_a + matches_b))
        
        if len(all_matches) == 1:
            print(f"  ✓ 唯一匹配: {all_matches[0]}")
            return all_matches[0], all_matches, 'testcase_unique'
        elif len(all_matches) > 1:
            print(f"  ⚠ 多匹配 ({len(all_matches)}个): {[str(p) for p in all_matches[:3]]}")
            return None, all_matches, 'testcase_multiple'
        else:
            print(f"  ✗ 无匹配")
            return None, [], 'testcase_none'
    
    def locate_by_testsuite(self, testsuite_name: str) -> Tuple[Optional[Path], List[Path], str]:
        """
        步骤二：搜索 testsuite 名称
        
        返回: (源码文件, 匹配列表, 匹配方法)
        """
        print(f"[步骤二] 搜索 testsuite: {testsuite_name}")
        
        # 搜索 describe() 定义（忽略大小写）
        cmd = f'grep -ri "describe.*{testsuite_name}" {self.oh_root}/acts --include="*.test.ets" --include="*.test.ts" 2>/dev/null'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        matches = self._parse_grep_output(result.stdout)
        
        if len(matches) == 1:
            print(f"  ✓ 唯一匹配: {matches[0]}")
            return matches[0], matches, 'testsuite_unique'
        elif len(matches) > 1:
            print(f"  ⚠ 多匹配 ({len(matches)}个): {[str(p) for p in matches[:3]]}")
            return None, matches, 'testsuite_multiple'
        else:
            print(f"  ✗ 无匹配")
            return None, [], 'testsuite_none'
    
    def locate_by_intersection(self, testcase_paths: List[Path], testsuite_paths: List[Path]) -> Tuple[Optional[Path], str]:
        """
        步骤三：路径交集检查
        
        返回: (源码文件, 匹配方法)
        """
        print(f"[步骤三] 路径交集检查")
        
        if not testcase_paths or not testsuite_paths:
            print(f"  ✗ 无法计算交集（缺少路径）")
            return None, 'intersection_none'
        
        intersection = set(testcase_paths) & set(testsuite_paths)
        
        if len(intersection) == 1:
            result = intersection.pop()
            print(f"  ✓ 交集唯一: {result}")
            return result, 'intersection_unique'
        elif len(intersection) > 1:
            print(f"  ⚠ 交集多匹配 ({len(intersection)}个)")
            return None, 'intersection_multiple'
        else:
            print(f"  ✗ 交集为空")
            return None, 'intersection_empty'
    
    def locate_by_hap(self, hap_name: str) -> Tuple[Optional[Path], List[Path], str]:
        """
        步骤四：搜索 HAP 名称（兜底方案）
        
        改进：通过 BUILD.gn 文件中的 hap_name 字段定位
        
        返回: (项目目录, 匹配列表, 匹配方法)
        """
        print(f"[步骤四] 搜索 HAP: {hap_name}")
        
        # 去掉.hap后缀（如果存在）
        hap_name_clean = hap_name.replace('.hap', '')
        print(f"  清理HAP名: {hap_name_clean}")
        
        # 搜索 BUILD.gn 文件中包含该 hap_name 的工程
        # 格式: hap_name = "ActsAceWeb...Test"
        cmd = f'find {self.oh_root}/acts -name "BUILD.gn" -exec grep -l "hap_name.*{hap_name_clean}" {{}} \\; 2>/dev/null'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        matches = []
        for line in result.stdout.strip().split('\n'):
            if line:
                # line 是 BUILD.gn 文件的完整路径
                # 项目目录是 BUILD.gn 的父目录
                build_gn_path = Path(line)
                project_dir = build_gn_path.parent
                if project_dir.exists():
                    matches.append(project_dir)
        
        if len(matches) == 1:
            print(f"  ✓ 唯一匹配: {matches[0]}")
            return matches[0], matches, 'hap_unique'
        elif len(matches) > 1:
            print(f"  ⚠ 多匹配 ({len(matches)}个): {[str(p) for p in matches[:3]]}")
            return None, matches, 'hap_multiple'
        else:
            print(f"  ✗ 无匹配")
            return None, [], 'hap_none'
    
    def convert_hap_to_dir(self, hap_name: str) -> str:
        """
        HAP名转换为目录名
        
        示例:
            ActsAceWebPageDownloadCloudServiceControllerGroupTwelveTest.hap
            → ace_web_page_download_cloudservice_controller_group_twelve
            
        注意：
            - CloudService → cloudservice（不是 cloud_service）
            - Controller → controller
            - Group → group
        """
        # 去掉 Acts 前缀
        name = hap_name.replace('Acts', '')
        
        # 去掉 Test.hap 或 .hap 后缀
        if name.endswith('Test.hap'):
            name = name[:-8]  # 去掉 "Test.hap"
        elif name.endswith('.hap'):
            name = name[:-4]  # 去掉 ".hap"
        
        # 特殊处理：连续的大写字母序列（如CloudService）应作为整体
        # 先在连续大写字母序列之间插入分隔符，然后整体转小写
        # 例如: CloudService -> Cloud_Service -> cloud_service（错误）
        #       CloudService -> cloudservice（正确）
        
        # 方法：只在后面跟着小写字母的大写字母前加下划线
        # A[A-Z]b -> A_Ab (A后面是小写字母b)
        # AB[A-Z]c -> AB_c (B后面是小写字母c)
        # 但 ABC -> ABC (连续大写不处理)
        
        result = []
        i = 0
        while i < len(name):
            if i > 0 and name[i].isupper():
                # 当前是大写字母
                if i + 1 < len(name) and name[i+1].islower():
                    # 后面跟着小写字母，前面加下划线
                    result.append('_')
                elif i > 0 and name[i-1].islower():
                    # 前面是小写字母，前面加下划线
                    result.append('_')
            result.append(name[i])
            i += 1
        
        name = ''.join(result).lower()
        
        # 去掉开头的下划线
        name = name.lstrip('_')
        
        return name
    
    def _parse_grep_output(self, grep_output: str) -> List[Path]:
        """解析 grep 输出，提取文件路径"""
        matches = []
        for line in grep_output.strip().split('\n'):
            if line:
                # 格式: /path/to/file.ets:content
                parts = line.split(':', 1)
                if parts:
                    file_path = Path(parts[0])
                    if file_path.exists():
                        matches.append(file_path)
        return matches
    
    def locate_source(self, testcase: str, testsuite: str, hap: str) -> Dict:
        """
        完整定位流程
        
        返回: 定位结果字典
        """
        result = {
            'source_file': None,
            'project_dir': None,
            'candidates': [],
            'step': None,
            'method': None,
            'success': False
        }
        
        # 步骤一：搜索 testcase
        source_file, testcase_paths, method1 = self.locate_by_testcase(testcase)
        if source_file:
            result['source_file'] = str(source_file)
            result['project_dir'] = str(source_file.parents[4])
            result['step'] = 'step1'
            result['method'] = method1
            result['success'] = True
            return result
        
        # 步骤二：搜索 testsuite
        source_file2, testsuite_paths, method2 = self.locate_by_testsuite(testsuite)
        if source_file2:
            result['source_file'] = str(source_file2)
            result['project_dir'] = str(source_file2.parents[4])
            result['step'] = 'step2'
            result['method'] = method2
            result['success'] = True
            return result
        
        # 步骤三：路径交集
        if testcase_paths and testsuite_paths:
            intersection_file, method3 = self.locate_by_intersection(testcase_paths, testsuite_paths)
            if intersection_file:
                result['source_file'] = str(intersection_file)
                result['project_dir'] = str(intersection_file.parents[4])
                result['step'] = 'step3'
                result['method'] = method3
                result['success'] = True
                return result
        
        # 步骤四：搜索 HAP
        project_dir, hap_paths, method4 = self.locate_by_hap(hap)
        if project_dir:
            result['project_dir'] = str(project_dir)
            result['candidates'] = [str(p) for p in hap_paths]
            result['step'] = 'step4'
            result['method'] = method4
            
            # 尝试从项目目录中查找测试文件并匹配 testcase/testsuite
            print(f"  搜索测试文件...")
            test_files = list(Path(project_dir).rglob('*.test.ets')) + list(Path(project_dir).rglob('*.test.ts'))
            
            if test_files:
                print(f"  找到 {len(test_files)} 个测试文件")
                
                # 优先匹配 testcase
                for test_file in test_files:
                    try:
                        content = test_file.read_text(encoding='utf-8', errors='ignore')
                        
                        # 检查 testcase 是否在文件中（it函数或@tc.name）
                        if f"it('{testcase}'" in content or f"@tc.name   {testcase}" in content:
                            print(f"  ✓ 匹配 testcase: {test_file}")
                            result['source_file'] = str(test_file)
                            result['success'] = True
                            return result
                        
                        # 检查 testsuite 是否在文件中（describe函数）
                        if f"describe('{testsuite}'" in content or testsuite.lower() in content.lower():
                            print(f"  ✓ 匹配 testsuite: {test_file}")
                            result['source_file'] = str(test_file)
                            result['success'] = True
                            return result
                    except Exception as e:
                        print(f"  ✗ 读取文件失败: {test_file} - {e}")
                        continue
                
                # 如果没有精确匹配，且只有一个测试文件，则使用它
                if len(test_files) == 1:
                    print(f"  ✓ 唯一测试文件: {test_files[0]}")
                    result['source_file'] = str(test_files[0])
                    result['success'] = True
                else:
                    print(f"  ⚠ 多个测试文件，无法自动选择")
            else:
                print(f"  ✗ 项目目录下无测试文件")
            
            return result
        
        # 未找到
        result['step'] = 'failed'
        result['method'] = 'not_found'
        return result


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='XTS源码定位工具 - 根据testcase/testsuite/hap名称定位源码文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python3 locate_xts_source.py \\
    --testcase "testWebView_getPercentComplete1006" \\
    --testsuite "getPercentComplete" \\
    --hap "ActsAceWebPageDownloadCloudServiceControllerGroupTwelveTest.hap" \\
    --root "/home/xianf/master/test/xts"
        '''
    )
    
    parser.add_argument('--testcase', required=True, help='失败用例名称（从日志提取）')
    parser.add_argument('--testsuite', required=True, help='测试套件名称（从日志提取）')
    parser.add_argument('--hap', required=True, help='HAP文件名（从日志提取）')
    parser.add_argument('--root', required=True, help='OH源码根路径')
    parser.add_argument('--output', choices=['json', 'text'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    # 执行定位
    try:
        locator = XtsSourceLocator(args.root)
        result = locator.locate_source(args.testcase, args.testsuite, args.hap)
        
        # 输出结果
        if args.output == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("\n" + "="*60)
            print("定位结果")
            print("="*60)
            print(f"成功: {result['success']}")
            print(f"定位步骤: {result['step']}")
            print(f"定位方法: {result['method']}")
            if result['source_file']:
                print(f"源码文件: {result['source_file']}")
            if result['project_dir']:
                print(f"项目目录: {result['project_dir']}")
            if result['candidates']:
                print(f"候选路径: {result['candidates'][:3]}")
            print("="*60)
    
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'step': 'error',
            'method': 'exception'
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()