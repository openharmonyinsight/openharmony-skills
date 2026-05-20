#!/usr/bin/env python3
"""
SearchEngine - 搜索引擎

职责：在索引中搜索匹配的条目，返回相关结果
"""

import json
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SearchResult:
    """搜索结果"""
    keyword: str  # 匹配的关键词
    description: str  # 描述（中文）
    description_en: str  # 描述（英文）
    synonyms: List[str]  # 同义词
    related: List[str]  # 相关概念
    modules: List[str]  # 相关模块
    classes: List[Dict[str, Any]]  # 相关类
    functions: List[Dict[str, Any]]  # 相关函数
    tfidf_score: float  # TF-IDF 得分
    relevance_score: float  # 相关性得分（综合得分）
    match_type: str  # 匹配类型：'exact', 'fuzzy', 'synonym'


class SearchEngine:
    """搜索引擎"""
    
    def __init__(self, index_path: str = None):
        """
        初始化搜索引擎
        
        Args:
            index_path: 索引文件路径
        """
        self.index_path = index_path
        self.index = None
        self.cross_references = None
        
        if index_path:
            self.load_index(index_path)
    
    def load_index(self, index_path: str):
        """
        加载搜索索引到内存
        
        Args:
            index_path: 索引文件路径
        """
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"索引文件不存在: {index_path}")
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.index = data.get('keywords', {})
        except json.JSONDecodeError as e:
            raise ValueError(f"索引文件格式错误: {e}")
        
        # 尝试加载交叉引用
        cross_ref_path = os.path.join(os.path.dirname(index_path), 'cross-references.json')
        if os.path.exists(cross_ref_path):
            try:
                with open(cross_ref_path, 'r', encoding='utf-8') as f:
                    self.cross_references = json.load(f)
            except json.JSONDecodeError:
                self.cross_references = None
    
    def search(self, keywords: List[str], max_results: int = 10, 
               enable_fuzzy: bool = True) -> List[SearchResult]:
        """
        执行搜索
        
        Args:
            keywords: 关键词列表
            max_results: 最大结果数
            enable_fuzzy: 是否启用模糊匹配
            
        Returns:
            List[SearchResult]: 搜索结果列表
        """
        if not self.index:
            raise RuntimeError("索引未加载，请先调用 load_index()")
        
        if not keywords:
            return []
        
        results = []
        
        for keyword in keywords:
            # 1. 精确匹配
            exact_matches = self._exact_match(keyword)
            results.extend(exact_matches)
            
            # 2. 同义词匹配
            synonym_matches = self._synonym_match(keyword)
            results.extend(synonym_matches)
            
            # 3. 模糊匹配
            if enable_fuzzy:
                fuzzy_matches = self._fuzzy_match(keyword)
                results.extend(fuzzy_matches)
        
        # 去重（基于关键词）
        seen_keywords = set()
        unique_results = []
        for result in results:
            if result.keyword not in seen_keywords:
                seen_keywords.add(result.keyword)
                unique_results.append(result)
        
        # 按相关性得分排序
        unique_results.sort(key=lambda r: r.relevance_score, reverse=True)
        
        # 限制结果数量
        return unique_results[:max_results]
    
    def _exact_match(self, keyword: str) -> List[SearchResult]:
        """
        精确匹配
        
        Args:
            keyword: 关键词
            
        Returns:
            List[SearchResult]: 匹配结果
        """
        results = []
        keyword_lower = keyword.lower()
        
        for key, entry in self.index.items():
            if key.lower() == keyword_lower:
                result = self._create_search_result(key, entry, 'exact', 1.0)
                results.append(result)
        
        return results
    
    def _synonym_match(self, keyword: str) -> List[SearchResult]:
        """
        同义词匹配
        
        Args:
            keyword: 关键词
            
        Returns:
            List[SearchResult]: 匹配结果
        """
        results = []
        keyword_lower = keyword.lower()
        
        for key, entry in self.index.items():
            synonyms = entry.get('synonyms', [])
            for synonym in synonyms:
                if synonym.lower() == keyword_lower:
                    result = self._create_search_result(key, entry, 'synonym', 0.9)
                    results.append(result)
                    break
        
        return results
    
    def _fuzzy_match(self, keyword: str, max_distance: int = 2) -> List[SearchResult]:
        """
        模糊匹配（使用编辑距离）
        
        根据关键词长度动态调整最大编辑距离:
        - 长度 <= 5: 不进行模糊匹配（避免短关键词匹配噪音）
        - 长度 6-8: 最大编辑距离 1
        - 长度 > 8: 最大编辑距离 2
        
        同时使用长度比率过滤（min_len/max_len >= 0.75）避免长度差异过大的匹配
        
        Args:
            keyword: 关键词
            max_distance: 最大编辑距离（会根据关键词长度动态调整）
            
        Returns:
            List[SearchResult]: 匹配结果
        """
        results = []
        keyword_lower = keyword.lower()
        keyword_len = len(keyword)
        
        # 根据关键词长度动态调整最大编辑距离
        if keyword_len <= 5:
            # 短关键词不进行模糊匹配，避免噪音
            return results
        elif keyword_len <= 8:
            # 中等长度关键词，最大编辑距离为1
            adjusted_max_distance = 1
        else:
            # 长关键词，最大编辑距离为2
            adjusted_max_distance = min(max_distance, 2)
        
        # 获取所有可能的匹配
        candidates = []
        for key in self.index.keys():
            key_lower = key.lower()
            
            # 长度差异过大时跳过（优化性能）
            if abs(len(key_lower) - keyword_len) > adjusted_max_distance:
                continue
            
            # 计算相似度比率（避免长度差异过大的匹配）
            min_len = min(keyword_len, len(key_lower))
            max_len = max(keyword_len, len(key_lower))
            length_ratio = min_len / max_len if max_len > 0 else 0
            
            # 如果长度比率太低（差异太大），跳过
            if length_ratio < 0.75:
                continue
            
            distance = self._edit_distance(keyword_lower, key_lower)
            if 0 < distance <= adjusted_max_distance:
                candidates.append((key, distance))
        
        # 按编辑距离排序
        candidates.sort(key=lambda x: x[1])
        
        # 创建搜索结果
        for key, distance in candidates:
            entry = self.index[key]
            # 相关性得分：距离越小，得分越高
            relevance = 0.6 * (1.0 - distance / (adjusted_max_distance + 1))
            result = self._create_search_result(key, entry, 'fuzzy', relevance)
            results.append(result)
        
        return results
    
    def _edit_distance(self, s1: str, s2: str) -> int:
        """
        计算编辑距离（Levenshtein 距离）
        
        Args:
            s1: 字符串1
            s2: 字符串2
            
        Returns:
            int: 编辑距离
        """
        if len(s1) < len(s2):
            return self._edit_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # 插入、删除、替换的代价
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _create_search_result(self, keyword: str, entry: Dict[str, Any], 
                             match_type: str, base_relevance: float) -> SearchResult:
        """
        创建搜索结果对象
        
        Args:
            keyword: 关键词
            entry: 索引条目
            match_type: 匹配类型
            base_relevance: 基础相关性得分
            
        Returns:
            SearchResult: 搜索结果
        """
        tfidf_score = entry.get('tfidf_score', 0.0)
        
        # 综合相关性得分：基础相关性 * TF-IDF 得分
        relevance_score = base_relevance * (0.5 + 0.5 * tfidf_score)
        
        return SearchResult(
            keyword=keyword,
            description=entry.get('description', ''),
            description_en=entry.get('description_en', ''),
            synonyms=entry.get('synonyms', []),
            related=entry.get('related', []),
            modules=entry.get('modules', []),
            classes=entry.get('classes', []),
            functions=entry.get('functions', []),
            tfidf_score=tfidf_score,
            relevance_score=relevance_score,
            match_type=match_type
        )
    
    def get_module_dependencies(self, module_name: str) -> Optional[Dict[str, Any]]:
        """
        获取模块依赖关系
        
        Args:
            module_name: 模块名
            
        Returns:
            Optional[Dict[str, Any]]: 模块依赖信息
        """
        if not self.cross_references:
            return None
        
        module_deps = self.cross_references.get('module_dependencies', {})
        return module_deps.get(module_name)
    
    def get_function_calls(self, function_name: str) -> Optional[Dict[str, Any]]:
        """
        获取函数调用关系
        
        Args:
            function_name: 函数名
            
        Returns:
            Optional[Dict[str, Any]]: 函数调用信息
        """
        if not self.cross_references:
            return None
        
        function_calls = self.cross_references.get('function_calls', {})
        return function_calls.get(function_name)


def main():
    """测试函数"""
    import sys
    
    # 查找索引文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(script_dir, '..', 'knowledge-base', 'search-index.json')
    
    if not os.path.exists(index_path):
        print(f"错误: 索引文件不存在: {index_path}")
        print("请先运行 generate_knowledge.py 生成知识库")
        sys.exit(1)
    
    # 创建搜索引擎
    engine = SearchEngine(index_path)
    
    # 测试搜索
    test_keywords = [
        ['lambda'],
        ['类型推断'],
        ['TypeChecker'],
        ['模式匹配'],
    ]
    
    print("SearchEngine 测试\n" + "=" * 60)
    
    for keywords in test_keywords:
        print(f"\n搜索关键词: {keywords}")
        results = engine.search(keywords, max_results=3)
        
        if not results:
            print("  未找到结果")
        else:
            for i, result in enumerate(results, 1):
                print(f"\n  结果 {i}:")
                print(f"    关键词: {result.keyword}")
                print(f"    匹配类型: {result.match_type}")
                print(f"    相关性得分: {result.relevance_score:.3f}")
                print(f"    描述: {result.description[:50]}..." if len(result.description) > 50 else f"    描述: {result.description}")
                print(f"    模块: {', '.join(result.modules[:3])}" if result.modules else "    模块: 无")


if __name__ == '__main__':
    main()
