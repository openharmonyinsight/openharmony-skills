#!/usr/bin/env python3
"""
explore_import_chain.py - 探索引用链（支持3层探索）

功能：
1. 提取测试文件的import语句
2. 探索内部模块的引用链（最多3层）
3. 汇总所有被测API
4. 生成引用链树（JSON格式）

用法：
    python3 explore_import_chain.py <测试文件路径> --max-depth 3

输出：
    {
      "root": {...},
      "all_apis": [
        {"module": "@ohos.arkui.inspector", "domain": "0xD003900", "layer": 2},
        ...
      ],
      "explored_files": ["Test.test.ets", "Utils.ets", ...]
    }
"""

import os
import re
import json
import argparse
import subprocess
from typing import List, Dict, Set, Optional
from pathlib import Path

# 测试框架模块列表
TEST_FRAMEWORKS = [
    '@ohos.hypium',
    '@ohos.UiTest',
    '@ohos.hypium-binary',
    '@ohos.test',
    '@kit.TestKit'
]

def extract_imports(file_path: str) -> List[Dict]:
    """提取文件中的import语句"""
    imports = []
    
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_no, line in enumerate(f, 1):
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
                    'imported_names': imported_names
                })
    
    return imports

def classify_import(module: str) -> str:
    """分类import语句"""
    
    if module.startswith('./') or module.startswith('../'):
        return 'internal_module'
    
    for tf in TEST_FRAMEWORKS:
        if module == tf or module.startswith(tf + '/'):
            return 'test_framework'
    
    if module.startswith('@kit.'):
        return 'kit_module'
    
    if module.startswith('@ohos.'):
        module_base = module.split('/')[0]
        return 'api_module'
    
    return 'unknown'

def resolve_relative_path(current_file: str, module: str) -> Optional[str]:
    """解析相对路径，返回绝对路径"""
    current_dir = os.path.dirname(current_file)
    
    extensions = ['.ets', '.ts', '.js', '']
    
    for ext in extensions:
        target_path = os.path.normpath(os.path.join(current_dir, module + ext))
        if os.path.exists(target_path):
            return target_path
    
    return None

def query_domain(module: str, script_dir: str, imported_names: List[str] = None) -> Dict:
    """查询API模块的domain（调用map_domain.py）
    
    Args:
        module: 模块名
        script_dir: 脚本目录
        imported_names: 引用的变量名列表（用于匹配kit中的具体模块）
    """
    try:
        script_path = os.path.join(script_dir, 'map_domain.py')
        result = subprocess.run(
            [sys.executable, script_path, module],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            
            # 如果是kit展开结果，找到具体模块
            if data.get('status') == 'expanded':
                modules = data.get('modules', [])
                mappings = data.get('mappings', [])
                
                # 尝试匹配import的名称
                matched_mapping = None
                if imported_names:
                    for imp_name in imported_names:
                        for i, mod in enumerate(modules):
                            if imp_name.lower() in mod.lower():
                                if i < len(mappings) and mappings[i].get('status') == 'mapped':
                                    matched_mapping = mappings[i]
                                    break
                        if matched_mapping:
                            break
                
                # 如果没找到，使用第一个mapped的模块
                if not matched_mapping:
                    for mapping in mappings:
                        if mapping.get('status') == 'mapped':
                            matched_mapping = mapping
                            break
                
                if matched_mapping:
                    return {
                        'status': 'mapped',
                        'domain': matched_mapping.get('domain'),
                        'subsystem': matched_mapping.get('subsystem'),
                        'kit': data.get('kit'),
                        'expanded_module': matched_mapping.get('module')
                    }
            
            return data
    except Exception as e:
        pass
    
    return {'status': 'error', 'module': module, 'reason': '查询失败'}

def explore_import_chain_recursive(
    file_path: str,
    max_depth: int,
    current_depth: int,
    explored_files: Set[str],
    script_dir: str
) -> Optional[Dict]:
    """递归探索引用链"""
    
    # 检查是否已探索（避免重复）
    if file_path in explored_files:
        return None
    
    # 检查是否超过最大深度
    if current_depth > max_depth:
        return None
    
    # 标记为已探索
    explored_files.add(file_path)
    
    # 提取import
    imports = extract_imports(file_path)
    
    if not imports:
        return None
    
    # 分类import
    for imp in imports:
        imp['type'] = classify_import(imp['module'])
    
    # 构建节点
    node = {
        'file': file_path,
        'layer': current_depth,
        'imports': [],
        'children': []
    }
    
    all_apis = []
    
    for imp in imports:
        if imp['type'] in ['api_module', 'kit_module']:
            # 查询domain（传入imported_names以便匹配kit中的具体模块）
            domain_info = query_domain(imp['module'], script_dir, imp.get('imported_names', []))
            
            # 确定最终显示的模块名
            display_module = imp['module']
            if domain_info.get('expanded_module'):
                display_module = domain_info['expanded_module']
            
            api_node = {
                'file': file_path,
                'module': display_module,  # 使用展开后的模块名
                'original_module': imp['module'],  # 保留原始模块名
                'type': imp['type'],
                'layer': current_depth,
                'domain': domain_info.get('domain'),
                'subsystem': domain_info.get('subsystem'),
                'imported_names': imp['imported_names']
            }
            
            all_apis.append(api_node)
            node['imports'].append(api_node)
        
        elif imp['type'] == 'internal_module' and current_depth < max_depth:
            # 探索内部模块
            internal_file = resolve_relative_path(file_path, imp['module'])
            
            if internal_file and internal_file not in explored_files:
                child_tree = explore_import_chain_recursive(
                    internal_file,
                    max_depth,
                    current_depth + 1,
                    explored_files,
                    script_dir
                )
                
                if child_tree:
                    node['children'].append(child_tree)
                    all_apis.extend(child_tree.get('all_apis', []))
    
    return {
        'root': node,
        'all_apis': all_apis,
        'explored_files': list(explored_files)
    }

def main():
    parser = argparse.ArgumentParser(description='探索引用链')
    parser.add_argument('file', help='测试文件路径')
    parser.add_argument('--max-depth', type=int, default=3, help='最大探索深度（默认3）')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    # 获取脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 探索引用链
    result = explore_import_chain_recursive(
        args.file,
        args.max_depth,
        current_depth=1,
        explored_files=set(),
        script_dir=script_dir
    )
    
    if not result:
        result = {
            'status': 'error',
            'file': args.file,
            'message': '无法探索引用链'
        }
    
    # 输出结果
    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"测试文件: {args.file}")
        print(f"探索深度: {args.max_depth}")
        print(f"已探索文件: {len(result.get('explored_files', []))}个")
        print(f"发现API: {len(result.get('all_apis', []))}个")
        
        print("\n被测API列表:")
        for api in result.get('all_apis', []):
            layer_mark = f" [第{api['layer']}层]"
            domain_str = f" → {api.get('subsystem', '未知')} ({api.get('domain', '未知')})"
            print(f"  {api['module']}{domain_str}{layer_mark}")

if __name__ == '__main__':
    main()