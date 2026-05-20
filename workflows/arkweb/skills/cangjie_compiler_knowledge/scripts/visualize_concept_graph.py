#!/usr/bin/env python3
"""
visualize_concept_graph.py - 概念关系图谱可视化
生成概念间关系的可视化图谱（Mermaid 格式）
"""

import os
import json
import argparse
from typing import Dict, List, Set
from pathlib import Path


class ConceptGraphVisualizer:
    """概念关系图谱可视化器"""
    
    def __init__(self, knowledge_base_dir: str):
        """
        初始化可视化器
        
        Args:
            knowledge_base_dir: 知识库目录
        """
        self.kb_dir = Path(knowledge_base_dir)
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
    
    def generate_concept_graph(self, keyword: str, depth: int = 1) -> str:
        """
        生成概念关系图谱（Mermaid 格式）
        
        Args:
            keyword: 中心关键词
            depth: 关系深度
            
        Returns:
            Mermaid 图谱代码
        """
        keywords_data = self.search_index.get('keywords', {})
        
        if keyword not in keywords_data:
            return f"错误: 关键词 '{keyword}' 不存在"
        
        keyword_info = keywords_data[keyword]
        
        # 开始构建 Mermaid 图
        mermaid = ["graph TD"]
        mermaid.append(f'    {self._node_id(keyword)}["{keyword}"]')
        mermaid.append(f'    style {self._node_id(keyword)} fill:#f9f,stroke:#333,stroke-width:4px')
        
        # 添加同义词
        synonyms = keyword_info.get('synonyms', [])
        for syn in synonyms[:5]:
            if syn in keywords_data:
                mermaid.append(f'    {self._node_id(syn)}["{syn}"]')
                mermaid.append(f'    {self._node_id(keyword)} -.同义词.- {self._node_id(syn)}')
        
        # 添加相关概念
        related = keyword_info.get('related', [])
        for rel in related[:10]:
            if rel in keywords_data:
                mermaid.append(f'    {self._node_id(rel)}["{rel}"]')
                mermaid.append(f'    {self._node_id(keyword)} -->|相关| {self._node_id(rel)}')
        
        # 添加模块
        modules = keyword_info.get('modules', [])
        for mod in modules[:5]:
            mermaid.append(f'    {self._node_id(mod)}{{"{mod}模块"}}')
            mermaid.append(f'    {self._node_id(keyword)} -->|使用于| {self._node_id(mod)}')
            mermaid.append(f'    style {self._node_id(mod)} fill:#bbf,stroke:#333')
        
        return '\n'.join(mermaid)
    
    def _node_id(self, name: str) -> str:
        """生成节点 ID（移除特殊字符）"""
        return name.replace('-', '_').replace(' ', '_').replace(':', '_')
    
    def generate_module_dependency_graph(self, module: str = None) -> str:
        """
        生成模块依赖关系图谱
        
        Args:
            module: 模块名（None 表示所有模块）
            
        Returns:
            Mermaid 图谱代码
        """
        module_deps = self.cross_refs.get('module_dependencies', {})
        
        if not module_deps:
            return "错误: 没有模块依赖信息"
        
        mermaid = ["graph LR"]
        
        if module:
            # 只显示指定模块的依赖
            if module not in module_deps:
                return f"错误: 模块 '{module}' 不存在"
            
            deps = module_deps[module].get('dependencies', [])
            mermaid.append(f'    {module}["{module}"]')
            mermaid.append(f'    style {module} fill:#f9f,stroke:#333,stroke-width:4px')
            
            for dep in deps:
                mermaid.append(f'    {dep}["{dep}"]')
                mermaid.append(f'    {module} --> {dep}')
        else:
            # 显示所有模块的依赖（限制数量）
            count = 0
            for mod, info in list(module_deps.items())[:15]:
                deps = info.get('dependencies', [])
                mermaid.append(f'    {mod}["{mod}"]')
                for dep in deps[:3]:
                    mermaid.append(f'    {dep}["{dep}"]')
                    mermaid.append(f'    {mod} --> {dep}')
                    count += 1
                    if count > 30:
                        break
                if count > 30:
                    break
        
        return '\n'.join(mermaid)
    
    def save_graph(self, content: str, output_file: str):
        """
        保存图谱到文件
        
        Args:
            content: Mermaid 内容
            output_file: 输出文件路径
        """
        output_path = Path(output_file)
        
        # 创建完整的 Markdown 文件
        markdown = f"""# 概念关系图谱

```mermaid
{content}
```

## 说明

- 粗边框节点：中心概念
- 虚线：同义词关系
- 实线箭头：相关概念或依赖关系
- 菱形节点：模块
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        print(f"✓ 图谱已保存到: {output_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='生成概念关系图谱',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成 lambda 概念的关系图谱
  python3 visualize_concept_graph.py --keyword lambda
  
  # 生成 sema 模块的依赖图谱
  python3 visualize_concept_graph.py --module sema
  
  # 保存到文件
  python3 visualize_concept_graph.py --keyword generic --output graph.md
        """
    )
    
    parser.add_argument(
        '--knowledge-base',
        default='../knowledge-base',
        help='知识库目录 (默认: ../knowledge-base)'
    )
    
    parser.add_argument(
        '--keyword',
        help='生成指定关键词的概念图谱'
    )
    
    parser.add_argument(
        '--module',
        help='生成指定模块的依赖图谱'
    )
    
    parser.add_argument(
        '--output',
        help='输出文件路径'
    )
    
    parser.add_argument(
        '--depth',
        type=int,
        default=1,
        help='关系深度 (默认: 1)'
    )
    
    args = parser.parse_args()
    
    # 创建可视化器
    visualizer = ConceptGraphVisualizer(
        knowledge_base_dir=args.knowledge_base
    )
    
    # 生成图谱
    if args.keyword:
        content = visualizer.generate_concept_graph(args.keyword, args.depth)
    elif args.module:
        content = visualizer.generate_module_dependency_graph(args.module)
    else:
        print("错误: 请指定 --keyword 或 --module")
        return
    
    # 输出或保存
    if args.output:
        visualizer.save_graph(content, args.output)
    else:
        print(content)


if __name__ == '__main__':
    main()
