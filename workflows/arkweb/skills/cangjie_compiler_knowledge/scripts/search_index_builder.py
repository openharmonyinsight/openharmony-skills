#!/usr/bin/env python3
"""
SearchIndexBuilder - 搜索索引构建器
构建从关键词到代码元素的倒排索引，支持 TF-IDF 权重计算
"""

import math
from typing import Dict, List, Set
from dataclasses import dataclass, field
from collections import defaultdict

from module_analyzer import ModuleTree, ModuleInfo
from keyword_extractor import KeywordExtractor
from markdown_parser import DescriptionEntry
from cpp_parser import ClassInfo, FunctionInfo


@dataclass
class CodeLocation:
    """代码位置信息"""
    name: str
    file: str
    line: int


@dataclass
class IndexEntry:
    """索引条目"""
    keyword: str
    description: str = ""
    description_en: str = ""
    synonyms: List[str] = field(default_factory=list)
    related: List[str] = field(default_factory=list)
    modules: List[str] = field(default_factory=list)
    classes: List[CodeLocation] = field(default_factory=list)
    functions: List[CodeLocation] = field(default_factory=list)
    tfidf_score: float = 0.0


class SearchIndex:
    """搜索索引"""
    
    def __init__(self):
        self.keywords: Dict[str, IndexEntry] = {}
    
    def add_entry(self, keyword: str, entry: IndexEntry):
        """添加索引条目"""
        self.keywords[keyword] = entry
    
    def get_entry(self, keyword: str) -> IndexEntry:
        """获取索引条目"""
        return self.keywords.get(keyword)
    
    def to_dict(self) -> Dict:
        """转换为字典格式（用于 JSON 序列化）"""
        result = {"keywords": {}}
        
        for keyword, entry in self.keywords.items():
            result["keywords"][keyword] = {
                "description": entry.description,
                "description_en": entry.description_en,
                "synonyms": entry.synonyms,
                "related": entry.related,
                "modules": entry.modules,
                "classes": [
                    {"name": cls.name, "file": cls.file, "line": cls.line}
                    for cls in entry.classes
                ],
                "functions": [
                    {"name": func.name, "file": func.file, "line": func.line}
                    for func in entry.functions
                ],
                "tfidf_score": entry.tfidf_score
            }
        
        return result


class SearchIndexBuilder:
    """搜索索引构建器"""
    
    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        # 关键词到代码元素的映射（用于构建倒排索引）
        self.keyword_to_modules: Dict[str, Set[str]] = defaultdict(set)
        self.keyword_to_classes: Dict[str, List[ClassInfo]] = defaultdict(list)
        self.keyword_to_functions: Dict[str, List[FunctionInfo]] = defaultdict(list)
    
    def build_index(self, module_tree: ModuleTree, descriptions: Dict[str, DescriptionEntry] = None) -> SearchIndex:
        """
        构建搜索索引
        
        Args:
            module_tree: 模块树
            descriptions: Markdown 描述字典（可选）
        
        Returns:
            SearchIndex 对象
        """
        print("开始构建搜索索引...")
        
        # 第一步：从代码元素提取关键词，构建倒排索引
        self._build_inverted_index(module_tree)
        
        # 第二步：创建索引条目
        index = SearchIndex()
        for keyword in self.keyword_to_modules.keys():
            entry = self._create_index_entry(keyword)
            index.add_entry(keyword, entry)
        
        # 第三步：合并 Markdown 描述
        if descriptions:
            index = self.merge_descriptions(index, descriptions)
        
        # 第四步：计算 TF-IDF 权重
        self._calculate_tfidf(index)
        
        print(f"✓ 索引构建完成，共 {len(index.keywords)} 个关键词")
        return index
    
    def _build_inverted_index(self, module_tree: ModuleTree):
        """构建倒排索引"""
        print("  提取关键词并构建倒排索引...")
        
        for module in module_tree.get_all_modules():
            # 从模块名提取关键词
            module_keywords = self.keyword_extractor.extract_from_text(module.name)
            for keyword in module_keywords:
                self.keyword_to_modules[keyword].add(module.name)
            
            # 从类名提取关键词
            for class_info in module.classes:
                class_keywords = self.keyword_extractor.extract_from_class(class_info)
                for keyword in class_keywords:
                    self.keyword_to_modules[keyword].add(module.name)
                    self.keyword_to_classes[keyword].append(class_info)
            
            # 从函数名提取关键词
            for func_info in module.functions:
                func_keywords = self.keyword_extractor.extract_from_function(func_info)
                for keyword in func_keywords:
                    self.keyword_to_modules[keyword].add(module.name)
                    self.keyword_to_functions[keyword].append(func_info)
        
        print(f"  ✓ 提取了 {len(self.keyword_to_modules)} 个关键词")
    
    def _create_index_entry(self, keyword: str) -> IndexEntry:
        """创建索引条目"""
        entry = IndexEntry(keyword=keyword)
        
        # 添加模块
        entry.modules = sorted(list(self.keyword_to_modules.get(keyword, set())))
        
        # 添加类
        classes = self.keyword_to_classes.get(keyword, [])
        entry.classes = [
            CodeLocation(name=cls.name, file=cls.file, line=cls.line)
            for cls in classes
        ]
        
        # 添加函数
        functions = self.keyword_to_functions.get(keyword, [])
        entry.functions = [
            CodeLocation(name=func.name, file=func.file, line=func.line)
            for func in functions
        ]
        
        return entry
    
    def merge_descriptions(self, index: SearchIndex, descriptions: Dict[str, DescriptionEntry]) -> SearchIndex:
        """
        合并 Markdown 描述到索引
        
        Args:
            index: 搜索索引
            descriptions: Markdown 描述字典
        
        Returns:
            更新后的搜索索引
        """
        print("  合并 Markdown 描述...")
        
        merged_count = 0
        for keyword, desc_entry in descriptions.items():
            # 查找或创建索引条目
            index_entry = index.get_entry(keyword)
            if not index_entry:
                # 如果索引中没有这个关键词，创建新条目
                index_entry = IndexEntry(keyword=keyword)
                index.add_entry(keyword, index_entry)
            
            # 合并描述信息
            index_entry.description = desc_entry.description_zh or ""
            index_entry.description_en = desc_entry.description_en or ""
            index_entry.synonyms = desc_entry.synonyms
            index_entry.related = desc_entry.related
            
            # 为同义词创建索引条目（指向主关键词）
            for synonym in desc_entry.synonyms:
                synonym_lower = synonym.lower()
                if synonym_lower not in index.keywords:
                    # 创建同义词条目，复制主关键词的信息
                    synonym_entry = IndexEntry(
                        keyword=synonym_lower,
                        description=index_entry.description,
                        description_en=index_entry.description_en,
                        synonyms=[keyword],  # 指向主关键词
                        related=index_entry.related,
                        modules=index_entry.modules,
                        classes=index_entry.classes,
                        functions=index_entry.functions
                    )
                    index.add_entry(synonym_lower, synonym_entry)
            
            merged_count += 1
        
        print(f"  ✓ 合并了 {merged_count} 个描述")
        return index
    
    def _calculate_tfidf(self, index: SearchIndex):
        """
        计算 TF-IDF 权重
        
        TF-IDF = TF * IDF
        TF (Term Frequency): 关键词在文档中出现的频率
        IDF (Inverse Document Frequency): log(总文档数 / 包含该关键词的文档数)
        
        这里我们将每个代码元素（类、函数）视为一个文档
        """
        print("  计算 TF-IDF 权重...")
        
        # 统计总文档数（类 + 函数）
        total_docs = 0
        for entry in index.keywords.values():
            total_docs += len(entry.classes) + len(entry.functions)
        
        if total_docs == 0:
            print("  警告: 没有文档，跳过 TF-IDF 计算")
            return
        
        # 为每个关键词计算 TF-IDF
        for keyword, entry in index.keywords.items():
            # 文档频率（包含该关键词的文档数）
            doc_freq = len(entry.classes) + len(entry.functions)
            
            if doc_freq == 0:
                entry.tfidf_score = 0.0
                continue
            
            # IDF = log(总文档数 / 文档频率)
            idf = math.log(total_docs / doc_freq)
            
            # TF = 文档频率 / 总文档数（简化计算）
            tf = doc_freq / total_docs
            
            # TF-IDF
            entry.tfidf_score = round(tf * idf, 4)
        
        print("  ✓ TF-IDF 计算完成")
    
    def add_entry(self, keyword: str, entry: IndexEntry):
        """
        添加索引条目（外部接口）
        
        Args:
            keyword: 关键词
            entry: 索引条目
        """
        # 更新内部映射
        if entry.modules:
            self.keyword_to_modules[keyword].update(entry.modules)
        
        if entry.classes:
            for cls_loc in entry.classes:
                # 转换为 ClassInfo
                cls_info = ClassInfo(name=cls_loc.name, file=cls_loc.file, line=cls_loc.line)
                self.keyword_to_classes[keyword].append(cls_info)
        
        if entry.functions:
            for func_loc in entry.functions:
                # 转换为 FunctionInfo
                func_info = FunctionInfo(name=func_loc.name, file=func_loc.file, line=func_loc.line)
                self.keyword_to_functions[keyword].append(func_info)


if __name__ == '__main__':
    # 测试代码
    import sys
    import os
    
    # 测试基本功能
    print("=== 测试 SearchIndexBuilder ===\n")
    
    # 创建测试数据
    from module_analyzer import ModuleTree, ModuleInfo
    from cpp_parser import ClassInfo, FunctionInfo
    
    # 创建模块树
    tree = ModuleTree()
    
    # 添加测试模块
    parse_module = ModuleInfo(
        name="parse",
        path="src/Parse",
        files=["src/Parse/Lambda.cpp", "src/Parse/Lambda.h"],
        classes=[
            ClassInfo(name="LambdaExpr", file="src/Parse/Lambda.h", line=45),
            ClassInfo(name="Parser", file="src/Parse/Parser.h", line=23)
        ],
        functions=[
            FunctionInfo(name="ParseLambda", file="src/Parse/Lambda.cpp", line=100),
            FunctionInfo(name="ParseExpression", file="src/Parse/Parser.cpp", line=200)
        ]
    )
    tree.add_module(parse_module)
    
    sema_module = ModuleInfo(
        name="sema",
        path="src/Sema",
        files=["src/Sema/TypeChecker.cpp", "src/Sema/TypeChecker.h"],
        classes=[
            ClassInfo(name="TypeChecker", file="src/Sema/TypeChecker.h", line=30)
        ],
        functions=[
            FunctionInfo(name="TypeCheckLambda", file="src/Sema/TypeChecker.cpp", line=150)
        ]
    )
    tree.add_module(sema_module)
    
    # 构建索引
    builder = SearchIndexBuilder()
    index = builder.build_index(tree)
    
    print(f"\n=== 索引统计 ===")
    print(f"关键词总数: {len(index.keywords)}")
    
    # 显示部分索引条目
    print(f"\n=== 部分索引条目 ===")
    for i, (keyword, entry) in enumerate(index.keywords.items()):
        if i >= 10:  # 只显示前 10 个
            break
        print(f"\n关键词: {keyword}")
        print(f"  模块: {entry.modules}")
        print(f"  类数: {len(entry.classes)}")
        print(f"  函数数: {len(entry.functions)}")
        print(f"  TF-IDF: {entry.tfidf_score}")
    
    # 测试转换为字典
    print(f"\n=== 测试 JSON 序列化 ===")
    index_dict = index.to_dict()
    print(f"✓ 成功转换为字典，包含 {len(index_dict['keywords'])} 个关键词")
    
    # 测试合并描述
    print(f"\n=== 测试合并描述 ===")
    from markdown_parser import DescriptionEntry
    
    test_desc = DescriptionEntry(
        keyword="lambda",
        synonyms=["匿名函数", "anonymous function"],
        related=["function", "closure"],
        category="language-feature",
        concept_name="Lambda 表达式",
        description_zh="Lambda 表达式是匿名函数特性",
        description_en="Lambda expressions are anonymous function features",
        use_cases=["函数式编程", "回调函数"],
        implementation_notes="LambdaExpr 类实现",
        file_path="test.md"
    )
    
    descriptions = {"lambda": test_desc}
    index = builder.merge_descriptions(index, descriptions)
    
    lambda_entry = index.get_entry("lambda")
    if lambda_entry:
        print(f"✓ 成功合并描述")
        print(f"  中文描述: {lambda_entry.description}")
        print(f"  英文描述: {lambda_entry.description_en}")
        print(f"  同义词: {lambda_entry.synonyms}")
        print(f"  相关概念: {lambda_entry.related}")
    
    # 检查同义词索引
    synonym_entry = index.get_entry("匿名函数")
    if synonym_entry:
        print(f"✓ 同义词索引创建成功")
        print(f"  同义词 '匿名函数' 指向: {synonym_entry.synonyms}")
    
    print("\n=== 测试完成 ===")
