#!/usr/bin/env python3
"""
generate_new_descriptions.py - 生成新的描述文件
基于搜索索引中的关键词自动生成描述文件模板
"""

import os
import json
import argparse
from typing import Dict, List, Set
from pathlib import Path


class DescriptionGenerator:
    """描述文件生成器"""
    
    def __init__(self, knowledge_base_dir: str, source_dir: str):
        """
        初始化生成器
        
        Args:
            knowledge_base_dir: 知识库目录
            source_dir: 源码目录
        """
        self.kb_dir = Path(knowledge_base_dir)
        self.source_dir = Path(source_dir)
        self.descriptions_dir = self.kb_dir / 'descriptions'
        self.search_index_path = self.kb_dir / 'search-index.json'
        
        # 加载索引
        self.search_index = self._load_json(self.search_index_path)
        
        # 获取已有的描述文件关键词
        self.existing_keywords = self._get_existing_keywords()
    
    def _load_json(self, path: Path) -> Dict:
        """加载 JSON 文件"""
        if not path.exists():
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_existing_keywords(self) -> Set[str]:
        """获取已有描述文件的关键词"""
        keywords = set()
        for desc_file in self.descriptions_dir.glob('*.md'):
            with open(desc_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('keyword:'):
                        keyword = line.split(':', 1)[1].strip()
                        keywords.add(keyword)
                        break
        return keywords
    
    def get_candidate_keywords(self, min_functions: int = 5, min_classes: int = 1) -> List[str]:
        """
        获取候选关键词（有足够代码支持的关键词）
        
        Args:
            min_functions: 最小函数数量
            min_classes: 最小类数量
            
        Returns:
            候选关键词列表
        """
        candidates = []
        keywords_data = self.search_index.get('keywords', {})
        
        for keyword, info in keywords_data.items():
            # 跳过已有描述的关键词
            if keyword in self.existing_keywords:
                continue
            
            # 跳过太短的关键词
            if len(keyword) < 3:
                continue
            
            # 跳过纯数字或特殊字符
            if not keyword[0].isalpha():
                continue
            
            # 检查是否有足够的代码支持
            functions = info.get('functions', [])
            classes = info.get('classes', [])
            
            if len(functions) >= min_functions or len(classes) >= min_classes:
                # 计算重要性得分
                score = len(functions) + len(classes) * 2
                candidates.append((keyword, score, info))
        
        # 按得分排序
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        return [(kw, info) for kw, score, info in candidates]
    
    def generate_description_template(self, keyword: str, info: Dict) -> str:
        """
        生成描述文件模板
        
        Args:
            keyword: 关键词
            info: 关键词信息
            
        Returns:
            描述文件内容
        """
        # 提取信息
        synonyms = info.get('synonyms', [])
        related = info.get('related', [])
        modules = info.get('modules', [])
        classes = info.get('classes', [])
        functions = info.get('functions', [])
        description = info.get('description', '')
        description_en = info.get('description_en', '')
        
        # 生成文件名
        filename = keyword.lower().replace(' ', '-').replace('_', '-')
        
        # 生成内容
        content = f"""---
keyword: {keyword}
synonyms: [{', '.join(synonyms)}]
related: [{', '.join(related[:10])}]
category: compiler-feature
---

# {keyword.title()}

## 中文描述
{description if description else f'{keyword} 是仓颉编译器中的一个重要概念。'}

## English Description
{description_en if description_en else f'{keyword} is an important concept in the Cangjie compiler.'}

## 使用场景
- 待补充

## 相关实现
"""
        
        # 添加相关模块
        if modules:
            content += f"- 相关模块: {', '.join(modules[:5])}\n"
        
        # 添加主要类
        if classes:
            content += f"- 主要类: {', '.join([c['name'] for c in classes[:5]])}\n"
        
        # 添加主要函数
        if functions:
            content += f"- 主要函数: {', '.join([f['name'] for f in functions[:5]])}\n"
        
        # 添加代码示例
        if functions:
            content += "\n## 代码示例\n\n"
            for i, func in enumerate(functions[:2], 1):
                content += f"### 示例 {i}: {func['name']}\n"
                content += f"文件: `{func['file']}:{func['line']}`\n\n"
                content += "```cpp\n// 代码示例待提取\n```\n\n"
        
        # 添加关系图谱
        content += "\n## 概念关系图谱\n\n"
        content += f"- **同义词**: {', '.join(synonyms) if synonyms else '无'}\n"
        content += f"- **相关概念**: {', '.join(related[:10]) if related else '无'}\n"
        content += f"- **相关模块**: {', '.join(modules[:10]) if modules else '无'}\n"
        
        # 添加 FAQ
        content += "\n## 常见问题\n\n"
        content += f"### {keyword} 是什么？\n\n"
        content += "请参考上面的概念描述部分。\n\n"
        content += f"### 如何在代码中使用 {keyword}？\n\n"
        content += "请参考上面的代码示例部分。\n\n"
        content += f"### {keyword} 在编译器的哪个阶段处理？\n\n"
        content += "请查看相关模块部分了解处理流程。\n"
        
        return filename, content
    
    def generate_descriptions(self, max_count: int = 60, min_functions: int = 5):
        """
        生成新的描述文件
        
        Args:
            max_count: 最大生成数量
            min_functions: 最小函数数量
        """
        print(f"正在查找候选关键词...")
        candidates = self.get_candidate_keywords(min_functions=min_functions)
        
        print(f"找到 {len(candidates)} 个候选关键词")
        print(f"将生成前 {min(max_count, len(candidates))} 个描述文件\n")
        
        generated = 0
        for keyword, info in candidates[:max_count]:
            filename, content = self.generate_description_template(keyword, info)
            filepath = self.descriptions_dir / f"{filename}.md"
            
            # 检查文件是否已存在
            if filepath.exists():
                print(f"跳过: {filename}.md (已存在)")
                continue
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ 生成: {filename}.md (关键词: {keyword})")
            generated += 1
        
        print(f"\n完成！共生成 {generated} 个新描述文件")
        print(f"现有描述文件总数: {len(self.existing_keywords) + generated}")
    
    def list_candidates(self, max_count: int = 100, min_functions: int = 5):
        """
        列出候选关键词
        
        Args:
            max_count: 最大显示数量
            min_functions: 最小函数数量
        """
        candidates = self.get_candidate_keywords(min_functions=min_functions)
        
        print(f"找到 {len(candidates)} 个候选关键词\n")
        print("排名  关键词                    函数数  类数   模块数")
        print("=" * 60)
        
        for i, (keyword, info) in enumerate(candidates[:max_count], 1):
            func_count = len(info.get('functions', []))
            class_count = len(info.get('classes', []))
            module_count = len(info.get('modules', []))
            
            print(f"{i:3d}   {keyword:25s} {func_count:6d}  {class_count:4d}  {module_count:6d}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='生成新的知识库描述文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出候选关键词
  python3 generate_new_descriptions.py --list
  
  # 生成 60 个新描述文件
  python3 generate_new_descriptions.py --count 60
  
  # 只生成有至少 10 个函数的关键词
  python3 generate_new_descriptions.py --min-functions 10
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
        '--list',
        action='store_true',
        help='只列出候选关键词，不生成文件'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=60,
        help='生成的描述文件数量 (默认: 60)'
    )
    
    parser.add_argument(
        '--min-functions',
        type=int,
        default=5,
        help='最小函数数量 (默认: 5)'
    )
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = DescriptionGenerator(
        knowledge_base_dir=args.knowledge_base,
        source_dir=args.source_dir
    )
    
    # 执行操作
    if args.list:
        generator.list_candidates(
            max_count=100,
            min_functions=args.min_functions
        )
    else:
        generator.generate_descriptions(
            max_count=args.count,
            min_functions=args.min_functions
        )


if __name__ == '__main__':
    main()
