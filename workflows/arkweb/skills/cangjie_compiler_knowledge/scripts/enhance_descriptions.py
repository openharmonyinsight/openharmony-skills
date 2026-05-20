#!/usr/bin/env python3
"""
enhance_descriptions.py - 增强描述文件工具
自动为描述文件添加代码示例、FAQ、关系图谱等内容
"""

import os
import json
import argparse
from typing import Dict, List, Set
from pathlib import Path


class DescriptionEnhancer:
    """描述文件增强器"""
    
    def __init__(self, knowledge_base_dir: str, source_dir: str):
        """
        初始化增强器
        
        Args:
            knowledge_base_dir: 知识库目录
            source_dir: 源码目录
        """
        self.kb_dir = Path(knowledge_base_dir)
        self.source_dir = Path(source_dir)
        self.descriptions_dir = self.kb_dir / 'descriptions'
        self.search_index_path = self.kb_dir / 'search-index.json'
        self.cross_ref_path = self.kb_dir / 'cross-references.json'
        
        # 加载索引
        self.search_index = self._load_json(self.search_index_path)
        self.cross_refs = self._load_json(self.cross_ref_path)
    
    def _load_json(self, path: Path) -> Dict:
        """加载 JSON 文件"""
        if not path.exists():
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_code_examples(self, keyword: str, max_examples: int = 3) -> List[Dict]:
        """
        从源码中提取代码示例
        
        Args:
            keyword: 关键词
            max_examples: 最大示例数
            
        Returns:
            代码示例列表
        """
        examples = []
        
        # 从搜索索引中获取相关函数
        keywords_data = self.search_index.get('keywords', {})
        keyword_info = keywords_data.get(keyword, {})
        functions = keyword_info.get('functions', [])[:max_examples]
        
        for func in functions:
            file_path = self.source_dir / func['file']
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        start_line = max(0, func['line'] - 1)
                        end_line = min(len(lines), start_line + 20)
                        code = ''.join(lines[start_line:end_line])
                        
                        examples.append({
                            'function': func['name'],
                            'file': func['file'],
                            'line': func['line'],
                            'code': code.strip()
                        })
                except Exception as e:
                    print(f"警告: 无法读取文件 {file_path}: {e}")
        
        return examples
    
    def generate_concept_graph(self, keyword: str) -> Dict:
        """
        生成概念关系图谱
        
        Args:
            keyword: 关键词
            
        Returns:
            关系图谱数据
        """
        keywords_data = self.search_index.get('keywords', {})
        keyword_info = keywords_data.get(keyword, {})
        
        graph = {
            'keyword': keyword,
            'synonyms': keyword_info.get('synonyms', []),
            'related': keyword_info.get('related', []),
            'modules': keyword_info.get('modules', []),
            'dependencies': []
        }
        
        # 添加模块依赖
        module_deps = self.cross_refs.get('module_dependencies', {})
        for module in graph['modules']:
            if module in module_deps:
                deps = module_deps[module].get('dependencies', [])
                graph['dependencies'].extend(deps)
        
        graph['dependencies'] = list(set(graph['dependencies']))
        
        return graph
    
    def generate_faq(self, keyword: str) -> List[Dict]:
        """
        生成常见问题（基于模板）
        
        Args:
            keyword: 关键词
            
        Returns:
            FAQ 列表
        """
        # 这里提供一些通用的 FAQ 模板
        # 实际使用时需要根据具体概念定制
        faq_templates = [
            {
                'question': f'{keyword} 是什么？',
                'answer': f'请参考上面的概念描述部分。'
            },
            {
                'question': f'如何在代码中使用 {keyword}？',
                'answer': f'请参考下面的代码示例部分。'
            },
            {
                'question': f'{keyword} 在编译器的哪个阶段处理？',
                'answer': f'请查看相关模块部分了解处理流程。'
            }
        ]
        
        return faq_templates
    
    def enhance_description_file(self, keyword: str, add_examples: bool = True,
                                 add_faq: bool = True, add_graph: bool = True):
        """
        增强单个描述文件
        
        Args:
            keyword: 关键词
            add_examples: 是否添加代码示例
            add_faq: 是否添加 FAQ
            add_graph: 是否添加关系图谱
        """
        # 查找对应的描述文件
        desc_file = None
        for file in self.descriptions_dir.glob('*.md'):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                if f'keyword: {keyword}' in content:
                    desc_file = file
                    break
        
        if not desc_file:
            print(f"未找到关键词 '{keyword}' 的描述文件")
            return
        
        print(f"增强描述文件: {desc_file.name}")
        
        # 读取现有内容
        with open(desc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有增强内容
        if '## 代码示例' in content:
            print("  文件已包含代码示例，跳过")
            return
        
        # 生成增强内容
        enhancements = []
        
        if add_examples:
            examples = self.extract_code_examples(keyword)
            if examples:
                enhancements.append('\n## 代码示例\n')
                for i, ex in enumerate(examples, 1):
                    enhancements.append(f'\n### 示例 {i}: {ex["function"]}\n')
                    enhancements.append(f'文件: `{ex["file"]}:{ex["line"]}`\n\n')
                    enhancements.append(f'```cpp\n{ex["code"]}\n```\n')
        
        if add_graph:
            graph = self.generate_concept_graph(keyword)
            enhancements.append('\n## 概念关系图谱\n\n')
            enhancements.append(f'- **同义词**: {", ".join(graph["synonyms"]) if graph["synonyms"] else "无"}\n')
            enhancements.append(f'- **相关概念**: {", ".join(graph["related"]) if graph["related"] else "无"}\n')
            enhancements.append(f'- **相关模块**: {", ".join(graph["modules"]) if graph["modules"] else "无"}\n')
            if graph['dependencies']:
                enhancements.append(f'- **模块依赖**: {", ".join(graph["dependencies"][:10])}\n')
        
        if add_faq:
            faq = self.generate_faq(keyword)
            enhancements.append('\n## 常见问题\n\n')
            for item in faq:
                enhancements.append(f'### {item["question"]}\n\n')
                enhancements.append(f'{item["answer"]}\n\n')
        
        # 写入增强后的内容
        enhanced_content = content + ''.join(enhancements)
        with open(desc_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        print(f"  ✓ 已增强")
    
    def enhance_all_descriptions(self, add_examples: bool = True,
                                 add_faq: bool = True, add_graph: bool = True):
        """
        增强所有描述文件
        
        Args:
            add_examples: 是否添加代码示例
            add_faq: 是否添加 FAQ
            add_graph: 是否添加关系图谱
        """
        print("开始增强所有描述文件...")
        
        # 获取所有关键词
        keywords_data = self.search_index.get('keywords', {})
        
        # 只处理有描述文件的关键词
        processed = 0
        for desc_file in self.descriptions_dir.glob('*.md'):
            with open(desc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取 keyword
                for line in content.split('\n'):
                    if line.startswith('keyword:'):
                        keyword = line.split(':', 1)[1].strip()
                        self.enhance_description_file(
                            keyword,
                            add_examples=add_examples,
                            add_faq=add_faq,
                            add_graph=add_graph
                        )
                        processed += 1
                        break
        
        print(f"\n完成！共处理 {processed} 个描述文件")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='增强知识库描述文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 增强所有描述文件
  python3 enhance_descriptions.py
  
  # 只增强特定关键词
  python3 enhance_descriptions.py --keyword lambda
  
  # 不添加 FAQ
  python3 enhance_descriptions.py --no-faq
        """
    )
    
    parser.add_argument(
        '--knowledge-base',
        default='../knowledge-base',
        help='知识库目录 (默认: ../knowledge-base)'
    )
    
    parser.add_argument(
        '--source-dir',
        default='../../../../cangjie_compiler',
        help='源码目录 (默认: ../../../../cangjie_compiler)'
    )
    
    parser.add_argument(
        '--keyword',
        help='只增强指定关键词的描述文件'
    )
    
    parser.add_argument(
        '--no-examples',
        action='store_true',
        help='不添加代码示例'
    )
    
    parser.add_argument(
        '--no-faq',
        action='store_true',
        help='不添加 FAQ'
    )
    
    parser.add_argument(
        '--no-graph',
        action='store_true',
        help='不添加关系图谱'
    )
    
    args = parser.parse_args()
    
    # 创建增强器
    enhancer = DescriptionEnhancer(
        knowledge_base_dir=args.knowledge_base,
        source_dir=args.source_dir
    )
    
    # 执行增强
    if args.keyword:
        enhancer.enhance_description_file(
            keyword=args.keyword,
            add_examples=not args.no_examples,
            add_faq=not args.no_faq,
            add_graph=not args.no_graph
        )
    else:
        enhancer.enhance_all_descriptions(
            add_examples=not args.no_examples,
            add_faq=not args.no_faq,
            add_graph=not args.no_graph
        )


if __name__ == '__main__':
    main()
