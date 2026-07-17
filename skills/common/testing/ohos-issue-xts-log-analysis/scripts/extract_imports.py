#!/usr/bin/env python3
"""
extract_imports.py - 从测试源码文件中提取import语句并分类

设计原则：
1. 自动提取所有import语句
2. 自动分类import类型（api_module / kit_module / internal_module / test_framework）
3. 提取kit引用中的具体模块名
4. 处理特殊路径引用

用法：
    python3 extract_imports.py <源码文件路径>

输出：
    {
      "status": "ok",
      "file": "StreamTest08.test.ets",
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
# 注意：import语句可能使用点号（@ohos.hypium）或斜杠（@ohos/hypium）
TEST_FRAMEWORKS = [
    '@ohos.hypium',
    '@ohos/hypium',  # 斜杠格式
    '@ohos.UiTest',
    '@ohos/UiTest',
    '@ohos.hypium-binary',
    '@ohos/hypium-binary',
    '@ohos.test',
    '@ohos/test',
    '@kit.TestKit',
    '@kit/TestKit'
]

def extract_imports(file_path: str) -> List[Dict]:
    """提取文件中的import语句"""
    imports = []
    
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_no, line in enumerate(f, 1):
            # 匹配import语句
            # 格式1: import X from 'module'
            # 格式2: import { X, Y } from 'module'
            # 格式3: import * as X from 'module'
            
            # 提取模块名
            match = re.search(r"from\s+['\"]([^'\"]+)['\"]", line)
            if match:
                module = match.group(1)
                
                # 提取引用的变量名/函数名
                imported_names = []
                # 格式: import { stream } from '@kit.ArkTS'
                names_match = re.search(r"import\s+\{([^}]+)\}", line)
                if names_match:
                    names_str = names_match.group(1)
                    # 分割多个名称
                    imported_names = [n.strip() for n in names_str.split(',') if n.strip()]
                # 格式: import stream from '@kit.ArkTS'
                elif 'import' in line and 'from' in line and '{' not in line:
                    name_match = re.search(r"import\s+(\w+)", line)
                    if name_match:
                        imported_names = [name_match.group(1)]
                
                imports.append({
                    'line': line_no,
                    'statement': line.strip(),
                    'module': module,
                    'imported_names': imported_names
                })
    
    return imports

def classify_import(module: str) -> str:
    """分类import语句
    
    返回值：
    - 'api_module': 被测API模块（需要查询domain）
    - 'kit_module': Kit引用（需要展开）
    - 'internal_module': 内部模块（需要探索引用链）
    - 'test_framework': 测试框架（跳过）
    - 'unknown': 未知类型
    """
    
    # 规则1：相对路径 → 内部模块
    if module.startswith('./') or module.startswith('../'):
        return 'internal_module'
    
    # 规则2：测试框架 → 跳过
    for tf in TEST_FRAMEWORKS:
        if module == tf or module.startswith(tf + '/'):
            return 'test_framework'
    
    # 规则3：Kit引用 → 展开
    if module.startswith('@kit.'):
        return 'kit_module'
    
    # 规则4：@ohos.XXX → API模块
    if module.startswith('@ohos.'):
        # 去除路径部分（如 @ohos.hypium-binary/src/main/indexStatic）
        module_base = module.split('/')[0]
        return 'api_module'
    
    # 默认：未知类型
    return 'unknown'

def process_imports(imports: List[Dict]) -> Dict:
    """处理import列表，分类并筛选"""
    
    test_apis = []
    
    for imp in imports:
        # 分类
        imp['type'] = classify_import(imp['module'])
        
        # 标记是否跳过
        imp['skip'] = imp['type'] in ['test_framework', 'unknown']
        
        # 收集需要查询的被测API
        if imp['type'] in ['api_module', 'kit_module']:
            test_apis.append({
                'module': imp['module'],
                'imported_names': imp['imported_names'],
                'type': imp['type']
            })
    
    return {
        'imports': imports,
        'test_apis': test_apis
    }

def main():
    parser = argparse.ArgumentParser(description='提取import语句并分类')
    parser.add_argument('file', help='源码文件路径')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    # 提取import
    imports = extract_imports(args.file)
    
    if not imports:
        result = {
            'status': 'ok',
            'file': args.file,
            'message': '未找到import语句',
            'imports': [],
            'test_apis': []
        }
    else:
        # 处理import
        processed = process_imports(imports)
        
        result = {
            'status': 'ok',
            'file': args.file,
            'imports': processed['imports'],
            'test_apis': processed['test_apis']
        }
    
    # 输出结果
    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"文件: {args.file}")
        print(f"import总数: {len(result['imports'])}")
        print(f"被测API数: {len(result['test_apis'])}")
        print("\nimport列表:")
        for imp in result['imports']:
            skip_mark = " [跳过]" if imp.get('skip') else ""
            print(f"  行{imp['line']}: {imp['module']} ({imp['type']}){skip_mark}")
        
        print("\n被测API:")
        for api in result['test_apis']:
            print(f"  {api['module']} ({api['type']})")

if __name__ == '__main__':
    main()