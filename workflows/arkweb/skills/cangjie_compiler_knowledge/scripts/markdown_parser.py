#!/usr/bin/env python3
"""
MarkdownParser - Markdown 解析器
解析 AI 维护的 Markdown 描述文件，提取概念描述、同义词、相关术语等信息
"""

import os
import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DescriptionEntry:
    """描述条目数据类"""
    keyword: str  # 主关键词
    synonyms: List[str]  # 同义词列表
    related: List[str]  # 相关概念列表
    category: Optional[str]  # 类别
    concept_name: str  # 概念名称
    description_zh: Optional[str]  # 中文描述
    description_en: Optional[str]  # 英文描述
    use_cases: List[str]  # 使用场景
    implementation_notes: Optional[str]  # 实现说明
    file_path: str  # 文件路径


class MarkdownParser:
    """Markdown 解析器"""
    
    def __init__(self):
        """初始化解析器"""
        pass
    
    def parse_description_file(self, file_path: str) -> Optional[DescriptionEntry]:
        """
        解析单个 Markdown 描述文件
        
        Args:
            file_path: Markdown 文件路径
        
        Returns:
            DescriptionEntry 对象，如果解析失败返回 None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 YAML front matter
            front_matter = self._parse_front_matter(content)
            if not front_matter:
                print(f"警告: {file_path} 缺少 YAML front matter")
                return None
            
            # 验证必需字段
            if not self.validate_format(content):
                print(f"警告: {file_path} 格式不符合规范")
                return None
            
            # 提取概念名称（一级标题）
            concept_name = self._extract_concept_name(content)
            if not concept_name:
                print(f"警告: {file_path} 缺少概念名称（一级标题）")
                return None
            
            # 提取中文描述
            description_zh = self._extract_section(content, '中文描述')
            
            # 提取英文描述
            description_en = self._extract_section(content, 'English Description')
            
            # 验证至少有一种语言的描述
            if not description_zh and not description_en:
                print(f"警告: {file_path} 缺少描述（中文或英文）")
                return None
            
            # 提取使用场景
            use_cases = self._extract_list_items(content, '使用场景')
            
            # 提取实现说明
            implementation_notes = self._extract_section(content, '相关实现')
            
            # 构建 DescriptionEntry
            entry = DescriptionEntry(
                keyword=front_matter.get('keyword', ''),
                synonyms=front_matter.get('synonyms', []),
                related=front_matter.get('related', []),
                category=front_matter.get('category'),
                concept_name=concept_name,
                description_zh=description_zh,
                description_en=description_en,
                use_cases=use_cases,
                implementation_notes=implementation_notes,
                file_path=file_path
            )
            
            return entry
            
        except Exception as e:
            print(f"错误: 解析文件 {file_path} 失败: {e}")
            return None
    
    def load_all_descriptions(self, descriptions_dir: str) -> Dict[str, DescriptionEntry]:
        """
        加载 descriptions/ 目录下所有描述文件
        
        Args:
            descriptions_dir: descriptions 目录路径
        
        Returns:
            关键词到 DescriptionEntry 的映射字典
        """
        descriptions = {}
        
        if not os.path.exists(descriptions_dir):
            print(f"警告: 目录不存在: {descriptions_dir}")
            return descriptions
        
        # 遍历目录下所有 .md 文件
        for filename in os.listdir(descriptions_dir):
            if not filename.endswith('.md'):
                continue
            
            file_path = os.path.join(descriptions_dir, filename)
            entry = self.parse_description_file(file_path)
            
            if entry:
                # 使用 keyword 作为键
                descriptions[entry.keyword] = entry
                print(f"✓ 加载描述: {entry.keyword} ({filename})")
            else:
                print(f"✗ 跳过无效文件: {filename}")
        
        print(f"\n共加载 {len(descriptions)} 个描述文件")
        return descriptions
    
    def validate_format(self, content: str) -> bool:
        """
        验证 Markdown 格式是否符合规范
        
        必需字段:
        - YAML front matter 中的 keyword
        - 一级标题（概念名称）
        - 至少一种语言的描述（中文描述或 English Description）
        
        Args:
            content: Markdown 文件内容
        
        Returns:
            是否符合规范
        """
        # 检查 YAML front matter
        front_matter = self._parse_front_matter(content)
        if not front_matter:
            return False
        
        # 检查 keyword 字段
        if 'keyword' not in front_matter or not front_matter['keyword']:
            print("错误: 缺少必需字段 'keyword'")
            return False
        
        # 检查一级标题
        concept_name = self._extract_concept_name(content)
        if not concept_name:
            print("错误: 缺少一级标题（概念名称）")
            return False
        
        # 检查至少有一种语言的描述
        description_zh = self._extract_section(content, '中文描述')
        description_en = self._extract_section(content, 'English Description')
        
        if not description_zh and not description_en:
            print("错误: 缺少描述（至少需要中文描述或 English Description）")
            return False
        
        return True
    
    def _parse_front_matter(self, content: str) -> Optional[Dict]:
        """
        解析 YAML front matter
        
        Args:
            content: Markdown 文件内容
        
        Returns:
            解析后的字典，如果没有 front matter 返回 None
        """
        # 匹配 YAML front matter (--- ... ---)
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
        
        yaml_content = match.group(1)
        front_matter = {}
        
        # 简单的 YAML 解析（只支持基本格式）
        for line in yaml_content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # 解析 key: value
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # 解析列表 [item1, item2, ...]
                if value.startswith('[') and value.endswith(']'):
                    # 移除方括号并分割
                    items = value[1:-1].split(',')
                    front_matter[key] = [item.strip() for item in items if item.strip()]
                else:
                    front_matter[key] = value
        
        return front_matter
    
    def _extract_concept_name(self, content: str) -> Optional[str]:
        """
        提取概念名称（一级标题）
        
        Args:
            content: Markdown 文件内容
        
        Returns:
            概念名称，如果没有返回 None
        """
        # 移除 YAML front matter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        
        # 匹配一级标题 # Title
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        return None
    
    def _extract_section(self, content: str, section_title: str) -> Optional[str]:
        """
        提取指定章节的内容
        
        Args:
            content: Markdown 文件内容
            section_title: 章节标题（不含 ##）
        
        Returns:
            章节内容，如果没有返回 None
        """
        # 匹配 ## Section Title 后的内容，直到下一个 ## 或文件结束
        pattern = rf'^##\s+{re.escape(section_title)}\s*\n(.*?)(?=^##|\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        
        if match:
            section_content = match.group(1).strip()
            return section_content if section_content else None
        
        return None
    
    def _extract_list_items(self, content: str, section_title: str) -> List[str]:
        """
        提取指定章节中的列表项
        
        Args:
            content: Markdown 文件内容
            section_title: 章节标题（不含 ##）
        
        Returns:
            列表项列表
        """
        section_content = self._extract_section(content, section_title)
        if not section_content:
            return []
        
        # 匹配列表项 - item 或 * item
        items = re.findall(r'^[-*]\s+(.+)$', section_content, re.MULTILINE)
        return [item.strip() for item in items if item.strip()]


if __name__ == '__main__':
    # 测试代码
    parser = MarkdownParser()
    
    # 测试示例 Markdown 内容
    test_content = """---
keyword: lambda
synonyms: [匿名函数, anonymous function, closure]
related: [function, closure, capture]
category: language-feature
---

# Lambda 表达式

## 中文描述
Lambda 表达式是仓颉语言中的匿名函数特性，支持捕获外部变量。

## English Description
Lambda expressions are anonymous function features in Cangjie language, supporting variable capture.

## 使用场景
- 函数式编程
- 回调函数
- 高阶函数参数

## 相关实现
- LambdaExpr 类 (src/Parse/Lambda.h)
- BuildLambdaClosure 函数 (src/Sema/Lambda.cpp)
"""
    
    # 创建临时测试文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        print("=== 测试解析单个文件 ===")
        entry = parser.parse_description_file(temp_file)
        
        if entry:
            print(f"✓ 解析成功")
            print(f"  关键词: {entry.keyword}")
            print(f"  同义词: {entry.synonyms}")
            print(f"  相关概念: {entry.related}")
            print(f"  类别: {entry.category}")
            print(f"  概念名称: {entry.concept_name}")
            print(f"  中文描述: {entry.description_zh[:50]}..." if entry.description_zh else "  中文描述: None")
            print(f"  英文描述: {entry.description_en[:50]}..." if entry.description_en else "  英文描述: None")
            print(f"  使用场景: {entry.use_cases}")
        else:
            print("✗ 解析失败")
        
        print("\n=== 测试格式验证 ===")
        is_valid = parser.validate_format(test_content)
        print(f"格式验证: {'✓ 通过' if is_valid else '✗ 失败'}")
        
    finally:
        # 清理临时文件
        os.unlink(temp_file)
    
    print("\n=== 测试完成 ===")
