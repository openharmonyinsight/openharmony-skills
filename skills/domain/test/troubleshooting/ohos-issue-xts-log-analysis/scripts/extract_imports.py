#!/usr/bin/env python3
"""
extract_imports.py - 从测试源码文件中提取import/include语句并分类

设计原则：
1. 支持 JS/TS/ETS 文件（import语句）
2. 支持 C/C++ 文件（#include语句）
3. 自动分类类型（api_module / kit_module / c_api / internal_module / test_framework）
4. 提取kit引用中的具体模块名
5. 处理特殊路径引用

用法：
    python3 extract_imports.py <源码文件路径>
    
输出：
    {
      "status": "ok",
      "file": "StreamTest08.test.ets",
      "language": "typescript",
      "imports": [
        {
          "line": 2,
          "statement": "import { stream } from '@kit.ArkTS';",
          "module": "@kit.ArkTS",
          "type": "kit_module",
          "imported_names": ["stream"],
          "skip": false
        }
      ],
      "test_apis": [
        {
          "module": "@kit.ArkTS",
          "imported_names": ["stream"],
          "type": "kit_module"
        }
      ]
    }
"""

import os
import re
import json
import argparse
from typing import List, Dict

# 测试框架模块列表（不作为被测API）
TEST_FRAMEWORKS_JS = [
    '@ohos.hypium',
    '@ohos/hypium',
    '@ohos.UiTest',
    '@ohos/UiTest',
    '@ohos.hypium-binary',
    '@ohos/hypium-binary',
    '@ohos.test',
    '@ohos/test',
    '@kit.TestKit',
    '@kit/TestKit'
]

# C/C++ 测试框架头文件（不作为被测API）
TEST_FRAMEWORKS_C = [
    'gtest.h',
    'gmock.h',
    'unity.h',
    'hctest.h',
    'xts_log.h',
    'test.h'
]

def detect_language(file_path: str) -> str:
    """检测文件语言类型"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.ets', '.ts', '.js']:
        return 'typescript'
    elif ext in ['.c', '.cpp', '.cc', '.cxx']:
        return 'cpp'
    elif ext in ['.h', '.hpp']:
        return 'header'
    else:
        return 'unknown'

def extract_js_imports(file_path: str) -> List[Dict]:
    """提取JS/TS/ETS文件中的import语句"""
    imports = []
    
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_no, line in enumerate(f, 1):
            # 匹配import语句
            # 格式1: import X from 'module'
            # 格式2: import { X, Y } from 'module'
            # 格式3: import * as X from 'module'
            
            match = re.search(r"from\s+['\"]([^'\"]+)['\"]", line)
            if match:
                module = match.group(1)
                
                imported_names = []
                names_match = re.search(r"import\s+\{([^}]+)\}", line)
                if names_match:
                    names_str = names_match.group(1)
                    imported_names = [n.strip() for n in names_str.split(',') if n.strip()]
                elif 'import' in line and 'from' in line and '{' not in line:
                    name_match = re.search(r"import\s+(\w+)", line)
                    if name_match:
                        imported_names = [name_match.group(1)]
                
                imports.append({
                    'line': line_no,
                    'statement': line.strip(),
                    'module': module,
                    'imported_names': imported_names,
                    'include_type': 'import'
                })
    
    return imports

def extract_c_includes(file_path: str) -> List[Dict]:
    """提取C/C++文件中的#include语句"""
    imports = []
    
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_no, line in enumerate(f, 1):
            # 匹配#include语句
            # 格式1: #include <xxx.h>  （系统头文件，跳过）
            # 格式2: #include "xxx.h"  （自定义头文件，可能是被测API）
            
            match = re.search(r'#include\s+"([^"]+)"', line)
            if match:
                header = match.group(1)
                
                # 提取头文件名（去掉路径）
                header_name = os.path.basename(header)
                
                imports.append({
                    'line': line_no,
                    'statement': line.strip(),
                    'module': header,
                    'imported_names': [header_name],
                    'include_type': 'include'
                })
    
    return imports

def classify_import_js(module: str) -> str:
    """分类JS/TS import语句
    
    返回值：
    - 'api_module': 被测API模块（@ohos.xxx，需要查询domain）
    - 'kit_module': Kit引用（@kit.xxx，需要展开）
    - 'internal_module': 内部模块（相对路径，需要探索引用链）
    - 'test_framework': 测试框架（跳过）
    - 'unknown': 未知类型
    """
    
    if module.startswith('./') or module.startswith('../'):
        return 'internal_module'
    
    for tf in TEST_FRAMEWORKS_JS:
        if module == tf or module.startswith(tf + '/'):
            return 'test_framework'
    
    if module.startswith('@kit.'):
        return 'kit_module'
    
    if module.startswith('@ohos.'):
        module_base = module.split('/')[0]
        return 'api_module'
    
    return 'unknown'

def classify_import_c(header: str) -> str:
    """分类C include语句
    
    返回值：
    - 'c_api': 被测C API头文件（sdk_c下的头文件）
    - 'internal_module': 内部模块（相对路径）
    - 'test_framework': 测试框架头文件（跳过）
    - 'system_header': 系统头文件（跳过）
    - 'unknown': 未知类型
    """
    
    header_name = os.path.basename(header)
    
    # 测试框架头文件
    for tf in TEST_FRAMEWORKS_C:
        if header_name.lower() == tf or header_name.lower().endswith(tf):
            return 'test_framework'
    
    # 相对路径
    if header.startswith('./') or header.startswith('../'):
        return 'internal_module'
    
    # OpenHarmony C API特征（常见头文件名）
    oh_c_api_patterns = [
        r'^oh_',
        r'^native_',
        r'^hiappevent',
        r'^hilog',
        r'^napi',
        r'^ability_',
        r'^bundle_',
        r'^window_',
        r'^display_',
        r'^image_',
        r'^audio_',
        r'^camera_',
        r'^media_',
        r'^sensor_',
        r'^bluetooth_',
        r'^wifi_',
        r'^network_',
        r'^file_',
        r'^data_',
        r'^account_',
        r'^security_',
        r'^power_',
        r'^battery_',
        r'^input_method_',
        r'^web_',
        r'^arkui_',
        r'^ace_',
    ]
    
    for pattern in oh_c_api_patterns:
        if re.match(pattern, header_name.lower()):
            return 'c_api'
    
    # 如果路径包含常见子系统名
    subsystem_patterns = [
        'hiviewdfx',
        'graphic',
        'multimedia',
        'arkui',
        'ability',
        'bundle',
        'window',
        'display',
        'image',
        'audio',
        'camera',
        'media',
        'sensor',
        'bluetooth',
        'wifi',
        'network',
        'file',
        'data',
        'account',
        'security',
        'power',
        'battery',
        'input',
        'web',
    ]
    
    for pattern in subsystem_patterns:
        if pattern in header.lower():
            return 'c_api'
    
    return 'unknown'

def process_imports(imports: List[Dict], language: str) -> Dict:
    """处理import列表，分类并筛选"""
    
    test_apis = []
    
    for imp in imports:
        # 分类
        if language in ['typescript']:
            imp['type'] = classify_import_js(imp['module'])
        else:
            imp['type'] = classify_import_c(imp['module'])
        
        # 标记是否跳过
        imp['skip'] = imp['type'] in ['test_framework', 'unknown', 'system_header']
        
        # 收集需要查询的被测API
        if imp['type'] in ['api_module', 'kit_module', 'c_api']:
            test_apis.append({
                'module': imp['module'],
                'imported_names': imp['imported_names'],
                'type': imp['type'],
                'include_type': imp.get('include_type', 'import')
            })
    
    return {
        'imports': imports,
        'test_apis': test_apis
    }

def main():
    parser = argparse.ArgumentParser(description='提取import/include语句并分类')
    parser.add_argument('file', help='源码文件路径')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    # 检测语言类型
    language = detect_language(args.file)
    
    # 根据语言类型提取
    if language in ['typescript']:
        imports = extract_js_imports(args.file)
    elif language in ['cpp', 'header']:
        imports = extract_c_includes(args.file)
    else:
        imports = []
    
    if not imports:
        result = {
            'status': 'ok',
            'file': args.file,
            'language': language,
            'message': '未找到import/include语句',
            'imports': [],
            'test_apis': []
        }
    else:
        processed = process_imports(imports, language)
        
        result = {
            'status': 'ok',
            'file': args.file,
            'language': language,
            'imports': processed['imports'],
            'test_apis': processed['test_apis']
        }
    
    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"文件: {args.file}")
        print(f"语言: {language}")
        print(f"import/include总数: {len(result['imports'])}")
        print(f"被测API数: {len(result['test_apis'])}")
        print("\n列表:")
        for imp in result['imports']:
            skip_mark = " [跳过]" if imp.get('skip') else ""
            print(f"  行{imp['line']}: {imp['module']} ({imp['type']}){skip_mark}")
        
        print("\n被测API:")
        for api in result['test_apis']:
            print(f"  {api['module']} ({api['type']})")

if __name__ == '__main__':
    main()