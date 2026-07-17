#!/usr/bin/env python3
"""
generate_evidence_chain.py - 自动生成证据链追溯

功能：
1. 读取测试源码文件，提取import语句
2. 解析kit和模块名
3. 查询domain和subsystem
4. 生成标准格式的证据链追溯（Markdown格式）

用法：
    python3 generate_evidence_chain.py <源码文件路径> --test-case <用例名称>

输出：
    Markdown格式的证据链追溯（可直接粘贴到报告）
"""

import os
import re
import json
import argparse
import subprocess
from typing import List, Dict, Optional
from pathlib import Path

class EvidenceChainGenerator:
    """证据链生成器"""
    
    def __init__(self, script_dir: str):
        self.script_dir = script_dir
        self.extract_imports_script = os.path.join(script_dir, 'extract_imports.py')
        self.explore_chain_script = os.path.join(script_dir, 'explore_import_chain.py')
        self.map_domain_script = os.path.join(script_dir, 'map_domain.py')
    
    def extract_imports(self, file_path: str) -> Dict:
        """提取import语句"""
        try:
            result = subprocess.run(
                ['python3', self.extract_imports_script, file_path, '--format', 'json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"❌ 提取import失败: {e}")
        return {'status': 'error', 'imports': [], 'test_apis': []}
    
    def explore_chain(self, file_path: str, max_depth: int = 3) -> Dict:
        """探索引用链"""
        try:
            result = subprocess.run(
                ['python3', self.explore_chain_script, file_path, '--max-depth', str(max_depth), '--format', 'json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"❌ 探索引用链失败: {e}")
        return {'status': 'error', 'all_apis': []}
    
    def query_domain(self, module: str, imported_names: List[str] = None) -> Dict:
        """查询domain
        
        Args:
            module: 模块名（如@kit.ArkTS或@ohos.util.stream）
            imported_names: 引用的变量名列表（如['stream']）
        """
        try:
            result = subprocess.run(
                ['python3', self.map_domain_script, module],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                # 如果是kit，需要展开并找到具体模块
                if data.get('status') == 'expanded':
                    kit_name = data.get('kit', '')
                    modules = data.get('modules', [])
                    mappings = data.get('mappings', [])
                    
                    # 尝试匹配import的名称（如stream对应@ohos.util.stream）
                    matched_module = None
                    matched_mapping = None
                    
                    if imported_names:
                        # 查找包含imported_name的模块
                        for imp_name in imported_names:
                            for i, mod in enumerate(modules):
                                if imp_name.lower() in mod.lower():
                                    matched_module = mod
                                    if i < len(mappings):
                                        matched_mapping = mappings[i]
                                    break
                            if matched_module:
                                break
                    
                    # 如果没找到匹配的，使用第一个mapped的模块
                    if not matched_mapping:
                        for mapping in mappings:
                            if mapping.get('status') == 'mapped':
                                matched_mapping = mapping
                                matched_module = mapping.get('module')
                                break
                    
                    if matched_mapping:
                        return {
                            'status': 'mapped',
                            'module': matched_module or module,
                            'domain': matched_mapping.get('domain'),
                            'subsystem': matched_mapping.get('subsystem'),
                            'kit': kit_name,
                            'expanded': True
                        }
                
                return data
        except Exception as e:
            pass
        return {'status': 'error', 'module': module}
    
    def generate_evidence_chain_markdown(
        self,
        source_file: str,
        test_case: str,
        api_list: List[Dict],
        include_layer: bool = True
    ) -> str:
        """生成Markdown格式的证据链追溯"""
        
        # 提取文件名
        file_name = os.path.basename(source_file)
        
        # 生成表格
        markdown = f"#### 3.X.3 源码→领域证据链\n\n"
        markdown += f"⚠️ **强制要求**: 此段落必须独立展示，包含表格和证据链追溯图。\n\n"
        markdown += f"| API | 子系统 | domain | 日志行 | 时间 |\n"
        markdown += f"|-----|--------|--------|--------|------|\n"
        
        for api in api_list[:5]:  # 限制最多5个API
            module = api.get('module', '未知')
            subsystem = api.get('subsystem', '未知')
            domain = api.get('domain', '未知')
            
            # 处理domain格式
            if domain and domain != '未知':
                domain_short = domain.replace('0xD00', 'C00')[:7]
            else:
                domain_short = '未知'
            
            layer_info = f" [第{api.get('layer', 1)}层]" if include_layer else ""
            markdown += f"| {module} | {subsystem} | {domain_short} | 待补充 | 待补充 |\n"
        
        # 生成证据链追溯图
        markdown += f"\n**证据链追溯**:\n"
        markdown += f"```\n"
        markdown += f"失败用例源码({file_name})\n"
        
        # 根据API类型生成不同的追溯路径
        for api in api_list[:3]:  # 只显示前3个API的追溯路径
            module = api.get('module', '')
            original_module = api.get('original_module', module)
            api_type = api.get('type', 'api_module')
            imported_names = api.get('imported_names', [''])
            
            if api_type == 'kit_module':
                # Kit引用路径
                kit_name = original_module.replace('@kit.', '')
                markdown += f"    │ import {{ {imported_names[0] if imported_names else ''} }} from '@kit.{kit_name}';  ← 实际源码引用\n"
                markdown += f"    ▼\n"
                markdown += f"@kit.{kit_name} 展开\n"
                markdown += f"    │ 查询 kit_module 表 → 找到 {module}\n"
                markdown += f"    ▼\n"
            elif api_type == 'api_module':
                # 直接引用路径
                markdown += f"    │ import {{ {imported_names[0] if imported_names else ''} }} from '{original_module}';  ← 实际源码引用\n"
                markdown += f"    ▼\n"
            elif api_type == 'internal_module':
                # 内部模块路径
                layer = api.get('layer', 2)
                markdown += f"    │ import {{ {imported_names[0] if imported_names else ''} }} from '{original_module}';  ← 第1层：内部模块\n"
                markdown += f"    ▼\n"
                markdown += f"内部模块({original_module}) - 第{layer}层\n"
                markdown += f"    │ import {{ ... }} from '@ohos.XXX';  ← 实际API引用\n"
                markdown += f"    ▼\n"
            
            # 统一的后续路径
            subsystem = api.get('subsystem', '未知')
            domain = api.get('domain', '未知')
            domain_short = domain.replace('0xD00', 'C00')[:7] if domain and domain != '未知' else '未知'
            
            markdown += f"@ohos API → domain\n"
            markdown += f"    │ {module} → {domain} → {subsystem}\n"
            markdown += f"    ▼\n"
            markdown += f"精准日志过滤\n"
            markdown += f"    │ 过滤域：{domain_short}/\n"
            markdown += f"    ▼\n"
            markdown += f"日志切片 → 行xxx-xxx\n"
            markdown += f"```\n\n"
            break  # 只显示一个完整的追溯路径
        
        # 生成Domain归属说明
        markdown += f"**Domain归属说明**（经map_domain.py验证）：\n"
        for api in api_list[:3]:
            module = api.get('module', '')
            subsystem = api.get('subsystem', '未知')
            domain = api.get('domain', '未知')
            layer = api.get('layer', 1)
            
            if api.get('type') == 'kit_module':
                markdown += f"- `{module}` → 展开 → `@ohos.XXX` → `{domain}` → **{subsystem}**\n"
            else:
                markdown += f"- `{module}` → `{domain}` → **{subsystem}** (第{layer}层)\n"
        
        # 生成查询工具说明
        markdown += f"\n**查询工具**: `python3 map_domain.py \"{api_list[0].get('module', '')}\"`\n"
        
        return markdown
    
    def generate_for_test_file(
        self,
        source_file: str,
        test_case: str = None,
        explore_internal: bool = True,
        max_depth: int = 3
    ) -> str:
        """为测试文件生成证据链"""
        
        print(f"📂 分析文件: {source_file}")
        
        # 步骤1：提取import
        imports_result = self.extract_imports(source_file)
        
        if imports_result.get('status') != 'ok':
            return "❌ 无法提取import语句"
        
        test_apis = imports_result.get('test_apis', [])
        
        print(f"✅ 发现 {len(test_apis)} 个直接引用的API")
        
        # 步骤2：探索引用链（如果有内部模块）
        all_apis = []
        
        if explore_internal:
            chain_result = self.explore_chain(source_file, max_depth)
            all_apis = chain_result.get('all_apis', [])
            print(f"✅ 发现 {len(all_apis)} 个API（包含内部模块引用）")
        else:
            # 只使用直接引用的API
            for api in test_apis:
                # 查询domain，传入imported_names以便匹配kit中的模块
                domain_info = self.query_domain(api['module'], api.get('imported_names', []))
                api['domain'] = domain_info.get('domain')
                api['subsystem'] = domain_info.get('subsystem')
                api['layer'] = 1
                
                # 如果kit展开后找到了具体模块，更新模块名
                if domain_info.get('expanded') and domain_info.get('module'):
                    api['expanded_module'] = domain_info.get('module')
                
                all_apis.append(api)
        
        if not all_apis:
            return "❌ 未发现被测API"
        
        # 步骤3：生成Markdown
        markdown = self.generate_evidence_chain_markdown(
            source_file,
            test_case,
            all_apis,
            include_layer=explore_internal
        )
        
        return markdown

def main():
    parser = argparse.ArgumentParser(description='自动生成证据链追溯')
    parser.add_argument('file', help='测试源码文件路径')
    parser.add_argument('--test-case', help='测试用例名称（可选）')
    parser.add_argument('--explore-internal', action='store_true', default=True, help='探索内部模块引用链')
    parser.add_argument('--max-depth', type=int, default=3, help='最大探索深度')
    parser.add_argument('--output', help='输出文件路径（可选）')
    
    args = parser.parse_args()
    
    # 获取脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建生成器
    generator = EvidenceChainGenerator(script_dir)
    
    # 生成证据链
    markdown = generator.generate_for_test_file(
        args.file,
        args.test_case,
        args.explore_internal,
        args.max_depth
    )
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"\n✅ 证据链已保存到: {args.output}")
    else:
        print("\n" + "="*80)
        print(markdown)

if __name__ == '__main__':
    main()